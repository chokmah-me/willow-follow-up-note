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
    # Labels stay off (the null check proper); the baseline Pauli noise
    # added 2026-10-17 makes detections nonzero but flat, not rising.
    assert fractions[-1] <= fractions[0] + 0.05
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
    off_detection = off["detection_fraction_per_cycle"]
    assert off_detection[-1] <= off_detection[0] + 0.05


def test_postselection(demo_memory):
    _, _, on, off = demo_memory
    assert 0 < on["keep_rate"] <= 1
    assert on["keep_rate"] < off["keep_rate"]
    assert 0 < off["keep_rate"] <= 1
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


# --- Added 2026-10-17 by the contract check (breaker WEAKENS 1-3). ---

def test_leaked_cz_skips_entangler_and_applies_partner_z():
    """Criterion: CZ with a leaked partner (2023 SI Sec. XIV). The ideal
    entangler is NOT applied; the partner gets the twirled Z instead.
    Added after mutation M1 (apply ideal CZ anyway, drop the Z) passed
    the original suite 15/15: the blindness sat on the mechanism behind
    the S24 covariance signature."""
    import stim
    params = LeakageParams(transport_on=False)  # label must stay put
    sim = HybridSimulator(2, params, np.random.default_rng(1100))
    sim.h(0)
    sim.h(1)
    sim.labels[0] = 2
    sim.cz(0, 1, higher_freq=1)
    assert sim.labels.tolist() == [2, 0]
    ref = stim.TableauSimulator(seed=1)
    ref.set_num_qubits(2)
    ref.h(0)
    ref.h(1)
    ref.z(1)  # partner Z, and no CZ anywhere
    assert (
        sim.branches[0].tableau.current_inverse_tableau()
        == ref.current_inverse_tableau()
    )


def test_surviving_branch_coefficients_stay_equal():
    """Invariant behind the reweight adjudication (breaker WEAKENS 3):
    branches stay Pauli-related in this engine, so after any measurement
    the surviving coefficients share one magnitude. Mutation M2 (drop the
    sqrt-likelihood reweight) is therefore unobservable in v0; this test
    pins the invariant that makes it harmless. If a future change breaks
    the invariant, the reweight becomes load-bearing and M2 turns real."""
    rng = np.random.default_rng(1200)
    for trial in range(60):
        sim = HybridSimulator(
            3, LeakageParams(enabled=False), np.random.default_rng(1300 + trial)
        )
        injected = set()
        for _ in range(12):
            op = int(rng.integers(5))
            q = int(rng.integers(3))
            if op == 0:
                getattr(sim, ["x", "y", "z", "h", "s"][int(rng.integers(5))])(q)
            elif op == 1:
                a, b = int(rng.integers(3)), int(rng.integers(3))
                if a != b:
                    sim.cx(a, b)
            elif op == 2:
                sim.depolarize(q, 0.4)
            elif op == 3 and q not in injected:
                try:
                    sim.inject_magic_state(q)
                    injected.add(q)
                except ValueError:
                    pass
            else:
                sim.measure(q)
                mags = [abs(b.coefficient) for b in sim.branches]
                assert max(mags) - min(mags) < 1e-9


def test_m_max_truncation_tripwire():
    """TRIPWIRE (breaker WEAKENS 1, pinned 2026-10-17): truncation at
    m_max is currently SILENT. Past the cap, branches are dropped and
    the survivors renormalized with no counter, flag, or warning, so a
    caller past the rank budget gets a wrong answer that looks right.
    This test pins the current behavior; it may change once adjudicated
    for v1. Recommendation on file: expose cumulative dropped mass."""
    params = LeakageParams(m_max=8)
    sim = HybridSimulator(4, params, np.random.default_rng(1400))
    for q in range(4):
        sim.inject_magic_state(q)
    assert sim.branch_count() == 8
    assert abs(sum(abs(b.coefficient) ** 2 for b in sim.branches) - 1.0) < 1e-9
