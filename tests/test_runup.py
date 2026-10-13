import numpy as np
import pytest

from evi.runup import deep_water_wavelength, deshoal, shoaling_coefficient, stockdon_r2, wavenumber


def test_stockdon_intermediate_hand_value():
    # H0=2 m, L0=100 m, beta=0.1 -> xi=0.707 (non-dissipative branch), hand-computed 1.3078 m
    assert stockdon_r2(2.0, 100.0, 0.1) == pytest.approx(1.3078, abs=1e-3)


def test_stockdon_dissipative_uses_0043_not_0016():
    # xi = 0.01/sqrt(4/100) = 0.05 < 0.3 -> R2 = 0.043*sqrt(400) = 0.86 (thesis typo 0.016 is the setup term)
    assert stockdon_r2(4.0, 100.0, 0.01) == pytest.approx(0.86, rel=1e-9)


def test_stockdon_nan_slope():
    assert np.isnan(stockdon_r2(2.0, 100.0, np.nan))


def test_dispersion_and_shoaling():
    k = wavenumber(np.array([8.0, 14.0]), 50.0)
    w = 2 * np.pi / np.array([8.0, 14.0])
    assert np.allclose(w ** 2, 9.81 * k * np.tanh(k * 50.0), rtol=1e-10)
    assert shoaling_coefficient(np.array([20.0]))[0] == pytest.approx(1.0, abs=1e-6)
    # short waves in 50 m are deep water: H0 == Hs
    assert deshoal(3.0, 5.0, 50.0) == pytest.approx(3.0, rel=1e-3)
    assert deep_water_wavelength(10.0) == pytest.approx(9.81 * 100 / (2 * np.pi))
