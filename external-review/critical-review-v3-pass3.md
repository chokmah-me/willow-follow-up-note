# Critical review, v3 draft, third pass (2026-10-18)

Target: `draft/follow-up-note-draft-v3.md` at commit 1fa5f0e.
Paper type: Empirical (secondary analysis of published data) plus a
pre-registered experimental design (Section V). Chokmah layer applied.
Line numbers refer to the draft at that commit.

Not run: the Kimi second pass (no OpenRouter access from this session),
and live reference checks (arXiv, Crossref and doi.org were blocked by the
session proxy). Reference findings below are from the reviewer's own
knowledge and are marked as such.

Compliance greps clean: no banned words, no em or en dashes, no non-ASCII
outside the Hebrew blocks, no banned paragraph openers, no "Deimos".
Hebrew date checked: 18 Oct 2026 is 7 Cheshvan 5787, so the date is right,
assuming the date is daytime (after sunset it is 8 Cheshvan).

---

## MUST-FIX

[Abstract, lines 29-31; Table 1 line 105; Sec. III.1 lines 243-248; Sec. III.5 lines 295-297]
The note contradicts itself on whether unoptimized readout and |2>
collisions are alternatives to leakage or the way leakage gets in. The
abstract calls them "other candidates", and Table 1 lists "a gap explained
by the unoptimized readout or by |2> collisions" as evidence against the
leakage row. But III.1 calls them "a path in ... with leakage after them",
and III.5 says the readout path "is part of the leakage score." A
falsification row can't count a mechanism against the claim when the text
elsewhere counts it as part of the claim.
Fix: Draw the causal graph once in III.1: (a) misconfigured readout or |2>
collision that causes leakage, which causes the gap; (b) misconfigured
readout that causes non-leakage errors, which cause the gap; (c) qubit
variability. Then rewrite Table 1's "counts against" cell and the abstract
so only (b) and (c) count against the claim.

[Sec. V, lines 415-456] The 2x2 design can't tell route (a) from route (b),
which is the question the leakage score depends on. Under (a), a readout-only
fix closes the gap and leakage is still the proximate cause. Outcome 2
("cause sits in the readout path ... inventory splits the channel") would
then score that as against leakage.
Fix: Make three-state readout (lines 375-378) a required measurement in all
four arms, not an optional cheaper check. Score outcome 2 by whether |2>
population falls along with the gap.

[Sec. V, lines 431-434] The success criterion "consistent with one within
the stated uncertainties" rewards a noisy run. A 9-cycle, single-configuration
d=5 rerun with wide error bars passes by default. That defeats the section's
stated purpose ("so the result cannot be read two ways", line 371).
Fix: State an equivalence margin, e.g. "ratio upper 95% bound below 1.5",
and a minimum shot count, or require the ratio's CI to exclude the v1 value
of about 6.6. Also say whether the removal-arm simulation includes the
removal-unit operations. Otherwise outcome 5 ("widens") can't be told apart
from outcome 4.

[Sec. V outcomes, lines 438-456] The outcomes aren't defined on the four
cells, and they aren't mutually exclusive. Outcome 3 assigns the residual to
"unoptimized readout calibration" even though one arm already re-optimizes
readout. The both-fixes arm is never mentioned.
Fix: Replace the bullets with a 4-cell outcome table (removal x readout ->
gap closed / partial / unchanged / widened), with one pre-assigned reading
for each pattern.

[Table 1 line 105; Sec. I lines 119-120; Abstract; Conclusion lines 493-494]
"No leakage removal units in the circuit" is listed as evidence for the
claim, and the score is said to "rest on" it. Missing mitigation is a
precondition for leakage to matter. It doesn't discriminate between leakage
and the alternatives. Combined with the admission that a gap is "close to
guaranteed" (line 116), only the two signatures carry evidential weight.
Fix: Move "no removal units" out of "counts for" and into a precondition
line. Restate the basis as "rests on the Fig. S23 and S24 signatures" in the
abstract, Sec. I and the Conclusion.

[Abstract line 22] "switching a distance-3 color code into a distance-5
surface code" contradicts Sec. II (lines 137-138, 183-185): the target is a
"surface-code-compatible encoding" that "mixes color-code and surface-code
stabilizers" and "is not matchable." The abstract's wording also hides why
Tesseract matters in the decoder-mismatch caveat.
Fix: "grafting a distance-3 color code into a distance-5 grafted code that
mixes color-code and surface-code stabilizers." Re-sync the abstract field
in `search-meta-v3.html`.

[Sec. II lines 130-132; Sec. VI; reference 2] Every scored number comes from
arXiv v1 (Dec 2025). The Science version came out Oct 15, 2026, and its
supplement was not checked. If Section XIV, Fig. S22's LER labels, or the
"likely" wording changed in review, the central score is built on a
superseded text. Disclosing this doesn't fix it: the published supplement is
available, and checking it is a bounded task.
Fix: Diff Section XIV, Figs. S14c, S22-S24 and the
data-availability line against the Science supplement before release. Then
either drop the v1 qualifiers or list each difference.

