# Open-source tools for the Section V leakage re-simulation

Checked 2026-10-16 against GitHub, PyPI, and papers. Search
only. Nothing was installed or run. Companion to
`results/section-v-simulation-design.md` (the design said
"No open-source Pauli+ implementation was found") and
`results/external-sme-review-simulation-design.md`.

## Verdict

That design sentence is too strong. Stim alone still cannot
carry leakage (Gidney, Quantum Computing Stack Exchange, 2023).
Two open-source leakage-aware Clifford simulators exist. The
paper's decoder is public. Google's **qevol** (cultivation SI
XI B), the engine behind Fig. S22(e), is still unpublished.

## Tools

**leaky** (`pip install leakysim`).
https://github.com/inmzhang/leaky
README: "An implementation of Google's Pauli+ simulator."
Leakage labels, `LeakyPauliChannel`, `generalized_pauli_twirling`
from Kraus operators, readout as 0/1 or raw 2/3. Built on
`stim.TableauSimulator`. Archived 18 Aug 2026; the archive
points at deltakit-stim. Clifford only: no T gates, so no
logical |T> and no S22(e) as published.

**deltakit-stim**.
https://github.com/Deltakit/deltakit-stim
Live Stim fork (updated 7 Oct 2026). `LEAKAGE(p)`, spread on
CZ/CX/CY, `HERALD_LEAKAGE_EVENT`, leakage reset `RL`. Apache-2.0.
Phenomenological leak/sealed bit plus transport, not the 2023
GPC-from-Kraus construction. Fast Clifford sampling.

**tesseract-decoder**.
https://github.com/quantumlib/tesseract-decoder
The cultivation paper's decoder (arXiv:2503.10988, footnote 1).
Apache-2.0. Color-code and surface-code tests. Stim DEM in.
Does not generate leakage shots.

**tsim** (QuEra, `pip install bloqade-tsim`).
https://github.com/QuEraComputing/tsim
Clifford+T, Stim API, 80+ qubits. Docs do not describe a
leakage model.

**qsim / Stim**.
qsim is a state-vector engine; 54 qubits is 2^54. Vanilla Stim
has no leakage states.

**qevol**.
Named in cultivation SI XI B as the restricted-rank trajectory
simulator used for the grafted memory experiment. No public
repository under that name was found.

## What an outside group can do with public tools

Clifford idle of the grafted geometry, with 2023-style GPCs
(leaky, unmaintained) or phenomenological leakage
(deltakit-stim), decoded with public Tesseract: S23/S24-class
syndromes, and an LER on a stabilizer state. That is the cheap
arm in the SME review.

They cannot reproduce the published |T> memory LER of 0.8% per
cycle without a qevol-class engine: tableau plus a coefficient
list for T, plus leakage GPCs. That hybrid is still not a
download.
