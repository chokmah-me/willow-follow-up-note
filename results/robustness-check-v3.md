# Robustness check: Willow, Tested Again (v3)

Skill: paper-robustness-check (local-paper-robustness-check),
own-draft mode. Object under test:
`draft/follow-up-note-draft-v3.md` at repository head 5b632ef,
SHA-256
b2cbdc025910bfd36475bb1085eb636f9f52ed47cc4b894a611179768f191d25
(455 lines, 3,703 words), read in full before the surface was
drawn. The v2 check (`robustness-check-v2.md`, 18 rows) is the
baseline; v3 changed the claim surface itself (40x stated as a
range, one TL;DR, preprint-v1 labeling, DQLR identity claim
withdrawn, Akshay row dropped, Gidney [13] added), so a fresh
surface was drawn rather than the v2 surface re-run.

Perturbation surface, FROZEN 2026-10-16 15:20 EDT, before any
perturbation was run. 16 rows, 3 claims. Axes: rc =
recomputation, sens = sensitivity, diag = diagnostic,
quote = misquotation, explore = scope probe. Attacks against
the note's scoring (T1), not against Rosenfeld et al.'s
experiment itself (T3, out of scope here). One flip threshold:
a claim flips when the perturbation makes its stated
conclusion false, not weaker.

## Claims

- C1. The leakage score: a likely hit, attributed and not
  ablated, for the roughly sevenfold gap, with variability
  open. (Abstract, Layman TL;DR, Sections I, III.1, V,
  Conclusion.)
- C2. The channel accounting: six channels scored once each,
  phase noise filed outside the channels, one likely hit, the
  other five at mentioned, present but not independent,
  baseline, baseline, untested. (Sections I, III, IV.)
- C3. The distance arithmetic: the 40x stated as a 22 to 44
  range from v1's own endpoints with "about 40" labeled the
  paper's headline; about five orders to the cited 1e-10, six
  from the measured value. (Sections I, II, Conclusion.)

## Frozen rows

