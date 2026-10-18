"""Certifier probes: brief criteria NOT covered by the shipped tests.
Run: .venv/bin/python contract-check/certifier-probes.py
Each probe prints PASS/FAIL with its criterion id."""
import json, math, subprocess, sys
import numpy as np
sys.path.insert(0, "/home/hatch/workspace/willow-leakage-sim")
from dataclasses import replace
from leakage_hybrid import HybridSimulator, LeakageEngine, LeakageParams, run_repetition_memory

results = []
def probe(cid, fn):
    try:
        fn(); results.append((cid, "PASS", ""))
    except Exception as e:
        results.append((cid, "FAIL", f"{type(e).__name__}: {e}"))

def expect(exc, fn):
    try:
        fn()
    except exc:
        return
    raise AssertionError(f"expected {exc.__name__}")

# C1 defaults
def c1():
    p = LeakageParams()
    assert p.cz_leak_prob == 8e-4 and p.t_cycle == 896e-9 and p.lifetime_cycles == 4.4
    assert p.epsilon == 1e-4 and p.m_max == 1000 and p.readout_leak_prob == 0.0
    assert p.transport_prob == 0.1 and p.leaked_partner_z_prob == 1.0 and p.removal_boost == 5.0
    assert abs(p.heating_rate - 1/700e-6) < 1e-6
probe("C1 param defaults", c1)

# C2 formulas
def c2():
    p = LeakageParams()
    assert abs(p.p_heat - (1 - math.exp(-(1/700e-6) * 896e-9))) < 1e-12
    assert abs(p.p_seep - (1 - math.exp(-1/4.4))) < 1e-12
    pr = replace(p, removal_on=True)
    assert abs(pr.p_seep - min(1.0, p.p_seep * 5.0)) < 1e-12
probe("C2 p_heat/p_seep formulas + removal boost", c2)

# C10/C18 switches
def c18a():
    p = LeakageParams(heating_on=False, t_cycle=1.0)  # p_heat ~ 1 if on
    e = LeakageEngine(64, p, np.random.default_rng(1))
    for _ in range(50): e.heat(64)
    assert np.all(e.labels == 0)
def c18b():
    p = LeakageParams(cz_leak_on=False, cz_leak_prob=1.0, heating_on=False)
    e = LeakageEngine(2, p, np.random.default_rng(2))
    for _ in range(50): e.cz(0, 1, higher_freq=0)
    assert np.all(e.labels == 0)
def c18c():
    p = LeakageParams(readout_leak_on=False, readout_leak_prob=1.0)
    s = HybridSimulator(1, p, np.random.default_rng(3))
    assert s.measure(0) == 0 and s.labels[0] == 0
probe("C18 heating_on=False kills heating", c18a)
probe("C18 cz_leak_on=False kills CZ creation", c18b)
probe("C18 readout_leak_on=False kills readout leakage", c18c)

# C11 inject raises
def c11a():
    s = HybridSimulator(1, LeakageParams(), np.random.default_rng(4))
    s.labels[0] = 2
    expect(ValueError, lambda: s.inject_magic_state(0))
def c11b():
    s = HybridSimulator(1, LeakageParams(), np.random.default_rng(5))
    s.x(0)
    expect(ValueError, lambda: s.inject_magic_state(0))
probe("C11 inject into leaked qubit raises ValueError", c11a)
probe("C11 inject into non-|0> target raises ValueError", c11b)

# C13 depolarize validation + effect
def c13():
    s = HybridSimulator(1, LeakageParams(), np.random.default_rng(6))
    expect(ValueError, lambda: s.depolarize(0, 1.5))
    expect(ValueError, lambda: s.depolarize(0, -0.1))
    s.depolarize(0, 0.0)
    assert s.branches[0].tableau.peek_z(0) == 1
probe("C13 depolarize validates p, p=0 is a no-op", c13)

# C15 epsilon + m_max pruning
def c15a():
    p = LeakageParams(epsilon=0.8)  # above 1/sqrt(2), so both |T> branches fall under the cutoff
    s = HybridSimulator(1, p, np.random.default_rng(7))
    expect(RuntimeError, lambda: s.inject_magic_state(0))
