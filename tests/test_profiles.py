import numpy as np
import pytest

from evi.profiles import berm_volume, landward_crossing, volume, volume_change


X = np.arange(0, 100.01, 0.1)


def lin(shift=0.0):
    z = 10 - 0.1 * (X + shift)
    return z


def test_volume_linear_profile():
    z = lin()
    assert volume(X, z, 100.0) == pytest.approx(500.0, rel=1e-6)
    # sand above the plane z=1.75: triangle 0.5 * 82.5 * 8.25
    assert volume(X, z, 100.0, 1.75) == pytest.approx(0.5 * 82.5 * 8.25, rel=1e-4)


def test_volume_change_sign_and_window():
    z0 = lin()
    z1 = lin(shift=5.0)            # profile 0.5 m lower everywhere -> erosion
    z1[800:] = np.nan              # shorter survey: common window must stop at x=79.9
    dv = volume_change(X, z0, z1)
    assert dv["x_max"] == pytest.approx(79.9)
    assert dv["total"] == pytest.approx(0.5 * 79.9, rel=1e-6)   # positive = erosion
    assert dv["upper"] + dv["lower"] == pytest.approx(dv["total"])
    assert np.isnan(volume(X, z1, 100.0))


def test_landward_crossing_on_barred_profile():
    z = lin()
    z[(X > 60) & (X < 70)] = 3.2   # a bar/berm seaward that re-crosses z=3
    assert landward_crossing(X, z, 3.0) == pytest.approx(70.0, abs=0.11)  # first down-crossing of 3 m
    zb = lin()
    zb[(X > 50) & (X < 60)] = 2.0  # trough then bar: the landward-most 4 m crossing is at x=60
    assert landward_crossing(X, zb, 4.0) == pytest.approx(50.0, abs=0.11)


def test_berm_volume_band():
    z = lin()
    # band between 1.75 and 4.0 seaward of x(4.0)=60: triangle 0.5*22.5*2.25 + nothing else
    assert berm_volume(X, z) == pytest.approx(0.5 * 22.5 * 2.25, rel=1e-3)
