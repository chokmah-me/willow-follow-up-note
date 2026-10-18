# Scoring the rise leg against the 2023 paper's published signature

Date: 2026-10-17. Question: the joint test in
`section-v-simulation-design.md` asks one (generation, lifetime)
pair to match three observables of the cultivation experiment,
but the supplement publishes no detector-level data and no
uncertainties for Figs. S23 and S24, so the rise and covariance
legs cannot be scored against the 2026 curves from outside. Can
the rise leg be scored against the 2023 paper's published rise
signature instead? Answer: yes, with the leg reworded. What it
buys and what it costs are both stated below. Sources are the
local copies in `sources/` (2023 paper: arXiv:2207.06431;
cultivation supplement: arXiv:2512.13908v1).

## The 2023 numbers, as published

The 2023 paper states its rise in the main text, in numbers:

- Average detection probabilities show a relative rise of 12%
  for distance 5 and 8% for distance 3 over 25 cycles, with a
  characteristic risetime of roughly 5 cycles. The text
  attributes the rise to data qubits leaking into
  non-computational states.
- Their Pauli+ simulation of the same experiment gives a 7%
  rise over 25 rounds at distance 5, and the paper calls the
  prediction accurate.

The cultivation supplement, by contrast, gives Fig. S23 a
caption ("a slow increase in detection fractions for some
detectors over time... suggestive of long-lived population
excitations") and no magnitude and no risetime anywhere in the
text.

## What the substitution buys

- A scoreable rise leg. Run the hybrid simulator
  (`simulator/`) on a 2023-style memory experiment at
  literature rates: the leakage arm either lands in the
  published envelope (rise between their model's 7% and the
  experiment's 12%, risetime of order 5 cycles) or it does not.
  Distance 3 against their 8% is checkable at current scale.
- A tolerance with provenance. Google's own Pauli+ came in at
  7% against the experiment's 12%, a factor of about 1.7 low,
  and the paper calls that accurate. That published gap is a
  defensible tolerance for the rise leg, which answers the
  "no uncertainties published" objection (internal SME major 6)
  for this leg without inventing one.
- The target is the team's own fingerprint. They named this
  rise as leakage's signature in their own paper. Calibrating
  against it is calibrating against their reading.
- Partial help on covariance: the 2023 supplement's Fig. S24
  publishes the correlation structure and its reading (broad
  time-correlated features are leakage; their model captured
  most of them). A structure-level comparison becomes
  possible. A numeric matrix distance does not; the matrix is
  a figure, not data.

## What it costs

- The rise leg changes kind. It stops being a fit to the
  cultivation experiment and becomes a calibration of the
  instrument on an earlier one: different processor
  generation, a plain memory circuit instead of a grafted
  code. If the cultivation rise is driven by the redefined
  readout path (the design's Arm 3), a 2023-shaped target
  cannot certify that shape. Section V's wording must change
  where the claim stands: "one rate pair reproduces all three
  signatures jointly" becomes "the rate pair reproduces the
  2026 ratio, on an instrument calibrated against the team's
  published 2023 leakage fingerprint." The grafted-circuit rise
  the sweep produces then counts as a prediction, not a fit.
- A device-transfer assumption becomes explicit. It was
  already inside the design: the generation and lifetime band
  comes from the same earlier device generation (McEwen 2021,
  Miao 2023). The substitution makes visible an assumption the
  sweep was already carrying.
- One caveat that cuts both ways. The 2023 correlation
  analysis found two data qubits whose leakage was stronger
  than the team's model, a device-specific hot spot a
  uniform-rate model missed. That is precedent for tolerance,
  and a warning that a uniform generation grid has the same
  blind spot.
- A mismatch in kind stays. The 2023 number is an average over
  detectors; S23 reports an increase "for some detectors."
  Scoring our average against theirs is clean, and it says
  nothing about the per-detector pattern, which remains
  unscoreable from outside.

## Net

The joint test survives with two legs scored (the 2026 ratio;
the rise, as instrument calibration) and one leg demoted to a
structural consistency check (covariance). Status: analysis
only. The design file is unchanged, Section V of the draft is
unchanged, and no run has been made under this substitution.
Adopting it is the author's call.