[Chokmah C4; header line 12; Availability lines 501-504] There is no Zenodo
DOI, and the only availability URL points to a private repository (fails
item 14).
Fix: Mint the Zenodo record (note plus review files plus simulator) and put
the DOI in the header, the Availability section and the SEARCH-META. Make the
repository public or drop the URL until it is.

---

## SHOULD-FIX

[Table 2, lines 353-365] The table defines "Evidence added" as "yes only
when the cultivation paper tests that 2024 objection," then marks yes on a
row it says "is not a 2024 objection." The table breaks its own definition.
Fix: Take the echo/kickback row out of Table 2 and move it to the
measurement-story subsection, or rename the column.

[Table 2 caption, lines 345-351] The author grades their own 2024 note from
a ResearchGate text scrape and says the column layout couldn't be recovered.
Fix: Take the grades from the author's source file of [1]. Cut the scrape
narrative from the caption.

[Table 1 / Sec. III] No single place lists the six 2026 verdicts. The reader
has to put them together from six subsections.
Fix: Add a "2026 verdict" column to Table 1, or a six-row summary at the top
of Sec. III.

[Sec. II lines 176-182] LER values (5.3%, 0.8%) have no unit (per cycle?
cumulative at 9 cycles?) and no uncertainty. The 0.8% has one significant
figure, so 5.3/0.8 spans about 6.2 to 7.1 from rounding alone.
Fix: State the unit as Fig. S22 defines it, and give the ratio as a range
("6 to 7").

[Sec. II lines 196-200] The "halving the noise gives about 2e-5" projection
is the author's extrapolation of the p-cubed scaling at fixed small
distance. Neither the paper nor [3] claims it.
Fix: Label it "my extrapolation, fixed distance 3, assuming the p-cubed fit
holds", or cut it. The five- and six-order comparisons stand without it.

[Sec. III.4 lines 287-289] "Injection-only error close to the physical gate
error rate" has no source. 4.4e-3 against SI1000 p = 2.3e-3 is a factor of
about 2.
Fix: Cite the v1 sentence that makes the comparison, or state the two
numbers and drop "close."

[Sec. I lines 68-83] The Willow figures (0.143% plus or minus 0.003%,
Lambda 2.14, 2.4x, 63 us, the 80/10/10 budget, the 14% discrepancy, the 1e-10
burst floor about once an hour) are cited only to [1]. They are Google's
numbers.
Fix: Add [4] after each figure, or once per sentence.

[Sec. V lines 380-386] The proposed outside check rests on reference [14],
which the author says "I have not read." The text also says to inject
leakage "at measured rates," but no grafted-circuit rates exist. The only
rates the note names are 2023 averages from a different processor.
Fix: Read [14] or drop the method claim. Name the leakage-rate source
explicitly (2023 [12]), and say the rerun is therefore an order-of-magnitude
check, not a reproduction.

[Sec. V lines 424-426] Freezing p on "the kickback-tomography circuit of
Fig. 3" calibrates on a postselected circuit (8% retention). The fitted p
then depends on the postselection rule.
Fix: Freeze p on an unpostselected memory circuit on the same qubits and the
same day. Keep Fig. 3 as a cross-check.

[Undefined acronyms and symbols, item 16 / item 12] SI1000 (line 171),
Pauli+ (line 394), DQLR (line 240), LER (line 179), qevol (line 170) and
Tesseract (line 185) are all undefined or uncited. N (line 408) is never
defined: cycle count? injection rounds? p is defined only implicitly as the
SI1000 strength.
Fix: Expand each on first use. Cite SI1000 (Gidney, Newman, Fowler,
Broughton, Quantum 5, 605, 2021), the Tesseract decoder paper, and Miao et
al. 2023 (Nature Physics) for DQLR. Define N and p in Sec. II.

[Abstract lines 28-29] "leakage is absent from the model and the circuits"
reads as if leakage physically doesn't happen in the circuits.
Fix: "leakage is absent from the simulation, and the circuits have no
leakage removal units."

[Abstract, TL;DR, Sec. I, Sec. VI, Conclusion] The same sentences repeat word
for word: "weak evidence on its own" / "rests on the signatures" appear 4
times, and the variability-on-the-earlier-figure caveat 5 times. That is
aphoristic repetition, not emphasis. The abstract is a 250-word run of
staccato verdicts and never states the contribution.
Fix: Keep each caveat once in the abstract and once in its home section.
Cut the TL;DR to about 80 words. Open the abstract with the contribution:
"This note scores ... and pre-registers the removal experiment that would
settle it."

[Abstract last line vs. "likely hit"] "The 2024 inventory is not confirmed"
next to "likely hit" leaves the reader unsure what a hit licenses. Lines
89-93 concede that Google's own budget already carried leakage.
Fix: One sentence saying what a hit means here: a model that omits the
channel mispredicts hardware by a named factor, attributed by the
experimenters. It does not mean the 2024 note found something Google didn't
know.

[Chokmah C5; AI statement lines 506-525] The in-paper statement differs from
`AI-USE-STATEMENT.md`, which says it is a copy. The paper drops the Grok
version (4.6), the Kimi K3 and Claude Opus 5.5 external evaluators, and the
d=3 calibration line. "Muse (model version not recorded)" also fails
"models named."
Fix: Re-copy the repo statement into the paper verbatim. Record the Muse
model identifier if it can be recovered. Otherwise keep the disclaimer.

