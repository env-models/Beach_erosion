#!/usr/bin/env python
"""Turn the Castelle et al. (2020) Truc Vert DEMs into longshore-averaged profiles and volumes.

Input : data/raw/castelle2020_osf/{Monitoring,ECORS08}_TrucVert_YYYY-MM-DD.nc + Grids.nc
        (scripts/download_castelle2020.py; OSF doi:10.17605/OSF.IO/JFTW8, CC0 1.0)
Method:
  * Each survey file holds raw DGPS points and `zg`, a DEM kriged by the authors on a regular local
    grid (Grids.nc): zg[i, j] with cross-shore xl = 20 + 2 i m (176 pts) and alongshore
    yl = -2000 + 20 j m (176 pts). The [i, j] orientation was checked against the raw points
    (nearest-cell RMSE 4-8 cm vs > 1 m for the transpose).
  * NOTE: although the NetCDF attribute says "cross-shore coordinate is positive onshore", in the
    data z decreases with xl (xl ~ 40 m is the dune crest at ~ +10.8 m, xl ~ 170 m is ~ MSL), i.e. xl
    increases SEAWARD - the same orientation as the legacy TrucVert_OCA.mat x (0 = dune, seaward +).
  * Elevations are metres above MSL as provided by the authors (MSL = NGF-IGN69 - 0.40 m; the
    legacy 2017 profiles use MSL = IGN69 - 0.39 m, a 1 cm difference that is NOT corrected here).
  * Longshore averaging: for each alongshore window below and each xl, z is the mean of the finite
    DEM cells inside the window, kept only if >= 80 % of the window cells are finite (else NaN).
      core300 : yl in [-440, -160] m (15 cells, 280 m) - surveyed in almost every survey 2003-2019,
                the only window that is consistent over the whole record.
      w740    : yl in [-700, 40] m (38 cells) - comparable to the thesis' 750 m window (2009-2011+).
      w1500   : yl in [-1100, 400] m (76 cells) - comparable to the thesis' 1500 m window (2013+).
  * Volumes (m3 per m alongshore) over a FIXED cross-shore window xl in [70, 170] m
    (dune toe/face at ~ +5 m down to ~ MSL; covered in >= 92 % of core300 profiles):
      v_total = int (z - Z_REF) dx with Z_REF = -1.5 m MSL
      v_upper = int max(z - 1.75, 0) dx   (above HAT = +2.14 m IGN69 ~ +1.75 m MSL)
      v_lower = int (min(z, 1.75) - Z_REF) dx,  so v_total = v_upper + v_lower
    Internal gaps of <= 10 m are linearly interpolated before integrating (trapezoid rule);
    `vol_valid` is True only if the profile is finite over the whole window after that.
Outputs (data/processed/):
  trucvert_castelle2020_surveys.parquet  one row per survey: survey_id, date, campaign
      (Monitoring|ECORS08), n_points, raw point extents (xl/yl min/max), DEM alongshore extent
      on the upper beach (yl_dem_min/max), and per-window flags have_<window>.
  trucvert_castelle2020_profiles.parquet long format: survey_id, date, campaign, window, xl,
      x_legacy (= xl - 40 m, see below), z, frac_cells (fraction of window cells finite at that xl).
  Cross-check with the legacy datasets/TrucVert_OCA.mat (2026-10-13): 165 of the 168 legacy survey
  dates are in this dataset (missing: 2005-06-06, 2012-02-08, 2012-03-09). Best-fit cross-shore shift
  legacy_x = xl - 40 m; RMSE legacy-vs-w1500 (2012-2015, 58 profiles) 0.09 m, bias +0.01 m;
  legacy-vs-w740 (2009-2011, 45 profiles) 0.11 m; legacy-vs-core300 (2005-2008) 0.22 m.
  trucvert_castelle2020_volumes.parquet  survey_id, date, campaign, window, v_total, v_upper,
      v_lower, vol_valid, xl_min_valid, xl_max_valid, z_at_xl70, z_at_xl170.
Run with:  python -I scripts/process_castelle2020.py
"""
from __future__ import annotations

import warnings
from pathlib import Path

import netCDF4
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "castelle2020_osf"
OUT = ROOT / "data" / "processed"

XL = 20.0 + 2.0 * np.arange(176)
YL = -2000.0 + 20.0 * np.arange(176)
WINDOWS = {"core300": (-440.0, -160.0), "w740": (-700.0, 40.0), "w1500": (-1100.0, 400.0)}
MIN_FRAC = 0.8
VOL_X = (70.0, 170.0)
Z_REF = -1.5
Z_HAT = 1.75
MAX_GAP = 10.0
X_LEGACY_SHIFT = 40.0  # legacy TrucVert_OCA.mat x = xl - 40 m (best fit, see docstring)