| # | Axis | Claim | Perturbation |
|---|------|-------|--------------|
| 1 | rc | C1 | The 7x is a ratio of unstated absolute rates; halve it and double it |
| 2 | diag | C1 | Removal rerun run, gap unchanged (the draft's own withdrawal case) |
| 3 | sens | C1 | Delete "likely" from the summaries only |
| 4 | sens | C1 | Variability, not leakage, is the main cause |
| 5 | sens | C1 | The simulations included leakage after all (counterfactual) |
| 6 | rc | C3 | Recompute orders to the 1e-10 target from the projected bound near 2e-5 |
| 7 | rc | C3 | Recompute orders from the measured cultivated error, 1e-4 to 2e-4 |
| 8 | rc/quote | C3 | The 40x: check every place v3 states it (Sections II, III.4, Conclusion), not only the qualified one |
| 9 | sens | C1 | DQLR and leakage removal units: same mechanism, or different; run the identity both ways |
| 10 | diag | C2 | Fig. S24 covariance scored to both leakage and correlated |
| 11 | diag | C2 | Phase noise read as a seventh channel, or as correlated corroboration; check against Table 1 giving the noise row "evidence added: yes" |
| 12 | explore | C2 | The Akshay row is gone: what scoring, if any, did the note lose |
| 13 | rc | C3/C1 | Preprint v1 versus the published Science version: if the supplement numbers move between versions, what happens to the scores |
| 14 | quote | C1 | A one-line quotation taken from the single Layman TL;DR alone |
| 15 | quote | C2 | "Nothing contradicted" quoted alone as a vindication of the 2024 note |
| 16 | sens | C2 | The echoed detuning bound near 1e-5 read as the correlated channel's score |

## Run log (2026-10-16)

1. The gap survives at 3.5x and at 14x as an unexplained gap
   against a model that omits a named channel. The score does
   not use the precision of 7. Survives.
2. The flip case, unchanged from v2 and still the draft's own:
   Section V pre-scores it ("the gap does not move in any arm
   ... this note's leakage score must be withdrawn"), and
   Section I's counts-against column now names it in advance
   ("a removal run that leaves the gap"). No other single
   observation flips C1. Keystone, team's run only.
3. Not run as an edit. v2 result stands and v3's text confirms
   the dependence: "likely" appears in the abstract, the TL;DR,
   III.1's header, and the conclusion. Remove it and C1 flips
   to demonstrated-by-implication. The word is load-bearing.
4. Variability as main cause: C1 weakens to "signature-supported
   candidate." The draft files this in advance in the Section I
   table ("a gap fully explained by variability" counts
   against). Survives as scored; the ranking is conceded-open.
5. Counterfactual premise, same as v2: the paper's supplement
   states the simulations exclude leakage (independently
   confirmed in the v1 trace). If they included it, C1 falls.
   Conditional on a stated premise, premise verified.
6. log10(2e-5 / 1e-10) = 5.30, recomputed 2026-10-16. v3:
   "about five orders." Survives.
7. log10(1e-4 / 1e-10) = 6.00 and log10(2e-4 / 1e-10) = 6.30,
   recomputed. v3: "six orders from the value actually
   measured." Survives at both ends.
8. Section II states the range and labels the headline
   correctly (4.4(2)e-3 / 2e-4 = 22.0 and / 1e-4 = 44.0,
   recomputed). The conclusion calls it "the factor-of-40
   headline" and separates it from the memory measurement.
   But Section III.4 says flatly "the 40-fold improvement is
   measured from an injection-only error," with no range and
   no label. One unqualified body mention, in the channel
   chapter, not in any summary. WEAKENS C3 mildly: a reader
   quoting III.4 alone gets the headline the draft elsewhere
   corrects. This is the one v2 weakening that survives into
   v3 in reduced form. A one-line fix exists (range or
   "headline" label at III.4); not applied, author's call.
9. v3 withdraws the identity claim the v2 check weakened on:
   "I do not treat those two names as the same mechanism
   here." Run both ways, the score no longer depends on it.
   Survives, and the v2 weakening is closed.
10. Not double-counted. III.3 scores the covariance as leakage
    propagation and refuses the independent correlated score
    in terms. The Section I map files the same evidence once.
    Survives.
11. v3's narrower filing holds under the read. The measurement
    story is headed "(not a channel)," the text states the
    note "does not widen that channel to include it," and
    Table 1's evidence-added "yes" sits on the noise-sensitivity
    objection row, whose caption defines the term to include a
    point for the simplified model; it is not a channel score.
    Consistent. Survives. (v2 filed this evidence as a
    correlated hit; v3's filing is the correction, and it costs
    the thesis a point rather than gaining one.)
12. Scope probe, not a fragility. The reachability objection
    (2e-5 bound against the 1e-10 RSA figure) is no longer a
    scored table row; the arithmetic remains in Section II,
    now cited to Gidney [13] instead of floating. C2 loses a
    row of coverage and gains a sourced number. No flip.
13. Version drift is v3's declared exposure, labeled in the
    abstract ("in preprint v1"), Section II ("I did not
    page-diff that file against the published Science
    supplement"), Limitations, and the AI statement. Every
    scored number is a v1 number and says so. If the Science
    supplement moves a scored number, the affected score is a
    v1 score and must be re-run; the draft's labeling makes
    that a bounded repair, not a silent error. Survives as
    scoped, with the exposure named rather than hidden.
14. The single TL;DR carries the full hedge set ("likely
    explanation," the second cause in plain words, "They did
    not run the removal step"), plus the scale ("one
    configuration, up to nine cycles"), and it never uses the
    40. Quoted alone it does not flip C1. Survives. Note the
    concentration effect: v3 has one summary surface where v1
    and v2 had three, so this one paragraph now carries the
    whole summary risk; it passes, and there is no second
    surface to catch a future careless edit.
15. Resisted by the sentence itself: the abstract pairs
    "Nothing in the 2024 note is contradicted" with "The
    inventory is not confirmed by it" in adjacent sentences,
    and the conclusion repeats the score as "one likely hit."
    A vindication quote must cut the pair apart. Survives.
16. The symmetry holds. The bound is scored three times in
    v3, always against the thesis: the measurement story ("a
    point for the simplified model on that measurement. It is
    not a score of the 2024 correlated channel"), Table 1's
    separate row, and the Section I map, which files the
    correlated channel's counts-against as hardware matching
    the omitting model. Survives.

## Verdict

C1 and C2 survive all 16 rows. C3 survives as corrected in
Section II and the conclusion, with one mild weakening carried
in reduced form: the unqualified "40-fold" at Section III.4
(row 8). Two v2 findings are closed outright: the 40x range is
now the draft's own text (rows 6 to 8 against the v2 surface),
and the DQLR identity dependence is withdrawn (row 9). The
phase-noise filing moved from a v2 scoring choice to an
explicit, argued refusal in v3, and it costs the thesis a
point (row 11).

Conditional flips, both unchanged and both named by the draft
itself: the removal rerun leaving the gap unchanged (row 2),
and the word "likely" (row 3).

Keystones, restated for v3:
1. The word "likely," now carried by one TL;DR instead of
   three summaries. Fewer surfaces, same keystone, higher
   concentration.
2. The Section V removal rerun, which only the cultivation
   team can run.

Files: this check ran on the v3 text at head 5b632ef, frozen
2026-10-16 15:20 EDT before running. Companion receipt from
the same day: `integrity_brief_v3.md` (scan fail on the
deferred ResearchGate identifier only, I1 limited advise-only).
This check does not mark the note scientifically verified.
