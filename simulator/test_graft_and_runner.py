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
