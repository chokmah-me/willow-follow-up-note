# Brief for Astra: hybrid leakage instrument, first build (v0)

You are writing code for a research prototype. Deliver two files only, as two
fenced code blocks in order, with no prose before, between, or after them
except one line naming each file:

1. `leakage_hybrid.py`
2. `test_leakage_hybrid.py`

Constraints: Python 3.12, dependencies are numpy and stim only. No network,
no file I/O in the module, all randomness through a caller-supplied
numpy.random.Generator. Deterministic under a fixed seed. Keep
leakage_hybrid.py under 900 lines and the tests under 300 lines. Every
physical parameter carries a comment naming its source.

## Physics specifications (from the published record, use exactly these)

Pauli+ leakage layer, from Google Quantum AI 2023, arXiv:2207.06431,
supplement Section XIV:
- Each qubit carries a leakage label in {0 = computational, 2, 3}.
- CZ leakage: Kraus sqrt(pt)(|02><11| + |11><02|), pt = 8e-4, leaking only
  the higher-frequency qubit. In a trajectory the pair is in |11> only in
  some branches; the paper's average is 0.25 * pt per CZ. Implement the
  per-CZ probability as a parameter `cz_leak_prob` defaulting to pt, and
  document the simplification in the docstring.
- Passive heating: |1> to |2> at Gamma = 1/(700 microseconds). Per-cycle
  probability p = 1 - exp(-Gamma * t_cycle), t_cycle = 896 ns default.
- Transport: calibrated transitions |22> <-> |13| and |21> <-> |03|
  between measure and data qubits. Implement as: during a CZ between a
  leaked qubit and a computational partner, the label may move to the
  partner with probability `transport_prob` (default 0.1), switchable off
  with `transport_on=False` (the transport-off control).
- CZ with a leaked partner: the non-leaked qubit gets a Z error with
  probability `leaked_partner_z_prob` (default 1.0, the twirled channel).
- Measurement map: the experiment does not resolve leaked states; a
  leaked qubit (|2> or |3>) is read out as 0 or 1 with equal probability
  (50/50). Documented in the 2023 supplement.
- Reset: reset of a leaked qubit sets its label back to computational
  (ideal in-model rule from the 2023 supplement).
- Leakage lifetime: injected |2> decays with a time constant near
  4.4 cycles (Miao et al., Nature Physics 2023). Per-cycle seepage
  probability = 1 - exp(-1 / lifetime_cycles), lifetime_cycles = 4.4
  default. |3> decays to |2>, |2> decays to computational.
- Readout-induced leakage: per measurement event, a computational qubit
  leaks to |2> with probability `readout_leak_prob` (default 0.0; this is
  the swept Arm-3 parameter).
- Removal (for a prediction arm): with removal on, a leaked measure qubit
  is cleared at reset with the ideal rule above and leaked data qubits
  decay faster; model removal as `removal_on` multiplying the seepage
  probability by `removal_boost` (default 5.0). Document that this is a
  stand-in for DQLR-style removal at the Miao efficacy, not a fit.

qevol layer, from Rosenfeld et al. 2026, arXiv:2512.13908v1, supplement
Section XI.2: the input state is a cultivated |T> state, which is not a
stabilizer state, so the simulator carries a superposition of stabilizer
states (branches), each branch a stim TableauSimulator with a complex
coefficient, coefficients below epsilon = 1e-4 dropped, branch count
capped at m_max = 1000.

Fusion design decision (the papers do not publish one; this is ours,
state it in the module docstring): one leakage-label trajectory per shot,
shared by all branches in that shot. Leakage is a classical environment
trajectory; the branches differ only in their stabilizer state and
coefficient.

## Required API

- `@dataclass LeakageParams` with every parameter above plus switches
  `heating_on, cz_leak_on, transport_on, readout_leak_on, removal_on`,
  and a master `enabled` flag. When `enabled=False`, the engine must be
  an exact no-op (labels stay computational, no extra errors): this is
  the no-leakage baseline arm and the null check.
- `class LeakageEngine`: holds labels (numpy int array), the params, and
  the rng. Methods: `heat(n_qubits)`, `cz(i, j, higher_freq)`,
  `measure(i) -> None` (applies readout-induced leakage; the outcome
  mapping lives in the simulator), `reset(i)`, `seep_cycle()`,
  `is_leaked(i)`.
