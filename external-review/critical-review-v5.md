# Critical review, v5 draft (2026-10-18)

Target: `draft/follow-up-note-draft-v5.md` at commit 218f757 (main).
Paper type: Empirical (secondary reading of published data) plus a
pre-registered experimental design. Chokmah layer applied. Line
numbers refer to the draft at that commit.

The reviewer also wrote v5, so this pass is adversarial on its own
restructuring. Source claims were checked against the local
`sources/cultivation-arxiv-2512.13908.txt`. Not run: the Kimi second
pass (no OpenRouter access) and live reference checks (Crossref and
Zenodo were blocked by the session proxy).

Compliance greps are clean: no banned words, no em or en dashes, no
non-ASCII outside the Hebrew blocks, and no banned paragraph openers.
The abstract is 220 words. The Hebrew date and ORCID are correct.

---

## MUST-FIX

[Sec. II, lines 120-142; Table 1; Abstract lines 24-27] Routes (b)
and (c) are presented as live alternatives without checking them
against the two signatures that the attribution rests on.
Readout-assignment errors are independent from shot to shot and from
cycle to cycle. They predict neither the slow rise in detection
likelihood (Fig. S23) nor time-correlated covariance spreading across
the grid (Fig. S24). Static qubit variability raises error rates, but
it does not make them grow over the circuit. Decoder or model mismatch
changes the LER ratio, but S23 and S24 are detector-level and don't
depend on the decoder. As written, the note understates how much the
signatures already discriminate, and it treats (b) as on a par with
(a).
Fix: Add a short table or paragraph in Sec. II with one row per
route, giving what each predicts for the gap, the S23 rise, and the
S24 covariance. State that (b), (c), and mismatch can explain the
magnitude of the gap but would each need a second mechanism to
explain the signatures. Adjust the abstract's "two others that would
[refute leakage]" to "two others that would, if they also explained
the signatures."

[Sec. IV rule 1 vs. rule 3, lines 205-222] The rules contradict each
other. Rule 1 re-freezes p from a new same-day control, so the
baseline arm B need not reproduce the v1 ratio of about 7. Rule 3
nonetheless defines "unchanged" as overlapping the v1 range of 6.2 to
7.1, and "widened" as above 7.1. If the new p comes out higher (for
example, because the control memory circuit also leaks), B itself
could read as "narrowed" and nothing would have been fixed. The
shot-count rule ("plus or minus 1 at a ratio of 7") has the same
dependence on v1.
Fix: Define every reading relative to arm B in the same run. For
example: unchanged when an arm's 95% interval overlaps B's; widened
when its lower bound exceeds B's upper bound; closed stays an
absolute upper bound below 2. Also require B to show a gap, e.g. a
lower bound above 3, for the run to count. Size the shots at B's
observed ratio, not at 7.

[Sec. I lines 101-105] "A gap between hardware and a depolarizing
simulation in a first grafted-code memory run is also expected on
general grounds" has no support, and the paper contradicts it. The
main text reports Fig. 2 "in approximate agreement with state vector
simulations" (source line 379) and Fig. 3 "in agreement" (line 617).
Fig. S21 shows "qualitative agreement" at the same p = 2.3e-3 (line
3098). The non-grafted circuits match SI1000, which makes the grafted
gap more informative, not less.
Fix: Replace the sentence with the contrast: "The non-grafted
circuits in Figs. 2, 3, and S21 agree with SI1000 at the same p, so
the gap is specific to the grafted memory run." Keep "The attribution
rests on the two signatures."

[Chokmah C4; header line 9; Availability] There is still no Zenodo
DOI, and the availability statement names no working URL (item 14).
Fix: Mint the record and put the DOI in the header, Availability, and
SEARCH-META before release.

---

## SHOULD-FIX

[Sec. IV lines 190-200] "Cycle-resolved |2> population" overstates
what three-state readout gives. Measure qubits are read every cycle.
Data qubits are read only at the end of the circuit, so leakage on
data qubits shows up mid-circuit only indirectly, through the
neighbouring measure qubits.
Fix: Say "cycle-resolved |2> population on measure qubits, and final
|2> population on data qubits". Apply the rule-4 criterion to both.

[Sec. IV line 190] "Uses the existing Willow processor" has no source.
Fix: Cite prior three-state readout on Google hardware: McEwen et al.
[9] and Miao et al. [7] both resolve |2>.

[Sec. V line 291] "halving p would give 1e-5 to 2.5e-5" does not
follow: 1e-4/8 = 1.25e-5.
Fix: "about 1.3e-5 to 2.5e-5".

[Sec. VI line 307] "reachability deficits" is the only objection in
the list without a citation.
Fix: Cite Akshay et al. (the 2020 reachability-deficits paper on
QAOA, as cited in [13]), or write "reachability deficits (Akshay et
al., as cited in [13])".

[Sec. I line 68] "used for all of the paper's Pauli-noise
simulations" is broader than needed. Some simulations add coherent
noise on top of SI1000 (source lines 2554, 2570).
Fix: "used throughout the paper's simulations, sometimes with added
coherent noise".

[Availability, line 341] "The scoring worksheet" refers to the
scoring frame that v5 dropped.
Fix: "The source pins, review files, and local simulator ...".

[Abstract lines 22-34] The abstract lists three contributions, but
Sec. V (numbers to cite with care) is a fourth, and it is what
citing readers will use.
Fix: Add one clause: "and a list of figures that are easy to quote
out of their conditions."

[Table 1 row 1] "L and RL closed; R not closed" reads as "leakage
confirmed" with no comment. Under route (a) the readout fix should
also close the gap, so this pattern means leakage enters by some
path other than the one the authors named.
Fix: "Leakage confirmed by removal; its entry is not the readout path
Section XIV names."

[Sec. II line 117-118] "a reader who lists 'unoptimized readout' as a
rival explanation has misread it" is accurate, but it reads as a dig.
Earlier versions of this note made that misreading.
Fix: "Listing unoptimized readout as a rival explanation misreads
it."

[Title] "What Would Confirm" leaves out that the same design can
refute the attribution, and three rows of Table 1 do exactly that.
Fix: Consider "What Would Settle the Leakage Attribution in
Magic-State Cultivation on Willow".

---

## SEARCH-META

`draft/search-meta-v5.html` is correctly filled from the current
draft: title, abstract, date, keywords, and license. The DOI,
`citation_abstract_html_url`, and `citation_pdf_url` stay PLACEHOLDER
until the Zenodo record exists. Re-sync the abstract field if the
MUST-FIX abstract change lands, and the title fields if the title
changes. No other edits are needed.
