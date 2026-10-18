device_params.py
```python
"""Verified aggregate leakage parameters, not a digitized device table.

Per-qubit values from supplement Figs. S5-S9 are NOT digitized; every
qubit currently gets the verified aggregate defaults unless explicitly
overridden by the caller. The digitization_status field travels with
serialized tables. Overrides are caller-supplied, not inferred data.

The uniform v0 engine adapter deliberately uses only the default row.
"""

from dataclasses import asdict, dataclass, field
import json
import math

from leakage_hybrid import LeakageParams


LITERATURE = {
    # McEwen et al. 2021, fitted leakage generation per cycle.
    "generation_per_cycle_band": (0.09e-2, 0.11e-2),
    # McEwen et al. 2021, steady-state |2> population.
    "steady_state_population_band": (0.97e-2, 1.30e-2),
    # Miao et al. 2023, leakage lifetime.
    "lifetime_cycles": 4.4,
    # Miao et al. 2023: excess |2> strictly below this bound by 2 cycles.
    "removal_excess_population_upper_bound": 1e-3,
    "removal_within_cycles": 2,
    # Cultivation supplement, Sec. XIV, SI1000 baseline.
    "si1000_p": 2.3e-3,
    # Cultivation supplement, Sec. XIV / Fig. S22 fit values.
    "experiment_logical_error_per_cycle": 5.3e-2,
    "simulated_logical_error_per_cycle": 0.8e-2,
}


def _validate_number(name, value, *, probability=False):
    try:
        valid = math.isfinite(value)
        valid = valid and (0 <= value <= 1 if probability else value > 0)
    except (TypeError, ValueError, OverflowError):
        valid = False
    if not valid:
        domain = "in [0, 1]" if probability else "positive"
        raise ValueError(f"{name} must be finite and {domain}")


@dataclass
class QubitParams:
    """Aggregate defaults; readout leakage is an unspecialized Arm-3 knob."""

    cz_leak_prob: float = 8e-4        # 2023 SI Sec. XIV: pt.
    heating_rate: float = 1.0 / 700e-6  # 2023 SI Sec. XIV: Gamma, s^-1.
    t_cycle: float = 896e-9          # 2023 SI Sec. XIV, seconds.
    lifetime_cycles: float = 4.4     # Miao et al. 2023.
    readout_leak_prob: float = 0.0   # Arm-3 swept knob, not measured here.

    def __post_init__(self):
        for name in ("cz_leak_prob", "readout_leak_prob"):
            _validate_number(name, getattr(self, name), probability=True)
        for name in ("heating_rate", "t_cycle", "lifetime_cycles"):
            _validate_number(name, getattr(self, name))


@dataclass
class DeviceParams:
    """Aggregate-backed table with explicit provenance and optional overrides."""

    default: QubitParams = field(default_factory=QubitParams)
    overrides: dict = field(default_factory=dict)
    digitization_status: str = "aggregate_only_not_digitized"

    def __post_init__(self):
        if not isinstance(self.default, QubitParams):
            raise ValueError("default must be a QubitParams")
        self.default.__post_init__()
        if not isinstance(self.overrides, dict):
            raise ValueError("overrides must be a dict")
        for index, row in self.overrides.items():
            if isinstance(index, bool) or not isinstance(index, int) or index < 0:
                raise ValueError("override indices must be nonnegative integers")
            if not isinstance(row, QubitParams):
                raise ValueError("override rows must be QubitParams")
            row.__post_init__()
        if not isinstance(self.digitization_status, str):
            raise ValueError("digitization_status must be a string")

    def for_qubit(self, i) -> QubitParams:
        """Return the explicit override, or the aggregate default row."""
        return self.overrides.get(i, self.default)

    def uniform_leakage_params(self, **overrides) -> LeakageParams:
        """Adapt defaults to v0; spatial overrides are intentionally not averaged."""
        values = asdict(self.default)
        values.update(overrides)
        # Validate the shared physical fields, including keyword replacements.
        QubitParams(**{name: values[name] for name in asdict(self.default)})
        return LeakageParams(**values)

    def save_json(self, path):
        """Save all rows and the provenance status, without inventing data."""
        self.__post_init__()
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(asdict(self), handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")

    @classmethod
    def load_json(cls, path):
        """Restore integer qubit indices and validate every parameter row."""
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        rows = {}
        for key, value in data["overrides"].items():
            try:
                index = int(key)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid qubit index: {key!r}") from exc
            if str(index) != key or index in rows:
                raise ValueError(f"noncanonical or duplicate qubit index: {key!r}")
            rows[index] = QubitParams(**value)
        return cls(
            default=QubitParams(**data["default"]),
            overrides=rows,
            digitization_status=data["digitization_status"],
        )

    def analytic_steady_state(self) -> float:
        """Heating/seepage two-state estimate, not the complete CZ-driven model."""
        self.default.__post_init__()
        p = self.default
        p_gen = -math.expm1(-p.heating_rate * p.t_cycle)
        p_seep = -math.expm1(-1.0 / p.lifetime_cycles)
        return p_gen / (p_gen + p_seep)
```

