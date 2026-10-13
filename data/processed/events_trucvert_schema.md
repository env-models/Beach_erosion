# Truc Vert event / interval tables — schema (v1.1 / v2, data version 2026-10-13b: HAT = +2.14 m MSL)

v1.1 (2026-10-13): added `max_P_kWm_*` and `hours_P_gt100_*` / `hours_P_gt200_*` (OCA operational wave-power
thresholds, BRGM report RP-67418-FR (2019), thresholds relayed by the orchestrator [verify]). Density documented below.

Built by `python -m evi.events` (Agent A, `src/evi/events.py`) from the legacy, read-only
`datasets/Data_frame.csv` (WW3 Hs/Tp + MARS2D water level, 3-hourly, 2008-01-01 → 2014-12-31) and
`datasets/TrucVert_OCA.mat` (168 longshore-averaged profiles 2005-04-08 → 2015-06-18).

* `intervals_trucvert.parquet|csv`: one row per pair of **consecutive surveys** both inside the forcing
  record (128 rows, including storm-free intervals — useful for calm-weather recovery).
* `events_trucvert.parquet|csv`: the subset with `n_storms >= 1` (51 rows), plus `event_id`.

No row is filtered on ΔV. Nothing in a row uses information from after `survey_end`, **except** the
storm thresholds (computed on 2009-01-01 → 2013-12-01, see below) — Agent C must treat events inside that
window as "in-sample" for the thresholds.

## Conventions
* Times: naive UTC. The CSV clock is shifted by +3600 s (it is CET, 1 h early; see reports/A_audit.md §2.2). Survey datenums converted exactly (`datetime.fromordinal(int(d)) + frac - 366 d`); every survey is at 12:00.
* Elevations: m relative to the profile datum = MSL at Truc Vert (0 = +0.39 m IGN69).
* Constants: ρ = 1025 kg/m³ (notebook value; the thesis and the 2018 JCR paper use 1030, which rescales energies by +0.5 %), g = 9.81 m/s², except `E_notebook_*`, which keeps the notebook's ρ = 1025, g = 9.8.
* **HAT = +2.14 m MSL** (`evi.constants.HAT_MSL`, data version 2026-10-13b). Source: SHOM RAM Cap Ferret, PHMA = 4.51 m ZH = +2.53 m IGN69, NM = +0.39 m IGN69, so PHMA − NM = 2.14 m [verify against thesis p. 20]. The earlier tables used +1.75 m (double-subtracted MSL offset); they are kept for sensitivity analysis as `events_trucvert_hat175.*`, `intervals_trucvert_hat175.*`, `events_trucvert_v2_hat175.*` and `intervals_trucvert_v2_hat175.*`.
* Δt = 3 h per forcing sample; a sample at time t belongs to interval [survey_start, survey_end).
* **Sign: ΔV > 0 = erosion** (volume lost between `survey_start` and `survey_end`), ΔV < 0 = accretion.
* Storms (`evi.storms.detect_storms`): maximal runs with Hs > Hs75 that contain at least one Hs > Hs95.
  Hs95 = 4.224 m, Hs75 = 2.374 m (quantiles of Hs over 2009-01-01 → 2013-12-01; thesis: 4.3 / 2.3 m).
  No merging (`min_gap_h = 0`); 83 storms over 2008–2014. A storm crossing a survey date is split between
  the two intervals (flag `storm_straddles_survey`).
