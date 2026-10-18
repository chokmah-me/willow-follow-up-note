"""Build digitize/device-values.json from digitize/raw-panels.json.

Qubits are keyed by device coordinate "r{row}c{col}" as printed in
Figs. S5/S9 (rows 3-11, columns 2-11, 54 qubits of the Fig. 4
grafting patch). CZ pairs are keyed "r{r1}c{c1}-r{r2}c{c2}" from the
edge-midpoint values of Fig. S7. The 54 site-centered "0.00"
strings in Fig. S7 are excluded: they sit exactly on qubit sites in
both panels, are identically "0.00", and cannot be interaction
frequencies; the remaining 89 values per panel are exactly the
nearest-neighbor adjacency of the 54-qubit patch (verified both
directions when this table is built).
"""
import json, statistics

RAW = "/home/hatch/workspace/willow-leakage-sim/digitize/raw-panels.json"
OUT = "/home/hatch/workspace/willow-leakage-sim/digitize/device-values.json"

QUBIT_FIELDS = {
    "10": ["freq_ghz", "f10_f21_mhz", "max_freq_ghz", "t1_us", "t2_us",
           "gate_err_1q_x1e-4"],
    "13": ["resonator_freq_ghz", "ringdown_ns", "coupling_eff_pct",
           "measurement_eff_pct", "freq_during_readout_ghz",
           "readout_pulse_ns", "readout_power_dbm", "max_photon_number",
           "readout_err_pct"],
}
# EDCF dashed-median lines (Figs. S6/S8), read from the PDF vector
# data (dashed-line x through the tick fit; the S8 method was
# verified against its own curve, which crosses 0.47-0.53 at the
# line). NOT the medians of the map values; see the report.
EDCF_MEDIANS = {"freq_ghz": 6.553, "f10_f21_mhz": 195.2,
                "max_freq_ghz": 6.688, "t1_us": 88.9, "t2_us": 64.2,
                "cz_interaction_freq_ghz": 6.448, "cz_err_x1e-3": 2.058}

def is_site(key):
    r, c = (float(x) for x in key.split(","))
    return r % 1 == 0 and c % 1 == 0

def main():
    raw = json.load(open(RAW))
    qubits = {}
    for page, fields in QUBIT_FIELDS.items():
        for field in fields:
            for key, val in raw[page][field].items():
                r, c = (int(float(x)) for x in key.split(","))
                qubits.setdefault(f"r{r}c{c}", {})[field] = val
    pairs = {}
    freq = {k: v for k, v in raw["12"]["cz_interaction_freq_ghz"].items() if not is_site(k)}
    err = {k: v for k, v in raw["12"]["cz_err_x1e-3"].items() if not is_site(k)}
    assert set(freq) == set(err)
    for key in freq:
        r, c = (float(x) for x in key.split(","))
        if r % 1 == 0:  # horizontal edge
            a, b = (int(r), int(c - 0.5)), (int(r), int(c + 0.5))
        else:           # vertical edge
            a, b = (int(r - 0.5), int(c)), (int(r + 0.5), int(c))
        assert f"r{a[0]}c{a[1]}" in qubits and f"r{b[0]}c{b[1]}" in qubits, key
        pairs[f"r{a[0]}c{a[1]}-r{b[0]}c{b[1]}"] = {
            "interaction_freq_ghz": freq[key], "cz_err_x1e-3": err[key]}
    # every adjacent qubit pair must carry a CZ value
    have = set(pairs)
    for qk in qubits:
        r, c = (int(x) for x in qk[1:].split("c"))
        for nb in ((r, c + 1), (r + 1, c)):
            nk = f"r{nb[0]}c{nb[1]}"
            if nk in qubits:
                assert f"{qk}-{nk}" in have, (qk, nk)
    medians = {}
    for page, fields in QUBIT_FIELDS.items():
        for field in fields:
            medians[field] = round(statistics.median(
                [q[field] for q in qubits.values()]), 3)
    medians["cz_interaction_freq_ghz"] = round(statistics.median(
        [p["interaction_freq_ghz"] for p in pairs.values()]), 3)
    medians["cz_err_x1e-3"] = round(statistics.median(
        [p["cz_err_x1e-3"] for p in pairs.values()]), 3)
    table = {
        "source": {
            "paper": "Rosenfeld et al., Magic state cultivation on a "
                     "superconducting quantum processor, Science 2026; "
                     "supplement of arXiv:2512.13908v1, Section V "
                     "(Figs. S5, S7, S9; EDCF Figs. S6, S8)",
            "pdf_sha256": "642ec2da74acd1b4df2a37985378dbbff69702b8c1314b7ad4e34ea1fcd5c43b",
            "scope": "qubits and couplers active in the Fig. 4 grafting "
                     "experiment, at the Fig. 4 control parameters "
                     "(S9 caption; S5/S7 captions say Fig. 4 likewise, "
                     "Section V text says the S9 parameters are taken "
                     "from the Fig. 2 experiment)",
            "method": "printed text values recovered from the PDF "
                      "vector layer by cell geometry "
                      "(digitize/extract_figs.py); no color estimation",
        },
        "qubits": qubits,
        "cz_pairs": pairs,
        "validation": {
            "qubit_count": len(qubits),
            "cz_pair_count": len(pairs),
            "panel_sets_identical": "all 15 square-lattice panels "
                                    "(S5 x6, S9 x9) carry the same 54 "
                                    "(row, column) cells; both S7 panels "
                                    "carry the same 89 edge midpoints",
            "adjacency_bijection": "the 89 S7 edges are exactly the "
                                    "nearest-neighbor pairs of the 54 "
                                    "qubits (checked both directions)",
            "map_medians": medians,
            "edcf_dashed_medians": EDCF_MEDIANS,
            "edcf_note": "the EDCF dashed medians do not all "
                         "reproduce from the map values (freq 6.553 "
                         "vs map 6.46; CZ error 2.058 vs map 1.9; the "
                         "rest agree within ~1%). The dashed lines do "
                         "mark their own curves' medians (verified on "
                         "S8b), so the EDCFs were computed on a "
                         "different sample than the maps. Use the map "
                         "values for the Fig. 4 patch.",
        },
    }
    json.dump(table, open(OUT, "w"), indent=1)
    print(f"wrote {OUT}: {len(qubits)} qubits, {len(pairs)} CZ pairs")

if __name__ == "__main__":
    main()
