# Held for a future Willow version: cultivation leakage note

Status: HELD, drafted 2026-10-16 at his tap. Not applied to the Zenodo
paper v2.0 (record 19651958, DOI 10.5281/zenodo.19651958). No number,
claim, or result in v2.0 changes, and this news does not mint a version
on its own. If a future version is minted for other reasons, drop the
entry below in as a dated postscript, or as a short addition after the
Limitations section and before the Conclusion.

This note is the revised assessment. It replaces the first assessment
delivered 2026-10-16 at 09:44 EDT, which called the contact with the
cultivation news general only. At his pointer to the Dec 2024 paper,
the contact was rechecked and is specific: the channel is leakage,
named in Dec 2024, not a generic point about missing noise.

## The note (paste-ready)

**Leakage, again outside the model.** In October 2026 Google reported
magic-state cultivation on Willow, in Science: T-states prepared at
99.99% logical fidelity, with preparation errors cut about 40-fold
against uncultivated preparation. The preparation result is not the
point of contact with this work. The storage test is. After the
cultivated states were grafted from a distance-3 color code into a
distance-5 surface code (54 qubits in the grafting experiment) and held
through further error-correction cycles, the observed logical error
rate came out about seven times higher than the simulations predicted.
The authors identify leakage as the likely main cause. Their
simulations did not include leakage, and the experimental circuits
carried no dedicated leakage-removal operations.

That is one of the channels inventoried in my December 2024 notes on
the Willow surface-code paper (DOI 10.13140/RG.2.2.30911.01443).
Leakage was not explicitly modeled in Google's simplified noise model
(Formula 77). In the 2024 experiments it was mitigated by data-qubit
leakage removal and still accounted for about 10% of the error budget,
against about 80% incoherent errors and about 10% coherent errors.
The 2026 storage miss repeats the structure, in a new protocol and a
new code pair: a channel left out of the simulation, and left without
a removal step in the circuit, accounts for most of the gap between
simulation and hardware. It changes no number in the OTOC analysis
above and no row in the Kalai scorecards. It is an independent
confirmation, from a different Willow experiment, that omitted error
channels are not a bookkeeping detail. They are where the simulation
and the device part company.

## Sources and verification

- Bilar, D. Y. (2024). Notes on Google Willow (2024), also titled
  Notes on Willow and NISQ Issues, Dec 31, 2024, 8 pages.
  DOI 10.13140/RG.2.2.30911.01443. Read in full via ResearchGate on
  2026-10-16. No local copy is held on the agent VM.
  Points used here, all from that text: the error-channel table
  comparing Google's simplified model (Formula 77) with Kalai et al.,
  Hirota (2021), and Boerner et al. across gate, readout, leakage,
  crosstalk, correlated, and classical-chaos channels; leakage not
  explicitly modeled in the simplified model, mitigated with
  data-qubit leakage removal; error budget in the appendix,
  incoherent about 80%, coherent about 10%, leakage about 10%;
  correlated bursts setting a 1e-10 error floor about once per hour;
  a 14% simulated against experimental discrepancy in the error
  suppression factor, attributed to excess correlations.
- Bilar, D. Y. (2026). How 'Stethoscopes' Unmasked Correlated Noise
  in Quantum Processors, v2.0, April 19, 2026. Zenodo record 19651958,
  DOI 10.5281/zenodo.19651958, file dyb2025c-OTOCStethoscope.pdf,
  CC-BY 4.0. Read in full on 2026-10-16 from the Zenodo record.
  This is the paper the held note would join in a future version.
