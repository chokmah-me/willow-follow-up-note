# Section V, simulation arm: a leakage-injected re-simulation design

Companion to `draft/follow-up-note-draft-v3.md`, Section V. The
note's Section V names two cheaper checks ahead of the hardware
2x2: three-state readout, and "the same simulations, rerun with
leakage injected at measured rates." This file specifies the
second check as an experiment that could settle, or exclude,
the leakage attribution for the grafted-code memory gap
(about 7x against SI1000 at p = 2.3e-3, arXiv:2512.13908v1
supplement, Section XIV). Written 2026-10-16. Nothing here has
been run.

## The instrument already exists

The cultivation paper's own distance-5 grafting simulations ran
in qevol, "an extension of the Pauli+ simulator" (supplement,
Section XI B). Pauli+ is Google's leakage-carrying stabilizer
simulator, specified in full in the 2023 surface-code
supplement (arXiv:2207.06431, Section XIV): each qubit carries
a leakage label (computational, |2>, |3>), each noisy gate gets
a generalized Pauli channel over those labels, and the run is a
Markov chain over label vectors plus a stabilizer tableau. The
twirling approximation underneath it is justified in Marshall
and Kafri (arXiv:2312.10277, Phys. Rev. Applied 2025). Stim
alone cannot do this; it has no leakage states. No open-source
Pauli+ implementation was found (checked 2026-10-16), so an
outside run is a reimplementation from a published algorithm.
The scored memory comparison used SI1000 noise inside that
framework with the leakage channels off. The settling run is
the same framework with them on.

## Inputs, from the published record

- Baseline: SI1000 depolarizing model at p = 2.3e-3, the note's
  and the paper's own baseline. Arm 1 (below) must reproduce
  the paper's simulated logical error rate before any leakage
  arm means anything.
- Leakage generation: about 0.09 to 0.11% per cycle per qubit
  (McEwen et al. 2021 rate-equation fits; steady-state |2>
  population 0.97 to 1.30% in the same fits).
- Leakage lifetime: injected |2> decays with a constant near
  4.4 cycles (Miao et al., Nature Physics 2023). Consistency:
  0.1% per cycle times a 4.4 to 11 cycle lifetime gives a
  steady state of 0.4 to 1.0%, matching the fitted ~1%.
- Removal efficacy, for Arm 4: excess |2> under 1e-3 within
  two cycles under DQLR-style removal (Miao et al. 2023).
- Device distributions: the cultivation supplement's Section V
  (Willow Device Properties, Figs. S5 to S9) gives the
  single-qubit, CZ, and readout parameters for the qubits
  active in the grafting experiment, as distributions and
  medians. Per-qubit values are in figure panels, not tables.
- Not published: per-CZ leakage on Willow. The design sweeps
  the generation rate and inverts for the value the gap
  requires, rather than assuming it.
- Referee precedent: in the published peer review file for the
  2024 Willow paper, Referee #2 asked the authors to estimate
  DQLR efficiency by injecting leakage errors, and Referee #3
  pressed on leakage-reduction efficiency and leakage
  lifetime. In the 2023 paper's peer review file, referees
  pressed on the Pauli+ leakage simulations, the leakage
  steady state, and state-dependent leakage rates. The
  injected-leakage check is a referee-grade request, not a
  new invention of this note.

## Arms (all against the same SI1000 baseline, same decoder)

1. Baseline. SI1000 at p = 2.3e-3, no leakage. Sanity: must
   reproduce the paper's simulated logical error per cycle.
2. Leakage injected. Stochastic |2> and |3> transitions on
   data and measure qubits, generation rate swept from 0 to
   0.5% per cycle, decay fixed at the 4.4-cycle constant,
   leakage transport on (a CZ with one leaked partner applies
   a noise channel to the other: the S24 mechanism), seepage
   on. No removal units, matching the paper's circuits.
3. Leakage plus readout path. Arm 2 with an elevated
   generation rate on the redefined measurement qubits (the
   supplement's proposed entry path: unoptimized readout
   parameters after grafting, |2> frequency collisions). The
   multiplier is swept as well, so this arm yields a family
   of curves, not a point.
4. Leakage plus removal. Arm 2 with modeled removal at the
   Miao efficacy. This arm is a prediction for the hardware
   rerun, not a fit: it states in advance how far the gap
   should close if removal is added.

## Observables: all three, at one rate pair

The attribution is tested against three observables jointly,
not one at a time:

a. The logical error ratio: simulated logical error per cycle
   over the Arm 1 baseline, target about 7.
b. The S23 shape: detection-event likelihood rising slowly
   over the cycles, matched in functional form and risetime.
   The 2023 paper's Pauli+ run already reproduced this
   signature's shape (experimental rise 12% over 25 cycles at
   distance 5; simulated 7%).
c. The S24 structure: the detector covariance matrix, strong
   time correlations spreading across the grid, compared as a
   structure (detector-pair classes or matrix distance), not
   as a single scalar.

## Criterion, fixed in advance

Leakage is quantitatively consistent if one (generation,
decay) pair inside the literature band (generation 0.05 to
0.3% per cycle, lifetime 3 to 11 cycles) reproduces (a), (b),
and (c) jointly to within the paper's stated uncertainties,
with the implied steady-state |2> population under about 1%.
Leakage is excluded as the sole explanation if no pair in
that band does: for example, the rate that yields 7x gives
the wrong S23 risetime, or 7x requires a generation rate an
order of magnitude above the literature band. Arms 2 and 3
both fitting means simulation cannot separate plain leakage
from the readout path; that separation is not this
experiment's to give.

## The pin that makes it near-decisive

A simulation with a swept rate ranks hypotheses. The same
simulation with the rate measured stops being a ranking. A
three-state readout measurement of the steady-state |2>
population on the grafted circuit (Section V's first cheap
check) fixes generation times lifetime directly and collapses
the sweep to one point: feed the measured population in, and
either the three observables come out together or the
attribution fails. Simulation alone cannot supply that
number; it is a hardware measurement, and a cheap one.

## Cost

About 100k shots per arm per sweep point for the logical
error ratio (the noisiest observable), 10 to 20 sweep points,
4 arms: a few million shots total. Hours to a day on a
workstation in an optimized Pauli+ reimplementation. The
covariance observable sets the shot floor.

## Limits, stated

- A joint match shows leakage is sufficient and quantitatively
  consistent. It does not show leakage happened. Only the
  removal rerun (the note's Section V 2x2) attributes.
- The framework twirls away coherence between computational
  and leaked subspaces. A tensor-network study
  (arXiv:2308.08186) shows coherent and stochastic leakage
  models can disagree; results are conditional on the
  incoherence assumption, which repeated stabilizer
  measurement plausibly enforces.
- Arm 3 is underdetermined without device-specific collision
  and readout data that only the team has.
- This design settles the simulation half of Section V. The
  note's scores do not change until a run exists.
