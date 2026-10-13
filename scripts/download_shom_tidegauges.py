#!/usr/bin/env python
"""Download observed sea levels from SHOM / REFMAR tide gauges (data.shom.fr web service).

Stations (SHOM ids from https://services.data.shom.fr/maregraphie/service/tidegauges):
    190 ARCACHON_EYRAC        (-1.16355E, 44.66500N; inside Arcachon lagoon, ~30 km from Truc Vert)
     94 BAYONNE_BOUCAU        (-1.51483E, 43.52732N)
     95 SAINT-JEAN-DE-LUZ_SOCOA (-1.68162E, 43.39524N)

Endpoint (undocumented public JSON service used by data.shom.fr, probed 2026-10-13):
    https://services.data.shom.fr/maregraphie/observation/json/{id}?sources={s}&dtStart=...&dtEnd=...
Source codes observed empirically: 1 = raw high-frequency (~1 min), 3 = 10-min, 4 = hourly
[verify exact SHOM definitions, e.g. validated vs raw, on refmar.shom.fr].
Heights are in metres above the local chart datum (zero hydrographique, ZH); timestamps are UTC
(station metadata 'fuseau_horaire' = 0). Datum offsets are saved from the station metadata
endpoint .../service/completetidegauge/{id} ('verticalRef').

Writes one JSON file per station, source and calendar year to data/raw/shom_refmar/<id>/.
Idempotent: existing yearly files are skipped (the current year is always refreshed).
Usage: python scripts/download_shom_tidegauges.py [--start 2000] [--end 2026] [--source 4] [--stations 190 94 95]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "shom_refmar"
BASE = "https://services.data.shom.fr/maregraphie"


def get(url: str, params: dict | None = None) -> requests.Response:
    for attempt in range(4):
        try:
            r = requests.get(url, params=params, timeout=180)
            if r.status_code == 200:
                return r
        except requests.RequestException:
            pass
        time.sleep(5 * (attempt + 1))
    r.raise_for_status()
    return r


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=2003)
    ap.add_argument("--end", type=int, default=dt.date.today().year)
    ap.add_argument("--source", type=int, default=4)
    ap.add_argument("--stations", nargs="+", default=["190", "94", "95"])
    a = ap.parse_args()
    this_year = dt.date.today().year
    for sid in a.stations:
        d = OUT / sid
        d.mkdir(parents=True, exist_ok=True)
        meta = d / "station_metadata.json"
        if not meta.exists():
            meta.write_text(get(f"{BASE}/service/completetidegauge/{sid}").text)
        for y in range(a.start, a.end + 1):
            f = d / f"obs_src{a.source}_{y}.json"
            if f.exists() and y != this_year:
                continue
            # The service silently truncates responses at ~745 records, so query month by month
            # (hourly source 4 -> <= 744 records/month) and concatenate into one yearly file.
            rows = []
            for m in range(1, 13):
                t0 = dt.datetime(y, m, 1)
                t1 = dt.datetime(y + (m == 12), m % 12 + 1, 1)
                if t0 > dt.datetime.now(dt.timezone.utc).replace(tzinfo=None):
                    break
                params = {"sources": a.source, "dtStart": t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
                          "dtEnd": t1.strftime("%Y-%m-%dT%H:%M:%SZ")}
                chunk = get(f"{BASE}/observation/json/{sid}", params).json().get("data", [])
                if len(chunk) > 745:  # 31-day month, hourly, inclusive end = 745 records
                    print(f"WARNING {sid} {y}-{m:02d}: {len(chunk)} records, possible truncation")
                rows += chunk
                time.sleep(0.2)
            f.write_text(json.dumps({"data": rows}))
            print(sid, y, len(rows), "records")


if __name__ == "__main__":
    main()
