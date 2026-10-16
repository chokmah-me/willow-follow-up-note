# DRAFT v2: follow-up note to the Dec 2024 Willow paper

Status: DRAFT v2, style pass 2026-10-16 on a copy of the working draft.
The prior file follow-up-note-draft.md is unchanged. Not published,
not posted, no DOI reserved. This is a standalone follow-up note to
the Dec 2024 paper. It does not amend that paper, and it does not
change any number in the Zenodo OTOC paper (v2.0, record 19651958).

Sources pinned for this draft:
- Bilar (2024), Notes on Google Willow, DOI 10.13140/RG.2.2.30911.01443,
  read in full 2026-10-16.
- Rosenfeld et al. (2026), Magic state cultivation on a
  superconducting quantum processor, Science, DOI
  10.1126/science.aee7961 (Science release of Oct 15, 2026); full text and
  supplement read as arXiv:2512.13908v1 (Dec 15, 2025).
- Google Quantum AI blog post, Oct 15, 2026, read in full.
Drafting rule carried through the text: the leakage attribution in
the cultivation paper is "likely," with signature evidence and no
ablation run. The draft keeps that word and never upgrades it.
Adversarial review 2026-10-16 (contract-certifier trace +
contract-breaker pass, files in adversarial/): BREAK 1, WEAKENS 4,
all accepted and fixed in the text (fixes F1 to F5, plus the
certifier's scope fix G1 and a voluntary softening of the F6
superlative). The adjudication record is
adversarial/ADJUDICATION.md. No original finding was rejected.
External review 2026-10-16 (Kimi K3 and Opus 5.5 via OpenRouter,
files in external-review/): both PUBLISH WITH REVISIONS. The
agreed revisions were applied at his instruction the same day:
channel accounting restored to the 2024 six (phase noise filed
under the correlated row as corroboration, abstract recounted to
one direct hit), the Layman priority line cut to the defensible
claim, variability alternative and no-ablation fact restored in
the TL;DRs, Section V rebuilt as a 2 by 2 design with cheaper
checks ahead of the settling run and five pre-scored outcomes, conflict disclosure
added, Akshay and leakage prior-art references added, and the
orders-of-magnitude arithmetic corrected. Record:
external-review/REVISIONS-APPLIED.md. Still DRAFT, not published.

---

<p class="hebrew-epigraph" dir="rtl" lang="he">אִם יִרְצֶה הַשֵּׁם</p>
<p class="hebrew-date" dir="rtl" lang="he">ה׳ בְּחֶשְׁוָן תשפ״ז</p>

# Willow, Tested Again: Magic-State Cultivation Against the 2024 Error-Channel Inventory

