#!/usr/bin/env python
"""Process climate indices into data/processed/climate_indices.parquet (NAO, monthly + DJFM winter).

Input : data/raw/climate_indices/nao_cpc_monthly.ascii  (scripts/download_climate_indices.py)
        data/raw/climate_indices/wepa_plymouth_Dataset.txt (optional, manual download; CC BY-NC-ND,
        so WEPA is written to a separate, NOT-committed file data/processed/wepa_winter_local.parquet)
Output: data/processed/climate_indices.parquet with columns
          date (first day of month, datetime64), year, month, nao (standardized, CPC),
          winter (int, label = year of the January of the DJFM winter, e.g. 2014 for Dec 2013-Mar 2014; NaN outside DJFM),
          nao_djfm (mean NAO of that DJFM winter, repeated on its months; NaN if the winter is incomplete)
Run with:  python -I scripts/process_climate_indices.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "climate_indices"
OUT = ROOT / "data" / "processed"


def main() -> None:
    nao = pd.read_csv(RAW / "nao_cpc_monthly.ascii", sep=r"\s+", header=None, names=["year", "month", "nao"])
    nao["date"] = pd.to_datetime(dict(year=nao.year, month=nao.month, day=1))
    nao["winter"] = np.where(nao.month == 12, nao.year + 1, np.where(nao.month <= 3, nao.year, np.nan))
    g = nao.dropna(subset=["winter"]).groupby("winter")["nao"].agg(["mean", "count"])
    djfm = g["mean"].where(g["count"] == 4)
    nao["nao_djfm"] = nao["winter"].map(djfm)
    nao = nao[["date", "year", "month", "nao", "winter", "nao_djfm"]]
    nao.attrs = {"source": "NOAA CPC monthly NAO index (norm.nao.monthly.b5001.current.ascii)"}
    nao.to_parquet(OUT / "climate_indices.parquet", index=False)
    print("climate_indices.parquet", len(nao), nao.date.min().date(), nao.date.max().date())

    wepa = RAW / "wepa_plymouth_Dataset.txt"
    if wepa.exists():
        # Format not inspected (download blocked on 2026-10-13); parse whitespace-delimited numbers.
        df = pd.read_csv(wepa, sep=r"[\s,;]+", engine="python", comment="%")
        df.to_parquet(OUT / "wepa_winter_local.parquet", index=False)
        print("wepa_winter_local.parquet", df.shape)
    else:
        print("WEPA raw file absent (manual download needed, see data/README.md)")


if __name__ == "__main__":
    main()
