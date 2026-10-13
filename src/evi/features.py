"""Per-timestep hydrodynamic features: profile in force, slope, R2%, TWL, HAT exceedance."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .constants import DEPTH_SHOAL, HAT_MSL, Z_SLOPE_TOP
from .io import Profiles
from .profiles import foreshore_slope
from .runup import deep_water_wavelength, deshoal, stockdon_r2


def profile_in_force(t_unix: np.ndarray, prof_t_unix: np.ndarray) -> np.ndarray:
    """Index of the last survey strictly before each time (-1 if none). No look-ahead."""
    return np.searchsorted(prof_t_unix, t_unix, side="left") - 1


def timestep_features(hydro: pd.DataFrame, prof: Profiles, hat: float = HAT_MSL,
                      z_top: float = Z_SLOPE_TOP, depth: float = DEPTH_SHOAL) -> pd.DataFrame:
    """Return per-timestep ``p_idx, beta, H0, L0, R2, twl, exceed_hat``.

    beta: mean slope between still water level and ``z_top`` on the pre-existing
    survey (landward-most crossings; seaward survey end used when the water level
    is below the surveyed profile). H0: linear de-shoaling from ``depth`` with the
    exact dispersion relation. TWL = wl (MARS2D tide+surge) + R2%.
    """
    p_idx = profile_in_force(hydro["t_unix"].values, prof.t_unix)
    wl = hydro["wl"].values
    beta = np.full(len(hydro), np.nan)
    for n, (p, w) in enumerate(zip(p_idx, wl)):
        if p >= 0:
            beta[n] = foreshore_slope(prof.x, prof.z[p], float(w), z_top)
    l0 = deep_water_wavelength(hydro["tp"].values)
    h0 = deshoal(hydro["hs"].values, hydro["tp"].values, depth, exact=True)
    r2 = stockdon_r2(h0, l0, beta)
    twl = wl + r2
    return pd.DataFrame({"p_idx": p_idx, "beta": beta, "H0": h0, "L0": l0, "R2": r2,
                         "twl": twl, "exceed_hat": twl >= hat}, index=hydro.index)
