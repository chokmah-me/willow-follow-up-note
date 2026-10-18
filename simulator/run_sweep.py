"""Section V design (2026-10-16), including the SME review majors.

Generation g maps to heating_rate = -log(1-g)/t_cycle and
cz_leak_prob = 8e-4 * g/g_default, where
g_default = 1-exp(-t_cycle/(700 us)). Both creation channels vanish at
zero. The readout arm additionally sets readout_leak_prob = multiplier*g.

Only the ratio and steady-state population enter evaluate_joint on
the grafted sweep; the ratio tolerance is the caller's. Grafted
rise is reported as a prediction, not a fit to Fig. S23. Covariance
is a structural report (SME major 6; adopted 2023 substitution).
The 2023 rise envelope (7% to 12% at distance 5, risetime of order
5 cycles; 8% at distance 3) is the instrument-calibration target
for a separate 2023-style memory run, not a gate on this driver.
Keep rate is also reported.
Arm 4 is a prediction, with removal_boost a Miao-efficacy stand-in,
not a fit. Reduced-scale results demonstrate machinery, not a verdict
on the paper's attribution.

All arms run by default. An optional ``arms`` list selects leakage
variants; both baseline engines always run for the cross-check.
Per-N records are stored in ``by_rounds``; other summaries use max(N).
Seeds are the configured seed plus a mixed-radix point/index offset,
wrapped to Stim's unsigned 64-bit range.
"""

import copy
import json
import math
import sys
from dataclasses import replace

import numpy as np

import decoder_pin
import graft_circuit
import hybrid_runner
import metrics
from leakage_hybrid import LeakageParams


ARM_NAMES = (
    "baseline_stim",
    "baseline_hybrid",
    "leakage",
    "leakage_readout",
    "leakage_removal",
)


def _jsonable(value):
    """Convert metric outputs to strict JSON, representing undefined values by null."""
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, np.generic):
        return _jsonable(value.item())
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _number(value, name, minimum=None, maximum=None):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    if maximum is not None and result > maximum:
        raise ValueError(f"{name} must be <= {maximum}")
    return result


def _validate(config):
    required = (
        "distance", "rounds_list", "shots", "seed", "generation_grid",
        "lifetime_grid", "readout_multipliers", "ratio_tolerance",
        "postselect_first_round",
    )
    missing = [key for key in required if key not in config]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")
    for key in ("distance", "shots", "seed"):
        value = config[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{key} must be an integer")
        if value < (0 if key == "seed" else 1):
            raise ValueError(f"Invalid {key}: {value}")
    if config["seed"] >= 2**64:
        raise ValueError("seed must fit in an unsigned 64-bit integer")
    rounds = config["rounds_list"]
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("rounds_list must contain at least one cycle count")
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 1 for n in rounds):
        raise ValueError("Cycle counts must be positive integers")
    if not isinstance(config["postselect_first_round"], bool):
        raise ValueError("postselect_first_round must be a bool")

    requested = config.get("arms", list(ARM_NAMES))
    if not isinstance(requested, list):
        raise ValueError("arms must be a list of arm names")
    if any(not isinstance(a, str) or a not in ARM_NAMES for a in requested):
        raise ValueError(f"Unknown arm names in {requested!r}")
    selected = set(requested) | {"baseline_stim", "baseline_hybrid"}
    for key in ("generation_grid", "lifetime_grid", "readout_multipliers"):
        if not isinstance(config[key], list):
            raise ValueError(f"{key} must be a list")
    if selected.intersection(ARM_NAMES[2:]):
        if not config["generation_grid"] or not config["lifetime_grid"]:
            raise ValueError("Leakage arms require nonempty generation and lifetime grids")

    for g in config["generation_grid"]:
        if _number(g, "generation", 0.0, 1.0) == 1.0:
            raise ValueError("Generation must be strictly less than one")
    for lifetime in config["lifetime_grid"]:
        if _number(lifetime, "lifetime", 0.0) == 0.0:
            raise ValueError("Lifetimes must be positive")
    for multiplier in config["readout_multipliers"]:
        m = _number(multiplier, "readout multiplier", 0.0)
        if "leakage_readout" in selected:
            if any(m * float(g) > 1 for g in config["generation_grid"]):
                raise ValueError("multiplier * generation must not exceed one")
    _number(config.get("p", 2.3e-3), "p", 0.0, 1.0)
    _number(config.get("removal_boost", 5.0), "removal_boost", 0.0)
    _number(config.get("target_ratio", 6.6), "target_ratio", 0.0)
    for key, default in (("ratio_tolerance", None), ("population_ceiling", 0.01)):
        if _number(config.get(key, default), key, 0.0) == 0.0:
            raise ValueError(f"{key} must be positive")
    return selected, sorted(set(rounds))


