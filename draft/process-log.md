# Process log (not part of the note)

Moved out of the paper body 2026-10-16. The shipping text is
`follow-up-note-draft-v6.md`. Older drafts stay as the audit trail.

## 2026-10-18 figure and sketchnote

Figure 1 was added to Section V of v6. The sketchnote is
`results/sketchnote-v6.png`, and its results panel copies that
figure. No DOI minted. No push.

## Status trail

DRAFT. Not published, not posted, no DOI reserved. Standalone
follow-up to the Dec 2024 paper. It does not amend that paper,
and it does not change any number in the Zenodo OTOC paper
(v2.0, record 19651958).

Sources pinned:

- Bilar (2024), Notes on Google Willow, DOI
  10.13140/RG.2.2.30911.01443, read in full 2026-10-16.
- Rosenfeld et al. (2026), Magic state cultivation on a
  superconducting quantum processor, Science, DOI
  10.1126/science.aee7961 (Science release of Oct 15, 2026).
  Science abstract read on science.org 2026-10-16. Full text and
  supplement read as arXiv:2512.13908v1 (Dec 15, 2025). The
  Science supplement was not page-diffed against v1.
- Google Quantum AI blog post, Oct 15, 2026, read in full.
  Diagnosis of phase noise in v3 is sourced from the v1
  supplement, not from the blog.

Drafting rule: the leakage attribution in the cultivation paper
is "likely," with signature evidence and no ablation run. Keep
that word. Never upgrade it.

## Review trail (2026-10-18, second pass)

Applied the pasted MUST-FIX and SHOULD-FIX items to v3.

- Zenodo 17872003 file list and README read. fig4.zip central
  directory listed: injection_N=2, cultivation_N=2,
  simulation_injection_N=2, cultivation_N=3. fig2 and fig3 top
  folders have no N=9 directory. S23 and S24 stay unchecked
  numerically.
- 2023 rise sentence in the local arXiv text is a rise in the
  average detection probability (12% d=5, 8% d=3, Pauli+ 7% at
  d=5, risetime about 5 cycles). Fig. S23 is "for some detectors."
- Science page for 10.1126/science.aee7961 read via search:
  First Release, 15 Oct 2026, abstract includes "at least
  0.9999(1)". A script GET of doi.org returned 403 for that DOI,
  for the ResearchGate DOI, and for the Entropy DOI. The
  ResearchGate HTML of the 2024 note showed a garbled challenge
  table; column headers were not recovered cleanly.
- Marshall and Kafri, Phys. Rev. Applied 23, 054025 (2025), DOI
  resolved. The article was not read.
- C4 mint not done. Repository confirmed private
  (`gh repo view`: isPrivate true). Left private.
- "Likely," no removal run, and variability (now located on the
  earlier grafting figure) kept in the abstract, TL;DR, and
  conclusion.

## Review trail (2026-10-16)

Adversarial: contract-certifier trace plus contract-breaker pass,
files in `adversarial/`. BREAK 1, WEAKENS 4, all accepted and
fixed (F1 to F5, certifier scope fix G1, voluntary softening of
the F6 superlative). Record: `adversarial/ADJUDICATION.md`.

External: Kimi K3 and Opus 5.5 via OpenRouter, files in
`external-review/`. Both PUBLISH WITH REVISIONS. Agreed
revisions applied the same day. Record:
`external-review/REVISIONS-APPLIED.md`.

v2: house style, IEEE refs, inventory-level falsifiability,
scale caveat, scorecard row for echoed kickback, grading
direction, channel 1 header, Kalai 2023 cite, Stethoscopes
reference removed.

v3: MUST-FIX from a later critical pass. Process notes stripped
from the paper. Six channels scored once. "Direct hit" removed.
SI numbers labeled preprint v1. Akshay row dropped. Phase noise
is a measurement story, not corroboration of the correlated
channel. One TL;DR. CC BY 4.0 in the body. No Zenodo DOI
minted in this pass.

2026-10-17: adopted the 2023 rise-leg substitution in Section V.
The cheaper simulation check now asks for the 2026 gap on an
instrument calibrated to the 2023 published fingerprint [12].
Grafted-circuit rise is a prediction. Covariance is a structural
check. "Likely," variability, and no-ablation left in place.

