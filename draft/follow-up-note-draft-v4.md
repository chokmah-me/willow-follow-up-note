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

This note scores Google's 2026 magic-state cultivation experiment
on Willow against the six error channels inventoried in the
author's 2024 note, and fixes in advance the experiment that would
settle the one channel it hits. Four channels were omitted or
treated thinly by the simplified noise model behind Google's 2024
predictions: leakage, crosstalk, correlated errors, and classical
chaos. Gate and readout sat inside that model as the baseline. The
cultivation experiment grafts a magic state from a distance-3 color
code into a distance-5 code that mixes color-code and surface-code
stabilizers. Supplement claims are from arXiv preprint v1. Leakage
is a likely hit (attributed, not ablated). In the supplement's
grafted-code memory experiment, the logical error rate is about
seven times a depolarizing simulation that omits leakage. The
authors name leakage as the likely main cause, trace its entry to
readout parameters not optimized for a redefined measurement
layout, and show two leakage signatures in the detector data. The
circuits had no leakage removal units, and no removal run exists.
Variability in physical qubit performance, named beside leakage on
an earlier grafting figure, stays open. A hit means a model that
omits the channel mispredicts the hardware by a stated factor, with
the experimenters' own attribution. Crosstalk is
mentioned. Correlated errors are present but not independent of the
leakage evidence. Gate and readout remain baseline. Classical chaos
is untested. The settling experiment crosses leakage removal with
readout re-optimization, requires three-state readout in every arm,
and fixes its pass margin before the run.

## Layman TL;DR

Google's 2026 experiment prepares a useful quantum state more
cleanly than before. When that state was held for a few rounds of
error correction, it failed about seven times more often than a
simulation without leakage predicted. Leakage means the qubit
escaping to a third energy level. The authors think that is the
main cause and show two traces of it, but they did not run the fix
that would prove it. Uneven quality across qubits is still a
possible cause. This note counts that as a likely hit for one
of six problems a 2024 note flagged, and says which experiment
would settle it.

## I. What the 2024 note claimed

The 2024 note [1] accepted the surface-code result on its own
terms: a distance-7 logical error rate of 0.143% plus or minus
0.003% per cycle, a logical lifetime 2.4 times the best physical
qubit, an error suppression factor Lambda of 2.14 plus or minus
0.02, and real-time decoding at 63 microseconds [4]. The 2024 note
read Google's error budget as about 80% incoherent errors, about
10% coherent errors, and about 10% leakage [1]. The simplified
noise model behind the headline simulations, labeled Formula 77 in
the 2024 note [1] and matching the Pauli simulations in [4] that
use the measured component error rates (Fig. 1b), assumed
independent gate errors and did not explicitly model leakage or
crosstalk. The 2024 note reported a 14% discrepancy between
simulated and experimental error suppression, which Google
attributed to excess correlations [1]. Repetition codes had already
shown a logical error floor near 1e-10 from correlated bursts about
once per hour [4]. The note's conclusion: Willow did not fully
resolve correlated errors, leakage, crosstalk, or the potential for
chaotic dynamics, and the gap to fault tolerance (Lambda near 10,
logical error near 1e-6, code distance near 27 on the note's
estimates) remained large.

None of those channels was a secret in 2024. Google's own budget
carried leakage, and Google's team had built a removal step,
data qubit leakage removal (DQLR) [15]. The 2024 claim was that
the simplified model used to turn measurements into predictions
left them out, and that the leaving-out would matter where the
model was trusted.

Table 1 lists the six channels, the 2024 claim for each, what in
the cultivation data would count for or against it, and the 2026
verdict from Section III.

Table 1. The six 2024 channels: 2024 claim, evidence that would
count for or against it in the cultivation data, and the verdict
this note assigns.

