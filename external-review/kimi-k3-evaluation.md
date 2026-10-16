# Review: "Willow, Tested Again"

## 1. Soundness

The central move — scoring an experiment against an inventory it was not designed to test — is legitimate as a monitoring exercise, and the note is more disciplined about it than most self-citation follow-ups. "It is not a memory experiment, and it was not designed to test my inventory. It tests it anyway" is the overreach: incidental evidence is not a test, and the note's own careful gradations (tested/touched/not tested) belie the sentence.

The deeper problem is that the scorecard is a one-way ratchet. Hits count *for* the inventory; misses count as "not tested," never against it. No possible outcome of this experiment could have counted against a channel — had the gap matched simulation with leakage removal in place, the channel would presumably have been "mitigated, still real." "Nothing in the 2024 note needs correction" is therefore unfalsifiable framing, not a finding. The note should state what observation *would* have damaged the 2024 inventory.

There is also a silent restructuring of the inventory. The 2024 channels were gate, readout, leakage, crosstalk, correlated, classical chaos. Section III scores: leakage, **low-frequency phase noise**, crosstalk, correlated, gate-and-readout (merged), chaos-and-nonlinear (merged). Phase noise has been promoted to a standalone channel and gate/readout merged to keep the count at six — without telling the reader. Worse, this contradicts the note's own anti-double-counting discipline: in channel 4 the author warns that scoring correlated errors from the leakage covariance "would be double-counting," yet phase noise — which the note itself ties to the 2024 Kalai non-stationary-noise objection, i.e., the correlated-errors row — is counted as a *second* "direct hit" in the abstract. By the note's own standard, it claims two hits where its logic permits one-and-a-half.

## 2. Claim discipline

Mostly good — the handling of "likely" is exemplary, and the note correctly reports the open alternative (physical-qubit performance variability) and the absence of an ablation run. Faults:

- **"Detector covariance shows strong time correlations that propagate across the qubit grid (their Fig. S24), which the authors describe as the characteristic leakage pattern."** The verified record supports "time-correlated detector covariance" and leakage attribution as *likely*. "Propagate across the qubit grid" and "characteristic leakage pattern" are embellishments not in the verified record. Quote the supplement or delete.
- **"The supplement names a path in: … frequency collisions involving the |2> state may have followed, with leakage after them."** Unverifiable mechanism detail presented with confidence. Cite the section or flag as paraphrase.
- **"their simulations bound the remaining detuning contribution near 1e-5 in infidelity"** — specific number, not verifiable against the record; needs a pinpoint citation.
- Layman TL;DR: **"I listed that leak, by name, in 2024."** True and self-serving. Per your own Section I, Google's *own* 2024 error budget carried leakage at ~10% and Google built DQLR years ago. Naming a channel the hardware team already budgeted and engineered against is not a prediction; the sentence claims priority for the obvious. The defensible claim is narrower: you flagged that the *simplified models* omitted it, and the 2026 simulations omitted it again.
- The layman TL;DR's "stored the ingredient in a stronger safe, it degraded seven times faster" elides that this is a supplementary diagnostic, not the cultivation pipeline — the body ("The result I score here is not in the headline list") is honest; the TL;DR is not quite.

## 3. Structure and rhetoric

The scorecard format genuinely clarifies — the tested/touched/not-tested gradation is the note's best feature. But it forces boxes in two ways: the renumbering above, and the ratchet asymmetry. The three TL;DRs are well-calibrated overall; the Non-Hype TL;DR is the most honest paragraph in the document and the abstract should be rewritten to sound like it. The uncited self-reference (Bilar 2026, Zenodo) in the reference list is padding. "Akshay et al." appears in the challenge table with no corresponding reference entry — a concrete omission. The Hebrew epigraph is the author's business; it costs nothing.

## 4. Section V

The proposed test — rerun the grafted-code memory experiment with leakage removal units — is the right idea; it is exactly the ablation whose absence the note deplores. As stated it is not a clean design:

1. LRUs add operations and hence errors; "unchanged except for" is not achievable, so outcome two ("gap narrows in part") is confounded between leakage-removal benefit and LRU overhead.
2. The note itself reports that readout parameters were not re-optimized for the redefined measurement pattern. The decisive design is a 2×2: {LRU, no LRU} × {readout re-optimized, not}, otherwise gap closure after *any* fix will be credited to leakage ambiguously.
3. Outcome three is scored too strongly: if the gap does not move, the signatures in S23/S24 "need another explanation," yes, but they remain leakage-shaped; "the attribution fails" overstates — LRUs address |2>-state population, and if the entry path is frequency-collision-driven readout leakage (the note's own claimed mechanism), LRUs alone may not fix it. The three outcomes should be pre-registered against *both* fixes, and a null result needs its own sub-interpretations.

## 5. Missing

- **Prior art:** Leakage in superconducting QEC is a decade-old, heavily worked topic (Suchara/Cross/Gambetta on leakage in surface codes; Google's own DQLR line; Varbanov et al.). The note cites none of it, which sustains the inflated "I listed that leak" framing.
- **Alternative explanations:** only qubit-performance variability is named; calibration drift and the readout re-optimization issue deserve equal billing, since the paper reportedly names them too.
- **Conflicts:** the author scores his own prior note against a result he is invested in; a one-line disclosure of this obvious conflict would be honest. The "Stethoscopes" self-reference suggests a prior commitment to correlated-noise centrality that should be declared.
- **Scale caveat:** one supplement figure (S22) from one grafting configuration is thin evidence for a channel-level verdict; the note should say so.

## 6. Verdict: **PUBLISH WITH REVISIONS**

Required, in priority order:

1. Fix the channel accounting. Either map phase noise explicitly onto the 2024 correlated-errors row (and claim one hit plus one corroboration) or acknowledge in the abstract that the six channels were re-partitioned. Delete or justify "Two channels