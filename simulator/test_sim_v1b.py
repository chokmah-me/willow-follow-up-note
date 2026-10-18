"""V1-B checks using the real installed decoder, without decoder substitutes."""

import json

import numpy as np
import pytest

from decoder_pin import available_decoders, check_pin, decode, write_pin
from device_params import DeviceParams, LITERATURE, QubitParams
from graft_circuit import build_memory_circuit
from leakage_hybrid import LeakageParams
from metrics import (
    covariance_matrix,
    detection_curve_chi2,
    evaluate_joint,
    lag_profile,
    matrix_distance,
    per_cycle_rate,
    ratio_ci,
    rise_summary,
)


def test_device_defaults_and_roundtrip(tmp_path):
    device = DeviceParams()
    expected = {
        "cz_leak_prob": 8e-4,
        "heating_rate": 1 / 700e-6,
        "t_cycle": 896e-9,
        "lifetime_cycles": 4.4,
        "readout_leak_prob": 0.0,
    }
    for name, value in expected.items():
        assert getattr(device.default, name) == pytest.approx(value)
    assert device.for_qubit(10) is device.default
    midpoint = np.mean(LITERATURE["steady_state_population_band"])
    assert midpoint / 2 <= device.analytic_steady_state() <= midpoint * 2
    assert device.digitization_status == "aggregate_only_not_digitized"

    # This is an explicit test knob, not a digitized per-qubit measurement.
    device.overrides[3] = QubitParams(readout_leak_prob=0.02)
    device.digitization_status = "aggregate_only_not_digitized_test_override"
    path = tmp_path / "device.json"
    device.save_json(path)
    restored = DeviceParams.load_json(path)
    assert restored == device
    assert list(restored.overrides) == [3]
    assert restored.for_qubit(3).readout_leak_prob == 0.02
    assert restored.for_qubit(4) == device.default


@pytest.mark.parametrize(
    "kwargs",
    [
        {"cz_leak_prob": -0.01},
        {"cz_leak_prob": 1.01},
        {"readout_leak_prob": float("nan")},
        {"heating_rate": 0},
        {"t_cycle": -1},
        {"lifetime_cycles": float("inf")},
    ],
)
def test_invalid_device_parameters(kwargs):
    with pytest.raises(ValueError):
        QubitParams(**kwargs)


def test_uniform_adapter():
    device = DeviceParams()
    params = device.uniform_leakage_params()
    assert isinstance(params, LeakageParams)
    for name in (
        "cz_leak_prob", "heating_rate", "t_cycle",
        "lifetime_cycles", "readout_leak_prob",
    ):
        assert getattr(params, name) == getattr(device.default, name)
    assert device.uniform_leakage_params(cz_leak_prob=0.003).cz_leak_prob == 0.003
    with pytest.raises(ValueError):
        device.uniform_leakage_params(readout_leak_prob=2)


def test_decoder_pin_and_zero_events(tmp_path):
    circuit = build_memory_circuit(
        distance=3, rounds=3, p=LITERATURE["si1000_p"]
    )
    path = tmp_path / "decoder_pin.json"
    pin = write_pin(path, circuit)
    assert available_decoders()
    assert pin["fingerprint"]["sample_count"] == 65
    assert len(pin["fingerprint"]["sha256"]) == 64
    assert check_pin(path, circuit) == (True, [])

    events = np.zeros((4, circuit.num_detectors), dtype=bool)
    predictions = decode(circuit, events)
    assert predictions.dtype == np.bool_
    assert predictions.shape == (4, circuit.num_observables)
    assert not predictions.any()

    pin["fingerprint"]["sha256"] = "deliberately changed"
    path.write_text(json.dumps(pin), encoding="utf-8")
    matches, diffs = check_pin(path, circuit)
    assert not matches
    assert any("fingerprint.sha256" in diff for diff in diffs)


def test_per_cycle_roundtrip():
    epsilon, n = 0.01, 25
    p_logical = 0.5 * (1 - (1 - 2 * epsilon) ** n)
    assert per_cycle_rate(p_logical, n) == pytest.approx(epsilon, abs=1e-9)
    assert per_cycle_rate(0, 1) == 0
    for p, cycles in [(-0.1, 1), (0.5, 1), (0.1, 0), (0.1, 1.5)]:
        with pytest.raises(ValueError):
            per_cycle_rate(p, cycles)


