# Brief V1-A: grafting memory circuit + hybrid circuit runner

You are extending an existing, tested prototype. The existing module
`leakage_hybrid.py` is appended at the end of this brief. Do not
rewrite it. Your two new modules import from it.

## Background in one paragraph

The prototype simulates Google's qevol + Pauli+ approach: a
qevol-style branch engine (superpositions of stabilizer states on
Stim tableaus) carrying a Pauli+ leakage layer (labels
{computational, 2, 3}). The target experiment is the grafted-code
memory comparison in Rosenfeld et al. 2026 (arXiv:2512.13908v1),
supplement Section XIV / Fig. S22-S24: a logical state stored in a
grafted surface code for N cycles, logical error per cycle about
5.3% in experiment vs 0.8% in no-leakage SI1000 simulations at
p = 2.3e-3, detection events rising over time (S23), and
time-correlated detector covariance (S24). The Section V design
runs four arms against one SI1000 baseline. This brief builds the
circuit and the shot-by-shot runner. Later briefs add the decoder
pin, metrics, and the sweep driver, so the APIs below are fixed:
implement them exactly.

## Deliverable 1: graft_circuit.py (under 350 lines)

```python
def build_memory_circuit(distance: int, rounds: int, p: float) -> stim.Circuit
def circuit_metadata(circuit) -> dict  # distance, rounds (from construction
    # is not recoverable from a bare circuit; instead return n_qubits,
    # n_detectors, n_observables), keys exactly:
    # {"n_qubits", "n_detectors", "n_observables"}
def role_map(circuit) -> dict  # {"data": sorted list, "measure": sorted list}
def higher_frequency(i: int, j: int, roles: dict) -> int
```

Rules:
- build_memory_circuit uses stim.Circuit.generated with
  "surface_code:rotated_memory_z", passing p to every noise knob
  it exposes (after_clifford_depolarization, before_round_data_
  depolarization, before_measure_flip_probability,
  after_reset_flip_probability). Module docstring states: this is
  the standard SI1000-style mapping used for generated circuits,
  all knobs at one p is a simplification of the paper's weighted
  SI1000; the cultivation and grafting stages of the real
  experiment are abstracted as a post-selected logical preparation,
  and the simulated object is the grafted memory stage, which is
  where S22-S24 live. Distance must be odd and >= 3, rounds >= 1,
  0 <= p <= 0.1, else ValueError.
- role_map: a qubit is a measure qubit if it is ever the target of
  an MR instruction in the flattened circuit; all other qubits are
  data. (For generated memory circuits this gives the standard
  split, e.g. distance 3: 9 data, 8 measure.)
