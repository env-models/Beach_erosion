"""Profile geometry: crossings, volumes, slopes, berm proxy.

Convention: x increases seaward from the dune (x=0); z in m MSL; trailing NaN
beyond the survey extent (checked: no interior NaN in TrucVert_OCA.mat).
"""
from __future__ import annotations

import numpy as np

from .constants import HAT_MSL, INTERTIDAL_BAND, Z_DUNE_TOE_PROXY

_trapz = getattr(np, "trapezoid", None) or np.trapz


def valid_extent(z: np.ndarray) -> int:
    """Number of leading finite samples (index of first NaN)."""
    f = np.isfinite(z)
    return int(len(z) if f.all() else np.argmin(f))


def landward_crossing(x: np.ndarray, z: np.ndarray, level: float) -> float:
    """x of the landward-most down-crossing of ``level`` (linear interpolation).

    Scans seaward from the dune and returns the first point where the profile
    drops to ``level``; NaN if the profile never reaches it, ``x[0]`` if it
    starts below it. Avoids the wrong-crossing problem of ``argmin|z-level|``
    on barred/bermed (non-monotonic) profiles (§2.1 item 4).
    """
    n = valid_extent(z)
    zz, xx = z[:n], x[:n]
    below = np.where(zz <= level)[0]
    if below.size == 0:
        return float("nan")
    j = int(below[0])
    if j == 0:
        return float(xx[0])
    z0, z1 = zz[j - 1], zz[j]
    return float(xx[j - 1] + (level - z0) * (xx[j] - xx[j - 1]) / (z1 - z0))


def volume(x: np.ndarray, z: np.ndarray, x_max: float, z_ref: float | None = None) -> float:
    """Profile volume per metre (m3/m) between x=0 and ``x_max``.

    ``z_ref=None``: integral of z (relative to MSL datum).
    ``z_ref=h``: volume of sand above the horizontal plane z=h, i.e. integral of max(z-h, 0).
    NaN if the profile does not cover ``x_max``.
    """
    n = valid_extent(z)
    m = x <= x_max + 1e-9
    if x[n - 1] < x_max - 1e-9:
        return float("nan")
    zz = z[m]
    if z_ref is not None:
        zz = np.maximum(zz - z_ref, 0.0)
    return float(_trapz(zz, x[m]))


def volume_change(x: np.ndarray, z_pre: np.ndarray, z_post: np.ndarray, x_max: float | None = None,
                  z_split: float = HAT_MSL) -> dict[str, float]:
    """Eroded volumes between two surveys over a common window (positive = erosion).

    Window: [0, x_max]; if ``x_max`` is None, the extent covered by BOTH profiles
    (§2.1 item 6). ``upper`` = change of sand above the plane z=z_split,
    ``lower`` = total - upper.
    """
    if x_max is None:
        x_max = float(x[min(valid_extent(z_pre), valid_extent(z_post)) - 1])
    tot = volume(x, z_pre, x_max) - volume(x, z_post, x_max)
    up = volume(x, z_pre, x_max, z_split) - volume(x, z_post, x_max, z_split)
    return {"total": tot, "upper": up, "lower": tot - up, "x_max": x_max}


def berm_volume(x: np.ndarray, z: np.ndarray, z_low: float = HAT_MSL,
                z_toe: float = Z_DUNE_TOE_PROXY) -> float:
    """Berm-volume proxy (m3/m): sand between the planes z_low and z_toe, seaward of the dune toe.

    Dune toe proxy = landward-most down-crossing of ``z_toe``. Volume = integral over
    x >= x_toe of clip(z, z_low, z_toe) - z_low. Captures upper-beach sand stored above
    HAT and below the dune toe (berm/upper beach); NaN if no toe crossing.
    """
    xt = landward_crossing(x, z, z_toe)
    if np.isnan(xt):
        return float("nan")
    n = valid_extent(z)
    m = (x[:n] >= xt)
    zz = np.clip(z[:n][m], z_low, z_toe) - z_low
    return float(_trapz(zz, x[:n][m]))


def intertidal_slope(x: np.ndarray, z: np.ndarray, band: tuple[float, float] = INTERTIDAL_BAND,
                     min_points: int = 20) -> float:
    """Least-squares slope (positive, dz/dx downward seaward) of z in ``band``.

    Uses points landward of the landward-most crossing of the band's lower level
    (or to the survey end if it is never reached). NaN if too few points.
    """
    n = valid_extent(z)
    xx, zz = x[:n], z[:n]
    xl = landward_crossing(xx, zz, band[0])
    lim = xx[-1] if np.isnan(xl) else xl
    m = (zz >= band[0]) & (zz <= band[1]) & (xx <= lim)
    if m.sum() < min_points:
        return float("nan")
    return float(-np.polyfit(xx[m], zz[m], 1)[0])


def foreshore_slope(x: np.ndarray, z: np.ndarray, wl: float, z_top: float = 4.0,
                    fallback_to_end: bool = True) -> float:
    """Mean slope between the still water level ``wl`` and ``z_top`` (notebook's beta for runup).

    Landward-most crossings. If ``wl`` is below the surveyed profile and
    ``fallback_to_end``, the seaward end of the survey is used instead.
    """
    n = valid_extent(z)
    x_top = landward_crossing(x, z, z_top)
    if wl < z[n - 1]:
        if not fallback_to_end:
            return float("nan")
        x_wl, z_wl = x[n - 1], z[n - 1]
    else:
        x_wl, z_wl = landward_crossing(x, z, wl), wl
    if np.isnan(x_top) or np.isnan(x_wl) or x_wl <= x_top:
        return float("nan")
    return float((z_top - z_wl) / (x_wl - x_top))


def foreshore_slope_band(x: np.ndarray, z: np.ndarray, band: tuple[float, float] = (0.0, 3.0),
                         cap: float = 0.2, min_points: int = 5) -> float:
    """Alternative runup slope (A slopefix): least-squares slope of z in a FIXED band [0, +3] m MSL.

    Uses points landward of the landward-most crossing of the band's lower level and caps the
    result at ``cap``. This is one slope per survey, independent of the instantaneous water level, so it cannot blow up
    when the water-level and +4 m crossings are close (the notebook definition). Band and cap
    are choices [verify against Stockdon et al. 2006 foreshore-slope definition, ±2σ around setup].
    """
    n = valid_extent(z)
    xx, zz = x[:n], z[:n]
    xl = landward_crossing(xx, zz, band[0])
    lim = xx[-1] if np.isnan(xl) else xl
    m = (zz >= band[0]) & (zz <= band[1]) & (xx <= lim)
    if m.sum() < min_points:
        return float("nan")
    return float(min(-np.polyfit(xx[m], zz[m], 1)[0], cap))
