leakage_hybrid.py
```python
"""A v0 reimplementation of qevol + Pauli+ from public specifications.

Sources:
* Google Quantum AI (2023), arXiv:2207.06431, supplement Section XIV.
* Rosenfeld et al. (2026), arXiv:2512.13908v1, supplement Section XI.2.
* Miao et al., Nature Physics (2023), injected-leakage lifetime/removal.

Our fusion design decision, not a published fusion prescription: each shot
has one classical leakage-label trajectory shared by all stabilizer branches.
Branches differ only in their stabilizer state and complex coefficient.

Simplifications:
* CZ creation is a state-independent Bernoulli event with cz_leak_prob=pt
  by default. The Kraus channel sqrt(pt)(|02><11| + |11><02|) acts only
  on suitable quantum-state components; its published average is 0.25*pt.
  This label-only model does not inspect |11>, implement the reverse
  Kraus transition, or reproduce that average unless the caller explicitly
  supplies an averaged probability.
* Heating uses the specified |1> -> |2> hazard on every computational
  label, without conditioning on the branch's |1> population.
* Calibrated transport is represented by moving a leakage label, not by
  resolving the amplitudes of |22> <-> |13| or |21> <-> |03|.
* Measurement uses the "mixture rule for branch-random measurements;
  coherent interference on such measurements is out of scope for v0".
  Branch probabilities are |coefficient|^2-weighted tableau probabilities.
  This is not a general coherent stabilizer-rank measurement algorithm:
  interference between overlapping branches and relative phases introduced
  by tableau projection are not tracked.
* Removal boosts and clips the per-cycle seepage probability. This is a
  stand-in for DQLR-style removal at the Miao efficacy, not a fit. The boost
  applies to all labels; measure labels are additionally cleared by reset.
* Leaked-partner CZ replaces the ideal entangler by the specified Z channel.
  Single-qubit Cliffords still update the underlying computational surrogate.
  On seepage or transport back to label 0, that surrogate is retained.

This is not Google's code, is not validated at 54 qubits, and is not the
Section V experiment itself. All stochastic choices use the caller's NumPy
Generator. Stim is used only for deterministic gates, expectations, copies,
and forced projections; its internal measurement RNG is never invoked.
"""

from dataclasses import dataclass
import math

import numpy as np
import stim


@dataclass
class LeakageParams:
    """Physical parameters and controls; time units are seconds."""

    enabled: bool = True  # Prototype master switch for the no-leakage arm.
    cz_leak_prob: float = 8e-4  # Google 2023 XIV: pt, not averaged 0.25*pt.
    heating_rate: float = 1.0 / (700e-6)  # Google 2023 XIV: Gamma, s^-1.
    t_cycle: float = 896e-9  # Google 2023 XIV: default cycle duration.
    transport_prob: float = 0.1  # Brief's phenomenological Google-XIV transport.
    leaked_partner_z_prob: float = 1.0  # Google 2023 XIV: twirled CZ channel.
    lifetime_cycles: float = 4.4  # Miao 2023: injected |2> lifetime in cycles.
    readout_leak_prob: float = 0.0  # Brief: swept Arm-3 readout parameter.
    removal_boost: float = 5.0  # Brief: Miao-efficacy stand-in, not a fit.

    heating_on: bool = True  # Prototype control for Google-XIV heating.
    cz_leak_on: bool = True  # Prototype control for Google-XIV CZ creation.
    transport_on: bool = True  # Brief: transport-off control.
    readout_leak_on: bool = True  # Brief: Arm-3 readout control.
    removal_on: bool = False  # Brief: prediction-arm removal control.

    epsilon: float = 1e-4  # Rosenfeld 2026 XI.2: coefficient cutoff.
    m_max: int = 1000  # Rosenfeld 2026 XI.2: maximum branch count.

    def __post_init__(self):
        for name in (
            "cz_leak_prob", "transport_prob", "leaked_partner_z_prob",
            "readout_leak_prob",
        ):
            value = getattr(self, name)
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must be a probability")
        for name in ("heating_rate", "t_cycle", "removal_boost"):
            value = getattr(self, name)
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if not math.isfinite(self.lifetime_cycles) or self.lifetime_cycles <= 0:
            raise ValueError("lifetime_cycles must be finite and positive")
        if not math.isfinite(self.epsilon) or not 0 <= self.epsilon < 1:
            raise ValueError("epsilon must be in [0, 1)")
        if not isinstance(self.m_max, int) or self.m_max < 1:
            raise ValueError("m_max must be a positive integer")

    @property
    def p_heat(self):
        return -math.expm1(-self.heating_rate * self.t_cycle)

    @property
    def p_seep(self):
        p = -math.expm1(-1.0 / self.lifetime_cycles)
        if self.removal_on:
            p *= self.removal_boost
        return min(1.0, p)


class LeakageEngine:
    """One shared leakage environment.

    ``cz`` returns the computational qubits requiring a Z error. The caller
    applies those errors identically to every branch. Label transitions and
    Z draws use labels at entry to the CZ, so a transported label cannot
    immediately undergo another transition in the same gate.
    """

    def __init__(self, n_qubits, params, rng):
        if not isinstance(n_qubits, int) or n_qubits < 1:
            raise ValueError("n_qubits must be a positive integer")
        if not isinstance(rng, np.random.Generator):
            raise TypeError("rng must be a numpy.random.Generator")
        self.labels = np.zeros(n_qubits, dtype=np.int8)
        self.params = params
        self.rng = rng

    def _check(self, i):
        if not isinstance(i, (int, np.integer)) or not 0 <= i < len(self.labels):
            raise IndexError("qubit index out of range")

    def heat(self, n_qubits):
        """Apply one cycle's unconditional heating hazard to the first n qubits."""
        if not isinstance(n_qubits, int) or not 0 <= n_qubits <= len(self.labels):
            raise ValueError("n_qubits exceeds the allocated register")
        p = self.params
        if not p.enabled or not p.heating_on:
            return
        candidates = np.flatnonzero(self.labels[:n_qubits] == 0)
        selected = self.rng.random(len(candidates)) < p.p_heat
        self.labels[candidates[selected]] = 2

    def cz(self, i, j, higher_freq):
        """Update labels and return a tuple of shared Z-error targets.

        Creation occurs only if both entry labels are computational, and only
        the explicitly identified higher-frequency qubit can acquire label 2.
        Transport preserves the moving label, including label 3.
        """
        self._check(i)
        self._check(j)
        if i == j or higher_freq not in (i, j):
            raise ValueError("CZ needs distinct qubits and a member higher_freq")
        p = self.params
        if not p.enabled:
            return ()

        li, lj = int(self.labels[i]), int(self.labels[j])
        if li == 0 and lj == 0:
            if p.cz_leak_on and self.rng.random() < p.cz_leak_prob:
                self.labels[higher_freq] = 2
            return ()
        if li != 0 and lj != 0:
            return ()

        leaked, partner = (i, j) if li else (j, i)
        errors = ()
        if self.rng.random() < p.leaked_partner_z_prob:
            errors = (partner,)
        if p.transport_on and self.rng.random() < p.transport_prob:
            self.labels[partner] = self.labels[leaked]
            self.labels[leaked] = 0
        return errors

    def measure(self, i) -> None:
        """Post-measurement readout-induced leakage; does not produce a bit."""
        self._check(i)
        p = self.params
        if (
            p.enabled and p.readout_leak_on and self.labels[i] == 0
            and self.rng.random() < p.readout_leak_prob
        ):
            self.labels[i] = 2

    def reset(self, i):
        """Ideal label reset, independent of removal_on (Google 2023 XIV)."""
        self._check(i)
        if self.params.enabled:
            self.labels[i] = 0

    def seep_cycle(self):
        """One simultaneous step: 3 -> 2 or 2 -> 0, never both in one cycle."""
        if not self.params.enabled:
            return
        candidates = np.flatnonzero(self.labels != 0)
        selected = candidates[
            self.rng.random(len(candidates)) < self.params.p_seep
        ]
        old = self.labels[selected].copy()
        self.labels[selected] = np.where(old == 3, 2, 0)

    def is_leaked(self, i):
        self._check(i)
        return bool(self.params.enabled and self.labels[i] != 0)


@dataclass
class Branch:
    tableau: stim.TableauSimulator
    coefficient: complex


class HybridSimulator:
    """Small qevol-style branch engine with a shared leakage trajectory.

    Coefficients are normalized in the mixture norm sum(|c|^2)=1.
    Measurement implements the mixture rule for branch-random measurements;
    coherent interference on such measurements is out of scope for v0.

    ``reset_after_measure`` is explicit: the caller declares a measure qubit
    by invoking it, rather than by registering a separate set of roles.
    """

    def __init__(self, n_qubits, params, rng):
        self.engine = LeakageEngine(n_qubits, params, rng)
        self.n_qubits = n_qubits
        self.params = params
        self.rng = rng
        # Stim requires a seed, but no stochastic Stim operation is used.
        tableau = stim.TableauSimulator(
            seed=int(rng.integers(0, np.iinfo(np.int64).max))
        )
        tableau.set_num_qubits(n_qubits)
        self.branches = [Branch(tableau, 1.0 + 0j)]

    @property
    def labels(self):
        """Live label array; direct mutation is useful for injection studies."""
        return self.engine.labels

    def branch_count(self):
        return len(self.branches)

    def _prune(self):
        kept = [
            branch for branch in self.branches
            if abs(branch.coefficient) >= self.params.epsilon
        ]
        # Stable sorting makes equal-weight truncation deterministic.
        kept.sort(key=lambda branch: -abs(branch.coefficient))
        kept = kept[:self.params.m_max]
        norm = math.sqrt(sum(abs(b.coefficient) ** 2 for b in kept))
        if norm == 0:
            raise RuntimeError("branch cutoff removed all probability mass")
        for branch in kept:
            branch.coefficient /= norm
        self.branches = kept

    def inject_magic_state(self, qubit):
        """Prepare a fresh |T> on qubit using |0>, |1> stabilizer branches.

        The target must be computational and deterministically |0> in every
        existing branch. On a fresh simulator this creates exactly two
        branches and preserves the other qubits. Further injections multiply
        the branch count, subject to epsilon and m_max truncation.
        """
        self.engine._check(qubit)
        if self.engine.is_leaked(qubit):
            raise ValueError("cannot inject into a leaked qubit")
        if any(b.tableau.peek_z(qubit) != 1 for b in self.branches):
            raise ValueError("magic-state injection requires a fresh |0> target")
        new = []
        phase = complex(np.exp(1j * np.pi / 4))  # Brief: cultivated |T> phase.
        scale = math.sqrt(0.5)  # Brief: normalized |T> decomposition.
        for branch in self.branches:
            zero = branch.tableau.copy()
            one = branch.tableau.copy()
            one.x(qubit)
            new.append(Branch(zero, branch.coefficient * scale))
            new.append(Branch(one, branch.coefficient * scale * phase))
        self.branches = new
        self._prune()

    def _single(self, gate, qubit):
        self.engine._check(qubit)
        for branch in self.branches:
            getattr(branch.tableau, gate)(qubit)

    def x(self, qubit):
        self._single("x", qubit)

    def y(self, qubit):
        self._single("y", qubit)

    def z(self, qubit):
        self._single("z", qubit)

    def h(self, qubit):
        self._single("h", qubit)

    def s(self, qubit):
        self._single("s", qubit)

    def cz(self, i, j, higher_freq):
        """Ideal CZ for computational entry labels, otherwise leaked CZ."""
        self.engine._check(i)
        self.engine._check(j)
        if i == j or higher_freq not in (i, j):
            raise ValueError("CZ needs distinct qubits and a member higher_freq")
        computational = not (
            self.engine.is_leaked(i) or self.engine.is_leaked(j)
        )
        errors = self.engine.cz(i, j, higher_freq)
        if computational:
            for branch in self.branches:
                branch.tableau.cz(i, j)
        for target in errors:
            self.z(target)

    def cx(self, control, target, higher_freq=None):
        """H-CZ-H implementation, with target higher-frequency unless specified."""
        self.engine._check(control)
        self.engine._check(target)
        higher_freq = target if higher_freq is None else higher_freq
        if control == target or higher_freq not in (control, target):
            raise ValueError("invalid CX pair or higher_freq")
        self.h(target)
        self.cz(control, target, higher_freq)
        self.h(target)

    def depolarize(self, qubit, p):
        """SI1000-style hook: independent per-branch Pauli, total probability p."""
        self.engine._check(qubit)
        if not math.isfinite(p) or not 0 <= p <= 1:
            raise ValueError("p must be a probability")
        if p == 0:
            return
        for branch in self.branches:
            if self.rng.random() < p:
                gate = ("x", "y", "z")[int(self.rng.integers(3))]
                getattr(branch.tableau, gate)(qubit)

    def _project_mixture(self, qubit):
        """Sample Z and force each surviving tableau onto the same outcome."""
        expectations = np.array(
            [b.tableau.peek_z(qubit) for b in self.branches], dtype=float
        )
        p_one = (1.0 - expectations) * 0.5
        weights = np.array(
            [abs(b.coefficient) ** 2 for b in self.branches], dtype=float
        )
        weights /= weights.sum()
        total_one = float(np.clip(weights @ p_one, 0.0, 1.0))
        outcome = int(self.rng.random() < total_one)
        likelihoods = p_one if outcome else 1.0 - p_one
        surviving = []
        for branch, likelihood in zip(self.branches, likelihoods):
            if likelihood == 0:
                continue
            branch.tableau.postselect_z(qubit, desired_value=bool(outcome))
            branch.coefficient *= math.sqrt(float(likelihood))
            surviving.append(branch)
        self.branches = surviving
        # Normalize before applying the coefficient cutoff.
        norm = math.sqrt(sum(abs(b.coefficient) ** 2 for b in surviving))
        for branch in surviving:
            branch.coefficient /= norm
        self._prune()
        return outcome

    def measure(self, qubit) -> int:
        """Measure Z, with fair leaked readout and post-readout leakage."""
        self.engine._check(qubit)
        if self.engine.is_leaked(qubit):
            # Google 2023 XIV: unresolved |2>, |3> map to 50/50 readout.
            return int(self.rng.integers(2))
        outcome = self._project_mixture(qubit)
        self.engine.measure(qubit)
        return outcome

    def reset_after_measure(self, qubit):
        """Reset a caller-designated measure qubit to label 0 and surrogate |0>.

        If leaked readout left the surrogate unmeasured, an unreported mixture
        measurement implements the trace-and-prepare trajectory. This operation
        uses NumPy randomness and deterministic Stim projections, not Stim reset.
        It can also be used as a standalone physical reset.
        """
        self.engine._check(qubit)
        outcome = self._project_mixture(qubit)
        if outcome:
            self.x(qubit)
        self.engine.reset(qubit)


def run_repetition_memory(
    n_data, n_cycles, params, shots, seed, postselect_first_cycle=False
) -> dict:
    """Run a miniature repetition memory, not a calibrated device prediction.

    There is one measure qubit for each neighboring data pair. Each cycle:
    heat all qubits; prepare each measure qubit in |+>; apply two CZs with
    the data qubits designated higher-frequency; H/measure/reset the measure
    qubit; then seep all labels once. Data start in |0> and are not reset.

    Detection events compare each check with its previous reported outcome,
    initially zero. Population is sampled after seepage and includes data
    and measure qubits. Both reported per-cycle observables average only over
    kept shots. If no shots survive, both lists contain NaN.
    """
    for name, value, minimum in (
        ("n_data", n_data, 2), ("n_cycles", n_cycles, 1), ("shots", shots, 1)
    ):
        if not isinstance(value, int) or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}")
    rng = np.random.default_rng(seed)
    n_checks = n_data - 1
    n_qubits = n_data + n_checks
    detections = np.zeros(n_cycles, dtype=float)
    populations = np.zeros(n_cycles, dtype=float)
    kept = 0

    for _ in range(shots):
        sim = HybridSimulator(n_qubits, params, rng)
        previous = np.zeros(n_checks, dtype=np.int8)
        shot_detections = np.empty(n_cycles, dtype=float)
        shot_populations = np.empty(n_cycles, dtype=float)
        keep = True
        for cycle in range(n_cycles):
            sim.engine.heat(n_qubits)
            outcomes = np.empty(n_checks, dtype=np.int8)
            for check in range(n_checks):
                ancilla = n_data + check
                sim.h(ancilla)
                sim.cz(check, ancilla, higher_freq=check)
                sim.cz(check + 1, ancilla, higher_freq=check + 1)
                sim.h(ancilla)
                outcomes[check] = sim.measure(ancilla)
                sim.reset_after_measure(ancilla)
            events = outcomes != previous
            shot_detections[cycle] = float(events.mean())
            previous = outcomes
            if cycle == 0 and postselect_first_cycle and events.any():
                keep = False
            sim.engine.seep_cycle()
            shot_populations[cycle] = float(np.mean(sim.labels != 0))
        # Complete discarded shots too, so postselection does not change draws.
        if keep:
            kept += 1
            detections += shot_detections
            populations += shot_populations

    if kept:
        detections /= kept
        populations /= kept
    else:
        detections.fill(np.nan)
        populations.fill(np.nan)
    return {
        "detection_fraction_per_cycle": detections.tolist(),
        "keep_rate": kept / shots,
        "mean_label_population": populations.tolist(),
    }
```

