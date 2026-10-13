# A — Reproduction and audit of the 2017/2020 EVI pipeline

Agent A, 2026-10-13. Code: `src/evi/` (clean package), tests: `tests/` (24 passing), data products:
`data/processed/{events,intervals}_trucvert.{parquet,csv}` + `events_trucvert_schema.md`,
`data/processed/reproduction_A.json` (all numbers below). Every number in this report was computed by
the commands in **Reproduce**; numbers quoted from the thesis are marked "thesis:"; anything I could not
check is tagged [verify].

## 0. Summary
* **The notebook is reproduced exactly from the repo data** (`evi.legacy.run_notebook()`): PPT train
  RMSE 11.73 / R 0.83 and PPT test RMSE 8.08 / R 0.97 — the values printed in the notebook's figures/outputs.
  This is pinned by a regression test (`tests/test_reproduction.py`).
* **The notebook is not the thesis pipeline.** It integrates ΔV over the whole profile for every model
  (no "above HAT" volume), uses a threshold of +3 m instead of HAT (+1.75 m MSL), a different train/test
  split (85/15 of the Hs series → split at 2013-12-13 08:00 UTC; test = Dec 2013–Dec 2014 only), quantiles on
  2008–2014, and a non-standard "R" (n-weighted average of two per-group Pearson R). Thesis numbers therefore
  cannot be reproduced exactly from this code; the closest analogues are reported side by side.
* **The headline "R = 0.97 / R² = 0.85" is not robust.** In the notebook test set (n = 8 erosive events), the
  "fat beach" group has n = 2, whose Pearson R is ±1 by construction. Merely correcting the profile-crossing
  routine (items 3–4) flips that 2-point R from +1 to −1 and the reported test R from 0.97 to 0.47, while
  the pooled R stays 0.94 and RMSE moves from 8.08 to 8.12.
* With a clean event table and the thesis split (calibration 2009-02-09 → 2013-12-01, validation ≥ 2013-12-01),
  and **without filtering on ΔV**, the linear EVI explains R² = 0.23 of calibration variance (General, ΔV above
  HAT; thesis: 0.26). Validation R² is higher (0.52–0.78) but n = 11 events, 9 of them in the 2013–14 winter,
  and bootstrap 95% CIs are wide (e.g. General R² [−0.24, 0.76]).
* Energy "units" are a pure rescaling for a linear model: E_notebook, ΣHs²Δt and Σ(1/16)ρgHs²Δt give
  identical fits (R², RMSE); time-integrated energy flux (with Tp) is marginally different. Restricting energy
  to HAT-exceeding hours did **not** improve skill on this data (R²_cal 0.23 vs 0.31 using all storm hours for
  ΔV_total), partly because TWL ≥ HAT is reached in 37% of all 3-h steps of the clean pipeline (see item 2).

## 1. Reproduction table

Definitions. R = Pearson correlation of observed vs fitted ΔV; R² = 1 − SSE/SST (equals R² of the fit
in-sample, can be negative out of sample). "R_w" = the notebook's n-weighted mean of the per-group
(fat/eroded) R; "RMSE_w" = n-weighted mean of the per-group RMSEs (the notebook does not pool).
Units: ΔV in m³/m (positive = erosion); E in the notebook's unit (1e6 J·h·m⁻², labelled "MJ/m" / "MJ/m²").