| Channel | 2024 claim [1] | Counts for the claim | Counts against the claim | 2026 verdict |
|---|---|---|---|---|
| Leakage | About 10% of the error budget, omitted from the 2024 note's Formula 77 (Pauli simulations in [4]), handled by a dedicated removal step | Leakage signatures in the detector data that the leakage-free simulation lacks, alongside a gap to that simulation | No gap; a gap explained without leakage (readout errors that never populate \|2>, qubit variability, decoder or model mismatch); or a removal run that leaves the gap | likely hit (attributed, not ablated) |
| Crosstalk | Omitted from the simplified model | A measured crosstalk contribution to the result | Agreement with a model that still omits it | mentioned |
| Correlated | Excess correlations and a burst floor near 1e-10; not solved by Willow | An independent correlated-error measurement that the model misses | Hardware matching the omitting model on a test of that floor | present but not independent |
| Gate | Inside the simplified model; the 2024 baseline | A new test of gate error beyond that baseline | This experiment using the same baseline, with no new test | baseline |
| Readout | Inside the simplified model; the 2024 baseline | A new test of readout error beyond that baseline | This experiment using the same baseline, with no new test | baseline |
| Classical chaos | Boerner-type dynamics in transmons, untested | A chaos diagnostic on this protocol | Untested, which is silence, not support | untested |

The absence of leakage removal units is a precondition for the
leakage row, not evidence for it: it lets leakage accumulate, and
it would let the other causes act just as well. A gap between
hardware and a depolarizing simulation in a first grafted-code
memory run is also expected on general grounds, so the gap alone
cannot discriminate. The leakage score rests on the two detector
signatures (Figs. S23 and S24 of [2]).

Hirota's nonlinear-error scaling [7] was an objection in the 2024
note. This note scores the six channels only.

## II. What the cultivation experiment did

Rosenfeld and a large Google team implemented magic-state
cultivation on Willow [2], the protocol proposed by Gidney, Shutty,
and Jones [3]. Article claims below that appear in the Science
abstract [2] are labeled as such. Claims that I take from the
supplement are from arXiv:2512.13908v1 (Dec 15, 2025). I did not
compare that file against the published Science supplement.

A noisy magic state is injected into a distance-3 color code,
refined by a fault-tolerant measurement of the logical Hadamard
operator with postselection, and the surviving state is then
grafted into a larger encoding (distance 5, 54 qubits in the
grafting experiment), because the color code that suits cultivation
cannot hold the state at low idle error on its own. The paper calls
the target the surface code. During the cycles reported here the
grafted code still contains stabilizers like the color code's as
well as the surface code's, so it is not matchable; the main text
says d - 1 cycles would be needed before switching to a matchable
code, and decodes the grafting data with Tesseract, a most-likely-
error decoder based on A* search [17].

Notation used below: d is code distance; N is the number of
error-correction cycles in the grafted code; p is the noise strength
of the SI1000 model, a superconducting-inspired circuit-level
depolarizing model [16] used for all of the paper's Pauli-noise
simulations; LER is logical error rate, as the supplement uses it.

Three headline results:

1. Preparation. The v1 main text [2] calls the cultivated result an
   upper bound of 1(1) x 10^-4 error, after discarding instances
   with detected errors in logical state preparation and
   measurement, with about 8% of the data retained. The Science
   abstract, retrieved on Oct. 18, 2026, says cultivation reduces
   the error by a factor of 40, with a state fidelity of at least
   0.9999(1) (retaining 8% of attempts). The v1 preprint gives
   injection-only error 4.4(2)e-3 and cultivated full-circuit error
   between 1e-4 and 2e-4, a ratio of about 22 to 44. "About 40" is
   the paper's headline, at the low-error end of that range. The v1
   abstract states the fidelity as 0.9999(1) and does not use "at
   least".
2. Metrology. The team could not measure that result with standard
   logical state tomography. They built kickback tomography instead,
   which in v1 resolves an error near 1e-4 with on the order of 1e4
   measurements, against 1e8 for standard tomography.
