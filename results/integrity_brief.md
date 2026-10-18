# Integrity brief — willow-follow-up-note

## Status
willow-follow-up-note — limited (I1 limited unbound 16; I3 limited (0 resolved, 0 unresolved))

## Reproduce
```
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --propose-bindings
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --online
```

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | unbound buckets {'other': 16} |
| I2 protocol | n/a | |
| I3 references | limited | existence via Zenodo/Crossref/OSF APIs for identifiers in this draft — not a four-API ScientistOne audit; not citation support |
| I4 method–artifact | limited | |
| I5 overclaim | warn | |

## Residual human gates
none from this scan

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`

## Annotation (2026-10-18, v4 scan)

This scan's "limited" is a status of the scan, not a verdict on the
note. Manuscript: `draft/follow-up-note-draft-v4.md`. Timestamp
2026-10-18T08:10:06Z. Run from a cloud session whose network proxy
blocks api.crossref.org and zenodo.org.

- I3 limited: all 12 identifiers returned no HTTP response (http 0).
  Nothing was resolved and nothing was found missing. This is weaker
  evidence than the v3 scan, where seven DOIs resolved and the
  ResearchGate DOI failed. The four DOIs new in v4 (Miao 2023,
  SI1000/Quantum, the Science article, Marshall and Kafri) are
  unchecked online. Tesseract and the Mataroa mirror carry no DOI.
  The deferral in `results/i3-researchgate-deferral.md` still stands.
  Re-run with `--online` from a networked machine before release.
  No offline citation finding: all 18 numbered references resolve
  in the reference list.
- I1 limited: 16 unbound percents (7 on v3). Under `i1_policy:
  advise`, cited priors are expected. New since v3: the 20% budget
  figure [4]; the 8% retention (three mentions) and the 12%, 8%, 7%
  2023 rises, all cited; and three "95%" tokens that are Section V
  design thresholds, not reported results.
- I4 limited: the scanner found the local simulator because v4's
  Limitations names it. Alignment judgment: the note reports no
  simulator output and makes no method claim the simulator would
  have to support. No misalignment.
- I5 warn: "first" (a first grafted-code memory run; checks that
  come first) and "First Release" in reference [2]. Not overclaims.
- Unchanged: this scan does not mark the note scientifically
  verified.

