"""Breaker probe 1: measurement correctness against exact numpy statevectors.

Three cases, true probabilities computed here from the statevector,
never copied from anywhere:
  (a) |T> then H then Z measurement:  P(1) = |<1|H|T>|^2
  (b) |T> then Z measurement:         P(1) = 1/2
  (c) |T> on q0, CX(q0->q1), Z q0:    P(1) = 1/2, joint P(00)=P(11)=1/2
All leakage disabled (enabled=False) so this probes the qevol branch
machinery alone. N=40000 trials each; report sim rate, exact rate, delta.
"""
import math
import numpy as np

from leakage_hybrid import HybridSimulator, LeakageParams

PHASE = np.exp(1j * np.pi / 4)

def state_T():
    return np.array([1.0, PHASE]) / math.sqrt(2)

def apply_H(psi):
    H = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    return H @ psi

N = 40000

# ---------- (a) T, then H, then Z ----------
t = state_T()
ht = apply_H(t)
exact_a = abs(ht[1]) ** 2          # |<1|H|T>|^2
print(f"(a) exact P(Z=1) after H on |T>: {exact_a:.6f}  (= (2-sqrt2)/4 = {(2-math.sqrt(2))/4:.6f})")

rng = np.random.default_rng(11)
ones = 0
for _ in range(N):
    sim = HybridSimulator(1, LeakageParams(enabled=False), rng)
    sim.inject_magic_state(0)
    sim.h(0)
    ones += sim.measure(0)
rate_a = ones / N
print(f"(a) sim    P(Z=1) after H on |T>: {rate_a:.6f}  delta={rate_a-exact_a:+.6f}")

# ---------- (b) T, then Z (no H) ----------
exact_b = 0.5
rng = np.random.default_rng(12)
ones = 0
for _ in range(N):
    sim = HybridSimulator(1, LeakageParams(enabled=False), rng)
    sim.inject_magic_state(0)
    ones += sim.measure(0)
rate_b = ones / N
print(f"(b) exact P(Z=1) on |T>:      {exact_b:.6f}")
print(f"(b) sim    P(Z=1) on |T>:      {rate_b:.6f}  delta={rate_b-exact_b:+.6f}")

# ---------- (c) entangled: T on q0, CX 0->1, measure Z q0, then Z q1 ----------
# exact state (|00> + e^{i pi/4} |11>)/sqrt2
rng = np.random.default_rng(13)
ones0 = ones1 = both11 = 0
n = 0
for _ in range(N):
    sim = HybridSimulator(2, LeakageParams(enabled=False), rng)
    sim.inject_magic_state(0)
    sim.cx(0, 1)
    m0 = sim.measure(0)
    m1 = sim.measure(1)
    ones0 += m0; ones1 += m1; both11 += (m0 and m1)
    n += 1
print(f"(c) exact: P(q0=1)=0.5, P(q1=1)=0.5, P(11)=0.5, P(00)=0.5")
print(f"(c) sim:   P(q0=1)={ones0/n:.6f} P(q1=1)={ones1/n:.6f} P(11)={both11/n:.6f}")

# also: measure q1 first, then q0 (order independence of the joint)
rng = np.random.default_rng(14)
mism = 0
for _ in range(N):
    sim = HybridSimulator(2, LeakageParams(enabled=False), rng)
    sim.inject_magic_state(0)
    sim.cx(0, 1)
    m1 = sim.measure(1)
    m0 = sim.measure(0)
    if m0 != m1:
        mism += 1
print(f"(c2) sim: fraction of shots where q0 != q1 (exact: 0.0): {mism/N:.6f}")
