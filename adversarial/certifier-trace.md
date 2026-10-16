# Certifier trace: follow-up note draft vs the contract (sources)

Pass: contract-certifier, run by the main agent 2026-10-16.
Contract (trusted source of truth, in order): (1) cultivation paper
full text, /tmp/cultivation/paper.txt (arXiv:2512.13908v1; Science
DOI 10.1126/science.aee7961); (2) the Dec 2024 paper as read via
ResearchGate (DOI 10.13140/RG.2.2.30911.01443); (3) the held note's
pre-registered grades (cultivation-leakage-note.md).
Rule: one row per load-bearing claim; a claim with no source row does
not ship. Line numbers are for paper.txt unless marked RG (the
ResearchGate extraction).

## Decision table

| # | Draft claim | Source | Verdict |
|---|---|---|---|
| 1 | Factor 40 error cut, fidelity at least 0.9999(1), 8% retained | Abstract, paper.txt lines 9-10; Science abstract wording "at least" checked at science.org | PASS, draft uses Science wording and says so |
| 2 | Injection-only logical error 4.4(2)e-3, near physical gate errors | paper.txt line 299 | PASS |
| 3 | Cultivated full circuit logical error 1 to 2 e-4 | paper.txt line 359 | PASS |
| 4 | Kickback tomography: O(1e4) measurements vs O(1e8) standard, at epsilon near 1e-4 | paper.txt lines 281-285 | PASS |
| 5 | Removing QEC cycles makes the measurement circuit error about 100x worse | paper.txt line 359 | PASS |
| 6 | Grafting: d3 color to d5, 54 qubits, extension cycle plus N-1 cycles, Tesseract decoder | Fig. 4 caption and text, paper.txt lines 430-450 | PASS |
| 7 | Memory experiment: idled up to 9 cycles, SI1000 p = 2.3e-3 simulations | Supp. Sec. XIV, paper.txt lines 1941-1948; Fig. S23 caption (N = 9) line 2042 | PASS |
| 8 | LER about 7x higher than simulations in that experiment | paper.txt lines 1947-1948 | PASS, scope is the memory experiment, draft keeps that scope in Abstract and Sec. III.1 |
| 9 | Leakage likely the main source (authors' word) | paper.txt lines 1948-1950 | PASS, "likely" kept in Abstract, TL;DRs, Sec. III.1, Sec. VI |
| 10 | Signature 1: detection likelihood rises over time, in data not simulation (Fig. S23) | paper.txt lines 1949-1950; Fig. S23 caption line 2042 | PASS |
| 11 | Signature 2: detector covariance, time-correlated, propagates (Fig. S24) | paper.txt lines 1951-1952, 1984-1986; Fig. S24 caption line 2095 | PASS (source text itself mislabels this figure once as S22 at line 1983; the caption and first mention agree on S24; draft follows the caption) |
| 12 | Simulations do not include leakage | paper.txt lines 439, 1950, 1986, 2044 | PASS |
| 13 | Circuits did not contain leakage removal units | paper.txt lines 1987-1988 | PASS on fact; SCOPE FLAG: the sentence sits in Sec. XIV and speaks of "this experiment" (the grafted memory experiment). See Spec Gap G1 |
| 14 | Readout parameters not optimized for the redefined configuration; possible |2> frequency collisions, then leakage | paper.txt lines 1990-1992 | PASS |
| 15 | Main text keeps qubit performance variability open beside leakage | paper.txt lines 439-440 (Fig. 4 discussion) | PASS, draft states it |
| 16 | Non-physical norm in tomography, attributed to low-frequency phase noise | Supp. Sec. X.A, paper.txt lines 1442-1443 | PASS |
| 17 | Phase-noise sources: slow frequency drift, residual fields from control lines, Stark shifts via microwave crosstalk | paper.txt lines 1444-1446 | PASS |
| 18 | Without echos, performance dominated by low-frequency phase noise | paper.txt line 1555 (Fig. S15 text) | PASS |
| 19 | With echoing, detuning limit near 1e-5 infidelity, below measured; performance limited by gate error and decoherence | paper.txt lines 1556-1560 | PASS |
| 20 | Infidelity scales as p cubed; halving p gives bound near 2e-5 | paper.txt lines 482-484; scaling fit lines 1863, 1897 | PASS |
| 21 | RSA-2048 needs infidelity near 1e-10; some simulations need 1e-6 to 1e-8 | Introduction, paper.txt lines 84-90 approx. (see Sec. I text) | PASS |
| 22 | 2024 numbers: Lambda 2.14 +/- 0.02; logical error 0.143% +/- 0.003% per cycle; lifetime 2.4x; decoder latency 63 us | RG lines 111-119, 151-157 | PASS |
| 23 | 2024 error budget: incoherent about 80%, coherent about 10%, leakage about 10% | RG lines 519-521 | PASS |
| 24 | 14% simulated vs experimental discrepancy, attributed to excess correlations | RG lines 263-285 | PASS |
| 25 | Correlated bursts: 1e-10 floor, about once per hour, transient and catastrophic | RG lines 137-147 | PASS |
| 26 | 2024 required-for-fault-tolerance estimates: Lambda near 10, logical error 1e-6 or lower, distance 27, about 1500 qubits | RG lines 429-457 | PASS |
| 27 | 2024 challenge table grades: noise Partially, nonlinear Indirectly, reachability Indirectly, chaos Partially | RG lines 376-423 | PASS |
| 28 | 2024 channel table: leakage not explicitly modeled in Formula 77, mitigated by DQLR | RG lines 123-131, 361-362 | PASS |
| 29 | Gidney, Shutty, Jones cultivation proposal (2024), arXiv:2409.17595 | References, raw extraction of paper.txt ref [1] | PASS (a layout extraction shows a stray 2506.14688 from the facing column; the raw extraction confirms 2409.17595) |
| 30 | Hebrew date 5 Cheshvan 5787 for Oct 16, 2026 | Hebcal converter API, checked 2026-10-16 | PASS |
| 31 | Science DOI 10.1126/science.aee7961, First Release Oct 15, 2026 | Crossref + science.org search record | PASS |

## Spec gaps (adjudication queue, not silently resolved)

- G1 (scope, row 13): the draft's Sec. III.1 sentence "a new protocol
  omitted the channel from its simulations and omitted the removal
  step from its circuits" reads protocol-wide. The source sentence
  is scoped to the grafted memory experiment. Candidate fixes:
  (a) narrow to "the grafted-code circuits" (recommended);
  (b) keep and add a footnote. Awaiting breaker pass before editing,
  so both passes adjudicate the same text.
- G2 (source conflict, minor): the cultivation supplement's own text
  calls the covariance figure S24 at first mention and in its
  caption, but S22 once in running text. Draft follows the caption.
  No action unless the breaker flags it.
- G3 (narrative source): "diagnose over months" in Sec. III.2 rests
  on the Google blog narrative, not the paper. The blog is a listed
  reference. Candidate fix if flagged: drop the duration or mark it
  as the blog's account.
