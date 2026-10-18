# Integrity brief — willow-follow-up-note

## Status
willow-follow-up-note — limited (I1 limited unbound 8; I3 limited (0 resolved, 0 unresolved))

## Reproduce
```
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --propose-bindings
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --online
```

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | unbound buckets {'other': 8} |
| I2 protocol | n/a | |
| I3 references | limited | existence via Zenodo/Crossref/OSF APIs for identifiers in this draft — not a four-API ScientistOne audit; not citation support |
| I4 method–artifact | limited | |
| I5 overclaim | warn | |

## Residual human gates
none from this scan

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`

## Annotation (2026-10-18, v5 scan)

Manuscript: `draft/follow-up-note-draft-v5.md`, the inverted draft.
Status limited, same session network as the v4 scan: I3 could not
reach Crossref or Zenodo, so no identifier was checked; all 18
numbered references resolve in the reference list offline, after
renumbering by first citation. I1: 8 unbound cited percents (the 2024
budget figures left the body with the scorecard; the 8% retention,
the 2023 rises, and three Section IV "95%" thresholds remain). I4:
local simulator named in Limitations; the note reports no simulator
output, no misalignment. I5: "first" (the abstract's "First, a
reading", "a first grafted-code memory run", "run first") and
"First Release" in a reference; not overclaims. A networked
`--online` re-run is still owed. This scan does not mark the note
scientifically verified.

