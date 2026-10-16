# SME review: Section V leakage-injected re-simulation design

Reviewer stance: skeptical practitioner in superconducting QEC
simulation. Object under review:
`results/section-v-simulation-design.md` (2026-10-16), the
specified "second cheap check" for the ~7x grafted-code memory
gap (arXiv:2512.13908v1, supplement Section XIV; experimental
LER fit 5.3%/cycle vs simulated 0.8%/cycle; signatures Figs.
S23/S24). Checked against the cultivation supplement text, the
2023 surface-code supplement (arXiv:2207.06431, Sec. XIV), and
both published peer review files. Nothing in the design has
been run; this review is of the design only.

## Verdict

The design is conceptually sound and asks the right question
in the right way: a joint fit of three observables at one
parameter point, with the exclusion case stated in advance.
No BLOCKERs. The gaps below are all fixable before anyone
builds, but several are load-bearing: as written, a
reimplementation could reproduce the wrong baseline, fit the
wrong thing, or declare victory on a comparison the paper
never made quantitative.

## What is sound

- SOUND: The instrument choice. The memory simulations in
  the supplement ran in qevol with SI1000 at p = 2.3e-3 and,
  in the authors' words, "do not include leakage
  approximations." Re-running the same framework with leakage
  channels on is exactly the experiment the authors did not
  run. Stim alone indeed cannot do this.
- SOUND: The Arm 1 null requirement. Reproducing the
  paper's 0.8%/cycle simulated rate before any leakage arm
  means anything is the correct gate.
- SOUND: The joint-fit logic. Requiring (a), (b), and (c) at
  one rate pair is the teeth of the design, and the
  pre-registered reading of "Arms 2 and 3 both fit" (cannot
  separate leakage from the readout path) is honest.
- SOUND: The literature band (generation 0.05 to 0.3%/cycle,
  lifetime 3 to 11 cycles, steady state under ~1%) is fairly
  drawn from McEwen 2021 and Miao 2023.
- SOUND: Arm 4 as a prediction for the hardware rerun rather
  than a fit. Correct.
- SOUND: The cost estimate, now checkable: at 100k shots,
  the 5.3% experimental-equivalent arm yields ~5,300 logical
  errors and the 0.8% baseline ~800, so the ratio resolves as
  roughly 6.6 +/- 0.25. That is adequate for the sweep.

## Findings

### MAJOR: the decoder is unnamed, and the 7x conflates two things

The design says "same decoder" for all arms but never names
it. The supplement does: "we decode the resulting data with
Tesseract, a most likely error decoder using the A* search
technique [39]." A reimplementation must decode simulated
shots with the same Tesseract configuration, or the Arm 1
sanity check is meaningless.

Deeper: Tesseract's error model is presumably Pauli-based.
A Pauli-assuming decoder degrades on leakage-correlated
syndromes, so the 7x ratio mixes "more physical errors" with
"decoder less suited to the error type." The design's
criterion attributes the whole joint fit to physical
leakage. Fix: name Tesseract, require the identical decoder
in all arms, and add a diagnostic variant that decodes Arm 2
with a leakage-aware (or correlated) decoder. If the ratio
shrinks substantially under the better decoder at fixed
physics, part of the 7x was decoder mismatch, and the
criterion must be restated in terms of the physical excess,
not the decoded ratio.

### MAJOR: post-selection is not replicated, and it is a fourth observable

The memory experiment post-selects ("for no detection events
on the state preparation detectors before grafting," main
text; Fig. S22 panels (c)/(f) report post-selection rates
for experiment vs simulation). Leakage during cultivation
and grafting would suppress the experimental keep rate
relative to simulation. The design never mentions
replicating the post-selection procedure, and it omits the
keep rate from the observables. Fix: replicate the
post-selection exactly in all arms and add (d) the
post-selection rate, experiment vs simulation, as a fourth
joint observable. It is cheap and it is in the paper.

### MAJOR: nine cycles make the S23 risetime a weak observable

The slow rise in Fig. S23 is fit over at most nine QEC
cycles. A risetime extracted from nine points under shot
noise has poor discriminating power: several (generation,
decay) pairs will fit it about equally well. The design
treats (a), (b), (c) as coequal. Fix: state plainly that
(b) is the weakest of the three at N <= 9, and put the
discriminating weight on (a) and (c). Do not let a joint
"pass" ride mostly on a loose risetime fit.

### MAJOR: the sweep is 1D but the criterion is 2D

The arms fix the decay at "the 4.4-cycle constant" while
sweeping generation; the criterion then asks for "one
(generation, decay) pair" inside a band that includes
lifetimes from 3 to 11 cycles. These disagree. Worse, the
4.4-cycle number is an injected-|2> decay constant from
Miao's device, while McEwen's fits give ~11 cycles without
reset for data qubits on Sycamore. Fix: run the 2D sweep
(generation 0 to 0.5%/cycle, lifetime 3 to 11 cycles), or
justify the 1D slice and rewrite the criterion to match
it. The steady-state bar (under ~1%) then becomes a curve
in the plane, which is the correct exclusion boundary.

### MAJOR: inject per location, not per cycle

