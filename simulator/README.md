# Willow leakage hybrid simulator, v0

First build of the instrument the Section V leakage-injected
re-simulation needs, written 2026-10-17 by OpenAI GPT-6 Astra
(`openai/gpt-6-astra` via OpenRouter, one call, $0.4097) at the
user's instruction, from the brief in `ASTRA-BRIEF.md`. The brief's
physics comes from the tool survey delivered the same day
(`~/workspace/your_files/willow-leakage-simulator-survey/`).

## What is here

- `leakage_hybrid.py`: a qevol-style branch engine (superpositions of
  stabilizer states on Stim tableaus, coefficients, epsilon = 1e-4
  cutoff, m_max = 1000, per Rosenfeld et al. 2026, arXiv:2512.13908v1
  supplement Section XI.2) carrying a Pauli+ leakage layer (per
  Google Quantum AI 2023, arXiv:2207.06431 supplement Section XIV):
  labels {computational, 2, 3}; CZ leakage at pt = 8e-4 on the
  higher-frequency qubit; passive heating at 1/(700 us); transport
  |22> <-> |13| and |21> <-> |03| with a transport-off control; a Z
  channel on the partner of a leaked qubit during CZ; the 50/50
  readout map for leaked states; reset clearing the label; seepage
  with the 4.4-cycle lifetime from Miao et al. 2023; a swept
  readout-induced leakage parameter (the design's Arm-3 knob); and a
  removal stand-in (seepage boost) for the prediction arm.
- Fusion decision (ours, the papers do not publish one): one
  leakage-label trajectory per shot, shared by all branches.
- `run_repetition_memory`: a miniature repetition-code memory
  experiment that returns the observables in small: detection
  fraction per cycle (the S23 shape), post-selection keep rate, and
  mean leaked population per cycle. Its baseline arm carries SI1000
  style Pauli noise at p = 2.3e-3.
- `test_leakage_hybrid.py`: 15 seeded tests, all passing
  (9.4 s, Python 3.12, stim + sinter + numpy in `.venv`).

## Review and fixes after the Astra delivery

The main agent read every line and ran the tests before accepting
anything. One fix was applied by hand on 2026-10-17: Astra's first
version had no baseline Pauli noise, so the no-leakage arm read
exactly zero, which is not the paper's baseline. `run_repetition_memory`
now applies the SI1000 stand-in noise (p = 2.3e-3 per qubit per cycle)
and three tests were updated from "exactly zero" to "nonzero but
flat". All 15 tests pass after the fix. Astra's documented
simplifications stand as written in the module docstring: the per-CZ
leakage probability is not conditioned on the |11> population, the
measurement rule for branch-random measurements is the |coefficient|^2
mixture rule (coherent interference on such measurements is out of
scope for v0), heating is not conditioned on the |1> population, and
the removal boost is a stand-in, not a fit.

Contract check, 2026-10-17 (files in `contract-check/`): certifier
15/15 shipped tests + 14/14 probes against the brief; breaker
BREAK 0 / WEAKENS 3 / SURVIVES 9. Two suite blindnesses found and
dispositioned (a leaked-partner CZ test added; the coefficient
reweight shown unobservable in v0 because branches stay
Pauli-related, the invariant now pinned by a test). One behavior
pinned as a tripwire: truncation at the m_max branch cap is silent,
so a caller past the rank budget gets a renormalized state with no
warning. Suite now 18/18. The mixture rule's cost is quantified in
the adjudication: exact for the detector measurements a memory
experiment uses, wrong by +0.36 on a rotated-basis readout of a
magic state.

## Measured behavior (seeded, this machine)

Paper defaults, 400 shots, 25 cycles, 3 data qubits:
- Leakage on: detection fraction 0.005 in cycle 1 to 0.013 in
  cycle 25; leaked population 0.50% at cycle 25 (analytic two-state
  steady estimate 0.63%).
- Leakage off: 0.001 to 0.006, flat within noise.
- Keep rate with first-cycle post-selection: 0.990 on, 0.998 off.

The rise at paper defaults is small because leakage is a ~1%
effect. The test suite's accelerated demo (heating exposure and
lifetime swept far off the paper values, labeled uncalibrated in
the test code) shows the S23 shape plainly: detection fraction
0.079 to 0.459 over 20 cycles.

## V1: the rest of the gap list (built 2026-10-17, same method)

Three more Astra calls ($0.4319 + $0.3864 + $0.4541), briefs in
`ASTRA-BRIEF-V1A/B/C.md`, each reviewed and tested on arrival.
59 tests pass across all modules.