| Model | thesis (2017) | notebook printed (2020) | my reproduction of the notebook (exact port) | corrected version (clean event table, no ΔV filter unless stated) | explanation of differences |
|---|---|---|---|---|---|
| General — fit | thesis: ΔV_upper = 10.2E − 3.2 | not printed (cell 18 is a scatter only) | ΔV_total = 11.87E + 1.05 (n = 35, whole profile, threshold +3 m) | ΔV_upper = 8.33E − 2.88 (n = 35) | notebook uses whole-profile ΔV and +3 m threshold; corrected uses ΔV above the HAT plane, HAT = +1.75 m, exact runup/crossings, calibration-only quantiles |
| General — calibration skill | thesis: R² = 0.26, RMSE 22.4 | not printed | R = 0.53 (R² = 0.28), RMSE 23.7 | R = 0.48, **R² = 0.23**, RMSE 14.0 | RMSE not comparable across ΔV definitions (upper-beach ΔV has lower variance) |
| General — validation | thesis abstract: "R² = 0.55" (body unclear) [verify which metric] | not printed | test (Dec 2013–Dec 2014): R = 0.86, RMSE 15.4 (n = 10) | val: R = 0.75, R² = 0.52 [CI −0.24, 0.76], RMSE 8.5 [5.3, 11.4] (n = 11) | different validation windows (thesis 2014–2015; repo forcing ends 2014-12-31) |
| TPTE — fit | thesis: ΔV = 18.7E + 2.1 | not printed (`r` computed, unused) | 10.72E + 9.64 (n = 28, erosive only) | erosive-only: 12.80E + 2.12 (n = 27); honest (all events): 12.62E − 4.99 (n = 35) | selection on ΔV changes intercept sign |
| TPTE — calibration skill | thesis: not given [verify] | not printed | R = 0.68, RMSE 15.5 | erosive-only: R = 0.73, R² = 0.53, RMSE 11.9; honest: R = 0.48, R² = 0.23, RMSE 21.6 | dropping accretion events inflates R (item 7) |
| TPTE — validation | thesis: "0.61" (body: "coefficient de corrélation", abstract implies R²), RMSE 11.9 | not printed | test: R = 0.88, RMSE 12.2 (n = 8) | erosive-only: R = 0.87, R² = 0.74, RMSE 10.0 [4.3, 14.1] (n = 8); honest: R = 0.88, R² = 0.76 [0.52, 0.87], RMSE 11.2 [6.6, 15.9] (n = 11) | |
| PPT — fit | thesis: fat 20.9E + 2.6; eroded 14.9E + 2.7 | figure only | fat 21.89E + 5.48 (n = 17); eroded 8.37E + 5.84 (n = 11) | erosive-only: fat 16.21E + 1.00, eroded 8.46E + 4.69 (n = 27); honest: fat 17.78E − 5.08, eroded 7.10E − 4.08 (n = 35) | label = pre-storm volume vs mean of calibration surveys only (notebook: mean of 2008–2014 incl. test) |
| PPT — calibration skill | thesis: not given [verify] | **R = 0.83, RMSE = 11.73** (figure, cell 20) | **R_w = 0.83, RMSE_w = 11.73** (pooled: R = 0.82, RMSE 12.18) | erosive-only: R = 0.78, R² = 0.61, RMSE 10.9; honest: R = 0.56, R² = 0.31, RMSE 20.4 | exact match |
| PPT — validation | thesis: "0.85" (abstract: R² = 0.85; body: correlation coefficient), RMSE 7.5 | **R = 0.97, RMSE = 8.08** (cell 23) | **R_w = 0.97, RMSE_w = 8.08** (n = 8; fat n = 2, eroded n = 6); pooled R = 0.94, RMSE 8.11 | erosive-only: R = 0.97, R² = 0.92 [0.76, 0.96], RMSE 5.6 [3.7, 7.6] (n = 8); honest: R = 0.91, R² = 0.78 [0.34, 0.89], RMSE 10.7 [7.5, 13.4] (n = 11) | exact match; the 0.97 is an artefact of a 2-point group (see item 9) |

Event counts: the clean table has 101 survey intervals between 2009-02-09 and 2014-01-02 (i.e. **102 profiles**,
thesis: 102), of which 38 contain ≥ 1 storm (thesis: 37 events), with 67 storm segments (a storm crossing a
survey date is counted in both intervals; thesis: 51 storms). Storm thresholds: Hs95 = 4.22 m, Hs75 = 2.37 m on
2009-01-01 → 2013-12-01 (thesis: 4.3 / 2.3 m; notebook, full 2008–2014 series: 4.41 / 2.49 m).

### 1.1 Ablation: effect of each fix on the notebook pipeline (cumulative)
Same code path as the notebook (85/15 split, whole-profile ΔV, notebook metrics), switching one issue at a time
(`evi.legacy.ablation()`).

