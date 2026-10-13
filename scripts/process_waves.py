#!/usr/bin/env python
"""Build wave time series parquet files at the Cap Ferret buoy location (44.6525N, -1.45E).

Outputs (data/processed/):
  waves_resourcecode_node94337.parquet  hourly, 1994-01 -> 2025-03 (RESOURCECODE WW3 hindcast, CC BY-SA 4.0)
      columns: time (UTC, tz-naive), hs [m], tp [s] (=1/fp), fp [Hz], dp [deg, peak direction, nautical
               "coming from"], dir [deg, mean direction], spr [deg], t02 [s], t0m1 [s],
               wlv [m, sea surface height used/produced by the hindcast], uwnd, vwnd [m/s], ucur, vcur [m/s],
               source, licence
  waves_castelle2020.parquet            hourly, 2000-01 -> 2020-01 (from Castelle et al. 2020 OSF file
      Waves_TrucVert_2000-2020.nc; WW3 HOMERE + NORGAS-UG hindcasts corrected with CANDHIS 03302, CC0)
      columns: time (UTC), hs [m], tp [s], dm [deg, mean direction], source, licence
Direction convention of each source is copied from the NetCDF/variable metadata; see data/README.md.
Run with:  python -I scripts/process_waves.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"


def resourcecode() -> None:
    d = RAW / "resourcecode"
    cols = {}
    for f in sorted(d.glob("node94337_*.json")):
        p = f.stem.split("_", 1)[1]
        arr = np.array(json.loads(f.read_text())["result"]["data"], dtype=float)
        s = pd.Series(arr[:, 1], index=pd.to_datetime(arr[:, 0].astype("int64"), unit="ms"))
        cols[p] = s[~s.index.duplicated()]
    df = pd.DataFrame(cols).sort_index()
    df.index.name = "time"
    df["tp"] = 1.0 / df["fp"]
    order = ["hs", "tp", "fp", "dp", "dir", "spr", "t02", "t0m1", "wlv", "uwnd", "vwnd", "ucur", "vcur"]
    df = df[[c for c in order if c in df]].reset_index()
    df["source"] = "RESOURCECODE WW3 hindcast node 94337 (-1.449812E, 44.655670N, 52 m)"
    df["licence"] = "CC BY-SA 4.0 (Accensi & Raillard 2022, doi:10.12770/d089a801-c853-49bd-9064-dde5808ff8d8)"
    df.to_parquet(OUT / "waves_resourcecode_node94337.parquet", index=False)
    print("resourcecode", df.shape, df.time.min(), df.time.max())
    print(df.describe().T[["count", "mean", "min", "max"]])


def castelle() -> None:
    import netCDF4

    f = RAW / "castelle2020_osf" / "Waves_TrucVert_2000-2020.nc"
    with netCDF4.Dataset(f) as nc:
        meta = {v: dict(nc[v].__dict__) for v in nc.variables}
        t = np.asarray(nc["waveTime"][:], dtype=float).ravel()
        data = {k: np.asarray(nc[v][:], dtype=float).ravel()
                for k, v in [("hs", "waveHs"), ("tp", "waveTp"), ("dm", "waveDm")]}
    units = meta["waveTime"].get("units", "")
    print("waveTime units:", units, "| Dm attrs:", meta["waveDm"])
    if "0000" in units:  # MATLAB datenum convention 'days since 01-Jan-0000'
        time = pd.to_datetime(t - 719529, unit="D")
    else:
        time = pd.to_datetime(netCDF4.num2date(t, units, only_use_cftime_datetimes=False, only_use_python_datetimes=True))
    data["dm"] = np.mod(data["dm"], 360.0)  # a few raw values exceed 360 deg (max 366.2)
    df = pd.DataFrame({"time": time.round("min"), **data})
    df["source"] = "Castelle et al. 2020 (OSF jftw8) Waves_TrucVert_2000-2020.nc: WW3 HOMERE+NORGAS-UG corrected with CANDHIS 03302"
    df["licence"] = "CC0 1.0"
    df.to_parquet(OUT / "waves_castelle2020.parquet", index=False)
    print("castelle", df.shape, df.time.min(), df.time.max())
    print(df.describe().T)


if __name__ == "__main__":
    resourcecode()
    if (RAW / "castelle2020_osf" / "Waves_TrucVert_2000-2020.nc").exists():
        castelle()
