# Contract-breaker findings: follow-up note draft (willow-paper-holds/follow-up-note-draft.md)

Contract-breaker pass, 2026-10-16. Not a fix pass. Report only.

Trusted sources: /tmp/cultivation/paper.txt (arXiv:2512.13908v1 full text
+ supplement; same work as Science DOI 10.1126/science.aee7961),
the held note's "Primary-source check" and "Follow-up assessment"
grades. The 2024 paper's claims are taken from the held note's summary
and the draft's own Section I, both consistent with the ResearchGate
full-text read done earlier the same day.

Method: every number, attribution, and grade in the draft was checked
against paper.txt by direct grep; line numbers below are paper.txt lines.

## Findings

### F1 — WEAKENS (borderline BREAK; see note) — Layman TL;DR

Draft: "Their best explanation is a known leak in the hardware that
the simulation did not model and the circuit did not guard against."

Source (paper.txt:1948): "It is likely that the main source of
disagreement is population leakage."

The draft drops the "likely" hedge in the layman register and
re-ranks the attribution as "best explanation" presented as settled
team position. "Likely main source" and "best explanation" are close
in rank, which is why this is WEAKENS rather than BREAK; a referee
can still quote it as a hedge-drop in a summary.

Hostile quote: "The paper says 'likely'; your summary announces
their 'best explanation' as if the hedge were never there."

Demanded fix: restore the hedge in the layman register, e.g.
"The authors' likely explanation is a leak the simulation did not
model and the circuit did not guard against."

### F2 — BREAK — Conclusion (final paragraph, most quotable sentence)

Draft: "A protocol that prepares states forty times cleaner than
injection then stores them seven times worse than its own
simulation, for reasons its authors locate in an omitted channel
and an omitted removal step, is the 2024 fine print appearing in
a new place."

Source (paper.txt:1948, 439-440): leakage is "likely" the main
source; the main text keeps a second cause open, "the variability
in physical qubit performance."

This is confidence inflation in effect, in the note's peroration:
the causal link is asserted as located fact with the "likely"
dropped and the open alternative unmentioned. It directly violates
the pre-registered grade ("likely, no ablation, no upgrade") in the
single sentence most likely to be quoted.

Hostile quote: "Your source calls leakage the 'likely' main source
and keeps qubit variability open; your conclusion asserts the
cause as fact."

Demanded fix: "for what the authors call the likely cause, an
omitted channel and an omitted removal step, with the alternative
still open".

### F3 — WEAKENS — Section III.2, phase-noise mitigation paragraph

Draft: "so they conclude the final performance is limited by gate
error and decoherence rather than quasi-static detunings."

Source (paper.txt:1560-1561): "This suggests that our magic state
performance when using echoing is limited by gate error and
decoherence, not quasi-static detunings."

The draft upgrades the authors' "suggests" to "conclude".

Hostile quote: "The authors merely suggest; the draft reports a
conclusion."

Demanded fix: "their simulations suggest the performance with
echoing is limited by gate error and decoherence, not
quasi-static detunings."

### F4 — WEAKENS — Section III.2, same paragraph

Draft: "Without echo pulses to filter this noise, the team's own
comparison says their performance was dominated by it."

Source (paper.txt:1555): "suggest that without echos, our
performance is dominated by low-frequency phase noise."

Same hedge-drop family as F3: "suggest" presented as "says".

Hostile quote: "The paper only suggests dominance without echos;
the draft states it as the team's finding."

Demanded fix: "their comparison suggests performance without
echos was dominated by low-frequency phase noise."

### F5 — WEAKENS — Section III.2, editorial paragraph

Draft: "It invalidated the standard measurement protocol, in a way
the authors had to diagnose over months."

Source: paper.txt contains no occurrence of "month" (verified by
grep). The timeline evidence comes from the Google blog account
(months of diagnosis before kickback tomography), which the draft
cites in its references but does not name at the claim. The
sentence presents the duration as part of the paper work.

Hostile quote: "The paper says nothing about months; you imported
the timeline from the company's blog and attributed it to the
authors."

Demanded fix: attribute explicitly, e.g. "the team's blog account
describes months of diagnosis before the new method", or drop the
duration.

### F6 — SURVIVES (flagged, author's risk call) — Section III.2

Draft: "That is the strongest form the objection has yet taken in
a Google paper, and it comes from inside the team."

