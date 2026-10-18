graft_circuit.py
```python
"""Generated surface-code memory circuits for the grafted-memory stand-in.

This is the standard SI1000-style mapping used for generated circuits.
Setting every noise knob to one p simplifies the paper's weighted SI1000
model; it is not a calibrated reproduction of that model.

The cultivation and grafting stages are abstracted as a post-selected logical
preparation. The simulated object is the grafted memory stage, where
Rosenfeld et al. (2026), arXiv:2512.13908v1, supplement S22-S24 live.
The actual preparation implemented here is Stim's logical-Z preparation,
not a simulation of cultivation or of its acceptance probability.

Design source: Section V simulation design, 2026-10-16.
Our stand-ins: equal noise-knob probabilities and a role-based frequency
ordering. The frequency ordering is not a device-frequency calibration.

Stim's generated qubit indices contain gaps. We densely relabel occupied
indices, preserving coordinates, operations, measurement records and repeat
blocks. Consequently distance 3 uses an allocated register of 17 qubits,
rather than a register whose size includes unused index positions.
"""

import math
from numbers import Integral, Real

import stim

from leakage_hybrid import LeakageParams  # Shared physical-model API.


def _occupied_qubits(circuit):
    """Find physical targets, excluding measurement-record references."""
    return {
        target.value
        for instruction in circuit.flattened()
        for target in instruction.targets_copy()
        if target.is_qubit_target
    }


def _relabel(circuit, mapping):
    """Relabel physical targets without changing record-relative references."""
    result = stim.Circuit()
    for instruction in circuit:
        if isinstance(instruction, stim.CircuitRepeatBlock):
            result.append(
                stim.CircuitRepeatBlock(
                    instruction.repeat_count,
                    _relabel(instruction.body_copy(), mapping),
                )
            )
            continue
        targets = []
        for target in instruction.targets_copy():
            if target.is_qubit_target:
                index = mapping[target.value]
                targets.append(
                    stim.target_inv(index) if target.is_inverted_result_target
                    else index
                )
            else:
                targets.append(target)
        result.append(
            instruction.name, targets, instruction.gate_args_copy()
        )
    return result


def build_memory_circuit(distance: int, rounds: int, p: float) -> stim.Circuit:
    """Build a densely indexed rotated logical-Z memory circuit.

    distance and rounds are experiment controls from the Section V design.
    The common probability p is our equal-knob SI1000-style stand-in.
    """
    if (
        isinstance(distance, bool)
        or not isinstance(distance, Integral)
        or distance < 3
        or distance % 2 == 0
    ):
        raise ValueError("distance must be an odd integer >= 3")
    if (
        isinstance(rounds, bool)
        or not isinstance(rounds, Integral)
        or rounds < 1
    ):
        raise ValueError("rounds must be an integer >= 1")
    if not isinstance(p, Real) or not math.isfinite(p) or not 0 <= p <= 0.1:
        raise ValueError("p must be finite and in [0, 0.1]")

    generated = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=int(distance),
        rounds=int(rounds),
        # Our stand-in: one probability for all generated SI1000-style knobs.
        after_clifford_depolarization=float(p),
        before_round_data_depolarization=float(p),
        before_measure_flip_probability=float(p),
        after_reset_flip_probability=float(p),
    )
    mapping = {
        old: new for new, old in enumerate(sorted(_occupied_qubits(generated)))
    }
    return _relabel(generated, mapping)


def circuit_metadata(circuit) -> dict:
    """Return Stim register dimensions, not inferred construction parameters."""
    return {
        "n_qubits": circuit.num_qubits,
        "n_detectors": circuit.num_detectors,
        "n_observables": circuit.num_observables,
    }


def role_map(circuit) -> dict:
    """Classify occupied physical qubits by whether they ever undergo MR.

    Unused gaps in a bare Stim circuit's index space are not physical qubits.
    Circuits returned by build_memory_circuit have no such gaps.
    """
    flat = circuit.flattened()
    occupied = _occupied_qubits(flat)
    measure = {
        target.value
        for instruction in flat
        if instruction.name == "MR"
        for target in instruction.targets_copy()
        if target.is_qubit_target
    }
    return {"data": sorted(occupied - measure), "measure": sorted(measure)}


def higher_frequency(i: int, j: int, roles: dict) -> int:
    """Our stand-in: measure beats data; within a role, larger index wins.

    The device grid places the roles at different frequencies, but this
    deterministic ordering is not a frequency map extracted from the paper.
    """
    data, measure = set(roles["data"]), set(roles["measure"])
    if data & measure:
        raise ValueError("data and measure roles must be disjoint")
    if i not in data | measure or j not in data | measure:
        raise ValueError("both qubits must have a role")
    return max((i, j), key=lambda q: (q in measure, q))
```

