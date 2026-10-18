# Brief V1-C: the four-arm sweep driver

You are adding the final module to an existing tested prototype.
Do not modify any existing file. Consume these APIs exactly:

- graft_circuit.build_memory_circuit(distance, rounds, p) -> stim.Circuit
- hybrid_runner.run_circuit(circuit, params, shots, seed,
  postselect_first_round=False) -> dict with keys det_events,
  obs_flips, keep_rate, detection_fraction_per_round,
  mean_label_population_per_round
- leakage_hybrid.LeakageParams (dataclass; fields include
  enabled, cz_leak_prob, heating_rate, t_cycle, lifetime_cycles,
  readout_leak_prob, removal_on, removal_boost)
- decoder_pin.decode(circuit, det_events) -> bool array of
  observable predictions; decoder_pin.write_pin(path, circuit)
- metrics: per_cycle_rate(p_logical, n_cycles),
  ratio_ci(arm_errors, arm_shots, base_errors, base_shots),
  detection_curve_chi2(a, b, shots), covariance_matrix(events),
  lag_profile(cov, detector_rounds), rise_summary(curve),
  evaluate_joint(observables, targets, tolerances)
- device_params: DeviceParams, LITERATURE dict

## The design being implemented (Section V design, 2026-10-16, plus SME review majors)

Four arms against one SI1000 baseline at p = 2.3e-3, same decoder
(Tesseract, via decoder_pin) everywhere:
1. baseline: no leakage. Must be run two ways: "baseline_stim"
   (Stim's own detector sampler) and "baseline_hybrid" (the v0
   hybrid runner with leakage disabled). Their agreement is the
   engine cross-check; report it, do not hide it.
2. leakage: generation rate swept over a grid, lifetime swept
   over a grid (2D, per SME review). Transport and seepage on,
   no removal.
3. leakage_readout: the Arm 2 point(s) with an elevated
   generation path on the redefined measure qubits, multiplier
   swept. In this engine the readout path is the
   readout_leak_prob parameter (per measurement, and only
   measure qubits are measured mid-circuit): set it to
   multiplier * g for swept g.
4. leakage_removal: Arm 2 at each grid point with removal on
   (removal_on=True, removal_boost from config, default 5.0,
   documented in v0 as a Miao-efficacy stand-in, not a fit).
   This arm is a prediction, not a fit.

Generation mapping (our documented mapping of the design's
single generation knob onto the two published channels): swept
per-cycle generation g sets heating_rate = -ln(1-g)/t_cycle AND
scales cz_leak_prob = 8e-4 * (g / g_default), where g_default =
1 - exp(-Gamma0 * t_cycle) with Gamma0 = 1/(700 us) (the default
per-cycle heating probability, about 0.00128). At g = g_default
the arm runs exactly the literature defaults; at g = 0 both
creation channels are off (a true zero point). The channel ratio
stays at the 2023 SI parameterization throughout.

Post-selection: every arm runs with the config's
postselect_first_round flag; keep_rate is reported for every
point (the fourth observable, per SME review).

## Deliverable: run_sweep.py (under 500 lines)

```python
def run_sweep(config: dict) -> dict
def main(argv=None)  # reads a JSON config path from argv[1],
    # writes results JSON to argv[2]
```

Config keys (all required unless noted): distance, rounds_list
(list of cycle counts N; each arm point runs every N),
p (default 2.3e-3), shots, seed, generation_grid (list),
lifetime_grid (list), readout_multipliers (list, may be empty),
removal_boost (optional, default 5.0), postselect_first_round
(bool), target_ratio (default 6.6, from LITERATURE: 5.3/0.8),
ratio_tolerance (required; the caller's, labeled as such in the
output), population_ceiling (default 0.01, the design's
steady-state |2> bound).

Per arm point, compute and record (JSON-serializable types only):
- ler_per_cycle: decode det_events with decoder_pin.decode;
  logical errors = predictions XOR obs_flips (for the stim arm,
  obs from the sampler); take the largest N in rounds_list:
  p_logical = mean logical error there, then
  metrics.per_cycle_rate(p_logical, N). Also record p_logical
  and n_logical_errors and shots_kept for every N.