decoder_pin.py
```python
"""Behavioral pin for OUR installed Tesseract decoder, not the paper's decoder.

Google published no version/settings underlying the 0.8%/cycle fit.
The requested long-beam configuration below is documentation provenance,
not a claim that the factory's first decoder applies those settings.
A small deterministic probe detects changes on its inputs, not every
possible decoder behavior change. No network access is performed.
"""

import hashlib
from importlib import metadata
import json

import numpy as np
import tesseract_decoder


# REQUESTED configuration: Tesseract documentation's long-beam example,
# recorded by the survey on 2026-10-17. Not silently applied to factory objects.
LONG_BEAM_REQUEST = {
    "pqlimit": 1000000,
    "det_beam": 20,
    "beam_climbing": True,
    "det_orders": 21,
    "no_revisit_dets": True,
}

_VERSION_PACKAGES = {
    "tesseract_version": "tesseract-decoder",
    "stim_version": "stim",
    "sinter_version": "sinter",
    "pymatching_version": "pymatching",
}
_PROBE_SEED = 0
_PROBE_RANDOM_SHOTS = 64


def _decoder_dict():
    factory = getattr(
        tesseract_decoder, "make_tesseract_sinter_decoders_dict", None
    )
    if not callable(factory):
        raise RuntimeError(
            "tesseract_decoder is missing "
            "make_tesseract_sinter_decoders_dict()"
        )
    return factory()


def available_decoders() -> list:
    """Return factory names in deterministic lexical order."""
    return sorted(_decoder_dict())


def _first_decoder(decoders):
    if not decoders:
        raise RuntimeError("Tesseract decoder factory returned no available decoders")
    return decoders[sorted(decoders)[0]]


def get_decoder():
    """Return the first decoder in sorted-name order."""
    return _first_decoder(_decoder_dict())


def _compile(decoder, dem):
    method = getattr(decoder, "compile_for_dem", None)
    if not callable(method):
        raise RuntimeError("Tesseract decoder is missing compile_for_dem(dem=...)")
    try:
        compiled = method(dem=dem)
    except NotImplementedError as exc:
        raise RuntimeError(
            "Tesseract decoder does not implement compile_for_dem(dem=...)"
        ) from exc
    if not callable(getattr(compiled, "decode_shots_bit_packed", None)):
        raise RuntimeError(
            "Compiled Tesseract decoder is missing decode_shots_bit_packed"
        )
    return compiled


def _predictions(compiled, events, n_observables):
    packed = np.packbits(events, axis=1, bitorder="little")
    try:
        result = compiled.decode_shots_bit_packed(
            bit_packed_detection_event_data=packed
        )
    except NotImplementedError as exc:
        raise RuntimeError(
            "Compiled Tesseract decoder does not implement "
            "decode_shots_bit_packed"
        ) from exc
    result = np.asarray(result)
    expected = (events.shape[0], (n_observables + 7) // 8)
    if result.dtype != np.uint8 or result.shape != expected:
        raise RuntimeError(
            "decode_shots_bit_packed returned an invalid result: "
            f"expected uint8 shape {expected}, got {result.dtype} {result.shape}"
        )
    return np.unpackbits(
        result, axis=1, count=n_observables, bitorder="little"
    ).astype(bool)


def decode(circuit, det_events) -> np.ndarray:
    """Predict observables using the actual compiled sinter decoder protocol."""
    events = np.asarray(det_events)
    if events.ndim != 2 or events.shape[1] != circuit.num_detectors:
        raise ValueError(
            "det_events must have shape (shots, circuit.num_detectors)"
        )
    if not np.all((events == 0) | (events == 1)):
        raise ValueError("det_events must contain only binary values")
    dem = circuit.detector_error_model(decompose_errors=True)
    compiled = _compile(get_decoder(), dem)
    return _predictions(compiled, events.astype(bool), circuit.num_observables)


def _version(package):
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        # JSON null explicitly records absence; it is not a guessed version.
        return None


def _make_pin(circuit):
    decoders = _decoder_dict()
    decoder = _first_decoder(decoders)
    dem = circuit.detector_error_model(decompose_errors=True)
    compiled = _compile(decoder, dem)
    rng = np.random.default_rng(_PROBE_SEED)
    events = np.zeros(
        (_PROBE_RANDOM_SHOTS + 1, circuit.num_detectors), dtype=bool
    )
    events[1:] = rng.random(
        (_PROBE_RANDOM_SHOTS, circuit.num_detectors)
    ) < 0.02
    predictions = _predictions(compiled, events, circuit.num_observables)
    return {
        **{key: _version(package) for key, package in _VERSION_PACKAGES.items()},
        "available_decoders": sorted(decoders),
        "selected_decoder": sorted(decoders)[0],
        "requested_config": dict(LONG_BEAM_REQUEST),
        "fingerprint": {
            "sha256": hashlib.sha256(predictions.tobytes(order="C")).hexdigest(),
            "sample_count": len(events),
            "seed": _PROBE_SEED,
            "flip_probability": 0.02,
            "prediction_encoding": "unpacked_bool_uint8_row_major",
            "num_detectors": circuit.num_detectors,
            "num_observables": circuit.num_observables,
        },
    }


def write_pin(path, circuit) -> dict:
    """Write versions, requested settings, and deterministic prediction hash."""
    pin = _make_pin(circuit)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(pin, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    return pin


def check_pin(path, circuit) -> tuple:
    """Recompute the probe and report each changed recorded field.

    Missing files or invalid JSON propagate their ordinary I/O/JSON errors.
    Missing decoder protocol support raises RuntimeError rather than faking
    predictions or reporting a successful comparison.
    """
    with open(path, encoding="utf-8") as handle:
        stored = json.load(handle)
    current = _make_pin(circuit)
    if not isinstance(stored, dict):
        return False, ["pin must be a JSON object"]
    diffs = []
    for key, value in current.items():
        if key not in stored:
            diffs.append(f"{key}: missing from stored pin")
        elif key == "fingerprint" and isinstance(stored[key], dict):
            for field, expected in value.items():
                if field not in stored[key]:
                    diffs.append(f"fingerprint.{field}: missing from stored pin")
                elif stored[key][field] != expected:
                    diffs.append(
                        f"fingerprint.{field}: stored {stored[key][field]!r}, "
                        f"current {expected!r}"
                    )
        elif stored[key] != value:
            diffs.append(f"{key}: stored {stored[key]!r}, current {value!r}")
    return not diffs, diffs
```

