# Integrity brief — willow-follow-up-note

## Status
willow-follow-up-note — limited (I1 limited unbound 10; I3 limited (0 resolved, 0 unresolved))

## Reproduce
```
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --propose-bindings
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --online
```

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | unbound buckets {'other': 10} |
| I2 protocol | n/a | |
| I3 references | limited | existence via Zenodo/Crossref/OSF APIs for identifiers in this draft — not a four-API ScientistOne audit; not citation support |
| I4 method–artifact | limited | |
| I5 overclaim | warn | |

## Residual human gates
none from this scan

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`

## Annotation (2026-10-18, v6 scan)

Manuscript: `draft/follow-up-note-draft-v6.md`. Status limited, same
session network as the v4 and v5 scans: I3 reached neither Crossref
nor Zenodo; offline, all 19 numbered references resolve in the list,
including the new [18] (Akshay et al.). I1: 10 unbound percents, all
cited figures or Section IV thresholds (the new "15%" shot-count
margin and the "95%" bounds are design parameters, not results). I4:
local simulator named in Limitations, no misalignment. I5: "first"
phrasing, not overclaims. A networked `--online` re-run is still
owed. This scan does not mark the note scientifically verified.