The design lumps leakage into a uniform per-cycle,
per-qubit generation rate. The 2023 supplement, from the
same team, parameterizes per mechanism: CZ dephasing with
Kraus operator sqrt(pt)(|02><11| + |11><02|), pt = 8e-4 per
CZ, leaking only the higher-frequency qubit; passive
heating |1> to |2>; and numerically calibrated transport
transitions (|22> <=> |13>, |21> <-> |03>) between measure
and data qubits. A uniform rate also repeats the exact
simplification a 2023 referee flagged ("in simulation the
leakage rates were uniformly picked while some qubits are
clearly leaking more than others"), to which the authors
answered that per-qubit rates would be "more accurate" and
"a subject of ongoing research." Fix: start from the 2023
per-mechanism parameterization, sweep an overall scale
factor, and where the cultivation supplement's Figs. S5-S9
give per-qubit distributions, use them. The S24 structure
(which qubit pairs correlate) depends on where leakage is
born; a uniform rate can fit the ratio while getting the
geography wrong.

### MAJOR: the reset rule for leaked measure qubits is unspecified

Measure qubits are measured and reset every cycle. Whether
a leaked measure qubit is cleared by reset, and with what
probability, controls the steady state and the S23 rise
shape. McEwen 2021 measured this: with reset, measure
gamma-down is 328%/cycle (reset clears it fast); data
qubits lose leakage largely by transport to measure
qubits. The design says "seepage on" and moves on. Fix:
specify the reset rule explicitly with literature
probabilities, including the data-to-measure transport
path. This is not a detail; it is half the steady-state
calculation.

### MAJOR: "the paper's stated uncertainties" may not exist for (b) and (c)

The criterion requires matching "to within the paper's
stated uncertainties." The supplement states LER fits
(5.3% vs 0.8%) but, in the extracted text, no uncertainties
are quoted for the S23 curves, the S24 matrices, or the 7x
ratio itself (5.3/0.8 = 6.6, rounded to "about seven").
Fix: define the comparison metric in the design. For
example: chi-square of the simulated S23 curve against
the experimental points with experimental shot noise;
Frobenius or per-class distance of the covariance
matrices with a null distribution from the no-leakage
arm; tolerance bands on the ratio from the shot counts.
Also recover the experimental shot count behind S23/S24
(check the paper's data availability); it sets the bar
the simulation must clear.

### MINOR: qevol, not Pauli+, is the build target

The memory experiment idles a cultivated |T> state, which
is not a stabilizer state. Plain Pauli+ (tableau only)
cannot represent it; the reimplementation must be
qevol-like, i.e. superpositions of stabilizer states per
the supplement's Section XI B. The design mentions qevol
but then prices "an optimized Pauli+ reimplementation."
Fix: state the required stabilizer rank explicitly (small
for |T>-like states, so the cost estimate survives) and
name qevol's Section XI B, not just the 2023 Pauli+
section, as the build spec.

### MINOR: add an explicit drift arm

A time-ramped readout error with no leakage (calibration
drift over the nine cycles) is the obvious alternative
mechanism for a slow S23 rise. It should reproduce (b) and
fail (c), since readout error correlates timelike, not
across the grid. The design's joint logic implies this,
but pre-registering the drift arm and its expected
negative result makes the test sharper and harder to
explain away afterward. Cheap in the same framework.

### MINOR: Arm 3's multiplier is ad hoc

"Elevated generation rate on the redefined measurement
qubits" via a swept multiplier is a placeholder, not a
mechanism. The literature has per-readout-event leakage
probabilities (the 2023 supplement's measurement section;
Miao). Fix: parameterize Arm 3 as a per-measurement
|2>-transition probability from the literature, swept over
its uncertainty range, rather than a dimensionless
multiplier.

### MINOR: pin down the small things

- |3> generation: the design carries |3> labels but gives
  no generation rate. State the assumption (e.g.
  second-order/negligible, or a fixed ratio to |2>).
- Sweep vs decision band: the sweep runs 0 to 0.5%/cycle
  while the criterion band is 0.05 to 0.3% and the text
  says "an order of magnitude above." Define the numeric
  exclusion threshold instead of the prose one.
- Simulate the full circuit (injection, cultivation,
  graft, then N idle cycles), not just the idle; the
  supplement's simulations did the full grafting
  experiment.
- Use the paper's detector definitions and the same
  covariance estimator for S24; say which.
- Null check, stated: at generation approaching zero the
  reimplementation must reproduce flat S23 and no S24
  bleeding. This guards against a reimplementation bug
  manufacturing the match.

## What the design gets right about its limits

The stated limits are the right ones: sufficiency is not
attribution; Arm 3 is underdetermined without device data;
the twirling/incoherence assumption is conditional (the
tensor-network caveat is correctly scoped). One addition
from the review record, worth a sentence in Limits: in
the 2023 peer review, the authors were pressed on exactly
the state-dependence the twirling approximation discards,
and answered that their trajectory simulator
(kraus_sim), which includes state-dependent leakage,
showed "these details do not significantly impact the
observed logical error rate or statistics of typical
detection event edges" for their parameters. That is the
team's own justification for the stochastic framework;
cite it, with the caveat that it was shown for the 2023
parameters, not the grafted configuration.

## Bottom line

Build it after the MAJOR items are fixed, in this order:
name Tesseract and add the decoder diagnostic; replicate
post-selection and add the keep rate; make the sweep 2D;
inject per location from the 2023 parameterization;
specify the reset rule; define the comparison metric.
With those in, the joint fit is a genuine test. Without
the decoder and post-selection items in particular, a
"pass" would not mean what the design claims it means.
