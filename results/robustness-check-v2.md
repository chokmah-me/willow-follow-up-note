# Robustness check: Willow, Tested Again (v2)

Mode: own-draft. Date: 2026-10-16.
Coverage: v2 draft (draft/follow-up-note-draft-v2.md at repo head,
commits 18d34bf and 89e4bad) read in full through the repo web view
on 2026-10-16 and checked against the full v1 text held locally
(SHA-256 c601db0ccf281128fb18244b1064db52516640ce8183dda142df901
for draft/follow-up-note-draft.md). The claims perturbed are the
v2 claims; where v2 text is identical to v1 the local v1 text is
the working copy. No code or data artifact exists for this note
(it is a commentary note scoring published work), so no
perturbation is a re-run of an experiment. Arithmetic rows are
recomputed. This check is a survival map, not a verification:
it does not mark the note scientifically verified.

## Frozen perturbation surface

Frozen 2026-10-16 14:10 EDT, before any perturbation result was
observed. 18 rows: 1-18 as listed. No rows were added after the
freeze. Axis-discovery walk: claim-defining, scope, model
structure, assumptions, diagnostics, and provenance/quotation
axes produced rows; input-construction, estimator/solver, seed
and Monte Carlo, and regression/simulation design axes are
not applicable to a commentary note with no local results
artifact (recorded here so the walk is not silent).

Claim objects:
- C1, leakage score. Outcome: the grafted-code memory experiment
  runs about 7 times worse than its SI1000 simulation
  (p = 2.3e-3), and leakage is the likely main cause. Claim type:
  associational attribution, conditional. Scope: one supplement
  memory experiment, one grafted configuration, up to nine
  cycles. Focal parameter: the roughly 7x ratio, with the word
  "likely" as part of the claim, not decoration on it.
- C2, channel accounting. Outcome: of the six 2024 channels,
  leakage takes one direct hit, phase noise corroborates the
  correlated row, crosstalk is touched only, correlated errors
  are leakage-mediated, gate and readout are baseline, and
  classical chaos and nonlinear errors are not tested. Claim
  type: accounting / existence. Focal statement: one direct
  hit, most channels untested by this experiment.
- C3, distance arithmetic. Outcome: the projected 2e-5 at half
  the current noise is about five orders of magnitude short of
  the 1e-10 RSA-2048 need, and the measured 1 to 2e-4 is about
  six orders short; the cultivation improvement itself is
  about 40x from an injection-only 4.4(2)e-3. Claim type:
  bound / arithmetic. Focal parameters: 5.3 and 6.0 to 6.3
  orders; the 40x ratio.

| # | Axis | Namespace | Tier | Baseline | Perturbed | Estimand relation | Load-bearing for |
|---|---|---|---|---|---|---|---|
| 1 | A1 parameter | rc/ | T4 | gap ratio 7x | 3.5x, 14x (x2, /2) | preserving | C1 |
| 2 | A4 diagnostic | diag/ | T1 | gap ratio 7x | ratio 1.0 in a removal rerun | preserving | C1 |
| 3 | A2 assumption | sens/ | T4 | attribution is "likely" | "likely" dropped, upgraded to demonstrated | preserving | C1, C2 |
| 4 | A2 assumption | sens/ | T2 | variability kept open as second cause | variability becomes the main cause | preserving | C1 |
| 5 | A2 assumption | sens/ | T4 | simulations omit leakage | simulations include leakage | preserving | C1 |
| 6 | A3 re-derivation | rc/ | T0 | 2e-5 vs 1e-10 = 5.3 orders | recompute | preserving | C3 |
| 7 | A3 re-derivation | rc/ | T0 | 1 to 2e-4 vs 1e-10 = 6 orders | recompute over the range | preserving | C3 |
| 8 | A1 parameter | rc/ | T2 | improvement "about 40x" | range ends: 4.4e-3 / 2e-4 and / 1e-4 | preserving | C3 |
| 9 | A2 assumption | sens/ | T2 | DQLR and leakage removal units are the same line of mechanism | they are distinct mechanisms | preserving | C1 (Sec III.1 only) |
| 10 | A4 diagnostic | diag/ | T4 | correlated row not double-counted | correlated scored as an independent second hit | preserving | C2 |
| 11 | A4 diagnostic | diag/ | T1 | phase noise filed under the correlated row | phase noise counted as a seventh channel | preserving | C2 |
| 12 | A5 alt frame | explore/ | T4 | inventory frame | cultivation read as a methods paper only | changing | C2 scope |
| 13 | A5 alt model | rc/ | T1 | leakage-first attribution | readout mis-calibration alone explains the gap | preserving | C1 |
| 14 | A6 quotation | quote/ | T4 | full caveat set | one-line quote: "leakage breaks cultivation, proven" | preserving | C1 |
| 15 | A6 quotation | quote/ | T4 | "nothing contradicted, most untested" | one-line quote: "the 2024 note is vindicated" | preserving | C2 |
| 16 | A3 re-derivation | infer/ | T0 | fidelity "at least 0.9999(1)" | fidelity read as exact 0.9999 | preserving | C3 |
| 17 | A1 parameter | explore/ | T4 | 7x in one configuration | 7x generalized across distances and processors | changing | C1 scope |
| 18 | A2 assumption | sens/ | T2 | echoed detuning bound near 1e-5, below measured error | bound above the measured error | preserving | C2 (disconfirming row) |

