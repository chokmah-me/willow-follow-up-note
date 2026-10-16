# Review: "Willow, Tested Again"

## 1. Soundness of the central move

Scoring an experiment that was not designed to test an inventory can be legitimate, but only if the scoring is symmetric. Here it is not.

**The inventory is re-carved to fit the paper.** The 2024 inventory had six channels: gate, readout, leakage, crosstalk, correlated, classical chaos. Section III scores a different six:
- Gate and readout are merged into one row (channel 5).
- Hirota's "nonlinear errors" is folded into the chaos row (channel 6).
- "Low-frequency phase noise" is inserted as channel 2.

Phase noise was never one of the six. The abstract's "Two channels take direct hits" therefore counts a channel the 2024 note did not list. At best it can be filed under Kalai's noise-sensitivity objection or under "correlated." This is the most serious soundness problem, because the abstract's headline count depends on it.

**Disconfirming evidence is omitted.** The fact sheet says the team's simulations "suggest the echoed performance is limited by gate error and decoherence." That means the headline result, a 40× reduction in error, is consistent with the simplified noise model the 2024 note criticized. A symmetric scorecard would record that as a point against the thesis that omitted channels decide performance. The note never does.

**The leakage "hit" is weaker than framed.** Leakage was already about 10% of Google's own 2024 error budget, and DQLR was Google's own fix. A run that omits the fix and then shows leakage signatures is evidence that the known mitigation is needed. It is not evidence that the inventory identified a hidden channel. "It moved to the storage step" is rhetoric. Leakage is there because the removal units were left out, not because it migrated.

**"Nothing in the 2024 note needs correction" overreaches.** By the note's own count, most channels are untested. Absence of disconfirmation is not confirmation.

## 2. Claim discipline

**Overreach**

- **Layman TL;DR:** "I listed that leak, by name, in 2024." Google listed it first, in its own error budget. The sentence claims priority the author does not have. The same TL;DR also drops the variability alternative and the absence of an ablation run.
- **SME TL;DR:** "The authors attribute the gap, as likely, to population leakage…" The hedge is preserved, but the main-text alternative (physical qubit performance variability) is cut. Two of the three summaries lose it.
- **Channel 1 header:** "tested, likely hit." The word "tested" contradicts the note's own concession that there is no controlled run. Use "signature present, attributed as likely."
- **Section IV:** "a second, independent documentation." It comes from the same team, the same processor family, and the same known channel. It is a second documentation, but not an independent one.
- **Reachability row (Akshay et al.).** Reachability deficits concern variational ansätze such as QAOA. Comparing a magic-state error of 2×10⁻⁵ against the RSA-2048 requirement of 1×10⁻¹⁰ is a category error. Also, Akshay et al. is absent from the references.

**Claims that go beyond the fact sheet.** These may be true, but each needs a pinpoint citation:
- "their simulations of coherent phase noise reproduce the effect"
- the ~1×10⁻⁵ residual detuning bound
- the "months of diagnosis" in the blog post
- the list of candidate noise sources
- the |2⟩ frequency-collision path
- "between 1 and 2 times 1e-4"
- the 2×10⁻⁵ projection at half the noise
- "a number the cultivation paper itself states" (the 1×10⁻¹⁰ figure)
- the "1e-6 to 1e-8 range," which is unsourced

**Hedging in the wrong place**

- "the team's own comparison suggests" should say *simulations* suggest.
- "Score this channel as a hit" is unhedged, even though the hit was diagnosed, mitigated, and is reported as no longer limiting performance. That is arguably evidence of tractability, which runs against Kalai's objection.
- "0.9999(1)" carries an uncertainty equal to the error itself. A note about calibration should say so.

**Arithmetic.** "Four to five orders of magnitude short." The gap from 2×10⁻⁵ to 1×10⁻¹⁰ is about 5.3 orders. From the measured value of about 1×10⁻⁴, it is about 6.

**Underreach.** The note does not report whether the cultivation result matched pre-experiment simulation, which is its most relevant fact. It also gives no uncertainty on the "seven times" figure, which rests on nine cycles.

## 3. Structure and rhetoric

The scorecard forces evidence into boxes. Row merges and insertions let the abstract claim two "direct hits" from a paper that hits, at most, one original channel.

The challenge table's grading direction is also ambiguous. If "Partially" means Google partially addressed an objection, then new evidence of the problem should not leave the grade unchanged. "The annotation is about the weight of evidence, not its direction" does not resolve this.

The three TL;DRs compare as follows:

| TL;DR | Assessment |
|---|---|
| Non-hype | Honest, and the best of the three. |
| SME | Accurate, but drops the alternative explanation. |
| Layman | Not an honest compression. It ends on self-credit, and it is the version most readers will share. |

## 4. The Section V settling experiment

The direction is right: an ablation is the correct test. As specified, however, it has four problems.

**The proposed run is confounded.**
- Leakage removal units add gates, duration, and their own error. "Unchanged except for" is not achievable.
- The note's own leakage path runs through unoptimized readout in the redefined configuration. Recalibrating readout is a separate intervention that the design does not separate out.
- A 2×2 design is needed: leakage removal on/off × readout recalibrated on/off.

**Cheaper and stronger tests are missing.**
- Three-state readout to measure |2⟩ population over cycles directly.
- Re-simulating with leakage injected at measured rates. If the simulation with leakage reproduces Figs. S23 and S24 and the 7× gap, that is strong evidence, and it needs no new hardware time.

**The three outcomes need sharpening.**
- "Closes toward one" needs a pre-registered threshold with error bars. SI1000 is itself simplified, so a ratio of exactly one is not the right target.
- An improvement after adding removal units does not uniquely confirm leakage, because those units can also suppress other errors.
- A fourth outcome is missing: the gap widens because of removal-unit overhead.

**Feasibility.** The author cannot run this experiment. The note should say who could, and acknowledge that the authors' stated expectation already gestures at it.

The withdrawal clause in the third outcome is commendable falsifiability. Keep it.

## 5. What is missing

- **Prior leakage work:** McEwen et al. (2021) on leakage-induced correlated errors, Miao et al. (2023) and the DQLR work, and the literature on 1/f flux noise. Low-frequency drift is decades-old engineering noise, and linking it to Kalai needs argument, not assertion.
- **Gidney, Shutty, and Jones's predicted performance** as a benchmark for the headline result.
- **A conflict statement.** The author is scoring his own prior work. The text never says so, and it should.
- **Unused references.** Kalai, Rinott, and Shoham (2023) concerns supremacy claims and is never used. The "Stethoscopes" self-citation is never referenced in the text.
- **Leakage removal units versus DQLR.** The note uses "leakage removal units" and "DQLR" interchangeably without saying whether they are the same mechanism.

## 