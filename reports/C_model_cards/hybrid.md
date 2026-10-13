# Model card — Hybrid (Equilibrium B + LightGBM residual) (`hybrid`)

* **Code:** `src/evi/models/ml.py`; run via `python -m evi.models.run_all`.
* **Inputs:** Equilibrium B inputs + LightGBM (100 trees) on E_Hs2dt_stormHAT_m2h, E_Pflux_storm_GJ_m, peak_hs, hat_exceed_hours_storm, n_clusters, dsls, interval_days, season_code, V_anom_past, berm_volume_pre, intertidal_slope_pre
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Equilibrium-B baseline + shallow LightGBM on its in-sample residuals (shrunk: 100 trees).
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.6 [7.8, 11.3] | 0.36 [0.04, 0.55] | 0.38 [0.10, 0.58] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 8.0 [3.8, 12.0] | 0.49 [-0.16, 0.85] | 0.59 [0.14, 0.89] |
| dV_upper | all | lowo | 51 | 12.6 [9.6, 15.7] | 0.01 [-0.59, 0.36] | 0.04 [-0.49, 0.39] |
| dV_upper | all | holdout_2013-14 | 12 | 13.0 [7.2, 18.4] | -0.36 [-1.87, 0.53] | -0.06 [-1.12, 0.64] |
| dV_total_fixed | resolvable | lowo | 48 | 15.8 [12.6, 18.9] | 0.50 [0.23, 0.64] | 0.51 [0.28, 0.66] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 10.9 [6.0, 14.9] | 0.76 [0.24, 0.90] | 0.76 [0.40, 0.91] |
| dV_total_fixed | all | lowo | 51 | 21.2 [15.4, 27.2] | 0.34 [0.16, 0.48] | 0.35 [0.19, 0.50] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 18.9 [11.9, 24.8] | 0.26 [-1.12, 0.66] | 0.29 [-0.65, 0.68] |
