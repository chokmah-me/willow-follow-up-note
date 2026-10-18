# Contract-breaker findings: leakage_hybrid.py v0

Adversarial pass against the contract in `../ASTRA-BRIEF.md`.
The code and the shipped tests were NOT modified. All probes live in
this folder and run with `../.venv/bin/python` from the project root
with `PYTHONPATH=.`.

**Tally: BREAK 0 / WEAKENS 3 / SURVIVES 9 / AMBIGUITIES 3**

The headline: no contract break. Every brief-specified number and rule
I checked is implemented as specified (pt = 8e-4, heating 1/(700 us),
896 ns cycle, 4.4-cycle seepage, 50/50 leaked readout, ideal reset,
epsilon = 1e-4, m_max = 1000, the |T> branch decomposition with the
correct phase). The three WEAKENS are all of one family: behaviors the
code gets right but the shipped tests cannot see, plus one silent
truncation. The three ambiguities are places the brief itself is
silent, pinned for adjudication rather than graded.

---

## WEAKENS 1 — m_max truncation is silent (brief: branch cap)

**Probe:** `probe_branches.py`, `cd ~/workspace/willow-leakage-sim && PYTHONPATH=. .venv/bin/python contract-check/probe_branches.py`

**Numbers:** 11 magic injections produce 2^11 = 2048 branches, each with
|coefficient| = 0.0221, all above the epsilon cutoff of 1e-4. `_prune`
keeps 1000 and drops 1048 branches — 51.2% of the expansion — with no
warning, no flag, and no return value. The surviving mixture is
renormalized to 1.0, so the state is silently a different state.

**Plain terms:** the brief sanctions the 1000-branch cap, and low-rank
cultivation states will never hit it, so this will not bite the
intended use. But a caller who pushes the engine past its rank budget
gets a wrong answer that looks exactly like a right one. A one-line
warning or a truncation counter would close this.

**Severity:** low for the Section V use; real for anyone reusing the
engine on higher-rank states.

## WEAKENS 2 — shipped tests are blind to the leaked-partner CZ rule (brief: CZ with leaked partner)

**Probe:** `mutation_hunt.py` (M1), same run command as above.

**What was done:** a copy of the module was mutated so
`HybridSimulator.cz` always applies the ideal tableau CZ, even when a
qubit is leaked — dropping both the twirled Z channel on the partner
and the skip of the ideal entangler. The full shipped suite still
passes: 15/15.

**Plain terms:** the code implements the brief's rule correctly (the
engine-level transport tests cover the label movement), but nothing in
the suite exercises a CZ through the simulator with a leaked partner.
If a future edit breaks that rule, the suite will not notice. This is
the load-bearing leakage mechanism for the S24 covariance signature,
so the blindness is in the worst place.

**Severity:** medium as a test-coverage gap; zero as a code defect (the
code is correct today).

## WEAKENS 3 — shipped tests are blind to coefficient reweighting (brief: collapse/reweight)

**Probe:** `mutation_hunt.py` (M2).

**What was done:** a copy of the module was mutated to skip the
`sqrt(likelihood)` coefficient reweight in `_project_mixture`. The full
shipped suite still passes: 15/15. (The control mutation M3 — leaked
readout always returning 0 — IS caught, 2 failed, so the suite is not
toothless everywhere.)

**Plain terms:** the code reweights correctly, but no test checks a
coefficient value after a measurement, only branch counts and tableau
states. A regression in the Bayesian update would ship silently.

**Severity:** low-medium as a test-coverage gap; zero as a code defect.

---

## SURVIVES 1 — measurement exactness, quantified (brief: measurement rule)

**Probe:** `probe_measure_exact.py`. True probabilities computed here
from numpy statevectors, never copied.

| case | exact P | sim P (N=40000) | delta |
|---|---|---|---|
| (a) |T>, H, measure Z: P(1) | 0.146447 (= (2-sqrt2)/4) | 0.506400 | **+0.359953** |
| (b) |T>, measure Z: P(1) | 0.500000 | 0.500200 | +0.000200 |
| (c) |T> on q0, CX(0->1): P(q0=1), P(q1=1), P(11) | 0.5, 0.5, 0.5 | 0.5024, 0.5024, 0.5024 | ~+0.002 |
| (c2) q0 != q1 fraction (exact 0) | 0.000000 | 0.000000 | 0 |

Case (a) is the brief's sanctioned simplification, named in the
docstring: the |coefficient|^2 mixture rule. It is NOT a contract
break, and the deviation is now quantified: up to ~0.36 absolute on a
maximally adversarial case (a branch-random measurement where both
branches are 50/50 and carry the magic phase).

**Practical weight, graded:** in a QEC memory experiment the mixture
rule is EXACT for the observables that matter. Syndrome and detector
measurements on stabilizer branches are deterministic per branch (0 in
the noiseless case), and the mixture rule collapses to the true value
whenever every branch's outcome is deterministic — proven by cases (b)
and (c), where entanglement is handled correctly through sequential
collapse. The deviation corrupts only measurements that are random
within a branch AND carry interfering phases across branches — e.g.
X-basis readout of magic states, i.e. non-stabilizer tomography. For
the Section V use (syndrome extraction on Clifford-evolved cultivated
states: S22 LER, S23 rise, S24 covariance), the affected measurement
class does not occur. If the engine is ever reused for magic-state
tomography, this limitation becomes load-bearing.

## SURVIVES 2 — branch normalization is exact (brief: coefficient handling)

