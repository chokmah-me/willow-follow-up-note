"""Breaker probe 3: hostile inputs to the leakage engine and params.

For each hostile input, report LOUD (raised a clear exception) or
SILENT/DANGEROUS (accepted, or raised something cryptic/misleading).
"""
import math
import numpy as np

from leakage_hybrid import HybridSimulator, LeakageEngine, LeakageParams

rng = np.random.default_rng(31)

def attempt(name, fn):
    try:
        fn()
        print(f"  SILENT-ACCEPT: {name}")
        return "silent"
    except (ValueError, TypeError, IndexError, RuntimeError) as e:
        print(f"  LOUD: {name} -> {type(e).__name__}: {e}")
        return "loud"
    except Exception as e:
        print(f"  CRYPTIC: {name} -> {type(e).__name__}: {e}")
        return "cryptic"

print("== invalid params ==")
attempt("cz_leak_prob=1.5", lambda: LeakageParams(cz_leak_prob=1.5))
attempt("cz_leak_prob=-0.1", lambda: LeakageParams(cz_leak_prob=-0.1))
attempt("cz_leak_prob=nan", lambda: LeakageParams(cz_leak_prob=float('nan')))
attempt("transport_prob=inf", lambda: LeakageParams(transport_prob=float('inf')))
attempt("lifetime_cycles=0", lambda: LeakageParams(lifetime_cycles=0))
attempt("lifetime_cycles=-2", lambda: LeakageParams(lifetime_cycles=-2))
attempt("lifetime_cycles=nan", lambda: LeakageParams(lifetime_cycles=float('nan')))
attempt("heating_rate=-1", lambda: LeakageParams(heating_rate=-1))
attempt("epsilon=1.5", lambda: LeakageParams(epsilon=1.5))
attempt("m_max=0", lambda: LeakageParams(m_max=0))
attempt("m_max=2.5", lambda: LeakageParams(m_max=2.5))

print("== invalid engine construction / calls ==")
attempt("n_qubits=0", lambda: LeakageEngine(0, LeakageParams(), rng))
attempt("n_qubits=-3", lambda: LeakageEngine(-3, LeakageParams(), rng))
attempt("rng=None", lambda: LeakageEngine(2, LeakageParams(), None))
eng = LeakageEngine(2, LeakageParams(), rng)
attempt("cz same qubit", lambda: eng.cz(0, 0, higher_freq=0))
attempt("cz higher_freq not in pair", lambda: eng.cz(0, 1, higher_freq=7))
attempt("cz negative index", lambda: eng.cz(-1, 1, higher_freq=1))
attempt("cz index out of range", lambda: eng.cz(0, 5, higher_freq=0))
attempt("heat too many qubits", lambda: eng.heat(99))
attempt("heat negative", lambda: eng.heat(-1))
attempt("measure out of range", lambda: eng.measure(9))
attempt("reset out of range", lambda: eng.reset(-2))

print("== invalid simulator calls ==")
sim = HybridSimulator(2, LeakageParams(), rng)
attempt("depolarize p=2", lambda: sim.depolarize(0, 2.0))
attempt("depolarize p=-0.1", lambda: sim.depolarize(0, -0.1))
attempt("depolarize p=nan", lambda: sim.depolarize(0, float('nan')))
attempt("measure out of range", lambda: sim.measure(5))
sim2 = HybridSimulator(1, LeakageParams(), rng)
sim2.labels[0] = 2
attempt("inject_magic_state on leaked qubit", lambda: sim2.inject_magic_state(0))
sim3 = HybridSimulator(1, LeakageParams(), rng)
sim3.inject_magic_state(0)
attempt("inject_magic_state twice on same qubit", lambda: sim3.inject_magic_state(0))
attempt("x on bad index", lambda: sim.x(10))