test_leakage_hybrid.py
```python
"""Seeded tests of the prototype rules, not device-level validation."""

from dataclasses import replace
import math

import numpy as np
import pytest

from leakage_hybrid import (
    HybridSimulator,
    LeakageEngine,
    LeakageParams,
    run_repetition_memory,
)


def test_disabled_null_check():
    params = LeakageParams(enabled=False)
    engine = LeakageEngine(12, params, np.random.default_rng(100))
    state_before = engine.rng.bit_generator.state
    for _ in range(200):
        engine.heat(12)
        engine.cz(0, 1, higher_freq=0)
        engine.measure(0)
        engine.reset(0)
        engine.seep_cycle()
    assert np.all(engine.labels == 0)
    assert engine.rng.bit_generator.state == state_before

    result = run_repetition_memory(3, 20, params, 80, seed=101)
    fractions = result["detection_fraction_per_cycle"]
    assert fractions[-1] <= fractions[0] + 0.05
    assert fractions == [0.0] * 20
    assert result["mean_label_population"] == [0.0] * 20
    assert result["keep_rate"] == 1.0


@pytest.mark.parametrize("label", [2, 3])
def test_leaked_measurement_map(label):
    sim = HybridSimulator(1, LeakageParams(), np.random.default_rng(200 + label))
    sim.h(0)
    sim.labels[0] = label
    before = sim.branches[0].tableau.current_inverse_tableau()
    bits = [sim.measure(0) for _ in range(20000)]
    assert abs(np.mean(bits) - 0.5) < 0.02
    assert sim.labels[0] == label
    assert sim.branches[0].tableau.current_inverse_tableau() == before


@pytest.mark.parametrize("label", [2, 3])
def test_reset_rule(label):
    engine = LeakageEngine(2, LeakageParams(), np.random.default_rng(300))
    engine.labels[0] = label
    engine.reset(0)
    assert not engine.is_leaked(0)

    sim = HybridSimulator(1, LeakageParams(), np.random.default_rng(301))
    sim.x(0)
    sim.labels[0] = label
    sim.reset_after_measure(0)
    assert sim.labels[0] == 0
    assert sim.branches[0].tableau.peek_z(0) == 1


def test_heating_seepage_steady_state():
    params = LeakageParams(cz_leak_on=False, transport_on=False)
    engine = LeakageEngine(4096, params, np.random.default_rng(400))
    populations = []
    for cycle in range(1800):
        engine.heat(4096)
        engine.seep_cycle()
        if cycle >= 300:
            populations.append(np.mean(engine.labels != 0))
    estimate = params.p_heat / (params.p_heat + params.p_seep)
    measured = np.mean(populations)
    # Sequential heat/seep has a slightly different discrete-time fixed point.
    assert 0.5 * estimate <= measured <= 2.0 * estimate


@pytest.mark.parametrize("label", [2, 3])
def test_transport_off_and_on(label):
    params = LeakageParams(
        heating_on=False, cz_leak_on=False,
        transport_on=False, transport_prob=1.0,
        # Brief's transport control, forced to its deterministic endpoint.
    )
    off = LeakageEngine(2, params, np.random.default_rng(500))
    off.labels[0] = label
    for _ in range(100):
        off.cz(0, 1, higher_freq=0)
        assert off.labels.tolist() == [label, 0]

    on = LeakageEngine(
        2, replace(params, transport_on=True), np.random.default_rng(501)
    )
    on.labels[0] = label
    for step in range(100):
        errors = on.cz(0, 1, higher_freq=0)
        expected = [0, label] if step % 2 == 0 else [label, 0]
        assert on.labels.tolist() == expected
        assert errors == ((1,) if step % 2 == 0 else (0,))


def test_magic_state_and_z_measurement():
    rng = np.random.default_rng(600)
    params = LeakageParams(enabled=False)
    sim = HybridSimulator(1, params, rng)
    sim.inject_magic_state(0)
    assert sim.branch_count() == 2
    coefficients = [branch.coefficient for branch in sim.branches]
    assert np.allclose(np.abs(coefficients), 1 / math.sqrt(2))
    assert np.allclose(coefficients[1] / coefficients[0], np.exp(1j * np.pi / 4))
    assert [b.tableau.peek_z(0) for b in sim.branches] == [1, -1]

    ones = 0
    for _ in range(4000):
        trial = HybridSimulator(1, params, rng)
        trial.inject_magic_state(0)
        outcome = trial.measure(0)
        ones += outcome
        assert trial.branch_count() == 1
        assert trial.branches[0].tableau.peek_z(0) == 1 - 2 * outcome
        assert trial.measure(0) == outcome
    assert abs(ones / 4000 - 0.5) < 0.04


def test_random_branch_projection_rule():
    sim = HybridSimulator(
        1, LeakageParams(enabled=False), np.random.default_rng(610)
    )
    sim.inject_magic_state(0)
    sim.h(0)
    outcome = sim.measure(0)
    assert sim.branch_count() == 2
    for branch in sim.branches:
        assert branch.tableau.peek_z(0) == 1 - 2 * outcome
        assert np.isclose(abs(branch.coefficient), 1 / math.sqrt(2))


def demo_params():
    """Accelerated, intentionally uncalibrated signal for a short test."""
    return LeakageParams(
        t_cycle=35e-6,  # Test sweep of Google-XIV heating exposure.
        lifetime_cycles=80.0,  # Test sweep of the Miao lifetime parameter.
        leaked_partner_z_prob=0.5,  # Test sweep of Google-XIV partner-Z channel.
        cz_leak_on=False,
        transport_on=False,
    )


@pytest.fixture(scope="module")
def demo_memory():
    params = demo_params()
    on = run_repetition_memory(3, 20, params, 500, seed=700)
    off = run_repetition_memory(
        3, 20, replace(params, enabled=False), 500, seed=700
    )
    selected_on = run_repetition_memory(
        3, 20, params, 500, seed=700, postselect_first_cycle=True
    )
    selected_off = run_repetition_memory(
        3, 20, replace(params, enabled=False), 500, seed=700,
        postselect_first_cycle=True,
    )
    return on, off, selected_on, selected_off


def test_leakage_rises(demo_memory):
    on, off, _, _ = demo_memory
    detection = on["detection_fraction_per_cycle"]
    assert detection[-1] >= detection[0] + 0.01
    population = on["mean_label_population"]
    assert population[-1] > population[0]
    assert off["detection_fraction_per_cycle"] == [0.0] * 20


def test_postselection(demo_memory):
    _, _, on, off = demo_memory
    assert 0 < on["keep_rate"] <= 1
    assert on["keep_rate"] < off["keep_rate"]
    assert off["keep_rate"] == 1
    assert on["detection_fraction_per_cycle"][0] == 0


def test_readout_leakage_hook_and_explicit_reset():
    params = LeakageParams(
        readout_leak_prob=1.0,  # Brief's Arm-3 parameter at a test endpoint.
    )
    sim = HybridSimulator(1, params, np.random.default_rng(800))
    assert sim.measure(0) == 0
    assert sim.labels[0] == 2
    sim.reset_after_measure(0)
    assert sim.labels[0] == 0
    assert sim.branches[0].tableau.peek_z(0) == 1


def test_creation_higher_frequency_and_removal_cascade():
    params = LeakageParams(
        cz_leak_prob=1.0,  # Google-XIV creation parameter at a test endpoint.
        removal_on=True,
        removal_boost=100.0,  # Brief's removal multiplier, forced to clipping.
    )
    engine = LeakageEngine(2, params, np.random.default_rng(900))
    engine.cz(0, 1, higher_freq=1)
    assert engine.labels.tolist() == [0, 2]
    engine.labels[:] = [3, 2]
    engine.seep_cycle()
    assert engine.labels.tolist() == [2, 0]
    engine.seep_cycle()
    assert engine.labels.tolist() == [0, 0]


def test_seeded_reproducibility():
    params = demo_params()
    first = run_repetition_memory(3, 5, params, 20, seed=1000)
    second = run_repetition_memory(3, 5, params, 20, seed=1000)
    assert first == second
```
