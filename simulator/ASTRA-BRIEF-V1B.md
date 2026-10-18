# Brief V1-B: device parameters, decoder pin, metrics

You are adding three modules to an existing tested prototype
(Stim + numpy + sinter; a v0 leakage engine `leakage_hybrid.py`
with dataclass `LeakageParams`, and a `graft_circuit.py` with
`build_memory_circuit(distance, rounds, p) -> stim.Circuit`).
Do not modify any existing file. Implement the APIs exactly;
a later sweep brief consumes them.

## Context

Experiment: grafted-code memory comparison in Rosenfeld et al.
2026 (arXiv:2512.13908v1) supplement Sections V and XIV. The
Section V design (2026-10-16) scores four simulation arms on
joint observables: (a) logical error ratio vs the
SI1000 baseline (target about 6.6, that is 5.3/0.8), (b) the S23
detection-likelihood rise shape, (c) the S24 detector covariance
structure, plus (d) the post-selection keep rate (added by SME
review). The supplement publishes device parameters only as
figure distributions (Figs. S5-S9), not tables, so per-qubit
digitization does not exist yet; this brief builds the data
layer honestly around that fact. The decoder is Tesseract
(Google's most-likely-error decoder, named by SME review), now
installed as a dated dev snapshot; the pin must be behavioral,
because the paper publishes no version or settings behind its
0.8%/cycle figure.

## Deliverable 1: device_params.py (under 250 lines)

```python
@dataclass QubitParams:  # defaults are the verified aggregates
    cz_leak_prob: float = 8e-4        # 2023 SI Sec. XIV: pt
    heating_rate: float = 1.0/700e-6  # 2023 SI Sec. XIV: Gamma
    t_cycle: float = 896e-9           # 2023 SI Sec. XIV
    lifetime_cycles: float = 4.4     # Miao et al. 2023
    readout_leak_prob: float = 0.0    # Arm-3 swept knob

LITERATURE: dict  # named constants with source comments:
    # generation band 0.09e-2..0.11e-2 per cycle (McEwen 2021 fits)
    # steady-state |2> population 0.97e-2..1.30e-2 (McEwen 2021)
    # lifetime 4.4 cycles (Miao 2023)
    # removal: excess |2> < 1e-3 within 2 cycles (Miao 2023)
    # SI1000 baseline p = 2.3e-3 (cultivation supplement Sec. XIV)
    # experiment per-cycle logical error 5.3e-2, simulated 0.8e-2
    #   (cultivation supplement Sec. XIV / Fig. S22 fit values)

@dataclass DeviceParams:
    default: QubitParams
    overrides: dict  # qubit index -> QubitParams
    digitization_status: str = "aggregate_only_not_digitized"
    def for_qubit(self, i) -> QubitParams
    def uniform_leakage_params(self, **overrides) -> LeakageParams
        # build a v0 LeakageParams from the defaults (cz_leak_prob,
        # heating_rate, t_cycle, lifetime_cycles, readout_leak_prob),
        # then apply keyword overrides; import LeakageParams from
        # leakage_hybrid.
    def save_json(self, path) / @classmethod load_json(cls, path)
    def analytic_steady_state(self) -> float
        # p_gen/(p_gen + p_seep) with p_gen = 1-exp(-heating_rate*t_cycle)
        # and p_seep = 1-exp(-1/lifetime_cycles), from the defaults.
```

Validation: probabilities in [0,1], positive rates/times, else
ValueError. JSON roundtrip must preserve overrides and status.
Module docstring states plainly: per-qubit values from Figs.
S5-S9 are NOT digitized; every qubit currently gets the verified
aggregate defaults, and the status field says so wherever the
table travels. No invented per-qubit numbers anywhere.

## Deliverable 2: decoder_pin.py (under 300 lines)

The installed package is `tesseract-decoder`, import name
`tesseract_decoder`; it exposes `make_tesseract_sinter_decoders_dict()`
returning a dict of sinter.Decoder-style objects, and
`TesseractSinterDecoder`. Its exact version string comes from
importlib.metadata.version("tesseract-decoder").

```python
LONG_BEAM_REQUEST: dict  # the survey's starting config, keys:
    # {"pqlimit": 1000000, "det_beam": 20, "beam_climbing": True,
    #  "det_orders": 21, "no_revisit_dets": True}
    # marked in code comments as requested, from the Tesseract
    # documentation's long-beam example (survey, 2026-10-17).

def available_decoders() -> list  # sorted keys of the factory dict
def get_decoder():  # first available decoder object; RuntimeError
    # with a clear message if the dict is empty.
def write_pin(path, circuit) -> dict
def check_pin(path, circuit) -> tuple  # (matches: bool, diffs: list[str])
def decode(circuit, det_events) -> numpy bool array  # observable
    # predictions, shape (shots, n_observables)
```

- write_pin records: tesseract_version, stim_version,
  sinter_version, pymatching_version (importlib.metadata each),
  available decoder names, LONG_BEAM_REQUEST as
  "requested_config", and a behavioral fingerprint: build the
  DEM from the given circuit (circuit.detector_error_model(
  decompose_errors=True)), compile the decoder for it through
  the sinter protocol, decode a fixed synthetic sample set
  (all-zero events plus 64 samples from a seeded Generator with
  per-detector flip probability 0.02), and store the SHA-256 of
  the concatenated prediction bytes plus the sample count.
  Returns the pin dict and also writes it as JSON to path.
- check_pin recomputes the fingerprint for the given circuit and
  reports (True, []) only if version, decoder names, and
  fingerprint all match the stored pin; otherwise (False, diffs)
  with one human-readable string per mismatch. This is the
  behavioral pin: Google published no version/settings behind
  0.8%/cycle, so we pin OUR decoder's behavior on a fixed input,
  and any silent behavior change breaks the pin loudly.
- decode uses the same compiled-decoder path (sinter protocol:
  decoder.compile_for_dem(dem) then decode_shots_bit_packed or
  the closest equivalent the installed objects expose; if the
  installed snapshot lacks the protocol, raise RuntimeError
  naming what is missing, do not fake it).
- Deterministic; no network. File I/O only in write_pin /
  check_pin / load paths.

## Deliverable 3: metrics.py (under 350 lines)

Pure functions, numpy only.

```python
def per_cycle_rate(p_logical: float, n_cycles: int) -> float
    # epsilon = (1 - (1 - 2*p_logical)**(1/n_cycles)) / 2, the
    # standard fit form P_L(N) = 0.5*(1 - (1-2e)^N) used in
    # Google's QEC papers. ValueError unless 0 <= p < 0.5 and
    # n_cycles >= 1.
def ratio_ci(arm_errors, arm_shots, base_errors, base_shots,
             z: float = 1.96) -> tuple  # (ratio, lo, hi), log-normal
    # delta method on log ratio of two binomial proportions.
    # ValueError on nonpositive shots or zero base errors.
def detection_curve_chi2(curve_a, curve_b, shots_per_point) -> tuple
    # (chi2, dof): binomial variance per point from curve_b,
    # dof = number of points. ValueError on length mismatch or
    # a zero-variance point.
def covariance_matrix(det_events) -> numpy array  # detectors x
    # detectors covariance over shots (float conversion).
def matrix_distance(a, b) -> float  # ||a-b||_F/(||a||_F+||b||_F),
    # 0.0 if both are zero; ValueError on shape mismatch.
def lag_profile(cov, detector_rounds) -> dict  # lag -> mean
    # covariance over detector pairs whose round indices differ
    # by that lag (diagonal excluded except lag 0 uses i<j pairs
    # in the same round); the S24 time-correlation signature.
def rise_summary(curve) -> dict  # {"first": mean of first third,
    # "last": mean of last third, "relative_rise": (last-first)/first}
    # ValueError if first == 0 or fewer than 3 points.
def evaluate_joint(observables: dict, targets: dict,
                   tolerances: dict) -> dict
    # For each key present in all three dicts: pass if
    # |observed - target| <= tolerance (for "cov_distance" the
    # target is 0 and the check is observed <= tolerance).
    # Returns {"per_observable": {key: bool}, "joint": bool}.
    # ValueError if a key is missing from any dict.
```

## Deliverable 4: test_sim_v1b.py (under 300 lines, pytest, under 60 seconds)

1. DeviceParams defaults match the verified aggregates; analytic
   steady state is within a factor 2 of the McEwen band midpoint
   (about 1.1%); JSON roundtrip preserves an override and the
   status string; invalid probability raises ValueError.
2. uniform_leakage_params returns a LeakageParams whose fields
   equal the defaults, and a keyword override lands.
3. Decoder pin: write_pin on a distance-3 memory circuit to a
   tmp path; check_pin returns (True, []); available_decoders is
   nonempty; decode of all-zero events returns all-zero
   predictions of the right shape.
4. per_cycle_rate roundtrip: pick epsilon 0.01, N 25, compute
   P_L from the fit form, recover epsilon to 1e-9.
5. ratio_ci: 100 errors / 10000 shots vs 10 / 10000 gives a ratio
   near 10 whose interval contains 10 and excludes 1.
6. detection_curve_chi2 of a curve against itself is 0.
7. covariance_matrix on two perfectly correlated detector columns
   gives off-diagonal equal to the variance (to 1e-9); lag_profile
   on a hand-built 3-detector example returns the hand-computed
   means; matrix_distance(a, a) == 0 and matrix_distance(a, -a)
   == 1 (for nonzero a).
8. rise_summary on a linear ramp 1..9 gives relative_rise 2.0
   (first third mean 2, last third mean 6, (6-2)/2 = 2).
9. evaluate_joint: all-pass case gives joint True; moving one
   observable outside tolerance gives joint False and that key
   False; a missing key raises ValueError.

## Style

Docstrings state sources and limits in the house style of the
existing modules: what is verified, what is a stand-in, what is
not claimed. No silent invention. Output only the four files as
fenced code blocks, one naming line before each, no other prose.
