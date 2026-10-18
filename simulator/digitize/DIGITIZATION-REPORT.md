# Digitization of the cultivation supplement's device figures (Figs. S5-S9)

Date: 2026-10-17. Source: Rosenfeld et al., "Magic state cultivation
on a superconducting quantum processor," supplement of
arXiv:2512.13908v1, Section V (PDF SHA-256
642ec2da74acd1b4df2a37985378dbbff69702b8c1314b7ad4e34ea1fcd5c43b).
Output: `device-values.json` (54 qubits x 15 quantities, 89 CZ
pairs x 2 quantities), built by `extract_figs.py` +
`build_device_table.py` in this directory. Page renders kept as
`page-11.png` to `page-14.png`.

## Verdict

The panels support full per-qubit digitization. Every value in
Figs. S5, S7, and S9 is printed as text inside its cell, so the
extraction reads the PDF's vector text layer positioned by cell
geometry. Nothing was estimated from color.

## What the figures hold

- Fig. S5 (p. 11): six lattice maps on device coordinates (rows
  3-11, columns 2-11): operating frequency, f10 - f21, maximum
  frequency, T1, T2 (CPMG), single-qubit gate error.
- Fig. S7 (p. 13): CZ interaction frequency and CZ error on
  diamond cells at edge midpoints, one per coupler.
- Fig. S9 (p. 14): nine lattice maps: bare resonator frequency,
  ringdown time, resonator-qubit coupling efficiency, measurement
  efficiency, qubit frequency during readout, readout pulse
  length, readout pulse power, maximum mean photon number,
  average readout error.
- Scope per the captions: the qubits and control parameters of
  the Fig. 4 grafting experiment (Section V text adds that the
  S9 parameters are taken from the Fig. 2 experiment). The maps
  are the 54-qubit patch, the largest lattice of the work.

## Validation

- All 15 square-lattice panels carry the identical set of 54
  (row, column) cells; both S7 panels carry the identical set of
  89 edge midpoints. Each cell holds exactly one printed value;
  the assignment (tick-label linear fits, robust to stray words)
  produced no collisions.
- The 89 S7 edges are exactly the nearest-neighbor adjacency of
  the 54 qubits, checked in both directions: every edge joins two
  patch qubits, and every adjacent qubit pair carries a value.
- Fig. S7 also prints a "0.00" string at every qubit site in both
  panels (54 per panel). These are excluded, on evidence: they
  sit exactly on sites rather than edge midpoints, they are
  identically "0.00", and 0.00 GHz is not a possible interaction
  frequency. They are a plotting artifact of the site grid, not
  data.
- Cross-check against the EDCF figures (S6, S8): the dashed
  median lines were read from the vector data through the axis
  tick fits (the method was verified on S8b, whose own curve
  crosses ECDF 0.47-0.53 at its dashed line). The EDCF medians do
  NOT all reproduce from the map values: T1 (88.9 vs map 89),
  f10 - f21 (195.2 vs 196), T2 (64.2 vs 64.5), maximum frequency
  (6.688 vs 6.725), and CZ interaction frequency (6.448 vs 6.45)
  agree within about 1%; operating frequency (6.553 vs map
  median 6.46, +1.4%) and CZ error (2.058 vs map 1.9, +8%) do
  not. Conclusion: the EDCFs were computed on a different sample
  than the maps (the supplement does not say which). For the
  Fig. 4 patch, the map values govern; do not quote the EDCF
  medians as patch medians.

## Extraction error

- Value reading: the text layer gives the printed digits exactly.
  The only error is the authors' print rounding, half a unit of
  the last printed digit: frequencies and resonator/readout
  quantities +/-0.005 of the printed unit (GHz, %, dBm as
  printed), T1/T2 and ringdown and pulse length +/-0.5 (us or
  ns), f10 - f21 +/-0.5 MHz, CZ error +/-0.05 x 10^-3 where two
  decimals are printed (a few cells print one decimal or a bare
  integer; there +/-0.5 of that digit), photon number +/-0.05.
- Cell assignment: zero residual error within the checks above.
  A misassignment would have to move a value to a neighboring
  cell while preserving the identical cell sets across 15 panels
  and the exact adjacency bijection in S7.
- The EDCF dashed-line readings carry the tick-fit error, about
  +/-0.01 GHz and +/-0.05 x 10^-3; this does not touch the map
  values.

## What the panels cannot give

- No per-qubit leakage quantity is plotted anywhere in Section V:
  no |2> population, no leakage generation or seepage rate per
  qubit. Gap 3's leakage inputs still rest on the literature
  band (McEwen 2021, Miao 2023). What the digitized table adds
  is the device's static variation (notably the per-pair CZ
  errors, median 1.9 x 10^-3 against the uniform SI1000
  p = 2.3 x 10^-3, and the per-qubit frequencies behind the
  supplement's readout-collision discussion).
- No measurement uncertainties for the individual values are
  published in the supplement.
- The key is the device coordinate (row, column). Mapping these
  onto a given Stim circuit's qubit indices requires the paper's
  explicit circuits (supplement Sec. VII, crumble links); the
  simulator's generated circuits have their own indexing, so the
  table is not yet wired into any run.
