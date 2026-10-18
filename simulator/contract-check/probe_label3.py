"""Breaker probe 7: label 3 creation.

Is there ANY mechanism in the code that can create label 3, or can it
only arrive via direct label injection (as the shipped tests do)?
Also check what the brief specifies about |3> creation.
"""
import inspect
import numpy as np
import leakage_hybrid
from leakage_hybrid import LeakageEngine, LeakageParams

src = inspect.getsource(leakage_hybrid)
import re
creations = re.findall(r"labels\[.*?\] = (\d)", src)
print(f"all literal label assignments in module: {set(creations)}")

# runtime: run every creation-capable method at prob=1.0 and watch for 3s
rng = np.random.default_rng(71)
p = LeakageParams(cz_leak_prob=1.0, readout_leak_prob=1.0,
                  transport_prob=1.0, heating_rate=1e9, t_cycle=1.0)
e = LeakageEngine(4, p, rng)
for _ in range(300):
    e.heat(4)
    e.cz(0, 1, higher_freq=0)
    e.measure(2)
    e.seep_cycle()
print(f"labels after 300 maxed cycles: {sorted(set(e.labels.tolist()))} (any 3? {3 in e.labels})")

# brief check
brief = open("ASTRA-BRIEF.md").read()
mentions = [l.strip() for l in brief.splitlines() if "|3>" in l]
print(f"\nbrief lines mentioning |3>: {len(mentions)}")
for m in mentions:
    print("  -", m[:160])
print("\nbrief specifies a |3> CREATION mechanism (generation rate):",
      any("creat" in l.lower() or "generat" in l.lower() for l in mentions))
