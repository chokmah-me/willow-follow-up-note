"""Generated surface-code memory circuits for the grafted-memory stand-in.

This is the standard SI1000-style mapping used for generated circuits.
Setting every noise knob to one p simplifies the paper's weighted SI1000
model; it is not a calibrated reproduction of that model.

The cultivation and grafting stages are abstracted as a post-selected logical
preparation. The simulated object is the grafted memory stage, where
Rosenfeld et al. (2026), arXiv:2512.13908v1, supplement S22-S24 live.
The actual preparation implemented here is Stim's logical-Z preparation,
not a simulation of cultivation or of its acceptance probability.

Design source: Section V simulation design, 2026-10-16.
Our stand-ins: equal noise-knob probabilities and a role-based frequency
ordering. The frequency ordering is not a device-frequency calibration.

Stim's generated qubit indices contain gaps. We densely relabel occupied
indices, preserving coordinates, operations, measurement records and repeat
blocks. Consequently distance 3 uses an allocated register of 17 qubits,
rather than a register whose size includes unused index positions.
"""

import math
from numbers import Integral, Real

import stim

from leakage_hybrid import LeakageParams  # Shared physical-model API.


def _occupied_qubits(circuit):
    """Find physical targets, excluding measurement-record references."""
    return {
        target.value
        for instruction in circuit.flattened()
        for target in instruction.targets_copy()
        if target.is_qubit_target
    }


def _relabel(circuit, mapping):
    """Relabel physical targets without changing record-relative references."""
    result = stim.Circuit()
    for instruction in circuit:
        if isinstance(instruction, stim.CircuitRepeatBlock):
            result.append(
                stim.CircuitRepeatBlock(
                    instruction.repeat_count,
                    _relabel(instruction.body_copy(), mapping),
                )
            )
            continue
        targets = []
        for target in instruction.targets_copy():
            if target.is_qubit_target:
                index = mapping[target.value]
                targets.append(
                    stim.target_inv(index) if target.is_inverted_result_target
                    else index
                )
            else:
                targets.append(target)
        result.append(
            instruction.name, targets, instruction.gate_args_copy()
        )
    return result


def build_memory_circuit(distance: int, rounds: int, p: float) -> stim.Circuit:
    """Build a densely indexed rotated logical-Z memory circuit.

    distance and rounds are experiment controls from the Section V design.
    The common probability p is our equal-knob SI1000-style stand-in.
    """
    if (
        isinstance(distance, bool)
        or not isinstance(distance, Integral)
        or distance < 3
        or distance % 2 == 0
    ):
        raise ValueError("distance must be an odd integer >= 3")
    if (
        isinstance(rounds, bool)
        or not isinstance(rounds, Integral)
        or rounds < 1
    ):
        raise ValueError("rounds must be an integer >= 1")
    if not isinstance(p, Real) or not math.isfinite(p) or not 0 <= p <= 0.1:
        raise ValueError("p must be finite and in [0, 0.1]")

    generated = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=int(distance),
        rounds=int(rounds),
        # Our stand-in: one probability for all generated SI1000-style knobs.
        after_clifford_depolarization=float(p),
        before_round_data_depolarization=float(p),
        before_measure_flip_probability=float(p),
        after_reset_flip_probability=float(p),
    )
    mapping = {
        old: new for new, old in enumerate(sorted(_occupied_qubits(generated)))
    }
    return _relabel(generated, mapping)


def circuit_metadata(circuit) -> dict:
    """Return Stim register dimensions, not inferred construction parameters."""
    return {
        "n_qubits": circuit.num_qubits,
        "n_detectors": circuit.num_detectors,
        "n_observables": circuit.num_observables,
    }


def role_map(circuit) -> dict:
    """Classify occupied physical qubits by whether they ever undergo MR.

    Unused gaps in a bare Stim circuit's index space are not physical qubits.
    Circuits returned by build_memory_circuit have no such gaps.
    """
    flat = circuit.flattened()
    occupied = _occupied_qubits(flat)
    measure = {
        target.value
        for instruction in flat
        if instruction.name == "MR"
        for target in instruction.targets_copy()
        if target.is_qubit_target
    }
    return {"data": sorted(occupied - measure), "measure": sorted(measure)}


def higher_frequency(i: int, j: int, roles: dict) -> int:
    """Our stand-in: measure beats data; within a role, larger index wins.

    The device grid places the roles at different frequencies, but this
    deterministic ordering is not a frequency map extracted from the paper.
    """
    data, measure = set(roles["data"]), set(roles["measure"])
    if data & measure:
        raise ValueError("data and measure roles must be disjoint")
    if i not in data | measure or j not in data | measure:
        raise ValueError("both qubits must have a role")
    return max((i, j), key=lambda q: (q in measure, q))