No source asserts this; it is the author's editorial superlative,
not a factual claim, so it cannot be falsified and is not a
contract violation. A referee cannot disprove it but can quote it
as rhetoric. SURVIVES; the author should decide whether the
superlative earns its space.

## Items checked and passed (SURVIVES)

- Fidelity wording across versions: the draft is honest. SME TL;DR
  uses Science's "at least 0.9999(1)"; Section II says "0.9999(1),
  at least that in the Science abstract's wording" (paper.txt:8-12
  has the arXiv wording; Science abstract checked separately).
- 40-fold reduction, 8% retention (paper.txt:8-12).
- Injection-only 4.4(2)e-3, "similar to our physical qubit gate
  errors" (paper.txt:299).
- Cultivated circuit 1-2e-4 (paper.txt:359); removing QEC cycles
  makes error ~100x worse (same line).
- Kickback tomography: O(1e4) vs O(1e8) measurements (paper.txt:282).
- Seven-fold gap placed correctly in the supplement, Sec. XIV /
  Fig. S22, not the headline (paper.txt:1946-1948).
- SI1000 depolarizing model at p = 2.3e-3 for the memory experiment
  (paper.txt:1946).
- Up to N=9 cycles (Fig. S23, paper.txt:2042); 54-qubit grafting
  experiment (paper.txt:1575, 422).
- Simulations do not include leakage (paper.txt:439, 1950, 2044,
  1986); circuits lacked leakage removal units (paper.txt:1987);
  |2> frequency-collision path named (paper.txt:1991); expected
  improvements list (paper.txt:1994).
- Main-text alternative kept open: qubit performance variability
  (paper.txt:440) — the draft discloses it (SURVIVES, and it is
  what makes F2 a violation rather than a paraphrase).
- Non-physical norm under logical state tomography, attributed to
  low-frequency phase noise (paper.txt:1441-1443).
- Detuning source list: slow drift, residual fields, Stark shifts
  via microwave crosstalk (paper.txt:1444-1446); idling-entangled
  exposure mechanism (paper.txt:1446-1448). "Candidate sources"
  hedge preserved in the draft.
- 1e-5 infidelity bound with echoing (paper.txt:1559-1560).
- Crosstalk appears in one place only (paper.txt:1446; no other
  mention found) — draft's "touched, not measured" is accurate.
- p^3 scaling and 2e-5 projection at halved noise (paper.txt:482,
  484, 1863); RSA-2048 needs ~1e-10 (paper.txt:84) — draft's gap
  arithmetic holds.
- Correlated-errors score: leakage-mediated, not double-counted —
  consistent with pre-registered grade (paper.txt:1984, 2095-2098).
- 2024-paper numbers as summarized (0.143% +/- 0.003%, 2.4x,
  Lambda 2.14 +/- 0.02, 63 us decoder, 80/10/10 budget, 14%
  discrepancy, 1e-10/hr burst floor, distance-27 / Lambda~10 /
  1e-6 targets): consistent with the held note's summary and the
  ResearchGate full-text read; no conflict found.
- DOIs and dates: Science 10.1126/science.aee7961 (Crossref,
  First Release 2026-10-15); arXiv:2512.13908v1 (Dec 15, 2025);
  Gidney-Shutty-Jones 2024 protocol (arXiv:2409.17595); blog post
  Oct 15, 2026.
- Version trap: the draft never amends the 2024 paper and never
  changes a Zenodo v2.0 number — consistent with the assessed
  "standalone note, no revision, no bump".

## Tally

- BREAK: 1 (F2 — conclusion asserts the leakage causal link as
  located fact, dropping "likely" and the open alternative, in the
  most quotable sentence).
- WEAKENS: 4 (F1 — layman TL;DR "best explanation" hedge-drop,
  borderline BREAK; F3 — "suggests" upgraded to "conclude"; F4 —
  "suggest" presented as "says"; F5 — "over months" unattributed
  to the blog).
- SURVIVES: everything else checked, including F6 (flagged
  editorial superlative, author's call).

Net: no wrong numbers, no scope swaps, no fabricated attributions,
no version traps. The draft's failure mode is concentrated and
specific: hedge-dropping on the phase-noise paragraph and, once,
on the leakage attribution where the contract forbids it. Fix F1-F5
and the note meets the pre-registered grades.
