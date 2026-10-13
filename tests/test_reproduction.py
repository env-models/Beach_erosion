"""Regression test: the notebook's printed numbers are reproduced from repo data."""
import pytest

from evi.legacy import run_notebook


@pytest.fixture(scope="module")
def nb():
    return run_notebook()


def test_ppt_train_matches_notebook_figure(nb):
    # notebook cell 20 figure: "RMSE =11.73", "R =0.83"
    assert round(nb["ppt_train"]["RMSE_weighted_nb"], 2) == 11.73
    assert round(nb["ppt_train"]["R_weighted_nb"], 2) == 0.83


def test_ppt_test_matches_notebook_output(nb):
    # notebook cell 23 output: "R =0.97", figure "RMSE =8.08"
    assert round(nb["ppt_test"]["R_weighted_nb"], 2) == 0.97
    assert round(nb["ppt_test"]["RMSE_weighted_nb"], 2) == 8.08
    assert nb["ppt_test"]["n"] == 8 and nb["ppt_test"]["fat_n"] == 2
