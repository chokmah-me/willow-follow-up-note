# 2023 rise calibration, distance 3

Date: 2026-10-18. Run of the adopted rise leg in
`results/2023-signature-substitution.md` and
`results/section-v-simulation-design.md`: a 2023-style
memory experiment at literature leakage rates, scored
against the published distance-3 relative rise of 8% over
25 cycles (Google Quantum AI, arXiv:2207.06431, main text).
Machine record: `results/2023-rise-calibration.json`.
Nothing here was written into the note body.

## Verdict

Directional shape match, 8% point unresolved. On the
fixed 8-detector rounds, leakage on produces a slow rise
with risetime 6.5 cycles (of order 5). The full relative
rise from an exponential fit is 12.6%, inside the
provenance band 4.7% to 13.7% taken from the 2023
distance-5 Pauli+ vs experiment factor (12% / 7%). The
8% point sits about one rough standard error below that
fit. The leakage-off control is consistent with flat.
This is not a calibration stamp, and it is not a local
results artifact for the note.

Do not score the raw first-cycle to last-cycle ratio on
times 0 through 24. Time 0 has 4 detectors; later syndrome
rounds have 8. That mix produced 85% relative rise and is
not the 2023 observable.

## What was run

Hybrid runner in `simulator/` at repository head 3eb8e1f,
Python 3.12.13, stim 1.16.0, no Tesseract (detection
fractions only). Seed 20231018. 2000 shots per arm, about
32 ms/shot, 65 s per arm.

- Circuit: Stim `surface_code:rotated_memory_z`, distance
  3, 25 rounds, densely relabeled (17 qubits, 200
  detectors). SI1000-style stand-in p = 2.3e-3 on every
  generated noise knob (`graft_circuit.build_memory_circuit`).
- Leakage on: `LeakageParams()` defaults. CZ leak
  pt = 8e-4, heating 1/(700 us), t_cycle = 896 ns so
  p_heat = 0.001279 per cycle, lifetime 4.4 cycles so
  p_seep = 0.203, transport on, no removal, no readout
  leak.
- Leakage off: same seed, `enabled=False`.
- No first-round postselection.

Detector times 0 through 25. Time 0: 4 detectors (first
partial round). Times 1 through 24: 8 detectors each.
Time 25: 4 detectors (terminal data readout), dropped.
The 25-cycle request is times 0 through 24 as Stim lays
them out. The scored curve is times 1 through 24, the
longest stretch with a fixed detector set.

## Numbers, leakage on

Average detection, times 1 through 24:

- First round (t=1): 0.0377 (binomial SE 0.0015)
- Last round (t=24): 0.0482 (SE 0.0017)
- First-third mean (8 rounds): 0.0410
- Last-third mean (8 rounds): 0.0431
- First/last third relative rise: 5.3% (SE 2.0%)
- Exponential least-squares p(t) = a + b exp(-t/tau) on
  those 24 points: tau = 6.5 cycles, late level a =
  0.0438, t=0 offset a+b = 0.0389. Full relative rise
  (a - (a+b)) / (a+b) = 12.6%. Rough SE on that ratio
  4.6% (delta method using first-round SE for t0 and
  last-third SE for a; not a profile interval).
- |2>/|3> population, first round 0.10%, last round
  0.29%.

Leakage off, same metric: first/last third 2.2% (SE
2.2%), consistent with zero. Population 0.

## Score against 8%

The 2023 sentence is a relative rise of 8% over 25
cycles with risetime roughly 5 cycles. That is a full
early-to-late rise on one detector set, not a first/last
third. First/last third understates the rise when tau is
of order 8 cycles: the first third already contains most
of it. 5.3% is that biased-low proxy. The scored number
is the fit full rise, 12.6%.

- Point target: 8%. Measured 12.6%, about 1 SE above.
- Provenance band: 8% divided and multiplied by 12/7,
  i.e. 4.7% to 13.7%. 12.6% is inside, near the top.
- Risetime target: of order 5 cycles. 6.5 is inside a
  factor of two (2.5 to 10).
- Off arm: no significant rise. The on-arm shape is not
  a Stim-circuit transient shared by both arms.

Call: the instrument at these rates produces a leakage
rise of the published kind. It does not pin the 8%
point. A tighter interval needs more shots or a
bootstrap of kept detector events (not saved here).

## Why this is not yet a stamp

Absolute detection is about 4%. The 2023 distance-3
averages were 0.175 and 0.115 on weight-4 and weight-2
stabilizers. Relative 8% was defined on that higher
floor. This run used the cultivation SI1000 p = 2.3e-3
stand-in, not the 2023 Fig. 1c component errors.

Steady leaked population is 0.29% at cycle 25, below the
McEwen fitted band 0.97% to 1.30%. Literature generation
here is heating plus CZ Bernoulli at pt, not a
state-conditioned Kraus average. Less leaked population
is a reason to expect a smaller rise than the 2023
device, and also a reason the 12.6% can still sit near
the top of the band on a quieter baseline.

The 85% first-to-last ratio on times 0 through 24 is an
artifact of mixing a 4-detector first group with
8-detector later groups. Off-arm the same mix gives 46%.
Neither number is a score.

## Reproduce

From `simulator/`, with the venv that has stim and numpy:

```
python -c "from graft_circuit import build_memory_circuit; from hybrid_runner import run_circuit; from leakage_hybrid import LeakageParams; from dataclasses import replace; c=build_memory_circuit(3,25,0.0023); on=run_circuit(c, LeakageParams(), shots=2000, seed=20231018); off=run_circuit(c, replace(LeakageParams(), enabled=False), shots=2000, seed=20231018)"
```

Score detection_fraction_per_round[1:25] (times 1 through
24). Do not use index 0 or 25 for the 8% comparison.