hybrid_runner.py
```python
"""Shot-by-shot Stim interpreter using the unchanged v0 hybrid engine.

Source: Section V simulation design, 2026-10-16. Noise is sampled separately
per stabilizer branch; leakage labels are shared across branches, as in v0.
This inherits v0's surrogate-state and mixture-measurement approximations.
It is not a decoder, a calibrated device prediction, or a simulation of
cultivation. Observable results are raw annotated measurement parities.

Timing caveat in the requested contract:
The design identifies every TICK with a round boundary: heat, seep, then
sample population. Under that convention population index 0 is after
round 1, aligned with the first detector-time group. However, actual Stim
generated surface-code circuits have multiple TICKs per syndrome round,
including a TICK after initialization, and a terminal detector-time group
for final data readout. Thus that claimed alignment does NOT hold for
these generated circuits.

This implementation follows the explicit every-TICK execution rule without
silently deleting TICKs or inventing a resampling prescription. Consequently
mean_label_population_per_round contains one entry per TICK, while
detection_fraction_per_round contains one entry per distinct detector time.
Their lengths generally differ. A physically round-aligned population API
requires revising either that rule or the circuit-generation contract.
"""

import math
from numbers import Integral

import numpy as np

from graft_circuit import higher_frequency, role_map
from leakage_hybrid import HybridSimulator


def _compile(circuit):
    """Validate once and prepare targets without altering execution order."""
    flat = circuit.flattened()
    roles = role_map(flat)
    # Our implementation: compact sparse input registers, excluding index holes
    # from leakage heating and from the physical population denominator.
    occupied = sorted(roles["data"] + roles["measure"])
    mapping = {q: k for k, q in enumerate(occupied)}
    if not occupied:
        raise ValueError("circuit must contain at least one physical qubit")

    supported = {
        "H", "X", "Y", "Z", "S", "CX", "CZ", "R", "M", "MR", "TICK",
        "DEPOLARIZE1", "DEPOLARIZE2", "X_ERROR", "Y_ERROR", "Z_ERROR",
        "DETECTOR", "OBSERVABLE_INCLUDE", "SHIFT_COORDS", "QUBIT_COORDS",
    }
    noise = {
        "DEPOLARIZE1", "DEPOLARIZE2", "X_ERROR", "Y_ERROR", "Z_ERROR"
    }
    coordinates = flat.get_detector_coordinates()
    detector_times = []
    operations = []
    measurements = 0
    ticks = 0

    for instruction in flat:
        name = instruction.name
        if name not in supported:
            raise ValueError(f"unsupported instruction: {name}")
        targets = instruction.targets_copy()
        args = instruction.gate_args_copy()

        if name in ("SHIFT_COORDS", "QUBIT_COORDS"):
            continue
        if name == "TICK":
            operations.append((name, (), None))
            ticks += 1
            continue
        if name in ("DETECTOR", "OBSERVABLE_INCLUDE"):
            offsets = []
            for target in targets:
                if (
                    not target.is_measurement_record_target
                    or not -measurements <= target.value < 0
                ):
                    raise ValueError(f"{name}: invalid measurement reference")
                offsets.append(target.value)
            if name == "DETECTOR":
                index = len(detector_times)
                coords = coordinates.get(index, ())
                # Design: detector time is coordinate 2, not instruction order.
                if len(coords) < 3 or not math.isfinite(coords[2]):
                    raise ValueError(
                        f"DETECTOR {index} requires a finite time coordinate"
                    )
                detector_times.append(coords[2])
            else:
                if (
                    len(args) != 1
                    or not math.isfinite(args[0])
                    or args[0] < 0
                    or args[0] != int(args[0])
                ):
                    raise ValueError("OBSERVABLE_INCLUDE: invalid index")
                index = int(args[0])
            operations.append((name, tuple(offsets), index))
            continue

        if any(not target.is_qubit_target for target in targets):
            raise ValueError(f"{name}: only physical qubit targets supported")
        if name not in ("M", "MR") and any(
            target.is_inverted_result_target for target in targets
        ):
            raise ValueError(f"{name}: inverted targets are unsupported")

        qubits = tuple(mapping[target.value] for target in targets)
        if name in ("CX", "CZ", "DEPOLARIZE2"):
            if len(qubits) % 2:
                raise ValueError(f"{name}: requires pairs of targets")
            if any(a == b for a, b in zip(qubits[::2], qubits[1::2])):
                raise ValueError(f"{name}: pair targets must be distinct")

        if name in noise:
            if (
                len(args) != 1
                or not math.isfinite(args[0])
                or not 0 <= args[0] <= 1
            ):
                raise ValueError(f"{name}: requires a probability in [0, 1]")
            operations.append((name, qubits, float(args[0])))
        elif name in ("CX", "CZ"):
            pairs = []
            for k in range(0, len(targets), 2):
                a, b = targets[k].value, targets[k + 1].value
                high = mapping[higher_frequency(a, b, roles)]
                pairs.append((mapping[a], mapping[b], high))
            operations.append((name, tuple(pairs), None))
        elif name in ("M", "MR"):
            # Generated circuits have no measurement-argument noise. Reject it
            # instead of silently ignoring an extra physical error channel.
            if any(arg != 0 for arg in args):
                raise ValueError(f"{name}: measurement-argument noise unsupported")
            inverted = tuple(t.is_inverted_result_target for t in targets)
            operations.append((name, qubits, inverted))
            measurements += len(qubits)
        else:
            operations.append((name, qubits, None))

    times = sorted(set(detector_times))
    groups = [
        np.flatnonzero(np.asarray(detector_times) == time) for time in times
    ]
    return flat, operations, len(occupied), groups, ticks


def _noise(sim, name, targets, probability):
    """Apply instruction probabilities, independently per branch."""
    if probability == 0:
        return
    if name == "DEPOLARIZE1":
        for qubit in targets:
            sim.depolarize(qubit, probability)
        return
    if name == "DEPOLARIZE2":
        # Design: uniform distribution over the 15 nonidentity Pauli pairs.
        paulis = (None, "x", "y", "z")
        for a, b in zip(targets[::2], targets[1::2]):
            for branch in sim.branches:
                if sim.rng.random() < probability:
                    code = int(sim.rng.integers(1, 16))
                    for qubit, digit in ((a, code // 4), (b, code % 4)):
                        if digit:
                            getattr(branch.tableau, paulis[digit])(qubit)
        return
    gate = name[0].lower()
    for qubit in targets:
        for branch in sim.branches:
            if sim.rng.random() < probability:
                getattr(branch.tableau, gate)(qubit)


def _parity(record, offsets):
    """Evaluate record-relative references at the current instruction."""
    result = False
    for offset in offsets:
        result ^= bool(record[offset])
    return result


def run_circuit(circuit, params, shots: int, seed: int,
                postselect_first_round: bool = False) -> dict:
    """Execute complete shots, excluding rejected shots only from statistics.

    params carries the v0 physical parameters and controls. shots, seed and
    first-round postselection are controls from the Section V design.
    All randomness comes from one caller-seeded NumPy Generator, including
    all draws made by the hybrid engine.

    Detector rounds are sorted distinct third coordinates. Missing time
    coordinates raise ValueError. Population boundaries follow every TICK;
    see the module docstring for the generated-circuit timing incompatibility.
    Empty retained ensembles produce correctly shaped arrays and NaN means.
    """
    if (
        isinstance(shots, bool)
        or not isinstance(shots, Integral)
        or shots < 1
    ):
        raise ValueError("shots must be an integer >= 1")
    shots = int(shots)
    flat, operations, n_qubits, groups, n_ticks = _compile(circuit)
    rng = np.random.default_rng(seed)
    detectors = np.zeros((shots, flat.num_detectors), dtype=np.bool_)
    observables = np.zeros((shots, flat.num_observables), dtype=np.bool_)
    population_sum = np.zeros(n_ticks, dtype=float)
    kept = 0

    for _ in range(shots):
        sim = HybridSimulator(n_qubits, params, rng)
        record = []
        events = np.zeros(flat.num_detectors, dtype=np.bool_)
        flips = np.zeros(flat.num_observables, dtype=np.bool_)
        populations = np.empty(n_ticks, dtype=float)
        tick_index = 0

        for name, targets, argument in operations:
            if name in ("H", "X", "Y", "Z", "S"):
                gate = getattr(sim, name.lower())
                for qubit in targets:
                    gate(qubit)
            elif name in ("CX", "CZ"):
                gate = getattr(sim, name.lower())
                for a, b, high in targets:
                    gate(a, b, higher_freq=high)
            elif name == "R":
                for qubit in targets:
                    sim.reset_after_measure(qubit)
            elif name in ("M", "MR"):
                for qubit, inverted in zip(targets, argument):
                    outcome = sim.measure(qubit)
                    record.append(bool(outcome) ^ inverted)
                    if name == "MR":
                        sim.reset_after_measure(qubit)
            elif name == "TICK":
                # Design's literal boundary rule, not a Stim syndrome round.
                sim.engine.heat(n_qubits)
                sim.engine.seep_cycle()
                populations[tick_index] = float(np.mean(sim.labels != 0))
                tick_index += 1
            elif name == "DETECTOR":
                events[argument] = _parity(record, targets)
            elif name == "OBSERVABLE_INCLUDE":
                flips[argument] ^= _parity(record, targets)
            else:
                _noise(sim, name, targets, argument)

        # Design/v0 convention: complete rejected shots to preserve RNG draws.
        rejected = (
            postselect_first_round
            and bool(groups)
            and bool(events[groups[0]].any())
        )
        if not rejected:
            detectors[kept] = events
            observables[kept] = flips
            population_sum += populations
            kept += 1

    detectors = detectors[:kept].copy()
    observables = observables[:kept].copy()
    if kept:
        detection_means = [
            float(detectors[:, group].mean()) for group in groups
        ]
        population_means = (population_sum / kept).tolist()
    else:
        detection_means = [float("nan")] * len(groups)
        population_means = [float("nan")] * n_ticks

    return {
        "det_events": detectors,
        "obs_flips": observables,
        "keep_rate": float(kept / shots),
        "detection_fraction_per_round": detection_means,
        "mean_label_population_per_round": population_means,
    }
```