* TWL = MARS2D water level (`setup` column, tide + surge) + Stockdon (2006) R2%. R2% uses deep-water H0
  (linear de-shoaling of Hs from 50 m depth, exact dispersion relation), L0 = gTp²/2π, and β = mean slope
  between the still water level and +4 m on the **last survey before the timestep** (landward-most
  crossings; when the water level is below the surveyed profile, the survey's seaward end is used).

## Columns
| column | unit | definition |
|---|---|---|
| event_id | – | `TV` + survey_start date (events table only) |
| survey_start, survey_end | datetime | consecutive survey times |
| p_start, p_end | – | row index of the profiles in `TrucVert_OCA.mat` |
| interval_days | d | survey spacing |
| period | – | `calibration` if survey_end ≤ 2013-12-01, else `validation` (thesis split) |
| n_storms | – | storms with ≥1 sample inside the interval |
| n_clusters | – | storms grouped when separated by < 72 h of calm (choice, `CLUSTER_GAP_H`) [verify vs literature] |
| storm_hours_total | h | storm samples in interval × 3 h |
| storm_durations_h | h | `;`-separated hours of each storm inside the interval |
| storm_straddles_survey | bool | a storm starts before survey_start or ends after survey_end |
| E_notebook_storm_MJh_m2 / E_notebook_stormHAT_MJh_m2 | 1e6 J·h·m⁻² | Σ (1/16)ρgHs²·3 / 1e6 with ρ=1025, g=9.8 — the notebook's "MJ/m" quantity (reproduction only) |
| E_Hs2dt_storm_m2h / …stormHAT_m2h | m²·h | Σ Hs²Δt |
| E_dens_storm_MJs_m2 / …stormHAT_MJs_m2 | MJ·s·m⁻² | Σ (1/16)ρgHs²Δt, ρ=1025, g=9.81, Δt in s (time-integrated energy density) |
| E_Pflux_storm_GJ_m / …stormHAT_GJ_m | GJ/m | Σ ρg²Hs²Tp/(64π)·Δt (time-integrated deep-water energy flux, Tp used as period) |
| (suffix `_storm`) | | summed over all storm samples in the interval |
| (suffix `_stormHAT`) | | summed only over storm samples with TWL ≥ HAT |
| peak_hs | m | max Hs over storm samples in interval |
| mean_tp_storm | s | mean Tp over storm samples |
| mean_dir | ° | NaN — no direction in repo data (Agent B to add) |
| hat_exceed_hours_storm | h | storm samples with TWL ≥ HAT × 3 h |
| hat_exceed_hours_all | h | all samples with TWL ≥ HAT × 3 h |
| max_twl_all, max_twl_storm | m MSL | max TWL over all / storm samples |
| max_wl | m MSL | max MARS2D water level in interval |
| max_P_kWm_all, max_P_kWm_storm | kW/m | max deep-water wave power P = ρg²Hs²Tp/(64π) over all / storm samples in the interval (Hs at the WW3 node, Tp as period) — v1.1 |
| hours_P_gt100_all, hours_P_gt100_storm | h | samples with P > 100 kW/m × 3 h, all / storm samples (OCA threshold, RP-67418-FR) — v1.1 |
| hours_P_gt200_all, hours_P_gt200_storm | h | same with P > 200 kW/m — v1.1 |
| V_pre_total | m³/m | ∫ z dx over the fixed window x ∈ [0, 139.9 m] on the survey_start profile (relative to the MSL datum) |
| V_pre_upper | m³/m | ∫ max(z − HAT, 0) dx, same window (sand above the HAT plane) |
| V_pre_lower | m³/m | V_pre_total − V_pre_upper |
| berm_volume_pre | m³/m | **proxy**: sand between the planes z = HAT (+2.14) and z = +4.0 m MSL seaward of the dune-toe proxy (landward-most crossing of +4.0 m) — `evi.profiles.berm_volume`. Dune toe at +4 m is an assumption (thesis tested 4/5/6 m NGF) [verify]. It includes any upper-beach sand in that band, not only a morphologically identified berm. |
| intertidal_slope_pre | m/m | least-squares slope of z ∈ [−1.5, +1.5] m MSL (landward of the first −1.5 m crossing) [band verify vs tidal datums] |
| dV_total, dV_upper, dV_lower | m³/m | ΔV over the window covered by **both** profiles, x ∈ [0, x_window_pair]; upper = change of sand above HAT plane; lower = total − upper |
| x_window_pair | m | seaward limit of the pairwise common window |
| dV_total_fixed, dV_upper_fixed, dV_lower_fixed | m³/m | same over the fixed global window [0, x_window_fixed] (comparable across events) |
| x_window_fixed | m | 139.9 m = shortest survey extent among all surveys used |
| days_since_last_storm | d | (start of first storm in interval, or survey_start if none) − end of the previous storm |
| winter | – | storm year July–June of the interval midpoint, e.g. `2013-14` |
| season | – | DJF/MAM/JJA/SON of the interval midpoint |

---

# v2 — extended table from Agent B's data (2008–2019)

Files: `events_trucvert_v2.{parquet,csv}` (98 events) and `intervals_trucvert_v2.{parquet,csv}` (201 intervals,
including storm-free ones). Built by `python -m evi.events_v2` (`src/evi/events_v2.py`). It reuses
`evi.events.build_intervals` with `dt_h = 1`, so it has the **same columns as v1** plus `frac_storm_no_surge`, and
the same definitions unless stated below. Event range: survey 2008-02-11 → survey 2019-12-26.

**Profiles.** `trucvert_castelle2020_profiles.parquet`, window **`w740`** (yl ∈ [−700, 40] m). This is the window
closest to the legacy 750 m longshore averaging, and the only one that covers 2008–2019 continuously (`w1500`
exists only from about 2013). Mixing windows would alias the averaging change into ΔV.
- Cross-shore coordinate: `x_legacy = xl − 40 m`.
- Grid: x ∈ [30, 274] m, 2 m step.
- Gaps of 10 m or less are filled linearly. The profile is truncated at the first larger gap.
- Of 224 w740 surveys, **202 are used**. The other 22 have no data at x = 30 m, the landward origin. That origin is
  xl = 70 m, ≈ +5 m MSL, and is the start of B's volume window. The w740 80% coverage rule usually removes the
  dune crest, so the v1 origin x = 0 cannot be used.
- **Vertical datum.** B's z is already **MSL = IGN69 − 0.40 m** (data/README.md), so no conversion was applied.
  HAT = +2.14 m MSL is used as in v1. The legacy datum is IGN69 − 0.39 m; the 1 cm difference is ignored.
- **Fixed volume window**: x ∈ [30, 130] m (= B's xl 70–170 m). Therefore `V_pre_*`, `dV_*_fixed` and `x_window_fixed`
  are **not on the same window as v1** (which uses x ∈ [0, 139.9]). They are NaN when a survey does not reach x = 130
  m: 17 of 98 events (27 of 201 intervals) have NaN `dV_total_fixed`.
- `dV_*` without a suffix uses the pairwise common window, starting at x = 30.
- Cross-check: `dV_upper` equals the differences of B's `v_upper` (w740) over the 174 intervals where both exist
  (correlation 1.000, mean absolute difference < 0.001 m³/m). Over the 97 survey intervals shared with v1,
  corr(dV_upper v1, v2) = 0.941 and the mean difference is −0.4 m³/m. The windows and averaging differ.

**Waves.** `waves_castelle2020.parquet`: hourly Hs, Tp, Dm (WW3 HOMERE+NORGAS-UG corrected with CANDHIS 03302,
CC0; source string from B).
- **`mean_dir`** is the circular mean of Dm over the storm hours in the interval, in degrees, nautical
  coming-from convention [verify convention with B].
- 17 slightly negative hourly Hs values (min −0.05 m) are clipped to 0.
- De-shoaling from 50 m is kept as in v1. The depth of the Castelle wave point is not checked [verify].
- These waves are **lower than the legacy WW3 node**. Over the 2008–2014 overlap (20,456 shared timestamps), corr
  0.988, mean Hs 1.66 vs 2.01 m, q95 3.72 vs 4.41 m. Storm thresholds are therefore lower than in v1.

**Storm thresholds.** Same rule as v1. Quantiles of hourly Hs on 2009-01-01 → 2013-12-01: **Hs95 = 3.56 m, Hs75 =
2.04 m**. For information, the 2008-01-01 → 2019-12-31 quantiles would be Hs95 = 3.75 m and Hs75 = 2.16 m; they
are **not** used. This gives 152 storms in 2008–2019.

**Water level.** wl = `tide_msl` (Castelle predicted tide at Truc Vert) + **surge**. Surge is the Arcachon-Eyrac
(SHOM 190) non-tidal `residual` from `tide_shom_gauges.parquet`.
- Where the residual is missing (15.3% of hours), surge = 0. `frac_storm_no_surge` gives the share of storm hours
  in each event without surge.
- The residual is measured inside the lagoon inlet, so it is a proxy for open-coast surge [verify]. It also contains
  seasonal and mean-sea-level anomalies.
- Over 2008–2014 this water level agrees with the legacy MARS2D level: corr 0.995, mean difference −0.001 m.

**Datum issue (applies to v1 and v2) — RESOLVED in data version 2026-10-13b by HAT = +2.14 m MSL. Original note, written for HAT = 1.75 m:** The *predicted astronomical tide alone* (Castelle `tide_msl`) exceeds
+1.75 m MSL in 3.7% of hours; its maximum is +2.45 m MSL and its 99th percentile +2.02 m. So +2.14 m IGN69 (+1.75 m
MSL) is **not** the highest astronomical tide at Truc Vert in these data. HAT-exceedance features (TWL ≥ HAT is
reached in 30% of hourly steps in v2) are therefore much less selective than the thesis intended. The water-level
datum is consistent between sources; the HAT value is what should be checked [verify the PHMA reference used in the
thesis against SHOM].

**Other notes**
- The wave-power columns and `E_*` use the hourly Δt = 1 h. `E_notebook_*` keeps the notebook unit (1e6 J·h·m⁻²)
  and is directly comparable with v1.
- The first 41 days (2008-01-01 → 2008-02-11, before the first used survey) have no profile in force, so their R2%
  is NaN. Hydro covers 2008-01-01 → 2019-12-31 23:00.
- Long gaps (up to 428 days, partly from dropped surveys) are kept. Filter on `interval_days`.
- `period` uses the v1 split: `calibration` if survey_end ≤ 2013-12-01, otherwise `validation`. That makes 2014–2019 all "validation".

**HAT = +2.14 m MSL (data version 2026-10-13b).** Steps with TWL ≥ HAT: 20.8% in v2 (30.7% at 1.75 m) and 27.4% in v1
(37.4% at 1.75 m). The still water level alone exceeds HAT 0.6% of the time in v2 and 0.41% in v1.