- The Quantum Insider, "Google Demonstrates Method to Cut Errors in
  Quantum Computing's 'Magic States'," Oct 16, 2026.
  https://thequantuminsider.com/2026/10/16/google-demonstrates-method-to-cut-errors-in-quantum-computings-magic-states/
  Read in full on 2026-10-16. It reports the Science paper and the
  Google Quantum AI blog post by Rosenfeld and Gidney, and it is the
  source for the cultivation figures used here: 99.99% logical
  T-state fidelity, about 40-fold preparation error reduction,
  distance-3 color code to distance-5 surface code grafting, 54 qubits
  in the grafting experiment, storage error about seven times the
  simulation, leakage as the likely main cause, no leakage in the
  simulations, and no dedicated leakage-removal operations in the
  circuits. The Feed unit c12febfb ("Willow cut magic-state errors
  40-fold") matches this article.

## Primary-source check (done 2026-10-16, replaces the earlier caveat)

The four items flagged in the first draft were rechecked against the
primary sources, not the trade report: the Science paper (Science,
First Release Oct 15, 2026, DOI 10.1126/science.aee7961, abstract
checked on science.org), its full text and supplement as the arXiv
version (arXiv:2512.13908v1, Dec 15, 2025, Rosenfeld et al., read in
full on 2026-10-16, including supplement Sec. XIV and Figs. S22 to
S24), and the Google Quantum AI blog post of Oct 15, 2026.
One version note: the Science abstract says fidelity "at least
0.9999(1)" where the arXiv abstract says "0.9999(1)"; nothing else in
the claims used here differs between the two.

All four items check out, with two precision fixes to the first
draft:

1. The seven times figure is the logical error rate of the grafted
   code memory experiment (supplement Sec. XIV, Fig. S22): experiment
   against state-vector simulations run with the SI1000 depolarizing
   model at p = 2.3e-3. It is not a ratio for the headline cultivation
   result, which stands at a 40-fold error reduction and 8% retention.
2. The leakage attribution is stated as likely, not proven. The
   supplement's words in substance: it is likely that the main source
   of the disagreement is population leakage. Support is two
   signatures, a slow rise in detection-event likelihood over time
   seen in experiment and not in simulation (Fig. S23), and
   time-correlated detector covariance that propagates across the
   grid, seen in experiment and not in simulation (Fig. S24). There
   is no controlled test with leakage removal added. The main text
   (Fig. 4 discussion) also keeps a second cause open: variability
   in physical qubit performance.
3. Simulations did not include leakage. Confirmed in both places:
   the main text says population leakage is not included in their
   noise model, and the supplement says the simulation results do not
   include leakage approximations and do not treat leakage.
4. The circuits had no leakage removal. Confirmed, in stronger form
   than the trade report: the supplement says the circuits did not
   contain the leakage removal units described in previous work, and
   names the mechanism, readout control parameters not optimized for
   the redefined configuration, leading to possible frequency
   collisions involving |2> states and subsequent leakage. The
   authors expect improvement from added leakage removal units,
   better calibration, and larger distances.

Residual caveat: because the attribution is "likely" with signature
evidence and no ablation run, any use of this note must keep the word
likely attached to the leakage claim. Do not upgrade it to proven.

## Assessment behind it (revised, 2026-10-16)

First assessment, 09:44 EDT: no claim in the Zenodo paper moves,
contact general only, a simulation omitting a whole channel and then
undershooting. That verdict on the Zenodo paper's own numbers stands.
Its account of the contact was too weak.

Revised verdict, after reading the Dec 2024 paper in full at his
pointer: the Dec 2024 error-channel inventory gets a direct and
specific hit. Leakage was named there as an unmodeled channel with a
measured share of the error budget and a named mitigation. The 2026
cultivation storage test then missed its simulation by about seven
times for, on the reported account, that same channel, omitted from
both the simulation and the circuit's removal steps. No version bump
follows from this on its own, because neither Willow paper's numbers,
methods, or scorecards change. The value of the note is as a dated
corroboration entry if a future version is minted for other reasons.

## Follow-up assessment (2026-10-16, primary sources checked)

Question put: does the cultivation result warrant a follow-up on the
Dec 2024 paper?

Answer: yes as a short, standalone follow-up note. No as a revision
of the 2024 paper, and no as a version bump of the Zenodo v2.0 paper.
Nothing in either paper is wrong or needs correction. What the new
experiment supplies is test evidence against the 2024 channel
inventory, channel by channel, from a different kind of experiment
(state preparation and code switching, not quantum memory). That is
new analysis material, not a correction.

Channel-by-channel test record, from the primary text:

- Leakage: TESTED, likely hit. Seven times logical error rate gap in
  the grafted-code memory experiment; two leakage signatures in the
  data that the no-leakage simulations do not show; no leakage
  removal units in the circuits; a named path in (readout parameters
  not optimized for the redefined lattice, possible |2> frequency
  collisions). Confidence ceiling: likely, no ablation run.
- Low-frequency phase noise and coherent noise: TESTED, hit, and
  acted on by the authors. Standard logical state tomography produced
  a non-physical norm, attributed to low-frequency phase noise;
  sources named in the supplement include slow qubit frequency drift,
  residual fields from control lines, and Stark shifts through
  microwave crosstalk. Without echoing, performance was dominated by
  this noise. The team replaced the measurement method itself
  (kickback tomography) because of it. With echoing, simulations put
  the remaining detuning limit near 1e-5 infidelity, below the
  measured result, so this channel was mitigated, not left standing.
- Crosstalk: TOUCHED, not measured separately. It appears as one
  named possible source of the fixed detunings above. No separate
  crosstalk measurement is reported.
- Correlated errors: SIGNATURE PRESENT, leakage-mediated. The
  detector covariance result is a time-correlation result, and the
  authors tie it to leakage propagation. It is not an independent
  test of the 2024 correlated-burst claim (the 1e-10 floor), which
  the cultivation experiment does not address.
- Gate and readout errors: BASELINE, no new test of the 2024 claims.
  The 40-fold result is measured against physical gate error scale
  (injection-only logical error 4.4(2)e-3, similar to physical gate
  errors), and the projected gains still assume the processor noise
  strength improves (infidelity scaling as p cubed; halving p gives
  a projected bound near 2e-5, against the 1e-10 that RSA-2048
  factoring would need).
- Classical chaos and nonlinear error scaling (Hirota, Boerner):
  NOT TESTED. Nothing in the cultivation paper addresses them.

What a follow-up note would have that a postscript does not: the
full six-channel scorecard above, the statement of what would settle
the leakage claim (the same grafted memory experiment rerun with
leakage removal units added, against the same SI1000 baseline), and
the updated standing of the 2024 challenge table (noise sensitivity
still Partially, now with a second experiment behind it; the other
rows unchanged). Scope it as a short note in the 2024 paper's own
form, dated, citing Science DOI 10.1126/science.aee7961 and
arXiv:2512.13908. Do not scope it as an amendment to the 2024 text
and do not let it claim the leakage attribution as proven.