[Ref. 4] Nature vol. 638 is the 2025 volume: online Dec. 9, 2024, print
Feb. 2025. (Reviewer knowledge; Crossref was unreachable.)
Fix: "vol. 638, pp. 920-926, 2025 (published online Dec. 2024)."

[Ref. 8] The first author is Börner. The ASCII "Boerner" is fine under house
style, but the reference list should match the arXiv record.
Fix: Use "S.-D. Boerner (Börner)" once in the reference entry, or confirm
the ASCII form is intentional.

[Process log vs. draft] `process-log.md` (2026-10-18 entry) says
"Limitations names the local simulator and d=3 calibration as not a result."
Sec. VI no longer does, and the AI statement says the note "reports no
output from that simulator."
Fix: Either restore the Limitations line or correct the process log.

---

## SEARCH-META

`draft/search-meta-v3.html` is already filled correctly from the current
draft. Two changes are needed once the MUST-FIX items land: re-sync the
`abstract` / `DC.description` fields (the "distance-5 surface code" wording),
and replace the three DOI PLACEHOLDERs and the two URL PLACEHOLDERs once the
Zenodo record exists. The block below is the current file with the abstract
corrected for the grafted-code wording only.

```html
<!-- SEARCH-META: paste into HTML <head> of landing page -->

<!-- 1. JSON-LD: Google, Bing, Semantic Scholar -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "name": "Willow, Tested Again: Magic-State Cultivation Against the 2024 Error-Channel Inventory",
  "abstract": "The 2024 note on Google's Willow surface-code paper inventoried six error channels. Four were omitted or treated thinly by the simplified noise model: leakage, crosstalk, correlated errors, and classical chaos. Gate and readout sat inside that model as the baseline. In October 2026 Google published magic-state cultivation on Willow, grafting a distance-3 color code into a distance-5 code that mixes color-code and surface-code stabilizers. This note scores that experiment against the six channels. Supplement claims are from arXiv preprint v1. Leakage is a likely hit (attributed, not ablated). In the supplement's grafted-code memory experiment, the authors name population leakage as the likely main cause of a logical error rate about seven times the simulation. Two leakage signatures are in the data, the simulation omits leakage, the circuits have no leakage removal units, and no removal run exists. Crosstalk is mentioned. Correlated errors are present in the detector data and are not scored on their own. Gate and readout remain the baseline. Classical chaos is untested. The 2024 inventory is not confirmed.",
  "author": {
    "@type": "Person",
    "name": "Daniyel Yaacov Bilar",
    "identifier": "https://orcid.org/0000-0002-9040-6914",
    "affiliation": {
      "@type": "Organization",
      "name": "Chokmah LLC"
    }
  },
  "datePublished": "2026-10-18",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "identifier": {
    "@type": "PropertyValue",
    "propertyID": "DOI",
    "value": "PLACEHOLDER"
  },
  "keywords": ["Google Willow", "magic state cultivation", "quantum error correction", "leakage", "surface code", "color code", "kickback tomography", "error channels"],
  "isPartOf": {
    "@type": "DataCatalog",
    "name": "Zenodo"
  }
}
</script>

<!-- 2. Dublin Core: OAI-PMH harvesters, institutional repositories -->
<meta name="DC.title"        content="Willow, Tested Again: Magic-State Cultivation Against the 2024 Error-Channel Inventory" />
<meta name="DC.creator"      content="Bilar, Daniyel Yaacov" />
<meta name="DC.subject"      content="Google Willow; magic state cultivation; quantum error correction; leakage; surface code; color code; kickback tomography; error channels" />
<meta name="DC.description"  content="A follow-up to Notes on Google Willow (2024) that scores the 2026 magic-state cultivation experiment, as read in arXiv preprint v1, against the 2024 six-channel inventory. Leakage is a likely hit (attributed, not ablated), resting on two detector signatures. The note pre-registers the removal experiment that would settle it." />
<meta name="DC.date"         content="2026-10-18" />
<meta name="DC.type"         content="Text" />
<meta name="DC.format"       content="text/html" />
<meta name="DC.identifier"   content="https://doi.org/PLACEHOLDER" />
<meta name="DC.rights"       content="https://creativecommons.org/licenses/by/4.0/" />

<!-- 3. citation_* tags: Google Scholar -->
<meta name="citation_title"             content="Willow, Tested Again: Magic-State Cultivation Against the 2024 Error-Channel Inventory" />
<meta name="citation_author"            content="Bilar, Daniyel Yaacov" />
<meta name="citation_publication_date"  content="2026-10-18" />
<meta name="citation_abstract_html_url" content="PLACEHOLDER" />
<meta name="citation_doi"               content="PLACEHOLDER" />
<meta name="citation_keywords"          content="Google Willow; magic state cultivation; quantum error correction; leakage; surface code; color code; kickback tomography; error channels" />
<meta name="citation_pdf_url"           content="PLACEHOLDER" />
```