2026-10-18: consistency fixes after the calibration run was
recorded. Limitations now say the paper's simulations were not
rerun (the repository holds a calibration run of our own
simulator, which is not the paper's). The AI statement names
the simulator's author and the calibration record. Section V
no longer claims the cheaper checks need no hardware time;
they need no new hardware. Date moved to October 18.

2026-10-18 (later): critical-review MUST-FIX and SHOULD-FIX
applied to v3. Abstract cites dropped. Byline conflict line
restored. Formula 77 tied to [1] and to Pauli simulations in
[4]. Tables numbered 1 (channels) and 2 (standing after
cultivation). Section V splits the cheaper checks by who
runs them and what they consume. Limitations names the local
simulator and d=3 calibration as not a result. Conclusion
cut the "good news" sentence. SEARCH-META dates filled;
DOI unminted. LF line endings. "Likely," variability, and
no-ablation rechecked in abstract, TL;DR, and conclusion.

2026-10-18 (v4): third critical pass
(`external-review/critical-review-v3-pass3.md`) applied as a new
file, `follow-up-note-draft-v4.md`. Section XIV re-read in the
local arXiv text: readout and |2> collisions are the authors'
entry path into leakage. Three routes kept apart. Section V pass
margin and |2> criterion fixed in advance; Table 3 holds the
readings. "Likely," variability, and no-ablation rechecked in the
abstract, TL;DR, and conclusion. The earlier entry's claim that
Limitations names the d=3 calibration is true again in v4.

2026-10-18 (v4 verification fix): the verification run on the
latest draft recovered the 2024 note's challenge table in clean
layout from the author's Mataroa mirror: four rows (Noise
Sensitivity Partially, Nonlinear Errors Indirectly, Reachability
Deficits Indirectly, Classical Chaos Partially). v4's Table 2
carried three rows; the Reachability deficits row (Akshay et al.)
is restored as Indirectly, unchanged, no evidence added. Table 2
caption and Limitations now name the mirror as the source of the
grades. Same run: Marshall and Kafri [14] read; published Science
supplement compared on the scored items, unchanged in substance
from v1, renumbered only. Draft pins stay on v1.

2026-10-18 (v4 leftover fixes): the two items flagged after the
verification fix are closed. (1) The CHANGELOG "Not done" list no
longer lists done work: of its four items, only the Zenodo mint
remains undone; the supplement comparison, the Marshall and Kafri
reading, and the Table 2 grades were completed in the verification
run. (2) Section I's 14% flag: the figure stays attributed to the
2024 note [1], and the Willow paper's own budget figure now stands
beside it, from the arXiv text of [4]: applying the same decoder
to the experimental data, the error budget overpredicts Lambda by
20%. No score or other number moved.

2026-10-18 (v4 consistency): Sec. II, Limitations, and the AI
statement no longer say the Science supplement was not compared.
They now record the comparison on the scored items and the
renumbering. Open: Sec. V still says [14] was not read, and the
Mataroa mirror has no URL or reference entry.

2026-10-18 (v4 [14] line): the Sec. V sentence saying [14] was not
read is deleted at the author's instruction. Still open: a URL or
reference entry for the Mataroa mirror.

2026-10-18 (v4 [18]): Mataroa mirror added as reference [18] and
cited where Table 2 and Limitations name it. No open items besides
the Zenodo mint.

2026-10-18 (v4 scan): integrity scan run on v4, status limited.
I3 could not reach Crossref or Zenodo from the session; re-run
online from a networked machine before release.

2026-10-18 (v5): inverted at the author's direction after an
assessment that the 2024 self-scoring frame hid the note's useful
parts. v5 leads with the attribution reading, the missing N = 9
data, and the pre-registered 2 by 2; the 2024 inventory is one
context section. "Likely," variability, and no-ablation rechecked
in the abstract, TL;DR, and conclusion. Scan re-run: limited.

2026-10-18 (v6): critical review of v5 applied. Route predictions
against S23 and S24 added; Section IV readings re-based on the
same-run baseline; "likely," variability, and no-ablation rechecked
in the abstract, TL;DR, and conclusion. Scan re-run: limited.
