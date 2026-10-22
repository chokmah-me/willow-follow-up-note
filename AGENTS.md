# AGENTS.md — willow-follow-up-note

Working draft of the follow-up note to *Notes on Google Willow (2024)*. Current copy is v6. A Zenodo mint is not a scientific Verified.

## Commands

No paper build. Simulator tests:

```powershell
python -m pytest simulator/
```

## Work rules

- Edit `draft/follow-up-note-draft-v6.md`. Older `draft/follow-up-note-draft-v*.md` files are the audit trail.
- No em dashes. Keep the authors' word "likely" on leakage attribution in summaries and the conclusion.
- Any edit to a summary, TL;DR, or conclusion reopens the hedge: recheck that "likely," the variability alternative, and the no-ablation fact survive.
- Do not invent a local results artifact for the cited rates. `integrity-manifest.json` sets `i1_policy` to `advise`.
- `held-note/` stays held. The Section V removal experiment is not runnable here.

## Pointers

- `README.md` — draft status, DOI pair, open items
- `draft/follow-up-note-draft-v6.md` — working copy
- `adversarial/` / `external-review/` — review trail
- `simulator/` — leakage hybrid; not a result of the note
- `ZENODO.md` / `CITATION.cff` — cite / DOI map
