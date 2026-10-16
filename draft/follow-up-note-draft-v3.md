<p class="hebrew-epigraph" dir="rtl" lang="he">אִם יִרְצֶה הַשֵּׁם</p>
<p class="hebrew-date" dir="rtl" lang="he">ה׳ בְּחֶשְׁוָן תשפ״ז</p>

# Willow, Tested Again: Magic-State Cultivation Against the 2024 Error-Channel Inventory

A follow-up to "Notes on Google Willow (2024)"
Daniyel Yaacov Bilar, Chokmah LLC, chokmah-dyb@pm.me
ORCID: [0000-0002-9040-6914](https://orcid.org/0000-0002-9040-6914)
License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
October 16, 2026
No DOI reserved.

## Abstract

In December 2024 I published a short note on Google's Willow
surface-code paper [1]. The note's core was an inventory of six
error channels that the simplified noise model treated thinly:
gate, readout, leakage, crosstalk, correlated, and classical
chaos. In October 2026 Google published magic-state cultivation
on Willow [2], a state-preparation protocol that switches a
distance-3 color code into a distance-5 surface code. This note
scores that experiment against the six channels. Leakage is a
likely hit (attributed, not ablated). The authors name population
leakage as the likely main cause of a logical error rate about
seven times the grafted-code simulation in preprint v1 of the
supplement [2]. Leakage signatures are in that data, leakage is
absent from the noise model and from the circuits, no ablation
run exists, and variability in physical qubit performance stays
open as a second cause. Standard tomography failed under
low-frequency phase noise. Echo plus kickback tomography restored
the measurement, with a residual detuning bound near 1e-5 in the
same preprint. Crosstalk is mentioned. Gate and readout are the
experiment's baseline. Classical chaos is untested. The
seven-fold gap is one supplement memory experiment, one grafted
configuration, up to nine cycles, in preprint v1. Nothing in the
2024 note is contradicted by this experiment. The inventory is
not confirmed by it.

## Layman TL;DR

Google's 2026 cultivation experiment on Willow prepares a useful
kind of quantum state more cleanly than injection. In a follow-up
memory run in the grafted code, described in preprint v1 of the
supplement [2], that state failed about seven times more often
than their simulation predicted. The authors' likely explanation
is a known leak in the hardware, population leaving the
computational subspace. They show two signatures of that leak.
They did not run the removal step that would test it, and they
leave a second cause open: some qubits may simply have performed
worse than others. This note scores that result against a 2024
inventory of six error channels. Leakage is a likely hit
(attributed, not ablated). The other five channels are mentioned,
present but not independent, baseline, or untested. The gap is
one configuration, up to nine cycles.

## I. What the 2024 note claimed

The 2024 note [1] accepted the surface-code result on its own
terms: a distance-7 logical error rate of 0.143% plus or minus
0.003% per cycle, a logical lifetime 2.4 times the best physical
qubit, an error suppression factor Lambda of 2.14 plus or minus
0.02, and real-time decoding at 63 microseconds. Google's error
budget was about 80% incoherent errors, about 10% coherent
errors, and about 10% leakage, yet the simplified noise model
behind the headline simulations (Formula 77) assumed independent
gate errors and did not explicitly model leakage or crosstalk.
A 14% discrepancy between simulated and experimental error
suppression was attributed by Google to excess correlations.
Repetition codes had already shown a floor near 1e-10 from
correlated bursts about once per hour. The note's conclusion:
Willow did not fully resolve correlated errors, leakage,
crosstalk, or the potential for chaotic dynamics, and the gap to
fault tolerance (Lambda near 10, logical error near 1e-6, code
distance near 27 on the note's estimates) remained large.

None of those channels was a secret in 2024. Google's own budget
carried leakage, and Google's team had built a removal step. The
2024 claim was that the simplified model used to turn measurements
into predictions left them out, and that the leaving-out would
matter where the model was trusted.

The six channels, the 2024 claim for each, and what would count:

| Channel | 2024 claim [1] | Counts for the claim | Counts against the claim |
|---|---|---|---|
| Leakage | About 10% of the error budget, omitted from Formula 77, handled by a dedicated removal step | A gap versus a model that omits leakage, leakage signatures in the data, no leakage removal units in the circuit | No gap, a gap fully explained by variability, or a removal run that leaves the gap |
| Crosstalk | Omitted from the simplified model | A measured crosstalk contribution to the result | Agreement with a model that still omits it |
| Correlated | Excess correlations and a burst floor near 1e-10; not solved by Willow | An independent correlated-error measurement that the model misses | Hardware matching the omitting model on a test of that floor |
| Gate | Inside the simplified model; the 2024 baseline | A new test of gate error beyond that baseline | This experiment using the same baseline, with no new test |
| Readout | Inside the simplified model; the 2024 baseline | A new test of readout error beyond that baseline | This experiment using the same baseline, with no new test |
| Classical chaos | Boerner-type dynamics in transmons, untested | A chaos diagnostic on this protocol | Untested, which is silence, not support |

What in the cultivation data would have counted against the
inventory: no gap between the grafted-code memory experiment and
its omitting simulation, or a gap the authors fully explained by
qubit-performance variability. What the v1 supplement reports is
a gap of about seven, leakage named as the likely main cause, and
variability left open. The inventory stays open on those terms.

Hirota's nonlinear-error scaling [7] was an objection in the 2024
note, not a seventh channel. It is not scored as a channel here.

## II. What the cultivation experiment did

Rosenfeld and a large Google team implemented magic-state
cultivation on Willow [2], the protocol proposed by Gidney,
Shutty, and Jones [3]. Article claims below that appear in the
Science abstract [2] are labeled as such. Claims that I take from
the supplement are from arXiv:2512.13908v1 (Dec 15, 2025). I did
not page-diff that file against the published Science supplement.

A noisy magic state is injected into a distance-3 color code,
refined by a fault-tolerant measurement of the logical Hadamard
operator with postselection, and the surviving state is then
grafted into a larger, surface-code-compatible encoding
(distance 5, 54 qubits in the grafting experiment), because the
color code that suits cultivation cannot hold the state at low
idle error on its own.

Three headline results:

1. Preparation. The Science abstract [2] says cultivation reduces
   the error by a factor of 40, with a state fidelity of at least
   0.9999(1) (retaining 8% of attempts). The v1 preprint gives
   injection-only error 4.4(2)e-3 and cultivated full-circuit
   error between 1e-4 and 2e-4, a ratio of about 22 to 44.
   "About 40" is the paper's headline, at the low-error end of
   that range. The v1 abstract omits the words "at least".
2. Metrology. The team could not measure that result with standard
   logical state tomography. They built kickback tomography
   instead, which in v1 resolves an error near 1e-4 with on the
   order of 1e4 measurements, against 1e8 for standard tomography.
3. Transfer. Cultivated states survive grafting into the
   distance-5 code. Removing the quantum error correction cycles
   from the measurement circuit makes its error about 100 times
   worse in v1, which shows the color code underneath cultivation
   is doing real work.

The result I score is in the v1 supplement, Section XIV [2]: a
memory experiment in the grafted code, where the cultivated state
is idled for up to nine error-correction cycles and the logical
error rate is extracted as a function of cycle count, against
state-vector simulations using the SI1000 depolarizing model at
p = 2.3e-3. That gap is one supplement figure, one grafted
configuration, and at most nine cycles. It is not a scan across
distances or processors.

The cultivation paper's introduction [2] states that magic-state
infidelities of about 1e-10 are required for factoring an
RSA-2048 key, citing Gidney [13], and that infidelities between
about 1e-6 and 1e-8 are needed for some quantum simulations and
optimization. Because cultivated infidelity scales as p cubed,
halving the processor noise strength would bring a bound near
2e-5. That is progress toward the 1e-6 to 1e-8 band. It is about
five orders of magnitude short of the 1e-10 figure the paper
cites, and six orders from the value actually measured. This
experiment is a small-distance demonstration. The Gidney-Shutty-
Jones protocol [3] reaches its low error rates at larger fault
distance. The comparison is one small-distance result against
the protocol's end target.

## III. The six channels, scored

Verdicts used below, and only these:

- likely hit (attributed, not ablated)
- mentioned
- present but not independent
- baseline
- untested

Each of the six 2024 channels is scored once. Low-frequency phase
noise is a measurement story after those six. It is not a seventh
channel.

### 1. Leakage: likely hit (attributed, not ablated)

The experimental logical error rate in the grafted-code memory
experiment is about seven times higher than the simulations
predict (v1 supplement, Section XIV [2]). The authors state that
population leakage is likely the main source of the disagreement.
Two signatures support the attribution, and both are absent from
the simulations, which do not include leakage:

- Detection-event likelihood rises slowly over time in the
  experimental data (Fig. S23 [2]), as long-lived population
  outside the computational subspace would produce.
- Detector covariance shows strong time correlations that
  propagate across the qubit grid (Fig. S24 [2]), which the
  authors describe as the characteristic leakage pattern.

The circuits did not contain the leakage removal units described
in previous work. The v1 supplement points to Google's 2023
surface-code scaling paper [12] (bibliography number 49 in
that supplement). This note
uses the supplement's phrase, leakage removal units, for that
citation. The 2024 Willow paper [4] named a DQLR step. I do not
treat those two names as the same mechanism here.

The v1 supplement names a path in, specific to this grafted
configuration: the grafting circuit redefines which qubits are
measured mid-circuit, the readout control parameters were not
optimized for that new configuration, and frequency collisions
involving the |2> state may have followed, with leakage after
them. The main text, on the earlier grafting figure, keeps one
alternative open alongside leakage: variability in physical qubit
performance [2].

"Likely" is the authors' word. There is no run with leakage
removal units added and everything else held fixed. Until that
run exists, the seven-fold gap has a named, signature-supported,
unproven cause.

Leakage in topological codes has a literature of its own, from
Suchara, Cross, and Gambetta [9] through McEwen and others [10]
and Battistel, Varbanov, and Terhal [11]. The 2024 note's claim
was about the model, not about priority.

Leakage reappears at the storage step in this grafted
configuration.

### 2. Crosstalk: mentioned

Crosstalk appears in the v1 supplement [2] as a candidate source
of fixed detunings, through microwave crosstalk producing Stark
shifts. There is no separate crosstalk measurement, no scaling
study, and no comparison against the nonlocal crosstalk the 2024
note [1] flagged on the 72-qubit processor.

### 3. Correlated errors: present but not independent

The detector covariance in Fig. S24 [2] is a time-correlation
result, and the correlations are the kind that break
independent-error decoding assumptions. The authors tie them to
leakage propagation. The experiment reports nothing about the
2024 claim of correlated bursts setting a 1e-10 floor in
repetition codes. Scoring this channel as independently confirmed
would double-count the leakage evidence.

### 4. Gate: baseline

The cultivation result is framed against gate error from the
start: the 40-fold improvement is measured from an injection-only
error close to the physical gate error rate. Nothing in the
experiment reopens the 2024 questions about the gate error
budget.

### 5. Readout: baseline

Readout enters the leakage path in channel 1, as unoptimized
readout parameters in a redefined configuration. That is part of
the leakage score. It is not a new, independent test of the 2024
readout baseline.

### 6. Classical chaos: untested

Nothing in the cultivation paper addresses Boerner and others [8]
on classical chaos in transmon systems. The p cubed scaling the
authors verify is the protocol's designed fault-tolerance
scaling, not a test of chaotic dynamics. Untested in either
direction.

### Measurement story: low-frequency phase noise (not a channel)

Early in the project, logical state tomography of cultivated
states returned a non-physical norm. The v1 supplement [2]
attributes this to low-frequency phase noise, and simulations of
coherent phase noise reproduce the effect. Candidate sources
named there: slow qubit frequency drift, residual magnetic fields
from control lines, and Stark shifts on the qubits through
microwave crosstalk. The cultivation circuit is exposed because
its data qubits spend long stretches idling in an entangled
state.

Without echo pulses to filter this noise, the team's comparison
in v1 suggests their performance was dominated by it. They built
kickback tomography so that the measurement is taken along the
prepared state's own axis in a single circuit. With echoing in
place, their simulations bound the remaining |T> infidelity from
quasi-static detunings near 1e-5, below the measured error, and
suggest the final performance is limited by gate error and
decoherence [2]. That residual is a point for the simplified
model on that measurement. It is not a score of the 2024
correlated channel. The 2024 correlated claim was the burst
floor. Low-frequency phase noise is a different object. This
note does not widen that channel to include it.

Kalai [5], and Kalai, Rinott, and Shoham [6], object that
time-independent Pauli models omit coherent and non-stationary
noise. The tomography failure is an instance of coherent
low-frequency noise breaking a measurement that those models
treat as routine. It does not test Kalai's claims about the
supremacy experiment.

## IV. Updated standing of the 2024 objections

Table 1. Standing of the 2024 objections [1] after the
cultivation experiment [2]. "Partially" means the 2024 note
already treated the objection as open, with some evidence.
"Indirectly" means the 2024 note treated it as relevant by
analogy. "Unchanged" means this experiment did not test the
objection. "Evidence added" is yes when the cultivation paper
or its v1 supplement supplies a new measurement that bears on
the row, including a point for the simplified model.

| Objection (source) | 2024 standing | After cultivation (2026) | Evidence added |
|---|---|---|---|
| Noise sensitivity (Kalai [5], [6]) | Partially | Partially. The tomography failure is coherent low-frequency noise. It is not a test of the 2024 burst floor. | yes |
| Nonlinear errors (Hirota [7]) | Indirectly | Indirectly, unchanged. | no |
| Classical chaos (Boerner et al. [8]) | Partially | Partially, unchanged. | no |
| After echo and kickback (cultivation team [2]) | Not in the 2024 table | Residual detuning bound near 1e-5 (v1), below the measured error. Point for the simplified model on that measurement. | yes |

Rows move only when the new experiment speaks to that objection.
Unchanged means this experiment did not test the row. No row
here moves to Solved. A partially addressed problem with a
second documentation, from a different kind of experiment, is
still partially addressed.

## V. What would settle the leakage claim

Only the cultivation team can run this experiment. This note
cannot. What a note can do is state, in advance, what each
outcome would mean, so the result cannot be read two ways after
the fact.

Two cheaper checks sit ahead of that experiment, and neither
needs new hardware time. Three-state readout on the grafted
circuit measures the |2> population directly, cycle by cycle,
instead of inferring it from detector signatures. And the same
simulations, rerun with leakage injected at measured rates,
should reproduce both signatures (Figs. S23 and S24 [2]) and the
size of the gap if the attribution is right. Either check could
sharpen or damage the claim before any rerun.

The settling experiment is a 2 by 2. Run the grafted-code memory
experiment in four arms: leakage removal units added or not,
crossed with readout control parameters re-optimized for the
redefined configuration or left as they were, all against the
same SI1000 baseline at p = 2.3e-3. The v1 supplement's own
entry path for leakage runs through the unoptimized readout, so
a rerun with only one fix that improves could credit the wrong
cause. The removal arm cannot be a pure change either: leakage
removal units add operations and their own error, and the design
has to say so. Success should be fixed in advance: the gap
counts as closed when the measured ratio to simulation is
consistent with one within the stated uncertainties, not when it
merely shrinks.

The outcomes, scored in advance:

- The gap closes in the removal arms and not in the
  readout-only arm. The leakage attribution is confirmed by
  removal, and the 2024 channel graduates from likely to
  demonstrated in this protocol.
- The gap closes in the readout-only arm as well, or mainly.
  The cause sits in the readout path itself, or splits between
  the two fixes, and the inventory splits the channel.
- The gap narrows in part in the removal arms. Leakage is one
  cause among several, the residual belongs to the alternatives
  the paper already names (qubit performance variability,
  calibration in the redefined configuration), and the inventory
  splits the channel.
- The gap does not move in any arm. The attribution fails, the
  signatures in Figs. S23 and S24 [2] need another explanation,
  and this note's leakage score must be withdrawn.
- The gap widens in the removal arms. Removal overhead dominates
  at this scale. The test is inconclusive, and should be
  reported as one.

The authors say they expect improvement from leakage removal,
better calibration, and larger distances. The follow-up
literature should be scored on which of these outcomes is
reported, and on whether the rerun is reported at all.

## Limitations

I am scoring my own 2024 inventory. The memory-experiment numbers,
figure pins, and "likely" wording come from arXiv:2512.13908v1,
not from a page-diffed Science supplement. I have no raw data and
I did not rerun the simulations. The score of leakage rests on
one grafted-code memory figure, one configuration, up to nine
cycles. Section V is a design. It is not a result of this note.

## VI. Conclusion

The 2024 note [1] argued that the channels the simplified model
omitted would decide how far the hardware scales. The cultivation
paper [2] is good news for quantum computing. Read against that
inventory, it supplies one likely hit on leakage, attributed and
not ablated, with variability still open, in this grafted
configuration, and leaves the other
five channels mentioned, present but not independent, baseline,
or untested. The factor-of-40 headline is state error against
injection. The factor-of-seven gap is memory logical error
against SI1000 at one p, in preprint v1. Those are different
measurements. Keep the inventory, score each new experiment
against it, and insist on the removal experiment that turns
"likely" into a measurement.

## Availability

The scoring worksheet, source pins, and review files are in the
working repository https://github.com/chokmah-me/willow-follow-up-note
A Zenodo DOI will be added at mint. None is reserved yet.

## AI Utilization Statement

This note was prepared with AI assistance, directed by the author
at every stage. Muse (Meta) agents (model version not recorded)
located and read the primary sources, cross-checked numbers and
attributions in the draft against them, and drafted the text at
the author's instruction. The draft then went through two
internal adversarial passes (a spec-faithful claims trace and an
independent adversarial review), and two external critical
evaluations commissioned by the author through OpenRouter, from
Moonshot Kimi K3 and Anthropic Claude Opus 5.5. Every finding
from those passes was adjudicated before any revision was
applied. The review files are in the repository named above and
will be part of the Zenodo deposit when minted. They have no
public URL yet. The author selected all sources, made every
publish and revise decision, and takes responsibility for the
claims, the scoring, and the conclusions. AI output was treated
as draft throughout. Claims scored here were checked against
arXiv:2512.13908v1 and the Science abstract [2]. The published
Science supplement was not page-diffed. No AI system is listed
as a co-author.

Affiliation: Chokmah LLC, Norwich, VT. Contact: chokmah-dyb@pm.me.

## References

[1] D. Y. Bilar, "Notes on Google Willow (2024)," preprint, 2024. doi: 10.13140/RG.2.2.30911.01443. [Online]. Available: https://www.researchgate.net/publication/387576664_Notes_on_Google_Willow_2024_aka_Quantum_Error_Correction_Below_the_Surface_Code_Threshold

[2] E. Rosenfeld, C. Gidney, et al., Google Quantum AI and Collaborators, "Magic state cultivation on a superconducting quantum processor," *Science*, release of Oct. 15, 2026 (no volume or pages yet). doi: 10.1126/science.aee7961. Supplement claims in this note are from arXiv:2512.13908v1, Dec. 15, 2025. [Online]. Available: https://doi.org/10.1126/science.aee7961

[3] C. Gidney, N. Shutty, and C. Jones, "Magic state cultivation: growing T states as cheap as CNOT gates," *arXiv preprint*, arXiv:2409.17595, 2024. [Online]. Available: https://arxiv.org/abs/2409.17595

[4] Google Quantum AI and Collaborators, "Quantum error correction below the surface code threshold," *Nature*, vol. 638, pp. 920-926, 2024. doi: 10.1038/s41586-024-08449-y. [Online]. Available: https://doi.org/10.1038/s41586-024-08449-y

[5] G. Kalai, "The Quantum Computer Puzzle," *arXiv preprint*, arXiv:1605.00992, 2016. [Online]. Available: https://arxiv.org/abs/1605.00992

[6] G. Kalai, Y. Rinott, and T. Shoham, "Questions and concerns about Google's quantum supremacy claim," *arXiv preprint*, arXiv:2305.01064, 2023. [Online]. Available: https://arxiv.org/abs/2305.01064

[7] O. Hirota, "Introduction to semi-classical analysis for digital errors of qubit in quantum processor," *Entropy*, vol. 23, no. 12, p. 1577, 2021. [Online]. Available: https://doi.org/10.3390/e23121577

[8] S.-D. Boerner et al., "Classical chaos in quantum computers," *arXiv preprint*, arXiv:2304.14435, 2023. [Online]. Available: https://arxiv.org/abs/2304.14435

[9] M. Suchara, A. W. Cross, and J. M. Gambetta, "Leakage suppression in the toric code," *Quantum Information and Computation*, vol. 15, pp. 997-1016, 2015. [Online]. Available: https://doi.org/10.26421/QIC15.11-12-8

[10] M. McEwen et al., "Removing leakage-induced correlated errors in superconducting quantum error correction," *Nature Communications*, vol. 12, p. 1761, 2021. [Online]. Available: https://doi.org/10.1038/s41467-021-21982-y

[11] F. Battistel, B. Varbanov, and B. Terhal, "Hardware-efficient leakage-reduction scheme for quantum error correction with superconducting transmon qubits," *PRX Quantum*, vol. 2, p. 030314, 2021. [Online]. Available: https://doi.org/10.1103/PRXQuantum.2.030314

[12] Google Quantum AI and Collaborators, "Suppressing quantum errors by scaling a surface code logical qubit," *Nature*, vol. 614, pp. 676-681, 2023. [Online]. Available: https://doi.org/10.1038/s41586-022-05434-1

[13] C. Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits," *arXiv preprint*, arXiv:2505.15917, 2025. [Online]. Available: https://arxiv.org/abs/2505.15917
