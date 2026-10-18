# Changelog

## Unreleased

DRAFT v4. Not minted. No public posting. v4 integrity scan
2026-10-18: limited, I3 offline. I3 is the deferred ResearchGate DOI.

### 2026-10-18 (v4 integrity scan)

- Ran manuscript-integrity-gate (75cb7f7) on v4 with `--online`.
  Status limited. I3: the session proxy blocked Crossref and
  Zenodo, so no identifier was checked; a networked re-run is owed.
  I1: 16 unbound cited percents, three of them Section V
  thresholds. I4: local simulator named in Limitations, no
  misalignment. I5: "first" warnings, not overclaims. Manifest now
  points at v4. Limitations: a semicolon after the Zenodo record id
  became a period, so the scanner reads one identifier, not two.
  Annotation in `results/integrity_brief.md`.

### 2026-10-18 (v4)

- Produced `draft/follow-up-note-draft-v4.md` from v3 by applying
  `external-review/critical-review-v3-pass3.md`. Source check
  against the local arXiv v1 text changed the causal reading:
  Section XIV gives unoptimized readout and |2> collisions as the
  entry path into leakage, not as alternatives. v4 names three
  routes: (a) readout to |2> to leakage (the authors' claim),
  (b) readout errors without |2> population, (c) qubit
  variability, plus decoder or model mismatch. Table 1 counts only
  (b), (c), and mismatch against leakage, and gains a 2026 verdict
  column. "No removal units" is now a precondition, not evidence.
- Section V: three-state readout in all four arms; p frozen on an
  unpostselected same-day memory circuit; removal-arm simulation
  includes the removal operations; pass margin (upper 95% bound on
  the ratio below 2), shot-count rule, and |2> criterion fixed in
  advance; outcomes moved to Table 3 keyed to the four arms.
- Abstract opens with the contribution, uses grafted-code wording,
  and says what a hit means; TL;DR cut to about 100 words. Table 2
  drops the echo/kickback row (it stays in the measurement story).
  LER unit stated as not given in Fig. S22; ratio range 6.2 to 7.1.
  p-cubed projection labeled the author's extrapolation. Gate
  baseline cites the main-text "similar to our physical qubit gate
  errors." Section I cites [4] for Google's numbers. N, p, d,
  SI1000, LER, qevol, Pauli+, DQLR, Tesseract defined; new refs
  [15] Miao 2023, [16] SI1000, [17] Tesseract. Ref [4] dated 2025.
  Repeated caveat sentences removed. Private repository URL removed
  from Availability. AI statement re-synced with
  `AI-USE-STATEMENT.md` and extended for this pass. Limitations
  again names the local d=3 calibration run.
- Not done: Zenodo mint. The supplement comparison, the reading
  of Marshall and Kafri [14], and the Table 2 grades from the 2024
  note's challenge table were completed in the 2026-10-18
  verification run (next entry). The Section I flag on the 14%
  figure is resolved in the same pass: it stays attributed to the
  2024 note [1], with the paper's own budget figure beside it
  (the error budget overpredicts Lambda by 20% [4]).
- Verification fix (2026-10-18): the latest-draft verification run
  recovered the 2024 note's challenge table in clean layout from
  the author's Mataroa mirror (read Oct. 18, 2026). Table 2 now
  carries all four objection rows; the restored row is
  Reachability deficits (Akshay et al.), Indirectly, unchanged,
  no evidence added. The Table 2 caption and Limitations name the
  mirror as the grades' source. The same run read Marshall and
  Kafri [14] and compared the published Science supplement on the
  scored items: numbers and wording unchanged from v1, numbering
  moved (Sec. XIV to VIII; S22 to S20, S23 to S21, S24 to S22,
  S14 to S11). The note's pins stay on v1, so its supplement
  disclosure stands.
- Consistency fix: the draft's three "not compared" sentences
  (Sec. II, Limitations, AI statement) now match the verification
  run. Sec. II gives the v1-to-published renumbering; pins stay on
  v1. `AI-USE-STATEMENT.md` re-synced.
- Sec. V: deleted the sentence saying [14] was not read.
- Added reference [18], the author's Mataroa mirror of [1], cited
  in the Table 2 caption and Limitations.

### 2026-10-18

- Applied a second critical pass on v3. Variability stays in the
  abstract and TL;DR as the alternative on the earlier grafting
  figure, and Section XIV's own alternatives (readout calibration
  and |2> collisions) are named for the seven-fold gap. Zenodo
  10.5281/zenodo.17872003 was opened: detector files for Figs. 2,
  3, and 4 (Fig. 4 at N = 2 and N = 3), no N = 9 directory.
  The 2023 rise numbers are pinned as averages. The 2 by 2 freezes
  p = 2.3e-3 from a same-day non-grafted control. Hebrew date
  prefix removed. Local simulator output stays out of the note.
  Zenodo mint (C4) and making the GitHub repo public were not
  done. Science DOI 10.1126/science.aee7961 confirmed as First
  Release, Oct. 15, 2026, still with no volume or pages.
- Applied the MUST-FIX and SHOULD-FIX items from the 2026-10-18
  critical pass on v3. Abstract: dropped numbered citations.
  Byline: the 2024 note scored here is the author's. Formula 77
  labeled as the 2024 note's name and matched to Pauli
  simulations in Google 2024 [4], Fig. 1b. Channel rubric
  captioned Table 1; standing table is Table 2, with the
  echo/kickback row labeled a 2026 measurement. Section V:
  three-state readout uses the existing processor and the
  team's runtime; the leakage-injected rerun needs no device.
  Limitations: the local simulator and d=3 calibration sit in
  the repository and are not a result of this note. Conclusion:
  cut "good news for quantum computing." SEARCH-META dates set
  to 2026-10-18; DOI left PLACEHOLDER. Draft converted to LF.
  Zenodo mint (C4) left to the author. No score or number
  changed. "Likely," variability, and no-ablation left in
  place in the abstract, TL;DR, and conclusion.
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
