# External SME review of the Section V simulation design

Pass against `results/external-sme-review-instructions.md`.
Design, note v3 I/III.1/V, arXiv:2512.13908v1 V/XI/XIV (S22–S24),
arXiv:2207.06431 XIV. Nothing run. Unverified items marked.

Fig. S22 captions: experimental LER 5.3% per cycle, SI1000
simulation 0.8% per cycle. Ratio 5.3/0.8 = 6.625. That is the
supplement's "about seven times" (XIV, after S21).

## Findings

**1. Instrument. BLOCKER.** qevol and Pauli+ are different
machines; this circuit needs both.

Cultivation SI XI B: qevol is "an extension of the Pauli+
simulator (described in ref. [44]) that maintains superpositions
of stabilizer states," used because T gates are non-Clifford. XIV
injects at theta = pi/4, cultivates |T>, grafts, idles N cycles;
simulations are "qevol, with a simple depolarizing noise model,
SI1000, p = 2.3e-3." XI B is a Gottesman tableau plus complex
coefficients. It specifies no leakage labels, GP channels, or
leaked-qubit measure/reset.

2023 SI XIV B.2: Pauli+ carries a leakage label in {c, 2, 3} and
an m-qubit stabilizer state on the computational subset.
Operations are Clifford, computational-basis measurement, reset
to |0>, and a Generalized Pauli channel. That object cannot
represent logical |T>. A 2023-faithful Pauli+ run cannot
reproduce S22(e). A XI-B-faithful qevol run has no leakage.

Implementer, before any leakage arm:

1. Keep qevol's coefficient list for the cultivation T gates.
2. Attach the 2023 leakage-label vector and GPC map (XIV B.2,
   XIV B.3) to every noisy gate.
3. Measure leaked devices as in 2023 XIV A.2: hardware does not
   distinguish |2> and |3>; map both to 0 or 1 with equal
   probability, then pass binary syndromes to the decoder. A
   third outcome changes the decoder's alphabet.
4. Write the leaked-measure reset rule. 2023 XIV B.2 reset on a
   leaked device sets the label to c and adds a sigma_z
   generator: every measure qubit un-leaks every cycle, S23's
   rise is then a data-qubit effect. Leaving |2> in place gives
   a different steady state. The design names neither rule.

Also specify the 2023 CZ leakage channel, not "transport on":
after each CZ, K1 = sqrt(pt)(|02><11| + |11><02|), pt = 8e-4,
higher-frequency qubit only (XIV A.3); leaked-partner CZs apply
conditional Z plus transport |22> <-> |13| and |21> <-> |03|.

Marshall and Kafri (cultivation [38]) justify twirling, not
qevol. Unverified that internal qevol already carries GPCs.

**2. Baseline / decoder. BLOCKER.** The design says "same
decoder" and does not name it.

Main text, grafting paragraph: "we decode the resulting data with
Tesseract, a most likely error decoder using the A* search
technique [39]" (arXiv:2503.10988). SI1000 is Gidney et al.,
Quantum 5, 605 (2021), ref. [37]. S22(e) is the 0.8% no-leakage
simulated LER. The SI never writes "S22(e) was decoded with
Tesseract." That is the natural reading, and it is unverified.

Implementer: decode every arm with Tesseract; freeze beam,
timeout, hypergraph, and priors to the paper's, or publish the
S22(e) values; Arm 1 passes only if fitted LER per cycle equals
0.8% to within S22(e)'s fit residual. If Arm 1 misses 0.8%,
later ratios are not 6.625.

An unpinned decoder makes 6.625 decoder-dependent. Leakage
yields time-correlated syndromes; MLE with independent SI1000
priors will mis-correct some of them.

**3. Confounds / post-selection. MAJOR.** The design is silent
on post-selection.

Main text: "For consistency with Figs. 2 and 3, we post select
for no detection events on the state preparation detectors
before grafting." S22(c, f) plot those keep rates versus angle.
Prep cuts sit before idle, so idle leakage should not move keep
rate with N. The same paragraph records a 10% retainment
difference between N = 2 and N = 3 around theta = pi/4, assigned
to flux transients or calibration drift: a time-dependent
confound on this circuit family.

Implementer: apply the same prep-detector cut to every shot;
report keep rate versus N as a fourth observable; require Arm 1
to match S22(f) as well as 0.8%.

Decoder-versus-physics diagnostic: score S23 and S24 on the raw
detector record; score LER after Tesseract. Signatures match and
LER misses: decoder mismatch. LER matches and signatures miss:
not S23/S24 leakage. Fraction of 6.625 that is decoder mismatch:
unverified.

**4. Injection model. MAJOR.** A single per-cycle generation
rate is the wrong parameter.

