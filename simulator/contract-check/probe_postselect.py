"""Breaker probe 5: post-selection edge.

Force zero kept shots in run_repetition_memory (postselect_first_cycle=True)
by hunting seeds with base_pauli_p=1.0 (every qubit gets a random Pauli
every cycle; a Y or Z on a measure qubit after the prep H deterministically
flips that check). Check what the function returns, and whether that
behavior is documented anywhere a user would see it.
"""
import math
import numpy as np

from leakage_hybrid import LeakageParams, run_repetition_memory

p = LeakageParams(enabled=False)
found = None
for seed in range(3000):
    r = run_repetition_memory(2, 3, p, 1, seed=seed,
                              postselect_first_cycle=True, base_pauli_p=1.0)
    if r["keep_rate"] == 0.0:
        found = seed
        break
print(f"seed forcing 0 kept shots (1 shot): {found}")
if found is not None:
    r = run_repetition_memory(2, 3, p, 1, seed=found,
                              postselect_first_cycle=True, base_pauli_p=1.0)
    print("returned dict:")
    print(f"  detection_fraction_per_cycle: {r['detection_fraction_per_cycle']}")
    print(f"  mean_label_population:        {r['mean_label_population']}")
    print(f"  keep_rate:                    {r['keep_rate']}")
    dets = r["detection_fraction_per_cycle"]
    print(f"  all-NaN detections: {all(math.isnan(x) for x in dets)}")
    print(f"  all-NaN populations: {all(math.isnan(x) for x in r['mean_label_population'])}")

# zero shots requested at all
try:
    r = run_repetition_memory(2, 3, p, 0, seed=1)
    print(f"shots=0 -> returned keep_rate={r['keep_rate']}")
except Exception as e:
    print(f"shots=0 -> {type(e).__name__}: {e}")

# documentation check: is the NaN behavior in the module docstring / README?
import inspect, leakage_hybrid
doc = inspect.getsource(leakage_hybrid.run_repetition_memory)
print(f"'NaN' mentioned in run_repetition_memory docstring: {'NaN' in doc}")
import pathlib
readme = pathlib.Path("README.md").read_text()
print(f"'NaN' mentioned in README: {'NaN' in readme}")
