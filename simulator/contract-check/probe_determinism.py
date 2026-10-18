"""Breaker probe 6: determinism across separate processes.

Run the same seeded experiment in two independent subprocesses and
compare the full returned dicts. Also compare a HybridSimulator-level
sequence across processes.
"""
import json
import subprocess
import sys

SNIPPET = """
import json, numpy as np
from dataclasses import replace
from leakage_hybrid import LeakageParams, HybridSimulator, run_repetition_memory
p = LeakageParams()
r = run_repetition_memory(3, 10, p, 60, seed=4242, postselect_first_cycle=True)
rng = np.random.default_rng(4242)
s = HybridSimulator(2, p, rng)
s.inject_magic_state(0)
s.cx(0, 1)
outcomes = [s.measure(0), s.measure(1)]
labels = s.labels.tolist()
branches = s.branch_count()
norm = sum(abs(b.coefficient)**2 for b in s.branches)
print(json.dumps({"runner": r, "outcomes": outcomes, "labels": labels,
                  "branches": branches, "norm": norm}))
"""

outs = []
for i in range(2):
    proc = subprocess.run([sys.executable, "-c", SNIPPET], capture_output=True,
                          text=True, cwd=".", timeout=300)
    if proc.returncode != 0:
        print("SUBPROCESS FAILED:", proc.stderr[-2000:])
        raise SystemExit(1)
    outs.append(proc.stdout.strip())
print("process 1 == process 2:", outs[0] == outs[1])
if outs[0] != outs[1]:
    a, b = json.loads(outs[0]), json.loads(outs[1])
    print("differing keys:")
    for k in a:
        if a[k] != b[k]:
            print(f"  {k}: {a[k]} != {b[k]}")
