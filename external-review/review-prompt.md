# External review prompt (identical for both models)

Sent 2026-10-16 via OpenRouter to moonshotai/kimi-k3 and
anthropic/claude-opus-5.5. Each model received the fact sheet and
the task below, followed by the full text of the note in its
pre-revision form (status header stripped, so neither model knew
about the internal adversarial review). The pre-revision draft
text is not reproduced here; the current draft is in ../draft/,
and the differences are itemized in REVISIONS-APPLIED.md.

---

VERIFIED FACT SHEET (checked against the primary sources by the author's team; treat as ground truth for judging the note's claim handling):
- The cultivation paper (Rosenfeld et al., Science 2026, DOI 10.1126/science.aee7961; arXiv:2512.13908v1) reports magic-state cultivation on Willow: error cut by a factor of 40, fidelity 0.9999(1) ("at least 0.9999(1)" in the Science abstract), 8% of attempts retained.
- The factor-of-7 figure is NOT the headline result. It is the logical error rate of a grafted-code memory experiment in the supplement (Sec. XIV, Fig. S22), about 7x higher than SI1000 depolarizing simulations at p = 2.3e-3.
- The authors call leakage "likely" the main source of that gap, from two signatures (detection likelihood rising over time, Fig. S23; time-correlated detector covariance, Fig. S24). There is NO ablation run with leakage removal. The main text also keeps physical qubit performance variability open as an alternative.
- The simulations do not include leakage. The grafting circuits did not contain leakage removal units.
- Low-frequency phase noise made standard logical state tomography return a non-physical norm; the team built kickback tomography in response. Their text says simulations "suggest" performance without echos was dominated by this noise, and "suggest" the echoed performance is limited by gate error and decoherence.
- The author's Dec 2024 note (DOI 10.13140/RG.2.2.30911.01443) built a six-channel error inventory (gate, readout, leakage, crosstalk, correlated, classical chaos) against Google's simplified noise model, with leakage at about 10% of the error budget, mitigated by a removal step (DQLR), and a challenge table grading skeptical objections (noise sensitivity: Partially; nonlinear errors: Indirectly; reachability: Indirectly; classical chaos: Partially).

---

You are an external reviewer. Give a critical evaluation of the short follow-up note below. The author is an independent researcher; the note scores a new Google experiment against an inventory from his own 2024 note. He wants criticism, not praise. Do not be polite at the expense of accuracy.

Evaluate:
1. Soundness: does the note's central move (scoring an experiment that was not designed to test his inventory, against that inventory) hold up, or is it self-serving framing? Where exactly does it overreach or underreach?
2. Claim discipline: using the fact sheet, find any place where the note states more than the sources support, states less, or hedges in the wrong place. Name the sentence.
3. Structure and rhetoric: does the scorecard format clarify or does it force the evidence into boxes? Are the three TL;DR summaries honest compressions?
4. The settling experiment proposed in Section V: is it the right test, is it feasible as stated, and are the three pre-scored outcomes the right ones?
5. Anything missing that a critical reader would demand: prior work, alternative explanations, conflicts, or context.
6. Verdict, one of: PUBLISH AS IS / PUBLISH WITH REVISIONS / DO NOT PUBLISH, with the specific revisions you require, in priority order. If you require a revision, quote the sentence or name the section.

Keep it under 1,200 words. Be specific. Quote sentences when you fault them.
