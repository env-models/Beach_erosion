import numpy as np
import pytest

from evi.energy import e_density_dt, e_hs2dt, e_notebook, energy_density, energy_flux, p_flux_dt


def test_energy_density_value():
    assert energy_density(1.0) == pytest.approx(1025 * 9.81 / 16)


def test_notebook_units_are_MJ_hour_per_m2():
    # notebook: (1/16) rho g Hs^2 * 3 / 1e6 with rho=1025, g=9.8, dt in HOURS
    assert e_notebook(2.0) == pytest.approx(1025 * 9.8 / 16 * 4 * 3 / 1e6)
    # converting to MJ s m^-2 needs x3600 (and the g change 9.8 -> 9.81)
    assert e_density_dt(2.0) == pytest.approx(e_notebook(2.0) * 3600 * 9.81 / 9.8)


def test_hs2dt_and_flux():
    assert e_hs2dt(np.array([2.0, 3.0])).sum() == pytest.approx((4 + 9) * 3)
    p = energy_flux(1.0, 10.0)
    assert p == pytest.approx(1025 * 9.81 ** 2 * 10 / (64 * np.pi))
    assert p_flux_dt(1.0, 10.0) == pytest.approx(p * 3 * 3600 / 1e6)
