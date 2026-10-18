"""Behavioral pin for OUR installed Tesseract decoder, not the paper's decoder.

Google published no version/settings underlying the 0.8%/cycle fit.
The requested long-beam configuration below is documentation provenance,
not a claim that the factory's first decoder applies those settings.
A small deterministic probe detects changes on its inputs, not every
possible decoder behavior change. No network access is performed.
"""

import hashlib
from importlib import metadata
import json

import numpy as np
import tesseract_decoder


# REQUESTED configuration: Tesseract documentation's long-beam example,
# recorded by the survey on 2026-10-17. Not silently applied to factory objects.
LONG_BEAM_REQUEST = {
    "pqlimit": 1000000,
    "det_beam": 20,
    "beam_climbing": True,
    "det_orders": 21,
    "no_revisit_dets": True,
}

_VERSION_PACKAGES = {
    "tesseract_version": "tesseract-decoder",
    "stim_version": "stim",
    "sinter_version": "sinter",
    "pymatching_version": "pymatching",
}
_PROBE_SEED = 0
_PROBE_RANDOM_SHOTS = 64


def _decoder_dict():
    factory = getattr(
        tesseract_decoder, "make_tesseract_sinter_decoders_dict", None
    )
    if not callable(factory):
        raise RuntimeError(
            "tesseract_decoder is missing "
            "make_tesseract_sinter_decoders_dict()"
        )
    return factory()


def available_decoders() -> list:
    """Return factory names in deterministic lexical order."""
    return sorted(_decoder_dict())


def _first_decoder(decoders):
    if not decoders:
        raise RuntimeError("Tesseract decoder factory returned no available decoders")
    # The survey's starting point is the factory's long-beam decoder;
    # fall back to sorted order if a future snapshot renames it
    # (main-agent fix, 2026-10-17: the installed snapshot's factory
    # keys are tesseract-long-beam, tesseract, short-beam and
    # sparsify variants).
    if "tesseract-long-beam" in decoders:
        return decoders["tesseract-long-beam"]
    return decoders[sorted(decoders)[0]]


def get_decoder():
    """Return the long-beam decoder (survey starting config)."""
    return _first_decoder(_decoder_dict())


def applied_config(decoder) -> dict:
    """Read the decoder's actual long-beam knobs, where exposed."""
    keys = ("pqlimit", "det_beam", "beam_climbing", "num_det_orders",
            "no_revisit_dets")
    return {k: getattr(decoder, k) for k in keys if hasattr(decoder, k)}


def _compile(decoder, dem):
    # The installed snapshot names the method compile_decoder_for_dem
    # (tesseract_sinter_compat), not sinter's compile_for_dem
    # (main-agent fix, 2026-10-17).
    method = getattr(decoder, "compile_decoder_for_dem", None)
    if not callable(method):
        method = getattr(decoder, "compile_for_dem", None)
    if not callable(method):
        raise RuntimeError(
            "Tesseract decoder is missing compile_decoder_for_dem(dem=...)"
        )
    try:
        compiled = method(dem=dem)
    except NotImplementedError as exc:
        raise RuntimeError(
            "Tesseract decoder does not implement compile_decoder_for_dem(dem=...)"
        ) from exc
    if not callable(getattr(compiled, "decode_shots_bit_packed", None)):
        raise RuntimeError(
            "Compiled Tesseract decoder is missing decode_shots_bit_packed"
        )
    return compiled


def _predictions(compiled, events, n_observables):
    packed = np.packbits(events, axis=1, bitorder="little")
    try:
        result = compiled.decode_shots_bit_packed(
            bit_packed_detection_event_data=packed
        )
    except NotImplementedError as exc:
        raise RuntimeError(
            "Compiled Tesseract decoder does not implement "
            "decode_shots_bit_packed"
        ) from exc
    result = np.asarray(result)
    expected = (events.shape[0], (n_observables + 7) // 8)
    if result.dtype != np.uint8 or result.shape != expected:
        raise RuntimeError(
            "decode_shots_bit_packed returned an invalid result: "
            f"expected uint8 shape {expected}, got {result.dtype} {result.shape}"
        )
    return np.unpackbits(
        result, axis=1, count=n_observables, bitorder="little"
    ).astype(bool)


def decode(circuit, det_events) -> np.ndarray:
    """Predict observables using the actual compiled sinter decoder protocol."""
    events = np.asarray(det_events)
    if events.ndim != 2 or events.shape[1] != circuit.num_detectors:
        raise ValueError(
            "det_events must have shape (shots, circuit.num_detectors)"
        )
    if not np.all((events == 0) | (events == 1)):
        raise ValueError("det_events must contain only binary values")
    dem = circuit.detector_error_model(decompose_errors=True)
    compiled = _compile(get_decoder(), dem)
    return _predictions(compiled, events.astype(bool), circuit.num_observables)


def _version(package):
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        # JSON null explicitly records absence; it is not a guessed version.
        return None


def _make_pin(circuit):
    decoders = _decoder_dict()
    decoder = _first_decoder(decoders)
    dem = circuit.detector_error_model(decompose_errors=True)
    compiled = _compile(decoder, dem)
    rng = np.random.default_rng(_PROBE_SEED)
    events = np.zeros(
        (_PROBE_RANDOM_SHOTS + 1, circuit.num_detectors), dtype=bool
    )
    events[1:] = rng.random(
        (_PROBE_RANDOM_SHOTS, circuit.num_detectors)
    ) < 0.02
    predictions = _predictions(compiled, events, circuit.num_observables)
    return {
        **{key: _version(package) for key, package in _VERSION_PACKAGES.items()},
        "available_decoders": sorted(decoders),
        "selected_decoder": (
            "tesseract-long-beam" if "tesseract-long-beam" in decoders
            else sorted(decoders)[0]
        ),
        "requested_config": dict(LONG_BEAM_REQUEST),
        "applied_config": applied_config(decoder),
        "fingerprint": {
            "sha256": hashlib.sha256(predictions.tobytes(order="C")).hexdigest(),
            "sample_count": len(events),
            "seed": _PROBE_SEED,
            "flip_probability": 0.02,
            "prediction_encoding": "unpacked_bool_uint8_row_major",
            "num_detectors": circuit.num_detectors,
            "num_observables": circuit.num_observables,
        },
    }


def write_pin(path, circuit) -> dict:
    """Write versions, requested settings, and deterministic prediction hash."""
    pin = _make_pin(circuit)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(pin, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    return pin


def check_pin(path, circuit) -> tuple:
    """Recompute the probe and report each changed recorded field.

    Missing files or invalid JSON propagate their ordinary I/O/JSON errors.
    Missing decoder protocol support raises RuntimeError rather than faking
    predictions or reporting a successful comparison.
    """
    with open(path, encoding="utf-8") as handle:
        stored = json.load(handle)
    current = _make_pin(circuit)
    if not isinstance(stored, dict):
        return False, ["pin must be a JSON object"]
    diffs = []
    for key, value in current.items():
        if key not in stored:
            diffs.append(f"{key}: missing from stored pin")
        elif key == "fingerprint" and isinstance(stored[key], dict):
            for field, expected in value.items():
                if field not in stored[key]:
                    diffs.append(f"fingerprint.{field}: missing from stored pin")
                elif stored[key][field] != expected:
                    diffs.append(
                        f"fingerprint.{field}: stored {stored[key][field]!r}, "
                        f"current {expected!r}"
                    )
        elif stored[key] != value:
            diffs.append(f"{key}: stored {stored[key]!r}, current {value!r}")
    return not diffs, diffs