def test_ratio_ci():
    ratio, lo, hi = ratio_ci(100, 10000, 10, 10000)
    assert ratio == pytest.approx(10)
    assert 1 < lo < 10 < hi
    with pytest.raises(ValueError):
        ratio_ci(100, 10000, 0, 10000)
    with pytest.raises(ValueError):
        ratio_ci(0, 0, 1, 10000)
    assert ratio_ci(0, 100, 1, 100) == (0, 0, float("inf"))


def test_detection_curve_chi2():
    curve = np.array([0.01, 0.03, 0.05])
    assert detection_curve_chi2(curve, curve, 10000) == (0.0, 3)
    chi2, dof = detection_curve_chi2([0.3], [0.2], 100)
    assert chi2 == pytest.approx(0.1**2 / (0.2 * 0.8 / 100))
    assert dof == 1
    with pytest.raises(ValueError):
        detection_curve_chi2([0.1], [0.1, 0.2], 100)
    with pytest.raises(ValueError):
        detection_curve_chi2([0.1], [0.0], 100)


def test_covariance_lags_and_distance():
    column = np.array([0, 1, 1, 0, 1], dtype=bool)
    events = np.column_stack([column, column])
    cov = covariance_matrix(events)
    variance = np.var(column.astype(float), ddof=1)
    assert cov.shape == (2, 2)
    assert cov[0, 1] == pytest.approx(variance, abs=1e-9)
    assert cov[0, 0] == pytest.approx(variance, abs=1e-9)

    hand_cov = np.array([
        [1.0, 0.2, 0.4],
        [0.2, 2.0, 0.6],
        [0.4, 0.6, 3.0],
    ])
    profile = lag_profile(hand_cov, [0, 0, 2])
    assert profile == pytest.approx({0: 0.2, 2: 0.5})
    assert matrix_distance(hand_cov, hand_cov) == 0
    assert matrix_distance(hand_cov, -hand_cov) == pytest.approx(1)
    assert matrix_distance(np.zeros((2, 2)), np.zeros((2, 2))) == 0
    with pytest.raises(ValueError):
        matrix_distance(np.zeros((2, 2)), np.zeros((3, 3)))


def test_rise_summary():
    # The brief's example is inconsistent: the last third of 1..9 is
    # 7,8,9, averaging 8, not 6. Test the specified first/last-third rule.
    summary = rise_summary(np.arange(1, 10))
    assert summary == pytest.approx(
        {"first": 2, "last": 8, "relative_rise": 3}
    )
    # An actual first-third mean 2 and last-third mean 6 gives rise 2.
    assert rise_summary([1, 2, 3, 3, 4, 5, 5, 6, 7]) == pytest.approx(
        {"first": 2, "last": 6, "relative_rise": 2}
    )
    with pytest.raises(ValueError):
        rise_summary([1, 2])
    with pytest.raises(ValueError):
        rise_summary([0, 1, 2])


def test_evaluate_joint():
    targets = {
        "logical_ratio": 5.3 / 0.8,
        "rise": 2.0,
        "cov_distance": 0.0,
        "keep_rate": 0.9,
    }
    tolerances = {
        "logical_ratio": 0.5,
        "rise": 0.1,
        "cov_distance": 0.05,
        "keep_rate": 0.02,
    }
    observed = dict(targets, cov_distance=0.03)
    result = evaluate_joint(observed, targets, tolerances)
    assert result["joint"] is True
    assert all(value is True for value in result["per_observable"].values())

    observed["keep_rate"] = 0.5
    result = evaluate_joint(observed, targets, tolerances)
    assert result["joint"] is False
    assert result["per_observable"]["keep_rate"] is False

    for missing_from in range(3):
        dictionaries = [dict(observed), dict(targets), dict(tolerances)]
        del dictionaries[missing_from]["rise"]
        with pytest.raises(ValueError):
            evaluate_joint(*dictionaries)
