# Integrity brief — willow-follow-up-note


## Status
willow-follow-up-note — fail (I1 limited unbound 8; I3 fail (8 resolved, 1 unresolved))


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
| I3 references | fail | existence via Zenodo/Crossref/OSF APIs for identifiers in this draft — not a four-API ScientistOne audit; not citation support |
| I4 method–artifact | n/a | |
| I5 overclaim | n/a | |


## Residual human gates
none from this scan


## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`

## Annotation (2026-10-16, reading of this scan)

This scan's "fail" is a status of the scan, not a verdict on the note.

- I3: the unresolved identifier, 10.13140/RG.2.2.30911.01443, is the ResearchGate DOI of the 2024 note. It is not resolved by the Crossref lookup this scan uses. The paper exists: it was read in full via ResearchGate on 2026-10-16 and is indexed as OpenAlex W6960451445. Reference [1] of the draft keeps the DOI and adds the ResearchGate URL, so a reader can resolve it without Crossref. Do not fix this by removing the DOI.
- I1: the 8 unbound percents are cited priors, not new measurements, under i1_policy "advise" in integrity-manifest.json. This note has no local results artifact, and none will be invented to bind them. "Limited" is the expected state for a commentary note.
- Unchanged from the brief above: this scan does not mark the note scientifically verified.
