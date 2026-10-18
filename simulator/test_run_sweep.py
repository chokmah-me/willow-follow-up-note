"""Small integration tests using the real hybrid engine and pinned decoder."""

import copy
import json
import math

import pytest

from run_sweep import run_sweep


@pytest.fixture(scope="module")
def tiny_config():
    return {
        "distance": 3,
        "rounds_list": [3, 5],
        "p": 0.002,
        "shots": 200,
        "seed": 1729,
        "generation_grid": [0.0, 0.002],
        "lifetime_grid": [4.4],
        "readout_multipliers": [3.0],
        "ratio_tolerance": 5.0,
        "postselect_first_round": False,
    }


@pytest.fixture(scope="module")
def results(tiny_config):
    return run_sweep(copy.deepcopy(tiny_config))


def _at_generation(results, arm, generation):
    return next(
        point for point in results["arms"][arm]
        if point["generation"] == generation
    )


def test_structure(results):
    arms = results["arms"]
    assert set(arms) == {
        "baseline_stim", "baseline_hybrid", "leakage",
        "leakage_readout", "leakage_removal",
    }
    points = [arms["baseline_stim"], arms["baseline_hybrid"]]
    for arm in ("leakage", "leakage_readout", "leakage_removal"):
        assert len(arms[arm]) == 2
        points.extend(arms[arm])
        for point in arms[arm]:
            if point["generation"] > 0:
                assert point["score"] is not None
    for point in points:
        assert "ler_per_cycle" in point
        assert 0 <= point["keep_rate"] <= 1
        assert set(point["by_rounds"]) == {"3", "5"}
        for record in point["by_rounds"].values():
            assert 0 <= record["n_logical_errors"] <= record["shots_kept"]
            assert record["shots_kept"] == 200
            assert 0 <= record["p_logical"] <= 1
    for arm in ("baseline_stim", "baseline_hybrid"):
        assert arms[arm]["ratio_vs_baseline_hybrid"] is None
        assert arms[arm]["score"] is None


def test_zero_generation_has_no_population(results):
    point = _at_generation(results, "leakage", 0.0)
    assert point["steady_population"] == 0.0
    assert results["arms"]["baseline_hybrid"]["steady_population"] == 0.0
    assert results["arms"]["baseline_stim"]["steady_population"] is None


def test_removal_reduces_population_directionally(results):
    leakage = _at_generation(results, "leakage", 0.002)
    removal = _at_generation(results, "leakage_removal", 0.002)
    assert removal["steady_population"] <= leakage["steady_population"]


def test_baseline_cross_check(results, tiny_config):
    check = results["baseline_cross_check"]
    assert check["dof"] > 0
    assert math.isfinite(check["detection_curve_chi2"])
    curve = results["arms"]["baseline_hybrid"]["detection_fraction_per_round"]
    assert len(curve) == max(tiny_config["rounds_list"]) + 1
    assert all(0 <= value <= 1 for value in curve)


def test_json_serializable(results, tiny_config):
    encoded = json.dumps(results, allow_nan=False)
    assert json.loads(encoded)["config"] == tiny_config


def test_deterministic_baseline(results, tiny_config):
    repeated = run_sweep(copy.deepcopy(tiny_config))
    assert (
        repeated["arms"]["baseline_hybrid"]["ler_per_cycle"]
        == results["arms"]["baseline_hybrid"]["ler_per_cycle"]
    )


@pytest.mark.parametrize(
    "override",
    [
        {"arms": ["unknown_arm"]},
        {"generation_grid": []},
        {"lifetime_grid": []},
        {"shots": 0},
        {"shots": -1},
        {"rounds_list": []},
    ],
)
def test_invalid_config_raises(tiny_config, override):
    config = copy.deepcopy(tiny_config)
    config.update(override)
    with pytest.raises(ValueError):
        run_sweep(config)