A follow-up to "Notes on Google Willow (2024)"
Daniyel Yaacov Bilar, Chokmah LLC, chokmah-dyb@pm.me
ORCID: [0000-0002-9040-6914](https://orcid.org/0000-0002-9040-6914)
October 16, 2026

Disclosure: the 2024 note whose inventory this note scores is my
own. The accounting below should be read with that in mind.

## Abstract

In December 2024 I published a short note on Google's Willow
surface-code paper. The note's core was an inventory of six error
channels that the simplified noise model treated thinly: gate,
readout, leakage, crosstalk, correlated, and classical chaos. In
October 2026 Google published magic-state cultivation on Willow, a
state-preparation protocol that switches a distance-3 color code
into a distance-5 surface code. This note scores that experiment
against the six channels. One channel takes a direct hit. The
authors name population leakage as the likely main cause of a
logical error rate about seven times the grafted-code simulation.
The word is theirs. Leakage signatures are in the data, leakage is
absent from the noise model and from the circuits, no ablation run
exists, and variability in physical qubit performance stays open
as a second cause. Low-frequency phase noise broke the standard
measurement method. The 2024 inventory filed that noise inside the
correlated row, so this note scores it as corroboration of that
row. Crosstalk is mentioned in passing. Gate and readout are the
experiment's baseline. Classical chaos is not tested. The
seven-fold gap is one supplement memory experiment, one grafted
configuration, up to nine cycles. Nothing in the 2024 note is
contradicted by this experiment, and most of its channels remain
untested by it.

## Layman TL;DR

Google found a cheaper way to prepare a special ingredient that
quantum computers consume in large amounts, and it works. But in
a side test of how well a stronger safe held the ingredient, it
degraded seven times faster than their simulation said it should.
The authors' likely explanation is a known leak in the hardware
that the simulation did not model and the circuit did not guard
against. Likely is their word. The leak was never a secret:
Google's own 2024 budget already carried it, and Google had built
a step to remove it. What my 2024 note flagged was narrower. The
simple model used to predict results left the leak out, and the
2026 simulation left it out again. The team keeps a second
possible cause open, and the clean test that would settle the
question has not been run.

## Quantum Computing SME TL;DR

Cultivation cuts the T-state error by a factor of 40, to a fidelity
of at least 0.9999(1), retaining 8% of attempts. The grafted-code
memory experiment in the supplement then runs about seven times
worse than its SI1000 simulation. The authors attribute the gap, as
likely, to population leakage: no leakage in the noise model, no
leakage removal units in the circuits, and two leakage signatures in
the data that the simulations do not reproduce. No run with leakage
removal added exists, so the attribution stays likely and unproven,
and the main text keeps a second possible cause open: variability
in physical qubit performance.

## Non-Hype TL;DR

This is a second experiment confirming a known weakness, not a
refutation of the cultivation result and not a vindication of every
skeptical claim made about Willow. The leakage attribution is
"likely," not demonstrated by a controlled run, and a second
possible cause, qubit performance variability, stays open in the
paper's main text. Two of the six
channels in the 2024 inventory are not addressed by this experiment
at all. The distance between a 1e-4 state error and the 1e-10 that
RSA-2048 factoring would need is unchanged.

## I. What the 2024 note claimed

The 2024 note accepted the surface-code result on its own terms:
a distance-7 logical error rate of 0.143% plus or minus 0.003% per
cycle, a logical lifetime 2.4 times the best physical qubit, an
error suppression factor Lambda of 2.14 plus or minus 0.02, and
real-time decoding at 63 microseconds. Its argument was about the
fine print. Google's error budget was about 80% incoherent errors,
about 10% coherent errors, and about 10% leakage, yet the simplified
noise model behind the headline simulations (Formula 77) assumed
independent gate errors, did not explicitly model leakage or
crosstalk, and left a 14% discrepancy between simulated and
experimental error suppression, which Google itself attributed to
excess correlations. Repetition codes had already shown a floor
near 1e-10 from correlated bursts about once per hour. The note's
conclusion was narrow: Willow did not fully resolve correlated
errors, leakage, crosstalk, or the potential for chaotic dynamics,
and the gap to fault tolerance (Lambda near 10, logical error near
1e-6, code distance near 27 on the note's estimates) remained large.

One honesty note on that inventory: none of its channels was a
secret in 2024. Google's own budget carried leakage, and Google's
team had built the removal step. The note's claim was never that
the channels were unknown. It was that the simplified model used
to turn measurements into predictions left them out, and that the
leaving-out would matter where the model was trusted.

A test of that inventory needs an experiment the inventory did not
describe, on a protocol where the omitted channels can show up in a
different place. Cultivation is such an experiment.

Three observations would damage the inventory. A later Willow
experiment whose simplified model omits the same channels, and
whose hardware agrees with that model inside the stated
uncertainties, damages the claim that the omissions decide the
result. A channel scored here as a hit must be withdrawn if a
pre-registered removal run leaves it unchanged. Section V states
that test for leakage. A channel scored as untested draws no
support from the experiment's silence.

## II. What the cultivation experiment did

Rosenfeld and a large Google team implemented magic-state
cultivation on Willow, the protocol proposed by Gidney, Shutty, and
Jones in 2024. A noisy magic state is injected into a distance-3
color code, refined by a fault-tolerant measurement of the logical
Hadamard operator with postselection, and the surviving state is
then grafted into a larger, surface-code-compatible encoding
(distance 5, 54 qubits in the grafting experiment), because the
color code that suits cultivation cannot hold the state at low idle
error on its own.

Three headline results:

1. Preparation. Adding cultivation to state preparation cuts the
   logical error probability by about a factor of 40 near the T
   state. The injection-only circuit sits at 4.4(2) times 1e-3,
   close to the physical gate error scale. The cultivated full
   circuit sits between 1 and 2 times 1e-4. The fidelity bound is
   0.9999(1), at least that in the Science abstract's wording, with
   8% of attempts retained.
2. Metrology. The team could not measure that result with standard
   logical state tomography, for reasons that are themselves a
   finding (Section III, channel 2). They built kickback tomography
   instead, which resolves an error near 1e-4 with on the order of
   1e4 measurements, against 1e8 for standard tomography.
3. Transfer. Cultivated states survive grafting into the distance-5
   code, a proof-of-principle demonstration of code switching for a
   non-Clifford state. Removing the quantum error correction cycles
   from the measurement circuit makes its error about 100 times
   worse, which shows the color code underneath cultivation is doing
   real work.

The result I score here is not in the headline list. It is in the
supplement, Section XIV: a memory experiment in the grafted code,
where the cultivated state is idled for up to nine error-correction
cycles and the logical error rate is extracted as a function of
cycle count, against state-vector simulations using the SI1000
depolarizing model at p = 2.3 times 1e-3. That gap is one
supplement figure, one grafted configuration, and at most nine
cycles. It is not a scan across distances or processors.

## III. The six channels, scored

An accounting note before the scoring, because the count matters.
The 2024 inventory has six channels: gate, readout, leakage,
crosstalk, correlated, and classical chaos. The sections below
keep that count. Leakage is section 1. Section 2 covers
low-frequency phase noise, which was not a seventh channel in
2024: it sat inside the noise-sensitivity objection and the
correlated row, and it is scored there, as corroboration. Gate and
readout are scored jointly in section 5 because the experiment
treats both as its baseline. Nonlinear errors, a 2024 objection
rather than a channel, are scored beside classical chaos in
section 6.

### 1. Leakage: signature present, attributed as likely

The experimental logical error rate in the grafted-code memory
experiment is about seven times higher than the simulations predict.
The authors state, in substance, that population leakage is likely
the main source of the disagreement. Two signatures support the
attribution, and both are absent from the simulations, which do not
include leakage at all:

- Detection-event likelihood rises slowly over time in the
  experimental data (their Fig. S23), as long-lived population
  outside the computational subspace would produce.
- Detector covariance shows strong time correlations that propagate
  across the qubit grid (their Fig. S24), which the authors describe
  as the characteristic leakage pattern.

The circuits did not contain the leakage removal units described in
Google's earlier work. The earlier work the supplement points to
is Google's 2023 surface-code scaling paper, whose removal step
is the DQLR step the 2024 note described: the two papers use
different words for the same line of mechanism. The supplement also names a path in: the
grafting circuit redefines which qubits are measured mid-circuit,
the readout control parameters were not optimized for that new
configuration, and frequency collisions involving the |2> state may
have followed, with leakage after them. The main text, on the
earlier grafting figure, keeps one alternative open alongside
leakage: variability in physical qubit performance.

Calibration of this claim matters. "Likely" is the authors' word
and it is the right one. There is no run with leakage removal units
added and everything else held fixed. Until that run exists, the
seven-fold gap has a named, signature-supported, unproven cause.

Leakage is also not a new discovery, in 2024 or now. It has a
literature of its own in topological codes, from Suchara, Cross,
and Gambetta (2015) through McEwen and others (2021) and
Battistel, Varbanov, and Terhal (2021). The 2024 note's claim was
about the model, not about priority, and this note keeps it that
way.

For the 2024 inventory, the point is structural. In 2024 leakage was
a tenth of the error budget, handled by a dedicated removal step
(DQLR), and absent from the simplified model. In 2026 the
grafting work omitted the channel from its simulations and omitted
the removal step from its circuits, and the channel is the
explanation the authors give when simulation and hardware part
company by a factor of seven. The channel did not go away when the protocol
changed. It moved to the storage step, which is exactly where a
consumable resource like a magic state has to live.

### 2. Low-frequency phase noise (the 2024 correlated row): corroborated

Early in the project, logical state tomography of cultivated states
returned a non-physical norm, a state that cannot exist. The team
attributes this to low-frequency phase noise, and their simulations
of coherent phase noise reproduce the effect. The supplement names
the candidate sources: slow qubit frequency drift, residual magnetic
fields from control lines, and Stark shifts on the qubits through
microwave crosstalk. The cultivation circuit is unusually exposed
to this noise because its data qubits spend long stretches idling in
an entangled state, accumulating coherent phase.

Without echo pulses to filter this noise, the team's own comparison
suggests their performance was dominated by it. They built kickback
tomography so that the measurement is taken along the prepared
state's own axis in a single circuit, avoiding the inconsistent-axis
problem the noise creates. With echoing in place,
their simulations bound the remaining detuning contribution near
1e-5 in infidelity, below the measured error, and suggest the
final performance is limited by gate error and decoherence, not
quasi-static detunings.

Score this as a corroboration of the 2024 noise-sensitivity row,
with a mitigation attached. It is not a second channel hit, and
the abstract does not count it as one. The 2024
note, following Kalai [6] and the questions in Kalai, Rinott, and
Shoham [7], treated non-stationary and coherent noise as a
standing objection to simplified models. In the cultivation work
this noise did not merely shift a number. It invalidated the
standard measurement protocol. The team's blog account describes
months of diagnosis before the new method was built. The point
that matters here is narrower and checkable: in this case the
objection changed the measurement method itself, not only a
reported number, and the finding comes from inside the team.

### 3. Crosstalk: touched, not measured

Crosstalk appears in the cultivation paper in one place only, as a
candidate source of the fixed detunings above, through microwave
crosstalk producing Stark shifts. There is no separate crosstalk
measurement, no scaling study, and no comparison against the
widespread nonlocal crosstalk the 2024 note flagged on the 72-qubit
processor. This channel is neither confirmed nor cleared. It is
mentioned, in passing, inside another channel's story.

### 4. Correlated errors: signature present, leakage-mediated

The detector covariance result in the leakage analysis is a
time-correlation result, and the correlations are the kind that
break independent-error decoding assumptions. But the authors tie
them to leakage propagation, and the experiment reports nothing
about the distinct 2024 claim, correlated bursts setting a 1e-10
floor in repetition codes. A reader who scores this channel as
independently confirmed would be double-counting the leakage
evidence. I score it as present but not independently tested.

### 5. Gate and readout errors: baseline, no new test

Two of the six channels are scored here together, because the
experiment treats both as its baseline. The cultivation result is
framed against gate error from the start:
the 40-fold improvement is measured from an injection-only error
close to the physical gate error rate. Nothing in the experiment
reopens the 2024 questions about the gate error budget. Readout
enters only through the leakage path in channel 1, unoptimized
readout parameters in a redefined configuration. The forward
projection in the paper also keeps the 2024 gap in view: because
the cultivated infidelity scales as p cubed, halving the processor
noise strength would bring the bound near 2 times 1e-5. That is
real progress toward the 1e-6 to 1e-8 range some simulations and
optimization work needs. It is about five orders of magnitude
short of the roughly 1e-10 that factoring an RSA-2048 key
requires, and six orders from the value actually measured, a
number the cultivation paper itself states.

### 6. Classical chaos, with the nonlinear-errors objection: not tested

Nothing in the cultivation paper addresses Boerner and others on
classical chaos in transmon systems, or Hirota on nonlinear error
scaling. The p cubed scaling the authors verify is the protocol's
designed fault-tolerance scaling, not a test of nonlinear noise.
These two rows of the 2024 inventory stand exactly where they
stood, untested by this experiment in either direction.

## IV. Updated standing of the 2024 challenge table

The 2024 note closed with a challenge table. Scored against the
cultivation experiment, it moves in one place:

| Challenge (source) | 2024 standing | After cultivation (2026) |
|---|---|---|
| Noise sensitivity (Kalai) | Partially | Partially, now on two experiments: memory (2024) and state preparation plus storage (2026). The leakage and phase-noise findings above are the new evidence. |
| Nonlinear errors (Hirota) | Indirectly | Indirectly, unchanged. Not tested here. |
| Reachability deficits (Akshay et al.) | Indirectly | Indirectly, with a sharper number: 2 times 1e-5 projected at half the current noise, against 1e-10 for RSA-2048 factoring. |
| Classical chaos (Boerner et al.) | Partially | Partially, unchanged. Not tested here. |
| After echo and kickback (cultivation team) | Not in the 2024 table | Point for the simplified model on that measurement: residual detuning bound near 1e-5, below the measured error. Does not clear the correlated row. |

Rows move only when the new experiment speaks to that objection.
Unchanged means this experiment did not test the row. No row here
moves to Solved. A partially addressed
problem with a second documentation, from a different kind of
experiment, is still partially addressed. The annotation is about
the weight of evidence, not its direction.

## V. What would settle the leakage claim

Only the cultivation team can run this experiment. This note
cannot. What a note can do is state, in advance, what each outcome
would mean, so the result cannot be read two ways after the fact.

Two cheaper checks sit ahead of that experiment, and neither needs new hardware
time. Three-state readout on the grafted circuit measures the |2>
population directly, cycle by cycle, instead of inferring it from
detector signatures. And the same simulations, rerun with leakage
injected at measured rates, should reproduce both signatures
(Figs. S23 and S24) and the size of the gap if the attribution is
right. Either check could sharpen or damage the claim before any
rerun.

The settling experiment is a 2 by 2. Run the grafted-code memory
experiment in four arms: leakage removal units added or not,
crossed with readout control parameters re-optimized for the
redefined configuration or left as they were, all against the
same SI1000 baseline at p = 2.3 times 1e-3. The crossing is not
decoration. The supplement's own entry path for leakage runs
through the unoptimized readout, so a rerun with only one fix that
improves could be crediting the wrong cause. The removal arm
cannot be a pure change either: removal units add operations and
their own error, and the design has to say so. Success should be
fixed in advance: the gap counts as closed when the measured
ratio to simulation is consistent with one within the stated
uncertainties, not when it merely shrinks.

The outcomes, scored in advance:

- The gap closes in the removal arms and not in the readout-only
  arm. The leakage attribution is confirmed in the only way that
  counts, by removal, and the 2024 channel graduates from likely
  to demonstrated in this protocol.
- The gap closes in the readout-only arm as well, or mainly. The
  cause sits in the readout path itself, or splits between the
  two fixes, and the scorecard splits the channel.
- The gap narrows in part in the removal arms. Leakage is one
  cause among several, the residual belongs to the alternatives
  the paper already names (qubit performance variability,
  calibration in the redefined configuration), and the scorecard
  splits the channel.
- The gap does not move in any arm. The attribution fails, the
  signatures in Figs. S23 and S24 need another explanation, and
  this note's channel 1 score must be withdrawn.
- The gap widens in the removal arms. Removal overhead dominates
  at this scale. The test is inconclusive, not a refutation, and
  should be reported as one.

The authors say they expect improvement from leakage removal,
better calibration, and larger distances. The follow-up literature
should be scored on which of these outcomes is reported, and on
whether the rerun is reported at all.

## VI. Conclusion

The 2024 note argued that the fine print of the Willow result was
its error channels: the ones the simplified model omitted were the
ones that would decide how far the hardware scales. The cultivation
paper is good news for quantum computing and, read closely, it is
also a second data set for that argument. A protocol that prepares
states forty times cleaner than injection then stores them seven
times worse than its own simulation, for what the authors call the
likely cause, an omitted channel and an omitted removal step, with
the alternative still open, is the 2024 fine print appearing in a
new place. Keep the inventory, score each new experiment against
it, and insist on the removal experiment that turns "likely" into
a measurement.

## AI Use Statement

This note was prepared with AI assistance, directed by the author
at every stage. Muse (Meta) agents located and read the primary
sources, cross-checked every number and attribution in the draft
against them, and drafted the text at the author's instruction.
The draft then went through two internal adversarial passes
(a spec-faithful claims trace and an independent adversarial
review), and two external critical evaluations commissioned by
the author through OpenRouter, from Moonshot Kimi K3 and
Anthropic Claude Opus 5.5. Every finding from those passes was
adjudicated before any revision was applied, and the review files
are preserved with the draft. The author selected all sources,
made every publish and revise decision, and takes responsibility
for the claims, the scoring, and the conclusions. AI output was
treated as draft throughout, and nothing in this note rests on a
claim that was not checked against a primary source. No AI system
is listed as a co-author.

Affiliation: Chokmah LLC, Norwich, VT. Contact: chokmah-dyb@pm.me.

## References

[1] D. Y. Bilar, "Notes on Google Willow (2024)," preprint, 2024. doi: 10.13140/RG.2.2.30911.01443. [Online]. Available: https://www.researchgate.net/publication/387576664_Notes_on_Google_Willow_2024_aka_Quantum_Error_Correction_Below_the_Surface_Code_Threshold

[2] E. Rosenfeld, C. Gidney, et al., Google Quantum AI and Collaborators, "Magic state cultivation on a superconducting quantum processor," *Science*, 2026. doi: 10.1126/science.aee7961. Full text and supplement as arXiv:2512.13908, 2025. [Online]. Available: https://doi.org/10.1126/science.aee7961

[3] C. Gidney, N. Shutty, and C. Jones, "Magic state cultivation: growing T states as cheap as CNOT gates," *arXiv preprint*, arXiv:2409.17595, 2024. [Online]. Available: https://arxiv.org/abs/2409.17595

[4] Google Quantum AI and Collaborators, "Quantum error correction below the surface code threshold," *Nature*, vol. 638, pp. 920-926, 2024. doi: 10.1038/s41586-024-08449-y. [Online]. Available: https://doi.org/10.1038/s41586-024-08449-y

[5] Google Quantum AI, "Bringing the magic: Google breaks open a bottleneck in quantum computing," blog post, Oct. 15, 2026. [Online]. Available: https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/

[6] G. Kalai, "The Quantum Computer Puzzle," *arXiv preprint*, arXiv:1605.00992, 2016. [Online]. Available: https://arxiv.org/abs/1605.00992

[7] G. Kalai, Y. Rinott, and T. Shoham, "Questions and concerns about Google's quantum supremacy claim," *arXiv preprint*, arXiv:2305.01064, 2023. [Online]. Available: https://arxiv.org/abs/2305.01064

[8] O. Hirota, "Introduction to semi-classical analysis for digital errors of qubit in quantum processor," *Entropy*, vol. 23, no. 12, p. 1577, 2021. [Online]. Available: https://doi.org/10.3390/e23121577

[9] S.-D. Boerner et al., "Classical chaos in quantum computers," *arXiv preprint*, arXiv:2304.14435, 2023. [Online]. Available: https://arxiv.org/abs/2304.14435

[10] V. Akshay, H. Philathong, M. E. S. Morales, and J. D. Biamonte, "Reachability deficits in quantum approximate optimization," *Physical Review Letters*, vol. 124, p. 090504, 2020. [Online]. Available: https://doi.org/10.1103/PhysRevLett.124.090504

[11] M. Suchara, A. W. Cross, and J. M. Gambetta, "Leakage suppression in the toric code," *Quantum Information and Computation*, vol. 15, pp. 997-1016, 2015. [Online]. Available: https://doi.org/10.26421/QIC15.11-12-8

[12] M. McEwen et al., "Removing leakage-induced correlated errors in superconducting quantum error correction," *Nature Communications*, vol. 12, p. 1761, 2021. [Online]. Available: https://doi.org/10.1038/s41467-021-21982-y

[13] F. Battistel, B. Varbanov, and B. Terhal, "Hardware-efficient leakage-reduction scheme for quantum error correction with superconducting transmon qubits," *PRX Quantum*, vol. 2, p. 030314, 2021. [Online]. Available: https://doi.org/10.1103/PRXQuantum.2.030314

[14] Google Quantum AI and Collaborators, "Suppressing quantum errors by scaling a surface code logical qubit," *Nature*, vol. 614, pp. 676-681, 2023. [Online]. Available: https://doi.org/10.1038/s41586-022-05434-1
