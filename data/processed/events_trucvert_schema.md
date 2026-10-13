# Truc Vert event / interval tables — schema (v1, repo data only)

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
* HAT (PHMA) = +2.14 m IGN69 = **+1.75 m MSL** (`evi.constants.HAT_MSL`).
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
| V_pre_total | m³/m | ∫ z dx over the fixed window x ∈ [0, 139.9 m] on the survey_start profile (relative to the MSL datum) |
| V_pre_upper | m³/m | ∫ max(z − HAT, 0) dx, same window (sand above the HAT plane) |
| V_pre_lower | m³/m | V_pre_total − V_pre_upper |
| berm_volume_pre | m³/m | **proxy**: sand between the planes z = HAT (+1.75) and z = +4.0 m MSL seaward of the dune-toe proxy (landward-most crossing of +4.0 m) — `evi.profiles.berm_volume`. Dune toe at +4 m is an assumption (thesis tested 4/5/6 m NGF) [verify]. It includes any upper-beach sand in that band, not only a morphologically identified berm. |
| intertidal_slope_pre | m/m | least-squares slope of z ∈ [−1.5, +1.5] m MSL (landward of the first −1.5 m crossing) [band verify vs tidal datums] |
| dV_total, dV_upper, dV_lower | m³/m | ΔV over the window covered by **both** profiles, x ∈ [0, x_window_pair]; upper = change of sand above HAT plane; lower = total − upper |
| x_window_pair | m | seaward limit of the pairwise common window |
| dV_total_fixed, dV_upper_fixed, dV_lower_fixed | m³/m | same over the fixed global window [0, x_window_fixed] (comparable across events) |
| x_window_fixed | m | 139.9 m = shortest survey extent among all surveys used |
| days_since_last_storm | d | (start of first storm in interval, or survey_start if none) − end of the previous storm |
| winter | – | storm year July–June of the interval midpoint, e.g. `2013-14` |
| season | – | DJF/MAM/JJA/SON of the interval midpoint |
