# Integrity brief — willow-follow-up-note

## Status
willow-follow-up-note — fail (I1 limited unbound 7; I3 fail (7 resolved, 1 unresolved))

## Reproduce
```
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --propose-bindings
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --online
```

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | unbound buckets {'other': 7} |
| I2 protocol | n/a | |
| I3 references | fail | existence via Zenodo/Crossref/OSF APIs for identifiers in this draft — not a four-API ScientistOne audit; not citation support |
| I4 method–artifact | n/a | |
| I5 overclaim | n/a | |

## Residual human gates
none from this scan

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`

## Annotation (2026-10-16, v3 scan)

This scan's "fail" is a status of the scan, not a verdict on the note.
Manuscript: `draft/follow-up-note-draft-v3.md`. Timestamp 2026-10-16T19:15:27Z.

- I3: the unresolved identifier, 10.13140/RG.2.2.30911.01443, is the ResearchGate DOI of the 2024 note. Deferred in `results/i3-researchgate-deferral.md`. Seven other DOIs resolved. A first pass of this scan also failed on `[49]` because the draft cited the cultivation supplement's own bibliography number in square brackets. That wording was changed to "bibliography number 49" and the re-run no longer reports a missing numbered ref.
- I1: 7 unbound percents (was 8 on v2; the extra 8% token in a second paragraph is gone). Cited priors under `i1_policy: advise`. Limited is the expected state for a commentary note.
- I5 is n/a. Unchanged: this scan does not mark the note scientifically verified.
