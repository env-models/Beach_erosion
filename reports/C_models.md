# C — Modelling report: physics-first baselines, then ML (Agent C)

Branch `revisit-2026`. All numbers below were produced in this session by `python -m evi.models.run_all`
(tables are filled by `python -m evi.models.report v1 v2 v2C` from `figures/tables/C_*.csv`). Thesis numbers are
quoted as "thesis:". The 2017 indicator was published as Nicolae Lerma et al. (2018), *Towards the Development of a
Storm Erosion EWS for the French Aquitaine Coast*, J. Coastal Research SI 85:666–670, doi:10.2112/SI85-134.1
(DOI verified by the orchestrator via Crossref). It is called the **2017/2018 EVI** below.

**Stages that ran:** 1 (2017/2018 EVI baselines) ✔ · 2 (Harley-type, Splinter-flavoured, equilibrium A/B,
ShoreFor-flavoured) ✔ · 3 (LightGBM, XGBoost, random forest + SHAP) ✔ · 4 (GP + coverage) ✔ · 5 (two-stage, hybrid
residual) ✔ · 6 (ablations) ✔ · 7 (PySR) ✘ not run (see Limitations). Data: v1 ✔, v2 (Agent A) ✔, v2C (Agent C's
own independent build from Agent B's files, robustness check) ✔ (with an earlier, single-hold-out layout; see §8).

## 1. Protocol as implemented (`src/evi/models/protocol.py`)

* **Unit** = event = survey-to-survey interval with ≥ 1 storm (`n_storms ≥ 1` in Agent A's table). No event is
  dropped on the value of ΔV. Events with a *missing* target (v2 `dV_total_fixed`, 17 events whose survey does not
  cover the fixed window) are dropped for that target only.
* **Sign convention** (schema): **ΔV > 0 = erosion** (volume lost between `survey_start` and `survey_end`).
* **Resolvability rule** (fixed before looking at any result, using survey spacing only):
  `resolvable = interval_days ≤ 45 d`. Rationale: the author's own diagnosis (HANDOFF §1) that > ~6-week gaps
  merge storms with post-storm recovery. v1: 48 of 51 events resolvable (the 3 excluded are 57 d, 307 d and 71 d).
  Every result is reported on **resolvable** events (headline) and on **all** events.
* **Cross-validation:** leave-one-winter-out (LOWO), grouping on Agent A's `winter` column = storm year July–June of
  the interval midpoint, so summer/autumn intervals belong to the winter that follows (e.g. Oct 2013 → `2013-14`).
* **Hold-outs:** (i) **stress test** = train on winters ≤ 2012-13, test 2013-14 (reported alone; v1 also 2013-14 +
  2014-15 together). (ii) v2 only: **recent hold-out** = train on winters ≤ 2014-15, test 2015-16 → 2019-20.
* **References for skill** (MSE skill = 1 − MSE_model / MSE_ref): climatology = training-fold mean ΔV (`clim`);
  interval-scaled climatology = (Σ ΔV / Σ days over **all** training-winter survey intervals, storm-free included,
  from `intervals_trucvert*.parquet`) × interval_days (`clim_rate`); thesis PPT = `ppt_2stage` (below).
* **Metrics:** RMSE, MAE, out-of-sample R² (1 − SSE/SS about the test mean; can be < 0), bias = mean(pred − obs),
  skill scores; **95 % percentile bootstrap CIs**, 1000 resamples of events, seed 0. n is given for every row.
* **Intervals:** GP posterior (Gaussian, includes the white-noise term) and **CV+ conformal** intervals for six
  models (inner leave-one-winter-out absolute residuals inside each training fold → quantile
  ⌈(n+1)α⌉/n). Coverage at 50/80/90/95 %.
* **Past-only antecedent state:** `V_anom_past` = V_pre_total − mean V_pre_total of surveys in the 365 d before
  `survey_start` (strictly earlier surveys; 0 when none). In v2, 9 events with missing pre-storm volume (survey does
  not cover the fixed window) take the last earlier survey's value (past-only carry-forward; counts in the data-info
  block). The PPT-style binary state and the equilibrium V_eq use the **training-fold** mean V_pre_total
  (fixes HANDOFF §2.1 item 8 leakage).
* **Seeds:** numpy/python 0; LightGBM/XGBoost/RF/GP `random_state = 0`; LightGBM `deterministic=True`.
* **Known in-sample element:** Agent A's storm thresholds (Hs95/Hs75) are computed on 2009-01-01 → 2013-12-01, so
  events in that window are in-sample for the storm *definition* (not for the model fits). The 2013-14 hold-out
  events after 2013-12-01 are not.

### Data versions used

**v1** (repo data, HAT = +2.14 m MSL, data version 2026-10-13b):
<!-- AUTO:datainfo_v1 -->
```
{
  "events": {
    "path": "data/processed/events_trucvert.parquet",
    "mtime": "2026-10-13 23:13:28 CEST",
    "n_rows": 51
  },
  "intervals": {
    "path": "data/processed/intervals_trucvert.parquet",
    "mtime": "2026-10-13 23:13:28 CEST",
    "n_rows": 128
  }
}
```
<!-- /AUTO:datainfo_v1 -->
**v2** (Agent A, Castelle et al. 2020 profiles window w740, hourly Castelle waves with direction, tide + Arcachon
surge proxy, HAT = +2.14 m MSL; features add `mean_dir` and `nao_winter` = DJFM NAO of the event's winter from
`climate_indices.parquet`, a *concurrent seasonal* index, not a forecastable predictor):
<!-- AUTO:datainfo_v2 -->
```
{
  "events": {
    "path": "data/processed/events_trucvert_v2.parquet",
    "mtime": "2026-10-13 23:13:29 CEST",
    "n_rows": 98
  },
  "intervals": {
    "path": "data/processed/intervals_trucvert_v2.parquet",
    "mtime": "2026-10-13 23:13:29 CEST",
    "n_rows": 201
  },
  "n_imputed_pre_state_past_only": {
    "V_pre_total": 9,
    "V_pre_upper": 9,
    "V_pre_lower": 9,
    "intertidal_slope_pre": 1
  }
}
```
<!-- /AUTO:datainfo_v2 -->

## 2. Models (one card each in `reports/C_model_cards/`)

| key | model | what it is |
|---|---|---|
| clim / clim_rate | climatologies | training mean; rate × interval length |
| evi_general | **2017/2018 EVI General** | ΔV = a·E + b, E = notebook energy above HAT (`E_notebook_stormHAT`), all events |
| ppt_all | PPT, honest | separate a·E + b for "fat"/"thin" pre-storm beach (vs training mean volume), fitted on all events |
| tpte_2stage | **TPTE (thesis-style)** | logistic erode/accrete classifier on E → erosive branch a·E + b fitted on training events with ΔV > 0, accretive branch = mean accretion; hard classification |
| ppt_2stage | **PPT (thesis-style)** | as TPTE with binary state in classifier and in the erosive regression. Used as the "thesis PPT" skill reference |
| harley | Harley et al. (2009)-type | ΔV = a·ΣHs²Δt + b over all storm samples (no HAT filter) [verify exact published form] |
| splinter | **Splinter-flavoured** | ΔV = a·ΣPΔt + c·n_clusters + b. *Not* the published Splinter et al. (2014) equation: I could not confirm its exact form offline, so the published relation is **[verify]**; this is a cumulative-storm-power + cluster term stand-in |
| eq_a | Equilibrium A | ΔV = a·E·(V_pre − V_eq) + b (as specified in the task; Yates et al. 2009 flavour) |
| eq_b | Equilibrium B | ΔV = a·E + c·E·(V_pre − V_eq) + b (adds the main energy term) |
| shorefor | ShoreFor-flavoured | ΔV = a·F⁻ + c·F⁺ + b, F = P^0.5·(Ω_eq − Ω)/σ summed over the interval (daily), Ω = Hs/(w_s·Tp), Ω_eq = 10^(−i/φ)-weighted past Ω over 2φ days (Davidson et al. 2013 form [verify]); φ ∈ {15,30,60,120,240} d picked per training fold by in-sample RMSE; w_s = 0.04 m/s [verify D50] |
| lgbm / xgb / rf | gradient boosting / random forest | 11 features (v2: 13), depth-2 trees, ≥ 6 samples per leaf, shrinkage 0.03, 300 trees; RF depth 3, leaf ≥ 4. Fixed a priori; **no tuning** |
| gp | Gaussian process | ConstantKernel·RBF(ARD) + White on standardised [log1p E_HAT, V_anom_past, berm, interval_days] |
| two_stage_ml | two-stage | logistic P(erode) on [E_HAT, V_anom_past, berm] → p·(erosive OLS) + (1−p)·(accretive OLS); expected value, not hard |
| hybrid | hybrid residual | Equilibrium B + LightGBM (100 trees) on its residuals |

Simple models are preferred by design: with n ≈ 40 training events per fold, every tree model is deliberately
shallow and the linear models have 1–4 parameters.

## 3. Results — v1 (repo data, 2008–2014)

### 3.1 Leave-one-winter-out, resolvable events, target ΔV upper beach (`dV_upper`, m³/m above HAT)
<!-- AUTO:lowo_v1_dV_upper_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 48 | 12.2 [9.8, 14.3] | 9.8 | -0.03 [-0.15, -0.01] | -0.1 | 0.00 [0.00, 0.00] | 0.21 | -0.67 |
| Climatology (rate x interval) | 48 | 13.7 [10.6, 16.6] | 9.6 | -0.31 [-0.63, -0.10] | -6.6 | -0.26 [-0.49, 0.03] | 0.00 | -1.11 |
| EVI General (dV ~ E_nbHAT) | 48 | 9.0 [7.3, 10.5] | 7.4 | 0.44 [0.19, 0.61] | +0.0 | 0.46 [0.24, 0.62] | 0.57 | 0.09 |
| PPT (binary state, all events) | 48 | 9.0 [7.0, 10.7] | 7.2 | 0.44 [0.19, 0.61] | +0.1 | 0.45 [0.24, 0.63] | 0.57 | 0.09 |
| TPTE 2-stage (thesis-style) | 48 | 9.6 [7.9, 11.1] | 8.0 | 0.36 [0.03, 0.54] | +3.5 | 0.38 [0.13, 0.57] | 0.51 | -0.04 |
| PPT 2-stage (thesis-style) | 48 | 9.4 [7.6, 11.1] | 7.6 | 0.38 [0.09, 0.57] | +3.3 | 0.40 [0.15, 0.60] | 0.53 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 48 | 8.8 [7.1, 10.2] | 7.2 | 0.47 [0.21, 0.62] | -0.0 | 0.48 [0.26, 0.63] | 0.59 | 0.14 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 48 | 9.2 [7.5, 10.7] | 7.7 | 0.41 [0.12, 0.58] | +0.4 | 0.43 [0.18, 0.60] | 0.55 | 0.04 |
| Equilibrium A (dV ~ E(V-Veq)) | 48 | 12.7 [9.6, 15.3] | 9.9 | -0.11 [-0.68, 0.26] | -0.4 | -0.08 [-0.53, 0.29] | 0.15 | -0.80 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 48 | 9.1 [7.1, 10.8] | 7.3 | 0.43 [0.19, 0.58] | +0.0 | 0.45 [0.25, 0.60] | 0.56 | 0.08 |
| ShoreFor-flavoured (phi by train fit) | 48 | 10.1 [8.1, 12.0] | 7.7 | 0.29 [-0.07, 0.52] | -0.5 | 0.32 [0.01, 0.53] | 0.46 | -0.14 |
| LightGBM | 48 | 10.8 [8.6, 12.8] | 8.4 | 0.19 [-0.25, 0.46] | -0.1 | 0.22 [-0.19, 0.48] | 0.38 | -0.30 |
| XGBoost | 48 | 10.4 [8.5, 12.2] | 8.3 | 0.24 [-0.17, 0.46] | -0.2 | 0.27 [-0.10, 0.49] | 0.42 | -0.23 |
| Random forest | 48 | 9.3 [7.6, 11.0] | 7.4 | 0.39 [0.13, 0.54] | +0.1 | 0.41 [0.18, 0.56] | 0.54 | 0.02 |
| Gaussian process (RBF-ARD + White) | 48 | 12.7 [10.3, 15.0] | 10.3 | -0.13 [-0.48, 0.05] | -0.3 | -0.09 [-0.38, 0.12] | 0.14 | -0.83 |
| Two-stage (logit -> OLS per branch, expected value) | 48 | 9.2 [7.4, 10.8] | 7.6 | 0.41 [0.17, 0.57] | -0.3 | 0.43 [0.23, 0.60] | 0.55 | 0.05 |
| Hybrid (Equilibrium B + LightGBM residual) | 48 | 9.6 [7.8, 11.3] | 7.8 | 0.36 [0.04, 0.55] | +0.0 | 0.38 [0.10, 0.58] | 0.51 | -0.04 |
<!-- /AUTO:lowo_v1_dV_upper_resolvable -->

### 3.2 Leave-one-winter-out, resolvable events, target ΔV total over the fixed 0–139.9 m window (`dV_total_fixed`)
<!-- AUTO:lowo_v1_dV_total_fixed_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 48 | 22.5 [16.6, 27.6] | 16.4 | -0.02 [-0.14, -0.00] | +0.0 | 0.00 [0.00, 0.00] | 0.21 | -1.14 |
| Climatology (rate x interval) | 48 | 25.3 [18.3, 31.7] | 17.4 | -0.29 [-0.63, -0.10] | -12.0 | -0.27 [-0.52, -0.00] | 0.00 | -1.72 |
| EVI General (dV ~ E_nbHAT) | 48 | 14.7 [11.4, 17.9] | 11.1 | 0.57 [0.31, 0.72] | +0.4 | 0.57 [0.35, 0.72] | 0.66 | 0.08 |
| PPT (binary state, all events) | 48 | 14.6 [11.4, 17.6] | 11.0 | 0.57 [0.31, 0.73] | -0.1 | 0.58 [0.33, 0.73] | 0.67 | 0.09 |
| TPTE 2-stage (thesis-style) | 48 | 15.9 [12.7, 19.1] | 12.0 | 0.49 [0.17, 0.65] | +4.8 | 0.50 [0.23, 0.67] | 0.60 | -0.08 |
| PPT 2-stage (thesis-style) | 48 | 15.4 [12.2, 18.3] | 11.6 | 0.53 [0.19, 0.69] | +4.4 | 0.53 [0.26, 0.70] | 0.63 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 48 | 13.7 [11.0, 16.3] | 10.7 | 0.62 [0.37, 0.75] | +0.2 | 0.63 [0.41, 0.76] | 0.71 | 0.20 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 48 | 15.1 [11.9, 18.2] | 11.7 | 0.54 [0.21, 0.71] | +1.6 | 0.55 [0.26, 0.72] | 0.65 | 0.04 |
| Equilibrium A (dV ~ E(V-Veq)) | 48 | 23.1 [16.7, 29.2] | 16.7 | -0.07 [-0.80, 0.35] | -0.7 | -0.06 [-0.69, 0.36] | 0.17 | -1.26 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 48 | 14.1 [11.0, 17.1] | 10.9 | 0.60 [0.39, 0.71] | +0.4 | 0.61 [0.43, 0.72] | 0.69 | 0.15 |
| ShoreFor-flavoured (phi by train fit) | 48 | 18.6 [12.9, 24.2] | 12.4 | 0.30 [-0.08, 0.59] | -1.0 | 0.32 [-0.03, 0.60] | 0.46 | -0.47 |
| LightGBM | 48 | 18.5 [14.1, 22.3] | 13.6 | 0.32 [-0.17, 0.54] | +0.9 | 0.33 [-0.10, 0.56] | 0.47 | -0.44 |
| XGBoost | 48 | 18.4 [13.9, 22.6] | 13.6 | 0.32 [-0.08, 0.55] | -0.4 | 0.33 [-0.01, 0.57] | 0.47 | -0.43 |
| Random forest | 48 | 15.7 [12.1, 18.9] | 11.7 | 0.51 [0.23, 0.64] | -0.2 | 0.51 [0.28, 0.65] | 0.62 | -0.04 |
| Gaussian process (RBF-ARD + White) | 48 | 19.6 [14.6, 24.3] | 14.8 | 0.23 [-0.07, 0.43] | -1.4 | 0.24 [-0.02, 0.45] | 0.40 | -0.63 |
| Two-stage (logit -> OLS per branch, expected value) | 48 | 14.6 [11.4, 17.9] | 11.4 | 0.57 [0.34, 0.71] | -0.4 | 0.58 [0.38, 0.72] | 0.67 | 0.09 |
| Hybrid (Equilibrium B + LightGBM residual) | 48 | 15.8 [12.6, 18.9] | 12.8 | 0.50 [0.23, 0.64] | +0.9 | 0.51 [0.28, 0.66] | 0.61 | -0.06 |
<!-- /AUTO:lowo_v1_dV_total_fixed_resolvable -->

### 3.3 Leave-one-winter-out, ALL events (incl. 57/71/307-day intervals)
`dV_upper`:
<!-- AUTO:lowo_v1_dV_upper_all -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 51 | 12.9 [10.2, 15.5] | 10.1 | -0.03 [-0.14, -0.01] | -0.1 | 0.00 [0.00, 0.00] | 0.16 | -0.23 |
| Climatology (rate x interval) | 51 | 14.0 [10.9, 17.3] | 9.9 | -0.23 [-0.54, -0.04] | -5.9 | -0.19 [-0.41, 0.05] | 0.00 | -0.46 |
| EVI General (dV ~ E_nbHAT) | 51 | 14.1 [9.6, 19.3] | 9.5 | -0.24 [-1.43, 0.26] | +0.6 | -0.21 [-1.30, 0.29] | -0.01 | -0.48 |
| PPT (binary state, all events) | 51 | 11.8 [8.4, 15.1] | 8.1 | 0.13 [-0.43, 0.49] | +0.7 | 0.16 [-0.35, 0.52] | 0.29 | -0.03 |
| TPTE 2-stage (thesis-style) | 51 | 14.0 [10.4, 18.1] | 10.8 | -0.22 [-1.08, 0.19] | +5.0 | -0.18 [-0.96, 0.24] | 0.00 | -0.46 |
| PPT 2-stage (thesis-style) | 51 | 11.6 [8.8, 14.7] | 8.8 | 0.16 [-0.23, 0.44] | +4.4 | 0.19 [-0.16, 0.47] | 0.32 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 51 | 12.8 [9.1, 16.8] | 9.0 | -0.02 [-0.81, 0.34] | +0.3 | 0.01 [-0.71, 0.37] | 0.17 | -0.21 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 51 | 12.2 [8.8, 15.9] | 8.8 | 0.07 [-0.61, 0.42] | +0.5 | 0.10 [-0.55, 0.46] | 0.24 | -0.11 |
| Equilibrium A (dV ~ E(V-Veq)) | 51 | 12.6 [10.1, 14.9] | 10.0 | 0.01 [-0.35, 0.25] | +0.1 | 0.04 [-0.26, 0.28] | 0.19 | -0.18 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 51 | 12.6 [9.2, 16.2] | 9.0 | 0.00 [-0.64, 0.37] | +0.8 | 0.04 [-0.56, 0.40] | 0.19 | -0.19 |
| ShoreFor-flavoured (phi by train fit) | 51 | 13.5 [8.9, 18.7] | 9.0 | -0.13 [-1.40, 0.47] | +1.0 | -0.10 [-1.26, 0.49] | 0.08 | -0.35 |
| LightGBM | 51 | 11.5 [8.8, 14.0] | 8.4 | 0.18 [-0.21, 0.40] | -0.9 | 0.20 [-0.16, 0.42] | 0.33 | 0.02 |
| XGBoost | 51 | 11.4 [8.8, 13.9] | 8.6 | 0.19 [-0.16, 0.40] | -0.6 | 0.22 [-0.10, 0.43] | 0.34 | 0.04 |
| Random forest | 51 | 10.9 [8.1, 13.8] | 8.0 | 0.26 [-0.01, 0.45] | +0.3 | 0.29 [0.05, 0.48] | 0.40 | 0.12 |
| Gaussian process (RBF-ARD + White) | 51 | 12.8 [10.5, 15.2] | 10.3 | -0.02 [-0.30, 0.16] | +1.0 | 0.01 [-0.24, 0.21] | 0.17 | -0.22 |
| Two-stage (logit -> OLS per branch, expected value) | 51 | 14.4 [10.7, 18.3] | 10.4 | -0.30 [-1.10, 0.07] | -0.4 | -0.26 [-1.00, 0.11] | -0.06 | -0.55 |
| Hybrid (Equilibrium B + LightGBM residual) | 51 | 12.6 [9.6, 15.7] | 9.3 | 0.01 [-0.59, 0.36] | +0.5 | 0.04 [-0.49, 0.39] | 0.19 | -0.18 |
<!-- /AUTO:lowo_v1_dV_upper_all -->
`dV_total_fixed`:
<!-- AUTO:lowo_v1_dV_total_fixed_all -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 51 | 26.3 [19.4, 33.5] | 18.2 | -0.01 [-0.11, -0.00] | -0.1 | 0.00 [0.00, 0.00] | 0.11 | -0.61 |
| Climatology (rate x interval) | 51 | 27.9 [20.9, 34.9] | 19.2 | -0.14 [-0.46, 0.04] | -10.9 | -0.13 [-0.37, 0.08] | 0.00 | -0.81 |
| EVI General (dV ~ E_nbHAT) | 51 | 25.1 [15.4, 34.7] | 15.3 | 0.07 [-0.37, 0.45] | +1.0 | 0.08 [-0.33, 0.46] | 0.19 | -0.47 |
| PPT (binary state, all events) | 51 | 21.1 [13.8, 29.2] | 13.8 | 0.35 [0.05, 0.61] | -0.1 | 0.36 [0.10, 0.63] | 0.43 | -0.04 |
| TPTE 2-stage (thesis-style) | 51 | 24.8 [16.5, 33.4] | 17.0 | 0.09 [-0.24, 0.37] | +8.3 | 0.11 [-0.18, 0.40] | 0.21 | -0.44 |
| PPT 2-stage (thesis-style) | 51 | 20.7 [13.7, 28.9] | 14.1 | 0.37 [0.05, 0.63] | +5.9 | 0.38 [0.09, 0.65] | 0.45 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 51 | 22.3 [14.0, 30.6] | 14.2 | 0.27 [-0.01, 0.53] | +0.4 | 0.28 [0.03, 0.54] | 0.36 | -0.16 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 51 | 23.0 [14.1, 31.7] | 14.4 | 0.23 [-0.17, 0.55] | +1.4 | 0.23 [-0.11, 0.57] | 0.32 | -0.23 |
| Equilibrium A (dV ~ E(V-Veq)) | 51 | 26.2 [18.7, 33.8] | 18.4 | -0.01 [-0.51, 0.27] | +0.1 | 0.01 [-0.45, 0.29] | 0.12 | -0.60 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 51 | 22.0 [15.1, 29.3] | 15.0 | 0.29 [0.09, 0.46] | +1.4 | 0.30 [0.11, 0.48] | 0.38 | -0.13 |
| ShoreFor-flavoured (phi by train fit) | 51 | 27.3 [13.6, 38.5] | 15.6 | -0.09 [-0.86, 0.57] | +2.3 | -0.08 [-0.79, 0.58] | 0.04 | -0.73 |
| LightGBM | 51 | 22.5 [15.7, 29.1] | 15.4 | 0.26 [-0.03, 0.48] | -2.0 | 0.27 [0.00, 0.49] | 0.35 | -0.17 |
| XGBoost | 51 | 23.7 [16.3, 31.1] | 16.2 | 0.18 [-0.17, 0.44] | -1.4 | 0.19 [-0.12, 0.46] | 0.28 | -0.31 |
| Random forest | 51 | 20.9 [13.9, 29.4] | 13.8 | 0.36 [0.06, 0.60] | -0.2 | 0.37 [0.11, 0.62] | 0.44 | -0.02 |
| Gaussian process (RBF-ARD + White) | 51 | 21.0 [14.4, 28.4] | 14.6 | 0.35 [0.05, 0.60] | -1.0 | 0.36 [0.08, 0.61] | 0.43 | -0.03 |
| Two-stage (logit -> OLS per branch, expected value) | 51 | 26.1 [18.0, 34.5] | 17.1 | 0.00 [-0.28, 0.25] | -2.3 | 0.01 [-0.23, 0.27] | 0.12 | -0.59 |
| Hybrid (Equilibrium B + LightGBM residual) | 51 | 21.2 [15.4, 27.2] | 14.9 | 0.34 [0.16, 0.48] | +1.1 | 0.35 [0.19, 0.50] | 0.42 | -0.05 |
<!-- /AUTO:lowo_v1_dV_total_fixed_all -->

### 3.4 Winter 2013-14 stress test (train ≤ 2012-13), resolvable events
`dV_upper`:
<!-- AUTO:w1314_v1_dV_upper_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 12 | 12.4 [7.7, 16.1] | 10.0 | -0.24 [-1.14, -0.00] | -5.5 | 0.00 [0.00, 0.00] | 0.39 | -1.84 |
| Climatology (rate x interval) | 12 | 15.9 [9.6, 20.6] | 11.6 | -1.04 [-2.81, -0.40] | -11.4 | -0.64 [-0.90, -0.39] | 0.00 | -3.67 |
| EVI General (dV ~ E_nbHAT) | 12 | 7.6 [4.6, 10.2] | 6.0 | 0.53 [-0.13, 0.80] | -1.3 | 0.63 [0.18, 0.83] | 0.77 | -0.06 |
| PPT (binary state, all events) | 12 | 7.3 [4.7, 9.7] | 6.0 | 0.57 [0.13, 0.80] | -2.0 | 0.65 [0.41, 0.83] | 0.79 | 0.02 |
| TPTE 2-stage (thesis-style) | 12 | 7.8 [5.6, 10.0] | 7.0 | 0.51 [-0.21, 0.75] | +2.8 | 0.60 [-0.11, 0.83] | 0.76 | -0.13 |
| PPT 2-stage (thesis-style) | 12 | 7.4 [5.7, 8.9] | 6.8 | 0.56 [0.06, 0.73] | +0.8 | 0.65 [0.10, 0.83] | 0.79 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 12 | 7.1 [4.5, 9.0] | 5.8 | 0.60 [0.15, 0.78] | -1.6 | 0.68 [0.38, 0.82] | 0.80 | 0.08 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 12 | 7.2 [4.3, 9.4] | 5.7 | 0.58 [0.13, 0.80] | -2.0 | 0.66 [0.36, 0.83] | 0.80 | 0.05 |
| Equilibrium A (dV ~ E(V-Veq)) | 12 | 16.9 [9.3, 23.0] | 12.9 | -1.31 [-4.06, 0.10] | -9.5 | -0.86 [-2.42, 0.21] | -0.13 | -4.28 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 12 | 7.7 [3.9, 11.5] | 5.8 | 0.52 [-0.07, 0.83] | -3.6 | 0.61 [0.26, 0.87] | 0.76 | -0.11 |
| ShoreFor-flavoured (phi by train fit) | 12 | 10.5 [5.5, 13.9] | 7.4 | 0.11 [-0.70, 0.50] | -6.5 | 0.29 [0.03, 0.52] | 0.57 | -1.02 |
| LightGBM | 12 | 7.9 [4.9, 10.4] | 6.3 | 0.50 [0.13, 0.68] | -4.2 | 0.60 [0.47, 0.71] | 0.76 | -0.14 |
| XGBoost | 12 | 8.8 [5.6, 11.6] | 7.5 | 0.37 [-0.12, 0.62] | -5.2 | 0.50 [0.24, 0.67] | 0.69 | -0.43 |
| Random forest | 12 | 7.5 [4.5, 9.9] | 6.1 | 0.55 [0.22, 0.72] | -3.1 | 0.64 [0.49, 0.77] | 0.78 | -0.03 |
| Gaussian process (RBF-ARD + White) | 12 | 11.6 [7.9, 14.6] | 9.8 | -0.09 [-1.12, 0.39] | -1.6 | 0.12 [-0.72, 0.51] | 0.47 | -1.49 |
| Two-stage (logit -> OLS per branch, expected value) | 12 | 8.4 [5.3, 11.3] | 6.8 | 0.43 [-0.14, 0.74] | -3.6 | 0.54 [0.16, 0.78] | 0.72 | -0.30 |
| Hybrid (Equilibrium B + LightGBM residual) | 12 | 8.0 [3.8, 12.0] | 5.7 | 0.49 [-0.16, 0.85] | -2.7 | 0.59 [0.14, 0.89] | 0.75 | -0.17 |
<!-- /AUTO:w1314_v1_dV_upper_resolvable -->
`dV_total_fixed`:
<!-- AUTO:w1314_v1_dV_total_fixed_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 12 | 22.3 [13.8, 29.1] | 18.1 | -0.03 [-0.80, -0.00] | -3.5 | 0.00 [0.00, 0.00] | 0.33 | -1.34 |
| Climatology (rate x interval) | 12 | 27.2 [13.5, 37.0] | 19.4 | -0.53 [-1.66, -0.07] | -16.0 | -0.49 [-0.85, 0.24] | 0.00 | -2.48 |
| EVI General (dV ~ E_nbHAT) | 12 | 13.0 [7.2, 17.5] | 9.5 | 0.65 [0.02, 0.85] | +5.5 | 0.66 [0.28, 0.86] | 0.77 | 0.21 |
| PPT (binary state, all events) | 12 | 13.2 [6.9, 18.3] | 10.2 | 0.64 [-0.02, 0.85] | +3.2 | 0.65 [0.24, 0.85] | 0.76 | 0.18 |
| TPTE 2-stage (thesis-style) | 12 | 14.0 [9.2, 18.0] | 11.2 | 0.59 [-0.41, 0.78] | +8.2 | 0.60 [0.04, 0.82] | 0.73 | 0.07 |
| PPT 2-stage (thesis-style) | 12 | 14.6 [8.3, 19.7] | 11.2 | 0.56 [-0.44, 0.80] | +5.4 | 0.57 [-0.00, 0.83] | 0.71 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 12 | 11.2 [7.0, 14.6] | 8.5 | 0.74 [0.22, 0.86] | +4.9 | 0.75 [0.44, 0.88] | 0.83 | 0.41 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 12 | 10.1 [6.4, 13.3] | 7.9 | 0.79 [0.30, 0.90] | +4.1 | 0.79 [0.49, 0.91] | 0.86 | 0.52 |
| Equilibrium A (dV ~ E(V-Veq)) | 12 | 31.9 [16.7, 45.6] | 23.2 | -1.09 [-3.41, 0.18] | -12.1 | -1.04 [-2.87, 0.23] | -0.37 | -3.77 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 12 | 11.2 [6.1, 15.3] | 8.4 | 0.74 [0.21, 0.89] | +0.7 | 0.75 [0.38, 0.91] | 0.83 | 0.41 |
| ShoreFor-flavoured (phi by train fit) | 12 | 19.3 [10.0, 26.3] | 14.5 | 0.23 [-0.31, 0.47] | -4.8 | 0.25 [0.10, 0.52] | 0.50 | -0.76 |
| LightGBM | 12 | 9.4 [5.7, 12.1] | 7.4 | 0.82 [0.54, 0.91] | -3.2 | 0.82 [0.66, 0.92] | 0.88 | 0.59 |
| XGBoost | 12 | 8.6 [5.9, 11.0] | 7.5 | 0.85 [0.63, 0.90] | -3.4 | 0.85 [0.72, 0.91] | 0.90 | 0.65 |
| Random forest | 12 | 9.3 [5.7, 12.2] | 7.2 | 0.82 [0.53, 0.89] | +1.0 | 0.83 [0.66, 0.91] | 0.88 | 0.59 |
| Gaussian process (RBF-ARD + White) | 12 | 17.5 [10.5, 22.9] | 13.9 | 0.37 [-0.10, 0.50] | -4.4 | 0.38 [0.25, 0.53] | 0.59 | -0.44 |
| Two-stage (logit -> OLS per branch, expected value) | 12 | 11.7 [7.3, 15.1] | 9.6 | 0.72 [0.28, 0.84] | +2.3 | 0.73 [0.44, 0.86] | 0.82 | 0.36 |
| Hybrid (Equilibrium B + LightGBM residual) | 12 | 10.9 [6.0, 14.9] | 8.1 | 0.76 [0.24, 0.90] | -0.2 | 0.76 [0.40, 0.91] | 0.84 | 0.44 |
<!-- /AUTO:w1314_v1_dV_total_fixed_resolvable -->
(All-event versions are in `figures/tables/C_results_v1.csv`, split `holdout_2013-14`, subset `all`; 2013-14 +
2014-15 pooled is split `holdout_2013-14..2014-15(...)`.) Figure: `figures/fig_winter_2013_14.png`.

## 4. Results — v2 (Agent A's extended table, 2008–2019)

### 4.1 LOWO, resolvable, `dV_upper`
<!-- AUTO:lowo_v2_dV_upper_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 91 | 10.7 [8.7, 12.5] | 7.9 | -0.02 [-0.08, -0.01] | -0.0 | 0.00 [0.00, 0.00] | 0.11 | -0.37 |
| Climatology (rate x interval) | 91 | 11.3 [9.0, 13.4] | 7.6 | -0.14 [-0.30, -0.05] | -3.8 | -0.12 [-0.24, 0.02] | 0.00 | -0.53 |
| EVI General (dV ~ E_nbHAT) | 91 | 8.5 [6.8, 10.2] | 6.1 | 0.36 [0.02, 0.57] | +0.1 | 0.37 [0.06, 0.58] | 0.44 | 0.14 |
| PPT (binary state, all events) | 91 | 8.3 [6.7, 9.9] | 5.8 | 0.38 [0.08, 0.57] | -0.0 | 0.39 [0.11, 0.59] | 0.46 | 0.17 |
| TPTE 2-stage (thesis-style) | 91 | 9.5 [8.1, 10.9] | 7.6 | 0.19 [-0.22, 0.44] | +0.4 | 0.21 [-0.18, 0.45] | 0.29 | -0.08 |
| PPT 2-stage (thesis-style) | 91 | 9.1 [7.7, 10.4] | 7.2 | 0.25 [-0.13, 0.46] | +0.9 | 0.27 [-0.07, 0.48] | 0.35 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 91 | 8.3 [6.8, 9.8] | 6.1 | 0.38 [0.14, 0.55] | +0.0 | 0.40 [0.17, 0.56] | 0.46 | 0.17 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 91 | 8.4 [6.9, 9.9] | 6.1 | 0.37 [0.12, 0.55] | +0.0 | 0.38 [0.15, 0.56] | 0.45 | 0.16 |
| Equilibrium A (dV ~ E(V-Veq)) | 91 | 10.8 [8.7, 12.8] | 8.0 | -0.04 [-0.36, 0.17] | -0.3 | -0.02 [-0.32, 0.18] | 0.09 | -0.39 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 91 | 7.9 [6.3, 9.4] | 5.6 | 0.45 [0.25, 0.62] | +0.3 | 0.46 [0.27, 0.63] | 0.51 | 0.26 |
| ShoreFor-flavoured (phi by train fit) | 91 | 8.0 [6.5, 9.4] | 5.9 | 0.43 [0.21, 0.59] | -0.0 | 0.44 [0.24, 0.60] | 0.50 | 0.24 |
| LightGBM | 91 | 8.8 [7.3, 10.3] | 6.6 | 0.30 [0.04, 0.47] | +0.2 | 0.31 [0.08, 0.50] | 0.39 | 0.06 |
| XGBoost | 91 | 8.9 [7.3, 10.3] | 6.6 | 0.29 [0.04, 0.47] | +0.2 | 0.31 [0.07, 0.49] | 0.38 | 0.06 |
| Random forest | 91 | 8.4 [6.9, 9.8] | 6.0 | 0.37 [0.15, 0.51] | -0.1 | 0.38 [0.19, 0.53] | 0.45 | 0.15 |
| Gaussian process (RBF-ARD + White) | 91 | 8.8 [7.1, 10.4] | 6.5 | 0.31 [0.05, 0.48] | -0.2 | 0.33 [0.08, 0.49] | 0.40 | 0.08 |
| Two-stage (logit -> OLS per branch, expected value) | 91 | 8.4 [6.9, 9.9] | 6.0 | 0.37 [0.07, 0.55] | +0.1 | 0.38 [0.10, 0.57] | 0.45 | 0.15 |
| Hybrid (Equilibrium B + LightGBM residual) | 91 | 8.0 [6.4, 9.4] | 5.7 | 0.43 [0.20, 0.59] | +0.3 | 0.44 [0.23, 0.61] | 0.50 | 0.24 |
<!-- /AUTO:lowo_v2_dV_upper_resolvable -->
### 4.2 LOWO, resolvable, `dV_total_fixed`
<!-- AUTO:lowo_v2_dV_total_fixed_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 76 | 18.3 [14.5, 21.7] | 13.7 | -0.02 [-0.10, -0.01] | +0.1 | 0.00 [0.00, 0.00] | 0.13 | -0.56 |
| Climatology (rate x interval) | 76 | 19.6 [15.6, 23.3] | 14.0 | -0.17 [-0.38, -0.04] | -7.3 | -0.15 [-0.32, 0.04] | 0.00 | -0.79 |
| EVI General (dV ~ E_nbHAT) | 76 | 14.3 [11.3, 17.3] | 10.4 | 0.38 [0.05, 0.58] | +0.2 | 0.39 [0.10, 0.59] | 0.47 | 0.06 |
| PPT (binary state, all events) | 76 | 13.3 [10.8, 15.8] | 10.0 | 0.46 [0.17, 0.64] | +0.3 | 0.47 [0.22, 0.66] | 0.54 | 0.18 |
| TPTE 2-stage (thesis-style) | 76 | 15.8 [13.9, 17.9] | 13.0 | 0.24 [-0.16, 0.44] | +1.3 | 0.25 [-0.10, 0.46] | 0.35 | -0.16 |
| PPT 2-stage (thesis-style) | 76 | 14.7 [12.8, 16.6] | 12.3 | 0.35 [-0.02, 0.54] | +2.0 | 0.36 [0.03, 0.56] | 0.44 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 76 | 13.9 [11.3, 16.3] | 10.5 | 0.42 [0.15, 0.57] | +0.0 | 0.43 [0.21, 0.58] | 0.50 | 0.11 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 76 | 14.0 [11.4, 16.5] | 10.4 | 0.40 [0.14, 0.57] | -0.1 | 0.41 [0.18, 0.58] | 0.49 | 0.09 |
| Equilibrium A (dV ~ E(V-Veq)) | 76 | 19.6 [14.7, 25.2] | 13.9 | -0.16 [-1.04, 0.20] | -0.5 | -0.14 [-0.94, 0.22] | 0.01 | -0.78 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 76 | 12.8 [10.4, 15.2] | 9.5 | 0.50 [0.28, 0.65] | +0.2 | 0.51 [0.33, 0.65] | 0.57 | 0.24 |
| ShoreFor-flavoured (phi by train fit) | 76 | 13.4 [11.1, 15.6] | 10.5 | 0.45 [0.20, 0.60] | -0.2 | 0.46 [0.24, 0.61] | 0.53 | 0.17 |
| LightGBM | 76 | 14.6 [11.6, 17.6] | 10.5 | 0.35 [0.08, 0.51] | +0.2 | 0.36 [0.11, 0.53] | 0.45 | 0.01 |
| XGBoost | 76 | 14.2 [11.3, 17.1] | 10.4 | 0.39 [0.14, 0.54] | +0.5 | 0.40 [0.17, 0.55] | 0.48 | 0.06 |
| Random forest | 76 | 14.3 [11.4, 17.0] | 10.4 | 0.38 [0.16, 0.52] | +0.1 | 0.39 [0.20, 0.54] | 0.47 | 0.06 |
| Gaussian process (RBF-ARD + White) | 76 | 14.6 [11.6, 17.4] | 11.0 | 0.35 [0.04, 0.56] | +0.1 | 0.37 [0.08, 0.57] | 0.45 | 0.01 |
| Two-stage (logit -> OLS per branch, expected value) | 76 | 14.3 [11.6, 16.9] | 10.6 | 0.38 [0.11, 0.55] | +0.1 | 0.39 [0.15, 0.56] | 0.47 | 0.05 |
| Hybrid (Equilibrium B + LightGBM residual) | 76 | 13.2 [10.6, 15.6] | 10.1 | 0.47 [0.22, 0.62] | +0.9 | 0.48 [0.26, 0.64] | 0.55 | 0.19 |
<!-- /AUTO:lowo_v2_dV_total_fixed_resolvable -->
### 4.3 LOWO, all events, `dV_upper`
<!-- AUTO:lowo_v2_dV_upper_all -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 98 | 10.7 [8.8, 12.6] | 8.0 | -0.02 [-0.08, -0.01] | -0.0 | 0.00 [0.00, 0.00] | 0.10 | 0.24 |
| Climatology (rate x interval) | 98 | 11.2 [9.0, 13.5] | 7.8 | -0.13 [-0.28, -0.05] | -3.7 | -0.11 [-0.22, 0.03] | 0.00 | 0.16 |
| EVI General (dV ~ E_nbHAT) | 98 | 11.3 [8.3, 14.5] | 7.7 | -0.15 [-0.90, 0.20] | +0.3 | -0.12 [-0.83, 0.22] | -0.01 | 0.15 |
| PPT (binary state, all events) | 98 | 13.0 [8.6, 17.4] | 7.9 | -0.52 [-2.07, 0.26] | +0.7 | -0.49 [-1.93, 0.28] | -0.34 | -0.12 |
| TPTE 2-stage (thesis-style) | 98 | 12.3 [10.1, 14.7] | 9.7 | -0.35 [-1.18, 0.07] | +3.7 | -0.32 [-1.07, 0.10] | -0.19 | -0.00 |
| PPT 2-stage (thesis-style) | 98 | 12.3 [9.3, 15.6] | 8.8 | -0.35 [-1.46, 0.23] | +2.9 | -0.32 [-1.39, 0.25] | -0.19 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 98 | 10.9 [8.4, 13.4] | 7.6 | -0.07 [-0.62, 0.20] | +0.2 | -0.04 [-0.55, 0.22] | 0.06 | 0.21 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 98 | 9.1 [7.6, 10.6] | 6.8 | 0.25 [-0.02, 0.44] | +0.2 | 0.27 [0.01, 0.45] | 0.34 | 0.44 |
| Equilibrium A (dV ~ E(V-Veq)) | 98 | 10.4 [8.5, 12.3] | 7.8 | 0.03 [-0.18, 0.17] | -0.1 | 0.05 [-0.14, 0.20] | 0.14 | 0.28 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 98 | 10.9 [8.3, 13.5] | 7.4 | -0.06 [-0.77, 0.31] | +0.2 | -0.04 [-0.67, 0.33] | 0.06 | 0.21 |
| ShoreFor-flavoured (phi by train fit) | 98 | 8.2 [6.8, 9.6] | 6.3 | 0.39 [0.14, 0.56] | -0.0 | 0.41 [0.18, 0.57] | 0.47 | 0.55 |
| LightGBM | 98 | 9.5 [7.8, 11.1] | 6.9 | 0.19 [-0.12, 0.39] | -0.1 | 0.21 [-0.08, 0.41] | 0.29 | 0.40 |
| XGBoost | 98 | 9.6 [7.9, 11.2] | 7.0 | 0.17 [-0.14, 0.37] | +0.1 | 0.18 [-0.09, 0.38] | 0.26 | 0.38 |
| Random forest | 98 | 8.8 [7.2, 10.4] | 6.3 | 0.30 [0.08, 0.46] | +0.1 | 0.31 [0.10, 0.47] | 0.38 | 0.48 |
| Gaussian process (RBF-ARD + White) | 98 | 8.6 [7.2, 10.0] | 6.7 | 0.33 [0.12, 0.48] | -0.0 | 0.35 [0.16, 0.49] | 0.41 | 0.51 |
| Two-stage (logit -> OLS per branch, expected value) | 98 | 11.1 [8.8, 13.5] | 7.6 | -0.11 [-0.74, 0.24] | -0.0 | -0.08 [-0.66, 0.25] | 0.03 | 0.18 |
| Hybrid (Equilibrium B + LightGBM residual) | 98 | 10.4 [7.7, 13.3] | 6.9 | 0.03 [-0.70, 0.45] | -0.1 | 0.05 [-0.62, 0.46] | 0.14 | 0.28 |
<!-- /AUTO:lowo_v2_dV_upper_all -->
### 4.4 Winter 2013-14 stress test (train ≤ 2012-13), resolvable, `dV_upper` / `dV_total_fixed`
<!-- AUTO:w1314_v2_dV_upper_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 12 | 12.2 [4.3, 18.0] | 8.0 | -0.11 [-0.82, -0.00] | -3.9 | 0.00 [0.00, 0.00] | 0.28 | -0.02 |
| Climatology (rate x interval) | 12 | 14.5 [4.0, 21.1] | 8.8 | -0.55 [-1.31, -0.26] | -8.6 | -0.40 [-0.66, -0.11] | 0.00 | -0.42 |
| EVI General (dV ~ E_nbHAT) | 12 | 12.7 [5.0, 19.2] | 8.4 | -0.20 [-6.71, 0.72] | +1.8 | -0.08 [-6.44, 0.76] | 0.23 | -0.09 |
| PPT (binary state, all events) | 12 | 11.7 [4.6, 17.5] | 7.8 | -0.01 [-5.42, 0.79] | +1.6 | 0.09 [-5.19, 0.82] | 0.35 | 0.08 |
| TPTE 2-stage (thesis-style) | 12 | 12.6 [7.4, 17.9] | 10.0 | -0.17 [-11.44, 0.63] | +1.4 | -0.05 [-6.65, 0.71] | 0.25 | -0.07 |
| PPT 2-stage (thesis-style) | 12 | 12.2 [7.0, 17.3] | 9.7 | -0.10 [-8.88, 0.67] | +2.1 | 0.01 [-5.94, 0.75] | 0.29 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 12 | 11.1 [5.1, 15.6] | 8.0 | 0.09 [-3.81, 0.69] | +0.4 | 0.18 [-3.31, 0.72] | 0.41 | 0.17 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 12 | 11.4 [4.9, 16.5] | 7.9 | 0.03 [-4.42, 0.72] | +1.1 | 0.13 [-4.09, 0.76] | 0.38 | 0.12 |
| Equilibrium A (dV ~ E(V-Veq)) | 12 | 14.8 [8.8, 19.7] | 10.6 | -0.62 [-4.86, -0.09] | -8.6 | -0.45 [-3.82, 0.01] | -0.04 | -0.48 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 12 | 11.2 [4.0, 16.5] | 7.6 | 0.07 [-4.29, 0.76] | +0.6 | 0.17 [-4.05, 0.79] | 0.40 | 0.16 |
| ShoreFor-flavoured (phi by train fit) | 12 | 9.3 [5.1, 12.6] | 6.9 | 0.35 [-1.14, 0.57] | -3.0 | 0.42 [-0.81, 0.60] | 0.58 | 0.41 |
| LightGBM | 12 | 7.9 [5.5, 10.3] | 6.6 | 0.53 [-0.93, 0.63] | -3.6 | 0.58 [-0.55, 0.69] | 0.70 | 0.57 |
| XGBoost | 12 | 8.4 [4.4, 11.9] | 6.4 | 0.48 [-0.46, 0.63] | -3.3 | 0.53 [-0.14, 0.66] | 0.67 | 0.52 |
| Random forest | 12 | 9.0 [4.5, 12.6] | 6.7 | 0.40 [-1.71, 0.59] | -1.5 | 0.46 [-0.28, 0.63] | 0.61 | 0.45 |
| Gaussian process (RBF-ARD + White) | 12 | 7.6 [3.7, 10.6] | 5.4 | 0.57 [-1.96, 0.86] | -2.1 | 0.61 [-1.00, 0.88] | 0.72 | 0.60 |
| Two-stage (logit -> OLS per branch, expected value) | 12 | 11.7 [4.6, 17.5] | 7.7 | -0.01 [-5.32, 0.76] | +1.0 | 0.09 [-5.06, 0.78] | 0.35 | 0.08 |
| Hybrid (Equilibrium B + LightGBM residual) | 12 | 10.1 [3.5, 14.9] | 6.7 | 0.24 [-3.53, 0.87] | -0.7 | 0.32 [-3.12, 0.88] | 0.51 | 0.31 |
<!-- /AUTO:w1314_v2_dV_upper_resolvable -->
<!-- AUTO:w1314_v2_dV_total_fixed_resolvable -->
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 8 | 20.9 [10.1, 32.2] | 16.1 | -0.02 [-1.47, -0.00] | -3.2 | 0.00 [0.00, 0.00] | 0.27 | -0.63 |
| Climatology (rate x interval) | 8 | 24.6 [8.0, 38.6] | 16.2 | -0.41 [-1.69, -0.03] | -13.2 | -0.38 [-1.00, 0.59] | 0.00 | -1.24 |
| EVI General (dV ~ E_nbHAT) | 8 | 19.4 [6.9, 31.3] | 13.2 | 0.12 [-3.79, 0.87] | +6.7 | 0.14 [-3.52, 0.88] | 0.38 | -0.40 |
| PPT (binary state, all events) | 8 | 15.3 [8.8, 22.2] | 12.7 | 0.46 [-0.63, 0.54] | +1.5 | 0.47 [-0.06, 0.55] | 0.61 | 0.13 |
| TPTE 2-stage (thesis-style) | 8 | 17.9 [9.9, 26.0] | 14.9 | 0.26 [-3.08, 0.76] | +8.6 | 0.27 [-2.19, 0.79] | 0.47 | -0.19 |
| PPT 2-stage (thesis-style) | 8 | 16.4 [8.9, 24.1] | 13.5 | 0.37 [-1.50, 0.50] | +3.0 | 0.39 [-0.29, 0.53] | 0.55 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 8 | 14.0 [5.9, 20.2] | 10.7 | 0.54 [-0.94, 0.81] | +3.1 | 0.55 [-0.67, 0.82] | 0.67 | 0.27 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 8 | 15.2 [6.4, 23.1] | 11.3 | 0.46 [-1.69, 0.85] | +4.7 | 0.48 [-1.41, 0.86] | 0.62 | 0.15 |
| Equilibrium A (dV ~ E(V-Veq)) | 8 | 41.0 [9.8, 64.2] | 26.5 | -2.92 [-17.60, -0.04] | -18.2 | -2.83 [-16.52, 0.25] | -1.78 | -5.25 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 8 | 10.8 [6.4, 15.4] | 9.0 | 0.73 [-0.06, 0.79] | +0.1 | 0.73 [0.30, 0.80] | 0.81 | 0.56 |
| ShoreFor-flavoured (phi by train fit) | 8 | 13.1 [7.1, 17.9] | 10.3 | 0.60 [-0.89, 0.76] | -0.1 | 0.61 [-0.40, 0.78] | 0.72 | 0.36 |
| LightGBM | 8 | 16.8 [4.0, 27.5] | 10.1 | 0.34 [-0.47, 0.89] | -3.7 | 0.36 [0.11, 0.90] | 0.53 | -0.05 |
| XGBoost | 8 | 13.1 [2.8, 21.5] | 7.8 | 0.60 [0.11, 0.95] | -3.1 | 0.61 [0.47, 0.95] | 0.72 | 0.37 |
| Random forest | 8 | 15.8 [6.7, 24.7] | 11.8 | 0.42 [-0.80, 0.72] | -0.7 | 0.43 [0.10, 0.75] | 0.59 | 0.07 |
| Gaussian process (RBF-ARD + White) | 8 | 14.6 [8.3, 21.4] | 12.0 | 0.50 [-0.59, 0.56] | +1.0 | 0.51 [0.11, 0.58] | 0.65 | 0.21 |
| Two-stage (logit -> OLS per branch, expected value) | 8 | 17.6 [8.4, 26.1] | 13.5 | 0.28 [-3.22, 0.84] | +8.0 | 0.30 [-2.39, 0.85] | 0.49 | -0.15 |
| Hybrid (Equilibrium B + LightGBM residual) | 8 | 11.8 [7.0, 15.6] | 10.2 | 0.68 [-0.78, 0.80] | -3.7 | 0.68 [-0.20, 0.81] | 0.77 | 0.48 |
<!-- /AUTO:w1314_v2_dV_total_fixed_resolvable -->
### 4.5 Recent hold-out (train ≤ 2014-15, test 2015-16 → 2019-20)
<!-- AUTO:recent_v2 -->
`dV_upper`, resolvable, split `recent_2015-16..2019-20(train<= 2014-15)`:
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 38 | 8.5 [6.7, 10.5] | 6.9 | -0.01 [-0.23, -0.00] | +0.9 | 0.00 [0.00, 0.00] | 0.12 | -0.63 |
| Climatology (rate x interval) | 38 | 9.1 [6.6, 11.8] | 6.8 | -0.15 [-0.42, -0.01] | -3.3 | -0.14 [-0.39, 0.17] | 0.00 | -0.86 |
| EVI General (dV ~ E_nbHAT) | 38 | 6.7 [4.6, 8.9] | 4.9 | 0.37 [-0.00, 0.62] | -1.3 | 0.38 [0.04, 0.64] | 0.45 | -0.02 |
| PPT (binary state, all events) | 38 | 6.4 [4.0, 8.6] | 4.4 | 0.43 [0.01, 0.73] | -1.0 | 0.44 [0.05, 0.74] | 0.51 | 0.08 |
| TPTE 2-stage (thesis-style) | 38 | 7.8 [5.3, 10.3] | 5.8 | 0.15 [-0.45, 0.54] | -2.0 | 0.16 [-0.39, 0.56] | 0.26 | -0.37 |
| PPT 2-stage (thesis-style) | 38 | 6.7 [4.7, 8.4] | 5.0 | 0.38 [-0.14, 0.67] | -0.0 | 0.39 [-0.06, 0.67] | 0.46 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 38 | 6.9 [4.7, 9.1] | 5.0 | 0.34 [-0.10, 0.66] | -0.4 | 0.35 [-0.05, 0.67] | 0.43 | -0.06 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 38 | 7.1 [5.0, 9.3] | 5.3 | 0.29 [-0.14, 0.60] | -0.9 | 0.30 [-0.08, 0.61] | 0.38 | -0.15 |
| Equilibrium A (dV ~ E(V-Veq)) | 38 | 7.8 [6.3, 9.3] | 6.3 | 0.16 [-0.18, 0.29] | +1.5 | 0.17 [0.03, 0.30] | 0.27 | -0.35 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 38 | 6.2 [4.1, 8.2] | 4.5 | 0.47 [0.08, 0.73] | -0.6 | 0.47 [0.13, 0.75] | 0.54 | 0.14 |
| ShoreFor-flavoured (phi by train fit) | 38 | 6.3 [4.3, 8.2] | 4.6 | 0.46 [0.08, 0.72] | +0.1 | 0.46 [0.14, 0.72] | 0.53 | 0.12 |
| LightGBM | 38 | 9.2 [6.9, 11.7] | 7.1 | -0.18 [-1.01, 0.34] | +3.2 | -0.17 [-0.85, 0.36] | -0.03 | -0.91 |
| XGBoost | 38 | 8.4 [6.1, 10.8] | 6.4 | 0.01 [-0.67, 0.47] | +3.2 | 0.02 [-0.54, 0.48] | 0.14 | -0.59 |
| Random forest | 38 | 6.9 [4.8, 9.1] | 5.1 | 0.33 [-0.08, 0.63] | +0.0 | 0.34 [-0.03, 0.64] | 0.42 | -0.08 |
| Gaussian process (RBF-ARD + White) | 38 | 7.1 [5.5, 8.5] | 5.6 | 0.30 [-0.23, 0.59] | +2.2 | 0.31 [-0.16, 0.60] | 0.39 | -0.13 |
| Two-stage (logit -> OLS per branch, expected value) | 38 | 6.6 [4.6, 8.5] | 4.7 | 0.39 [0.08, 0.61] | +0.1 | 0.39 [0.14, 0.63] | 0.47 | 0.01 |
| Hybrid (Equilibrium B + LightGBM residual) | 38 | 6.8 [4.4, 9.2] | 4.6 | 0.35 [-0.17, 0.71] | +1.8 | 0.36 [-0.07, 0.71] | 0.44 | -0.05 |

`dV_total_fixed`, resolvable, split `recent_2015-16..2019-20(train<= 2014-15)`:
| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |
|---|---|---|---|---|---|---|---|---|
| Climatology (train mean) | 36 | 16.9 [13.8, 20.0] | 14.4 | -0.01 [-0.23, -0.00] | +1.7 | 0.00 [0.00, 0.00] | 0.11 | -0.45 |
| Climatology (rate x interval) | 36 | 17.9 [13.6, 22.4] | 13.8 | -0.13 [-0.43, -0.01] | -6.2 | -0.12 [-0.39, 0.18] | 0.00 | -0.62 |
| EVI General (dV ~ E_nbHAT) | 36 | 12.9 [9.4, 16.3] | 9.7 | 0.41 [0.11, 0.61] | -1.5 | 0.41 [0.13, 0.64] | 0.48 | 0.15 |
| PPT (binary state, all events) | 36 | 13.5 [9.9, 17.3] | 10.4 | 0.35 [-0.11, 0.64] | -2.3 | 0.36 [-0.07, 0.65] | 0.43 | 0.07 |
| TPTE 2-stage (thesis-style) | 36 | 14.3 [11.8, 16.8] | 11.6 | 0.28 [-0.10, 0.46] | +5.1 | 0.28 [0.06, 0.47] | 0.36 | -0.04 |
| PPT 2-stage (thesis-style) | 36 | 14.1 [10.9, 17.1] | 11.7 | 0.30 [-0.15, 0.57] | +3.2 | 0.31 [-0.06, 0.58] | 0.38 | 0.00 |
| Harley-type (dV ~ sum Hs2 dt) | 36 | 13.1 [9.7, 16.6] | 10.1 | 0.39 [0.01, 0.63] | -0.2 | 0.40 [0.06, 0.64] | 0.46 | 0.13 |
| Splinter-flavoured (dV ~ sum P dt + n_clusters) | 36 | 13.3 [9.9, 16.8] | 10.3 | 0.38 [0.01, 0.62] | -0.7 | 0.38 [0.05, 0.63] | 0.45 | 0.11 |
| Equilibrium A (dV ~ E(V-Veq)) | 36 | 15.9 [13.2, 18.4] | 13.6 | 0.11 [-0.17, 0.19] | +2.2 | 0.11 [0.03, 0.21] | 0.21 | -0.28 |
| Equilibrium B (dV ~ E + E(V-Veq)) | 36 | 12.2 [8.7, 15.5] | 9.1 | 0.48 [0.16, 0.71] | -1.1 | 0.48 [0.18, 0.71] | 0.54 | 0.25 |
| ShoreFor-flavoured (phi by train fit) | 36 | 12.3 [9.5, 15.1] | 9.9 | 0.46 [0.11, 0.68] | +0.9 | 0.47 [0.18, 0.69] | 0.53 | 0.23 |
| LightGBM | 36 | 14.6 [10.5, 19.1] | 11.1 | 0.25 [-0.38, 0.59] | +0.0 | 0.26 [-0.31, 0.60] | 0.34 | -0.07 |
| XGBoost | 36 | 14.4 [10.7, 18.1] | 11.0 | 0.27 [-0.28, 0.59] | +1.6 | 0.28 [-0.19, 0.60] | 0.36 | -0.05 |
| Random forest | 36 | 13.1 [9.7, 16.6] | 9.9 | 0.39 [0.03, 0.61] | -1.8 | 0.40 [0.08, 0.63] | 0.46 | 0.13 |
| Gaussian process (RBF-ARD + White) | 36 | 12.7 [9.6, 15.7] | 10.1 | 0.43 [0.11, 0.65] | +0.9 | 0.44 [0.15, 0.65] | 0.50 | 0.18 |
| Two-stage (logit -> OLS per branch, expected value) | 36 | 12.8 [9.1, 16.2] | 9.5 | 0.42 [0.11, 0.63] | -1.7 | 0.43 [0.13, 0.65] | 0.49 | 0.17 |
| Hybrid (Equilibrium B + LightGBM residual) | 36 | 12.2 [8.4, 16.1] | 8.8 | 0.47 [0.02, 0.74] | -0.9 | 0.48 [0.09, 0.74] | 0.53 | 0.24 |

<!-- /AUTO:recent_v2 -->

**Reading v2.** v2 has 98 events (91 resolvable; 76 resolvable with a `dV_total_fixed` value). On LOWO the
ranking is the same as v1, and it is still a physics/linear story: for `dV_upper`, Equilibrium B skill 0.46
[0.27, 0.63] vs EVI General 0.37 [0.06, 0.58] vs LightGBM 0.31 [0.08, 0.50] (n = 91). On the **2013-14 stress test**
(train ≤ 2012-13, n = 12) the linear energy models lose their skill on `dV_upper` (EVI General −0.08, CI
[−6.44, 0.76]); GP (0.61 [−1.00, 0.88]), LightGBM (0.58 [−0.55, 0.69]) and ShoreFor-flavoured (0.42) do better,
but every lower CI bound is below zero, so 12 events cannot separate them. The single event that drives this is
TV20140131 (observed 5.2 m³/m, EVI predicted 39.7; see `figures/tables/C_pred_v2_dV_upper_resolvable_holdout.csv`).
On the **recent hold-out** (train ≤ 2014-15, test 2015-16 → 2019-20, n = 38 resolvable), Equilibrium B (0.47
[0.13, 0.75]) and ShoreFor-flavoured (0.46 [0.14, 0.72]) lead, EVI General is at 0.38 [0.04, 0.64], and the boosted
trees fail (LightGBM −0.17 [−0.85, 0.36]). The ML models' winter-2013-14 advantage does **not** carry over to the
recent winters.

## 5. Ablations (one question at a time; OLS family unless stated; LOWO; paired bootstrap of ΔRMSE)

Negative ΔRMSE = the variant is better. "Reference" is the simpler / thesis choice.

### v1
<!-- AUTO:abl_v1 -->
| target | subset | question | n | RMSE variant | RMSE reference | ΔRMSE (variant − ref) [95 % CI] | skill vs clim (variant / ref) |
|---|---|---|---|---|---|---|---|
| dV_upper | resolvable | Antecedent state (past-only anomaly): continuous vs binary | 48 | 9.15 | 9.13 | +0.02 [-0.41, +0.43] | 0.44 / 0.44 |
| dV_upper | resolvable | Antecedent state (vs training-mean volume): continuous vs binary | 48 | 9.07 | 8.94 | +0.13 [-0.52, +0.85] | 0.45 / 0.46 |
| dV_upper | resolvable | Antecedent state (continuous, past-only) vs none | 48 | 9.15 | 9.00 | +0.15 [-0.71, +0.91] | 0.44 / 0.46 |
| dV_upper | resolvable | Berm volume (continuous) vs none | 48 | 8.56 | 9.00 | -0.44 [-1.73, +0.70] | 0.51 / 0.46 |
| dV_upper | resolvable | Cluster count: with vs without | 48 | 9.60 | 9.15 | +0.45 [+0.01, +0.96] | 0.38 / 0.44 |
| dV_upper | resolvable | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 48 | 9.23 | 9.00 | +0.23 [+0.02, +0.43] | 0.43 / 0.46 |
| dV_upper | resolvable | Energy: notebook units vs Hs2 dt (HAT) | 48 | 9.00 | 9.00 | +0.00 [-0.00, +0.00] | 0.46 / 0.46 |
| dV_upper | resolvable | Energy: HAT-filtered vs all-storm (Hs2 dt) | 48 | 9.00 | 8.76 | +0.24 [-0.21, +0.71] | 0.46 / 0.48 |
| dV_upper | resolvable | Energy: HAT-filtered vs all-storm (flux) | 48 | 9.23 | 8.89 | +0.34 [-0.08, +0.75] | 0.43 / 0.47 |
| dV_upper | resolvable | ML: LightGBM with vs without antecedent features | 48 | 10.77 | 10.90 | -0.13 [-1.20, +0.95] | 0.22 / 0.20 |
| dV_upper | all | Antecedent state (past-only anomaly): continuous vs binary | 51 | 13.57 | 12.30 | +1.27 [+0.09, +2.47] | -0.11 / 0.09 |
| dV_upper | all | Antecedent state (vs training-mean volume): continuous vs binary | 51 | 12.64 | 12.05 | +0.59 [-0.43, +1.75] | 0.04 / 0.12 |
| dV_upper | all | Antecedent state (continuous, past-only) vs none | 51 | 13.57 | 14.12 | -0.55 [-2.04, +1.14] | -0.11 / -0.21 |
| dV_upper | all | Berm volume (continuous) vs none | 51 | 11.41 | 14.12 | -2.71 [-5.08, -0.56] | 0.21 / -0.21 |
| dV_upper | all | Cluster count: with vs without | 51 | 13.25 | 13.57 | -0.32 [-1.08, +0.49] | -0.06 / -0.11 |
| dV_upper | all | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 51 | 14.08 | 14.12 | -0.05 [-0.20, +0.11] | -0.20 / -0.21 |
| dV_upper | all | Energy: notebook units vs Hs2 dt (HAT) | 51 | 14.12 | 14.12 | -0.00 [-0.00, +0.00] | -0.21 / -0.21 |
| dV_upper | all | Energy: HAT-filtered vs all-storm (Hs2 dt) | 51 | 14.12 | 12.78 | +1.34 [+0.37, +2.55] | -0.21 / 0.01 |
| dV_upper | all | Energy: HAT-filtered vs all-storm (flux) | 51 | 14.08 | 12.79 | +1.29 [+0.40, +2.40] | -0.20 / 0.01 |
| dV_upper | all | ML: LightGBM with vs without antecedent features | 51 | 11.48 | 11.79 | -0.31 [-1.51, +1.10] | 0.20 / 0.16 |
| dV_total_fixed | resolvable | Antecedent state (past-only anomaly): continuous vs binary | 48 | 14.39 | 15.05 | -0.66 [-1.27, -0.07] | 0.59 / 0.55 |
| dV_total_fixed | resolvable | Antecedent state (vs training-mean volume): continuous vs binary | 48 | 14.14 | 14.57 | -0.44 [-1.53, +0.77] | 0.61 / 0.58 |
| dV_total_fixed | resolvable | Antecedent state (continuous, past-only) vs none | 48 | 14.39 | 14.71 | -0.32 [-1.35, +0.56] | 0.59 / 0.57 |
| dV_total_fixed | resolvable | Berm volume (continuous) vs none | 48 | 14.72 | 14.71 | +0.02 [-1.39, +1.42] | 0.57 / 0.57 |
| dV_total_fixed | resolvable | Cluster count: with vs without | 48 | 15.83 | 14.39 | +1.44 [-0.62, +3.94] | 0.51 / 0.59 |
| dV_total_fixed | resolvable | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 48 | 15.23 | 14.71 | +0.52 [-0.05, +0.99] | 0.54 / 0.57 |
| dV_total_fixed | resolvable | Energy: notebook units vs Hs2 dt (HAT) | 48 | 14.71 | 14.71 | -0.00 [-0.00, +0.00] | 0.57 / 0.57 |
| dV_total_fixed | resolvable | Energy: HAT-filtered vs all-storm (Hs2 dt) | 48 | 14.71 | 13.71 | +1.00 [+0.02, +1.92] | 0.57 / 0.63 |
| dV_total_fixed | resolvable | Energy: HAT-filtered vs all-storm (flux) | 48 | 15.23 | 14.05 | +1.18 [+0.26, +1.98] | 0.54 / 0.61 |
| dV_total_fixed | resolvable | ML: LightGBM with vs without antecedent features | 48 | 18.46 | 17.18 | +1.28 [-0.02, +2.61] | 0.33 / 0.42 |
| dV_total_fixed | all | Antecedent state (past-only anomaly): continuous vs binary | 51 | 23.50 | 23.16 | +0.34 [-1.18, +1.86] | 0.20 / 0.22 |
| dV_total_fixed | all | Antecedent state (vs training-mean volume): continuous vs binary | 51 | 22.04 | 21.13 | +0.90 [-1.29, +3.72] | 0.30 / 0.35 |
| dV_total_fixed | all | Antecedent state (continuous, past-only) vs none | 51 | 23.50 | 25.14 | -1.64 [-4.47, +1.14] | 0.20 / 0.08 |
| dV_total_fixed | all | Berm volume (continuous) vs none | 51 | 22.78 | 25.14 | -2.36 [-5.12, +0.68] | 0.25 / 0.08 |
| dV_total_fixed | all | Cluster count: with vs without | 51 | 24.13 | 23.50 | +0.63 [-0.47, +1.78] | 0.16 / 0.20 |
| dV_total_fixed | all | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 51 | 25.11 | 25.14 | -0.04 [-0.31, +0.35] | 0.09 / 0.08 |
| dV_total_fixed | all | Energy: notebook units vs Hs2 dt (HAT) | 51 | 25.14 | 25.14 | +0.00 [-0.00, +0.00] | 0.08 / 0.08 |
| dV_total_fixed | all | Energy: HAT-filtered vs all-storm (Hs2 dt) | 51 | 25.14 | 22.31 | +2.83 [+1.04, +5.07] | 0.08 / 0.28 |
| dV_total_fixed | all | Energy: HAT-filtered vs all-storm (flux) | 51 | 25.11 | 22.34 | +2.77 [+1.11, +4.87] | 0.09 / 0.28 |
| dV_total_fixed | all | ML: LightGBM with vs without antecedent features | 51 | 22.46 | 22.49 | -0.03 [-1.50, +1.73] | 0.27 / 0.27 |
<!-- /AUTO:abl_v1 -->
Target ablation (EVI-type OLS on E_HAT, LOWO):
<!-- AUTO:ablt_v1 -->
| target | subset | n | sd(obs) | RMSE | R² [95 % CI] | skill vs clim [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | 48 | 12.1 | 9.0 | 0.44 [0.19, 0.61] | 0.46 [0.24, 0.62] |
| dV_upper | all | 51 | 12.8 | 14.1 | -0.24 [-1.43, 0.26] | -0.21 [-1.30, 0.29] |
| dV_total_fixed | resolvable | 48 | 22.6 | 14.7 | 0.57 [0.31, 0.72] | 0.57 [0.35, 0.72] |
| dV_total_fixed | all | 51 | 26.4 | 25.1 | 0.07 [-0.37, 0.45] | 0.08 [-0.33, 0.46] |
| dV_total | resolvable | 48 | 34.7 | 27.3 | 0.37 [-0.08, 0.55] | 0.38 [-0.02, 0.57] |
| dV_total | all | 51 | 38.9 | 38.3 | 0.01 [-0.56, 0.34] | 0.02 [-0.52, 0.36] |
| dV_lower_fixed | resolvable | 48 | 14.4 | 11.5 | 0.35 [0.04, 0.56] | 0.36 [0.10, 0.57] |
| dV_lower_fixed | all | 51 | 17.1 | 15.0 | 0.21 [-0.01, 0.40] | 0.22 [0.04, 0.41] |
<!-- /AUTO:ablt_v1 -->

### v2
<!-- AUTO:abl_v2 -->
| target | subset | question | n | RMSE variant | RMSE reference | ΔRMSE (variant − ref) [95 % CI] | skill vs clim (variant / ref) |
|---|---|---|---|---|---|---|---|
| dV_upper | resolvable | Antecedent state (past-only anomaly): continuous vs binary | 91 | 7.92 | 8.21 | -0.30 [-1.19, +0.41] | 0.45 / 0.41 |
| dV_upper | resolvable | Antecedent state (vs training-mean volume): continuous vs binary | 91 | 7.87 | 8.19 | -0.32 [-1.31, +0.58] | 0.46 / 0.41 |
| dV_upper | resolvable | Antecedent state (continuous, past-only) vs none | 91 | 7.92 | 8.47 | -0.55 [-1.69, +0.24] | 0.45 / 0.37 |
| dV_upper | resolvable | Berm volume (continuous) vs none | 91 | 11.64 | 8.47 | +3.18 [-0.60, +8.80] | -0.19 / 0.37 |
| dV_upper | resolvable | Cluster count: with vs without | 91 | 8.00 | 7.92 | +0.08 [-0.05, +0.22] | 0.44 / 0.45 |
| dV_upper | resolvable | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 91 | 8.66 | 8.47 | +0.20 [-0.03, +0.48] | 0.34 / 0.37 |
| dV_upper | resolvable | Energy: notebook units vs Hs2 dt (HAT) | 91 | 8.47 | 8.47 | -0.00 [-0.00, +0.00] | 0.37 / 0.37 |
| dV_upper | resolvable | Energy: HAT-filtered vs all-storm (Hs2 dt) | 91 | 8.47 | 8.30 | +0.17 [-0.46, +1.01] | 0.37 / 0.40 |
| dV_upper | resolvable | Energy: HAT-filtered vs all-storm (flux) | 91 | 8.66 | 8.33 | +0.33 [-0.37, +1.27] | 0.34 / 0.39 |
| dV_upper | resolvable | ML: LightGBM with vs without antecedent features | 91 | 9.32 | 8.98 | +0.34 [-0.20, +0.91] | 0.24 / 0.29 |
| dV_upper | all | Antecedent state (past-only anomaly): continuous vs binary | 98 | 11.98 | 13.10 | -1.12 [-3.75, +1.24] | -0.26 / -0.51 |
| dV_upper | all | Antecedent state (vs training-mean volume): continuous vs binary | 98 | 10.86 | 12.15 | -1.29 [-3.19, +0.23] | -0.04 / -0.30 |
| dV_upper | all | Antecedent state (continuous, past-only) vs none | 98 | 11.98 | 11.29 | +0.69 [-0.18, +1.97] | -0.26 / -0.12 |
| dV_upper | all | Berm volume (continuous) vs none | 98 | 10.58 | 11.29 | -0.71 [-1.85, +0.35] | 0.01 / -0.12 |
| dV_upper | all | Cluster count: with vs without | 98 | 8.75 | 11.98 | -3.24 [-5.60, -1.15] | 0.33 / -0.26 |
| dV_upper | all | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 98 | 11.25 | 11.29 | -0.04 [-0.09, +0.00] | -0.11 / -0.12 |
| dV_upper | all | Energy: notebook units vs Hs2 dt (HAT) | 98 | 11.29 | 11.29 | +0.00 [+0.00, +0.00] | -0.12 / -0.12 |
| dV_upper | all | Energy: HAT-filtered vs all-storm (Hs2 dt) | 98 | 11.29 | 10.89 | +0.40 [-0.32, +1.23] | -0.12 / -0.04 |
| dV_upper | all | Energy: HAT-filtered vs all-storm (flux) | 98 | 11.25 | 10.84 | +0.41 [-0.30, +1.20] | -0.11 / -0.03 |
| dV_upper | all | ML: LightGBM with vs without antecedent features | 98 | 9.71 | 9.41 | +0.30 [-0.46, +1.12] | 0.17 / 0.22 |
| dV_total_fixed | resolvable | Antecedent state (past-only anomaly): continuous vs binary | 76 | 13.14 | 13.62 | -0.49 [-1.50, +0.26] | 0.49 / 0.45 |
| dV_total_fixed | resolvable | Antecedent state (vs training-mean volume): continuous vs binary | 76 | 12.80 | 12.98 | -0.18 [-1.18, +0.82] | 0.51 / 0.50 |
| dV_total_fixed | resolvable | Antecedent state (continuous, past-only) vs none | 76 | 13.14 | 14.27 | -1.13 [-3.35, +0.26] | 0.49 / 0.39 |
| dV_total_fixed | resolvable | Berm volume (continuous) vs none | 76 | 13.74 | 14.27 | -0.53 [-1.83, +0.54] | 0.44 / 0.39 |
| dV_total_fixed | resolvable | Cluster count: with vs without | 76 | 13.33 | 13.14 | +0.19 [-0.18, +0.63] | 0.47 / 0.49 |
| dV_total_fixed | resolvable | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 76 | 14.57 | 14.27 | +0.30 [-0.12, +0.87] | 0.37 / 0.39 |
| dV_total_fixed | resolvable | Energy: notebook units vs Hs2 dt (HAT) | 76 | 14.27 | 14.27 | +0.00 [-0.00, +0.00] | 0.39 / 0.39 |
| dV_total_fixed | resolvable | Energy: HAT-filtered vs all-storm (Hs2 dt) | 76 | 14.27 | 13.87 | +0.39 [-0.83, +2.14] | 0.39 / 0.43 |
| dV_total_fixed | resolvable | Energy: HAT-filtered vs all-storm (flux) | 76 | 14.57 | 13.86 | +0.70 [-0.68, +2.76] | 0.37 / 0.43 |
| dV_total_fixed | resolvable | ML: LightGBM with vs without antecedent features | 76 | 16.00 | 14.71 | +1.29 [-0.27, +3.10] | 0.24 / 0.36 |
| dV_total_fixed | all | Antecedent state (past-only anomaly): continuous vs binary | 81 | 18.54 | 18.73 | -0.19 [-1.40, +1.37] | -0.02 / -0.04 |
| dV_total_fixed | all | Antecedent state (vs training-mean volume): continuous vs binary | 81 | 18.35 | 20.35 | -2.00 [-5.11, +1.53] | 0.00 / -0.23 |
| dV_total_fixed | all | Antecedent state (continuous, past-only) vs none | 81 | 18.54 | 17.31 | +1.23 [-0.18, +2.73] | -0.02 / 0.11 |
| dV_total_fixed | all | Berm volume (continuous) vs none | 81 | 17.31 | 17.31 | +0.00 [-0.34, +0.38] | 0.11 / 0.11 |
| dV_total_fixed | all | Cluster count: with vs without | 81 | 14.81 | 18.54 | -3.73 [-7.42, -0.32] | 0.35 / -0.02 |
| dV_total_fixed | all | Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT) | 81 | 16.93 | 17.31 | -0.38 [-0.95, +0.08] | 0.15 / 0.11 |
| dV_total_fixed | all | Energy: notebook units vs Hs2 dt (HAT) | 81 | 17.31 | 17.31 | +0.00 [-0.00, +0.00] | 0.11 / 0.11 |
| dV_total_fixed | all | Energy: HAT-filtered vs all-storm (Hs2 dt) | 81 | 17.31 | 18.57 | -1.26 [-2.79, +0.01] | 0.11 / -0.02 |
| dV_total_fixed | all | Energy: HAT-filtered vs all-storm (flux) | 81 | 16.93 | 18.14 | -1.21 [-2.89, +0.13] | 0.15 / 0.03 |
| dV_total_fixed | all | ML: LightGBM with vs without antecedent features | 81 | 15.22 | 14.33 | +0.88 [+0.06, +1.72] | 0.31 / 0.39 |
<!-- /AUTO:abl_v2 -->
<!-- AUTO:ablt_v2 -->
| target | subset | n | sd(obs) | RMSE | R² [95 % CI] | skill vs clim [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | 91 | 10.6 | 8.5 | 0.36 [0.02, 0.57] | 0.37 [0.06, 0.58] |
| dV_upper | all | 98 | 10.6 | 11.3 | -0.15 [-0.90, 0.20] | -0.12 [-0.83, 0.22] |
| dV_total_fixed | resolvable | 76 | 18.3 | 14.3 | 0.38 [0.05, 0.58] | 0.39 [0.10, 0.59] |
| dV_total_fixed | all | 81 | 18.3 | 17.3 | 0.10 [-0.50, 0.41] | 0.11 [-0.44, 0.42] |
| dV_total | resolvable | 91 | 22.4 | 17.9 | 0.36 [0.11, 0.52] | 0.37 [0.14, 0.54] |
| dV_total | all | 98 | 22.6 | 23.5 | -0.10 [-0.86, 0.25] | -0.07 [-0.78, 0.27] |
| dV_lower_fixed | resolvable | 76 | 10.6 | 8.9 | 0.29 [0.08, 0.47] | 0.30 [0.11, 0.48] |
| dV_lower_fixed | all | 81 | 11.0 | 10.2 | 0.12 [-0.14, 0.31] | 0.13 [-0.10, 0.33] |
<!-- /AUTO:ablt_v2 -->

### v2 — wave direction and winter NAO (`run_all.direction_ablation`)
<!-- AUTO:abl_dir_v2 -->
| target | subset | question | n | RMSE variant | RMSE reference | ΔRMSE (variant − ref) [95 % CI] | skill vs clim (variant / ref) |
|---|---|---|---|---|---|---|---|
| dV_upper | resolvable | Direction (OLS): E + dir vs E | 91 | 8.43 | 8.47 | -0.04 [-0.24, +0.18] | 0.38 / 0.37 |
| dV_upper | resolvable | Direction (OLS): E + E*dir vs E | 91 | 9.01 | 8.47 | +0.54 [-0.28, +1.55] | 0.29 / 0.37 |
| dV_upper | resolvable | Direction: Equilibrium B + dir vs Equilibrium B | 91 | 7.77 | 7.87 | -0.10 [-0.32, +0.17] | 0.47 / 0.46 |
| dV_upper | resolvable | Direction (LightGBM): + mean_dir vs base | 91 | 9.11 | 9.32 | -0.21 [-0.72, +0.33] | 0.27 / 0.24 |
| dV_upper | resolvable | NAO (LightGBM): + nao_winter vs base | 91 | 8.91 | 9.32 | -0.40 [-0.84, -0.00] | 0.30 / 0.24 |
| dV_upper | resolvable | Direction + NAO (LightGBM) vs base | 91 | 8.84 | 9.32 | -0.48 [-0.99, -0.06] | 0.31 / 0.24 |
| dV_upper | all | Direction (OLS): E + dir vs E | 98 | 11.10 | 11.29 | -0.19 [-0.45, +0.12] | -0.08 / -0.12 |
| dV_upper | all | Direction (OLS): E + E*dir vs E | 98 | 11.05 | 11.29 | -0.24 [-1.02, +0.65] | -0.08 / -0.12 |
| dV_upper | all | Direction: Equilibrium B + dir vs Equilibrium B | 98 | 10.61 | 10.86 | -0.25 [-0.55, +0.10] | 0.01 / -0.04 |
| dV_upper | all | Direction (LightGBM): + mean_dir vs base | 98 | 9.55 | 9.71 | -0.17 [-0.52, +0.22] | 0.20 / 0.17 |
| dV_upper | all | NAO (LightGBM): + nao_winter vs base | 98 | 9.56 | 9.71 | -0.15 [-0.48, +0.20] | 0.19 / 0.17 |
| dV_upper | all | Direction + NAO (LightGBM) vs base | 98 | 9.49 | 9.71 | -0.22 [-0.57, +0.17] | 0.21 / 0.17 |
| dV_total_fixed | resolvable | Direction (OLS): E + dir vs E | 76 | 14.30 | 14.27 | +0.03 [-0.15, +0.23] | 0.39 / 0.39 |
| dV_total_fixed | resolvable | Direction (OLS): E + E*dir vs E | 76 | 15.23 | 14.27 | +0.96 [-0.29, +2.69] | 0.31 / 0.39 |
| dV_total_fixed | resolvable | Direction: Equilibrium B + dir vs Equilibrium B | 76 | 12.78 | 12.80 | -0.02 [-0.23, +0.22] | 0.51 / 0.51 |
| dV_total_fixed | resolvable | Direction (LightGBM): + mean_dir vs base | 76 | 15.68 | 16.00 | -0.32 [-1.22, +0.56] | 0.27 / 0.24 |
| dV_total_fixed | resolvable | NAO (LightGBM): + nao_winter vs base | 76 | 14.79 | 16.00 | -1.21 [-2.00, -0.44] | 0.35 / 0.24 |
| dV_total_fixed | resolvable | Direction + NAO (LightGBM) vs base | 76 | 14.60 | 16.00 | -1.40 [-2.41, -0.39] | 0.36 / 0.24 |
| dV_total_fixed | all | Direction (OLS): E + dir vs E | 81 | 17.23 | 17.31 | -0.08 [-0.29, +0.20] | 0.12 / 0.11 |
| dV_total_fixed | all | Direction (OLS): E + E*dir vs E | 81 | 17.57 | 17.31 | +0.26 [-0.17, +1.01] | 0.09 / 0.11 |
| dV_total_fixed | all | Direction: Equilibrium B + dir vs Equilibrium B | 81 | 18.24 | 18.35 | -0.11 [-0.33, +0.19] | 0.02 / 0.00 |
| dV_total_fixed | all | Direction (LightGBM): + mean_dir vs base | 81 | 14.80 | 15.22 | -0.41 [-1.26, +0.40] | 0.35 / 0.31 |
| dV_total_fixed | all | NAO (LightGBM): + nao_winter vs base | 81 | 14.17 | 15.22 | -1.05 [-1.70, -0.37] | 0.41 / 0.31 |
| dV_total_fixed | all | Direction + NAO (LightGBM) vs base | 81 | 14.11 | 15.22 | -1.10 [-1.95, -0.26] | 0.41 / 0.31 |
<!-- /AUTO:abl_dir_v2 -->

### HAT sensitivity (HAT = +2.14 m vs superseded +1.75 m MSL tables; LOWO, resolvable)
<!-- AUTO:hat -->
| data | target | model | n | RMSE HAT 2.14 | RMSE HAT 1.75 | skill vs clim HAT 2.14 [CI] | skill vs clim HAT 1.75 [CI] |
|---|---|---|---|---|---|---|---|
| v1 | dV_upper | evi_general | 48 | 9.00 | 10.92 | 0.46 [0.24, 0.62] | 0.43 [0.18, 0.61] |
| v1 | dV_upper | ppt_2stage | 48 | 9.44 | 11.72 | 0.40 [0.15, 0.60] | 0.34 [0.07, 0.54] |
| v1 | dV_upper | harley | 48 | 8.76 | 10.39 | 0.48 [0.26, 0.63] | 0.48 [0.25, 0.65] |
| v1 | dV_upper | eq_b | 48 | 9.07 | 10.58 | 0.45 [0.25, 0.60] | 0.46 [0.27, 0.63] |
| v1 | dV_upper | rf | 48 | 9.33 | 10.44 | 0.41 [0.18, 0.56] | 0.48 [0.28, 0.61] |
| v1 | dV_total_fixed | evi_general | 48 | 14.71 | 14.91 | 0.57 [0.35, 0.72] | 0.56 [0.32, 0.71] |
| v1 | dV_total_fixed | ppt_2stage | 48 | 15.37 | 15.47 | 0.53 [0.26, 0.70] | 0.53 [0.23, 0.70] |
| v1 | dV_total_fixed | harley | 48 | 13.71 | 13.71 | 0.63 [0.41, 0.76] | 0.63 [0.41, 0.76] |
| v1 | dV_total_fixed | eq_b | 48 | 14.14 | 13.87 | 0.61 [0.43, 0.72] | 0.62 [0.42, 0.75] |
| v1 | dV_total_fixed | rf | 48 | 15.68 | 15.14 | 0.51 [0.28, 0.65] | 0.55 [0.31, 0.68] |
| v2 | dV_upper | evi_general | 91 | 8.47 | 10.07 | 0.37 [0.06, 0.58] | 0.37 [0.08, 0.57] |
| v2 | dV_upper | ppt_2stage | 91 | 9.13 | 10.86 | 0.27 [-0.07, 0.48] | 0.27 [-0.07, 0.47] |
| v2 | dV_upper | harley | 91 | 8.30 | 9.95 | 0.40 [0.17, 0.56] | 0.39 [0.16, 0.56] |
| v2 | dV_upper | eq_b | 91 | 7.87 | 9.30 | 0.46 [0.27, 0.63] | 0.46 [0.26, 0.62] |
| v2 | dV_upper | rf | 91 | 8.67 | 10.54 | 0.34 [0.13, 0.50] | 0.31 [0.09, 0.48] |
| v2 | dV_total_fixed | evi_general | 76 | 14.27 | 14.01 | 0.39 [0.10, 0.59] | 0.42 [0.15, 0.60] |
| v2 | dV_total_fixed | ppt_2stage | 76 | 14.68 | 14.51 | 0.36 [0.03, 0.56] | 0.37 [0.06, 0.57] |
| v2 | dV_total_fixed | harley | 76 | 13.87 | 13.87 | 0.43 [0.21, 0.58] | 0.43 [0.21, 0.58] |
| v2 | dV_total_fixed | eq_b | 76 | 12.80 | 12.67 | 0.51 [0.33, 0.65] | 0.52 [0.32, 0.67] |
| v2 | dV_total_fixed | rf | 76 | 14.71 | 14.67 | 0.36 [0.14, 0.51] | 0.36 [0.14, 0.51] |
<!-- /AUTO:hat -->

**Verdicts (one line each; "no detectable effect" = the paired 95 % CI of ΔRMSE includes 0):**
* *Continuous vs binary antecedent state:* no detectable effect on `dV_upper` (v1 ΔRMSE +0.02 [−0.41, +0.43]; v2
  −0.30 [−1.19, +0.41]). Small gain on `dV_total_fixed` in v1 (−0.66 [−1.27, −0.07], past-only anomaly), not
  significant in v2 (−0.49 [−1.50, +0.26]).
* *Antecedent state vs none:* no detectable effect (v1 `dV_upper` +0.15 [−0.71, +0.91]; v2 −0.55 [−1.69, +0.24]).
  The berm proxy helps neither consistently (v1 `dV_upper` −0.44 [−1.73, +0.70]; v2 `dV_upper` +3.18 [−0.60, +8.80]).
* *Storm-cluster count:* adds nothing, and in v1 slightly hurts `dV_upper` (+0.45 [+0.01, +0.96]); v2 +0.08
  [−0.05, +0.22]. SHAP agrees: `n_clusters` has the lowest mean |SHAP| in both versions.
* *Energy flux vs Hs²Δt:* flux is not better; slightly worse in v1 `dV_upper` (+0.23 [+0.02, +0.43]).
* *Notebook units vs Hs²Δt:* identical (ΔRMSE 0.00): they are constant multiples, so the 2017 unit error changes
  slopes, not skill.
* *HAT-filtered vs all-storm energy:* HAT filtering never helps; all-storm energy is better for `dV_total_fixed` in
  v1 (Hs²Δt: +1.00 [+0.02, +1.92]; flux +1.18 [+0.26, +1.98]) and no different elsewhere. This is expected because
  TWL ≥ HAT is reached in a large share of time steps even at HAT = +2.14 m (Agent A: 27 % v1 / 21 % v2), so
  "stormHAT" energy ≈ "storm" energy for almost every event (v1: 50/51 events have HAT-exceeding energy).
* *Wave direction (v2):* no detectable effect in the linear/equilibrium models (`dV_upper` resolvable: E + dir
  −0.04 [−0.24, +0.18]; Equilibrium B + dir −0.10 [−0.32, +0.17]); a non-significant gain in LightGBM (−0.21
  [−0.72, +0.33]).
* *Winter NAO (v2, concurrent DJFM index):* the only added variable with a detectable gain, and only inside
  LightGBM (`dV_upper` −0.40 [−0.84, −0.00]; `dV_total_fixed` −1.21 [−2.00, −0.44]); even then LightGBM + NAO
  (skill 0.30 / 0.35) stays below Equilibrium B (0.46 / 0.51). NAO is not known in advance, so this is a
  seasonal-context signal, not a forecast gain.
* *ML with vs without antecedent features:* no detectable gain (v1 `dV_upper` −0.13 [−1.20, +0.95]; v2 +0.34
  [−0.20, +0.91]); without them LightGBM is even marginally better on `dV_total_fixed`.
* *Upper vs total ΔV:* in v1 the whole-profile fixed-window target is more predictable from energy (skill 0.57
  [0.35, 0.72]) than the upper beach (0.46 [0.24, 0.62]); in v2 they are similar (0.39 vs 0.37). The pairwise-window
  `dV_total` is worse than the fixed window in v1 (0.38 [−0.02, 0.57]), as HANDOFF §2.1 item 6 warned.
* *HAT value (2.14 vs 1.75 m):* skill vs climatology barely moves (v1 EVI General `dV_upper` 0.46 vs 0.43; v2 0.37 vs
  0.37). RMSEs differ mostly because `dV_upper` itself is redefined by the HAT plane. (The RF row of this table uses
  the 11 base features for both versions, so its v2 numbers differ slightly from §4.)

## 6. Prediction intervals and coverage

v1:
<!-- AUTO:cov_v1 -->
| target | subset | split | model | n | nominal | empirical coverage | mean width (m³/m) |
|---|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | gp | 48 | 0.80 | 0.58 | 21.9 |
| dV_upper | resolvable | lowo | gp | 48 | 0.90 | 0.73 | 28.1 |
| dV_upper | resolvable | lowo | evi_general | 48 | 0.80 | 0.79 | 23.5 |
| dV_upper | resolvable | lowo | evi_general | 48 | 0.90 | 0.92 | 33.9 |
| dV_upper | resolvable | lowo | ppt_all | 48 | 0.80 | 0.81 | 24.0 |
| dV_upper | resolvable | lowo | ppt_all | 48 | 0.90 | 0.92 | 34.9 |
| dV_upper | resolvable | lowo | eq_b | 48 | 0.80 | 0.77 | 22.2 |
| dV_upper | resolvable | lowo | eq_b | 48 | 0.90 | 0.92 | 35.3 |
| dV_upper | resolvable | lowo | lgbm | 48 | 0.80 | 0.88 | 33.4 |
| dV_upper | resolvable | lowo | lgbm | 48 | 0.90 | 0.92 | 39.8 |
| dV_upper | resolvable | lowo | two_stage_ml | 48 | 0.80 | 0.81 | 23.5 |
| dV_upper | resolvable | lowo | two_stage_ml | 48 | 0.90 | 0.92 | 35.1 |
| dV_upper | resolvable | lowo | hybrid | 48 | 0.80 | 0.83 | 28.0 |
| dV_upper | resolvable | lowo | hybrid | 48 | 0.90 | 0.92 | 36.4 |
| dV_upper | resolvable | holdout_2013-14 | gp | 12 | 0.80 | 0.58 | 21.3 |
| dV_upper | resolvable | holdout_2013-14 | gp | 12 | 0.90 | 0.58 | 27.4 |
| dV_upper | resolvable | holdout_2013-14 | evi_general | 12 | 0.80 | 0.83 | 24.3 |
| dV_upper | resolvable | holdout_2013-14 | evi_general | 12 | 0.90 | 1.00 | 38.0 |
| dV_upper | resolvable | holdout_2013-14 | ppt_all | 12 | 0.80 | 0.92 | 27.1 |
| dV_upper | resolvable | holdout_2013-14 | ppt_all | 12 | 0.90 | 1.00 | 35.1 |
| dV_upper | resolvable | holdout_2013-14 | eq_b | 12 | 0.80 | 0.92 | 23.5 |
| dV_upper | resolvable | holdout_2013-14 | eq_b | 12 | 0.90 | 0.92 | 39.4 |
| dV_upper | resolvable | holdout_2013-14 | lgbm | 12 | 0.80 | 1.00 | 36.9 |
| dV_upper | resolvable | holdout_2013-14 | lgbm | 12 | 0.90 | 1.00 | 42.4 |
| dV_upper | resolvable | holdout_2013-14 | two_stage_ml | 12 | 0.80 | 0.83 | 23.5 |
| dV_upper | resolvable | holdout_2013-14 | two_stage_ml | 12 | 0.90 | 0.92 | 37.4 |
| dV_upper | resolvable | holdout_2013-14 | hybrid | 12 | 0.80 | 0.92 | 29.5 |
| dV_upper | resolvable | holdout_2013-14 | hybrid | 12 | 0.90 | 0.92 | 42.1 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.80 | 0.64 | 20.3 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.90 | 0.64 | 26.0 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.80 | 0.86 | 24.3 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.90 | 1.00 | 38.0 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.80 | 0.93 | 27.1 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.90 | 1.00 | 35.1 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.80 | 0.93 | 23.5 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.90 | 0.93 | 39.4 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.80 | 1.00 | 36.9 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.90 | 1.00 | 42.4 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.80 | 0.86 | 23.5 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.90 | 0.93 | 37.4 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.80 | 0.93 | 29.5 |
| dV_upper | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.90 | 0.93 | 42.1 |
| dV_upper | all | lowo | gp | 51 | 0.80 | 0.59 | 23.4 |
| dV_upper | all | lowo | gp | 51 | 0.90 | 0.71 | 30.0 |
| dV_upper | all | lowo | evi_general | 51 | 0.80 | 0.80 | 34.2 |
| dV_upper | all | lowo | evi_general | 51 | 0.90 | 0.90 | 44.0 |
| dV_upper | all | lowo | ppt_all | 51 | 0.80 | 0.84 | 27.4 |
| dV_upper | all | lowo | ppt_all | 51 | 0.90 | 0.92 | 45.3 |
| dV_upper | all | lowo | eq_b | 51 | 0.80 | 0.80 | 27.6 |
| dV_upper | all | lowo | eq_b | 51 | 0.90 | 0.90 | 48.1 |
| dV_upper | all | lowo | lgbm | 51 | 0.80 | 0.82 | 30.9 |
| dV_upper | all | lowo | lgbm | 51 | 0.90 | 0.90 | 42.5 |
| dV_upper | all | lowo | two_stage_ml | 51 | 0.80 | 0.80 | 37.1 |
| dV_upper | all | lowo | two_stage_ml | 51 | 0.90 | 0.92 | 53.5 |
| dV_upper | all | lowo | hybrid | 51 | 0.80 | 0.82 | 31.1 |
| dV_upper | all | lowo | hybrid | 51 | 0.90 | 0.90 | 48.2 |
| dV_upper | all | holdout_2013-14 | gp | 12 | 0.80 | 0.50 | 21.5 |
| dV_upper | all | holdout_2013-14 | gp | 12 | 0.90 | 0.58 | 27.6 |
| dV_upper | all | holdout_2013-14 | evi_general | 12 | 0.80 | 0.83 | 35.6 |
| dV_upper | all | holdout_2013-14 | evi_general | 12 | 0.90 | 1.00 | 55.3 |
| dV_upper | all | holdout_2013-14 | ppt_all | 12 | 0.80 | 0.83 | 28.7 |
| dV_upper | all | holdout_2013-14 | ppt_all | 12 | 0.90 | 1.00 | 62.4 |
| dV_upper | all | holdout_2013-14 | eq_b | 12 | 0.80 | 0.83 | 27.4 |
| dV_upper | all | holdout_2013-14 | eq_b | 12 | 0.90 | 0.92 | 56.5 |
| dV_upper | all | holdout_2013-14 | lgbm | 12 | 0.80 | 1.00 | 41.6 |
| dV_upper | all | holdout_2013-14 | lgbm | 12 | 0.90 | 1.00 | 45.8 |
| dV_upper | all | holdout_2013-14 | two_stage_ml | 12 | 0.80 | 0.75 | 38.6 |
| dV_upper | all | holdout_2013-14 | two_stage_ml | 12 | 0.90 | 0.92 | 55.4 |
| dV_upper | all | holdout_2013-14 | hybrid | 12 | 0.80 | 0.83 | 32.1 |
| dV_upper | all | holdout_2013-14 | hybrid | 12 | 0.90 | 0.92 | 52.6 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.80 | 0.57 | 20.4 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.90 | 0.64 | 26.2 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.80 | 0.86 | 35.6 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.90 | 1.00 | 55.3 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.80 | 0.86 | 28.7 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.90 | 1.00 | 62.4 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.80 | 0.86 | 27.4 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.90 | 0.93 | 56.5 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.80 | 1.00 | 41.6 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.90 | 1.00 | 45.8 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.80 | 0.79 | 38.6 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.90 | 0.93 | 55.4 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.80 | 0.86 | 32.1 |
| dV_upper | all | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.90 | 0.93 | 52.6 |
| dV_total_fixed | resolvable | lowo | gp | 48 | 0.80 | 0.67 | 36.4 |
| dV_total_fixed | resolvable | lowo | gp | 48 | 0.90 | 0.79 | 46.7 |
| dV_total_fixed | resolvable | lowo | evi_general | 48 | 0.80 | 0.83 | 42.3 |
| dV_total_fixed | resolvable | lowo | evi_general | 48 | 0.90 | 0.96 | 54.3 |
| dV_total_fixed | resolvable | lowo | ppt_all | 48 | 0.80 | 0.75 | 39.5 |
| dV_total_fixed | resolvable | lowo | ppt_all | 48 | 0.90 | 0.94 | 57.7 |
| dV_total_fixed | resolvable | lowo | eq_b | 48 | 0.80 | 0.79 | 40.3 |
| dV_total_fixed | resolvable | lowo | eq_b | 48 | 0.90 | 0.94 | 55.6 |
| dV_total_fixed | resolvable | lowo | lgbm | 48 | 0.80 | 0.81 | 52.2 |
| dV_total_fixed | resolvable | lowo | lgbm | 48 | 0.90 | 0.85 | 73.6 |
| dV_total_fixed | resolvable | lowo | two_stage_ml | 48 | 0.80 | 0.85 | 40.6 |
| dV_total_fixed | resolvable | lowo | two_stage_ml | 48 | 0.90 | 0.92 | 54.1 |
| dV_total_fixed | resolvable | lowo | hybrid | 48 | 0.80 | 0.81 | 42.3 |
| dV_total_fixed | resolvable | lowo | hybrid | 48 | 0.90 | 0.92 | 61.6 |
| dV_total_fixed | resolvable | holdout_2013-14 | gp | 12 | 0.80 | 0.67 | 32.9 |
| dV_total_fixed | resolvable | holdout_2013-14 | gp | 12 | 0.90 | 0.83 | 42.2 |
| dV_total_fixed | resolvable | holdout_2013-14 | evi_general | 12 | 0.80 | 0.92 | 44.5 |
| dV_total_fixed | resolvable | holdout_2013-14 | evi_general | 12 | 0.90 | 1.00 | 58.8 |
| dV_total_fixed | resolvable | holdout_2013-14 | ppt_all | 12 | 0.80 | 0.83 | 37.9 |
| dV_total_fixed | resolvable | holdout_2013-14 | ppt_all | 12 | 0.90 | 1.00 | 64.4 |
| dV_total_fixed | resolvable | holdout_2013-14 | eq_b | 12 | 0.80 | 0.83 | 39.3 |
| dV_total_fixed | resolvable | holdout_2013-14 | eq_b | 12 | 0.90 | 1.00 | 72.1 |
| dV_total_fixed | resolvable | holdout_2013-14 | lgbm | 12 | 0.80 | 1.00 | 64.5 |
| dV_total_fixed | resolvable | holdout_2013-14 | lgbm | 12 | 0.90 | 1.00 | 99.5 |
| dV_total_fixed | resolvable | holdout_2013-14 | two_stage_ml | 12 | 0.80 | 1.00 | 45.9 |
| dV_total_fixed | resolvable | holdout_2013-14 | two_stage_ml | 12 | 0.90 | 1.00 | 57.5 |
| dV_total_fixed | resolvable | holdout_2013-14 | hybrid | 12 | 0.80 | 1.00 | 53.1 |
| dV_total_fixed | resolvable | holdout_2013-14 | hybrid | 12 | 0.90 | 1.00 | 71.8 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.80 | 0.64 | 32.6 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.90 | 0.86 | 41.9 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.80 | 0.93 | 44.5 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.90 | 1.00 | 58.8 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.80 | 0.86 | 37.9 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.90 | 1.00 | 64.4 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.80 | 0.86 | 39.3 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.90 | 1.00 | 72.1 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.80 | 1.00 | 64.5 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.90 | 1.00 | 99.5 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.80 | 1.00 | 45.9 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.90 | 1.00 | 57.5 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.80 | 1.00 | 53.1 |
| dV_total_fixed | resolvable | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.90 | 1.00 | 71.8 |
| dV_total_fixed | all | lowo | gp | 51 | 0.80 | 0.75 | 39.5 |
| dV_total_fixed | all | lowo | gp | 51 | 0.90 | 0.86 | 50.8 |
| dV_total_fixed | all | lowo | evi_general | 51 | 0.80 | 0.80 | 50.1 |
| dV_total_fixed | all | lowo | evi_general | 51 | 0.90 | 0.92 | 81.8 |
| dV_total_fixed | all | lowo | ppt_all | 51 | 0.80 | 0.78 | 46.6 |
| dV_total_fixed | all | lowo | ppt_all | 51 | 0.90 | 0.90 | 69.9 |
| dV_total_fixed | all | lowo | eq_b | 51 | 0.80 | 0.82 | 55.3 |
| dV_total_fixed | all | lowo | eq_b | 51 | 0.90 | 0.92 | 77.0 |
| dV_total_fixed | all | lowo | lgbm | 51 | 0.80 | 0.80 | 54.1 |
| dV_total_fixed | all | lowo | lgbm | 51 | 0.90 | 0.90 | 85.2 |
| dV_total_fixed | all | lowo | two_stage_ml | 51 | 0.80 | 0.84 | 64.2 |
| dV_total_fixed | all | lowo | two_stage_ml | 51 | 0.90 | 0.94 | 103.8 |
| dV_total_fixed | all | lowo | hybrid | 51 | 0.80 | 0.80 | 54.3 |
| dV_total_fixed | all | lowo | hybrid | 51 | 0.90 | 0.92 | 80.8 |
| dV_total_fixed | all | holdout_2013-14 | gp | 12 | 0.80 | 0.75 | 32.4 |
| dV_total_fixed | all | holdout_2013-14 | gp | 12 | 0.90 | 0.83 | 41.6 |
| dV_total_fixed | all | holdout_2013-14 | evi_general | 12 | 0.80 | 0.92 | 55.7 |
| dV_total_fixed | all | holdout_2013-14 | evi_general | 12 | 0.90 | 1.00 | 106.6 |
| dV_total_fixed | all | holdout_2013-14 | ppt_all | 12 | 0.80 | 0.83 | 47.9 |
| dV_total_fixed | all | holdout_2013-14 | ppt_all | 12 | 0.90 | 1.00 | 87.8 |
| dV_total_fixed | all | holdout_2013-14 | eq_b | 12 | 0.80 | 0.75 | 49.1 |
| dV_total_fixed | all | holdout_2013-14 | eq_b | 12 | 0.90 | 1.00 | 82.7 |
| dV_total_fixed | all | holdout_2013-14 | lgbm | 12 | 0.80 | 1.00 | 69.0 |
| dV_total_fixed | all | holdout_2013-14 | lgbm | 12 | 0.90 | 1.00 | 96.8 |
| dV_total_fixed | all | holdout_2013-14 | two_stage_ml | 12 | 0.80 | 0.83 | 68.6 |
| dV_total_fixed | all | holdout_2013-14 | two_stage_ml | 12 | 0.90 | 1.00 | 126.8 |
| dV_total_fixed | all | holdout_2013-14 | hybrid | 12 | 0.80 | 0.75 | 54.5 |
| dV_total_fixed | all | holdout_2013-14 | hybrid | 12 | 0.90 | 1.00 | 93.2 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.80 | 0.71 | 32.1 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | gp | 14 | 0.90 | 0.79 | 41.2 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.80 | 0.93 | 55.7 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | evi_general | 14 | 0.90 | 1.00 | 106.6 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.80 | 0.86 | 47.9 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | ppt_all | 14 | 0.90 | 1.00 | 87.8 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.80 | 0.79 | 49.1 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | eq_b | 14 | 0.90 | 1.00 | 82.7 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.80 | 1.00 | 69.0 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | lgbm | 14 | 0.90 | 1.00 | 96.8 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.80 | 0.86 | 68.6 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | two_stage_ml | 14 | 0.90 | 1.00 | 126.8 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.80 | 0.79 | 54.5 |
| dV_total_fixed | all | holdout_2013-14..2014-15(train<= 2012-13) | hybrid | 14 | 0.90 | 1.00 | 93.2 |
<!-- /AUTO:cov_v1 -->
v2:
<!-- AUTO:cov_v2 -->
| target | subset | split | model | n | nominal | empirical coverage | mean width (m³/m) |
|---|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | gp | 91 | 0.80 | 0.74 | 17.8 |
| dV_upper | resolvable | lowo | gp | 91 | 0.90 | 0.86 | 22.9 |
| dV_upper | resolvable | lowo | evi_general | 91 | 0.80 | 0.80 | 17.9 |
| dV_upper | resolvable | lowo | evi_general | 91 | 0.90 | 0.89 | 29.3 |
| dV_upper | resolvable | lowo | ppt_all | 91 | 0.80 | 0.81 | 17.0 |
| dV_upper | resolvable | lowo | ppt_all | 91 | 0.90 | 0.89 | 29.0 |
| dV_upper | resolvable | lowo | eq_b | 91 | 0.80 | 0.80 | 17.4 |
| dV_upper | resolvable | lowo | eq_b | 91 | 0.90 | 0.89 | 28.8 |
| dV_upper | resolvable | lowo | lgbm | 91 | 0.80 | 0.77 | 21.2 |
| dV_upper | resolvable | lowo | lgbm | 91 | 0.90 | 0.93 | 32.2 |
| dV_upper | resolvable | lowo | two_stage_ml | 91 | 0.80 | 0.77 | 18.8 |
| dV_upper | resolvable | lowo | two_stage_ml | 91 | 0.90 | 0.90 | 31.3 |
| dV_upper | resolvable | lowo | hybrid | 91 | 0.80 | 0.79 | 19.4 |
| dV_upper | resolvable | lowo | hybrid | 91 | 0.90 | 0.89 | 30.1 |
| dV_upper | resolvable | holdout_2013-14 | gp | 12 | 0.80 | 0.83 | 21.1 |
| dV_upper | resolvable | holdout_2013-14 | gp | 12 | 0.90 | 0.92 | 27.0 |
| dV_upper | resolvable | holdout_2013-14 | evi_general | 12 | 0.80 | 0.75 | 20.2 |
| dV_upper | resolvable | holdout_2013-14 | evi_general | 12 | 0.90 | 0.83 | 32.5 |
| dV_upper | resolvable | holdout_2013-14 | ppt_all | 12 | 0.80 | 0.75 | 18.0 |
| dV_upper | resolvable | holdout_2013-14 | ppt_all | 12 | 0.90 | 0.92 | 39.1 |
| dV_upper | resolvable | holdout_2013-14 | eq_b | 12 | 0.80 | 0.75 | 16.6 |
| dV_upper | resolvable | holdout_2013-14 | eq_b | 12 | 0.90 | 0.83 | 32.2 |
| dV_upper | resolvable | holdout_2013-14 | lgbm | 12 | 0.80 | 0.92 | 30.2 |
| dV_upper | resolvable | holdout_2013-14 | lgbm | 12 | 0.90 | 1.00 | 47.5 |
| dV_upper | resolvable | holdout_2013-14 | two_stage_ml | 12 | 0.80 | 0.75 | 19.6 |
| dV_upper | resolvable | holdout_2013-14 | two_stage_ml | 12 | 0.90 | 0.83 | 31.8 |
| dV_upper | resolvable | holdout_2013-14 | hybrid | 12 | 0.80 | 0.83 | 21.1 |
| dV_upper | resolvable | holdout_2013-14 | hybrid | 12 | 0.90 | 0.83 | 31.9 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | gp | 38 | 0.80 | 0.82 | 21.2 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | gp | 38 | 0.90 | 0.95 | 27.2 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 38 | 0.80 | 0.89 | 20.9 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 38 | 0.90 | 0.97 | 40.9 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 38 | 0.80 | 0.95 | 23.0 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 38 | 0.90 | 0.97 | 39.9 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 38 | 0.80 | 0.95 | 23.9 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 38 | 0.90 | 0.97 | 42.2 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 38 | 0.80 | 0.87 | 28.2 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 38 | 0.90 | 0.95 | 33.4 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 38 | 0.80 | 0.89 | 25.5 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 38 | 0.90 | 0.97 | 37.3 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 38 | 0.80 | 0.95 | 24.9 |
| dV_upper | resolvable | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 38 | 0.90 | 0.97 | 38.4 |
| dV_upper | all | lowo | gp | 98 | 0.80 | 0.81 | 18.9 |
| dV_upper | all | lowo | gp | 98 | 0.90 | 0.86 | 24.2 |
| dV_upper | all | lowo | evi_general | 98 | 0.80 | 0.82 | 21.1 |
| dV_upper | all | lowo | evi_general | 98 | 0.90 | 0.92 | 40.8 |
| dV_upper | all | lowo | ppt_all | 98 | 0.80 | 0.81 | 21.3 |
| dV_upper | all | lowo | ppt_all | 98 | 0.90 | 0.92 | 39.3 |
| dV_upper | all | lowo | eq_b | 98 | 0.80 | 0.82 | 20.7 |
| dV_upper | all | lowo | eq_b | 98 | 0.90 | 0.90 | 38.7 |
| dV_upper | all | lowo | lgbm | 98 | 0.80 | 0.80 | 23.5 |
| dV_upper | all | lowo | lgbm | 98 | 0.90 | 0.91 | 35.7 |
| dV_upper | all | lowo | two_stage_ml | 98 | 0.80 | 0.81 | 22.1 |
| dV_upper | all | lowo | two_stage_ml | 98 | 0.90 | 0.90 | 42.9 |
| dV_upper | all | lowo | hybrid | 98 | 0.80 | 0.82 | 22.7 |
| dV_upper | all | lowo | hybrid | 98 | 0.90 | 0.91 | 35.4 |
| dV_upper | all | holdout_2013-14 | gp | 12 | 0.80 | 0.83 | 21.5 |
| dV_upper | all | holdout_2013-14 | gp | 12 | 0.90 | 0.92 | 27.6 |
| dV_upper | all | holdout_2013-14 | evi_general | 12 | 0.80 | 0.83 | 29.6 |
| dV_upper | all | holdout_2013-14 | evi_general | 12 | 0.90 | 0.92 | 53.1 |
| dV_upper | all | holdout_2013-14 | ppt_all | 12 | 0.80 | 0.83 | 22.3 |
| dV_upper | all | holdout_2013-14 | ppt_all | 12 | 0.90 | 1.00 | 46.7 |
| dV_upper | all | holdout_2013-14 | eq_b | 12 | 0.80 | 0.58 | 23.8 |
| dV_upper | all | holdout_2013-14 | eq_b | 12 | 0.90 | 1.00 | 54.8 |
| dV_upper | all | holdout_2013-14 | lgbm | 12 | 0.80 | 0.92 | 32.6 |
| dV_upper | all | holdout_2013-14 | lgbm | 12 | 0.90 | 0.92 | 44.3 |
| dV_upper | all | holdout_2013-14 | two_stage_ml | 12 | 0.80 | 0.83 | 32.9 |
| dV_upper | all | holdout_2013-14 | two_stage_ml | 12 | 0.90 | 0.92 | 48.2 |
| dV_upper | all | holdout_2013-14 | hybrid | 12 | 0.80 | 0.58 | 31.3 |
| dV_upper | all | holdout_2013-14 | hybrid | 12 | 0.90 | 1.00 | 54.8 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | gp | 41 | 0.80 | 0.88 | 22.5 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | gp | 41 | 0.90 | 0.95 | 28.9 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 41 | 0.80 | 0.95 | 28.1 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 41 | 0.90 | 1.00 | 50.5 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 41 | 0.80 | 0.90 | 21.4 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 41 | 0.90 | 0.95 | 40.7 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 41 | 0.80 | 0.95 | 26.7 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 41 | 0.90 | 0.98 | 45.8 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 41 | 0.80 | 0.98 | 28.8 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 41 | 0.90 | 0.98 | 44.5 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 41 | 0.80 | 0.90 | 29.1 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 41 | 0.90 | 0.98 | 48.8 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 41 | 0.80 | 0.95 | 29.1 |
| dV_upper | all | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 41 | 0.90 | 0.95 | 37.7 |
| dV_total_fixed | resolvable | lowo | gp | 76 | 0.80 | 0.79 | 31.2 |
| dV_total_fixed | resolvable | lowo | gp | 76 | 0.90 | 0.88 | 40.1 |
| dV_total_fixed | resolvable | lowo | evi_general | 76 | 0.80 | 0.82 | 30.3 |
| dV_total_fixed | resolvable | lowo | evi_general | 76 | 0.90 | 0.91 | 55.9 |
| dV_total_fixed | resolvable | lowo | ppt_all | 76 | 0.80 | 0.82 | 29.3 |
| dV_total_fixed | resolvable | lowo | ppt_all | 76 | 0.90 | 0.91 | 48.6 |
| dV_total_fixed | resolvable | lowo | eq_b | 76 | 0.80 | 0.82 | 26.8 |
| dV_total_fixed | resolvable | lowo | eq_b | 76 | 0.90 | 0.91 | 49.2 |
| dV_total_fixed | resolvable | lowo | lgbm | 76 | 0.80 | 0.82 | 34.8 |
| dV_total_fixed | resolvable | lowo | lgbm | 76 | 0.90 | 0.92 | 58.9 |
| dV_total_fixed | resolvable | lowo | two_stage_ml | 76 | 0.80 | 0.80 | 34.1 |
| dV_total_fixed | resolvable | lowo | two_stage_ml | 76 | 0.90 | 0.89 | 56.4 |
| dV_total_fixed | resolvable | lowo | hybrid | 76 | 0.80 | 0.82 | 29.6 |
| dV_total_fixed | resolvable | lowo | hybrid | 76 | 0.90 | 0.91 | 49.1 |
| dV_total_fixed | resolvable | holdout_2013-14 | gp | 8 | 0.80 | 0.75 | 28.3 |
| dV_total_fixed | resolvable | holdout_2013-14 | gp | 8 | 0.90 | 0.88 | 36.3 |
| dV_total_fixed | resolvable | holdout_2013-14 | evi_general | 8 | 0.80 | 0.88 | 44.2 |
| dV_total_fixed | resolvable | holdout_2013-14 | evi_general | 8 | 0.90 | 0.88 | 66.6 |
| dV_total_fixed | resolvable | holdout_2013-14 | ppt_all | 8 | 0.80 | 0.88 | 37.1 |
| dV_total_fixed | resolvable | holdout_2013-14 | ppt_all | 8 | 0.90 | 1.00 | 80.8 |
| dV_total_fixed | resolvable | holdout_2013-14 | eq_b | 8 | 0.80 | 0.88 | 35.1 |
| dV_total_fixed | resolvable | holdout_2013-14 | eq_b | 8 | 0.90 | 1.00 | 63.3 |
| dV_total_fixed | resolvable | holdout_2013-14 | lgbm | 8 | 0.80 | 0.88 | 52.0 |
| dV_total_fixed | resolvable | holdout_2013-14 | lgbm | 8 | 0.90 | 0.88 | 84.2 |
| dV_total_fixed | resolvable | holdout_2013-14 | two_stage_ml | 8 | 0.80 | 0.88 | 46.6 |
| dV_total_fixed | resolvable | holdout_2013-14 | two_stage_ml | 8 | 0.90 | 0.88 | 65.0 |
| dV_total_fixed | resolvable | holdout_2013-14 | hybrid | 8 | 0.80 | 0.88 | 38.1 |
| dV_total_fixed | resolvable | holdout_2013-14 | hybrid | 8 | 0.90 | 1.00 | 55.0 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | gp | 36 | 0.80 | 0.81 | 28.8 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | gp | 36 | 0.90 | 0.86 | 36.9 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 36 | 0.80 | 0.81 | 30.0 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 36 | 0.90 | 1.00 | 71.3 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 36 | 0.80 | 0.78 | 25.7 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 36 | 0.90 | 0.83 | 36.6 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 36 | 0.80 | 0.81 | 26.5 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 36 | 0.90 | 0.92 | 49.4 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 36 | 0.80 | 0.94 | 42.5 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 36 | 0.90 | 0.97 | 74.8 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 36 | 0.80 | 0.83 | 35.0 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 36 | 0.90 | 1.00 | 71.1 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 36 | 0.80 | 0.83 | 32.0 |
| dV_total_fixed | resolvable | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 36 | 0.90 | 0.92 | 47.0 |
| dV_total_fixed | all | lowo | gp | 81 | 0.80 | 0.85 | 32.4 |
| dV_total_fixed | all | lowo | gp | 81 | 0.90 | 0.89 | 41.6 |
| dV_total_fixed | all | lowo | evi_general | 81 | 0.80 | 0.81 | 33.1 |
| dV_total_fixed | all | lowo | evi_general | 81 | 0.90 | 0.91 | 64.5 |
| dV_total_fixed | all | lowo | ppt_all | 81 | 0.80 | 0.79 | 37.1 |
| dV_total_fixed | all | lowo | ppt_all | 81 | 0.90 | 0.91 | 59.5 |
| dV_total_fixed | all | lowo | eq_b | 81 | 0.80 | 0.79 | 32.6 |
| dV_total_fixed | all | lowo | eq_b | 81 | 0.90 | 0.91 | 60.6 |
| dV_total_fixed | all | lowo | lgbm | 81 | 0.80 | 0.80 | 34.2 |
| dV_total_fixed | all | lowo | lgbm | 81 | 0.90 | 0.91 | 55.2 |
| dV_total_fixed | all | lowo | two_stage_ml | 81 | 0.80 | 0.80 | 36.6 |
| dV_total_fixed | all | lowo | two_stage_ml | 81 | 0.90 | 0.91 | 61.4 |
| dV_total_fixed | all | lowo | hybrid | 81 | 0.80 | 0.79 | 30.6 |
| dV_total_fixed | all | lowo | hybrid | 81 | 0.90 | 0.91 | 55.0 |
| dV_total_fixed | all | holdout_2013-14 | gp | 8 | 0.80 | 0.75 | 28.0 |
| dV_total_fixed | all | holdout_2013-14 | gp | 8 | 0.90 | 0.88 | 35.9 |
| dV_total_fixed | all | holdout_2013-14 | evi_general | 8 | 0.80 | 0.75 | 30.2 |
| dV_total_fixed | all | holdout_2013-14 | evi_general | 8 | 0.90 | 0.88 | 70.2 |
| dV_total_fixed | all | holdout_2013-14 | ppt_all | 8 | 0.80 | 0.88 | 29.0 |
| dV_total_fixed | all | holdout_2013-14 | ppt_all | 8 | 0.90 | 0.88 | 79.3 |
| dV_total_fixed | all | holdout_2013-14 | eq_b | 8 | 0.80 | 0.75 | 31.0 |
| dV_total_fixed | all | holdout_2013-14 | eq_b | 8 | 0.90 | 1.00 | 61.9 |
| dV_total_fixed | all | holdout_2013-14 | lgbm | 8 | 0.80 | 0.88 | 56.3 |
| dV_total_fixed | all | holdout_2013-14 | lgbm | 8 | 0.90 | 1.00 | 91.9 |
| dV_total_fixed | all | holdout_2013-14 | two_stage_ml | 8 | 0.80 | 0.75 | 34.1 |
| dV_total_fixed | all | holdout_2013-14 | two_stage_ml | 8 | 0.90 | 1.00 | 78.7 |
| dV_total_fixed | all | holdout_2013-14 | hybrid | 8 | 0.80 | 0.88 | 35.6 |
| dV_total_fixed | all | holdout_2013-14 | hybrid | 8 | 0.90 | 1.00 | 54.1 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | gp | 39 | 0.80 | 0.82 | 30.7 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | gp | 39 | 0.90 | 0.87 | 39.4 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 39 | 0.80 | 0.85 | 41.5 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | evi_general | 39 | 0.90 | 0.97 | 69.2 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 39 | 0.80 | 0.74 | 26.2 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | ppt_all | 39 | 0.90 | 0.82 | 38.7 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 39 | 0.80 | 0.79 | 30.4 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | eq_b | 39 | 0.90 | 0.92 | 58.1 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 39 | 0.80 | 0.95 | 47.4 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | lgbm | 39 | 0.90 | 0.97 | 70.4 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 39 | 0.80 | 0.87 | 47.0 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | two_stage_ml | 39 | 0.90 | 0.95 | 67.6 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 39 | 0.80 | 0.79 | 30.5 |
| dV_total_fixed | all | recent_2015-16..2019-20(train<= 2014-15) | hybrid | 39 | 0.90 | 0.95 | 53.0 |
<!-- /AUTO:cov_v2 -->

**Reading.** CV+ conformal intervals are close to nominal on LOWO (v1 `dV_upper`, 90 % nominal → 0.92 for
all six models, n = 48; v2 0.89–0.93, n = 91) and conservative on hold-outs (often 1.00 on n = 12). They are,
however, **wide**: the 90 % interval for `dV_upper` is ~34–40 m³/m wide in v1 (observed SD 12.1 m³/m) and ~29–32 m³/m
in v2. The GP posterior is **over-confident** in v1 (90 % → 0.73 empirical, 80 % → 0.58) and only close to nominal
in v2 (0.86 at 90 %), so with n ≈ 50 the GP's own uncertainty should not be trusted without recalibration; the
conformal wrapper is the safer choice for an early-warning product. See `figures/fig_calibration.png`.

## 7. SHAP (LightGBM, `dV_upper`, fit on all resolvable events — an in-sample explanation)

v1:
<!-- AUTO:shap_v1 -->
| feature | mean abs SHAP (m³/m) |
|---|---|
| E_Hs2dt_stormHAT_m2h | 3.67 |
| intertidal_slope_pre | 2.59 |
| interval_days | 1.65 |
| E_Pflux_storm_GJ_m | 1.50 |
| berm_volume_pre | 1.45 |
| V_anom_past | 1.40 |
| dsls | 1.24 |
| hat_exceed_hours_storm | 1.14 |
| peak_hs | 0.84 |
| season_code | 0.42 |
| n_clusters | 0.00 |
<!-- /AUTO:shap_v1 -->
v2:
<!-- AUTO:shap_v2 -->
| feature | mean abs SHAP (m³/m) |
|---|---|
| E_Hs2dt_stormHAT_m2h | 3.90 |
| berm_volume_pre | 1.55 |
| mean_dir | 1.51 |
| E_Pflux_storm_GJ_m | 1.22 |
| hat_exceed_hours_storm | 1.15 |
| nao_winter | 1.07 |
| interval_days | 0.85 |
| dsls | 0.80 |
| V_anom_past | 0.46 |
| intertidal_slope_pre | 0.40 |
| peak_hs | 0.39 |
| season_code | 0.28 |
| n_clusters | 0.04 |
<!-- /AUTO:shap_v2 -->

**In words.** The storm energy reaching HAT (`E_Hs2dt_stormHAT_m2h`) dominates in both versions (mean |SHAP|
3.7 m³/m v1, 3.9 v2). In v1 the next features are the pre-storm intertidal slope (2.6) and the interval length
(1.7); in v2 they are the berm proxy (1.6), wave direction `mean_dir` (1.5) and the energy flux (1.2), with the
winter NAO at 1.1. The continuous antecedent anomaly is mid-ranked (1.4 v1, 0.5 v2) and the cluster count is
last in both. These are **in-sample** explanations of a model that does *not* beat the linear baselines out of
sample, so they describe what the trees use, not proven physical controls. Direction ranks high in v2 SHAP, but the direction
ablation (§5) shows no detectable out-of-sample gain from it. Figures:
`figures/fig_shap_summary.png`, `fig_shap_dependence.png` (and `_v2` versions).

## 8. v2C — Agent C's independent v2 build (robustness check only)

`src/evi/models/events_v2.py` builds a second extended table from Agent B's files *before* Agent A's v2 existed:
window `core300` (yl ∈ [−440, −160] m, the only window covering 2003–2019), Monitoring campaign only, B's fixed
volume window xl 70–170 m, hourly Castelle waves, **tide-only** TWL (no surge) and **HAT = +1.75 m** (superseded).
128 events, 2003–2019 (`figures/tables/C_events_v2C.csv`). Results are in `figures/tables/C_results_v2C.csv`
(hold-out layout: train ≤ 2012-13, test every winter from 2013-14; split `holdout_2013-14`, `holdout_all`).
It is **not** the headline; it shows whether conclusions survive a different longshore window, record length and
water-level treatment.

**Reading v2C (n = 128 events, 112 resolvable).** LOWO `dV_upper`: Equilibrium B 0.36 [0.15, 0.51], ShoreFor-
flavoured 0.33, EVI General 0.28 [0.04, 0.45], Harley 0.28, LightGBM 0.01 [−0.35, 0.26], GP 0.14. 2013-14 stress
test (n = 8): EVI General 0.63 [0.53, 0.96], ShoreFor-flavoured 0.60, LightGBM −0.04, GP −0.17. So with a different
window, a 2003–2019 record and tide-only TWL, the qualitative conclusion holds: physics/linear models ≥ ML, and the
equilibrium-type models are the most consistent. The sign of the ML-vs-EVI comparison on 2013-14 flips between v2
and v2C, which shows how fragile any 2013-14 ranking based on 8–12 events is.

## 8b. Slope sensitivity (slopefix tables)

Agent A's alternative tables recompute the runup foreshore slope β as the least-squares slope over 0 to +3 m MSL,
capped at 0.2 (HAT = +2.14 m as in the defaults): `data/processed/events_trucvert_slopefix.parquet` (51 events, mtime
2026-10-13 23:29:39 CEST) and `data/processed/events_trucvert_v2_slopefix.parquet` (98 events, mtime 2026-10-13 23:29:39 CEST),
with matching `intervals_*_slopefix.parquet`. Only the TWL-dependent columns change: the `*_stormHAT` energies,
the HAT-exceedance hours and max TWL (v2 max TWL 15.59 → 6.73 m; v1 8.67 → 7.92 m; correlation of `E_Hs2dt_stormHAT`
old vs new 0.975 for v1 and 0.974 for v2). Targets, volumes and storm definitions are unchanged, so models that do
not use HAT-filtered energy (Harley-type, ShoreFor-flavoured) give identical numbers. Run with
`python -m evi.models.run_all --data v1s|v2s --no-figs`; full tables in `figures/tables/C_*_v1s.csv`, `C_*_v2s.csv`,
side-by-side in `figures/tables/C_slopefix_comparison.csv`. Default results (v1, v2) are untouched.

**dV_upper, resolvable, LOWO** — skill vs climatology [95 % CI] (RMSE, m³/m)

| model | v1 (n=48) | v1s (n=48) | v2 (n=91) | v2s (n=91) |
|---|---|---|---|---|
| EVI General (dV ~ E_nbHAT) | 0.46 [0.24, 0.62] (9.0) | 0.56 [0.33, 0.71] (8.1) | 0.37 [0.06, 0.58] (8.5) | 0.39 [0.23, 0.51] (8.3) |
| PPT 2-stage (thesis-style) | 0.40 [0.15, 0.60] (9.4) | 0.51 [0.29, 0.67] (8.6) | 0.27 [-0.07, 0.48] (9.1) | 0.33 [0.04, 0.52] (8.8) |
| Harley-type (dV ~ sum Hs2 dt) | 0.48 [0.26, 0.63] (8.8) | 0.48 [0.26, 0.63] (8.8) | 0.40 [0.17, 0.56] (8.3) | 0.40 [0.17, 0.56] (8.3) |
| Equilibrium B (dV ~ E + E(V-Veq)) | 0.45 [0.25, 0.60] (9.1) | 0.52 [0.32, 0.68] (8.4) | 0.46 [0.27, 0.63] (7.9) | 0.47 [0.32, 0.59] (7.8) |
| ShoreFor-flavoured (phi by train fit) | 0.32 [0.01, 0.53] (10.1) | 0.32 [0.01, 0.53] (10.1) | 0.44 [0.24, 0.60] (8.0) | 0.44 [0.24, 0.60] (8.0) |
| Random forest | 0.41 [0.18, 0.56] (9.3) | 0.47 [0.25, 0.61] (8.8) | 0.38 [0.19, 0.53] (8.4) | 0.43 [0.23, 0.58] (8.1) |
| XGBoost | 0.27 [-0.10, 0.49] (10.4) | 0.31 [-0.03, 0.52] (10.1) | 0.31 [0.07, 0.49] (8.9) | 0.37 [0.13, 0.56] (8.4) |
| LightGBM | 0.22 [-0.19, 0.48] (10.8) | 0.31 [-0.10, 0.56] (10.1) | 0.31 [0.08, 0.50] (8.8) | 0.40 [0.16, 0.57] (8.3) |
| Gaussian process (RBF-ARD + White) | -0.09 [-0.38, 0.12] (12.7) | 0.24 [-0.09, 0.48] (10.6) | 0.33 [0.08, 0.49] (8.8) | 0.25 [-0.03, 0.46] (9.2) |
| Two-stage (logit -> OLS per branch, expected value) | 0.43 [0.23, 0.60] (9.2) | 0.53 [0.31, 0.70] (8.4) | 0.38 [0.10, 0.57] (8.4) | 0.43 [0.25, 0.58] (8.1) |
| Hybrid (Equilibrium B + LightGBM residual) | 0.38 [0.10, 0.58] (9.6) | 0.47 [0.21, 0.66] (8.9) | 0.44 [0.23, 0.61] (8.0) | 0.43 [0.26, 0.58] (8.1) |

**dV_upper, resolvable, 2013-14 hold-out (train ≤ 2012-13)** — skill vs climatology [95 % CI] (RMSE, m³/m)

| model | v1 (n=12) | v1s (n=12) | v2 (n=12) | v2s (n=12) |
|---|---|---|---|---|
| EVI General (dV ~ E_nbHAT) | 0.63 [0.18, 0.83] (7.6) | 0.75 [0.59, 0.86] (6.2) | -0.08 [-6.44, 0.76] (12.7) | 0.36 [-1.40, 0.65] (9.8) |
| PPT 2-stage (thesis-style) | 0.65 [0.10, 0.83] (7.4) | 0.65 [0.06, 0.84] (7.3) | 0.01 [-5.94, 0.75] (12.2) | 0.51 [-2.71, 0.85] (8.5) |
| Harley-type (dV ~ sum Hs2 dt) | 0.68 [0.38, 0.82] (7.1) | 0.68 [0.38, 0.82] (7.1) | 0.18 [-3.31, 0.72] (11.1) | 0.18 [-3.31, 0.72] (11.1) |
| Equilibrium B (dV ~ E + E(V-Veq)) | 0.61 [0.26, 0.87] (7.7) | 0.69 [0.38, 0.89] (6.9) | 0.17 [-4.05, 0.79] (11.2) | 0.56 [0.38, 0.62] (8.1) |
| ShoreFor-flavoured (phi by train fit) | 0.29 [0.03, 0.52] (10.5) | 0.29 [0.03, 0.52] (10.5) | 0.42 [-0.81, 0.60] (9.3) | 0.42 [-0.81, 0.60] (9.3) |
| Random forest | 0.64 [0.49, 0.77] (7.5) | 0.69 [0.58, 0.81] (7.0) | 0.46 [-0.28, 0.63] (9.0) | 0.50 [-0.44, 0.67] (8.7) |
| XGBoost | 0.50 [0.24, 0.67] (8.8) | 0.58 [0.36, 0.75] (8.0) | 0.53 [-0.14, 0.66] (8.4) | 0.51 [-0.35, 0.64] (8.6) |
| LightGBM | 0.60 [0.47, 0.71] (7.9) | 0.68 [0.54, 0.81] (7.1) | 0.58 [-0.55, 0.69] (7.9) | 0.58 [-0.90, 0.72] (7.9) |
| Gaussian process (RBF-ARD + White) | 0.12 [-0.72, 0.51] (11.6) | 0.29 [-0.40, 0.55] (10.5) | 0.61 [-1.00, 0.88] (7.6) | 0.62 [-1.25, 0.90] (7.5) |
| Two-stage (logit -> OLS per branch, expected value) | 0.54 [0.16, 0.78] (8.4) | 0.66 [0.35, 0.85] (7.2) | 0.09 [-5.06, 0.78] (11.7) | 0.43 [-1.43, 0.71] (9.2) |
| Hybrid (Equilibrium B + LightGBM residual) | 0.59 [0.14, 0.89] (8.0) | 0.65 [0.27, 0.91] (7.3) | 0.32 [-3.12, 0.88] (10.1) | 0.65 [0.17, 0.79] (7.2) |

**dV_total_fixed, resolvable, LOWO** — skill vs climatology [95 % CI] (RMSE, m³/m)

| model | v1 (n=48) | v1s (n=48) | v2 (n=76) | v2s (n=76) |
|---|---|---|---|---|
| EVI General (dV ~ E_nbHAT) | 0.57 [0.35, 0.72] (14.7) | 0.59 [0.35, 0.76] (14.3) | 0.39 [0.10, 0.59] (14.3) | 0.40 [0.12, 0.59] (14.1) |
| PPT 2-stage (thesis-style) | 0.53 [0.26, 0.70] (15.4) | 0.48 [0.15, 0.68] (16.2) | 0.36 [0.03, 0.56] (14.7) | 0.33 [-0.04, 0.54] (15.0) |
| Harley-type (dV ~ sum Hs2 dt) | 0.63 [0.41, 0.76] (13.7) | 0.63 [0.41, 0.76] (13.7) | 0.43 [0.21, 0.58] (13.9) | 0.43 [0.21, 0.58] (13.9) |
| Equilibrium B (dV ~ E + E(V-Veq)) | 0.61 [0.43, 0.72] (14.1) | 0.59 [0.36, 0.74] (14.5) | 0.51 [0.33, 0.65] (12.8) | 0.53 [0.30, 0.69] (12.6) |
| ShoreFor-flavoured (phi by train fit) | 0.32 [-0.03, 0.60] (18.6) | 0.32 [-0.03, 0.60] (18.6) | 0.46 [0.24, 0.61] (13.4) | 0.46 [0.24, 0.61] (13.4) |
| Random forest | 0.51 [0.28, 0.65] (15.7) | 0.47 [0.21, 0.63] (16.4) | 0.39 [0.20, 0.54] (14.3) | 0.42 [0.22, 0.55] (14.0) |
| XGBoost | 0.33 [-0.01, 0.57] (18.4) | 0.26 [-0.10, 0.53] (19.3) | 0.40 [0.17, 0.55] (14.2) | 0.43 [0.22, 0.57] (13.8) |
| LightGBM | 0.33 [-0.10, 0.56] (18.5) | 0.31 [-0.11, 0.55] (18.7) | 0.36 [0.11, 0.53] (14.6) | 0.41 [0.17, 0.56] (14.1) |
| Gaussian process (RBF-ARD + White) | 0.24 [-0.02, 0.45] (19.6) | 0.20 [-0.06, 0.40] (20.1) | 0.37 [0.08, 0.57] (14.6) | 0.31 [-0.02, 0.52] (15.2) |
| Two-stage (logit -> OLS per branch, expected value) | 0.58 [0.38, 0.72] (14.6) | 0.59 [0.36, 0.76] (14.4) | 0.39 [0.15, 0.56] (14.3) | 0.40 [0.16, 0.56] (14.2) |
| Hybrid (Equilibrium B + LightGBM residual) | 0.51 [0.28, 0.66] (15.8) | 0.55 [0.31, 0.72] (15.1) | 0.48 [0.26, 0.64] (13.2) | 0.51 [0.27, 0.67] (12.8) |

**dV_total_fixed, resolvable, 2013-14 hold-out (train ≤ 2012-13)** — skill vs climatology [95 % CI] (RMSE, m³/m)

| model | v1 (n=12) | v1s (n=12) | v2 (n=8) | v2s (n=8) |
|---|---|---|---|---|
| EVI General (dV ~ E_nbHAT) | 0.66 [0.28, 0.86] (13.0) | 0.73 [0.24, 0.92] (11.6) | 0.14 [-3.52, 0.88] (19.4) | 0.08 [-3.89, 0.92] (20.1) |
| PPT 2-stage (thesis-style) | 0.57 [-0.00, 0.83] (14.6) | 0.47 [-0.42, 0.80] (16.2) | 0.39 [-0.29, 0.53] (16.4) | 0.23 [-1.90, 0.55] (18.4) |
| Harley-type (dV ~ sum Hs2 dt) | 0.75 [0.44, 0.88] (11.2) | 0.75 [0.44, 0.88] (11.2) | 0.55 [-0.67, 0.82] (14.0) | 0.55 [-0.67, 0.82] (14.0) |
| Equilibrium B (dV ~ E + E(V-Veq)) | 0.75 [0.38, 0.91] (11.2) | 0.64 [0.06, 0.86] (13.4) | 0.73 [0.30, 0.80] (10.8) | 0.66 [-0.77, 0.86] (12.2) |
| ShoreFor-flavoured (phi by train fit) | 0.25 [0.10, 0.52] (19.3) | 0.25 [0.10, 0.52] (19.3) | 0.61 [-0.40, 0.78] (13.1) | 0.61 [-0.40, 0.78] (13.1) |
| Random forest | 0.83 [0.66, 0.91] (9.3) | 0.70 [0.16, 0.89] (12.2) | 0.43 [0.10, 0.75] (15.8) | 0.41 [-0.14, 0.73] (16.1) |
| XGBoost | 0.85 [0.72, 0.91] (8.6) | 0.77 [0.49, 0.86] (10.8) | 0.61 [0.47, 0.95] (13.1) | 0.58 [0.32, 0.85] (13.5) |
| LightGBM | 0.82 [0.66, 0.92] (9.4) | 0.73 [0.32, 0.87] (11.7) | 0.36 [0.11, 0.90] (16.8) | 0.37 [0.12, 0.80] (16.6) |
| Gaussian process (RBF-ARD + White) | 0.38 [0.25, 0.53] (17.5) | 0.36 [0.18, 0.48] (17.9) | 0.51 [0.11, 0.58] (14.6) | 0.41 [-1.36, 0.67] (16.1) |
| Two-stage (logit -> OLS per branch, expected value) | 0.73 [0.44, 0.86] (11.7) | 0.74 [0.30, 0.91] (11.3) | 0.30 [-2.39, 0.85] (17.6) | 0.22 [-3.28, 0.87] (18.6) |
| Hybrid (Equilibrium B + LightGBM residual) | 0.76 [0.40, 0.91] (10.9) | 0.72 [0.28, 0.88] (11.8) | 0.68 [-0.20, 0.81] (11.8) | 0.65 [-0.78, 0.84] (12.5) |

Recent hold-out (v2s, train ≤ 2014-15, test 2015-16 → 2019-20, n = 38, `dV_upper`): EVI General 0.37
[0.11, 0.60] (v2: 0.38), Equilibrium B 0.48 [0.20, 0.71] (v2: 0.47), ShoreFor-flavoured 0.46 (same), LightGBM 0.05
[−0.56, 0.53] (v2: −0.17), GP 0.41 [0.07, 0.66] (v2: 0.31).

The HAT-filter ablation changes direction on v1s `dV_upper`. HAT-filtered Hs²Δt is now marginally better than
all-storm Hs²Δt (ΔRMSE −0.64 [−1.57, +0.18]), where on v1 it was +0.24 [−0.21, +0.71]. The CI still includes 0, and
v2s shows no difference (+0.04 [−0.57, +0.80]).

**Verdict:** the slope fix makes the HAT-filtered models better, and does so most clearly on v1. EVI General goes
from 0.46 to 0.56 on LOWO `dV_upper` and from 0.63 to 0.75 on 2013-14. On v2 2013-14, EVI General goes from −0.08 to
0.36 and Equilibrium B from 0.17 to 0.56 [0.38, 0.62], so the v2 2013-14 collapse of the linear models was partly a
TWL artefact. **No conclusion changes:**
* No model beats EVI General by more than the CIs on LOWO.
* The trees and the GP still do not beat the best linear or equilibrium baseline on LOWO (v2s `dV_upper`:
  LightGBM 0.40 and GP 0.25, against Equilibrium B 0.47).
* Equilibrium B remains the most consistent model.
* The antecedent-state, cluster and flux verdicts are unaffected.

## 9. Honest conclusion

1. **Honest re-evaluation of the 2017/2018 EVI.** Under leave-one-winter-out on resolvable events, the General
   model (ΔV_upper = a·E + b) has skill 0.46 [0.24, 0.62] vs climatology in v1 (n = 48), RMSE 9.0 [7.3, 10.5] m³/m,
   R² 0.44 [0.19, 0.61], and 0.37 [0.06, 0.58] in v2 (n = 91). It is a real but modest predictor. Thesis: General
   calibration R² = 0.26, RMSE 22.4 m³/m (different units/HAT/event set, not comparable one-to-one). The thesis-style
   PPT (classifier → erosive-only regression) is **not** better than General: v1 LOWO skill 0.40 [0.15, 0.60], v2
   0.27 [−0.07, 0.48]. On the v1 2013-14 hold-out it reaches RMSE 7.4 m³/m, R² 0.56 [0.06, 0.73] on `dV_upper`
   (n = 12); thesis: "0.85", RMSE 7.5 m³/m on erosive events only (whole profile, R vs R² ambiguous). The thesis's
   high validation score is **not** reproduced as an R² on all events.
2. **Survey spacing matters more than any model.** Including the three intervals > 45 d (v1) turns the EVI's
   LOWO skill from 0.46 to −0.21 [−1.30, 0.29] (n = 51); v2 from 0.37 to −0.12. The resolvability rule is the
   single most important modelling decision, and it was fixed before seeing results.
3. **Does anything beat the baselines on held-out winters?** Not convincingly. Best LOWO model per target and
   version, skill vs climatology: v1 `dV_upper` Harley-type 0.48 [0.26, 0.63]; v1 `dV_total_fixed` Harley-type
   0.63 [0.41, 0.76]; v2 `dV_upper` Equilibrium B 0.46 [0.27, 0.63]; v2 `dV_total_fixed` Equilibrium B 0.51
   [0.33, 0.65]. All of these overlap the EVI General CI. Skill vs the thesis PPT: Harley-type +0.14 (v1 `dV_upper`),
   Equilibrium B +0.26 (v2 `dV_upper`) and +0.24 (v2 `dV_total_fixed`). The ML models (LightGBM, XGBoost, RF, GP,
   hybrid) **never** beat the best linear/equilibrium baseline on LOWO; they win only on single hold-out winters
   with n = 8–12 and CIs that include the baseline (e.g. v1 2013-14 `dV_total_fixed`: XGBoost 0.85 [0.72, 0.91] vs
   EVI General 0.66 [0.28, 0.86]; on LOWO the same XGBoost is at 0.33). On the v2 recent hold-out (2015-16 → 2019-20,
   n = 38) Equilibrium B is best (0.47 [0.13, 0.75]) and LightGBM is worse than climatology.
4. **Antecedent state, clustering, flux, HAT filter, direction:** none of the 2017 open questions gives a
   detectable gain with these data (§5); the only detectable gain is the concurrent winter NAO inside LightGBM,
   which still leaves LightGBM below Equilibrium B. The most defensible improvement over the 2017 EVI is the **equilibrium/disequilibrium**
   form (Equilibrium B: a·E + c·E·(V_pre − V_eq)) and, in v2, the ShoreFor-flavoured model. Both are physics-based
   and give the best and most stable out-of-winter skill, but their margin over EVI General is within the CIs.
5. **Uncertainty:** conformal intervals are calibrated but ~3× the observed SD wide; GP intervals are
   over-confident in v1. An early-warning use should report conformal intervals, not GP posteriors.

**Bottom line for the paper:** with 48–91 resolvable events, a continuous antecedent state and storm sequencing do
**not** measurably beat the 2017/2018 linear EVI on held-out winters; a disequilibrium term gives a small,
non-significant improvement that is consistent across v1, v2 and v2C. This is the "state clearly why it doesn't"
outcome of HANDOFF §0, and it is publishable. Positioning: comparable small-n ML storm-erosion studies at Narrabeen
(Simmons & Splinter 2022, Env. Modelling & Software 150:105356; Harley et al. 2023; Calcraft et al. 2025, Coastal
Engineering 201:104813) and the GP approach of Beuzen et al. 2019 (NHESS 19:2295) are the right comparison set
(references from Agent D's review; check them there before citing).

## 10. Data issues for Agent A (flagged, not fixed)

1. **peak_hs = 14.23 m on 2009-01-24 09:00 (Klaus), v1 event TV20080408.** It is a single 3-h sample; the samples
   either side are 10.51 and 10.63 m. Independent series for the same window: Castelle et al. 2020 buoy-corrected
   hindcast max 9.32 m, RESOURCECODE node 94337 max 12.3 m. Likely a spike in the legacy WW3 series, or at least an
   outlier to check [verify]. It only affects the 307-day (non-resolvable) event in v1.
2. **The legacy WW3 Hs runs high against both of Agent B's series at storm peaks** (e.g. 2008-03-11: 9.61 m vs
   7.0 m Castelle / 7.17 m RESOURCECODE; 2014-03-03: 9.15 vs 7.77 / 8.11 m). This is consistent with Agent A's lower
   v2 thresholds (Hs95 3.56 m vs 4.22 m) and means energies are not comparable between v1 and v2 in absolute terms.
3. **max_twl_all = 15.59 m MSL in v2 event TV20140303** (peak Hs 7.77 m). That is beyond any plausible runup at
   Truc Vert. Probably a runup β or H0 artefact (very steep slope from the last survey, or a de-shoaling blow-up).
   In v1, max TWL reaches 8.67 m (TV20140303) and 8.26 m (TV20080211), which are also high for Stockdon on a
   dissipative beach. Please check β (slope from SWL to +4 m) for those surveys [verify].
4. **v2 missing pre-storm state:** 9 events have NaN `V_pre_total/upper/lower` and 17 NaN `dV_*_fixed` (survey does
   not reach the fixed window). I carried the last earlier survey's value forward for the predictors (past-only) and
   dropped the 17 only for the `dV_total_fixed` target. A cleaner fix upstream would help.
5. `days_since_last_storm` is NaN for the first v1 event; I filled it with the column max (documented in
   `protocol.prepare`).
6. (Fixed by A during this session: the 1-h clock offset in the legacy CSV and the HAT datum, 1.75 → 2.14 m MSL.)

## 11. Limitations

* **Small n:** 48 (v1) / 91 (v2) resolvable events and 12 events in the 2013-14 hold-out (8 for v2
  `dV_total_fixed`). Bootstrap CIs on hold-out skills are very wide; hold-out rankings are unstable (v2 vs v2C).
* **Bootstrap CIs** resample events and ignore within-winter dependence, so they are, if anything, too narrow.
* **Splinter et al. (2014) and Harley et al. (2009)** are implemented as *flavoured* stand-ins; the published
  equations were not checked against the papers in this session [verify]. ShoreFor is a simplified, survey-interval
  version (daily Ω, φ chosen in-sample, w_s assumed) and is not the full Davidson et al. (2013) model.
* **Hyper-parameters** were fixed a priori, not tuned; a nested tuning might help the trees slightly, but n is too
  small for it to be trusted.
* **SHAP** values are in-sample.
* `nao_winter` is a concurrent seasonal index (DJFM of the same winter), so it is diagnostic, not a forecast input.
* **PySR not run.** First import downloads Julia from the internet. It was skipped to keep inside the time box and to
  avoid an unplanned large download on the owner's machine.
* The storm thresholds are in-sample for events before 2013-12-01 (Agent A's choice, documented).
* v2C (my own build) uses HAT = 1.75 m and tide-only TWL; it is a robustness check only. Its result tables use the
  earlier single hold-out layout (train ≤ 2012-13, test every later winter).

## 12. Reproduce

```bash
source .venv/bin/activate            # Python 3.12, requirements.txt
python -m evi.models.run_all --data v1   # ~2 min: tables in figures/tables/, figures in figures/
python -m evi.models.run_all --data v2   # ~6 min (needs data/processed/events_trucvert_v2.parquet)
python -m evi.models.run_all --data v2C  # optional: C's own build from Agent B's files (+ raw tide nc)
python -m evi.models.run_all --data v1s --no-figs  # slope-fix sensitivity (Agent A's *_slopefix tables)
python -m evi.models.run_all --data v2s --no-figs
python -c "from evi.models.run_all import hat_sensitivity, direction_ablation; hat_sensitivity(); direction_ablation()"
python -m evi.models.report v1 v2 v2C   # refresh the auto tables in this file + model cards
```
Seeds are fixed (0); results are deterministic on the same library versions (`requirements.lock.txt`).
Checked in this session: a fresh `git clone` of `revisit-2026` run with `python -m evi.models.run_all --data v1`
reproduced `figures/tables/C_results_v1.csv` exactly (max absolute difference 0.0). Figures can be re-drawn from the
saved tables without refitting (see `evi.models.figures.make_all`).