| step | Hs95/Hs75 | General train R / RMSE (n) | General test R / RMSE (n) | TPTE train R / RMSE (n) | TPTE test R / RMSE (n) | PPT train R_w / RMSE_w (n) | PPT test R_w / R_pooled / RMSE_w (n; n_fat) |
|---|---|---|---|---|---|---|---|
| 0 notebook as-is | 4.41/2.49 | 0.53 / 23.7 (35) | 0.86 / 15.4 (10) | 0.68 / 15.5 (28) | 0.88 / 12.2 (8) | 0.83 / 11.73 (28) | 0.97 / 0.94 / 8.08 (8; 2) |
| 1 +exact datenum (item 5) | 4.41/2.49 | 0.53 / 23.7 (35) | 0.86 / 15.4 (10) | 0.68 / 15.5 (28) | 0.88 / 12.2 (8) | 0.83 / 11.73 (28) | 0.97 / 0.94 / 8.08 (8; 2) |
| 2 +landward crossing, NaN-safe (items 3-4) | 4.41/2.49 | 0.53 / 23.7 (35) | 0.86 / 15.3 (10) | 0.69 / 15.5 (28) | 0.88 / 12.2 (8) | 0.83 / 11.67 (28) | 0.47 / 0.94 / 8.12 (8; 2) |
| 3 +HAT=1.75 m MSL threshold (item 2) | 4.41/2.49 | 0.55 / 23.0 (36) | 0.86 / 14.9 (10) | 0.70 / 15.1 (29) | 0.86 / 12.1 (8) | 0.87 / 10.51 (29) | 0.47 / 0.92 / 8.27 (8; 2) |
| 4 +exact de-shoaling, g=9.81 | 4.41/2.49 | 0.55 / 23.1 (36) | 0.86 / 14.9 (10) | 0.70 / 15.2 (29) | 0.86 / 12.2 (8) | 0.87 / 10.51 (29) | 0.47 / 0.92 / 8.27 (8; 2) |
| 5 +storm quantiles on calibration only (item 8) | 4.22/2.37 | 0.54 / 22.6 (39) | 0.87 / 15.0 (10) | 0.68 / 15.4 (30) | 0.87 / 12.5 (8) | 0.85 / 11.01 (30) | 0.48 / 0.92 / 8.30 (8; 2) |
| 6 +mean profile from train only (item 8) | 4.22/2.37 | 0.54 / 22.6 (39) | 0.87 / 15.0 (10) | 0.68 / 15.4 (30) | 0.87 / 12.5 (8) | 0.82 / 11.73 (30) | 0.48 / 0.92 / 7.64 (8; 2) |
| 7 +no erosive-only filter (item 7) | 4.22/2.37 | 0.54 / 22.6 (39) | 0.87 / 15.0 (10) | 0.54 / 22.6 (39) | 0.87 / 15.0 (10) | 0.68 / 19.32 (39) | 0.53 / 0.90 / 10.91 (10; 2) |

### 1.2 Energy variants (clean table, thesis split, y = aE + b, all events, no ΔV filter)
`stormHAT` = sum over storm samples with TWL ≥ HAT; `storm` = all storm samples in the interval.