- ratio_vs_baseline_hybrid (Arm 2/3/4 points): ratio_ci of the
  point's logical errors vs baseline_hybrid's at the same N.
  Arms 1 report ratio 1.0 against themselves by construction;
  record null instead, plus the baseline cross-check (below).
- detection_fraction_per_round (hybrid points: from the runner;
  stim point: group sampled events by detector time coordinate,
  same rule as the runner: distinct third coordinates from
  get_detector_coordinates).
- rise: metrics.rise_summary of that curve (null if it raises).
- covariance_lag1_excess: lag_profile(cov)[1] of this point
  minus lag_profile(cov of baseline_hybrid)[1], both at the
  largest N (null for baseline arms themselves; for
  baseline_stim report it against baseline_hybrid). Detector
  round indices come from get_detector_coordinates (third
  coordinate, as ints).
- steady_population: mean of the last half of
  mean_label_population_per_round at the largest N (null for
  the stim arm, which has no labels; 0.0 for baseline_hybrid).
- keep_rate at the largest N.
- score: metrics.evaluate_joint with observables
  {"ratio": ratio, "steady_population": steady_population},
  targets {"ratio": target_ratio, "steady_population": 0.0},
  tolerances {"ratio": ratio_tolerance,
  "steady_population": population_ceiling}; leakage arms only,
  null elsewhere. evaluate_joint's cov_distance special case is
  not used here.

Top-level results dict: {"config": config echo, "arms":
{"baseline_stim": {...}, "baseline_hybrid": {...}, "leakage":
[point, ...], "leakage_readout": [point, ...],
"leakage_removal": [point, ...]}, "baseline_cross_check":
{"detection_curve_chi2": ..., "dof": ..., "ler_ratio_stim_over_hybrid": ...},
"notes": [strings]}. Point dicts carry their grid coordinates
(generation, lifetime, multiplier where relevant). The notes
list must include, verbatim in substance: the generation
mapping; that rise and covariance are reported, not gated,
because the supplement states no uncertainties for S23/S24 and
no detector-level target data is public (SME major 6); that
Arm 4 is a prediction; and that results from this code at
reduced scale are machinery demonstrations, not a verdict on
the paper's attribution.

Seeds: derive each point's seed deterministically from the
config seed and the point's indices (seed + a stable offset),
so reruns reproduce exactly.

Validation: unknown arm names, empty grids where an arm needs
them, nonpositive shots, or a rounds_list with fewer than 1
entry raise ValueError. No network. Stim arm sampling: use
circuit.compile_detector_sampler().sample(shots, append_observables=True)
or the closest current Stim API; separate observables from
detector events by shape.

## Deliverable: test_run_sweep.py (under 250 lines, pytest, under 120 seconds)

Tiny config: distance 3, rounds_list [3, 5], p 0.002, shots 200,
generation_grid [0.0, 0.002], lifetime_grid [4.4],
readout_multipliers [3.0], ratio_tolerance 5.0,
postselect_first_round False.
1. Structure: all five arm keys present; leakage has 2 points,
   leakage_readout has 2, leakage_removal has 2; every point
   has ler_per_cycle, keep_rate in [0, 1], and a score for
   leakage points with generation > 0.
2. Zero point: the leakage point at generation 0.0 has
   steady_population == 0.0.
3. Removal works directionally: at generation 0.002,
   leakage_removal steady_population <= leakage
   steady_population.
4. Baseline cross-check exists with dof > 0 and a finite
   chi2; baseline_hybrid detection curve length equals
   rounds max + 1.
5. json.dumps(results) succeeds (serializability).
6. Determinism: a second run_sweep with the same config gives
   identical ler_per_cycle for baseline_hybrid.

## Style

Module docstring states the design source, the generation
mapping, what is gated and what is only reported and why, and
the reduced-scale caveat. No silent invention. Output only the
two files as fenced code blocks, one naming line before each,
no other prose.
