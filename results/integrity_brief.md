# Integrity brief — willow-follow-up-note

## Status
willow-follow-up-note — limited (I1 limited unbound 13; I3 pass (19 resolved, 0 unresolved, 1 grandfathered))

The 2024 ResearchGate DOI `10.13140/RG.2.2.30911.01443` is grandfathered by the author on 2026-10-19. Crossref has no record. DataCite does: client `rg.rg`, issued 2024, title matching the 2024 note. The creator string there is "Daniel Yaacob Bilar," which is not the house byline. The reader path stays the ResearchGate URL in reference [13]. This pass is not a scientific verification. The draft was not edited.

## Reproduce
```
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --propose-bindings
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note
python path/to/manuscript-integrity-gate/scripts/audit_manuscript.py --project willow-follow-up-note --online
```

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | unbound buckets {'other': 13} |
| I2 protocol | n/a | |
| I3 references | pass | existence via Zenodo/Crossref/OSF APIs for identifiers in this draft — not a four-API ScientistOne audit; not citation support |
| I4 method–artifact | limited | |
| I5 overclaim | warn | |

## Residual human gates
none from this scan

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`
