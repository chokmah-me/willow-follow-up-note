# Changelog

## Unreleased

DRAFT v3. Not minted. No public posting. The v3 integrity scan
is not a scientific verification. I3 is the deferred ResearchGate
DOI.

### 2026-10-18

- Four consistency fixes to the v3 draft after the distance-3
  rise calibration was recorded. Limitations: "I did not rerun
  the simulations" now reads "the paper's simulations," since
  the repository holds a calibration run of our own simulator.
  AI Utilization Statement: names the simulator (written by
  OpenAI GPT-6 Astra through OpenRouter from the author's
  briefs, reviewed and tested before use) and the calibration
  record, which is not a result of the note. Section V: the
  two cheaper checks "need no new hardware," not "no new
  hardware time" (three-state readout needs time on the
  team's processor). Draft date moved to October 18, 2026
  (7 Cheshvan 5787). No claim, score, or number changed.

### 2026-10-17

- Built the leakage hybrid simulator for Section V's
  re-simulation check (`simulator/`). v0: the qevol-style
  branch engine fused with the Pauli+ leakage layer of the 2023
  supplement, one label trajectory per shot. v1: grafted-memory
  circuit runner, Tesseract decoder pin (behavioral), metrics,
  and the design's four-arm sweep. Code written by GPT-6 Astra
  via OpenRouter (four calls, $1.6821 total), reviewed line by
  line; contract check PASS against the brief (BREAK 0,
  WEAKENS 3, all dispositioned). 59 of 59 tests pass. A
  distance-3 demonstration run behaves as designed; it is
  machinery, not evidence.
- Digitized the device figures of the cultivation supplement
  (`simulator/digitize/`). Figs. S5, S7, and S9 print every
  value as text in its cell: 54 qubits by 15 quantities and 89
  CZ pairs by 2, extracted by cell geometry, error limited to
  the print rounding. The S7 site-centered "0.00" strings are a
  plotting artifact and are excluded on evidence. Finding: the
  EDCF medians in Figs. S6 and S8 do not all reproduce from the
  map values (operating frequency 6.553 against a map median of
  6.46; CZ error 2.058 against 1.9, in units of 10^-3), so the
  EDCFs rest on a different sample than the maps.
- Recorded the 2023-signature substitution analysis
  (`results/2023-signature-substitution.md`): the joint test's
  rise leg can be scored against the 2023 paper's published
  signature, at the cost of rewording that leg from a fit to an
  instrument calibration.
- Adopted that substitution in Section V of v3 and in
  `results/section-v-simulation-design.md`. The 2026 ratio stays
  the grafted-circuit score. The rise is an instrument
  calibration against the 2023 fingerprint (12% experiment, 7%
  their Pauli+, risetime about 5 cycles). Covariance is a
  structural check. No run at design scale has been made.
- Made the |T> coefficient test independent of prune order
  (`simulator/test_leakage_hybrid.py`). Equal-weight branches
  can swap after magnitude sort when those magnitudes differ
  by an ulp.

### 2026-10-16

- Kept `draft/follow-up-note-draft.md` as the post-review copy.
- Added `draft/follow-up-note-draft-v2.md`. House byline and ORCID.
  Abstract cut to the inventory, the one direct hit, the hedge, and
  the untested remainder. IEEE references with URLs. Nature 2023
  pages set to 676-681. AI statement closer added. Phase-noise
  header no longer says the noise was engineered around.
- Applied the external-review items that were still open: what would
  damage the inventory, a scale caveat (one supplement memory
  experiment, one grafted configuration, at most nine cycles), a
  scorecard row for the echoed kickback measurement, grading
  direction under the table, channel 1 titled "signature present,
  attributed as likely," Kalai, Rinott, and Shoham (2023) cited in
  Section III.2. Removed the unused Stethoscopes reference. The
  header still says this note does not change Zenodo record 19651958.
- The leakage attribution stays "likely." The variability alternative
  and the missing ablation stay in the summaries.
- Added `integrity-manifest.json` (`i1_policy: advise`) and
  `results/` from the online integrity scan. I1 limited, I3
  unresolved on the ResearchGate DOI, I5 clear.
- Corrected the 2023 Nature page range in `sources/SOURCES.md` from
  676-687 to 676-681.
- Regenerated `AI-USE-STATEMENT.md` from the v2 section, including
  the no-co-author line and the Chokmah LLC affiliation.
- Deferred the I3 ResearchGate DOI miss. Record:
  `results/i3-researchgate-deferral.md`. The scan JSON is
  unchanged. Status in this repo is evidence-ready, not verified.
- Saved `results/robustness-check-v2.md` (own-draft robustness
  check, 18 frozen rows) and annotated `results/integrity_brief.md`
  (I3 resolver scope, I1 advise-only).
- Added `draft/follow-up-note-draft-v3.md` from the MUST-FIX
  pass. Process notes moved to `draft/process-log.md`. Six
  channels scored once. "Direct hit" removed. SI numbers labeled
  preprint v1. Akshay row dropped. Phase noise is a measurement
  story, not corroboration of the correlated channel. One TL;DR.
  CC BY 4.0 in the body. No Zenodo DOI minted. SEARCH-META in
  `draft/search-meta-v3.html` with PLACEHOLDER identifiers.
- Regenerated `AI-USE-STATEMENT.md` from the v3 AI Utilization
  Statement.
- Ran the online integrity scan on v3. I1 limited (7 unbound
  percents). I3 fail is the deferred ResearchGate DOI. A
  spurious `[49]` missing-ref fail was a wording parse; the
  draft now says "bibliography number 49".
- Robustness check of v3 saved (results/robustness-check-v3.md): 16 frozen rows run against v3 at 5b632ef; channel claims survive; one mild weakening (unqualified 40-fold at Section III.4).
- Saved `results/external-sme-review-instructions.md` (identical
  SME brief for the Section V simulation design) and
  `results/external-sme-review-simulation-design.md` (independent
  pass; verdict BUILD AFTER FIXES).
- Sources completed under the SI and peer review rule (2023 and
  2024 papers plus both Nature peer review files, recorded in
  sources/SOURCES.md). Section V simulation design saved with its
  SME review and the peer-review-files assessment (results/).
  Section III.4 of v3 now qualifies the 40-fold with the 22 to 44
  range, closing the robustness check's one weakening.
- Recorded `results/open-source-simulator-check.md`: the design's
  "no open-source Pauli+" line is too strong (leaky, deltakit-stim,
  public Tesseract). qevol remains unpublished. Search only; nothing
  run.
- Archived the Kimi second-opinion tooling report as
  `results/kimi-leakage-tooling-report.md` with
  `results/fig_recommended_stack.png` and
  `results/fig_tesseract_pypi_cadence.png`. Search only. Names SOFT
  as an open qevol-class engine; omits leaky; qevol unpublished.
