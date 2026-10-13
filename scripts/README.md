# scripts/ — download and process external data (Agent B)

[← back to the project README](../README.md) · full provenance: [`../data/README.md`](../data/README.md) ·
report: [`../reports/B_data.md`](../reports/B_data.md)

Run from the repository root with the venv active and Python's isolated mode (`python -I`), never from inside
`data/raw/` (downloaded files are untrusted data). Downloads need network access and write to the git-ignored
`data/raw/`; process scripts read `data/raw/` and write the committed `data/processed/`. All download scripts are
idempotent (existing files are skipped; `--force` refreshes where available). Shortcuts: `make download`,
`make process`.

## Download scripts

| script | fetches | licence | output | options |
|---|---|---|---|---|
| `download_castelle2020.py` | Castelle et al. (2020) Truc Vert DEMs 2003–2019 (325 surveys), hourly wave hindcast, astronomical tide, `Grids.nc`, from OSF project jftw8 (doi:10.17605/OSF.IO/JFTW8); ~196 MB, 329 files | CC0 1.0 (paper CC BY 4.0, cite it) | `data/raw/castelle2020_osf/` + `_manifest.json` | `--workers 6` |
| `download_resourcecode.py` | RESOURCECODE WW3 hindcast, node 94337 (0.35 km from the Cap Ferret buoy), hourly 1994-01 → 2025-03, Hs/Tp/directions/wind | CC BY-SA 4.0 [verify] | `data/raw/resourcecode/node94337_<param>.json` | `--force`, `--params` |
| `download_shom_tidegauges.py` | SHOM/REFMAR observed sea level, hourly: Arcachon-Eyrac (190), Boucau (94), Socoa (95); one month per request | Licence Ouverte 2.0 (presumed [verify]) | `data/raw/shom_refmar/<id>/obs_src4_<year>.json`, `station_metadata.json` | `--start 2003 --end <year> --source 4 --stations 190 94 95` |
| `download_shom_ram.py` | SHOM RAM tidal reference levels (PHMA/HAT, NM, ZH …) via the INSPIRE WFS; prints the sites near Truc Vert | Licence Ouverte 2.0 | `data/raw/shom_ram/ram_wfs.json` | `--force` |
| `download_climate_indices.py` | NAO monthly (NOAA CPC); WEPA (Univ. Plymouth) is attempted but blocked (HTTP 403), download it manually | NAO: US public domain [verify]; WEPA: CC BY-NC-ND (never commit) | `data/raw/climate_indices/` | `--force` |

Not scripted (blocked or not attempted, see `data/README.md` §2c–2e, §5): CANDHIS buoy (API key on request),
Copernicus Marine IBI and ERA5 (credentials), OCA LiDAR, Pléiades DEMs, CoastSat, Biscarrosse surveys.

## Process scripts

| script | reads | writes (`data/processed/`) |
|---|---|---|
| `process_castelle2020.py` | `castelle2020_osf/*.nc` | `trucvert_castelle2020_surveys.parquet`, `…_profiles.parquet` (windows core300 / w740 / w1500), `…_volumes.parquet`, `…_volumes_hat.parquet` (HAT alternatives) |
| `process_waves.py` | `resourcecode/*.json`, Castelle wave netCDF | `waves_resourcecode_node94337.parquet`, `waves_castelle2020.parquet` |
| `process_tide.py` (needs `utide`) | `shom_refmar/`, Castelle tide netCDF | `tide_shom_gauges.parquet` (observed, UTide harmonic tide, non-tidal residual), `tide_trucvert_castelle2020.parquet` |
| `process_climate_indices.py` | `climate_indices/` | `climate_indices.parquet` (NAO monthly + DJFM winter); `wepa_winter_local.parquet` only if WEPA was downloaded manually (not committed) |

The event tables themselves are built by the package, not by these scripts: `python -m evi.events_v2` reads the
processed files above (see [`../src/evi/README.md`](../src/evi/README.md)).
