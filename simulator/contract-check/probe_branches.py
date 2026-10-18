"""Breaker probe 2: branch machinery edges.

- 2a: repeated magic injections on fresh qubits toward m_max=1000.
      2^n branches with equal |c|=2^-n/2; epsilon=1e-4 keeps all for
      n<=12 (2^12=4096, |c|=1/64=0.0156 > 1e-4). Does m_max truncation
      happen silently, and is the surviving state still normalized?
- 2b: coefficient normalization after many measurements (100 random
      Z measurements on an entangled 3-qubit state): sum|c|^2 must be 1.
- 2c: does truncation report anything to the caller?
"""
import math
import numpy as np

from leakage_hybrid import HybridSimulator, LeakageParams


def norm(sim):
    return sum(abs(b.coefficient) ** 2 for b in sim.branches)

print("== 2a: injections toward m_max ==")
rng = np.random.default_rng(21)
n = 11
sim = HybridSimulator(n, LeakageParams(enabled=False), rng)
for q in range(n):
    sim.inject_magic_state(q)
print(f"  {n} injections -> branch_count={sim.branch_count()} (raw 2^{n}={2**n}), m_max=1000")
print(f"  mixture norm after prune: {norm(sim):.12f}")
# how much mass was silently discarded?
expected_per = 2 ** (-n / 2)
print(f"  per-branch |c| = {expected_per:.6f} (>= epsilon 1e-4: all kept by epsilon)")
print(f"  truncated branches: {2**n - sim.branch_count()} of {2**n} = "
      f"{(2**n - sim.branch_count())/2**n*100:.1f}% of branches silently dropped")
# does the surviving truncated expansion still sample the right marginals?
ones = 0
T = 20000
rng2 = np.random.default_rng(22)
for _ in range(T):
    s2 = HybridSimulator(1, LeakageParams(enabled=False), rng2)
    s2.inject_magic_state(0)
    ones += s2.measure(0)
print(f"  single-qubit sanity after truncation test: P(1)={ones/T:.4f} (exact 0.5)")

print("== 2b: normalization after many measurements ==")
rng = np.random.default_rng(23)
sim = HybridSimulator(3, LeakageParams(enabled=False), rng)
for q in range(3):
    sim.inject_magic_state(q)
worst = 0.0
for _ in range(100):
    q = int(rng.integers(3))
    sim.measure(q)
    worst = max(worst, abs(norm(sim) - 1.0))
print(f"  max |sum|c|^2 - 1| over 100 measurements: {worst:.2e}")
print(f"  final branch count: {sim.branch_count()}")

print("== 2c: can the caller detect truncation? ==")
import inspect
src = inspect.getsource(type(sim)._prune)
print(f"  _prune emits warning/log/flag: {'warn' in src or 'log' in src or 'flag' in src}")
print("  (see source above for judgment)")
