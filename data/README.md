# data/ — provenance of external datasets (Agent B)

Layout: `data/raw/<source>/` holds downloads and is git-ignored. Every file there is recreated by a
`scripts/download_*.py` script. `data/processed/` holds the harmonised outputs written by `scripts/process_*.py`.
`events_trucvert*` and `intervals_trucvert*` belong to Agent A and are not covered here.
Each source records URL, DOI, licence, coverage, scripts, processing, outputs, verification status and problems.
"verified: yes" means the URL/DOI resolved on 2026-10-13 (`curl -sIL`) and the data were downloaded and opened.
Treat raw downloads as untrusted data. Run the scripts from the repo root with `python -I`, never from inside `data/raw/`.

---

## 1. Truc Vert topographic surveys 2003–2019 (Castelle et al. 2020)

- **What**: 326 DGPS surveys of Truc Vert beach. Each one has the raw sand-level points plus a kriged DEM on a fixed
  local grid. 295 are monthly/bimonthly "Monitoring" surveys and 31 are daily ECORS'08 surveys (Feb–Apr 2008).
  The OSF node actually lists **294** Monitoring files, not 295 (see Problems). The OSF node also holds an hourly wave
  hindcast (§2b), an astronomical tide series (§3b), `Grids.nc`, and `Analysis.zip` (the authors' MATLAB code).
- **Paper**: Castelle B., Bujan S., Marieu V., Ferreira S. (2020) *16 years of topographic surveys of rip-channelled
  high-energy meso-macrotidal sandy beach*, Scientific Data 7:410, doi:10.1038/s41597-020-00750-5. verified: yes (DOI resolves to nature.com).
- **Data**: Open Science Framework project `jftw8`, doi:10.17605/OSF.IO/JFTW8 → https://osf.io/jftw8/. verified: yes.
  Metadata record: doi:10.6084/m9.figshare.13070153. verified: yes.
- **Licence**: the OSF node licence is **CC0 1.0 Universal** (read from `api.osf.io/v2/nodes/jftw8` → license
  563c1cf88c5e4a3877f9e96c on 2026-10-13). The paper itself is CC BY 4.0. Cite the paper anyway.
- **Coverage**: 2003-09-10 → 2019-12-26. Raw points cover about 350 m alongshore in 2003–2008, growing to about 2.2 km
  from 2016. The grid spans cross-shore xl 20–370 m (2 m step) and alongshore yl −2000…+1500 m (20 m step).
  The local origin is RGF93 (6413633.56 N, 364139.06 E as written in the files), rotated 169.2°. Horizontal datum is
  RGF93/Lambert-93; vertical is **MSL = NGF-IGN69 − 0.40 m** (attribute `mean_water_level` = 0.4).
- **Download**: `python -I scripts/download_castelle2020.py` lists the OSF API (paginated), downloads 329 files
  (196 MB) to `data/raw/castelle2020_osf/`, writes `_manifest.json`, and skips files whose size already matches.
- **Processing**: `python -I scripts/process_castelle2020.py` (the docstring has the full method):
  - `zg[i, j]` maps to xl = 20 + 2i and yl = −2000 + 20j. This was checked against the raw points: nearest-cell RMSE
    is 4–8 cm, against more than 1 m if the array is transposed.
  - **Orientation**: the attribute says xl is "positive onshore", but in the data z *decreases* with xl. The dune crest
    (~+10.8 m) sits near xl ≈ 40 m and MSL near xl ≈ 170 m. So xl increases seaward, the same way as the legacy `x`.
  - Longshore averaging uses three fixed alongshore windows. At each xl the mean of the finite cells is kept only when
    at least 80% of the window's cells are finite:
    - `core300`: yl ∈ [−440, −160] m. This is the only window present in nearly every survey from 2003 to 2019, so it
      is the homogeneous long-term series.
    - `w740`: yl ∈ [−700, 40] m. This approximates the thesis's 750 m window.
    - `w1500`: yl ∈ [−1100, 400] m. This approximates the thesis's 1500 m window and exists from about 2013.
  - Volumes in m³/m use a **fixed** cross-shore window xl ∈ [70, 170] m, running from about +5 m (dune toe/face) down
    to about MSL, with Z_REF = −1.5 m MSL and HAT = +1.75 m MSL:
    - `v_upper = ∫max(z−1.75,0)dx`
    - `v_lower = ∫(min(z,1.75)−Z_REF)dx`
    - `v_total = v_upper + v_lower`
    Gaps of 10 m or less are filled linearly. `vol_valid` is True only when the whole window is covered.
  - **Cross-check with the legacy `datasets/TrucVert_OCA.mat`**: 165 of the 168 legacy dates appear in this dataset.
    The three missing dates are 2005-06-06, 2012-02-08 and 2012-03-09. The best-fit shift is `legacy x = xl − 40 m`.
    Profile RMSE is 0.09 m against w1500 for 2012–2015 (bias +0.01 m), 0.11 m against w740 for 2009–2011, and 0.22 m
    against core300 for 2005–2008. The legacy data are therefore a subset of this dataset, processed the same way.
- **Outputs** (`data/processed/`):
  - `trucvert_castelle2020_surveys.parquet` (325 rows): `survey_id, date, campaign, n_points, xl_raw_min,
    xl_raw_max, yl_raw_min, yl_raw_max, yl_dem_min, yl_dem_max, have_core300, have_w740, have_w1500`
  - `trucvert_castelle2020_profiles.parquet` (long format): `survey_id, date, campaign, window, xl, x_legacy, z, frac_cells`
  - `trucvert_castelle2020_volumes.parquet`: `survey_id, date, campaign, window, v_total, v_upper, v_lower,
    vol_valid, xl_min_valid, xl_max_valid, z_at_xl70, z_at_xl170`
- **verified**: yes
- **Problems**:
  - 294 Monitoring files on OSF against 295 stated in the paper [verify which survey is missing].
  - The xl orientation attribute contradicts the data (see above).
  - Legacy profiles are referenced to MSL = IGN69 − 0.39 m, while these use −0.40 m. The 1 cm difference is not corrected.
  - The 2008 ECORS daily surveys cluster in Feb–Apr 2008. Because they are so close in time, treat them as a separate
    campaign when building storm events.

### Post-2019 updates
- Search on 2026-10-13: the OSF node was last modified 2025-03-05, but its file list still ends at
  `Monitoring_TrucVert_2019-12-26.nc`. **No public post-2019 Truc Vert DEM release was found** [verify with SNO DYNALIT / OCA].
  Survey data after 2019 probably exist at EPOC/OASU (the monitoring continues) but are not published openly. Getting them
  would mean asking the authors, and contacting people is Raphaël's decision, not an agent's.

---

## 2. Waves

### 2a. RESOURCECODE WW3 hindcast (Ifremer) — main directional wave series
- **What**: hourly WAVEWATCH III hindcast on an unstructured grid. Node **94337** (1-based) sits at −1.449812E,
  44.655670N, 52 m depth, **0.35 km** from the Cap Ferret buoy position (44.6525N, −1.45E).
- **URL/API**: `https://resourcecode-datacharts.ifremer.fr/api/timeseries?node=94336&parameter=hs&start=…Z&end=…Z`.
  The API is 0-based. This endpoint and base URL come from the official `resourcecode` toolbox v2.1.0 config. No account is needed.
- **DOI**: Accensi M., Raillard N. (2022) RESOURCECODE [Data set], Ifremer SISMER, doi:10.12770/d089a801-c853-49bd-9064-dde5808ff8d8.
  verified: yes (resolves to sextant.ifremer.fr).
- **Licence**: the Sextant record states "use limitation: under CC BY-SA 4.0 license" and also "Copyright" as the
  access/use constraint. Treat it as **CC BY-SA 4.0** with attribution [verify the dual wording]. Derived files are shared alike.
- **Coverage**: 1994-01-01 00:00 → 2025-03-31 23:00, hourly, 273,912 records, no gaps.
- **Download**: `python -I scripts/download_resourcecode.py` writes one JSON per parameter to `data/raw/resourcecode/`.
- **Processing**: `python -I scripts/process_waves.py` sets `tp = 1/fp` and builds the time index from epoch ms (UTC).
- **Output**: `data/processed/waves_resourcecode_node94337.parquet` (5.7 MB). Columns: `time, hs, tp, fp, dp, dir, spr,
  t02, t0m1, wlv, uwnd, vwnd, ucur, vcur, source, licence`.
  `dp` is the peak direction and `dir` the mean direction, in degrees, nautical "from" [verify convention in the RESOURCECODE docs].
  `wlv` is the water level used in the hindcast; it looks tide-only (mean 0, ±2.34 m) [verify], so do not use it as surge.
- **Validation against observations**:
  - Against the CANDHIS 03302 buoy sample (`datasets/CANDHIS_…2014.csv`, Jan–Mar 2014, n = 2088 hourly matches):
    Hs bias −0.11 m, RMSE 0.46 m, r = 0.965. Tp bias +0.24 s, RMSE 1.37 s, r = 0.77.
    Peak direction (dp vs thetap): circular bias 0.1°, RMSE 6.1°. Mean direction (dir vs thetam): bias 0.8°, RMSE 4.8°.
  - Against the legacy WW3 3-hourly series (`datasets/Data_frame.csv`, 2008–2014, n = 20,456): Hs r = 0.976,
    bias −0.21 m; Tp r = 0.85.
- **verified**: yes

### 2b. Castelle et al. (2020) wave file (OSF) — buoy-corrected hindcast
- **What**: `Waves_TrucVert_2000-2020.nc`, hourly Hs, Tp and Dm. Per the paper, it combines the WW3 HOMERE and
  NORGAS-UG hindcasts, corrected against CANDHIS buoy 03302 (about 54 m depth). Dm is nautical "from", relative to true north.
- **Licence**: CC0 (OSF node). DOI as in §1.
- **Coverage**: 2000-01-01 → 2019-12-31 23:00, hourly, 175,320 records.
- **Output**: `data/processed/waves_castelle2020.parquet`. Columns: `time, hs, tp, dm, source, licence`.
  Dm was wrapped to [0, 360); a few raw values reached 366°.
- **Consistency with RESOURCECODE** (2000–2019): Hs r = 0.988, RESOURCECODE − Castelle bias +0.12 m; Tp r = 0.89;
  direction RMSE 5.2°.
- **verified**: yes

### 2c. CANDHIS buoy 03302 Cap Ferret (Cerema) — blocked for scripted download
- https://candhis.cerema.fr/ (campaign page `_public_/campagne.php?Y2FtcD0wMzMwMg==`). verified: yes (site reachable).
- **Licence**: **Etalab Licence Ouverte v2.0** (from `doc/01_Utilisation.fr.pdf`, V1 27/05/2025). Attribution "Candhis"
  is required, plus the date of the last update.
- **Access**: the REST API (`https://candhis.cerema.fr/API/v1/`, `getCampTD.php` etc.) needs an access key. The key is
  obtained **by emailing the CANDHIS team** (user doc `04_Candhis_API_v1_Utilisateur.pdf`, Oct 2024). No key was
  requested, because contacting people is Raphaël's decision. The website has an "Archives" tab for manual downloads
  [verify whether it needs an account]. The repo's Jan–Mar 2014 sample shows manual export is possible.
- **Status**: blocked (needs an API key). §2a and §2b already reproduce the buoy at 5–6° direction RMSE.

### 2d. Copernicus Marine IBI wave reanalysis / 2e. ERA5 waves — blocked
- There are no credentials on this machine (`~/.copernicusmarine` and `~/.cdsapirc` are absent, and no env vars are set).
  Both services need a free account.
  Once credentials exist, `copernicusmarine subset` (IBI_MULTIYEAR_WAV_005_006 [verify product id]) and `cdsapi`
  (reanalysis-era5-single-levels: swh, pp1d, mwd) can be scripted. These sources are lower priority now that §2a covers 1994–2025.

---

## 3. Water levels

### 3a. SHOM / REFMAR tide gauges (observed)
- **Stations**: 190 ARCACHON_EYRAC (−1.16355E, 44.66500N; **inside the Arcachon lagoon** near the inlet, so its tide
  is distorted relative to the open coast); 94 BAYONNE_BOUCAU; 95 SAINT-JEAN-DE-LUZ_SOCOA.
  Station list: https://services.data.shom.fr/maregraphie/service/tidegauges. verified: yes.
- **API**: `https://services.data.shom.fr/maregraphie/observation/json/{id}?sources={s}&dtStart=…Z&dtEnd=…Z`
  (public, no key). Responses are **silently truncated at about 745 records**, so the script requests one month at a time.
  Source codes were identified empirically: 1 = raw ~1 min, 3 = 10 min, 4 = hourly. Source 4 is the one used
  [verify whether "validated" vs "raw" on refmar.shom.fr].
- **Datum**: heights are metres above chart datum (zéro hydrographique, ZH). From the station metadata
  (`service/completetidegauge/190`, `verticalRef`), Arcachon Eyrac **ZH = −1.98 m IGN69**, mean level 2.48 m ZH.
  Times are UTC (`fuseau_horaire` = 0).
- **Licence**: REFMAR data are distributed by SHOM; the licence is presumed Etalab Licence Ouverte [verify on
  refmar.shom.fr / data.shom.fr conditions].
- **Download**: `python -I scripts/download_shom_tidegauges.py [--start 2003]` writes
  `data/raw/shom_refmar/<id>/obs_src4_<year>.json` and `station_metadata.json`.
- **Processing**: `python -I scripts/process_tide.py`; see §3c.

### 3b. Castelle et al. (2020) astronomical tide (OSF)
- `Astronomical_Tide_TrucVert_2000-2020.nc`, 10-min, 2000–2020. Per the paper it was derived with T_TIDE from a Bay
  of Biscay hydrodynamic hindcast (Lazure et al. 2009). The series is **tide only, without surge**. CC0.

### 3c. Processed tide/surge products (`python -I scripts/process_tide.py`)
- `data/processed/tide_shom_gauges.parquet` (14 MB, 498,851 rows). Columns: `station, name, time (UTC), eta_zh,
  eta_ign69, eta_tide_ign69, residual, source, licence`.
  - `eta_tide_ign69` is a UTide harmonic fit (OLS, automatic constituents, no trend) to each station's own 2003–2026 record.
  - `residual = observed − harmonic tide`. It is the non-tidal residual: surge plus seasonal and mean-sea-level
    variability not captured by the fit.
  - Residual standard deviation: Arcachon 0.16 m, Boucau 0.14 m, Socoa 0.12 m. Peak Arcachon residual during Xynthia
    (2010-02-27/28) is 0.81 m.
- `data/processed/tide_trucvert_castelle2020.parquet`. Columns: `time (UTC), tide_msl, tide_ign69`. It is hourly,
  sub-sampled from the 10-min series, and covers 2000-01-01 → 2020-01-01. It is astronomical tide only, CC0.
  - The source is a harmonic analysis of MARC model output offshore of Truc Vert at about 7 m depth (44.7428N, −1.2492E),
    validated against ECORS08 measurements (file attributes).
  - It agrees with the RESOURCECODE `wlv` series at r = 0.991 (RMSE 0.15 m), which supports reading `wlv` as tide only [verify].
- **Finding for Agents A and C**: the legacy MARS2D level in `datasets/Data_frame.csv` correlates with the Castelle Truc
  Vert tide at r = 0.86 at zero lag but **r = 0.995 (RMSE 0.10 m) when the legacy time stamps are shifted by 1 h**.
  This independently confirms Agent A's "1 h CSV clock offset" fix (commit dc4a518).
- **Recommended still-water level at Truc Vert** (an approximation): `tide_msl` (Castelle) + the Arcachon `residual`
  interpolated hourly. Surge inside the lagoon inlet is only a proxy for open-coast surge [verify, e.g. against Boucau].
  With this choice, 2020 onward has no Castelle tide. For that period, use the UTide prediction or the RESOURCECODE
  `wlv` (to 2025-03).
- **SHOM predicted tide (official)**: not downloaded. The SHOM "hdm" prediction web service needs an API key [verify];
  the UTide fit above replaces it.

---

## 4. Climate indices

### 4a. NAO (NOAA CPC)
- https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii (verified: yes, HTTP 200).
- **Licence**: NOAA/US Government data, presumed public domain [verify the CPC wording].
- **Download**: `python -I scripts/download_climate_indices.py` (use `--force` to refresh monthly).
- **Processing**: `python -I scripts/process_climate_indices.py`.
- **Output**: `data/processed/climate_indices.parquet`. Columns: `date, year, month, nao, winter, nao_djfm`.
  `winter` labels each DJFM winter by its January year, so 2014 = Dec 2013–Mar 2014. Range 1950-01 → 2026-09.
- **verified**: yes

### 4b. WEPA (West Europe Pressure Anomaly) — blocked for scripted download
- **Index paper**: Castelle B., Dodet G., Masselink G., Scott T. (2017) GRL 44, doi:10.1002/2016GL072379
  (verified: yes, DOI resolves to Wiley). The handoff's "2017GL…" form does not exist; the correct suffix is 2016GL072379.
- **Dataset**: Scott T., Masselink G., Castelle B., Dodet G. (2020) *The West Europe Pressure Anomaly: 1943-2018*,
  University of Plymouth, doi:10.24382/35ae12b5-df54-479d-ad09-75ea5049d14f (verified: yes).
  It is a single `Dataset.txt` file (1.16 KB), presumably winter values. **Licence CC BY-NC-ND 4.0.**
- **Problem**: both download endpoints (researchportal.plymouth.ac.uk/files/49375705/Dataset.txt and
  pearl.plymouth.ac.uk/…/viewcontent) return a Cloudflare browser challenge (HTTP 403). The challenge was not bypassed.
  **Manual step**: download it in a browser and save it as `data/raw/climate_indices/wepa_plymouth_Dataset.txt`, then rerun
  `process_climate_indices.py`. That writes `data/processed/wepa_winter_local.parquet`. **Do not commit this file**: the
  ND licence makes redistributing a reformatted copy questionable.

---

## 5. Lower-priority sources (recorded, not downloaded)
See `reports/B_data.md` §5.