def c15b():
    p = LeakageParams(m_max=2)
    s = HybridSimulator(2, p, np.random.default_rng(8))
    s.inject_magic_state(0); s.inject_magic_state(1)
    assert s.branch_count() == 2
    assert abs(sum(abs(b.coefficient) ** 2 for b in s.branches) - 1.0) < 1e-9
probe("C15 epsilon cutoff fails loud (RuntimeError) when all mass pruned", c15a)
probe("C15 m_max truncates branches and renormalizes", c15b)

# C17 validation error types
def c17():
    expect(ValueError, lambda: LeakageParams(cz_leak_prob=1.5))
    expect(ValueError, lambda: LeakageParams(lifetime_cycles=0))
    expect(ValueError, lambda: LeakageParams(m_max=0))
    e = LeakageEngine(2, LeakageParams(), np.random.default_rng(9))
    expect(IndexError, lambda: e.is_leaked(5))
    expect(ValueError, lambda: e.cz(0, 1, higher_freq=7))
    expect(ValueError, lambda: run_repetition_memory(1, 5, LeakageParams(), 10, seed=1))
    expect(ValueError, lambda: run_repetition_memory(3, 5, LeakageParams(), 10, seed=1, base_pauli_p=2.0))
probe("C17 hostile constructor/index/arg inputs raise the named errors", c17)

# C12 Clifford agreement with a Stim reference on stabilizer states
def c12():
    import stim
    rng = np.random.default_rng(10)
    gates1 = ["x", "y", "z", "h", "s"]
    for trial in range(30):
        s = HybridSimulator(3, LeakageParams(enabled=False), np.random.default_rng(100 + trial))
        ref = stim.TableauSimulator(seed=1); ref.set_num_qubits(3)
        for _ in range(25):
            g = gates1[int(rng.integers(5))]; q = int(rng.integers(3))
            getattr(s, g)(q); getattr(ref, g)(q)
            if rng.random() < 0.4:
                a, b = int(rng.integers(3)), int(rng.integers(3))
                if a != b:
                    s.cx(a, b); ref.cx(a, b)
        t = s.branches[0].tableau
        for q in range(3):
            assert t.peek_x(q) == ref.peek_x(q) and t.peek_y(q) == ref.peek_y(q) and t.peek_z(q) == ref.peek_z(q)
probe("C12 Clifford+CX evolution matches Stim reference (30 random circuits)", c12)

# C16 zero-kept-shots behavior (seed scan, bounded)
def c16():
    p = LeakageParams()
    found = None
    for seed in range(60):
        r = run_repetition_memory(8, 3, p, 20, seed=seed, postselect_first_cycle=True, base_pauli_p=1.0)
        if r["keep_rate"] == 0.0:
            found = r; break
    assert found is not None, "no zero-kept seed found in scan"
    assert all(math.isnan(v) for v in found["detection_fraction_per_cycle"])
probe("C16 zero kept shots returns NaN lists, keep_rate 0 (docstring-documented)", c16)

# C19 determinism across processes
def c19():
    code = ("import sys, json; sys.path.insert(0, '/home/hatch/workspace/willow-leakage-sim');"
            "from leakage_hybrid import LeakageParams, run_repetition_memory;"
            "print(json.dumps(run_repetition_memory(3, 8, LeakageParams(), 30, seed=777)))")
    outs = []
    for _ in range(2):
        r = subprocess.run(["/home/hatch/workspace/willow-leakage-sim/.venv/bin/python", "-c", code],
                           capture_output=True, text=True, timeout=120)
        assert r.returncode == 0, r.stderr[-300:]
        outs.append(r.stdout.strip())
    assert outs[0] == outs[1]
probe("C19 identical results across separate processes", c19)

for cid, status, note in results:
    print(f"{status}  {cid}" + (f"  -- {note}" if note else ""))
print(f"\n{sum(1 for _, s, _ in results if s == 'PASS')}/{len(results)} certifier probes pass")
