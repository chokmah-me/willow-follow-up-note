"""Verified aggregate leakage parameters, plus a digitized device table.

The DeviceParams leakage table still runs on verified aggregate
defaults: the supplement figures carry no per-qubit leakage rates,
so no per-qubit leakage override can be sourced from them. What the
figures do carry, printed as text per cell, is the device table of
Figs. S5/S7/S9 (frequencies, T1/T2, gate and readout parameters for
the 54 qubits and 89 couplers of the Fig. 4 grafting patch). That
table is digitized in digitize/device-values.json and loaded by
load_digitized_device_table below; it is device data, not leakage
parameters, and is kept out of the QubitParams rows on purpose.
The digitization_status field travels with serialized tables.
Overrides are caller-supplied, not inferred data.

The uniform v0 engine adapter deliberately uses only the default row.
"""

from dataclasses import asdict, dataclass, field
import json
import math
import os

from leakage_hybrid import LeakageParams


DIGITIZED_TABLE_STATUS = "digitized_from_printed_fig_values_s5_s7_s9"
DIGITIZED_TABLE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "digitize", "device-values.json")

_DIGITIZED_QUBIT_FIELDS = {
    "freq_ghz", "f10_f21_mhz", "max_freq_ghz", "t1_us", "t2_us",
    "gate_err_1q_x1e-4", "resonator_freq_ghz", "ringdown_ns",
    "coupling_eff_pct", "measurement_eff_pct", "freq_during_readout_ghz",
    "readout_pulse_ns", "readout_power_dbm", "max_photon_number",
    "readout_err_pct",
}


def load_digitized_device_table(path=DIGITIZED_TABLE_PATH):
    """Load the Figs. S5/S7/S9 device table digitized from print.

    Keys are device coordinates ("r{row}c{col}"), not simulator
    indices: mapping them onto a specific circuit's qubit order
    requires the paper's explicit circuits (supplement Sec. VII).
    Validates the published counts (54 qubits, 89 CZ pairs) and the
    full per-qubit field set; raises ValueError on any mismatch.
    """
    with open(path, encoding="utf-8") as handle:
        table = json.load(handle)
    qubits, pairs = table["qubits"], table["cz_pairs"]
    if len(qubits) != 54 or len(pairs) != 89:
        raise ValueError("digitized table must hold 54 qubits and 89 CZ pairs")
    for key, row in qubits.items():
        if set(row) != _DIGITIZED_QUBIT_FIELDS:
            raise ValueError(f"digitized qubit {key} has wrong fields")
    for key, row in pairs.items():
        if set(row) != {"interaction_freq_ghz", "cz_err_x1e-3"}:
            raise ValueError(f"digitized pair {key} has wrong fields")
        a, b = key.split("-")
        if a not in qubits or b not in qubits:
            raise ValueError(f"digitized pair {key} joins unknown qubits")
    return table


LITERATURE = {
    # McEwen et al. 2021, fitted leakage generation per cycle.
    "generation_per_cycle_band": (0.09e-2, 0.11e-2),
    # McEwen et al. 2021, steady-state |2> population.
    "steady_state_population_band": (0.97e-2, 1.30e-2),
    # Miao et al. 2023, leakage lifetime.
    "lifetime_cycles": 4.4,
    # Miao et al. 2023: excess |2> strictly below this bound by 2 cycles.
    "removal_excess_population_upper_bound": 1e-3,
    "removal_within_cycles": 2,
    # Cultivation supplement, Sec. XIV, SI1000 baseline.
    "si1000_p": 2.3e-3,
    # Cultivation supplement, Sec. XIV / Fig. S22 fit values.
    "experiment_logical_error_per_cycle": 5.3e-2,
    "simulated_logical_error_per_cycle": 0.8e-2,
}


def _validate_number(name, value, *, probability=False):
    try:
        valid = math.isfinite(value)
        valid = valid and (0 <= value <= 1 if probability else value > 0)
    except (TypeError, ValueError, OverflowError):
        valid = False
    if not valid:
        domain = "in [0, 1]" if probability else "positive"
        raise ValueError(f"{name} must be finite and {domain}")


@dataclass
class QubitParams:
    """Aggregate defaults; readout leakage is an unspecialized Arm-3 knob."""

    cz_leak_prob: float = 8e-4        # 2023 SI Sec. XIV: pt.
    heating_rate: float = 1.0 / 700e-6  # 2023 SI Sec. XIV: Gamma, s^-1.
    t_cycle: float = 896e-9          # 2023 SI Sec. XIV, seconds.
    lifetime_cycles: float = 4.4     # Miao et al. 2023.
    readout_leak_prob: float = 0.0   # Arm-3 swept knob, not measured here.

    def __post_init__(self):
        for name in ("cz_leak_prob", "readout_leak_prob"):
            _validate_number(name, getattr(self, name), probability=True)
        for name in ("heating_rate", "t_cycle", "lifetime_cycles"):
            _validate_number(name, getattr(self, name))


@dataclass
class DeviceParams:
    """Aggregate-backed table with explicit provenance and optional overrides."""

    default: QubitParams = field(default_factory=QubitParams)
    overrides: dict = field(default_factory=dict)
    digitization_status: str = "aggregate_only_not_digitized"

    def __post_init__(self):
        if not isinstance(self.default, QubitParams):
            raise ValueError("default must be a QubitParams")
        self.default.__post_init__()
        if not isinstance(self.overrides, dict):
            raise ValueError("overrides must be a dict")
        for index, row in self.overrides.items():
            if isinstance(index, bool) or not isinstance(index, int) or index < 0:
                raise ValueError("override indices must be nonnegative integers")
            if not isinstance(row, QubitParams):
                raise ValueError("override rows must be QubitParams")
            row.__post_init__()
        if not isinstance(self.digitization_status, str):
            raise ValueError("digitization_status must be a string")

    def for_qubit(self, i) -> QubitParams:
        """Return the explicit override, or the aggregate default row."""
        return self.overrides.get(i, self.default)

    def uniform_leakage_params(self, **overrides) -> LeakageParams:
        """Adapt defaults to v0; spatial overrides are intentionally not averaged."""
        values = asdict(self.default)
        values.update(overrides)
        # Validate the shared physical fields, including keyword replacements.
        QubitParams(**{name: values[name] for name in asdict(self.default)})
        return LeakageParams(**values)

    def save_json(self, path):
        """Save all rows and the provenance status, without inventing data."""
        self.__post_init__()
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(asdict(self), handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")

    @classmethod
    def load_json(cls, path):
        """Restore integer qubit indices and validate every parameter row."""
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        rows = {}
        for key, value in data["overrides"].items():
            try:
                index = int(key)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid qubit index: {key!r}") from exc
            if str(index) != key or index in rows:
                raise ValueError(f"noncanonical or duplicate qubit index: {key!r}")
            rows[index] = QubitParams(**value)
        return cls(
            default=QubitParams(**data["default"]),
            overrides=rows,
            digitization_status=data["digitization_status"],
        )

    def analytic_steady_state(self) -> float:
        """Heating/seepage two-state estimate, not the complete CZ-driven model."""
        self.default.__post_init__()
        p = self.default
        p_gen = -math.expm1(-p.heating_rate * p.t_cycle)
        p_seep = -math.expm1(-1.0 / p.lifetime_cycles)
        return p_gen / (p_gen + p_seep)