def fill_small_gaps(x: np.ndarray, z: np.ndarray, max_gap: float) -> np.ndarray:
    z = z.copy()
    ok = np.isfinite(z)
    if ok.sum() < 2:
        return z
    idx = np.where(ok)[0]
    for a, b in zip(idx[:-1], idx[1:]):
        if b - a > 1 and x[b] - x[a] <= max_gap:
            z[a + 1:b] = np.interp(x[a + 1:b], [x[a], x[b]], [z[a], z[b]])
    return z


def volumes(z: np.ndarray) -> dict:
    zf = fill_small_gaps(XL, z, MAX_GAP)
    m = (XL >= VOL_X[0]) & (XL <= VOL_X[1])
    x, zz = XL[m], zf[m]
    fin = np.isfinite(zf)
    out = {
        "xl_min_valid": float(XL[fin].min()) if fin.any() else np.nan,
        "xl_max_valid": float(XL[fin].max()) if fin.any() else np.nan,
        "z_at_xl70": float(zf[XL == VOL_X[0]][0]),
        "z_at_xl170": float(zf[XL == VOL_X[1]][0]),
    }
    valid = bool(np.isfinite(zz).all())
    out["vol_valid"] = valid
    if valid:
        out["v_upper"] = float(np.trapezoid(np.maximum(zz - Z_HAT, 0.0), x))
        out["v_lower"] = float(np.trapezoid(np.minimum(zz, Z_HAT) - Z_REF, x))
        out["v_total"] = out["v_upper"] + out["v_lower"]
    else:
        out.update(v_upper=np.nan, v_lower=np.nan, v_total=np.nan)
    return out


def main() -> None:
    files = sorted(list(RAW.glob("Monitoring_TrucVert_*.nc")) + list(RAW.glob("ECORS08_TrucVert_*.nc")),
                   key=lambda p: (p.stem.split("_")[-1], p.stem))
    surveys, profiles, vols = [], [], []
    upper = (XL >= 150) & (XL <= 220)
    for f in files:
        campaign = f.stem.split("_")[0]
        with netCDF4.Dataset(f) as nc:
            datenum = float(np.asarray(nc["Date"][:]).ravel()[0])
            zg = np.ma.filled(nc["zg"][:].astype(float), np.nan)
            xl = np.asarray(nc["xl"][:], dtype=float)
            yl = np.asarray(nc["yl"][:], dtype=float)
            date_attr = nc.getncattr("date")
        date = pd.to_datetime(datenum - 719529, unit="D")  # MATLAB datenum -> datetime
        sid = f"{campaign}_{date_attr}"
        cov_y = np.isfinite(zg[upper, :]).mean(axis=0) > 0.9
        row = {"survey_id": sid, "date": date, "campaign": campaign, "n_points": xl.size,
               "xl_raw_min": xl.min(), "xl_raw_max": xl.max(), "yl_raw_min": yl.min(), "yl_raw_max": yl.max(),
               "yl_dem_min": YL[cov_y].min() if cov_y.any() else np.nan,
               "yl_dem_max": YL[cov_y].max() if cov_y.any() else np.nan}
        for w, (y0, y1) in WINDOWS.items():
            cols = (YL >= y0) & (YL <= y1)
            sub = zg[:, cols]
            frac = np.isfinite(sub).mean(axis=1)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                z = np.where(frac >= MIN_FRAC, np.nanmean(sub, axis=1), np.nan)
            row[f"have_{w}"] = bool(np.isfinite(z).any())
            if not np.isfinite(z).any():
                continue
            profiles.append(pd.DataFrame({"survey_id": sid, "date": date, "campaign": campaign, "window": w,
                                          "xl": XL, "x_legacy": XL - X_LEGACY_SHIFT, "z": z, "frac_cells": frac}).dropna(subset=["z"]))
            vols.append({"survey_id": sid, "date": date, "campaign": campaign, "window": w, **volumes(z)})
        surveys.append(row)
    s = pd.DataFrame(surveys)
    p = pd.concat(profiles, ignore_index=True)
    v = pd.DataFrame(vols)[["survey_id", "date", "campaign", "window", "v_total", "v_upper", "v_lower", "vol_valid",
                            "xl_min_valid", "xl_max_valid", "z_at_xl70", "z_at_xl170"]]
    for name, df in [("surveys", s), ("profiles", p), ("volumes", v)]:
        df.to_parquet(OUT / f"trucvert_castelle2020_{name}.parquet", index=False)
        print(name, df.shape)
    print(v.groupby("window")["vol_valid"].agg(["size", "sum"]))
    print(s.groupby([s.date.dt.year, "campaign"]).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()