3. Transfer. Cultivated states survive grafting into the distance-5
   code. Removing the error-correction cycles from the measurement
   circuit makes its error about 100 times worse in v1, which shows
   the color code underneath cultivation is doing real work.

The result I score is in the v1 supplement, Section XIV [2]: a
grafted-code memory experiment, which the authors call a start on
studying the cost of error-correction cycles. The cultivated |T>
state is idled for up to N = 9 cycles, and the LER is compared with
state-vector simulations in qevol, the supplement's restricted-rank
trajectory extension of the Pauli+ simulator of [12], using SI1000
at p = 2.3e-3. Section XIV carries that p over from Fig. 4. The main
text uses p = 3.0e-3 for Fig. 2 and p = 2.3e-3 for Figs. 3 and 4,
attributes the change to shifted qubit frequencies and different
control calibrations, and reports logical-error variation of about
1e-4 over an hour.

The seven-fold gap is the experimental LER divided by the simulated
LER at that fixed p. Fig. S22 places "Exp. fit, LER = 5.3%" on the
experimental panel (b) and "Exp. fit, LER = 0.8%" on the simulation
panel (e); I read "Exp. fit" as an exponential fit. The caption
gives LER "as a function of N" and does not state whether 5.3% and
0.8% are per cycle. The 0.8% carries one significant figure, so the
ratio lies between about 6.2 and 7.1 from rounding alone, in line
with the text's "about seven times." Section XIV does not say the
simulated curve was decoded with Tesseract. A decoder mismatch, or a
model mismatch, remains a candidate cause this comparison does not
close. The gap is one supplement figure, one grafted configuration,
and at most nine cycles.

The cultivation paper's introduction [2] states that magic-state
infidelities of about 1e-10 are required for factoring an RSA-2048
key, citing Gidney [13], and that infidelities between about 1e-6
and 1e-8 are needed for some quantum simulations and optimization.
The measured value, near 1e-4, is about six orders of magnitude from
the 1e-10 figure. The supplement shows cultivated error scaling as p
cubed in simulation. My own extrapolation from that fit, at fixed
distance 3 and assuming it holds: halving p would give a bound near
1e-5 to 2.5e-5, still above the 1e-6 to 1e-8 band and about five
orders of magnitude short of 1e-10.
Neither [2] nor [3] makes that projection. The Gidney-Shutty-Jones
protocol [3] reaches its low error rates at larger fault distance,
so this is one small-distance result set against the protocol's end
target.

## III. The six channels, scored

Verdicts used below, and only these:

- likely hit (attributed, not ablated)
- mentioned
- present but not independent
- baseline
- untested

Each of the six 2024 channels is scored once, with the verdicts
collected in Table 1. Low-frequency phase noise follows as a
measurement story, outside the six.

### 1. Leakage: likely hit (attributed, not ablated)

The experimental LER in the grafted-code memory experiment is about
seven times the simulated LER (v1 supplement, Section XIV [2]). The
authors state that population leakage is likely the main source of
the disagreement. Two signatures support the attribution, and both
are absent from the simulations, which do not include leakage:

- Detection-event likelihood rises slowly over time in the
  experimental data (Fig. S23 [2]), as long-lived population
  outside the computational subspace would produce.
- Detector covariance shows strong time correlations that
  propagate across the qubit grid (Fig. S24 [2]), which the authors
  describe as the characteristic leakage pattern.

The circuits did not contain the leakage removal units described in
previous work; the v1 supplement points to Google's 2023
surface-code scaling paper [12] (its reference 49). This note uses
the supplement's phrase, leakage removal units. The 2024 Willow
paper [4] used DQLR [15]. I do not treat the two names as the same
mechanism here.

Three routes could produce the gap, and the note keeps them apart:

(a) Readout control parameters, not optimized after the grafting
circuit redefines which sub-lattice of qubits is measured
mid-circuit, cause frequency collisions involving |2> states, which
cause leakage, which causes the gap. This is the route Section XIV
names. It is the leakage claim, not an alternative to it.

