# Adjudication: adversarial review of the follow-up note draft

Date: 2026-10-16. Passes: contract-certifier trace
(certifier-trace.md, main agent, 31 claims) and contract-breaker
pass (breaker-findings.md, independent agent).
Tally at adjudication: BREAK 1, WEAKENS 4, SURVIVES the rest.
Disposition: every finding accepted. No finding rejected, none
quarantined as dissent. All fixes applied to
follow-up-note-draft.md in the same pass and verified by grep
after editing.

## Findings and fixes

- F1, WEAKENS (breaker, borderline BREAK), Layman TL;DR: "Their
  best explanation is a known leak" dropped the "likely" hedge.
  FIXED: now "The authors' likely explanation is a known leak in
  the hardware..."
- F2, BREAK (breaker), Conclusion: "for reasons its authors locate
  in an omitted channel and an omitted removal step" asserted the
  leakage cause as located fact, hedge dropped, open alternative
  (physical qubit performance variability, main text) unmentioned,
  in the note's most quotable sentence. FIXED: now "for what the
  authors call the likely cause, an omitted channel and an omitted
  removal step, with the alternative still open."
- F3, WEAKENS (breaker), Sec. III.2: source "This suggests" was
  upgraded to "so they conclude" on the gate-error and decoherence
  limit. FIXED: now "and suggest the final performance is limited
  by gate error and decoherence, not quasi-static detunings."
- F4, WEAKENS (breaker), Sec. III.2: source "suggest that without
  echos, our performance is dominated" was presented as "the
  team's own comparison says." FIXED: "says" changed to "suggests."
- F5, WEAKENS (breaker), Sec. III.2: "had to diagnose over months"
  has no source in the paper (zero occurrences of "month" in
  paper.txt); the duration comes from the Google blog. FIXED: now
  "The team's blog account describes months of diagnosis before
  the new method was built."
- F6, SURVIVES with flag (breaker): "the strongest form the
  objection has yet taken in a Google paper" is an unfalsifiable
  editorial superlative, the author's risk call, not a contract
  violation. DISPOSITION by the drafter: accepted voluntarily and
  softened anyway. Replaced with a checkable claim: "in this case
  the objection changed the measurement method itself, not only a
  reported number, and the finding comes from inside the team."
- G1, certifier spec gap (not flagged by the breaker, which passed
  the sentence): Sec. III.1 "a new protocol omitted the channel
  from its simulations and omitted the removal step from its
  circuits" read protocol-wide; the source sentence is scoped to
  the grafted memory experiment. FIXED for precision despite the
  pass: now "the grafting work omitted the channel from its
  simulations and omitted the removal step from its circuits."

## What survived, and why it matters

The certifier traced 31 of 31 load-bearing claims to source with no
scope swap and no wrong number. The breaker confirmed the same set
independently, including the two traps (Fig. S24 numbering, where
the source text mislabels once and the caption governs; the
Gidney-Shutty-Jones arXiv ID 2409.17595, where a two-column
extraction artifact suggests a wrong ID) and the Science against
arXiv fidelity wording ("at least" in Science, not in arXiv),
which the draft handles openly. The failure mode of the first draft
was one family only: hedge-dropping in summary and conclusion
sentences, five instances, all on the two claims where the
pre-registered grades forbade it. Numbers, scopes, attributions,
dates, and DOIs all held.

## Standing note for any revision round

Any future edit to a summary, TL;DR, or conclusion sentence in this
note reopens the hedge question. Those sentences are the attack
surface; re-run the breaker grep for "likely" coverage after any
edit to them.
