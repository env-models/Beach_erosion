# Model card — LightGBM (`lgbm`)

* **Code:** `src/evi/models/ml.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Hs2dt_stormHAT_m2h, E_Pflux_storm_GJ_m, peak_hs, hat_exceed_hours_storm, n_clusters, dsls, interval_days, season_code, V_anom_past, berm_volume_pre, intertidal_slope_pre
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** {"n_estimators": 300, "learning_rate": 0.03, "num_leaves": 4, "max_depth": 2, "min_child_samples": 6, "subsample": 0.8, "subsample_freq": 1, "colsample_bytree": 0.8, "reg_lambda": 2.0, "random_state": 0, "verbose": -1, "deterministic": true, "force_row_wise": true}; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** LightGBM
* **Known failure modes:** n ≈ 40 training events per fold; depth-2 trees still unstable; extrapolates flat beyond training energy range.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 10.8 [8.6, 12.8] | 0.19 [-0.25, 0.46] | 0.22 [-0.19, 0.48] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.9 [4.9, 10.4] | 0.50 [0.13, 0.68] | 0.60 [0.47, 0.71] |
| dV_upper | all | lowo | 51 | 11.5 [8.8, 14.0] | 0.18 [-0.21, 0.40] | 0.20 [-0.16, 0.42] |
| dV_upper | all | holdout_2013-14 | 12 | 9.3 [6.6, 11.7] | 0.30 [-0.34, 0.56] | 0.46 [0.00, 0.64] |
| dV_total_fixed | resolvable | lowo | 48 | 18.5 [14.1, 22.3] | 0.32 [-0.17, 0.54] | 0.33 [-0.10, 0.56] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 9.4 [5.7, 12.1] | 0.82 [0.54, 0.91] | 0.82 [0.66, 0.92] |
| dV_total_fixed | all | lowo | 51 | 22.5 [15.7, 29.1] | 0.26 [-0.03, 0.48] | 0.27 [0.00, 0.49] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 9.1 [6.1, 11.8] | 0.83 [0.60, 0.90] | 0.84 [0.68, 0.90] |
