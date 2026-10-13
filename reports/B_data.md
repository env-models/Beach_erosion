# B — Data expansion report (Agent B)

Prepared 2026-10-13 on branch `revisit-2026`. Full provenance for every source is in `data/README.md`.
"Verified" means the DOI/URL resolved on 2026-10-13 and the data were downloaded and opened.

## 1. Source status

| # | Source | Licence | Coverage | Status | Verified |
|---|---|---|---|---|---|
| 1 | **Castelle et al. 2020 Truc Vert DEMs** (OSF doi:10.17605/OSF.IO/JFTW8; paper doi:10.1038/s41597-020-00750-5) | CC0 1.0 (OSF node) | 2003-09-10 → 2019-12-26, 325 surveys (294 Monitoring + 31 ECORS'08) | **downloaded + processed** | yes |
| 1b | Post-2019 Truc Vert surveys (SNO DYNALIT / OCA / OSF) | — | — | **not found** (OSF node modified 2025-03 but no files after 2019-12-26) | — |
| 2a | **RESOURCECODE WW3 hindcast**, node 94337, 0.35 km from the buoy (doi:10.12770/d089a801-c853-49bd-9064-dde5808ff8d8) | CC BY-SA 4.0 (Sextant record also says "Copyright" [verify]) | 1994-01 → 2025-03, hourly, Hs/Tp/Dp/Dm/spread/wind | **downloaded + processed** | yes |
| 2b | **Castelle 2020 wave file** (WW3 HOMERE + NORGAS-UG, CANDHIS-corrected) | CC0 | 2000 → 2019, hourly, Hs/Tp/Dm | **downloaded + processed** | yes |
| 2c | CANDHIS 03302 Cap Ferret buoy | Etalab Licence Ouverte 2.0 | — | **blocked**: the API key must be requested by email to Cerema, and contacting people is the owner's call. The manual "Archives" tab on the website was not tested [verify] | site yes |
| 2d | Copernicus Marine IBI wave reanalysis | CMEMS licence | — | **blocked**: no account/credentials on this machine | — |
| 2e | ERA5 waves (CDS) | Copernicus licence | — | **blocked**: no `~/.cdsapirc` | — |
| 3a | **SHOM/REFMAR tide gauges**: Arcachon-Eyrac (190), Boucau (94), Socoa (95) | Licence Ouverte 2.0, doi:10.17183/REFMAR#RONIM | 2003 → 2026-06, hourly (gaps: Arcachon 2013, 2014, 2016) | **downloaded + processed** (UTide harmonic fit + residual) | yes |
| 3b | **Castelle 2020 astronomical tide at Truc Vert** (7 m depth) | CC0 | 2000 → 2020, 10 min (hourly output) | **downloaded + processed** | yes |
| 3c | SHOM official tide predictions | — | — | not downloaded (needs an API key [verify]); replaced by the UTide fit | — |
| 4a | **NAO** (NOAA CPC monthly) | US Gov. public domain [verify wording] | 1950-01 → 2026-09 | **downloaded + processed** | yes |
| 4b | WEPA (Scott et al. 2020, doi:10.24382/35ae12b5-df54-479d-ad09-75ea5049d14f; index paper doi:10.1002/2016GL072379) | **CC BY-NC-ND 4.0** | 1943–2018, winter | **blocked**: Cloudflare browser challenge (HTTP 403). Download manually; the script processes it but it must not be committed | yes (DOIs) |
| 5 | CoastSat / SDS Benchmark (Truc Vert), OCA LiDAR, Pléiades DEMs, Biscarrosse EPOC | various | — | recorded only (see `data/README.md` §5) | partly |

## 2. How much the Castelle dataset adds

**The legacy 2017 profile set is a subset of the Castelle dataset.**
- 165 of the 168 legacy survey dates are present. The three missing dates are 2005-06-06, 2012-02-08 and 2012-03-09.
- After a cross-shore shift of `legacy_x = xl − 40 m`, the legacy profiles match the re-averaged Castelle profiles with
  RMSE 0.09 m against the 1500 m window for 2012–2015 (bias +0.01 m), and 0.11 m against the 750 m window for 2009–2011.
- So the extension is a *superset* of the 2017 data, processed the same way. It is not a different instrument.

### Surveys per year

`castelle_all` counts all files. `*_vol_valid` counts surveys whose longshore-averaged profile fully covers the
fixed volume window xl ∈ [70, 170] m (see data/README.md §1). `legacy_2017` is `datasets/TrucVert_OCA.mat`.

| Year | castelle_all | Monitoring | ECORS08 | core300 vol-valid | w740 vol-valid | w1500 vol-valid | legacy_2017 |
|---|---|---|---|---|---|---|---|
| 2003 | 7 | 7 | 0 | 5 | 0 | 0 | 0 |
| 2004 | 18 | 18 | 0 | 17 | 0 | 0 | 0 |
| 2005 | 15 | 15 | 0 | 13 | 0 | 0 | 10 |
| 2006 | 10 | 10 | 0 | 9 | 0 | 0 | 10 |
| 2007 | 10 | 10 | 0 | 8 | 0 | 0 | 10 |
| 2008 | 32 | 1 | 31 | 27 | 5 | 2 | 3 |
| 2009 | 17 | 17 | 0 | 15 | 1 | 0 | 17 |
| 2010 | 21 | 21 | 0 | 17 | 13 | 0 | 21 |
| 2011 | 22 | 22 | 0 | 20 | 20 | 0 | 22 |
| 2012 | 22 | 22 | 0 | 19 | 19 | 3 | 20 |
| 2013 | 22 | 22 | 0 | 20 | 21 | 21 | 22 |
| 2014 | 24 | 24 | 0 | 18 | 20 | 21 | 24 |
| 2015 | 20 | 20 | 0 | 20 | 20 | 20 | 9 |
| 2016 | 19 | 19 | 0 | 19 | 19 | 17 | 0 |
| 2017 | 21 | 21 | 0 | 21 | 21 | 21 | 0 |
| 2018 | 24 | 24 | 0 | 24 | 22 | 22 | 0 |
| 2019 | 21 | 21 | 0 | 21 | 5 | 15 | 0 |
| **total** | **325** | **294** | **31** | **293** | **186** | **142** | **168** |

That is **157 more surveys** than the legacy set (325 vs 168): 2003–2004 (+25), the ECORS'08 daily campaign (+31 in
2008), the second half of 2015 (+11) and 2016–2019 (+85).

