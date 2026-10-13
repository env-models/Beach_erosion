"""Wave energy metrics with explicit units (§2.1 item 1).

All take Hs (m) [and Tp (s)] per time step and a time step ``dt_h`` in hours.
"""
from __future__ import annotations

import numpy as np

from .constants import DT_HOURS, G, G_NB, RHO, RHO_NB


def energy_density(hs: np.ndarray, rho: float = RHO, g: float = G) -> np.ndarray:
    """Wave energy density E = (1/16) rho g Hs^2, J/m^2."""
    return rho * g * np.asarray(hs, float) ** 2 / 16.0


def energy_flux(hs: np.ndarray, tp: np.ndarray, rho: float = RHO, g: float = G) -> np.ndarray:
    """Deep-water energy flux P = rho g^2 Hs^2 Tp / (64 pi), W/m (= J/s/m).

    Uses Tp as the thesis did (strictly Te/Tm-1,0 is the energy period).
    """
    return rho * g ** 2 * np.asarray(hs, float) ** 2 * np.asarray(tp, float) / (64 * np.pi)


def e_notebook(hs: np.ndarray, dt_h: float = DT_HOURS) -> np.ndarray:
    """The notebook quantity (1/16) rho g Hs^2 * dt[hours] / 1e6.

    Units: 1e6 J h m^-2 ("MJ.h/m^2"); labelled "MJ/m" or "MJ/m^2" in notebook and thesis.
    Multiply by 3600 to get MJ s m^-2.
    """
    return energy_density(hs, RHO_NB, G_NB) * dt_h / 1e6


def e_hs2dt(hs: np.ndarray, dt_h: float = DT_HOURS) -> np.ndarray:
    """Hs^2 dt, m^2 h (Harley et al. 2009-style storm 'energy')."""
    return np.asarray(hs, float) ** 2 * dt_h


def e_density_dt(hs: np.ndarray, dt_h: float = DT_HOURS) -> np.ndarray:
    """Time-integrated energy density (1/16) rho g Hs^2 dt, in MJ s m^-2."""
    return energy_density(hs) * dt_h * 3600.0 / 1e6


def p_flux_dt(hs: np.ndarray, tp: np.ndarray, dt_h: float = DT_HOURS) -> np.ndarray:
    """Time-integrated energy flux P dt, in MJ/m (energy delivered per metre of crest)."""
    return energy_flux(hs, tp) * dt_h * 3600.0 / 1e6
