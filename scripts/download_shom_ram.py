#!/usr/bin/env python
"""Download SHOM 'Références Altimétriques Maritimes' (RAM) via the public INSPIRE WFS and print
the tidal reference levels of the sites around Truc Vert.

Source : SHOM RAM (data.gouv.fr dataset 'references-altimetriques-maritimes', licence: Licence Ouverte v2.0 'lov2'),
         WFS https://services.data.shom.fr/INSPIRE/wfs, typeName RAM_BDD_WLD_WGS84G_WFS:ram_3857
Fields : phma (HAT), pmve (MHWS), pmme (MHWN), nm (mean level), bmve, bmme, pbma (LAT) in metres above
         chart datum (ZH); zh_ref = height of ZH in the land datum `reference` (IGN69) -> level_IGN69 = level_ZH + zh_ref.
Output : data/raw/shom_ram/ram_wfs.json (idempotent; --force to refresh)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "shom_ram"
URL = ("https://services.data.shom.fr/INSPIRE/wfs?service=WFS&version=2.0.0&request=GetFeature"
       "&typeNames=RAM_BDD_WLD_WGS84G_WFS:ram_3857&outputFormat=application/json&count=5000")
SITES = ["Cap Ferret", "Arcachon", "Le Grand Piquey", "Pilat Plage", "Lacanau", "Biscarrosse", "Boucau-Bayonne"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "ram_wfs.json"
    if a.force or not f.exists():
        r = requests.get(URL, timeout=120)
        r.raise_for_status()
        f.write_text(r.text)
    feats = json.loads(f.read_text())["features"]
    print(f"{len(feats)} RAM sites")
    hdr = ("site", "zh_ref", "phma", "pmve", "nm", "pbma", "PHMA_IGN69", "NM_IGN69", "PHMA-NM")
    print("\t".join(hdr))
    for x in feats:
        p = x["properties"]
        if p["site"] in SITES:
            z = p["zh_ref"]
            ign = (lambda v: f"{v + z:.2f}") if z is not None else (lambda v: "n/a")
            print("\t".join(str(v) for v in (p["site"], z, p["phma"], p["pmve"], p["nm"], p["pbma"],
                                               ign(p["phma"]), ign(p["nm"]), f"{p['phma'] - p['nm']:.2f}")))


if __name__ == "__main__":
    main()
