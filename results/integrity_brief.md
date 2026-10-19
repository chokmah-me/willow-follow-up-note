# Integrity brief — willow-follow-up-note

## Status
Fail. Standing block is I3: `10.13140/RG.2.2.30911.01443` was not found in Crossref. This is not a scientific verification.

## Reproduce
```
python C:\Users\Elke Shayna\Documents\00Dev\manuscript-integrity-gate\scripts\audit_manuscript.py --project C:\Users\Elke Shayna\Documents\00Dev\willow-follow-up-note --manuscript C:\Users\Elke Shayna\Documents\00Dev\willow-follow-up-note\draft\follow-up-note-draft-v6.md --propose-bindings
python C:\Users\Elke Shayna\Documents\00Dev\manuscript-integrity-gate\scripts\audit_manuscript.py --project C:\Users\Elke Shayna\Documents\00Dev\willow-follow-up-note --manuscript C:\Users\Elke Shayna\Documents\00Dev\willow-follow-up-note\draft\follow-up-note-draft-v6.md --online
```
Scan date: 2026-10-19. Exit code 1. `i1_policy` in `integrity-manifest.json` is `advise`.

## Surfaces
- Manuscript: `draft/follow-up-note-draft-v6.md` (minted version of record 10.5281/zenodo.23455661)
- Bibliography: numbered references inside that file. No `.bib`.
- Results / code: `results/`; simulator under `simulator/` is declared in the note as not a result of the note

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | 13 unbound `other` tokens under advise policy. Not a new-measurement mismatch. |
| I2 protocol | n/a | No "we prove", "verified", or "reproduced" in v6. |
| I3 references | fail | 17 identifiers resolved. 2 script-unresolved. One is a real Crossref miss. One is a wrong-registry miss. |
| I4 method–artifact | limited | Simulator files exist. The note says they are not its result. No algorithm-class contradiction found. |
| I5 overclaim | warn | Scanner flagged "First" / "first". Those are "First, a reading" and "First Release", not a novelty claim. |

## Blocking
1. I3. Reference [13], DOI `10.13140/RG.2.2.30911.01443`, returned no Crossref record. The same deferral is already in `integrity-manifest.json` and `results/i3-researchgate-deferral.md`. The reader path is the ResearchGate URL in that reference. The minted draft was not edited. Removing the DOI would hide the identifier to force a pass.

The script also failed `10.17605/OSF.IO/QME2W` because it asked Crossref. The same node resolved as `osf:qme2w` through the OSF API, and DataCite lists `10.17605/osf.io/qme2w` as findable, title matching v6, created 2026-10-18. That second fail is a resolver limit, not a missing record. It does not clear the ResearchGate block.

## WARN
1. I5 lexicon: "First" in the abstract's "First, a reading" and "First Release" in reference [1]. Not treated as a priority claim.
2. Citation support is not a full passage check. A separate Lucerna read of v6 against arXiv:2512.13908v1 found one stronger gloss: v6 says the supplement cites Marshall and Kafri (its refs 38 and 43) for leakage modeling. The in-text uses found are SI1000 on Fig. 2 and simulation bookkeeping. Recorded here as support WARN, not an I3 existence fail.

## I1 reading of the 13 unbound tokens
- `12%`, `8%`, `7%`: cited from the 2023 surface-code paper, reference [5]. Prior cited, not a local result.
- `8%` retention: cited from the cultivation paper's retained-attempt figure.
- `95%` and `15%`: the note's own pre-registered pass rules in Section IV. Design text, not a measured outcome.
- `100%`: the HTML `width: 100%` on Figure 1. Not a result.

## Not checked here
- Re-running the leakage simulator or any computational-claim gate
- Lean
- Whether each cited paper supports every sentence (beyond the one Marshall WARN)
- Scientific importance
- Deposit prose and badges after mint

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`
- `results/proposed_bindings.json`

## Residual human gates
The ResearchGate DOI remains unresolved in Crossref. A reader uses the URL in reference [13]. No further mint step belongs to this gate.