(b) The same unoptimized readout causes errors that never populate
|2>, such as assignment errors, and those cause the gap. Section XIV
does not name this route. It is this note's alternative, and it
counts against the leakage row.

(c) Variability in physical qubit performance. The main text names
it, beside leakage, for the experiment-simulation difference in the
Fig. 4 injection-only tomography [2]. Section XIV, where the
seven-fold gap is reported, does not name it. It counts against the
leakage row, as does the decoder or model mismatch noted in
Section II.

"Likely" is the authors' word. There is no run with leakage removal
units added and everything else held fixed, and no direct
measurement of |2> population on the grafted circuit. Until one
exists, the seven-fold gap has a named cause supported by
signatures and not proven.

Leakage in topological codes has a literature of its own, from
Suchara, Cross, and Gambetta [9] through McEwen and others [10] and
Battistel, Varbanov, and Terhal [11]. The 2024 note's claim was
about the model, not about priority.

### 2. Crosstalk: mentioned

Crosstalk appears in the v1 supplement [2] as a candidate source of
fixed detunings, through microwave crosstalk producing Stark shifts.
There is no separate crosstalk measurement, no scaling study, and no
comparison against the nonlocal crosstalk the 2024 note [1] flagged
on the 72-qubit processor.

### 3. Correlated errors: present but not independent

The detector covariance in Fig. S24 [2] is a time-correlation
result, and the correlations are the kind that break
independent-error decoding assumptions. The authors tie them to
leakage propagation. The experiment reports nothing about the 2024
claim of correlated bursts setting a 1e-10 floor in repetition
codes. Scoring this channel as independently confirmed would
double-count the leakage evidence.

### 4. Gate: baseline

The improvement the paper headlines as about 40-fold (22 to 44 on
the preprint v1 endpoints, Section II) is measured from an
injection-only error of 4.4(2)e-3, which the main text calls
"similar to our physical qubit gate errors" [2]. Nothing in the
experiment reopens the 2024 questions about the gate error budget.

### 5. Readout: baseline

Readout enters channel 1 through route (a), as unoptimized
parameters in a redefined measurement layout. That is part of the
leakage score. It is not a new, independent test of the 2024
readout baseline.

### 6. Classical chaos: untested

Nothing in the cultivation paper addresses Boerner and others [8] on
classical chaos in transmon systems. The p-cubed scaling the authors
verify is the protocol's designed fault-tolerance scaling, and it
does not probe chaotic dynamics. Untested in either direction.

### Measurement story: low-frequency phase noise (not a channel)

Early in the project, logical state tomography of cultivated states
returned a non-physical norm. The v1 supplement [2] attributes this
to low-frequency phase noise, and simulations of coherent phase
noise reproduce the effect. Candidate sources named there: slow
qubit frequency drift, residual magnetic fields from control lines,
and Stark shifts on the qubits through microwave crosstalk. The
cultivation circuit is exposed because its data qubits spend long
stretches idling in an entangled state.

Without echo pulses to filter this noise, the team's comparison in
v1 suggests their performance was dominated by it. They built
kickback tomography so that the measurement is taken along the
prepared state's own axis in a single circuit. With echoing in
place, a further simulation bounds the remaining |T> infidelity from
quasi-static detunings near 1e-5 [2]. That figure is a simulated
bound under assumed plus or minus 200 kHz quasi-static detunings,
run with no depolarizing noise, and the supplement's Fig. S14c still
shows non-physical norms for some echoed detuning draws. This is a
2026 measurement, not a 2024 objection, so it does not appear in
Table 2. The 2024 correlated claim was the burst floor, and this note
does not widen that channel to include low-frequency phase noise.