def _detector_rounds(circuit):
    coordinates = circuit.get_detector_coordinates()
    values = []
    for detector in range(circuit.num_detectors):
        coordinate = coordinates[detector]
        if len(coordinate) < 3:
            raise ValueError("Each detector must have a third (time) coordinate")
        time = float(coordinate[2])
        if not math.isfinite(time) or not time.is_integer():
            raise ValueError("Detector time coordinates must be finite integers")
        values.append(int(time))
    return np.asarray(values, dtype=int)


def _stim_sample(circuit, detector_rounds, shots, seed, postselect):
    samples = circuit.compile_detector_sampler(seed=seed).sample(
        shots, append_observables=True
    )
    events = np.asarray(samples[:, :circuit.num_detectors], dtype=bool)
    observables = np.asarray(samples[:, circuit.num_detectors:], dtype=bool)
    times = np.unique(detector_rounds)
    keep = np.ones(shots, dtype=bool)
    if postselect and times.size:
        keep = ~events[:, detector_rounds == times[0]].any(axis=1)
    events, observables = events[keep], observables[keep]
    curve = [
        float(events[:, detector_rounds == time].mean()) if len(events) else None
        for time in times
    ]
    return {
        "det_events": events,
        "obs_flips": observables,
        "keep_rate": float(keep.mean()),
        "detection_fraction_per_round": curve,
        "mean_label_population_per_round": None,
    }


def _logical_counts(circuit, events, observables):
    kept = len(events)
    if not kept:
        return {"p_logical": None, "n_logical_errors": 0, "shots_kept": 0}
    predictions = np.asarray(decoder_pin.decode(circuit, events), dtype=bool)
    observables = np.asarray(observables, dtype=bool)
    if predictions.ndim == 1:
        predictions = predictions[:, None]
    if observables.ndim == 1:
        observables = observables[:, None]
    expected = (kept, circuit.num_observables)
    if predictions.shape != expected or observables.shape != expected:
        raise ValueError("Decoder predictions and observable samples must match")
    errors = int(np.any(predictions ^ observables, axis=1).sum())
    return {
        "p_logical": errors / kept,
        "n_logical_errors": errors,
        "shots_kept": kept,
    }


def _ratio(point, baseline):
    if not point["shots_kept"] or not baseline["shots_kept"]:
        return None
    return metrics.ratio_ci(
        point["n_logical_errors"], point["shots_kept"],
        baseline["n_logical_errors"], baseline["shots_kept"],
    )


def _ratio_estimate(result):
    """Accept the named or tuple form without changing the metric's estimator."""
    if result is None:
        return None
    if isinstance(result, dict):
        value = result["ratio"]
    elif isinstance(result, (tuple, list, np.ndarray)):
        value = result[0]
    else:
        value = result
    if value is None:
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def _chi2_fields(result):
    if isinstance(result, dict):
        return result["chi2"], result["dof"]
    chi2, dof = result
    return chi2, dof


