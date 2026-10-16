# Peer review files: what they give the follow-up note

Question: do the published referee exchanges for the 2023
surface-code paper (70 pp) and the 2024 Willow paper (34 pp)
give v3's Section V or Section III.1 anything citable that v3
does not already have?

Short answer: yes, three sentences' worth for the note
itself, plus three items for the simulation design file. Not
"nothing new."

Files read in full (text extractions):
- `~/workspace/willow-sources/google-2023-surface-code-peer-review-file.txt`
  (2,873 lines)
- `~/workspace/willow-sources/google-2024-willow-peer-review-file.txt`
  (1,390 lines)
Line numbers below are approximate positions in those files.

## For the note, worth a sentence each

### 1. Section V: a referee already asked for the injected-leakage DQLR calibration

2024 file, Version 0, Referee #2, item 2D (near line 203):
"Could the authors also estimate more precisely the DQLR
efficiency by injecting leakage errors? (they give only a
very crude estimate for the transition probabilities
Pi→j) presented in the supplemental materials (bottom of
p14))."

Author response (near line 830): "This study was previously
undertaken in the paper that first introduced the DQLR
method ('Overcoming leakage in quantum error correction.'
Nature Physics 19.12 (2023))."

What this gives Section V: the injected-leakage
calibration that the design's Arm 4 needs was requested in
Nature peer review and not produced; the authors pointed
to Miao et al. 2023 instead. So the removal-efficacy input
for any near-term version of the Section V test rests on
the 2023 measurement, not on a Willow-class
injected-leakage calibration. That is both a precedent
(the check is referee-grade, not the note's invention)
and a qualification (the number is borrowed). One
sentence in Section V earns both.

### 2. Section III.1: the authors' own account of why leakage spreads

2024 file, Version 0, Referee #3, item 5 (near line 300):
"DQLR seems to help strongly distance-5 but not
distance-3. I understand this fits with simulation in the
supplementary material, but can one give an intuitive
explanation of the reasoning in the main text? Is the key
element leakage lifetime, or how it spreads across the
lattice, ...?"

Author response (near line 1017): "Qualitatively, a single
long-lived leakage event can cause failure by spreading
errors across the lattice. We hypothesize that at larger
distances, this high-weight correlated failure mechanism
becomes more pronounced relative to the higher degree
error suppression."

What this gives III.1: the team's own words for the
mechanism behind the S24 "bleeding" signature (time
correlations spreading across the grid), stated for the
distance-5 case specifically. The note currently describes
the signature; this quote supplies the authors'
mechanistic reading of it, on the record. One sentence.

### 3. Section V: the removal arm must cover data qubits, not just measure qubits

2023 file, Referee #1 (near line 152): "For leakage removal
the authors cite [42,47-49], but [42] and [49] only
considers removing measure qubit leakage while from the
Suppl. Material it is clear that data qubit leakage is
important."

What this gives Section V: the 2x2's "leakage removal
units added" arm needs one qualifying clause, that the
removal must act on data qubits as well as measure
qubits, because a referee established on the record that
measure-only removal leaves the important channel
untouched. Without that clause, a future removal run
could "add removal" in the measure-only sense and still
leave the gap, producing a false negative for the
attribution. One sentence.

## For the simulation design file, not the note

### 4. Uniform leakage rates were already flagged as a simplification

2023 file, Referee #1 (near line 176): "in simulation the
leakage rates were uniformly picked while some qubits are
clearly leaking more than others."

Author response (near line 1070): "The referee is observant
to point out that some qubits are leaking more than
others... the simulation reported here uses uniform
leakage parameters. It would be more complicated but
surely more accurate to use separate measurements on
each qubit in order to refine the model, as the referee
suggests. This is a subject of ongoing research."

Design use: this is the published precedent for the
design's per-location/per-qubit injection (my SME review's
MAJOR #5). The cultivation supplement's Figs. S5-S9 give
the per-qubit distributions the 2023 authors said they
lacked. Cite it in the design as the reason the
reimplementation should do better than uniform.

### 5. The team's own defense of the stochastic leakage framework

2023 file, Referee #1 (near line 181): Pauli+ "cannot
capture the fact of course that leakage is
state-dependent (i.e in a CZ |11> can leak to |02>, but
not the other states...). You model this by assuming the
qubit is in a random state and reducing the leakage rate
correspondingly, but it is a feature that one cannot
model easily."

Author response (near line 1093): their trajectory
simulator kraus_sim "explicitly includes the
state-dependent nature of leakage, yet we find that, for
our current experimental parameters, these details do not
significantly impact the observed logical error rate or
statistics of typical detection event edges."

Design use: this is the citable justification for the
design's twirled/stochastic framework, answering the
coherence caveat with the team's own finding. Caveat to
carry alongside: shown for the 2023 parameters, not the
grafted configuration. Belongs in the design's Limits,
not in the note.

### 6. The ~5-cycle rise as a steady-state question

2023 file, Referee #1 (near line 151): "'The average
detection..roughly 5 cycles [43]': is this the number of
cycles for the qubits to reach their leakage steady
state? Could be discussed in more detail."

Design use: the same slow-rise signature as the
cultivation Fig. S23, and the referee's steady-state
reading is exactly the physical interpretation behind
the design's exclusion boundary (implied steady-state
|2> under ~1%). One line in the design's criterion
discussion.

## Checked and set aside

- 2023 Referee #1's broad endorsement ("scalable
  Pauli+Leakage simulations... are able to capture the
  performance of the device fairly well," near line 29):
  supports the design's instrument choice, but the design
  already asserts this; no sentence needed.
- 2023 Referee #1 on post-selecting leakage events (near
  line 238): the cultivation experiment does post-select
  on state-preparation detectors, so the point does not
  transfer cleanly; the design should still replicate the
  actual post-selection (see SME review).
- 2024 Referee #1 on the 10^-10 repetition-code floor:
  the note's correlated row already covers the floor;
  nothing new for any section.
- 2024 Referee #4's caveat on detection probability
  rising with code size: a scaling caveat for the 2024
  paper, not for the cultivation memory experiment; not
  used.

## Bottom line for the author

Three insertions, each one sentence, all with published
peer-review provenance: (1) Section V, the injected-leakage
DQLR calibration was requested in review and deferred to
Miao 2023; (2) Section III.1, the authors' "single
long-lived leakage event... spreading errors across the
lattice" as the mechanism behind the S24 signature;
(3) Section V, the removal arm must include data-qubit
removal, per the 2023 referee. Items 4-6 go into the
design file. None of this changes any score; it hardens
the sourcing around the leakage claim.