| E | scope | y | n_cal | R2_cal | n_val | R_val | R2_val | RMSE_val |
|---|---|---|---|---|---|---|---|---|
| E_notebook | stormHAT | dV_upper | 35 | 0.23 | 11 | 0.75 | 0.52 | 8.53 |
| E_notebook | stormHAT | dV_total_fixed | 35 | 0.23 | 11 | 0.88 | 0.76 | 11.25 |
| E_notebook | storm | dV_upper | 36 | 0.29 | 11 | 0.78 | 0.60 | 7.85 |
| E_notebook | storm | dV_total_fixed | 36 | 0.31 | 11 | 0.91 | 0.80 | 10.37 |
| E_Hs2dt | stormHAT | dV_upper | 35 | 0.23 | 11 | 0.75 | 0.52 | 8.53 |
| E_Hs2dt | stormHAT | dV_total_fixed | 35 | 0.23 | 11 | 0.88 | 0.76 | 11.25 |
| E_Hs2dt | storm | dV_upper | 36 | 0.29 | 11 | 0.78 | 0.60 | 7.85 |
| E_Hs2dt | storm | dV_total_fixed | 36 | 0.31 | 11 | 0.91 | 0.80 | 10.37 |
| E_dens | stormHAT | dV_upper | 35 | 0.23 | 11 | 0.75 | 0.52 | 8.53 |
| E_dens | stormHAT | dV_total_fixed | 35 | 0.23 | 11 | 0.88 | 0.76 | 11.25 |
| E_dens | storm | dV_upper | 36 | 0.29 | 11 | 0.78 | 0.60 | 7.85 |
| E_dens | storm | dV_total_fixed | 36 | 0.31 | 11 | 0.91 | 0.80 | 10.37 |
| E_Pflux | stormHAT | dV_upper | 35 | 0.22 | 11 | 0.75 | 0.52 | 8.58 |
| E_Pflux | stormHAT | dV_total_fixed | 35 | 0.22 | 11 | 0.89 | 0.77 | 10.98 |
| E_Pflux | storm | dV_upper | 36 | 0.28 | 11 | 0.79 | 0.60 | 7.84 |
| E_Pflux | storm | dV_total_fixed | 36 | 0.31 | 11 | 0.92 | 0.82 | 9.81 |

## 2. Audit of HANDOFF §2.1 (11 items)