### Plausible number of events

This is a first screen, not Agent A's event definition.
- **Method**: take consecutive pairs of `core300`, vol-valid Monitoring surveys and keep the intervals containing at
  least one hour with RESOURCECODE Hs > 4.3 m (the thesis Hs95 threshold).
- **Result**: 266 intervals, of which **103 contain a storm**. The median survey gap is 16 days.
- Of those 103, 45 start in 2009–2015 and **58 start outside 2009–2015** (2003–2008: 27; 2016–2019: 35).
- Adding the ECORS'08 surveys gives 110 storm intervals, but these daily surveys split single storms into several intervals.
- Compare with 51 storms and 37 resolvable events in the 2017 calibration and the handoff's estimate of "80–120 with
  extended data". The extended record lands at the top of that range before any HAT/TWL filtering.
- **Caveat**: RESOURCECODE Hs is about 0.2 m lower than the legacy WW3 series (2008–2014) and about 0.1 m lower than
  the buoy, so the threshold count is approximate.

## 3. What Agent C can use now

All files are in `data/processed/`. Times are UTC and tz-naive.

| File | Rows | Columns | Notes |
|---|---|---|---|
| `trucvert_castelle2020_surveys.parquet` | 325 | survey_id, date, campaign, n_points, xl_raw_min, xl_raw_max, yl_raw_min, yl_raw_max, yl_dem_min, yl_dem_max, have_core300, have_w740, have_w1500 | survey inventory |
| `trucvert_castelle2020_profiles.parquet` | 59,403 | survey_id, date, campaign, window, xl, x_legacy, z, frac_cells | long format; z in m above MSL (= IGN69 − 0.40); xl increases seaward, 2 m step; `x_legacy = xl − 40` aligns with `TrucVert_OCA.mat` x |
| `trucvert_castelle2020_volumes.parquet` | 701 | survey_id, date, campaign, window, v_total, v_upper, v_lower, vol_valid, xl_min_valid, xl_max_valid, z_at_xl70, z_at_xl170 | m³/m over fixed xl ∈ [70, 170]; v_upper = above +1.75 m MSL (HAT); v_total = v_upper + v_lower; use `vol_valid` |
| `waves_resourcecode_node94337.parquet` | 273,912 | time, hs, tp, fp, dp, dir, spr, t02, t0m1, wlv, uwnd, vwnd, ucur, vcur, source, licence | hourly 1994-01 → 2025-03; **directional**; vs CANDHIS 2014: Hs r = 0.965, bias −0.11 m; dp RMSE 6° |
| `waves_castelle2020.parquet` | 175,320 | time, hs, tp, dm, source, licence | hourly 2000–2019, buoy-corrected hindcast; Dm nautical "from" |
| `tide_trucvert_castelle2020.parquet` | 175,321 | time, tide_msl, tide_ign69 | astronomical tide at Truc Vert, hourly 2000–2020 |
| `tide_shom_gauges.parquet` | 498,851 | station, name, time, eta_zh, eta_ign69, eta_tide_ign69, residual, source, licence | hourly observed + UTide tide + non-tidal residual; Arcachon = 190 |
| `trucvert_castelle2020_volumes_hat.parquet` | 701 | survey_id, date, campaign, window, vol_valid, v_total, v_upper_175, v_lower_175, v_upper_214, v_lower_214, v_upper_245, v_lower_245 | same fixed window; upper/lower split at HAT = 1.75 / 2.14 / 2.45 m MSL (see Vertical datums) |
| `climate_indices.parquet` | 921 | date, year, month, nao, winter, nao_djfm | NAO monthly + DJFM winter mean (winter label = January's year) |

Recommendations:
- For a homogeneous 2003–2019 series, use `window == "core300"`. For comparability with the thesis, use `w740`
  (2009–2012) and `w1500` (2013+).
- Never difference volumes computed from different windows.
- Still-water level at Truc Vert: `tide_msl` + the Arcachon `residual` (hourly). This is an approximation, documented in
  data/README.md §3c.
- Independent confirmation: the legacy `Data_frame.csv` water level matches the Castelle tide at r = 0.995 only after a
  **1 h time shift**, which agrees with Agent A's clock-offset fix.

## 3b. Vertical datums (answer to the HAT/PHMA question)

**Source**: SHOM *Références Altimétriques Maritimes* (RAM), Licence Ouverte v2.0.
- Read from the public INSPIRE WFS `https://services.data.shom.fr/INSPIRE/wfs` (typeName
  `RAM_BDD_WLD_WGS84G_WFS:ram_3857`) by `scripts/download_shom_ram.py` → `data/raw/shom_ram/ram_wfs.json`.
- Dataset page: https://www.data.gouv.fr/datasets/references-altimetriques-maritimes (last update 2024-06-06).
- Levels are in m above chart datum (ZH). Level_IGN69 = level_ZH + zh_ref.

| RAM site | ZH in IGN69 (zh_ref) | PHMA (HAT) ZH | PMVE (MHWS) ZH | NM (mean level) ZH | PHMA IGN69 | NM IGN69 | **PHMA − NM** |
|---|---|---|---|---|---|---|---|
| **Cap Ferret** (44.629N, −1.242E) | −1.98 | 4.51 | 4.20 | 2.37 | **+2.53** | **+0.39** | **2.14** |
| Arcachon (Eyrac gauge) | −1.98 | 4.91 | 4.35 | 2.48 | +2.93 | +0.50 | 2.43 |
| Le Grand Piquey | −1.981 | 4.65 | 4.20 | 2.37 | +2.67 | +0.39 | 2.28 |
| Pilat Plage | −2.005 | 4.54 | 4.05 | 2.33 | +2.54 | +0.33 | 2.21 |
| Lacanau (no IGN link) | n/a | 5.30 | 4.65 | 2.69 | n/a | n/a | 2.61 |
| Biscarrosse (no IGN link) | n/a | 4.91 | 4.35 | 2.49 | n/a | n/a | 2.42 |
| Boucau-Bayonne | −2.143 | 4.84 | 4.25 | 2.53 | +2.70 | +0.39 | 2.31 |

**Finding**: the thesis value "PHMA = +2.14 m IGN69" is **exactly Cap Ferret PHMA − NM = 4.51 − 2.37 = 2.14 m**.
- That number is HAT measured **above mean sea level**, not above IGN69.
- Cap Ferret NM = +0.39 m IGN69, the same 0.39 m the thesis uses for MSL.
- So Cap Ferret HAT = **+2.53 m IGN69 = +2.14 m MSL**.
- The 2017 code/handoff conversion "2.14 m IGN69 − 0.39 = +1.75 m MSL" subtracts the MSL offset a second time.
  The HAT threshold should have been **+2.14 m MSL** in the MSL-referenced profiles [verify against the thesis text/table
  that defines PHMA; this is an inference from the exact numerical match].

**Exceedance check** (hourly, percent of time above each threshold in m MSL):

| Threshold (m MSL) | Castelle astronomical tide at Truc Vert, 2000–2019 | Legacy MARS2D level, 2008–2014 |
|---|---|---|
| 1.75 | 3.71% | 3.71% |
| 2.14 | 0.42% | 0.41% |
| 2.45 | 0% | 0% |

- The 3.7% at 1.75 m matches Agent A's figure.
- At 2.14 m MSL, still water alone exceeds HAT only about 0.4% of the time, which fits "rarely exceeded".
- The maximum astronomical tide at Truc Vert itself (open coast, 7 m depth) over 2000–2019 is **+2.45 m MSL**. That is
  an empirical local HAT, between Cap Ferret (2.14) and Lacanau (2.61). Cap Ferret's RAM point is at the lagoon
  inlet, so a Truc Vert-specific HAT of about 2.45 m MSL is defensible [verify].
- `trucvert_castelle2020_volumes_hat.parquet` gives the upper/lower split for all three thresholds (1.75 / 2.14 / 2.45),
  so Agents A and C can test the sensitivity.

**Datum of each processed file**

| File / column | Vertical datum |
|---|---|
| `trucvert_castelle2020_profiles.z`, `*_volumes*` | m above **MSL, defined as NGF-IGN69 − 0.40 m** (Castelle et al. 2020 file attribute `mean_water_level` = 0.4). The legacy `TrucVert_OCA.mat` uses IGN69 − 0.39 m (= Cap Ferret NM); the 1 cm difference is not corrected. `v_upper` in `trucvert_castelle2020_volumes.parquet` uses 1.75 m MSL (thesis-code value, kept for comparability). |
| `tide_trucvert_castelle2020.tide_msl` / `.tide_ign69` | m above MSL (IGN69 − 0.40) / m IGN69 (= tide_msl + 0.40). Astronomical only. |
| `tide_shom_gauges.eta_zh` | m above the station's chart datum (ZH) |
| `tide_shom_gauges.eta_ign69`, `.eta_tide_ign69` | m IGN69 (= ZH value + zh_ref: Arcachon −1.98, Boucau −2.143, Socoa −2.173) |
| `tide_shom_gauges.residual` | m, observed − harmonic tide (both IGN69). The harmonic fit includes the record mean, so the residual has about zero mean. |
| `waves_resourcecode_node94337.wlv` | m relative to the model mean level (mean about 0); tide-like [verify] |

## 4. Unfinished / open items
- CANDHIS raw buoy data (API key needed), CMEMS IBI and ERA5 (credentials needed), WEPA (manual browser download),
  OCA LiDAR, Pléiades DEMs, CoastSat/SDS satellite shorelines and Biscarrosse: not downloaded (reasons above).
- [verify] which of the 295 Monitoring surveys stated in the paper is missing from OSF (294 files).
- [verify] RESOURCECODE `wlv` is tide-only, and the dp/dir conventions.
- [verify] Whether the Arcachon residual is an adequate open-coast surge proxy; compare with Boucau and the legacy MARS2D for 2008–2014.
- No post-2019 Truc Vert topography is openly available as far as this session found.
- Housekeeping: Agent A's commits 3a72c36 and dc4a518 swept several of my processed files into their commits
  (`git add` of `data/processed/`). The content is the same; later B commits update them.

## Reproduce

From the repo root, with the venv active (`source .venv/bin/activate`):

```bash
python -I scripts/download_castelle2020.py          # ~196 MB -> data/raw/castelle2020_osf/
python -I scripts/download_resourcecode.py          # 12 JSON -> data/raw/resourcecode/
python -I scripts/download_shom_tidegauges.py       # monthly requests 2003-now -> data/raw/shom_refmar/
python -I scripts/download_shom_ram.py              # SHOM RAM tidal levels (prints Cap Ferret etc.)
python -I scripts/download_climate_indices.py       # NAO (WEPA: manual, see data/README.md §4b)
python -I scripts/process_castelle2020.py
python -I scripts/process_waves.py
python -I scripts/process_tide.py                   # needs utide (requirements.txt)
python -I scripts/process_climate_indices.py
```
