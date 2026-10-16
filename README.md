# Willow, Tested Again: working repo

Private working repo for the follow-up note to "Notes on Google
Willow (2024)." Status: DRAFT, revised after internal adversarial
review and two external reviews (2026-10-16). Not published, no
DOI reserved. Publication is the author's decision alone.

## The draft

`draft/follow-up-note-draft.md` is the single working copy. Edit
it here. It carries its own status header, the disclosure line,
and an AI Use Statement section (also kept standalone in
`AI-USE-STATEMENT.md` for reuse, for example in a deposit
description).

House style for this draft, enforced in every pass so far: no em
dashes; simple words; the leakage attribution keeps the authors'
word "likely" everywhere, including summaries and the conclusion.
Any edit to a summary, TL;DR, or conclusion sentence reopens the
hedge question: recheck that "likely," the variability
alternative, and the no-ablation fact all survive the edit.

## Contents

- `draft/` the note itself.
- `AI-USE-STATEMENT.md` standalone copy of the statement.
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

## Open items (author's calls, not yet applied)

From the external reviews' split findings, recorded in
external-review/REVISIONS-APPLIED.md: an inventory-level
falsifiability paragraph; an abstract rewrite in the Non-Hype
register; a scale caveat; an explicit disconfirming-evidence
scorecard entry; softening the channel 1 header; two unused
references to cut or use; the challenge table's grading
direction to define.

## Working on the desktop

Clone, edit `draft/follow-up-note-draft.md`, commit, push. The
review folders are the audit trail; add new passes as new files
rather than editing the old ones.
