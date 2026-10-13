"""Deep-water de-shoaling and Stockdon et al. (2006) R2% runup."""
from __future__ import annotations

import numpy as np

from .constants import DEPTH_SHOAL, G


def deep_water_wavelength(tp: np.ndarray, g: float = G) -> np.ndarray:
    """L0 = g T^2 / (2 pi)."""
    return g * np.asarray(tp, float) ** 2 / (2 * np.pi)


def wavenumber(tp: np.ndarray, h: float, g: float = G, n_iter: int = 50) -> np.ndarray:
    """Solve the linear dispersion relation w^2 = g k tanh(k h) (Newton iterations)."""
    w = 2 * np.pi / np.asarray(tp, float)
    k = w ** 2 / g / np.sqrt(np.tanh(w ** 2 * h / g))  # Eckart-type first guess
    for _ in range(n_iter):
        f = g * k * np.tanh(k * h) - w ** 2
        df = g * np.tanh(k * h) + g * k * h / np.cosh(k * h) ** 2
        k = k - f / df
    return k


def shoaling_coefficient(kh: np.ndarray) -> np.ndarray:
    """Ks = sqrt(cg0/cg) = [tanh(kh) (1 + 2kh/sinh(2kh))]^-1/2 (linear theory)."""
    kh = np.asarray(kh, float)
    return np.sqrt(1.0 / (np.tanh(kh) * (1 + 2 * kh / np.sinh(2 * kh))))


def deshoal(hs: np.ndarray, tp: np.ndarray, h: float = DEPTH_SHOAL, exact: bool = True,
            g: float = G) -> np.ndarray:
    """Return deep-water H0 = Hs / Ks at depth ``h``.

    ``exact=True`` uses the dispersion-relation k; ``exact=False`` reproduces the
    notebook, which used the deep-water k0 = 2 pi / L0 inside Ks.
    """
    if exact:
        kh = wavenumber(tp, h, g) * h
    else:
        kh = 2 * np.pi * h / deep_water_wavelength(tp, g)
    return np.asarray(hs, float) / shoaling_coefficient(kh)


def iribarren(beta: np.ndarray, h0: np.ndarray, l0: np.ndarray) -> np.ndarray:
    """xi0 = beta / sqrt(H0/L0)."""
    return np.asarray(beta, float) / np.sqrt(np.asarray(h0, float) / np.asarray(l0, float))


def stockdon_r2(h0: np.ndarray, l0: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """Stockdon et al. (2006) 2% exceedance runup (m above still water level).

    Dissipative (xi0 < 0.3): R2 = 0.043 sqrt(H0 L0).
    Otherwise: R2 = 1.1 (0.35 beta sqrt(H0 L0) + 0.5 sqrt(H0 L0 (0.563 beta^2 + 0.004))).
    NaN slopes give NaN runup.
    """
    h0, l0, beta = (np.asarray(a, float) for a in np.broadcast_arrays(h0, l0, beta))
    hl = np.sqrt(h0 * l0)
    xi = iribarren(beta, h0, l0)
    general = 1.1 * (0.35 * beta * hl + 0.5 * np.sqrt(h0 * l0 * (0.563 * beta ** 2 + 0.004)))
    out = np.where(xi < 0.3, 0.043 * hl, general)
    return np.where(np.isnan(beta), np.nan, out)