- `graft_circuit.py`: the grafted memory stage as a Stim circuit
  (rotated surface code memory from Stim's generator, all SI1000
  knobs at one p, a documented simplification). Cultivation and
  grafting are abstracted as a post-selected logical preparation;
  the simulated object is the memory stage where S22-S24 live.
  Also the qubit role map and the higher-frequency stand-in rule.
- `hybrid_runner.py`: executes the circuit shot by shot on the v0
  engine, with exact detector and observable bookkeeping from the
  circuit annotations. Main-agent revision on arrival: generated
  circuits have 7 TICKs per round, so heating and seepage are
  grouped per round, not per TICK.
- `device_params.py`: the parameter table. Verified aggregate
  defaults and the literature constants for the leakage rates
  (the figures carry no per-qubit leakage rates, so the leakage
  table stays aggregate). The device table printed in Figs.
  S5/S7/S9 is digitized separately, in `digitize/` (below).
- `decoder_pin.py`: Tesseract (installed snapshot
  0.1.1.dev20261013012529), long-beam factory decoder. Its actual
  settings match the survey's starting config exactly (pqlimit
  1,000,000, det_beam 20, beam climbing, 21 detector orders, no
  detector revisits). The pin is behavioral: versions, decoder
  names, applied settings, and a SHA-256 fingerprint of the
  decoder's predictions on a fixed probe. Main agent fixed the
  compile-method name the installed snapshot actually exposes.
- `metrics.py`: per-cycle logical rate (the standard fit form),
  ratio with confidence interval, chi-square on detection curves,
  detector covariance, lag profile, rise summary, the joint
  evaluator.
- `run_sweep.py`: the design's four arms. Baseline run two ways
  (Stim's sampler and the hybrid runner) with their agreement
  reported as a cross-check. Leakage on a 2D generation-by-
  lifetime grid with a documented mapping of the generation knob
  onto the heating and CZ channels. Readout arm via the
  readout-leakage multiplier. Removal arm as the prediction.
  Keep rate at every point. Rise and covariance reported, not
  gated (the supplement publishes no uncertainties for them).

Demonstration run (`sweep-demo-results.json`, distance 3, 2,000
shots per point, 6m52s on this VM): the two baseline engines'
detection curves agree (chi-square 3.19 on 10 degrees of
freedom); their logical rates differ by a factor 0.63 on roughly
13 to 20 counted errors each, inside counting noise. Leakage
raises the logical rate monotonically with generation (ratio
0.58 at the zero point, 1.37 at literature defaults, 2.05 at
g = 0.3%), raises the lag-1 covariance excess monotonically,
the readout arm adds damage on top (2.63), and the removal arm
returns the ratio to about 1.1 with the steady population at
zero. Directionally the design's machinery works end to end.
Distance 3 compresses the ratio; the design's real test is
distance 5 at about 100,000 shots per point, which is hours to
days of compute beyond this VM's interactive use (the hybrid
runner costs about 24 ms per shot at distance 5).

## What this is not

- Not Google's code, and not validated at 54 qubits. The toy memory
  is 3 data qubits; nothing here reproduces S22(d)-(f) or the
  0.8%/cycle figure.
- Not yet the Section V experiment at full scale. Gaps 2, 4, 5,
  and 6 are built (decoder pin, detector/covariance pipeline,
  metrics, sweep driver). Gap 3 is closed as far as the source
  allows: the values in Figs. S5/S7/S9 are printed text in the
  PDF, and `digitize/device-values.json` now holds all of them
  (54 qubits x 15 quantities, 89 CZ pairs x 2), extracted by cell
  geometry and cross-validated (see
  `digitize/DIGITIZATION-REPORT.md`). What remains
  before a verdict-grade run: distance-5 execution at design
  shot counts (a compute problem, roughly 40 minutes per point
  per cycle count at 100k shots on this class of machine), and
  Google's detector-level S23/S24 data, which is not public, so
  the joint fit against their curves cannot be scored from
  outside. The v0 core's two named limits stand: the scalable
  fusion at 54 qubits is exercised only through the memory
  circuit's branch structure, and the coherent measurement
  treatment is out of scope.
- Committed 2026-10-17 at the user's word to the private repo
  chokmah-me/willow-follow-up-note, under `simulator/`. The
  working copy stays at ~/workspace/willow-leakage-sim on the VM;
  the repo copy is the record. Nothing public.

## Cost

OpenRouter key spend before this build: $1.0470. Astra call:
$0.4097 (2,342 prompt + 7,609 completion tokens). Key total after:
$1.4567 of the $50 key limit; the user's standing $12 cap governs.
Key expires 2026-10-22T18:52:18.954Z.
V1 calls: $0.4319 + $0.3864 + $0.4541 = $1.2724. Total Astra
spend on this project: $1.6821. Key total at the end of the v1
build: $2.7291.
