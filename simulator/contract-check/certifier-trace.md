# Contract check: certifier trace (spec-faithful pass)

Contract: `ASTRA-BRIEF.md` (the human-supplied criteria; trusted source).
Code: `leakage_hybrid.py` as delivered by Astra 2026-10-17, plus the
main agent's documented baseline-noise fix the same day.
Date: 2026-10-17. Runner: `.venv/bin/python` (stim 1.16.0).

## Receipts

- Shipped suite: 15/15 pass in 9.54 s (re-run for this check).
- Certifier probes (`contract-check/certifier-probes.py`): 14/14 pass.
  Two probes failed on first run; both were probe bugs, not code bugs,
  and are recorded here rather than hidden:
  - C15 epsilon probe used epsilon = 0.6, which is below 1/sqrt(2) =
    0.707, so both |T> branches correctly survive the cutoff. Fixed to
    0.8; the code then fails loud with RuntimeError when all mass is
    pruned, exactly as the code's `_prune` guard promises.
  - C16 zero-kept probe tried to force discards through the readout
    leakage parameter; that path cannot discard first-cycle shots
    (readout leakage is applied after the outcome, and measure qubits
    are reset every cycle). Re-forced through base_pauli_p = 1.0; the
    zero-kept case then returns NaN lists and keep_rate 0.0, as the
    `run_repetition_memory` docstring states.

## Decision table: brief criterion -> evidence

| Criterion | Evidence |
|---|---|
| Parameter defaults (pt 8e-4, heating 1/(700 us), t_cycle 896 ns, lifetime 4.4, epsilon 1e-4, m_max 1000, readout leak default 0, transport 0.1, partner Z 1.0, removal boost 5.0) | Probe C1 PASS; shipped tests use the defaults throughout |
| p_heat = 1 - exp(-Gamma * t_cycle); p_seep = 1 - exp(-1/lifetime); removal multiplies p_seep by boost, clipped at 1 | Probe C2 PASS (exact to 1e-12) |
| enabled=False is an exact no-op, labels and RNG untouched | Shipped test_disabled_null_check PASS (RNG state compared) |
| Heating hits computational labels only, per cycle | Engine code + steady-state shipped test PASS (measured within a factor 2 of the analytic p_heat/(p_heat + p_seep)) |
| CZ creation only on the higher-frequency qubit, only when both partners are computational | Shipped test_creation_higher_frequency_and_removal_cascade PASS (pt forced to 1.0, label lands on qubit 1, not 0) |
| CZ with leaked partner: Z error on the partner; transport moves the label (3 preserved as 3), transport_off control holds the label in place | Shipped test_transport_off_and_on PASS for labels 2 and 3, both directions, error tuples checked |
| Leaked measurement map: 50/50, tableau untouched, label unchanged | Shipped test_leaked_measurement_map PASS (20,000 draws, both labels, tableau compared before/after) |
| Reset clears the label; reset_after_measure also restores the surrogate to |0> | Shipped test_reset_rule PASS, both labels |
| Seepage cascade 3 -> 2 -> 0, never both steps in one cycle | Shipped removal cascade assertions PASS ([3,2] -> [2,0] -> [0,0] under a clipped boost) |
| Readout-induced leakage fires after a computational measurement; readout_leak_on=False kills it | Shipped test_readout_leakage_hook_and_explicit_reset PASS; probe C18c PASS |
| Every mechanism switch off fully disables its mechanism | Probes C18a (heating), C18b (CZ creation), C18c (readout), shipped transport test |
| Magic injection: exactly 2 branches, coefficients 1/sqrt(2), phase ratio e^{i pi/4}; raises on leaked target, raises on non-|0> target | Shipped test_magic_state_and_z_measurement PASS; probes C11a/C11b PASS |
| Clifford gates + CX agree with Stim on stabilizer states | Probe C12 PASS (30 random circuits, peek_x/y/z on all qubits vs a TableauSimulator reference) |
| Depolarize: per branch, total probability p, invalid p raises ValueError, p = 0 is a no-op | Probe C13 PASS |
| Epsilon cutoff: prunes below 1e-4; all-mass pruning fails loud, not silent | Probe C15a PASS (RuntimeError at epsilon = 0.8) |
| m_max cap: truncates to the cap and renormalizes to sum |c|^2 = 1 | Probe C15b PASS (m_max = 2, two injections) |
| Hostile inputs raise the named errors (ValueError for bad probabilities, lifetime, m_max, run args; IndexError for bad qubit index) | Probe C17 PASS |
| run_repetition_memory returns the three named observables; zero kept shots gives NaN lists and keep_rate 0 | Shipped demo tests PASS; probe C16 PASS |
| Deterministic under a fixed seed, across processes | Shipped test_seeded_reproducibility PASS; probe C19 PASS (two separate processes, byte-identical JSON) |
| Brief's 8 required tests all present and passing | Shipped suite maps 1:1 (null, map, reset, steady state, transport, magic, rise, post-selection) plus 7 more |

## Spec gaps pinned for adjudication (not silently resolved)

- G1: No mechanism creates label 3. The brief lists labels {c, 2, 3},
  the 3 -> 2 decay, and transport preserving 3, but never a generation
  rate into |3>. The Section V design itself flagged the same hole
  ("|3> generation: state the assumption"). Code follows the brief
  literally: |3> is reachable only by direct label injection in tests.
  Candidate adjudications: (a) accept for v0, |3> is a bookkeeping
  state carried for the decay chain; (b) add a second-order generation
  rule (a fixed ratio to |2> generation) in v1.
- G2: `base_pauli_p` in run_repetition_memory is an addition past the
  brief (the main agent's 2026-10-17 fix). The brief's required API
  does not name it, but the Section V design requires a nonzero
  SI1000 baseline arm; the addition is documented in the function
  docstring and the README. Candidate adjudication: ratify as part of
  the runner contract for v0.
- G3: The brief sanctions the |coefficient|^2 mixture rule for
  branch-random measurements by name. The breaker pass quantifies
  what that rule costs against exact statevector references; the
  number belongs in the adjudication, not in this trace.

## Certifier verdict

Every criterion in the brief is either covered by a passing shipped
test, a passing certifier probe, or pinned above as a gap. CERTIFIED
against the brief as written, with G1-G3 carried to adjudication.