Kalai [5], and Kalai, Rinott, and Shoham [6], object that
time-independent Pauli models omit coherent and non-stationary
noise. The tomography failure is an instance of coherent
low-frequency noise breaking a measurement that those models treat
as routine. It does not test Kalai's claims about the supremacy
experiment.

## IV. Updated standing of the 2024 objections

Table 2. Standing of the 2024 third-party objections [1] after the
cultivation experiment [2]. The 2024 grades are copied from the
challenge table of [1] as read from its ResearchGate text, without
redefinition. "Unchanged" means this experiment did not test the
objection. "Evidence added" is yes only when the cultivation paper
tests that 2024 objection.

| Objection (source) | 2024 grade in [1] | After cultivation (2026) | Evidence added |
|---|---|---|---|
| Noise sensitivity (Kalai [5], [6]) | Partially | Partially. The tomography failure is coherent low-frequency noise. It does not test Kalai's claims, and it does not test the 2024 burst floor. | no |
| Nonlinear errors (Hirota [7]) | Indirectly | Indirectly, unchanged. | no |
| Classical chaos (Boerner et al. [8]) | Partially | Partially, unchanged. | no |

No row moves to Solved.

## V. What would settle the leakage claim

Only the cultivation team can run the settling experiment. What a
note can do is fix, before the run, what each outcome would mean.

Two cheaper checks come first. Three-state readout on the grafted
circuit uses the existing Willow processor and needs the team's
runtime. It measures |2> population directly, cycle by cycle,
instead of inferring it from detector signatures, and it is the
only measurement that separates route (a) from route (b). The
second check needs no device: rerun the simulations with leakage
injected. The v1 supplement cites Marshall and Kafri's incoherent
approximation of leakage [14] (its references 38 and 43) for its
leakage modeling. I have not read [14] and do not evaluate that
method here; the cultivation team can apply its own implementation
directly. No leakage rates have been measured on the grafted
circuit, so an outside rerun would have to borrow rates from the
2023 paper [12]. That makes it an order-of-magnitude check on
whether leakage at 2023-like rates can produce a gap of about
seven, not a reproduction.

The 2023 calibration target is the average detection probability
in [12]. After the Fig. 2 averages there, that average shows a
relative rise of 12% at distance 5 and 8% at distance 3 over 25
cycles, with a typical risetime of roughly 5 cycles, and the
Pauli+ simulation raises it by 7% over 25 cycles at distance 5.
Those are rises in averages over stabilizers of the same weight.
Fig. S23 of [2] reports a slow increase for some detectors, not an
array average, so a match to the 2023 averages would not certify
the shape of those traces. The 2023 target is also a different
processor generation and a plain memory circuit. The grafted-circuit
rise is a prediction of the check, not a fit to Fig. S23.

The Zenodo record cited in the v1 data-availability line,
10.5281/zenodo.17872003, publishes measurements.csv and
detection_events.csv for Figs. 2, 3, and 4, with Fig. 4 at N = 2 and
N = 3. It has no directory for the N = 9 run behind Figs. S22, S23,
and S24. The S23 rise and the S24 covariance therefore stay
structural checks; neither can be scored as a numeric match from
that record.

The settling experiment is a 2 by 2. Run the grafted-code memory
experiment in four arms: leakage removal units added or not, crossed
with readout control parameters re-optimized for the redefined
layout or left as they were. Every arm carries three-state readout,
so each arm reports both its LER ratio and its cycle-resolved |2>
population.

Four design rules hold for every arm:

1. Fixed p. Freeze p from an unpostselected memory circuit on the
   same qubits on the same day, and use that one value for every
   arm. Do not fit p to the grafted data; a per-arm fit could shrink
   the ratio by construction. The postselected kickback-tomography
   circuit of Fig. 3 serves as a cross-check, not as the
   calibration, because its 8% retention makes a fitted p depend on
   the postselection rule.
2. Matched simulation. The simulation for each removal arm includes
   the removal-unit operations at the same SI1000 strength, so that
   the overhead those units add sits in the denominator as well as
   the numerator.