| # | issue | confirmed? (evidence) | fix applied (where) | effect on metrics |
|---|---|---|---|---|
| 1 | Energy units | **Yes.** Notebook: `En=(1/16*densi*g*Hs**2)*3`, then `/1e6`, Δt = 3 in hours → unit is 1e6 J·h·m⁻², labelled "MJ/m" (notebook) and "MJ/m²" (thesis). Thesis Eq. (p. 10) defines flux P = ρg²Hs²TpΔt/(64π) with Δt "en heures", and §II defines E as the time integral of energy density in J/m². Neither label is dimensionally right. | Four explicitly-unitised variants in `evi.energy` and in the event table: `E_notebook_*_MJh_m2` (reproduction only), `E_Hs2dt_*_m2h`, `E_dens_*_MJs_m2`, `E_Pflux_*_GJ_m` (ρ=1025, g=9.81). Tested in `tests/test_energy.py`. | None on linear-fit skill: the first three are exact multiples of each other (test `test_energy_variants_are_rescalings`), identical R²/RMSE (§1.2); only the slope's numeric value changes (×3600×9.81/9.8 from notebook unit to MJ·s·m⁻²). Energy flux (Tp-weighted) is marginally different (val R² 0.82 vs 0.80 on ΔV_total, all storm hours, n = 11 — within noise). |
| 2 | Threshold: β = 3 vs HAT = +1.75 m MSL | **Yes.** Notebook cell 10: `beta = 3`. HAT/PHMA = +2.14 m IGN69 (thesis p. 20, Fig. list) = +1.75 m in the MSL-referenced profiles. The thesis figures were produced with PHMA by the author's description; the 2020 notebook (a later Python port) used +3 m, so the notebook cannot have produced the thesis figures [verify against original 2017 code, not in repo]. | `HAT_MSL = 1.75` in `evi.constants`; clean pipeline compares TWL to HAT vertically. Ablation step 3. | Notebook pipeline: PPT train R_w 0.83 → 0.87, RMSE_w 11.67 → 10.51; General/TPTE ±0.02 in R. **Side finding [verify]:** with HAT = +1.75 m, the MARS2D still water level alone exceeds HAT in 3.7% of samples and TWL ≥ HAT in 37% of samples; this is inconsistent with HAT being "rarely exceeded" (thesis p. 20). The source variable in `datasets/Level/2010/*.nc` (`XE`, MARS2D AQUI250, point 44.641 N, −1.290 E) has CF standard name `sea_surface_height_above_sea_level` (model mean level) and the CSV `setup` column equals it exactly (after the 1 h clock fix), so the water level is nominally MSL-referenced; the mismatch then points to the HAT value/datum or to a model-vs-site MSL offset [verify with SHOM PHMA and a tide gauge — Agent B]. |
| 3 | Index misalignment (`ELE[~isnull]` vs unfiltered `DIST=x`) | **Latent only.** All 168 profiles have NaNs only as a trailing block (0 profiles with leading/interior NaN; checked in code), so `ELE` indices still align with `x`. Valid points per profile: 1400–2980. | `evi.profiles` never strips NaNs; it uses `valid_extent` and the original grid. | None on this dataset (ablation step 2 combines items 3–4). |
| 4 | `find_nearest` on non-monotonic profiles | **Yes, but rare.** Only 1/168 profiles crosses +3 m or +1.75 m more than once. The nearest-value search also picks the nearest *sample* rather than an interpolated crossing. Exceedance sign disagreements between nearest and landward-most crossing: 13 of 18,057 defined steps (β=3), 31 (HAT). | `evi.profiles.landward_crossing` (first down-crossing from the dune, linear interpolation); test with a barred profile. | Tiny on fits (General RMSE 15.4 → 15.3; PPT train RMSE_w 11.73 → 11.67) but it **flips the reported PPT test R from 0.97 to 0.47** because one 2-event group's R goes from +1 to −1 (see item 9). |
| 5 | Datenum fudge | **Yes.** `X*86400+epoch−365.242*86400−155491` is 3599.8 s (≈1 h) earlier than the exact conversion (`tests/test_io.py`). Surveys are all at 12:00 UTC (datenum fraction 0.5); the notebook places them at 11:00 UTC. | `evi.io.datenum_to_datetime` / `datenum_to_unix` (exact; `datetime.fromordinal(int(d)) + timedelta(days=d%1) − timedelta(days=366)`). | **None** on the notebook (ablation step 1 identical to step 0). Reason found (§2.2): the CSV clock is itself 1 h early (CET), so the fudge (surveys at 11:00:00.2 UTC-label) is consistent with the CSV; with either conversion the 11:00-labelled sample falls before the survey. The clean pipeline uses the exact datenum **and** shifts the CSV clock by +3600 s. |
| 6 | Volume integration window | **Partly.** The notebook window `end` = first NaN of the mean profile over all 2008–2014 surveys − 1 → x ≤ 139.8 m, which every profile covers (the mean is NaN as soon as one profile is). So there is **no aliasing of survey extent** into ΔV; the cost is discarding everything seaward of 139.8 m (surveys reach up to 297.9 m). | Event table gives both `dV_*` over the pairwise common window (both surveys cover it; `x_window_pair`) and `dV_*_fixed` over the global common window (139.9 m). Upper/lower split by the HAT plane, so `dV_upper` is window-independent. | Notebook metrics unchanged. In the clean table, ΔV_total over the pairwise window has a larger spread (−102 to +141 m³/m) than over the fixed window (−76 to +76); models use the fixed window for comparability. |
| 7 | Selection on the target | **Yes.** Cells 20/23 drop events with `V_err < 0` before fitting and testing. Thesis §III-1-2 does the same for TPTE/PPT. | Clean pipeline never filters on ΔV; erosive-only fits are kept only as labelled "SECONDARY" rows. | Ablation step 7: TPTE train R 0.68 → 0.54, RMSE 15.4 → 22.6; PPT train R_w 0.82 → 0.68, RMSE_w 11.7 → 19.3; PPT test RMSE_w 7.6 → 10.9. Clean table: TPTE calibration R² 0.53 (erosive-only) vs 0.23 (all). |
| 8 | Leakage (mean profile; storm indices) | **Yes, both.** Mean profile = mean of all surveys between first and last forcing sample (2008–2014, includes test). Quantiles Hs95/Hs75 computed on the full 2008–2014 series (4.41/2.49 m). Storm start/stop found on the full series (a train storm can be delimited using test data — minor). Also the per-timestep slope uses the last survey before t (no look-ahead — fine). | Quantiles on 2009-01-01 → 2013-12-01 (4.22/2.37 m, `storm_thresholds`); fat/eroded reference = mean pre-storm volume of calibration surveys only (472.4 m³/m over 0–139.9 m). | Ablation steps 5–6: train RMSE_w 10.5 → 11.0 → 11.7; test RMSE_w 8.3 → 8.3 → 7.6; test n unchanged (8). Small, but it must be fixed for a paper. Agent C note: the thresholds in the event table are fitted on 2009–2013, so events in that window are in-sample for the thresholds. |
| 9 | Tiny test set; R vs R² | **Yes.** Notebook test: 10 events with non-zero filtered energy, 8 after the erosive filter, split 2 fat / 6 eroded. Pearson R of a 2-point group is ±1 by definition; the notebook's reported R = (2·R_fat + 6·R_eroded)/8 = (2·1 + 6·0.964)/8 = 0.97. The printed number is an R (correlation), not R², and is not a standard pooled statistic (pooled R = 0.94). Thesis: abstract says "R² = 0.85" (also 0.55), body says "coefficient de corrélation de respectivement 0.61 et 0.85" — the thesis itself is inconsistent about R vs R² [verify against thesis figures 26–28]. | `evi.metrics`: R, R² (1−SSE/SST), RMSE, bias, n, with seeded percentile bootstrap CIs (2000 resamples, seed 42). | With n = 8–11, bootstrap 95% CIs on validation R² have widths of 0.2–1.0 (§1). The headline should be pooled R² with CI and n, never the weighted per-group R. |
| 10 | Runup typo in thesis | **Yes.** Thesis p. 24: "Si є < 0.3 … Runup = 0.016√(HsL0)"; Stockdon et al. (2006) dissipative R2% is 0.043√(H0L0) (0.016 is their dissipative *setup*). The thesis also writes Hs where deep-water H0 is meant. The notebook code uses 0.043 and de-shoaled H0 (correct). | `evi.runup.stockdon_r2` (0.043 branch), tested. | None on the notebook (already correct); the thesis text should be corrected in the paper. |
| 11 | README image paths | **Yes.** `README.md` line 10 links `https://raw.githubusercontent.com/Raph9989/Beach_erosion/master/images/Schema_english.jpg` (other account). | Not edited (README is outside Agent A's paths). Suggested fix: relative path `images/Schema_english.jpg`. | n/a |

### 2.2 Additional findings (not in §2.1)
* **CSV clock is 1 h early (new, confirmed).** `Data_frame.csv` `# time` starts at 1199142000 =
  2007-12-31T23:00Z, i.e. the stamps were made from CET local time. Against the raw repo files: Hs and
  1/fp equal the WW3 2010 fields at the nearest grid node (44.667 N, −1.500 E; 0.25° grid) with max
  difference 0.000 only after adding +1 h (no overlap at 0 h, corr 0.97 / 0.82 at +4 h), and `setup` equals
  MARS2D `XE` from `datasets/Level/2010/Niveaux_mars_2010_1.nc` (corr 1.000, std diff 0.000) only at +60 min
  (corr 0.876 at 0 min). Fixed in `evi.io.load_hydro` (`CSV_TIME_OFFSET_S = 3600`); the notebook port keeps the
  raw clock. Effect on the clean energy-variant table: ≤ 0.01 in R², ≤ 0.12 m³/m in RMSE.
* **Forcing location.** Hs/Tp come from the nearest node of a 0.25° WW3 grid (44.667 N, −1.5 E), not an
  interpolation to the stated buoy point (44.6525 N, −1.45 E); the water level is from a different, MARS2D
  AQUI250 point (44.641 N, −1.290 E). Documented here; not changed.
* **Hidden state / stale outputs.** Cell 23's saved output is `Text(0.1, 47, 'R =0.97')`, but the cell source
  draws `RMSE` at y = 50 and no `R` label at all; the saved figure shows both labels. The outputs therefore come
  from a different version of the cell than the one saved. The numbers are still reproduced exactly by the
  saved logic (`tests/test_reproduction.py`).
* **Off-by-one in cell 23.** Energies loop over `range(ini, fin)` but volumes produce one fewer ΔV, so
  `En_sum` is one element longer than `V_err`; the subsequent `np.delete` with an out-of-bounds index only
  worked because old NumPy ignored it with a DeprecationWarning (visible in the saved output). Modern NumPy
  raises `IndexError`. The port reproduces the old behaviour explicitly (`_safe_delete`).
* **De-shoaling approximation.** The notebook's shoaling coefficient uses the deep-water wavenumber
  k0 = 2π/L0 instead of solving the dispersion relation at 50 m. Corrected in `evi.runup.deshoal(exact=True)`;
  effect on metrics ≤ 0.1 m³/m in RMSE and ≤ 0.01 in R (ablation step 4).
* **Constants.** Notebook ρ = 1025, g = 9.8; thesis text ρ = 1030, g = 9.81. Package uses ρ = 1025, g = 9.81
  except in the notebook-unit column.
* **Storm boundary convention.** The notebook storm window `Hs[start:stop]` includes the last calm sample
  before the storm and excludes the first calm sample after it; the clean `detect_storms` uses exactly the
  samples above Hs75.
* **Water level below survey.** In the notebook, runup (hence the indicator) is undefined whenever the still
  water level is below the seaward end of the surveyed profile (2,399 of 20,456 steps). The clean pipeline
  uses the seaward survey end as the lower slope point in that case (flagged in the schema).
* **Survey gaps.** Interval 2008-04-08 → 2009-02-09 is 307 days long (11 storms) and is not usable as an event;
  `interval_days` is in the table so Agent C can exclude long gaps.

## 3. Interpretation for Agents C/F (no new numbers)
* The 2017 calibration-period finding is reproduced: storm energy alone explains about a quarter of
  storm-event ΔV variance at Truc Vert (thesis R² 0.26; here 0.23 for ΔV above HAT with HAT-filtered energy).
* The validation numbers look better than calibration because the validation set is dominated by the
  extreme 2013–14 winter (large, mostly erosive events spanning a wide range), not because the model
  generalises; CIs are wide and n is ~10. Leave-one-winter-out (Agent C protocol) is required.
* The "PPT 0.85 / 0.97" headline rests on (i) dropping accretion events, (ii) a per-group weighted R and
  (iii) a 2-event subgroup. It should not be quoted as model skill in the paper.
* The HAT filter adds little; the datum of the MARS2D water level vs the profile datum must be verified
  before interpreting HAT-exceedance features [verify].

## 4. Unfinished / caveats
* Exact thesis numbers (10.2E − 3.2, 18.7E + 2.1, PPT coefficients, R²/RMSE) are not reproduced exactly: the
  original 2017 code (likely MATLAB [verify]) is not in the repo, and the 2020 notebook differs in method
  (§0). The closest analogues are reported.
* `berm_volume_pre` is a proxy (sand between +1.75 m and +4.0 m MSL seaward of the +4 m crossing); the
  +4 m dune-toe level and the −1.5/+1.5 m intertidal band are assumptions [verify].
* Wave direction is not in the repo data (`mean_dir` = NaN); Agent B's CANDHIS/hindcast data should fill it.
* Validation window here ends 2014-12-31 (repo forcing), whereas the thesis validated to mid-2015.
* `docs/thesis/thesis_key_sections_en.md` (optional translation): see that file if present.

## Reproduce
```bash
cd Beach_erosion
source .venv/bin/activate            # Python 3.12, package `evi` installed editable from src/
python -m evi.events                 # -> data/processed/{events,intervals}_trucvert.{parquet,csv}
python -m evi.reproduce              # -> prints §1 tables (notebook ablation, corrected models, energy variants)
                                     #    and writes data/processed/reproduction_A.json (bootstrap seed 42)
pytest -q                            # 24 tests: runup, energy units, storms, volumes, datenum, events, notebook regression
python -c "from evi.legacy import run_notebook; r=run_notebook(); print(r['ppt_train'], r['ppt_test'])"  # notebook as-is
```