- `class HybridSimulator`: the qevol-style engine.
  - Constructor: `HybridSimulator(n_qubits, params, rng)`.
  - `inject_magic_state(qubit)`: set the branches to the |T> state
    decomposition, (|0> + exp(i*pi/4)|1>) / sqrt(2), as two branches
    whose tableaus prepare |0> and |1> on that qubit.
  - Clifford gates `x, y, z, h, s, cx, cz` applied to every branch.
    `cz` also calls the leakage engine for that pair (the caller states
    which qubit is higher frequency).
  - Pauli noise: `depolarize(qubit, p)` applying a random Pauli with
    total probability p, sampled per branch (SI1000-style hook).
  - `measure(qubit) -> int`: if the qubit is leaked, return a fair
    random bit (the 50/50 map) and do not touch the tableaus. If not
    leaked, the outcome must be sampled correctly for a superposition:
    compute each branch's deterministic-or-random outcome distribution
    from its tableau; where branches disagree, sample the outcome with
    probability weighted by |coefficient|^2 and collapse/reweight the
    branches consistently. Where the correct coherent treatment exceeds
    this prototype (interference between branches on a measurement
    where both branches are random), implement the |coefficient|^2
    mixture rule and document that limitation in the docstring, by name:
    "mixture rule for branch-random measurements; coherent interference
    on such measurements is out of scope for v0".
    After a computational measurement, call the leakage engine's
    readout-leakage hook and, if the measured qubit is a measure qubit,
    its reset (label cleared) via `reset_after_measure(qubit)` when the
    caller asks for it.
  - `branch_count()`, `labels` property exposing the engine labels.
- `run_repetition_memory(n_data, n_cycles, params, shots, seed,
  postselect_first_cycle=False) -> dict`: a small end-to-end memory
  experiment using HybridSimulator: data qubits start in |0>, one
  measure qubit per neighboring pair (or a single reused measure qubit
  per parity check, your choice, documented), each cycle measures the
  parity checks with CZ/CX gates, applies heating and seepage once per
  cycle, records detection events (a detection event is a parity-check
  outcome that differs from the previous cycle's outcome for the same
  check), and returns a dict with:
  - `detection_fraction_per_cycle`: list of floats, mean detection
    fraction per cycle across kept shots,
  - `keep_rate`: fraction of shots kept (if postselect_first_cycle,
    shots with any first-cycle detection event are discarded),
  - `mean_label_population`: mean fraction of qubits leaked per cycle.
  This is the S23-shape observable in miniature: with leakage on, the
  detection fraction should rise over cycles; with leakage off, it
  should stay flat.
- Module docstring: state what this is (a v0 reimplementation of the
  qevol + Pauli+ hybrid from the two public specifications), the fusion
  design decision, the documented simplifications (per-CZ probability,
  mixture rule, removal stand-in), and what it is not (not Google's code,
  not validated at 54 qubits, not the Section V experiment itself).

## Tests (pytest, numpy + stim only, all seeded, total runtime < 60 s)

1. Null check: with `enabled=False`, labels stay all-computational over
   200 cycles of heating/seepage calls, and
   `run_repetition_memory` with leakage off gives a detection fraction
   with no rising trend (last-cycle mean <= first-cycle mean + 0.05).
2. Measurement map: a leaked qubit measured 20000 times gives a 1
   fraction within 0.02 of 0.5.
3. Reset rule: a leaked qubit is computational after `reset`.
4. Steady state: heating plus seepage alone reaches a mean leaked
   population within a factor of 2 of p_heat / (p_heat + p_seep)
   (analytic two-state estimate), with heating and lifetime defaults.
5. Transport off control: with `transport_on=False`, a label never moves
   to a partner qubit during CZ calls; with it on and
   transport_prob = 1.0, it always does.
6. Magic state: after `inject_magic_state`, branch count is 2 and the
   coefficients have modulus 1/sqrt(2) each; a Z measurement of the
   magic qubit over 4000 shots gives a 1 fraction within 0.04 of 0.5.
7. Leakage rises: `run_repetition_memory` with leakage on gives a
   last-cycle detection fraction higher than its first-cycle value by
   at least 0.01, with the fixed seed you choose (tune the demo
   parameters in the test so this holds deterministically).
8. Post-selection: keep_rate is in (0, 1] and drops when leakage is on
   versus off under the same seed and postselect_first_cycle=True.

Write clean, documented code. The tests must pass as written.