## Perturbation log

Run 2026-10-16, after the freeze above, in row order.

1. Survives. At 3.5x or 14x the qualitative score is unchanged:
   a substantial simulation gap with two leakage signatures.
   The exact 7 is not a keystone; any ratio well above 1 scores
   the same. Scale: full.
2. Flips, by the draft's own pre-scoring. A removal rerun that
   leaves the gap at 1.0 (no gap) is Section V outcome 4 in
   reverse: if the gap does not move in any arm, the channel 1
   score must be withdrawn. This is the single run that can
   kill C1, it is named in advance, and only the cultivation
   team can run it. Scale: full.
3. Flips. Without "likely" the attribution exceeds its
   evidence: there is no ablation run, so a demonstrated-cause
   reading is unsupported. The draft's hedge is load-bearing,
   which is why the repo house rule reopens the hedge check on
   any summary or conclusion edit. Scale: full.
4. Weakens. If qubit performance variability is the main
   cause, C1 splits: the signatures stay leakage-shaped, the
   attribution does not. The draft already scores this branch
   in Section V outcome 3 and keeps the alternative in the
   abstract and all three TL;DRs, so the weakening is priced
   in, not hidden. Scale: full.
5. Flips, counterfactual. If the SI1000 simulations had
   included leakage, the omission argument (the 2024 note's
   actual claim) would fall. Checked against the source: the
   supplement states the simulations do not include leakage.
   The assumption is a reported fact, not a modeling choice
   of this note. Scale: full.
6. Survives, recomputed. log10(2e-5 / 1e-10) = log10(2e5) =
   5.30. The draft's "about five orders" for the projection
   is exact. Scale: full.
7. Survives, recomputed. log10(1e-4 / 1e-10) = 6.00 and
   log10(2e-4 / 1e-10) = 6.30. "About six orders from the
   value actually measured" holds over the whole stated
   range. Scale: full.
8. Weakens. Over the draft's own ranges the ratio is
   4.4e-3 / 1e-4 = 44 at the favorable end and
   4.4e-3 / 2e-4 = 22 at the other (21 to 46 using the
   4.4(2)e-3 uncertainty). "About 40x" is the cultivation
   paper's headline framing near the T state, not a value
   that holds over the full 1 to 2e-4 range. The draft
   reports both inputs, so a reader can recompute; the
   headline number is the paper's, flagged as such in
   Section II. Cheapest fix if this is ever tightened: write
   "about 40x near the T state (22 to 44 over the stated
   range)". Not applied here; recorded as the one weakening
   found in C3. Scale: full.
9. Weakens one paragraph, not the score. If DQLR and the
   2023 leakage removal units were distinct mechanisms, the
   clarification sentence in Section III.1 would need a
   rewrite. C1 does not rest on the identity; it rests on
   the omitted channel and the omitted removal step, both
   stated in the supplement. Scale: sign only.
10. Flips the count, and the draft refuses it in text.
    Scoring correlated errors as an independent hit would
    double-count the leakage covariance evidence and return
    the abstract to two direct hits, the error the external
    reviews caught in v1. C2 survives because the draft
    states the anti-double-counting rule where the evidence
    is presented (Section III.4). Scale: full.
11. Survives. Counting phase noise as a seventh channel is
    the v1 accounting error. V2 files it under the 2024
    correlated row in the abstract, in the Section III
    accounting note, and in the Section III.2 header, so
    the count of six is consistent at every level a reader
    meets it. Scale: full.
12. Scope limit, not fragility (explore/). Read as a methods
    paper only, the cultivation result stands on its own and
    the inventory frame adds a scoring, not a correction.
    The draft says the experiment was not designed to test
    the inventory. No flip scored.