**Probe:** `probe_branches.py` section 2b. After 100 sequential Z
measurements on a 3-qubit triple-magic state, max |sum|c|^2 - 1| =
0.00e+00. Both `_project_mixture` and `_prune` renormalize correctly.

## SURVIVES 3 — hostile inputs all fail loud (brief: API)

**Probe:** `probe_hostile.py`. 30 hostile inputs: out-of-range and NaN
probabilities, zero/negative lifetime, non-integer m_max, bad qubit
indices, CZ with `higher_freq` outside the pair, `heat()` over the
register, wrong rng type, bad depolarize probabilities, double magic
injection, injection into a leaked qubit. Every one raises a clear
`ValueError`/`TypeError`/`IndexError`. Zero silent accepts.

## SURVIVES 4 — enabled=False is an exact no-op (brief: baseline arm)

**Probe:** `probe_switches.py` section 4a. Every engine method
(`heat`, `cz`, `measure`, `reset`, `seep_cycle`) with `enabled=False`
leaves labels untouched AND consumes zero RNG draws — verified by
bit-generator state comparison, including with labels pre-seeded to
[2, 3, 0] (left untouched, consistent with "exact no-op").
`HybridSimulator.measure` and `reset_after_measure` draw RNG only for
legitimate measurement sampling; `depolarize` draws as the brief's
SI1000 baseline hook, which is the intended no-leakage-arm behavior,
not a leakage draw.

## SURVIVES 5 — every mechanism switch fully disables its mechanism (brief: switches)

**Probe:** `probe_switches.py` section 4b. With the corresponding
probability forced to 1.0 and 200-500 trials: `heating_on=False` ->
zero labels created; `cz_leak_on=False` -> zero labels created;
`transport_on=False` -> label never moves; `readout_leak_on=False` ->
zero labels created; all creation switches off together -> labels stay
0. `removal_on=False` ignores `removal_boost=100` (seeped fraction
0.2122 vs unboosted analytic 0.2033); `removal_on=True` boosts to the
1.0 clip as designed.

## SURVIVES 6 — post-selection edge returns NaN, documented (brief: runner)

**Probe:** `probe_postselect.py`. A seed hunt forced zero kept shots
(`postselect_first_cycle=True`); the function returns
`detection_fraction_per_cycle: [nan, nan, nan]`,
`mean_label_population: [nan, nan, nan]`, `keep_rate: 0.0` — no crash,
no hang. The NaN behavior IS documented in the `run_repetition_memory`
docstring ("If no shots survive, both lists contain NaN"); it is not
in the README, but the docstring is where a user reads the API.
`shots=0` raises `ValueError` loudly.

## SURVIVES 7 — determinism across separate processes (brief: seeded RNG)

**Probe:** `probe_determinism.py`. The same seeded runner call plus a
simulator-level sequence (magic injection, CX, two measurements) in two
independent subprocesses: byte-identical outputs.

## SURVIVES 8 — the |T> branch decomposition is the brief's decomposition

**Probe:** `probe_branches.py` / shipped test 6 (independently
re-verified in probe 1 setup). After `inject_magic_state`: exactly 2
branches, |coefficients| = 1/sqrt(2), relative phase e^{i pi/4},
tableaus |0> and |1>. Matches the brief's specified decomposition
exactly.

## SURVIVES 9 — M3 control: the suite catches a wrong readout map

**Probe:** `mutation_hunt.py` (M3). Mutating leaked readout to always
return 0 fails 2 shipped tests. The suite is not blind everywhere.

---

## AMBIGUITIES (for adjudication — the brief is silent, not broken)

**A1. No mechanism creates label 3.** `probe_label3.py`: the only
literal label assignments in the module are 0 and 2; 300 cycles with
every creation probability maxed never produce a 3. The brief mentions
|3> exactly twice (the 50/50 readout map and the 3 -> 2 -> 0 decay
chain) and specifies no |3> generation mechanism or rate. The code
handles |3> correctly wherever it appears (measurement map, seepage
cascade, transport preserves it), so carrying the label is harmless —
but if the intent was for |3> to be reachable in a run, the creation
path is unspecified in both brief and code. Recommend: either specify
a |3> creation rule or document that |3> is a carried-but-unreachable
label in v0.

**A2. `heat(-1)` error message is misleading.** It raises `ValueError`
("n_qubits exceeds the allocated register") — loud and safe, but the
message describes the wrong violation for a negative count. Cosmetic.

**A3. `reset()` with `enabled=False` is a no-op even on pre-seeded
labels.** Consistent with the brief's "exact no-op" requirement; noted
only because a caller injecting labels for a study and then toggling
the master switch might expect `reset` to still clear them. The brief's
wording supports the code. No action needed unless the intended
semantics differ.

---

## Probe index

All in `~/workspace/willow-leakage-sim/contract-check/`, run from
`~/workspace/willow-leakage-sim` with `PYTHONPATH=. ../.venv/bin/python`:

- `probe_measure_exact.py` — SURVIVES 1 (statevector comparison)
- `probe_branches.py` — WEAKENS 1, SURVIVES 2, SURVIVES 8
- `probe_hostile.py` — SURVIVES 3
- `probe_switches.py` — SURVIVES 4, SURVIVES 5
- `probe_postselect.py` — SURVIVES 6
- `probe_determinism.py` — SURVIVES 7
- `probe_label3.py` — A1
- `mutation_hunt.py` — WEAKENS 2, WEAKENS 3, SURVIVES 9