metrics.py
```python
"""NumPy-only comparison metrics for joint memory-experiment scoring.

The per-cycle conversion uses Google's standard parity-flip fit.
Intervals and chi-square scores are binomial approximations, not fitted
experimental uncertainties. Covariances are unbiased sample estimates;
these summaries do not claim to reproduce unavailable figure digitization.
"""

import numpy as np


def _finite_scalar(value, name):
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite scalar") from exc
    if not np.isfinite(result):
        raise ValueError(f"{name} must be a finite scalar")
    return result


def _vector(values, name):
    result = np.asarray(values, dtype=float)
    if result.ndim != 1 or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a finite one-dimensional array")
    return result


def per_cycle_rate(p_logical: float, n_cycles: int) -> float:
    """Invert P_L(N) = (1 - (1 - 2*epsilon)**N) / 2 stably."""
    p = _finite_scalar(p_logical, "p_logical")
    if not 0 <= p < 0.5:
        raise ValueError("p_logical must satisfy 0 <= p_logical < 0.5")
    if (
        isinstance(n_cycles, (bool, np.bool_))
        or not isinstance(n_cycles, (int, np.integer))
        or n_cycles < 1
    ):
        raise ValueError("n_cycles must be an integer >= 1")
    return float(-0.5 * np.expm1(np.log1p(-2 * p) / n_cycles))


def ratio_ci(arm_errors, arm_shots, base_errors, base_shots,
             z: float = 1.96) -> tuple:
    """Binomial risk ratio with a log-delta-method interval.

    At zero arm errors the log approximation is undefined; return the
    explicitly uninformative boundary interval (0, infinity), without
    inventing pseudocounts. This boundary interval is not a calibrated CI.
    """
    ae = _finite_scalar(arm_errors, "arm_errors")
    an = _finite_scalar(arm_shots, "arm_shots")
    be = _finite_scalar(base_errors, "base_errors")
    bn = _finite_scalar(base_shots, "base_shots")
    z = _finite_scalar(z, "z")
    if an <= 0 or bn <= 0:
        raise ValueError("shot counts must be positive")
    if not 0 <= ae <= an or not 0 < be <= bn:
        raise ValueError("errors must be within shots; base errors must be positive")
    if z <= 0:
        raise ValueError("z must be positive")
    if ae == 0:
        return 0.0, 0.0, float("inf")
    ratio = (ae / an) / (be / bn)
    variance = (1 - ae / an) / ae + (1 - be / bn) / be
    width = z * np.sqrt(variance)
    with np.errstate(over="ignore", under="ignore"):
        lo, hi = np.exp(np.log(ratio) + np.array([-width, width]))
    return float(ratio), float(lo), float(hi)


def detection_curve_chi2(curve_a, curve_b, shots_per_point) -> tuple:
    """Score against curve_b's binomial variance, treating curve_b as fixed.

    shots_per_point may be a positive scalar or a matching vector. No
    uncertainty contribution from curve_a or fitted-parameter correction
    to the requested degrees of freedom is added.
    """
    a = _vector(curve_a, "curve_a")
    b = _vector(curve_b, "curve_b")
    if a.shape != b.shape:
        raise ValueError("curve lengths must match")
    if np.any((a < 0) | (a > 1) | (b < 0) | (b > 1)):
        raise ValueError("curves must contain probabilities in [0, 1]")
    shots = np.asarray(shots_per_point, dtype=float)
    if shots.ndim != 0 and shots.shape != b.shape:
        raise ValueError("shots_per_point must be scalar or match the curves")
    if not np.all(np.isfinite(shots)) or np.any(shots <= 0):
        raise ValueError("shots_per_point must be finite and positive")
    variance = b * (1 - b) / shots
    if np.any(variance <= 0):
        raise ValueError("curve_b contains a zero-variance point")
    return float(np.sum((a - b) ** 2 / variance)), int(a.size)


def covariance_matrix(det_events) -> np.ndarray:
    """Unbiased covariance (ddof=1), always shaped detectors by detectors."""
    events = np.asarray(det_events, dtype=float)
    if events.ndim != 2 or events.shape[0] < 2:
        raise ValueError("det_events must be a 2D array with at least two shots")
    if not np.all(np.isfinite(events)):
        raise ValueError("det_events must be finite")
    centered = events - np.mean(events, axis=0)
    return centered.T @ centered / (events.shape[0] - 1)


def matrix_distance(a, b) -> float:
    """Normalized Frobenius distance, with an explicit all-zero convention."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("matrix shapes must match")
    if a.ndim != 2 or not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("inputs must be finite matrices")
    # Common scaling avoids overflow without changing the ratio.
    scale = max(np.max(np.abs(a), initial=0), np.max(np.abs(b), initial=0))
    if scale == 0:
        return 0.0
    a, b = a / scale, b / scale
    denominator = np.linalg.norm(a, "fro") + np.linalg.norm(b, "fro")
    return float(np.linalg.norm(a - b, "fro") / denominator)


def lag_profile(cov, detector_rounds) -> dict:
    """Mean covariance per absolute round lag, using each i<j pair once.

    Diagonals are never included. Lag zero contains distinct same-round
    detectors only. Lags without any pairs are omitted.
    """
    cov = np.asarray(cov, dtype=float)
    rounds = _vector(detector_rounds, "detector_rounds")
    if cov.shape != (rounds.size, rounds.size):
        raise ValueError("cov must be square and match detector_rounds")
    if not np.all(np.isfinite(cov)):
        raise ValueError("cov must be finite")
    if np.any(rounds != np.floor(rounds)):
        raise ValueError("detector_rounds must contain integer round indices")
    i, j = np.triu_indices(rounds.size, k=1)
    lags = np.abs(rounds[i] - rounds[j])
    values = cov[i, j]
    return {
        int(lag): float(np.mean(values[lags == lag]))
        for lag in np.unique(lags)
    }


def rise_summary(curve) -> dict:
    """Compare the first and last floor(n/3) points, ignoring the middle.

    For the ramp 1..9 these means are 2 and 8, giving relative rise 3.
    The brief's example mean of 6 for the last third is an arithmetic
    inconsistency; this function follows the specified first/last thirds.
    """
    curve = _vector(curve, "curve")
    if curve.size < 3:
        raise ValueError("curve must have at least three points")
    third = curve.size // 3
    first = float(np.mean(curve[:third]))
    last = float(np.mean(curve[-third:]))
    if first == 0:
        raise ValueError("first-third mean must be nonzero")
    return {"first": first, "last": last, "relative_rise": (last - first) / first}


def evaluate_joint(observables: dict, targets: dict,
                   tolerances: dict) -> dict:
    """Require identical key sets and apply every requested tolerance.

    cov_distance uses the specified one-sided upper bound and requires its
    target to be zero. An empty, consistently specified comparison passes
    vacuously.
    """
    keys = set(observables) | set(targets) | set(tolerances)
    for name, values in (
        ("observables", observables), ("targets", targets),
        ("tolerances", tolerances),
    ):
        missing = keys - set(values)
        if missing:
            raise ValueError(f"{name} is missing keys: {sorted(missing)!r}")
    passed = {}
    for key in observables:
        observed = _finite_scalar(observables[key], f"observables[{key!r}]")
        target = _finite_scalar(targets[key], f"targets[{key!r}]")
        tolerance = _finite_scalar(tolerances[key], f"tolerances[{key!r}]")
        if tolerance < 0:
            raise ValueError("tolerances must be nonnegative")
        if key == "cov_distance":
            if target != 0:
                raise ValueError("cov_distance target must be zero")
            passed[key] = bool(observed <= tolerance)
        else:
            passed[key] = bool(abs(observed - target) <= tolerance)
    return {"per_observable": passed, "joint": all(passed.values())}
```

test_sim_v1b.py
```python
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
```