- higher_frequency(i, j, roles): the documented stand-in rule:
  measure qubits count as higher frequency than data qubits (in
  the device's grid the two roles sit at different frequencies);
  within a role, the larger index wins. Deterministic. The CZ
  leakage channel applies to whichever qubit this returns.

## Deliverable 2: hybrid_runner.py (under 600 lines)

```python
def run_circuit(circuit, params, shots: int, seed: int,
                postselect_first_round: bool = False) -> dict
```

Executes the circuit shot by shot on the v0 HybridSimulator plus
LeakageEngine, and returns exactly these keys:
- "det_events": numpy bool array, shape (kept_shots, n_detectors)
- "obs_flips": numpy bool array, shape (kept_shots, n_observables)
- "keep_rate": float
- "detection_fraction_per_round": list of floats, one per round,
  averaged over kept shots (round of a detector = grouping by the
  time coordinate from circuit.get_detector_coordinates(); if a
  detector has no coordinates, raise ValueError, do not guess)
- "mean_label_population_per_round": list of floats, mean fraction
  of qubits with a nonzero leakage label at each round boundary,
  averaged over kept shots (zeros when leakage is disabled)

Execution rules:
- Flatten the circuit first (circuit.flattened()). Walk the
  instructions in order; annotations and gates interleave, which
  is what makes detector bookkeeping exact.
- Supported gate instructions: H, X, Y, Z, S, CX, CZ, R, M, MR,
  TICK. Supported noise instructions: DEPOLARIZE1, DEPOLARIZE2,
  X_ERROR, Y_ERROR, Z_ERROR. Supported annotations: DETECTOR,
  OBSERVABLE_INCLUDE, SHIFT_COORDS (ignore), QUBIT_COORDS
  (ignore). Anything else: raise ValueError naming the instruction.
- Noise is sampled independently per branch using the simulator's
  Generator (the v0 convention): DEPOLARIZE1(q) with the given
  probability applies a uniform random non-identity Pauli to that
  branch; DEPOLARIZE2 applies a uniform random non-identity
  two-qubit Pauli; X_ERROR/Y_ERROR/Z_ERROR apply that Pauli with
  the given probability. Noise probabilities come from the
  instruction's float argument.
- CZ goes through HybridSimulator.cz with higher_frequency from
  graft_circuit.higher_frequency and the circuit's role_map.
  CX goes through HybridSimulator.cx with the same higher_frequency
  rule (pass it explicitly).
- M measures without reset; MR measures then calls
  reset_after_measure. Measurements of leaked qubits return the
  fair random bit (v0 measure already does this). Record every
  measurement outcome in order.
- DETECTOR annotation: its targets are rec[-k] references; the
  event is the XOR (parity) of the referenced measurement
  outcomes. OBSERVABLE_INCLUDE: XOR its referenced outcomes into
  that observable's flip. Compute both from the recorded outcomes
  at the point the annotation appears (all referenced measurements
  have already happened in a well-formed circuit).
- Round boundaries: at each TICK, first call engine.heat(all
  qubits) then engine.seep_cycle(), then record the mean label
  population. (Heating and seepage are per-cycle processes; TICK
  is the cycle boundary in generated circuits. The first TICK
  comes after the first round's gates, so population index 0 is
  "after round 1"; detection_fraction_per_round groups detectors
  by their time coordinate, which starts at the first round, so
  the two lists align by round: state this alignment in the
  docstring.)
- Post-selection: if postselect_first_round, a shot is discarded
  when any detector whose time coordinate equals the first
  round's time has event 1. Discarded shots still run to
  completion (so the RNG stream stays shot-aligned, the v0
  convention); they are excluded from every returned array and
  average. If no shots are kept, det_events/obs_flips are empty
  arrays of the right width and the per-round lists are NaN.
- Deterministic under a fixed seed. No network, no file I/O.
  Dependencies: numpy, stim, and the local leakage_hybrid module.

## Deliverable 3: test_graft_and_runner.py (under 300 lines, pytest, total runtime under 120 seconds)

1. test_circuit_shape: distance 3, rounds 3, p=0.002: metadata
   n_qubits == 17, n_detectors > 0, n_observables == 1; role_map
   gives 9 data and 8 measure, disjoint, covering all qubits.
2. test_noiseless_runner_is_silent: p=0 circuit, rounds 4,
   LeakageParams(enabled=False), 200 shots: det_events all False,
   obs_flips all False, keep_rate == 1.0, population all 0. (This
   is the interpreter's correctness anchor: any bookkeeping error
   shows up here.)
3. test_noisy_runner_produces_events: p=0.01, rounds 4, leakage
   disabled, 300 shots: some detector events, obs flip fraction
   strictly between 0 and 0.5.
4. test_leakage_population_and_postselection: p=0.002, rounds 6,
   default LeakageParams, 300 shots: some round has mean label
   population > 0; with enabled=False it is all zero; with
   postselect_first_round=True keep_rate is in (0, 1].
5. test_runner_determinism: same seed twice gives identical
   det_events and obs_flips arrays.
6. test_higher_frequency_rule: with the d3 role map, a data/measure
   pair returns the measure qubit; a data/data pair returns the
   larger index.

## Style constraints (match the existing module)

- Module docstrings state what the code is, what it simplifies,
  and what it is not. No silent invention: where the paper does
  not specify something (the frequency stand-in, the SI1000 knob
  mapping, the cultivation abstraction), the docstring says so.
- Every physical or design parameter carries a comment naming its
  source: the design (Section V simulation design, 2026-10-16),
  the paper, or "our stand-in".
- No global state; all randomness from numpy Generators seeded by
  the caller.
- Output only the three files as fenced code blocks, one naming
  line before each. No other prose.
