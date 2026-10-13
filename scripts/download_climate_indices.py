#!/usr/bin/env python
"""Download climate indices: NAO (NOAA CPC, monthly) and WEPA (Univ. Plymouth, winter DJFM).

NAO : NOAA Climate Prediction Center monthly standardized NAO index (1950-present),
      https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii
      US Government work (no copyright restriction in the US) [verify licence wording on CPC site].
WEPA: Scott, Masselink, Castelle, Dodet (2020) "The West Europe Pressure Anomaly: 1943-2018",
      University of Plymouth dataset, doi:10.24382/35ae12b5-df54-479d-ad09-75ea5049d14f,
      licence CC BY-NC-ND (as shown on the dataset page). Index defined in
      Castelle et al. (2017) GRL 44, doi:10.1002/2016GL072379.

Writes raw files to data/raw/climate_indices/. Idempotent (skips existing files unless --force).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "climate_indices"
SOURCES = {
    "nao_cpc_monthly.ascii": "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii",
    "wepa_plymouth_Dataset.txt": "https://researchportal.plymouth.ac.uk/files/49375705/Dataset.txt",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download (NAO file is updated monthly)")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        dest = OUT / name
        if dest.exists() and not args.force:
            print("skip", name)
            continue
        r = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0 (research data download)"})
        if r.status_code != 200 or r.headers.get("content-type", "").startswith("text/html"):
            # 2026-10-13: both Plymouth endpoints sit behind a Cloudflare browser challenge (HTTP 403).
            print(f"BLOCKED {name}: HTTP {r.status_code} from {url}.\n"
                  f"  Download it manually in a browser (also mirrored at "
                  f"https://pearl.plymouth.ac.uk/fose-datasets/45) and save it as {dest}")
            continue
        dest.write_bytes(r.content)
        print("ok", name, len(r.content), "bytes")


if __name__ == "__main__":
    main()