13. Weakens, pre-scored. A readout-only explanation is
    Section V outcome 2: the 2 by 2 design exists because
    the leakage entry path runs through the unoptimized
    readout, so a single-fix rerun cannot separate the two.
    Until that rerun, C1 stays "likely," which is the
    correct grade under this alternative, not a refutation
    of it. Scale: full.
14. Flips under misquotation. The one-line version drops
    "likely," the signatures-only evidence, and the open
    alternative, and upgrades a supplement memory result
    into a claim about cultivation itself, which the draft
    explicitly separates (the scored result is not in the
    headline list, Section II). The draft's defenses are
    its Non-Hype TL;DR and the repeated hedge; a quoter
    who drops both is outside what any draft can control.
    Recorded as the highest quotation risk in the note.
    Scale: none (quotation, not recomputation).
15. Weakens under misquotation. "Nothing contradicted, most
    channels untested" is a deliberately weak claim; the
    vindication reading inflates it. The draft resists it
    in three places (abstract last sentence, Non-Hype
    TL;DR, challenge table: no row moves to Solved), so
    the inflation is a reader error the text anticipates.
    Scale: none.
16. Survives. The draft keeps the Science wording "at
    least 0.9999(1)" for the fidelity bound and reports
    the 1 to 2e-4 error range separately; reading the
    bound as an exact value is a misread the text does
    not invite. Scale: full.
17. Scope limit, not fragility (explore/). The 7x does not
    extend across distances or processors, and v2 says so
    (abstract scale caveat; Section II: not a scan across
    distances or processors). A claim of generality would
    flip; the draft does not make it.
18. Survives as scored, and the symmetry is the point. The
    disconfirming row credits the simplified model because
    the echoed detuning bound (near 1e-5) sits below the
    measured error. If the bound were above the measured
    error, that row would move to the inventory's side.
    The row is scored from the reported bound either way,
    which is what makes the scorecard symmetric rather
    than a ratchet. Scale: sign only (the bound is the
    supplement's simulation result, not recomputed here).

## Survival table

| Claim | A1 params | A2 assumptions | A3 re-derivation | A4 diag | A5 alt model | A6 quotation | Overall (T0-T2) | Overall (all rows) |
|---|---|---|---|---|---|---|---|---|
| C1 leakage score | survives (ratio not a keystone) | flips if "likely" dropped (row 3) | n.a. | flips on removal rerun (row 2) | weakens (rows 4, 13) | flips under misquotation (row 14) | weakens | conditional: survives every perturbation the draft controls |
| C2 channel accounting | n.a. | survives | n.a. | survives (rows 10, 11 refused in text) | scope only (row 12) | weakens (row 15) | survives | survives |
| C3 distance arithmetic | weakens (40x is range-dependent, row 8) | n.a. | survives (rows 6, 7, 16 recomputed) | n.a. | n.a. | n.a. | survives | survives with one recorded weakening |

## Keystones

Two, and both are already named in the draft.
1. The word "likely" (row 3). Drop it and C1 exceeds its
   evidence. It is protected by the repo house rule: any
   edit to a summary, TL;DR, or conclusion sentence reopens
   the hedge check.
2. The Section V removal rerun (row 2). It is the only
   perturbation that can kill C1 outright, it is pre-scored
   with a withdrawal clause, and only the cultivation team
   can run it. Until it exists, C1's correct state is
   conditional, and the draft grades it that way.

## Verdict

Author-anchored (T0 to T2 rows): C2 and C3 survive; C1
weakens under the variability and readout alternatives,
both of which the draft keeps open and pre-scores.
Full surface (all 18 rows): the same, plus two conditional
flips that define the claim rather than break it, the
removal rerun (row 2) and the dropped hedge (row 3), and
one recorded weakening, the 40x headline is 22 to 44 over
the draft's own range (row 8). No frozen row produced a
flip the draft does not already name. The leakage score,
the other-channels-untested score, and the five to six
orders arithmetic survive the frozen perturbations in the
conditional form the draft states them.

## What this check could not do

No experiment was re-run: the note reports no local results
and the settling experiment needs the cultivation team's
hardware. Rows depending on supplement simulations (the 7x
extraction, the 1e-5 detuning bound) perturb the draft's
use of those numbers, not the numbers themselves, which
were traced to the supplement in the earlier certifier
pass (adversarial/certifier-trace.md). The v2 text was
read through the repo web view, not a local checkout (git
access from the drafting VM was unavailable), so no
line-level diff of v1 to v2 was recomputed here; the
delta relied on is the browser-verified v2 structure plus
the repo CHANGELOG. Denominator: 18 of 18 frozen rows run,
2 of them as scope limits (rows 12, 17) by design.