def run_sweep(config: dict) -> dict:
    selected, rounds = _validate(config)
    largest = rounds[-1]
    shots = config["shots"]
    postselect = config["postselect_first_round"]
    generations = config["generation_grid"]
    lifetimes = config["lifetime_grid"]
    multipliers = config["readout_multipliers"]
    target = float(config.get("target_ratio", 6.6))
    tolerance = float(config["ratio_tolerance"])
    ceiling = float(config.get("population_ceiling", 0.01))
    boost = float(config.get("removal_boost", 5.0))

    defaults = LeakageParams()
    t_cycle = float(defaults.t_cycle)
    if not math.isfinite(t_cycle) or t_cycle <= 0:
        raise ValueError("LeakageParams.t_cycle must be positive, in seconds")
    gamma0 = 1.0 / (700e-6)
    g_default = -math.expm1(-gamma0 * t_cycle)
    circuits = {
        n: graft_circuit.build_memory_circuit(
            config["distance"], n, config.get("p", 2.3e-3)
        )
        for n in rounds
    }
    detector_rounds = {n: _detector_rounds(circuits[n]) for n in rounds}

    def seed_for(arm, gi, li, mi, ni):
        offset = ARM_NAMES.index(arm)
        for index, radix in (
            (gi, len(generations) + 1), (li, len(lifetimes) + 1),
            (mi, len(multipliers) + 1), (ni, len(rounds) + 1),
        ):
            offset = offset * radix + index
        return (config["seed"] + offset) % (2**64)

    def run_point(arm, params, coordinates, indices, baseline=None):
        point = dict(coordinates)
        point["by_rounds"] = {}
        final_sample = None
        for ni, n in enumerate(rounds):
            seed = seed_for(arm, *indices, ni)
            if arm == "baseline_stim":
                sample = _stim_sample(
                    circuits[n], detector_rounds[n], shots, seed, postselect
                )
            else:
                sample = hybrid_runner.run_circuit(
                    circuits[n], params, shots, seed,
                    postselect_first_round=postselect,
                )
            events = np.asarray(sample["det_events"], dtype=bool)
            if events.ndim != 2 or events.shape[1] != circuits[n].num_detectors:
                raise ValueError("Runner returned an invalid detector-event shape")
            record = _logical_counts(circuits[n], events, sample["obs_flips"])
            record["keep_rate"] = float(sample["keep_rate"])
            record["ratio_vs_baseline_hybrid"] = (
                _ratio(record, baseline["by_rounds"][str(n)])
                if baseline is not None else None
            )
            point["by_rounds"][str(n)] = record
            if n == largest:
                final_sample = sample
                final_events = events

        record = point["by_rounds"][str(largest)]
        point.update(record)
        probability = record["p_logical"]
        point["ler_per_cycle"] = (
            metrics.per_cycle_rate(probability, largest)
            if probability is not None else None
        )
        curve = final_sample["detection_fraction_per_round"]
        point["detection_fraction_per_round"] = curve
        try:
            point["rise"] = metrics.rise_summary(curve)
        except Exception:
            point["rise"] = None

        lag1 = None
        if len(final_events):
            covariance = metrics.covariance_matrix(final_events)
            lag1 = metrics.lag_profile(covariance, detector_rounds[largest])[1]
        point["covariance_lag1_excess"] = None
        if arm == "baseline_stim":
            population = None
        elif arm == "baseline_hybrid":
            population = 0.0
        else:
            populations = np.asarray(
                final_sample["mean_label_population_per_round"], dtype=float
            )
            population = (
                float(populations[len(populations) // 2:].mean())
                if populations.size else None
            )
        point["steady_population"] = population
        point["score"] = None
        if baseline is not None:
            estimate = _ratio_estimate(point["ratio_vs_baseline_hybrid"])
            if estimate is not None and population is not None:
                point["score"] = metrics.evaluate_joint(
                    {"ratio": estimate, "steady_population": population},
                    {"ratio": target, "steady_population": 0.0},
                    {"ratio": tolerance, "steady_population": ceiling},
                )
        return point, lag1

    disabled = replace(
        defaults, enabled=False, heating_rate=0.0, cz_leak_prob=0.0,
        readout_leak_prob=0.0, removal_on=False,
    )
    hybrid, hybrid_lag = run_point(
        "baseline_hybrid", disabled, {}, (0, 0, 0)
    )
    stim, stim_lag = run_point("baseline_stim", disabled, {}, (0, 0, 0))
    if stim_lag is not None and hybrid_lag is not None:
        stim["covariance_lag1_excess"] = stim_lag - hybrid_lag
    arms = {
        "baseline_stim": stim, "baseline_hybrid": hybrid,
        "leakage": [], "leakage_readout": [], "leakage_removal": [],
    }

    for gi, generation in enumerate(generations):
        g = float(generation)
        for li, lifetime in enumerate(lifetimes):
            base_params = replace(
                defaults, enabled=True,
                heating_rate=-math.log1p(-g) / t_cycle,
                cz_leak_prob=8e-4 * (g / g_default),
                lifetime_cycles=float(lifetime), readout_leak_prob=0.0,
                removal_on=False, removal_boost=boost,
            )
            for arm in ARM_NAMES[2:]:
                if arm not in selected:
                    continue
                variants = enumerate(multipliers) if arm == "leakage_readout" else [(0, None)]
                for mi, multiplier in variants:
                    coordinates = {"generation": g, "lifetime": float(lifetime)}
                    params = base_params
                    if arm == "leakage_readout":
                        coordinates["multiplier"] = float(multiplier)
                        params = replace(
                            params, readout_leak_prob=float(multiplier) * g
                        )
                    elif arm == "leakage_removal":
                        params = replace(params, removal_on=True)
                    point, lag1 = run_point(
                        arm, params, coordinates, (gi, li, mi), hybrid
                    )
                    if lag1 is not None and hybrid_lag is not None:
                        point["covariance_lag1_excess"] = lag1 - hybrid_lag
                    arms[arm].append(point)

    comparison_shots = min(stim["shots_kept"], hybrid["shots_kept"])
    chi2, dof = None, 0
    if comparison_shots:
        chi2, dof = _chi2_fields(metrics.detection_curve_chi2(
            stim["detection_fraction_per_round"],
            hybrid["detection_fraction_per_round"], comparison_shots,
        ))
    stim_ler, hybrid_ler = stim["ler_per_cycle"], hybrid["ler_per_cycle"]
    ler_ratio = None
    if stim_ler is not None and hybrid_ler is not None and hybrid_ler != 0:
        ler_ratio = stim_ler / hybrid_ler

    notes = [
        "Generation mapping: heating_rate = -ln(1-g)/t_cycle and "
        "cz_leak_prob = 8e-4*(g/g_default), with "
        "g_default = 1-exp(-Gamma0*t_cycle), Gamma0 = 1/(700 us). "
        "At g_default these are the literature-default channels; at g=0 "
        "both creation channels are off. The 2023 SI channel ratio is preserved.",
        f"Using LeakageParams defaults: t_cycle={t_cycle} seconds; "
        f"g_default={g_default}. Transport and seepage retain engine defaults.",
        "The readout path is readout_leak_prob = multiplier*g per measurement.",
        "Rise and covariance are reported, not gated, because the supplement "
        "states no uncertainties for S23/S24 and no detector-level target "
        "data is public (SME major 6).",
        "Arm 4 is a prediction, not a fit. removal_boost (default 5.0) is "
        "the v0 Miao-efficacy stand-in, not a fitted efficacy.",
        "Results from this code at reduced scale are machinery demonstrations, "
        "not a verdict on the paper's attribution.",
        f"ratio_tolerance={tolerance} is caller-supplied. Joint scoring uses "
        f"target_ratio={target} and population_ceiling={ceiling}; the default "
        "ratio target 6.6 is the rounded LITERATURE comparison 5.3/0.8.",
        "Baseline ratios against themselves are null. Leakage ratio_ci "
        "results use error counts and retained shots at each N. The baseline "
        "cross-check LER ratio uses per-cycle rates at the largest N.",
        "The cross-check chi-square uses the smaller retained shot count "
        "because detection_curve_chi2 accepts one common count; with unequal "
        "postselected counts this is a conservative common-count approximation.",
        "Logical failure means any observable prediction differs from its "
        "sampled flip. Covariance uses retained detector events. The population "
        "tail starts at floor(curve_length/2).",
        "Undefined or nonfinite numerical results are JSON null; scoring is "
        "null when its ratio or population is unavailable. Rise is null if "
        "rise_summary raises. No pseudocounts are added by this driver.",
    ]
    return _jsonable({
        "config": copy.deepcopy(config),
        "arms": arms,
        "baseline_cross_check": {
            "detection_curve_chi2": chi2,
            "dof": dof,
            "ler_ratio_stim_over_hybrid": ler_ratio,
        },
        "notes": notes,
    })


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) != 3:
        raise SystemExit("Usage: run_sweep.py CONFIG.json RESULTS.json")
    with open(argv[1], encoding="utf-8") as source:
        config = json.load(source)
    results = run_sweep(config)
    with open(argv[2], "w", encoding="utf-8") as destination:
        json.dump(results, destination, indent=2, sort_keys=True, allow_nan=False)
        destination.write("\n")


if __name__ == "__main__":
    main()