test_graft_and_runner.py
```python
"""Regression tests for generated memory circuits and the literal interpreter.

Parameters in the six principal tests come from Brief V1-A / the Section V
simulation design, 2026-10-16. Seeds are our reproducibility choices, not
physical parameters. These are interpreter checks, not validation against
the paper's measured logical-error rates or a decoder.
"""

import numpy as np
import pytest
import stim

from graft_circuit import (
    build_memory_circuit,
    circuit_metadata,
    higher_frequency,
    role_map,
)
from hybrid_runner import run_circuit
from leakage_hybrid import LeakageParams


def test_circuit_shape():
    # Brief V1-A: distance 3, three rounds, common noise probability 0.002.
    circuit = build_memory_circuit(3, 3, 0.002)
    metadata = circuit_metadata(circuit)
    assert set(metadata) == {"n_qubits", "n_detectors", "n_observables"}
    assert metadata["n_qubits"] == 17
    assert metadata["n_detectors"] > 0
    assert metadata["n_observables"] == 1
    roles = role_map(circuit)
    assert len(roles["data"]) == 9
    assert len(roles["measure"]) == 8
    assert not set(roles["data"]) & set(roles["measure"])
    assert set(roles["data"]) | set(roles["measure"]) == set(range(17))
    assert roles["data"] == sorted(roles["data"])
    assert roles["measure"] == sorted(roles["measure"])


def test_noiseless_runner_is_silent():
    # Brief V1-A: noiseless distance-3 memory, four rounds and 200 shots.
    circuit = build_memory_circuit(3, 4, 0)
    result = run_circuit(
        circuit, LeakageParams(enabled=False), shots=200, seed=101
    )
    assert result["det_events"].shape == (200, circuit.num_detectors)
    assert result["obs_flips"].shape == (200, circuit.num_observables)
    assert result["det_events"].dtype == np.bool_
    assert result["obs_flips"].dtype == np.bool_
    assert not result["det_events"].any()
    assert not result["obs_flips"].any()
    assert result["keep_rate"] == 1.0
    assert np.all(np.asarray(result["mean_label_population_per_round"]) == 0)
    assert np.all(np.asarray(result["detection_fraction_per_round"]) == 0)


def test_noisy_runner_produces_events():
    # Brief V1-A: p=0.01, four rounds and 300 shots with leakage disabled.
    circuit = build_memory_circuit(3, 4, 0.01)
    result = run_circuit(
        circuit, LeakageParams(enabled=False), shots=300, seed=202
    )
    assert result["det_events"].any()
    assert 0 < result["obs_flips"].mean() < 0.5


def test_leakage_population_and_postselection():
    # Brief V1-A: p=0.002, six rounds, 300 shots; v0 default leakage model.
    circuit = build_memory_circuit(3, 6, 0.002)
    leaked = run_circuit(circuit, LeakageParams(), shots=300, seed=303)
    disabled = run_circuit(
        circuit, LeakageParams(enabled=False), shots=300, seed=303
    )
    selected = run_circuit(
        circuit, LeakageParams(), shots=300, seed=303,
        postselect_first_round=True,
    )
    assert np.any(np.asarray(leaked["mean_label_population_per_round"]) > 0)
    assert np.all(np.asarray(disabled["mean_label_population_per_round"]) == 0)
    assert 0 < selected["keep_rate"] <= 1

    # Same seed and completed rejected shots imply exact retained subsequences.
    coords = circuit.get_detector_coordinates()
    first_time = min(coord[2] for coord in coords.values())
    first_group = [i for i, coord in coords.items() if coord[2] == first_time]
    mask = ~leaked["det_events"][:, first_group].any(axis=1)
    np.testing.assert_array_equal(
        selected["det_events"], leaked["det_events"][mask]
    )
    np.testing.assert_array_equal(
        selected["obs_flips"], leaked["obs_flips"][mask]
    )
    assert selected["keep_rate"] == float(mask.mean())


def test_runner_determinism():
    # Our regression workload: three rounds, 40 shots, common p=0.002.
    circuit = build_memory_circuit(3, 3, 0.002)
    first = run_circuit(circuit, LeakageParams(), shots=40, seed=404)
    second = run_circuit(circuit, LeakageParams(), shots=40, seed=404)
    for key in ("det_events", "obs_flips"):
        np.testing.assert_array_equal(first[key], second[key])
    for key in (
        "detection_fraction_per_round", "mean_label_population_per_round"
    ):
        np.testing.assert_array_equal(first[key], second[key])
    assert first["keep_rate"] == second["keep_rate"]


def test_higher_frequency_rule():
    # Brief V1-A: distance-3 roles; our stand-in frequency ordering.
    roles = role_map(build_memory_circuit(3, 1, 0))
    data = roles["data"]
    measure = roles["measure"]
    assert higher_frequency(data[-1], measure[0], roles) == measure[0]
    assert higher_frequency(measure[0], data[-1], roles) == measure[0]
    assert higher_frequency(data[0], data[-1], roles) == data[-1]
    assert higher_frequency(measure[0], measure[-1], roles) == measure[-1]


@pytest.mark.parametrize(
    "distance,rounds,p",
    [(2, 1, 0), (1, 1, 0), (3, 0, 0), (3, 1, -0.1),
     (3, 1, 0.11), (3, 1, float("nan"))],
)
def test_invalid_construction(distance, rounds, p):
    # Our boundary tests of the brief's construction domain.
    with pytest.raises(ValueError):
        build_memory_circuit(distance, rounds, p)


def test_empty_retained_ensemble():
    # Our deterministic rejection fixture: the first detector is always one.
    circuit = stim.Circuit("""
        R 0
        X 0
        TICK
        M 0
        DETECTOR(0, 0, 0) rec[-1]
        OBSERVABLE_INCLUDE(0) rec[-1]
    """)
    result = run_circuit(
        circuit, LeakageParams(enabled=False), shots=3, seed=505,
        postselect_first_round=True,
    )
    assert result["keep_rate"] == 0.0
    assert result["det_events"].shape == (0, 1)
    assert result["obs_flips"].shape == (0, 1)
    assert np.isnan(result["detection_fraction_per_round"]).all()
    assert np.isnan(result["mean_label_population_per_round"]).all()


def test_invalid_detector_coordinates_and_unsupported_gate():
    # Our fixtures: fail loudly rather than inventing timing or gate behavior.
    params = LeakageParams(enabled=False)
    with pytest.raises(ValueError, match="DETECTOR"):
        run_circuit(
            stim.Circuit("R 0\nM 0\nDETECTOR rec[-1]"),
            params, shots=1, seed=606,
        )
    with pytest.raises(ValueError, match="SQRT_X"):
        run_circuit(
            stim.Circuit("SQRT_X 0"), params, shots=1, seed=606
        )
```