# Contract check adjudication: Astra leakage simulator v0

Date: 2026-10-17. Contract: `ASTRA-BRIEF.md`. Code: `leakage_hybrid.py`.
Passes: certifier (`certifier-trace.md`), breaker (`breaker-findings.md`,
8 probe scripts in this folder, all re-run or spot-verified by the
main agent before adjudication).

## Tallies

- Certifier: shipped suite 15/15, certifier probes 14/14, every brief
  criterion covered by a passing test, a passing probe, or a pinned gap.
- Breaker: **BREAK 0 / WEAKENS 3 / SURVIVES 9 / AMBIGUITIES 3.**
- Combined verdict: **PASS against the brief as written**, with the
  three WEAKENS dispositioned below and three ambiguities pinned.
  Nothing in the code misimplements the brief. Two suite blindnesses
  were real and are now closed or proven harmless; one silent
  behavior is pinned as a tripwire for a v1 decision.

## The sanctioned simplification, quantified (SURVIVES, with numbers)

The brief orders the |coefficient|^2 mixture rule for branch-random
measurements by name. Against exact statevector references (40,000
shots per case, breaker's `probe_measure_exact.py`, re-run by the
main agent):

- |T>, then H, then measure Z: simulator P(1) = 0.5064, exact
  P(1) = 0.146447. The rule is badly wrong here, by +0.36.
- |T>, measure Z directly: 0.5002 vs 0.5 exact.
- |T> on q0, CX to q1, joint outcomes: 0.5024 per outcome vs 0.5
  exact, zero mismatched pairs in 40,000 shots.

Disposition: not a contract break (the brief sanctions the rule and
requires it be documented, which the module docstring does). The
practical weight is narrow: the rule is exact whenever the measured
observable is deterministic per branch, which covers the syndrome
and detector measurements that produce S22, S23, and S24 in a memory
experiment. It corrupts only measurements that are random within a
branch and carry interfering phases, such as a rotated-basis readout
of a magic state. Section V's observables do not include that class.
Any future tomography-style arm does, and must not use v0 for it.

## WEAKENS dispositions

**W1. m_max truncation is silent.** 11 injections produce 2,048
branches; the cap keeps 1,000, drops 51.2% of the expansion, and
renormalizes with no warning, flag, or return value. A caller past
the rank budget gets a wrong answer that looks right. Severity is
low for Section V (cultivation states are low-rank, which is why the
cap exists in the paper's own method) and real for any reuse on
higher-rank states.
Disposition: PINNED as a tripwire test in the shipped suite
(`test_m_max_truncation_tripwire`), stating the behavior may change
once adjudicated. Recommendation for v1: expose cumulative dropped
mass on the simulator. The user's call when v1 is scoped.

**W2. The shipped suite was blind to the leaked-partner CZ rule.**
Mutation M1 (apply the ideal entangler even when a partner is
leaked, drop the twirled Z) passed the original suite 15/15. The
code is correct; the blindness sat on the load-bearing mechanism
for the S24 covariance signature.
Disposition: CLOSED. New test
`test_leaked_cz_skips_entangler_and_applies_partner_z` compares the
post-CZ tableau against a Stim reference (H, H, Z on the partner,
no CZ). Verified both ways: 18/18 on the real code, and the new
test fails on a rebuilt M1 mutant while the other 17 pass.

**W3. The shipped suite was blind to coefficient reweighting.**
Mutation M2 (skip the sqrt(likelihood) factor in measurement)
passed 15/15. The breaker reported blindness; the main agent's
adjudication found the deeper fact: the mutation is unobservable
in v0 by construction. Branches in this engine stay Pauli-related
(injections relate branches by X, Cliffords conjugate that
relation, depolarize and the leakage Z channel multiply it by
another Pauli), and a Pauli preserves the magnitude of every Pauli
expectation, so surviving branches always share one likelihood and
the factor cancels in renormalization. Empirical check: 1,593
measurements across 300 random circuits with injections,
depolarize, and entangling gates; surviving-branch coefficient
magnitudes were equal in every case (0 violations).
Disposition: DOWNGRADED from suite blindness to a pinned invariant.
A comment at the reweight line records why it is currently
unobservable and that it becomes load-bearing if v1 adds per-branch
non-Clifford operations or branch merging. New test
`test_surviving_branch_coefficients_stay_equal` pins the invariant
itself, so a future change that breaks it fails loudly.

## Ambiguities

- **A1 / G1 (same item from both passes): no mechanism creates
  label 3.** The brief names |3> in the readout map and the decay
  chain and gives no generation rate; the Section V design flagged
  the same hole. Code follows the brief literally. Disposition:
  documented in the module docstring (carried, reachable only by
  direct assignment). Candidate adjudications for v1: (a) accept,
  |3> stays bookkeeping; (b) add a generation rule with a stated
  ratio to |2> creation. The user's call when v1 is scoped.
- **A2: `heat(-1)` error message was misleading** ("exceeds the
  allocated register" for a negative count). Disposition: FIXED,
  message now states the valid range. Suite re-run green.
- **A3: `reset()` is a no-op when enabled=False, even on pre-seeded
  labels.** Consistent with the brief's "exact no-op" wording for
  the disabled arm. No action.
- **G2 (certifier): `base_pauli_p`** is an addition past the brief
  (the main agent's baseline-noise fix). Documented in the function
  docstring and the README; the Section V design requires a nonzero
  SI1000 baseline arm. Recommendation: ratify as part of the runner
  contract for v0. The user's call; it stands documented meanwhile.

## Post-adjudication state

- Shipped suite: 18/18 pass in 9.07 s (15 original + leaked-CZ test
  + invariant test + truncation tripwire).
- Code changes from this check: one error-message fix, two comments,
  one docstring paragraph. No behavior change to any physics.
- Files: `certifier-trace.md`, `certifier-probes.py`,
  `breaker-findings.md`, 8 breaker probe scripts, this file, all in
  `contract-check/`.
