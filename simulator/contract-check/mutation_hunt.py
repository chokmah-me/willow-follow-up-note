"""Breaker probe 8: mutation testing of the shipped test suite.

Copy leakage_hybrid.py into contract-check, apply ONE mutation per copy,
run the SHIPPED tests against the mutant. If the suite still passes, the
behavior is untested: a real regression there would ship silently.

M1: HybridSimulator.cz always applies the ideal tableau CZ, even when a
    qubit is leaked (drops the leaked-partner replacement).
M2: _project_mixture drops the likelihood reweighting of coefficients.
M3: leaked-qubit measurement always returns 0 (not a fair coin).
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
original = (ROOT / "leakage_hybrid.py").read_text()

MUTANTS = {
    "M1_ideal_cz_when_leaked": (
        "        errors = self.engine.cz(i, j, higher_freq)\n"
        "        if computational:\n"
        "            for branch in self.branches:\n"
        "                branch.tableau.cz(i, j)",
        "        errors = self.engine.cz(i, j, higher_freq)\n"
        "        for branch in self.branches:\n"
        "            branch.tableau.cz(i, j)",
    ),
    "M2_no_likelihood_reweight": (
        "            branch.coefficient *= math.sqrt(float(likelihood))",
        "            pass  # MUTANT: skip likelihood reweighting",
    ),
    "M3_leaked_measure_always_zero": (
        "            return int(self.rng.integers(2))",
        "            return 0  # MUTANT: leaked readout always 0",
    ),
}

import shutil
shutil.copy(ROOT / "test_leakage_hybrid.py", HERE / "mut_test_leakage_hybrid.py")
for name, (old, new) in MUTANTS.items():
    assert original.count(old) == 1, f"mutation anchor not unique for {name}"
    mutant = original.replace(old, new)
    # mutant must import as `leakage_hybrid`, the name the tests use
    (HERE / "leakage_hybrid.py").write_text(mutant)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(HERE / "mut_test_leakage_hybrid.py"),
         "-q", "-p", "no:cacheprovider"],
        capture_output=True, text=True, cwd=str(HERE), timeout=300,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": str(HERE)},
    )
    tail = proc.stdout.strip().splitlines()[-3:]
    print(f"{name}: exit={proc.returncode} :: {' | '.join(tail)}")
    if proc.returncode != 0:
        print("   (suite caught the mutation)")
(HERE / "leakage_hybrid.py").unlink(missing_ok=True)
(HERE / "mut_test_leakage_hybrid.py").unlink(missing_ok=True)
