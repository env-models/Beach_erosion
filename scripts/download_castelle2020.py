#!/usr/bin/env python
"""Download the Castelle et al. (2020) Truc Vert topographic survey dataset.

Paper : Castelle, Bujan, Marieu & Ferreira (2020), Scientific Data 7:410,
        doi:10.1038/s41597-020-00750-5
Data  : Open Science Framework project jftw8, doi:10.17605/OSF.IO/JFTW8
Licence (OSF node licence, checked 2026-10-13 via api.osf.io): CC0 1.0 Universal.

Files are listed through the public OSF v2 API (paginated) and written to
data/raw/castelle2020_osf/. Idempotent: a file is skipped when it already
exists locally with the size reported by OSF. A manifest (file name, size,
OSF download URL, md5/sha256 if provided) is written next to the files.

Usage:  python scripts/download_castelle2020.py [--workers 6]
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

NODE = "jftw8"
API = f"https://api.osf.io/v2/nodes/{NODE}/files/osfstorage/"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "castelle2020_osf"


def list_files(url: str, prefix: str = "") -> list[dict]:
    files = []
    while url:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        d = r.json()
        for item in d["data"]:
            a = item["attributes"]
            if a["kind"] == "folder":
                sub = item["relationships"]["files"]["links"]["related"]["href"]
                files += list_files(sub, prefix + a["name"] + "/")
            else:
                files.append({
                    "name": prefix + a["name"],
                    "size": a.get("size"),
                    "download": item["links"]["download"],
                    "hashes": (a.get("extra") or {}).get("hashes", {}),
                    "date_modified": a.get("date_modified"),
                })
        url = d["links"].get("next")
    return files


def fetch(f: dict) -> str:
    dest = OUT / f["name"]
    if dest.exists() and f["size"] is not None and dest.stat().st_size == f["size"]:
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(f["download"], stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
    tmp.rename(dest)
    return "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    files = list_files(API)
    (OUT / "_manifest.json").write_text(json.dumps(files, indent=1))
    print(f"{len(files)} files listed on OSF node {NODE}")
    with ThreadPoolExecutor(args.workers) as ex:
        res = list(ex.map(fetch, files))
    print({k: res.count(k) for k in set(res)})
    bad = [f["name"] for f in files if f["size"] and (OUT / f["name"]).stat().st_size != f["size"]]
    if bad:
        print("size mismatch:", bad, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
