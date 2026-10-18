# Integrity brief — willow-follow-up-note

## Status
willow-follow-up-note — limited (I1 limited unbound 12; I3 limited (9 resolved, 0 unresolved))

## Reproduce
```
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --propose-bindings
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --online
```

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | unbound buckets {'other': 12} |
| I2 protocol | n/a | |
| I3 references | limited | existence via Zenodo/Crossref/OSF APIs for identifiers in this draft — not a four-API ScientistOne audit; not citation support |
| I4 method–artifact | limited | |
| I5 overclaim | warn | |

## Residual human gates
none from this scan

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`
