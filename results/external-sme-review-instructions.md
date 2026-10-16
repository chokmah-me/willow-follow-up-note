# Review instructions for an external SME

You are a subject-matter expert in superconducting quantum error
correction and its simulation. Review an experiment design, not a
paper. Be skeptical. Your job is to decide whether the proposed
simulation, if built and run as specified, would actually settle
the question it claims to settle, and to name what is missing
before anyone builds it.

Context. A follow-up note scores Google's 2026 magic-state
cultivation experiment (Rosenfeld et al., Science 2026; supplement
read as arXiv:2512.13908v1) against a 2024 error-channel
inventory. In the supplement's grafted-code memory experiment
(distance-3 color code grafted to a distance-5 surface code, 54
qubits, cultivated state idled up to nine QEC cycles), the
measured logical error rate is about seven times the SI1000
depolarizing simulation at p = 2.3e-3. The authors attribute the
gap as "likely" mainly to population leakage, supported by two
signatures (Fig. S23: detection-event likelihood rising slowly
over time; Fig. S24: detector covariance with strong time
correlations spreading across the grid). No ablation run exists.
The note's Section V proposes cheaper checks before any hardware
rerun, one of them a leakage-injected re-simulation. The design
under review specifies that re-simulation.

Materials provided: (1) the design file,
results/section-v-simulation-design.md; (2) the note itself,
draft/follow-up-note-draft-v3.md, Sections I, III.1, and V; (3)
the cultivation supplement text (arXiv:2512.13908v1), Sections V,
XI, and XIV with Figs. S22 to S24; (4) the 2023 surface-code
supplement (arXiv:2207.06431), Section XIV, the Pauli+ simulator
specification.

Answer these questions, in this order:

Instrument. Is the Pauli+ / qevol framing correct for this
circuit? What exactly must a reimplementation reproduce (leakage
labels, channel construction, measurement and reset rules for
leaked qubits) before its output means anything?

Baseline. The paper decodes its grafted data with a specific
decoder. Does the design pin the decoder and its configuration
tightly enough that the no-leakage arm can be checked against the
paper's simulated rate? If the decoder is not pinned, say what
happens to every later arm.

Confounds inside the comparison. The experiment post-selects on
preparation detectors and reports keep rates. Does the design
handle post-selection? How much of the sevenfold gap could be
decoder mismatch on leakage-correlated syndromes rather than
physical excess error, and what diagnostic separates the two?

Injection model. The design sweeps a per-cycle leakage generation
rate. Is that the right parameterization, or must injection be
per mechanism and per location (CZ |11> to |02>, heating,
transport, readout) as in the 2023 supplement? Does the sweep
need to be two-dimensional in generation and lifetime? Is the
reset rule for leaked measure qubits specified well enough to
fix the steady state?

Observables and criterion. The design requires one parameter
point to reproduce three observables jointly: the logical error
ratio, the S23 rise shape, and the S24 covariance structure. Are
these the right three? Is a fourth (for example the post-selection
keep rate) needed? The supplement states no uncertainties for
these observables: what comparison metric and what experimental
shot count make the pass/fail criterion operable? With at most
nine cycles, how much discriminating power does the S23 risetime
actually have?

Alternatives. Name any physical mechanism, other than leakage and
the readout path, that could reproduce the same three observables
in this simulation framework, and whether the design's arms would
distinguish it.

Feasibility. Are the shot counts and compute claims realistic for
the covariance observable? What is the cheapest version of this
experiment that still settles something?

Rules. Recompute any number you rely on; do not copy a headline
figure, including the "about seven times" (the underlying rates
are 5.3% and 0.8% per cycle in the supplement). Quote the source
for every factual claim about the papers, with section or figure.
Mark anything you cannot verify as unverified. Do not rewrite the
design; specify changes as instructions an implementer can follow.

Deliverable. A findings list, each finding tagged BLOCKER, MAJOR,
MINOR, or SOUND, in the order of the questions above, then a
one-paragraph verdict, exactly one of: READY TO BUILD, BUILD
AFTER FIXES (list them), or NOT SETTLING AS DESIGNED (say why).
Under 1,500 words.