2023 XIV A.3 names heating Gamma_1->2 = 1/(700 us), CZ |11> <->
|02| at pt = 8e-4, crosstalk leakage, plus transport and
conditional Z. Spatial fingerprints differ. A homogeneous |2>
draw can raise LER and slope S23; it is a weak way to get S24
bleeding, which XIV attributes to leakage that "can propagate
across the qubit grid" (covariance paragraph; figure is S24).
The criterion asks for a (generation, decay) pair; Arm 2 fixes
decay at 4.4 cycles. Those sentences disagree.

McEwen 0.09 to 0.11% per cycle, Miao 4.4-cycle lifetime, Miao
DQLR |2> under 1e-3 in two cycles: cited from papers not in the
bundle. Unverified here.

Implementer: inject the 2023 mechanisms separately, with a
homogeneous per-cycle rate only as a nested comparison; sweep
generation and lifetime on a 2-D grid, or replace the product
with a measured |2> population (note Section V, three-state
readout); write the leaked-measure reset rule so the steady
state is determined. Arm 3 stays a family of curves.

**5. Observables and criterion. MAJOR.** The three observables
are the right core set. The pass/fail line is not operable.

S22 captions give 5.3% and 0.8% with no uncertainties, no shot
counts, no fit covariance. S23: heatmaps, "slow increase ... for
some detectors," no numeric rise. S24: covariance plots. The SI
paragraph describing bleeding mislabels the figure as "Fig. S22,
left/right." Use S24.

"Within the paper's stated uncertainties" has no referent.
Replace it with: (a) fitted LER per cycle on the S22(b, e) N
grid; Arm 1 = 0.8%; leakage arm = 5.3% to a stated relative
tolerance (20% until fit errors exist, about 5.3 plus or minus
1.1); (b) S23 mean detection fraction versus cycle on the
detectors that rise in the experimental panel, positive slope
and 1/e time within a factor of two of the injected lifetime;
(c) S24 class-level (same-stabilizer time correlations; off-grid
boxes with x != y), not Frobenius distance on the full spacetime
matrix; (d) keep rate versus N.

S23 power at N <= 9: 2023 main text, 12% relative rise over 25
cycles at distance 5, risetime "roughly 5 cycles," Pauli+
simulated rise 7% over 25 rounds. If tau = 5, 1 - exp(-9/5) =
0.83 of the approach to steady state occurs inside nine cycles
(0.993 at 25). The shape is visible. S23 quotes no amplitude, so
a 7% versus 12% test cannot be run on these figures.

**6. Alternatives. MAJOR.** A time-correlated Pauli channel with
4-to-5-cycle memory (drift, flux transients, a phenomenological
hook) can raise LER, slope S23, and darken time-adjacent
covariance cells. The main text already offers qubit-performance
variability on the earlier grafting figure, and flux transients
or drift for the 10% retainment-versus-N effect. Stray CZ
interactions are the 2023 alternative for a larger
detection-probability rise at distance 5 (paragraph after the
12% rise). None of those injects |2>, so none produces leakage
transport across the grid. Arm 2 with transport off versus on
discriminates S24 bleeding; the design leaves transport on in
every leakage arm. Add a transport-off control. Arm 4 is a
hardware prediction, not a discriminator among simulation
alternatives.

**7. Feasibility. MINOR on shots; BLOCKER on the
reimplementation story.**

2023: 25-cycle, 50,000-repetition dataset for detection
correlations (Fig. 2 caption region). 100k shots per point is
enough for the LER fit: at 0.8% per cycle, nine-cycle cumulative
error is 1 - (0.992)^9 = 0.0696; binomial se at 100k is about
8e-4. For S24, 100k is enough at class level (finding 5c).
Full-matrix distance on O(30) detectors times 9 cycles burns
shots on the wrong metric. "Hours to a day" assumes a Pauli+
reimplementation the published record does not contain (finding
1). Building qevol-plus-GPC from XI B plus 2023 XIV is a
project, not a day of sampling.

Cheapest version that still settles something: (1) Arm 1 only,
Tesseract frozen, prep post-selection on: hit 0.8% and S22(f) or
stop; (2) syndrome-only Clifford idle of the grafted geometry,
2023 mechanisms, transport on/off: can match or fail S23/S24
without |T>, and does not settle 6.625; (3) one leakage point at
the 2023 CZ and heating numbers, scored on the four observables.
Three-state |2> readout on the grafted circuit (note Section V)
collapses generation times lifetime and is cheaper than any
sweep.

**SOUND.** Joint three-observable test and Arm 1 as a sanity
gate are the right ideas. A joint match shows sufficiency. The
2x2 hardware rerun remains the attribution experiment.

## Verdict

**BUILD AFTER FIXES.** Pin Tesseract so Arm 1 must hit 0.8% per
cycle; specify the qevol-plus-GPC hybrid, the leaked-measure map
to {0,1}, and the leaked reset rule; inject 2023 mechanisms with
a transport-off control; add prep post-selection and keep rate
versus N; replace "stated uncertainties" with the tolerances in
finding 5. Until those are written, a run of this file cannot be
checked against S22 to S24, and a miss can always be blamed on
the decoder, the reset, or the injection parameterization.
