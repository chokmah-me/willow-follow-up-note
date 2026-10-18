<p class="hebrew-epigraph" dir="rtl" lang="he">אִם יִרְצֶה הַשֵּׁם</p>
<p class="hebrew-date" dir="rtl" lang="he">ז׳ חֶשְׁוָן תשפ״ז</p>

# Willow, Tested Again: Magic-State Cultivation Against the 2024 Error-Channel Inventory

A follow-up to "Notes on Google Willow (2024)"
The 2024 note scored here is the author's.
Daniyel Yaacov Bilar, Chokmah LLC, chokmah-dyb@pm.me
ORCID: [0000-0002-9040-6914](https://orcid.org/0000-0002-9040-6914)
License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
October 18, 2026
No DOI reserved.

## Abstract

The 2024 note on Google's Willow surface-code paper inventoried
six error channels. Four were omitted or treated thinly by the
simplified noise model: leakage, crosstalk, correlated errors,
and classical chaos. Gate and readout sat inside that model as
the baseline. In October 2026 Google published magic-state
cultivation on Willow, switching a distance-3 color code into a
distance-5 surface code. This note scores that experiment against
the six channels. Supplement claims are from arXiv preprint v1.
Leakage is a likely hit (attributed, not ablated). In the
supplement's grafted-code memory experiment, the authors name
population leakage as the likely main cause of a logical error
rate about seven times the simulation. Signatures are in the data,
leakage is absent from the model and the circuits, and no removal
run exists. That section's other candidates are unoptimized
readout parameters and |2> frequency collisions after the grafting
circuit redefines which qubits are measured. Variability in
physical qubit performance is left open on an earlier grafting
figure, next to an injection-only tomography mismatch. The residual
detuning bound near 1e-5 is a simulated bound under assumed plus
or minus 200 kHz quasi-static detunings, with no depolarizing
noise. Crosstalk is mentioned. Correlated errors are present in
the detector data and are not scored on their own. Gate and readout
remain the baseline. Classical chaos is untested. The seven-fold
gap is one configuration and at most nine cycles. It is weak
evidence on its own. The leakage score rests on the signatures.
The 2024 inventory is not confirmed.

## Layman TL;DR

Google's 2026 cultivation experiment on Willow prepares a useful
quantum state more cleanly than injection. In the grafted-code
memory experiment in preprint v1 of the supplement [2], that
state failed about seven times more often than the simulation.
The authors' likely explanation is population leakage, leaving
the computational subspace. They show two signatures of that
leak, and they did not run the removal step that would test it.
The same supplement section names two other candidates for that
gap: readout parameters that were not optimized for the grafted
circuit, and frequency collisions involving the |2> state.
Variability in physical qubit performance is left open on an
earlier grafting figure in the main text, beside a tomography
mismatch, and is not named in the section that reports the
seven-fold gap. This note scores the result against a 2024
inventory of six error channels: four omitted or thin (leakage,
crosstalk, correlated errors, classical chaos) and two baseline
channels (gate and readout). Leakage is a likely hit (attributed,
not ablated). The gap is one configuration, up to nine cycles,
and it is weak evidence on its own. The leakage score rests on
the signatures.

## I. What the 2024 note claimed

The 2024 note [1] accepted the surface-code result on its own
terms: a distance-7 logical error rate of 0.143% plus or minus
0.003% per cycle, a logical lifetime 2.4 times the best physical
qubit, an error suppression factor Lambda of 2.14 plus or minus
0.02, and real-time decoding at 63 microseconds. Google's error
budget was about 80% incoherent errors, about 10% coherent
errors, and about 10% leakage, yet the simplified noise model
behind the headline simulations, labeled Formula 77 in the
2024 note [1] and matching the Pauli simulations in [4] that
use the measured component error rates (Fig. 1b), assumed
independent gate errors and did not explicitly model leakage
or crosstalk.
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

The six channels, the 2024 claim for each, and what would count.
Four were omitted or treated thinly: leakage, crosstalk,
correlated errors, and classical chaos. Gate and readout are
the two baseline channels inside the simplified model.

Table 1. Six 2024 channels: 2024 claim, and what in the
cultivation data would count for or against it.

| Channel | 2024 claim [1] | Counts for the claim | Counts against the claim |
|---|---|---|---|
| Leakage | About 10% of the error budget, omitted from the 2024 note's Formula 77 (Pauli simulations in [4]), handled by a dedicated removal step | A gap versus a model that omits leakage, leakage signatures in the data, no leakage removal units in the circuit | No gap, a gap explained by the unoptimized readout or by \|2> collisions in the redefined configuration, or a removal run that leaves the gap |
| Crosstalk | Omitted from the simplified model | A measured crosstalk contribution to the result | Agreement with a model that still omits it |
| Correlated | Excess correlations and a burst floor near 1e-10; not solved by Willow | An independent correlated-error measurement that the model misses | Hardware matching the omitting model on a test of that floor |
| Gate | Inside the simplified model; the 2024 baseline | A new test of gate error beyond that baseline | This experiment using the same baseline, with no new test |
| Readout | Inside the simplified model; the 2024 baseline | A new test of readout error beyond that baseline | This experiment using the same baseline, with no new test |
| Classical chaos | Boerner-type dynamics in transmons, untested | A chaos diagnostic on this protocol | Untested, which is silence, not support |

What would have counted against the leakage row is no gap, a
gap explained by the unoptimized readout or by the |2>
collisions, or a removal run that leaves the gap. A
hardware-versus-SI1000 gap in a first grafted-code memory run
is close to guaranteed, so the gap is weak evidence on its own.
The v1 supplement reports a gap of about seven, names leakage
as the likely main cause, and shows the Fig. S23 and Fig. S24
signatures, with no removal units in the circuit. The score
rests on those signatures and on the missing removal units.

Hirota's nonlinear-error scaling [7] was an objection in the
2024 note. This note scores the six channels only.

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

1. Preparation. The v1 main text [2] calls the cultivated result
   an upper bound of 1(1) x 10^-4 error, after discarding
   instances with detected errors in logical state preparation
   and measurement, with about 8% of the data retained. The
   Science abstract, retrieved on Oct. 18, 2026, says cultivation
   reduces the error by a factor of 40, with a state fidelity of
   at least 0.9999(1) (retaining 8% of attempts). The v1 preprint
   gives injection-only error 4.4(2)e-3 and cultivated
   full-circuit error between 1e-4 and 2e-4, a ratio of about 22
   to 44. "About 40" is the paper's headline, at the low-error
   end of that range. The v1 abstract states the fidelity as
   0.9999(1) and does not use "at least".
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
grafted-code memory experiment. The authors call it a start on
studying the cost of error-correction cycles. The cultivated
state is idled for up to nine cycles, and the logical error rate
is extracted against state-vector simulations in qevol, using the
SI1000 depolarizing model at p = 2.3e-3. Section XIV carries that
p over from Fig. 4. The main text uses p = 3.0e-3 for Fig. 2 and
p = 2.3e-3 for Figs. 3 and 4, and attributes the change to
shifted qubit frequencies and different control calibrations. It
also reports logical-error variation of about 1e-4 over an hour.
The seven-fold gap is the experimental rate divided by the
simulation at that fixed p = 2.3e-3. Fig. S22 places the label
"Exp. fit, LER = 5.3%" on the experimental logical-error panel
(b) and "Exp. fit, LER = 0.8%" on the simulation panel (e). The
caption assigns (a-c) to experiment, (d-f) to simulation, and
(b, e) to logical error rate versus cycle count. 5.3 / 0.8 is
about 6.6, in line with "about seven times." I read "Exp. fit"
as an exponential fit. The grafted code is not matchable, because
it mixes color-code and surface-code stabilizers, and the main
text says the grafting data were decoded with Tesseract [2].
Section XIV does not say the simulation curve was decoded with
Tesseract. Those simulations are state-vector runs. A decoder
mismatch, or a model mismatch, remains a candidate cause this
comparison does not close. The gap is one supplement figure, one
grafted configuration, and at most nine cycles.

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
noise is a measurement story after those six channels.

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

The v1 supplement names a path in, specific to this grafted-code
memory experiment: the grafting circuit redefines which qubits
are measured mid-circuit, the readout control parameters were not
optimized for that new configuration, and frequency collisions
involving the |2> state may have followed, with leakage after
them. The main text, on the earlier grafting figure, keeps one
alternative open alongside leakage: variability in physical qubit
performance [2]. That alternative sits next to the Fig. 4
injection-only tomography mismatch. Section XIV, where the
seven-fold gap is reported, does not name it. Leakage shows up
again in this grafted-code memory experiment.

"Likely" is the authors' word. There is no run with leakage
removal units added and everything else held fixed. Until that
run exists, the seven-fold gap has a named, signature-supported,
unproven cause.

Leakage in topological codes has a literature of its own, from
Suchara, Cross, and Gambetta [9] through McEwen and others [10]
and Battistel, Varbanov, and Terhal [11]. The 2024 note's claim
was about the model, not about priority.

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
start: the improvement the paper headlines as about 40-fold
(22 to 44 on the preprint v1 endpoints, Section II) is measured
from an injection-only error close to the physical gate error
rate. Nothing in the
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
place, a further simulation bounds the remaining |T> infidelity
from quasi-static detunings near 1e-5 [2]. That figure is a
simulated bound under assumed plus or minus 200 kHz quasi-static
detunings, run with no depolarizing noise. The supplement's
Fig. S14c still shows non-physical norms for some echoed
detuning draws. The 2024 correlated claim was the burst floor.
Low-frequency phase noise is a different object. This note does
not widen that channel to include it.

Kalai [5], and Kalai, Rinott, and Shoham [6], object that
time-independent Pauli models omit coherent and non-stationary
noise. The tomography failure is an instance of coherent
low-frequency noise breaking a measurement that those models
treat as routine. It does not test Kalai's claims about the
supremacy experiment.

## IV. Updated standing of the 2024 objections

Table 2. Standing after the cultivation experiment [2].
The first three rows are 2024 objections [1]. The last row
is a 2026 measurement, not a 2024 objection. The 2024 note's
challenge table, as read from the ResearchGate text of [1] on
Oct. 18, 2026, puts "Partially" under a header fragment
"Challenge Addressed by Willow?" The noise-sensitivity grade
there is Partially, with the nearby words "Significant
progress, but error floor remains." I could not recover a clean
column layout from that file, so this table copies the grades
Partially and Indirectly and does not redefine them.
"Unchanged" means this experiment did not test the objection.
"Evidence added" is yes only when the cultivation paper tests
that 2024 objection.

| Objection (source) | 2024 grade in [1] | After cultivation (2026) | Evidence added |
|---|---|---|---|
| Noise sensitivity (Kalai [5], [6]) | Partially | Partially. The tomography failure is coherent low-frequency noise. It does not test Kalai's claims, and it does not test the 2024 burst floor. | no |
| Nonlinear errors (Hirota [7]) | Indirectly | Indirectly, unchanged. | no |
| Classical chaos (Boerner et al. [8]) | Partially | Partially, unchanged. | no |
| After echo and kickback (cultivation team [2]) | Not in the 2024 table | Simulated bound near 1e-5 under assumed plus or minus 200 kHz quasi-static detunings, with no depolarizing noise (v1). Fig. S14c still shows non-physical norms for some echoed draws. | yes |

Rows move only when the new experiment tests that objection.
No row here moves to Solved. The last row's "yes" records a
new measurement. It is not a 2024 objection.

## V. What would settle the leakage claim

Only the cultivation team can run this experiment. This note
cannot. What a note can do is state, in advance, what each
outcome would mean, so the result cannot be read two ways after
the fact.

Two cheaper checks sit ahead of that experiment.
Three-state readout on the grafted circuit uses the existing
Willow processor and needs the team's runtime. It measures
the |2> population directly, cycle by cycle, instead of
inferring it from detector signatures. The second check needs
no device. It would rerun the simulations with leakage injected
at measured rates. The v1 supplement cites Marshall and Kafri,
"Incoherent approximation of leakage in quantum error
correction," Phys. Rev. Applied 23, 054025 (2025), as its
references 38 and 43 [14]. I have not read that paper. A check
from outside would use that approximation or duplicate it. The
cultivation team can run their own implementation directly. If
the attribution is right, the rerun should reproduce the size of
the 2026 gap. The rise target is the 2023 paper's average
detection probability [12], and the grafted-circuit rise is a
prediction, not a fit to Fig. S23 [2]. In the main text of [12],
after the Fig. 2 averages, the average detection probability
shows a relative rise of 12% at distance 5 and 8% at distance 3
over 25 cycles, with a typical characteristic risetime of roughly
5 cycles. The Pauli+ simulation increases that average by 7% over
25 rounds at distance 5. Fig. 2 of [12] plots detection
probability per stabilizer, and the darker lines are the average
over stabilizers of the same weight. The 12%, 8%, and 7% figures
are rises in those averages, not per-detector traces. Fig. S23
of [2] reports a slow increase for some detectors, not an array
average. A match to the 2023 averages would not certify the
shape of those traces. The 2023 target is also a different
processor generation and a plain memory circuit. If the
cultivation rise is driven by the redefined readout path, a
2023-shaped average cannot certify that shape.

The Zenodo record cited in the v1 data-availability line,
10.5281/zenodo.17872003, publishes measurements.csv and
detection_events.csv for Figs. 2, 3, and 4. Fig. 4 is present at
N = 2 and N = 3 (injection, cultivation, and one injection
simulation). The record has no directory for the N = 9 run behind
Figs. S22, S23, and S24. Detector covariance in Fig. S24 [2] stays
a structural check (time-correlated features that spread across
the grid). The S23 rise and the S24 covariance cannot be scored
as a numeric match from that record.

The settling experiment is a 2 by 2. Run the grafted-code memory
experiment in four arms: leakage removal units added or not,
crossed with readout control parameters re-optimized for the
redefined configuration or left as they were. The seven-fold gap
in Section XIV is the ratio to the SI1000 simulation at
p = 2.3e-3, the value used for Figs. 3 and 4 and carried into
Section XIV from Fig. 4, not the p = 3.0e-3 of Fig. 2. A rerun
that re-fits p inside each grafted arm could shrink that ratio
by construction. Freeze p from a non-grafted control on the same
day, for example the kickback-tomography circuit of Fig. 3, and
use that one value for every arm. Do not fit a separate p to the
grafted data. The v1 supplement's own entry path for leakage
runs through the unoptimized readout, so a rerun with only one
fix that improves could credit the wrong cause. The removal arm
cannot be a pure change either: leakage removal units add
operations and their own error, and the design has to say so.
Success should be fixed in advance: the gap counts as closed
when the measured ratio to that fixed-p simulation is consistent
with one within the stated uncertainties, and not when the ratio
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
  cause among several. The residual belongs to the alternatives
  Section XIV names for this configuration: unoptimized readout
  calibration, and frequency collisions involving the |2> state
  after the mid-circuit redefinition of measured qubits. The
  inventory splits the channel.
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

## VI. Limitations

I am scoring my own 2024 inventory. The memory-experiment numbers,
figure pins, and "likely" wording come from arXiv:2512.13908v1,
not from a page-diffed Science supplement. The v1
data-availability line points to Zenodo record
10.5281/zenodo.17872003. Opened on Oct. 18, 2026, that record
holds detector-level files for Figs. 2, 3, and 4, including
Fig. 4 at N = 2 and N = 3, and it has no N = 9 directory for
Figs. S22 to S24. I did not rerun the paper's simulations.
Section V states a design. The leakage score rests on one
grafted-code memory figure, one configuration, and at most nine
cycles. The rise target in the simulation check is the 2023
average detection-probability rise [12]. It is an instrument
target, and it is not a fit to Fig. S23 [2].

## VII. Conclusion

The 2024 note [1] argued that the channels the simplified model
omitted would decide how far the hardware scales. Read against
that inventory, the cultivation paper [2] supplies one likely
hit on leakage, attributed and not ablated, in this grafted
configuration. Variability in physical qubit performance stays
open on the earlier grafting figure. Section XIV names readout
calibration and |2> collisions as the other candidates for the
seven-fold gap. The other five channels are mentioned, present
but not independent, baseline, or untested. The factor-of-40
headline is state error against injection. The factor-of-seven
gap is memory logical error against SI1000 at p = 2.3e-3, the
value carried into Section XIV from Fig. 4. Those are different
measurements. The gap is weak evidence on its own. The leakage
score rests on the signatures and on the missing removal units.
Keep the inventory, score each new experiment against it, and
insist on the removal experiment that turns "likely" into a
measurement.

## Availability

The scoring worksheet, source pins, and review files are in
https://github.com/chokmah-me/willow-follow-up-note
That repository is private. It stays private until a DOI is
minted. No DOI is reserved.

## AI Utilization Statement

This note was prepared with AI assistance, directed by the author
at every stage. Muse (Meta) agents (model version not recorded)
located and read the primary sources, cross-checked numbers and
attributions in the draft against them, and drafted the text at
the author's instruction. Later edits used Grok under the
author's direction. A leakage simulator in the private repository
was written with OpenAI GPT-6 Astra through OpenRouter from the
author's briefs. This note reports no output from that simulator.
The draft went through internal adversarial passes and external
critical evaluations commissioned by the author. The author
selected all sources, made every publish and revise decision, and
takes responsibility for the claims, the scoring, and the
conclusions. AI output was treated as draft throughout. Claims
scored here were checked against arXiv:2512.13908v1 and the
Science abstract [2]. The published Science supplement was not
page-diffed. Review files are in the private repository named
above and will be part of the Zenodo deposit when a DOI is
minted. No AI system is listed as a co-author.

Affiliation: Chokmah LLC, Norwich, VT. Contact: chokmah-dyb@pm.me.

## References

[1] D. Y. Bilar, "Notes on Google Willow (2024)," preprint, 2024. doi: 10.13140/RG.2.2.30911.01443. Accessed: Oct. 18, 2026. [Online]. Available: https://www.researchgate.net/publication/387576664_Notes_on_Google_Willow_2024_aka_Quantum_Error_Correction_Below_the_Surface_Code_Threshold

[2] E. Rosenfeld, C. Gidney, et al., Google Quantum AI and Collaborators, "Magic state cultivation on a superconducting quantum processor," *Science*, First Release, Oct. 15, 2026 (no volume or pages yet). doi: 10.1126/science.aee7961. Accessed: Oct. 18, 2026. Supplement claims in this note are from arXiv:2512.13908v1, Dec. 15, 2025. [Online]. Available: https://doi.org/10.1126/science.aee7961

[3] C. Gidney, N. Shutty, and C. Jones, "Magic state cultivation: growing T states as cheap as CNOT gates," *arXiv preprint*, arXiv:2409.17595, 2024. Accessed: Oct. 18, 2026. [Online]. Available: https://arxiv.org/abs/2409.17595

[4] Google Quantum AI and Collaborators, "Quantum error correction below the surface code threshold," *Nature*, vol. 638, pp. 920-926, 2024. doi: 10.1038/s41586-024-08449-y. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.1038/s41586-024-08449-y

[5] G. Kalai, "The Quantum Computer Puzzle," *arXiv preprint*, arXiv:1605.00992, 2016. Accessed: Oct. 18, 2026. [Online]. Available: https://arxiv.org/abs/1605.00992

[6] G. Kalai, Y. Rinott, and T. Shoham, "Questions and concerns about Google's quantum supremacy claim," *arXiv preprint*, arXiv:2305.01064, 2023. Accessed: Oct. 18, 2026. [Online]. Available: https://arxiv.org/abs/2305.01064

[7] O. Hirota, "Introduction to semi-classical analysis for digital errors of qubit in quantum processor," *Entropy*, vol. 23, no. 12, p. 1577, 2021. doi: 10.3390/e23121577. Link check: Oct. 18, 2026 (doi.org returned 403). [Online]. Available: https://doi.org/10.3390/e23121577

[8] S.-D. Boerner et al., "Classical chaos in quantum computers," *arXiv preprint*, arXiv:2304.14435, 2023. Accessed: Oct. 18, 2026. [Online]. Available: https://arxiv.org/abs/2304.14435

[9] M. Suchara, A. W. Cross, and J. M. Gambetta, "Leakage suppression in the toric code," *Quantum Information and Computation*, vol. 15, pp. 997-1016, 2015. doi: 10.26421/QIC15.11-12-8. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.26421/QIC15.11-12-8

[10] M. McEwen et al., "Removing leakage-induced correlated errors in superconducting quantum error correction," *Nature Communications*, vol. 12, p. 1761, 2021. doi: 10.1038/s41467-021-21982-y. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.1038/s41467-021-21982-y

[11] F. Battistel, B. Varbanov, and B. Terhal, "Hardware-efficient leakage-reduction scheme for quantum error correction with superconducting transmon qubits," *PRX Quantum*, vol. 2, p. 030314, 2021. doi: 10.1103/PRXQuantum.2.030314. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.1103/PRXQuantum.2.030314

[12] Google Quantum AI and Collaborators, "Suppressing quantum errors by scaling a surface code logical qubit," *Nature*, vol. 614, pp. 676-681, 2023. doi: 10.1038/s41586-022-05434-1. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.1038/s41586-022-05434-1

[13] C. Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits," *arXiv preprint*, arXiv:2505.15917, 2025. Accessed: Oct. 18, 2026. [Online]. Available: https://arxiv.org/abs/2505.15917

[14] J. Marshall and D. Kafri, "Incoherent approximation of leakage in quantum error correction," *Physical Review Applied*, vol. 23, p. 054025, 2025. doi: 10.1103/PhysRevApplied.23.054025. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.1103/PhysRevApplied.23.054025
