#!/usr/bin/env python
"""Build water-level products: observed tide gauges, harmonic tide, non-tidal residual (surge),
and the Castelle et al. (2020) astronomical tide at Truc Vert.

Inputs : data/raw/shom_refmar/<id>/obs_src4_<year>.json + station_metadata.json (download_shom_tidegauges.py)
         data/raw/castelle2020_osf/Astronomical_Tide_TrucVert_2000-2020.nc (download_castelle2020.py)
Outputs (data/processed/):
  tide_shom_gauges.parquet   hourly, one row per (station, time):
      station (SHOM id), name, time (UTC), eta_zh [m above chart datum], eta_ign69 [m NGF-IGN69,
      = eta_zh + zh_ref], eta_tide_ign69 [m, UTide harmonic prediction fitted on the station's own
      record 2003-2026, IGN69], residual [m, = eta - tide; 'non-tidal residual' ~ surge + seasonal +
      mean-sea-level variability not in the fit], source, licence
  tide_trucvert_castelle2020.parquet  hourly (sub-sampled from 10 min): time (UTC), tide_msl [m above
      MSL = IGN69 - 0.40 m], tide_ign69 [m]; astronomical only (no surge / set-up), CC0.
Harmonic analysis: utide.solve on the hourly IGN69 series (constit='auto', method='ols',
conf_int='none', trend=False, Rayleigh criterion default), utide.reconstruct on the same times.
Run with:  python -I scripts/process_tide.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
MSL_IGN69 = 0.40  # Castelle et al. 2020: MSL = IGN69 - 0.40 m


def load_station(d: Path) -> tuple[pd.DataFrame, dict]:
    meta = json.loads((d / "station_metadata.json").read_text())
    rows = []
    for f in sorted(d.glob("obs_src4_*.json")):
        rows += json.loads(f.read_text()).get("data", [])
    df = pd.DataFrame(rows)
    if df.empty:
        return df, meta
    df["time"] = pd.to_datetime(df["timestamp"], format="%Y/%m/%d %H:%M:%S")
    df = df.drop_duplicates("time").sort_values("time")
    zh_ref = float(meta["verticalRef"]["zh_ref"])  # chart datum height in IGN69 (e.g. -1.98 at Arcachon)
    out = pd.DataFrame({"time": df["time"].values, "eta_zh": df["value"].astype(float).values})
    out["eta_ign69"] = out["eta_zh"] + zh_ref
    return out, meta


def harmonic(df: pd.DataFrame, lat: float) -> np.ndarray:
    import utide

    t = df["time"].to_numpy()
    y = df["eta_ign69"].to_numpy()
    ok = np.isfinite(y)
    coef = utide.solve(t[ok], y[ok], lat=lat, method="ols", conf_int="none", trend=False, verbose=False)
    return utide.reconstruct(t, coef, verbose=False).h


def main() -> None:
    frames = []
    for d in sorted((RAW / "shom_refmar").iterdir()):
        if not d.is_dir():
            continue
        df, meta = load_station(d)
        if df.empty:
            continue
        df["eta_tide_ign69"] = harmonic(df, float(meta["latitude"]))
        df["residual"] = df["eta_ign69"] - df["eta_tide_ign69"]
        df.insert(0, "name", meta["name"])
        df.insert(0, "station", int(meta["shom_id"]))
        df["source"] = "SHOM/REFMAR via services.data.shom.fr (source 4, hourly)"
        df["licence"] = "Licence Ouverte Etalab v2.0; cite SHOM REFMAR doi:10.17183/REFMAR#RONIM"
        print(meta["name"], len(df), df.time.min(), df.time.max(),
              "residual std %.3f m, 99.9%% %.2f m" % (df.residual.std(), df.residual.quantile(0.999)))
        frames.append(df)
    g = pd.concat(frames, ignore_index=True)
    g.to_parquet(OUT / "tide_shom_gauges.parquet", index=False)
    print("tide_shom_gauges.parquet", g.shape)

    f = RAW / "castelle2020_osf" / "Astronomical_Tide_TrucVert_2000-2020.nc"
    if f.exists():
        import netCDF4

        with netCDF4.Dataset(f) as nc:
            t = np.asarray(nc["tideTime"][:], dtype=float)
            h = np.asarray(nc["Tide"][:], dtype=float)
        s = pd.Series(h, index=pd.to_datetime(t - 719529, unit="D").round("min"))
        s = s[s.index.minute == 0]
        tv = pd.DataFrame({"time": s.index, "tide_msl": s.values})
        tv["tide_ign69"] = tv["tide_msl"] + MSL_IGN69
        tv.to_parquet(OUT / "tide_trucvert_castelle2020.parquet", index=False)
        print("tide_trucvert_castelle2020.parquet", tv.shape, tv.time.min(), tv.time.max())


if __name__ == "__main__":
    main()
