#!/usr/bin/env python
"""Download the RESOURCECODE WAVEWATCH III hindcast time series at the node nearest the
Cap Ferret CANDHIS buoy (44.6525N, -1.45E).

Database : RESOURCECODE metocean hindcast (Ifremer), hourly, 1994-01 -> 2025-03 at the time
           of download (2026-10-13). Public API used by the official `resourcecode` Python
           toolbox (v2.1.0, config.ini: cassandra-base-url = https://resourcecode-datacharts.ifremer.fr/),
           endpoint  api/timeseries?node=<node-1>&parameter=<p>&start=<ISO Z>&end=<ISO Z>.
Node     : FIELD-grid node 94337 (1-based, as in the toolbox grid table; API index 94336),
           -1.449812E 44.655670N, depth 52 m, 0.35 km from the buoy position.
Licence  : see data/README.md (checked separately) [verify].

Writes data/raw/resourcecode/node94337_<param>.json (one JSON per parameter).
Idempotent: skips parameters already downloaded (use --force to refresh).
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "resourcecode"
URL = "https://resourcecode-datacharts.ifremer.fr/api/timeseries"
NODE_1BASED = 94337
PARAMS = ["hs", "fp", "dp", "dir", "spr", "t02", "t0m1", "wlv", "uwnd", "vwnd", "ucur", "vcur"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--params", nargs="+", default=PARAMS)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for p in a.params:
        f = OUT / f"node{NODE_1BASED}_{p}.json"
        if f.exists() and not a.force:
            print("skip", f.name)
            continue
        q = {"node": NODE_1BASED - 1, "parameter": p,
             "start": "1994-01-01T00:00:00Z", "end": "2030-01-01T00:00:00Z"}
        for attempt in range(4):
            r = requests.get(URL, params=q, timeout=600)
            if r.ok and "result" in r.json():
                break
            time.sleep(10 * (attempt + 1))
        r.raise_for_status()
        d = r.json()
        f.write_text(json.dumps(d))
        print("ok", p, d["result"]["dataSetSize"], "records")


if __name__ == "__main__":
    main()
