# External review synthesis: Kimi K3 and Opus 5.5

Date: 2026-10-16. Method: identical prompt to both models via
OpenRouter. Each received the note itself (status header stripped,
so neither knew about the internal adversarial review), a verified
fact sheet from the primary sources, and a referee brief. Neither
saw the other's review. Both main calls hit the 6,000-token output
cap before finishing, so each verdict and revisions list was
completed in a short follow-up call.

Files: kimi-k3-evaluation.md, kimi-k3-verdict.md,
opus-55-evaluation.md, opus-55-verdict.md.
Costs: Kimi main $0.1455, Kimi verdict $0.0603, Opus main $0.1490,
Opus verdict $0.0311. Round total $0.3858.

## Both verdicts

PUBLISH WITH REVISIONS. Both models, independently.

## Where they agree (highest weight)

1. CHANNEL RE-PARTITION, the finding of the round. The 2024
   inventory's six channels are gate, readout, leakage, crosstalk,
   correlated, classical chaos. The draft's Section III scores
   leakage, low-frequency phase noise, crosstalk, correlated,
   gate-and-readout merged, chaos-and-nonlinear merged. Phase
   noise was never one of the six. So the abstract's "two channels
   take direct hits" counts a channel the 2024 note did not list.
   Both demand: file phase noise under the correlated row or under
   Kalai's noise-sensitivity objection, or state openly in the
   abstract that the channels were re-partitioned, and recount.
   Kimi adds that by the note's own anti-double-counting rule
   (channel 4), this is one hit plus a corroboration, not two
   hits. VERIFIED against the draft: the charge is correct.
2. The Layman TL;DR closing line, "I listed that leak, by name,
   in 2024," claims a priority the author does not have: Google's
   own 2024 budget carried leakage at about 10 percent and DQLR
   predates the note. Both demand the narrower, defensible claim:
   the simplified models omitted it, and the 2026 simulations
   omitted it again. Both also note the TL;DRs drop the
   variability alternative and the no-ablation fact (the internal
   breaker pass had already forced the variability alternative
   into the Conclusion; it is still missing from both TL;DRs).
3. Section V needs a 2 by 2 design: leakage removal on or off,
   crossed with readout recalibrated or not. Both models, same
   reasoning: the note's own entry path for leakage runs through
   unoptimized readout, so a single-intervention rerun cannot
   credit gap closure to leakage alone. Opus adds a fourth
   outcome (gap widens from removal-unit overhead), a
   pre-registered threshold with error bars, cheaper tests
   (three-state readout, leakage-injected re-simulation), and a
   line saying who could run it.
4. Conflict disclosure: one line stating the author scores his
   own prior note. Both ask. Neither the internal certifier nor
   the breaker raised this.
5. Missing reference: Akshay et al. appears in the challenge
   table and nowhere in the references. Both caught it. VERIFIED:
   correct, grep finds Akshay only in the table.
6. Prior leakage literature is uncited (Suchara, Cross, Gambetta;
   McEwen et al. 2021; Miao et al. 2023; Varbanov et al.), and its
   absence props up the priority framing in item 2. Both ask.

## Where they split

- Kimi's second demand: a falsifiability paragraph. Hits count
  for the inventory, misses count as "not tested," never against
  it, so "nothing in the 2024 note needs correction" is a ratchet
  unless the note states what observation would have damaged a
  channel. Also: soften "It tests it anyway," rewrite the abstract
  in the Non-Hype TL;DR's register, add a scale caveat (one
  supplement figure, one grafting configuration).
- Opus's second demand: score the disconfirming evidence. The
  echoed performance being limited by gate error and decoherence
  means the headline result is consistent with the simplified
  model; a symmetric scorecard records that against the thesis.
  Also: "independent" in Section IV should be "second" (same
  team, same processor family); the channel 1 header's "tested"
  overstates a result with no controlled run; clarify whether
  DQLR and leakage removal units are the same mechanism; drop or
  use two unused references; define the challenge table's grading
  direction.
- Opus arithmetic check: the projected 2e-5 against the 1e-10
  requirement is about 5.3 orders of magnitude, not the draft's
  "four to five." VERIFIED: Opus is right; the sentence's subject
  is the projection. Minor fix.

## Findings that do not stand (checked against the full text)

Both models worked from a fact sheet, not the papers, and both
flagged specifics as unsourced that are in fact in the cultivation
paper: the 1e-6 to 1e-8 need range (paper, page 1), the near-1e-5
detuning bound (supplement Sec. X.B), the |2> frequency-collision
path (supplement Sec. XIV), the candidate noise source list
(Sec. X.A), the 2e-5 projection, the 1 to 2 e-4 cultivated error,
and the 1e-10 RSA figure. Those citation demands collapse,
although adding pinpoint citations would still help the note.
Kimi's charge that "propagate across the qubit grid" is an
embellishment also fails: it is the supplement's own phrase
("leakage, which is time-correlated and can propagate across the
qubit grid").

## Net adjudication

The round's real yield is items 1 to 6 in the agreement list,
none of which the internal passes caught, because all of them are
framing and accounting questions rather than claim-accuracy
questions. The note's numbers and hedges survived three
independent passes. Its scorecard accounting, its TL;DR
self-credit line, and its Section V design did not survive two.
No revision has been applied yet; that is the author's call.
