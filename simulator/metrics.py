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
