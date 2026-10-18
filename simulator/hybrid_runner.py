"""Shot-by-shot Stim interpreter using the unchanged v0 hybrid engine.

Source: Section V simulation design, 2026-10-16. Noise is sampled separately
per stabilizer branch; leakage labels are shared across branches, as in v0.
This inherits v0's surrogate-state and mixture-measurement approximations.
It is not a decoder, a calibrated device prediction, or a simulation of
cultivation. Observable results are raw annotated measurement parities.

Timing convention (revised by the main agent, 2026-10-17, after the
first delivered version heated at every TICK): generated surface-code
circuits have multiple TICKs per syndrome round (7 per round at both
distances tested), so heating at every TICK would apply the per-cycle
heating hazard several times per cycle. Heating and seepage are
per-cycle processes. This runner therefore groups TICKs into rounds:
the number of rounds is the number of distinct detector time
coordinates minus one (the last group is the terminal data-readout
detectors), and heat + seep + a population sample happen once per
round, at the round's first TICK. The phase within the round is a
modeling convention, stated here rather than hidden.
mean_label_population_per_round has one entry per round;
detection_fraction_per_round has one entry per detector time group
(rounds + 1 for memory circuits, the last from the final readout).
"""

import math
from numbers import Integral

import numpy as np

from graft_circuit import higher_frequency, role_map
from leakage_hybrid import HybridSimulator


def _compile(circuit):
    """Validate once and prepare targets without altering execution order."""
    flat = circuit.flattened()
    roles = role_map(flat)
    # Our implementation: compact sparse input registers, excluding index holes
    # from leakage heating and from the physical population denominator.
    occupied = sorted(roles["data"] + roles["measure"])
    mapping = {q: k for k, q in enumerate(occupied)}
    if not occupied:
        raise ValueError("circuit must contain at least one physical qubit")

    supported = {
        "H", "X", "Y", "Z", "S", "CX", "CZ", "R", "M", "MR", "TICK",
        "DEPOLARIZE1", "DEPOLARIZE2", "X_ERROR", "Y_ERROR", "Z_ERROR",
        "DETECTOR", "OBSERVABLE_INCLUDE", "SHIFT_COORDS", "QUBIT_COORDS",
    }
    noise = {
        "DEPOLARIZE1", "DEPOLARIZE2", "X_ERROR", "Y_ERROR", "Z_ERROR"
    }
    coordinates = flat.get_detector_coordinates()
    detector_times = []
    operations = []
    measurements = 0
    ticks = 0

    for instruction in flat:
        name = instruction.name
        if name not in supported:
            raise ValueError(f"unsupported instruction: {name}")
        targets = instruction.targets_copy()
        args = instruction.gate_args_copy()

        if name in ("SHIFT_COORDS", "QUBIT_COORDS"):
            continue
        if name == "TICK":
            operations.append((name, (), None))
            ticks += 1
            continue
        if name in ("DETECTOR", "OBSERVABLE_INCLUDE"):
            offsets = []
            for target in targets:
                if (
                    not target.is_measurement_record_target
                    or not -measurements <= target.value < 0
                ):
                    raise ValueError(f"{name}: invalid measurement reference")
                offsets.append(target.value)
            if name == "DETECTOR":
                index = len(detector_times)
                coords = coordinates.get(index, ())
                # Design: detector time is coordinate 2, not instruction order.
                if len(coords) < 3 or not math.isfinite(coords[2]):
                    raise ValueError(
                        f"DETECTOR {index} requires a finite time coordinate"
                    )
                detector_times.append(coords[2])
            else:
                if (
                    len(args) != 1
                    or not math.isfinite(args[0])
                    or args[0] < 0
                    or args[0] != int(args[0])
                ):
                    raise ValueError("OBSERVABLE_INCLUDE: invalid index")
                index = int(args[0])
            operations.append((name, tuple(offsets), index))
            continue

        if any(not target.is_qubit_target for target in targets):
            raise ValueError(f"{name}: only physical qubit targets supported")
        if name not in ("M", "MR") and any(
            target.is_inverted_result_target for target in targets
        ):
            raise ValueError(f"{name}: inverted targets are unsupported")

        qubits = tuple(mapping[target.value] for target in targets)
        if name in ("CX", "CZ", "DEPOLARIZE2"):
            if len(qubits) % 2:
                raise ValueError(f"{name}: requires pairs of targets")
            if any(a == b for a, b in zip(qubits[::2], qubits[1::2])):
                raise ValueError(f"{name}: pair targets must be distinct")

        if name in noise:
            if (
                len(args) != 1
                or not math.isfinite(args[0])
                or not 0 <= args[0] <= 1
            ):
                raise ValueError(f"{name}: requires a probability in [0, 1]")
            operations.append((name, qubits, float(args[0])))
        elif name in ("CX", "CZ"):
            pairs = []
            for k in range(0, len(targets), 2):
                a, b = targets[k].value, targets[k + 1].value
                high = mapping[higher_frequency(a, b, roles)]
                pairs.append((mapping[a], mapping[b], high))
            operations.append((name, tuple(pairs), None))
        elif name in ("M", "MR"):
            # Generated circuits have no measurement-argument noise. Reject it
            # instead of silently ignoring an extra physical error channel.
            if any(arg != 0 for arg in args):
                raise ValueError(f"{name}: measurement-argument noise unsupported")
            inverted = tuple(t.is_inverted_result_target for t in targets)
            operations.append((name, qubits, inverted))
            measurements += len(qubits)
        else:
            operations.append((name, qubits, None))

    times = sorted(set(detector_times))
    groups = [
        np.flatnonzero(np.asarray(detector_times) == time) for time in times
    ]
    # Rounds = detector time groups minus the terminal readout group.
    # Heating/seepage are per-cycle, so TICKs are grouped by round
    # (main-agent revision, 2026-10-17; see module docstring). A
    # single-group circuit is treated as one round.
    if ticks == 0:
        raise ValueError("circuit has no TICK; cannot place per-cycle heating")
    if len(groups) == 1:
        rounds, ticks_per_round = 1, ticks
    else:
        rounds = len(groups) - 1
        if ticks % rounds != 0:
            raise ValueError(
                "cannot group TICKs into rounds: "
                f"{ticks} ticks, {len(groups)} detector time groups"
            )
        ticks_per_round = ticks // rounds
    return flat, operations, len(occupied), groups, ticks_per_round, rounds