3. Pass margin. Fix the shot count in advance so that the 95%
   interval on each arm's LER ratio is no wider than plus or minus 1
   at a ratio of 7. SI1000 is itself simplified, so a ratio of
   exactly one is not the target. Call an arm closed when the upper
   95% bound on its ratio is below 2; unchanged when its interval
   overlaps the v1 range of 6.2 to 7.1; narrowed in between; widened
   when its lower bound exceeds 7.1.
4. |2> criterion. Call an arm leakage-reduced when its mean |2>
   population over cycles 2 to 9 is below half that of the baseline
   arm, with non-overlapping 95% intervals.

Table 3. Pre-registered readings of the 2 by 2. Arms: B, baseline
(no removal, readout as in v1); R, readout re-optimized only; L,
leakage removal only; RL, both. "Closed", "narrowed", "unchanged",
and "widened" follow rule 3; "|2> down" follows rule 4.

| Pattern | Reading |
|---|---|
| L and RL closed; R not closed | Leakage confirmed by removal. The 2024 channel moves from likely to demonstrated in this protocol. |
| R closed with \|2> down; L closed | Route (a) confirmed: readout misconfiguration caused leakage, which caused the gap. Leakage moves to demonstrated, with its entry path named. |
| R closed without \|2> down | Route (b): the readout path causes the gap without leakage. The leakage score is withdrawn and the gap is scored to readout. |
| L or RL narrowed, not closed | Leakage is one cause among several. The residual goes to route (b), route (c), or decoder or model mismatch, and the inventory splits the channel. |
| All arms unchanged | The attribution fails. The signatures in Figs. S23 and S24 [2] need another explanation, and this note's leakage score is withdrawn. |
| L or RL widened | Removal overhead dominates at this scale despite rule 2. The test is inconclusive and is reported as such. |

The authors say they expect improvement from leakage removal, better
calibration, and larger distances. The follow-up literature should
be scored on which row of Table 3 is reported (a pattern not listed
there is reported as observed and scored inconclusive), and on whether the
rerun is reported at all.

## VI. Limitations

I am scoring my own 2024 inventory, and the Table 2 grades come from
a ResearchGate text of that note whose column layout did not survive
extraction. The memory-experiment numbers, figure pins, and "likely"
wording come from arXiv:2512.13908v1, not from the published Science
supplement, which I did not compare. The v1 data-availability line
points to Zenodo record 10.5281/zenodo.17872003; opened on Oct. 18,
2026, it holds detector-level files for Figs. 2, 3, and 4 and no
N = 9 directory for Figs. S22 to S24. I did not rerun the paper's
simulations. The repository behind this note holds a distance-3
calibration run of a local leakage simulator; it is not a result of
this note. The pass margin and |2> criterion in Section V are my
choices, fixed here before any rerun. The leakage score rests on one
grafted-code memory figure, one configuration, and at most nine
cycles.

## VII. Conclusion

The 2024 note [1] argued that the channels the simplified model
omitted would decide how far the hardware scales. Read against that
inventory, the cultivation paper [2] supplies one likely hit on
leakage, attributed and not ablated, in one grafted configuration.
The authors' own account puts readout misconfiguration upstream of
the leakage, so readout is part of that hit. Route (b), qubit
variability, and decoder or model mismatch remain open. The other
five channels are mentioned, present but not independent, baseline,
or untested. The factor-of-40 headline is state error against
injection. The factor-of-seven gap is memory LER against SI1000 at
p = 2.3e-3. Those are different measurements. Keep the inventory,
score each new experiment against it, and insist on the 2 by 2 with
three-state readout that turns "likely" into a measurement.

## Availability

The scoring worksheet, source pins, review files, and local
simulator will be deposited on Zenodo with this note's DOI. No DOI
is minted yet, and the working repository is not public.

