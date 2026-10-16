# Willow, Tested Again: working repo

Private working repo for the follow-up note to "Notes on Google
Willow (2024)." Status: DRAFT v3, evidence-ready residual from v2
still named. Not minted, not published, no DOI reserved.
Publication is the author's decision alone. Evidence-ready means
the integrity residual is named and deferred. It does not mean
scientifically verified. v3 has not been re-scanned.

## The draft

`draft/follow-up-note-draft-v3.md` is the current working copy.
`draft/follow-up-note-draft-v2.md` and
`draft/follow-up-note-draft.md` stay as the audit trail. Edit v3.
Process notes that used to sit above the title are in
`draft/process-log.md` and are not part of the note.
`AI-USE-STATEMENT.md` is a copy of the v3 AI Utilization
Statement.

House style for this draft, enforced in every pass so far: no em
dashes; simple words; the leakage attribution keeps the authors'
word "likely" everywhere, including summaries and the conclusion.
Any edit to a summary, TL;DR, or conclusion sentence reopens the
hedge question: recheck that "likely," the variability
alternative, and the no-ablation fact all survive the edit.

## Contents

- `draft/` the note itself, plus `process-log.md` and
  `search-meta-v3.html`.
- `AI-USE-STATEMENT.md` standalone copy of the v3 statement.
- `held-note/cultivation-leakage-note.md` the earlier held
  postscript note for the Zenodo paper, with the primary-source
  check and the follow-up assessment that led to this draft. It
  stays held; the follow-up note superseded it as the vehicle.
- `adversarial/` internal passes: certifier-trace.md (31 claims
  traced to source), breaker-findings.md (BREAK 1, WEAKENS 4),
  ADJUDICATION.md (all findings accepted and fixed).
- `external-review/` Kimi K3 and Opus 5.5 evaluations and
  verdicts (both PUBLISH WITH REVISIONS), SYNTHESIS.md,
  REVISIONS-APPLIED.md, review-prompt.md (the prompt both models
  received), raw/ (the four raw API responses).
- `sources/` SOURCES.md (pins, DOIs, hashes) plus the arXiv full
  text of the cultivation paper, PDF and extracted text.

## Checks on v2

`integrity-manifest.json` sets `i1_policy` to `advise`. The rates
in the note are cited priors (Rosenfeld et al. 2026, Google 2024,
the 2024 note). There is no local results artifact, and none
should be invented.

`results/integrity_audit.json` is the 2026-10-16 online scan of
v2. I1 is limited (eight unbound percents). I2 and I4 are not
applicable. I5 is clear. I3 fails on one identifier:
`10.13140/RG.2.2.30911.01443` is not in Crossref. Eight other
DOIs resolved. The scan file is unchanged. The deferral is
`results/i3-researchgate-deferral.md`: keep the DOI, send readers
to the ResearchGate page already in reference [1], and do not
treat the Crossref miss as a repaired citation. The scan does not
mark the note scientifically verified.

A robustness check of v2 is in `results/robustness-check-v2.md`
(own-draft, 2026-10-16, 18 frozen rows). It is a survival map,
not a verification stamp. The conditional leakage score, the
other-channels-untested score, and the five-to-six-orders
arithmetic survive the frozen perturbations. The score flips if
"likely" is dropped, or if a removal run leaves the gap
unchanged. That run is the one in Section V. This repo cannot
perform it. One recorded weakening: the 40x headline is 22 to 44
over the draft's own stated range. v3 has not been re-checked.

## Open items

The split findings listed in `external-review/REVISIONS-APPLIED.md`
were applied in v2: inventory-level falsifiability paragraph,
shorter abstract, scale caveat, disconfirming scorecard row,
channel 1 header softened, Kalai 2023 cited, Stethoscopes
reference removed, challenge-table grading direction stated.

Still open, on purpose:

- The removal experiment in Section V. Only the cultivation team
  can run it. That is a scientific residual, not an integrity-scan
  residual.
- A Zenodo DOI. None is reserved. SEARCH-META placeholders stay
  until mint.
- Re-scan of v3 with `manuscript-integrity-gate`.

## Working on the desktop

Clone, edit `draft/follow-up-note-draft-v3.md`, commit, push. The
review folders are the audit trail; add new passes as new files
rather than editing the old ones. Do not overwrite
`follow-up-note-draft.md` or `follow-up-note-draft-v2.md`.
