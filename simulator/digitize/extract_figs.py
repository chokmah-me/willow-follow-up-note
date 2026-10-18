"""Extract the printed per-cell values from Figs. S5, S7, S9 of the
cultivation supplement (arXiv:2512.13908v1, Section V).

Method: the figures are vector graphics and every value is printed
as text inside its cell. Panel anchors are the white background
rectangles in the drawing stream. Row/column tick labels sit just
outside each panel; a linear fit through the tick label positions
maps every value word's center to (row, column). For S5/S9 the
values land on integer cells (one per qubit); for S7 they land on
edge midpoints (half-integer in exactly one coordinate), which
identifies the CZ pair. Values are read as printed text, never
estimated from color, so the reading error is the print rounding.
"""
import json, re, statistics
import pymupdf

PDF = "/home/hatch/workspace/willow-sources/rosenfeld-2026-cultivation-arxiv-2512.13908.pdf"
OUT = "/home/hatch/workspace/willow-leakage-sim/digitize/raw-panels.json"
NUM = re.compile(r"^-?\d+(\.\d+)?$")

# page index -> (panel keys in reading order, snap mode)
PAGES = {
    10: (["freq_ghz", "f10_f21_mhz", "max_freq_ghz", "t1_us", "t2_us",
          "gate_err_1q_x1e-4"], "cell", None),
    12: (["cz_interaction_freq_ghz", "cz_err_x1e-3"], "edge", 300),
    13: (["resonator_freq_ghz", "ringdown_ns", "coupling_eff_pct",
          "measurement_eff_pct", "freq_during_readout_ghz",
          "readout_pulse_ns", "readout_power_dbm", "max_photon_number",
          "readout_err_pct"], "cell", None),
}

def numeric_words(page):
    out = []
    for x0, y0, x1, y1, text, *_ in page.get_text("words"):
        t = text.replace("−", "-")
        if NUM.match(t):
            out.append({"cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2,
                        "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                        "val": float(t), "int": "." not in t})
    return out

def backgrounds(page, ymax=None):
    out = []
    for d in page.get_drawings():
        r = d["rect"]
        if d["fill"] == (1.0, 1.0, 1.0) and 100 < r.width < 300 and 100 < r.height < 240:
            if ymax is None or r.y0 < ymax:
                out.append(r)
    return sorted(out, key=lambda r: (round(r.y0 / 100), r.x0))

def fit(pairs):
    """Linear fit value(pos) over (pos, value) pairs, robust to a
    stray word: median position per tick value, then one pass that
    drops points with residual > 2.5 pt and refits."""
    by = {}
    for pos, v in pairs:
        by.setdefault(v, []).append(pos)
    pts = [(statistics.median(p), v) for v, p in sorted(by.items())]
    for _ in range(2):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        b = my - a * mx
        # residual is in tick-value units; 0.18 of a tick ~ 2.6 pt
        pts = [(x, y) for x, y in pts if abs(a * x + b - y) < 0.18]
        if len(pts) < 3:
            break
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return lambda pos: a * pos + (my - a * mx)

def snap(v, mode):
    if mode == "cell":
        return round(v)
    # edge: integer or half-integer
    return round(v * 2) / 2

def largest_cluster(items, key):
    """items: list of dicts; cluster by a coordinate (5 pt bins),
    return the biggest cluster. Tick labels share one line: row
    ticks share an x, column ticks share a y. Neighbouring panels'
    labels and title fragments fall on other lines and lose."""
    bins = {}
    for it in items:
        bins.setdefault(round(key(it) / 5), []).append(it)
    return max(bins.values(), key=len) if bins else []

def extract_panel(page, bg, mode):
    ws = numeric_words(page)
    row_cand = [w for w in ws
                if w["int"] and w["x1"] < bg.x0 - 1 and bg.y0 < w["cy"] < bg.y1
                and 2 <= w["val"] <= 12]
    col_cand = [w for w in ws
                if w["int"] and w["y0"] > bg.y1 + 1 and bg.x0 < w["cx"] < bg.x1
                and 1 <= w["val"] <= 12]
    row_ticks = [(w["cy"], int(w["val"])) for w in largest_cluster(row_cand, lambda w: w["cx"])]
    col_ticks = [(w["cx"], int(w["val"])) for w in largest_cluster(col_cand, lambda w: w["cy"])]
    if len(row_ticks) < 3 or len(col_ticks) < 3:
        raise RuntimeError(f"ticks missing: rows={row_ticks} cols={col_ticks}")
    row_of = fit(row_ticks)
    col_of = fit(col_ticks)
    values = {}
    for w in ws:
        if bg.x0 + 1 < w["cx"] < bg.x1 - 1 and bg.y0 + 1 < w["cy"] < bg.y1 - 1:
            r = snap(row_of(w["cy"]), mode)
            c = snap(col_of(w["cx"]), mode)
            if (r, c) in values:
                raise RuntimeError(f"collision at {(r, c)}")
            values[(r, c)] = w["val"]
    return values, len(row_ticks), len(col_ticks)

def main():
    doc = pymupdf.open(PDF)
    result = {}
    for pno, (keys, mode, ymax) in PAGES.items():
        page = doc[pno]
        bgs = backgrounds(page, ymax)
        assert len(bgs) == len(keys), (pno, len(bgs), len(keys))
        result[pno] = {}
        for key, bg in zip(keys, bgs):
            vals, nr, nc = extract_panel(page, bg, mode)
            result[pno][key] = {f"{r},{c}": v for (r, c), v in sorted(vals.items())}
            print(f"page {pno+1} {key}: values={len(vals)} rowticks={nr} colticks={nc}")
    json.dump(result, open(OUT, "w"), indent=1)
    print("wrote", OUT)

if __name__ == "__main__":
    main()