## AI Utilization Statement

This note was prepared with AI assistance, directed by the author at
every stage. Muse (Meta) agents (model version not recorded) located
and read the primary sources, cross-checked numbers and attributions
in the draft against them, and drafted the text at the author's
instruction. Grok 4.6 applied the author's 2023 rise-leg
substitution to Section V wording, then a later critical-review pass
(abstract citations, table captions, Section V hardware split,
Limitations local-instrument line). The leakage simulator in the
repository was written by OpenAI GPT-6 Astra through OpenRouter from
the author's briefs, then reviewed and tested before use; a
distance-3 calibration run of it is recorded in the repository and
is not a result of this note. The draft then went through two
internal adversarial passes (a spec-faithful claims trace and an
independent adversarial review), and two external critical
evaluations commissioned by the author through OpenRouter, from
Moonshot Kimi K3 and Anthropic Claude Opus 5.5. Claude (Anthropic),
through Claude Code, ran a further critical review of v3 and applied
its findings to produce v4, checking each change against the local
copy of arXiv:2512.13908v1. Every finding from those passes was
adjudicated before any revision was applied. The review files will
be part of the Zenodo deposit when minted. They have no public URL
yet. The author selected all sources, made every publish and revise
decision, and takes responsibility for the claims, the scoring, and
the conclusions. AI output was treated as draft throughout. Claims
scored here were checked against arXiv:2512.13908v1 and the Science
abstract [2]. The published Science supplement was not compared. No
AI system is listed as a co-author.

Affiliation: Chokmah LLC, Norwich, VT. Contact: chokmah-dyb@pm.me.

## References

[1] D. Y. Bilar, "Notes on Google Willow (2024)," preprint, 2024. doi: 10.13140/RG.2.2.30911.01443. Accessed: Oct. 18, 2026. [Online]. Available: https://www.researchgate.net/publication/387576664_Notes_on_Google_Willow_2024_aka_Quantum_Error_Correction_Below_the_Surface_Code_Threshold

[2] E. Rosenfeld, C. Gidney, et al., Google Quantum AI and Collaborators, "Magic state cultivation on a superconducting quantum processor," *Science*, First Release, Oct. 15, 2026 (no volume or pages yet). doi: 10.1126/science.aee7961. Accessed: Oct. 18, 2026. Supplement claims in this note are from arXiv:2512.13908v1, Dec. 15, 2025. [Online]. Available: https://doi.org/10.1126/science.aee7961

[3] C. Gidney, N. Shutty, and C. Jones, "Magic state cultivation: growing T states as cheap as CNOT gates," *arXiv preprint*, arXiv:2409.17595, 2024. Accessed: Oct. 18, 2026. [Online]. Available: https://arxiv.org/abs/2409.17595

[4] Google Quantum AI and Collaborators, "Quantum error correction below the surface code threshold," *Nature*, vol. 638, pp. 920-926, 2025 (published online Dec. 2024). doi: 10.1038/s41586-024-08449-y. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.1038/s41586-024-08449-y

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

[15] K. C. Miao et al., "Overcoming leakage in quantum error correction," *Nature Physics*, vol. 19, pp. 1780-1786, 2023. doi: 10.1038/s41567-023-02226-w. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.1038/s41567-023-02226-w

[16] C. Gidney, M. Newman, A. Fowler, and M. Broughton, "A fault-tolerant honeycomb memory," *Quantum*, vol. 5, p. 605, 2021. doi: 10.22331/q-2021-12-20-605. Accessed: Oct. 18, 2026. [Online]. Available: https://doi.org/10.22331/q-2021-12-20-605

[17] L. A. Beni, O. Higgott, and N. Shutty, "Tesseract: A search-based decoder for quantum error correction," *arXiv preprint*, arXiv:2503.10988, 2025. Accessed: Oct. 18, 2026. [Online]. Available: https://arxiv.org/abs/2503.10988