def _noise(sim, name, targets, probability):
    """Apply instruction probabilities, independently per branch."""
    if probability == 0:
        return
    if name == "DEPOLARIZE1":
        for qubit in targets:
            sim.depolarize(qubit, probability)
        return
    if name == "DEPOLARIZE2":
        # Design: uniform distribution over the 15 nonidentity Pauli pairs.
        paulis = (None, "x", "y", "z")
        for a, b in zip(targets[::2], targets[1::2]):
            for branch in sim.branches:
                if sim.rng.random() < probability:
                    code = int(sim.rng.integers(1, 16))
                    for qubit, digit in ((a, code // 4), (b, code % 4)):
                        if digit:
                            getattr(branch.tableau, paulis[digit])(qubit)
        return
    gate = name[0].lower()
    for qubit in targets:
        for branch in sim.branches:
            if sim.rng.random() < probability:
                getattr(branch.tableau, gate)(qubit)


def _parity(record, offsets):
    """Evaluate record-relative references at the current instruction."""
    result = False
    for offset in offsets:
        result ^= bool(record[offset])
    return result


def run_circuit(circuit, params, shots: int, seed: int,
                postselect_first_round: bool = False) -> dict:
    """Execute complete shots, excluding rejected shots only from statistics.

    params carries the v0 physical parameters and controls. shots, seed and
    first-round postselection are controls from the Section V design.
    All randomness comes from one caller-seeded NumPy Generator, including
    all draws made by the hybrid engine.

    Detector rounds are sorted distinct third coordinates. Missing time
    coordinates raise ValueError. Population is sampled once per round
    (TICKs grouped by round; see the module docstring).
    Empty retained ensembles produce correctly shaped arrays and NaN means.
    """
    if (
        isinstance(shots, bool)
        or not isinstance(shots, Integral)
        or shots < 1
    ):
        raise ValueError("shots must be an integer >= 1")
    shots = int(shots)
    flat, operations, n_qubits, groups, ticks_per_round, n_rounds = _compile(circuit)
    rng = np.random.default_rng(seed)
    detectors = np.zeros((shots, flat.num_detectors), dtype=np.bool_)
    observables = np.zeros((shots, flat.num_observables), dtype=np.bool_)
    population_sum = np.zeros(n_rounds, dtype=float)
    kept = 0

    for _ in range(shots):
        sim = HybridSimulator(n_qubits, params, rng)
        record = []
        events = np.zeros(flat.num_detectors, dtype=np.bool_)
        flips = np.zeros(flat.num_observables, dtype=np.bool_)
        populations = np.empty(n_rounds, dtype=float)
        tick_index = 0

        for name, targets, argument in operations:
            if name in ("H", "X", "Y", "Z", "S"):
                gate = getattr(sim, name.lower())
                for qubit in targets:
                    gate(qubit)
            elif name in ("CX", "CZ"):
                gate = getattr(sim, name.lower())
                for a, b, high in targets:
                    gate(a, b, higher_freq=high)
            elif name == "R":
                for qubit in targets:
                    sim.reset_after_measure(qubit)
            elif name in ("M", "MR"):
                for qubit, inverted in zip(targets, argument):
                    outcome = sim.measure(qubit)
                    record.append(bool(outcome) ^ inverted)
                    if name == "MR":
                        sim.reset_after_measure(qubit)
            elif name == "TICK":
                # Once per round (first TICK of the round): the
                # per-cycle heating hazard, seepage, population sample.
                if tick_index % ticks_per_round == 0:
                    sim.engine.heat(n_qubits)
                    sim.engine.seep_cycle()
                    populations[tick_index // ticks_per_round] = float(
                        np.mean(sim.labels != 0)
                    )
                tick_index += 1
            elif name == "DETECTOR":
                events[argument] = _parity(record, targets)
            elif name == "OBSERVABLE_INCLUDE":
                flips[argument] ^= _parity(record, targets)
            else:
                _noise(sim, name, targets, argument)

        # Design/v0 convention: complete rejected shots to preserve RNG draws.
        rejected = (
            postselect_first_round
            and bool(groups)
            and bool(events[groups[0]].any())
        )
        if not rejected:
            detectors[kept] = events
            observables[kept] = flips
            population_sum += populations
            kept += 1

    detectors = detectors[:kept].copy()
    observables = observables[:kept].copy()
    if kept:
        detection_means = [
            float(detectors[:, group].mean()) for group in groups
        ]
        population_means = (population_sum / kept).tolist()
    else:
        detection_means = [float("nan")] * len(groups)
        population_means = [float("nan")] * n_rounds

    return {
        "det_events": detectors,
        "obs_flips": observables,
        "keep_rate": float(kept / shots),
        "detection_fraction_per_round": detection_means,
        "mean_label_population_per_round": population_means,
    }
