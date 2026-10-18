"""Breaker probe 4: the switches.

4a. enabled=False: engine must be an exact no-op AND must not consume
    RNG draws. Test every path: engine methods directly, and
    HybridSimulator.measure / reset_after_measure / depolarize with
    leakage off (the shipped test only covers engine methods).
4b. Each mechanism switch off must fully disable its mechanism:
    heating_on, cz_leak_on, transport_on, readout_leak_on, removal_on.
"""
import numpy as np

from leakage_hybrid import HybridSimulator, LeakageEngine, LeakageParams


def rng_state(rng):
    return rng.bit_generator.state  # full state dict, as the shipped test does

print("== 4a: RNG untouched with enabled=False ==")
p_off = LeakageParams(enabled=False)
paths = {}
# engine methods
rng = np.random.default_rng(41)
e = LeakageEngine(4, p_off, rng)
before = rng_state(rng)
e.heat(4); e.cz(0, 1, higher_freq=0); e.measure(0); e.reset(0); e.seep_cycle()
paths['engine methods'] = (rng_state(rng) == before)

# HybridSimulator.measure on computational qubit (legit measurement sampling)
rng = np.random.default_rng(42)
s = HybridSimulator(2, p_off, rng)
before = rng_state(rng)
m = s.measure(0)
paths['sim.measure (computational)'] = (rng_state(rng) == before)
print(f"  sim.measure returned {m}; RNG untouched: {paths['sim.measure (computational)']} "
      "(note: measurement sampling SHOULD draw)")

# HybridSimulator.measure on a leaked-looking label while disabled:
# labels are forced 0 by disabled engine; is_leaked False -> tableau path.
rng = np.random.default_rng(43)
s = HybridSimulator(2, p_off, rng)
s.engine.labels[0] = 2   # hostile direct injection; engine disabled
paths['is_leaked(0) with enabled=False'] = (not s.engine.is_leaked(0))
before = rng_state(rng)
s.measure(0)
paths['sim.measure after hostile label (disabled)'] = (rng_state(rng) == before)

# depolarize with leakage off: Pauli baseline hook still draws/applies
rng = np.random.default_rng(44)
s = HybridSimulator(2, p_off, rng)
before = rng_state(rng)
s.depolarize(0, 1.0)
paths['sim.depolarize draws when disabled'] = (rng_state(rng) != before)
tab_before = None  # tableau check: did a Pauli get applied?
print(f"  sim.depolarize(p=1.0) with enabled=False draws RNG: "
      f"{paths['sim.depolarize draws when disabled']} (baseline Pauli hook, not leakage)")

# reset_after_measure with leakage off
rng = np.random.default_rng(45)
s = HybridSimulator(2, p_off, rng)
before = rng_state(rng)
s.reset_after_measure(0)
paths['sim.reset_after_measure draws (projection sampling)'] = (rng_state(rng) != before)
print(f"  reset_after_measure draws RNG (mixture projection sampling): "
      f"{paths['sim.reset_after_measure draws (projection sampling)']}")

print()
print("== 4b: each mechanism switch off ==")
def labels_after(fn, params, seed=46):
    rng = np.random.default_rng(seed)
    out = fn(LeakageEngine(3, params, rng), rng)
    return out

# heating_on=False: no labels ever become 2 from heat
rng = np.random.default_rng(47)
e = LeakageEngine(8, LeakageParams(heating_on=False), rng)
for _ in range(500):
    e.heat(8)
print(f"  heating_on=False -> any leaked after 500 heat cycles: {bool((e.labels != 0).any())}")

# cz_leak_on=False: CZ never creates a label
rng = np.random.default_rng(48)
e = LeakageEngine(2, LeakageParams(cz_leak_prob=1.0, cz_leak_on=False), rng)
for _ in range(500):
    e.cz(0, 1, higher_freq=0)
print(f"  cz_leak_on=False (prob=1.0) -> any leaked after 500 CZs: {bool((e.labels != 0).any())}")

# transport_on=False with prob=1: label never moves
rng = np.random.default_rng(49)
e = LeakageEngine(2, LeakageParams(transport_on=False, transport_prob=1.0), rng)
e.labels[0] = 2
moved = False
for _ in range(200):
    e.cz(0, 1, higher_freq=0)
    if e.labels[1] != 0:
        moved = True
print(f"  transport_on=False (prob=1.0) -> label ever moved: {moved}")

# readout_leak_on=False with prob=1: measure never leaks
rng = np.random.default_rng(50)
e = LeakageEngine(2, LeakageParams(readout_leak_on=False, readout_leak_prob=1.0), rng)
for _ in range(500):
    e.measure(0)
print(f"  readout_leak_on=False (prob=1.0) -> leaked after 500 measures: {bool((e.labels != 0).any())}")

# removal_on=False: seepage uses unboosted rate only
rng = np.random.default_rng(51)
e = LeakageEngine(4096, LeakageParams(removal_on=False, removal_boost=100.0), rng)
e.labels[:] = 2
e.seep_cycle()
frac = float(np.mean(e.labels == 0))
expected = 1 - np.exp(-1 / 4.4)
print(f"  removal_on=False (boost=100) -> seeped fraction {frac:.4f} vs unboosted {expected:.4f}")

# removal_on=True actually boosts
rng = np.random.default_rng(52)
e = LeakageEngine(4096, LeakageParams(removal_on=True, removal_boost=100.0), rng)
e.labels[:] = 2
e.seep_cycle()
frac = float(np.mean(e.labels == 0))
print(f"  removal_on=True (boost=100) -> seeped fraction {frac:.4f} (clipped at 1.0)")

# heating_on=False + cz_leak_on=False + readout_leak_on=False + transport irrelevant:
# with seepage present, pre-seeded labels decay; nothing new appears
rng = np.random.default_rng(53)
e = LeakageEngine(2, LeakageParams(heating_on=False, cz_leak_on=False,
                                  readout_leak_on=False, transport_on=False), rng)
for _ in range(300):
    e.heat(2); e.cz(0, 1, higher_freq=0); e.measure(0)
print(f"  all creation switches off -> labels stay 0: {bool((e.labels == 0).all())}")
