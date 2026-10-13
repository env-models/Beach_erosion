# Model card — XGBoost (`xgb`)

* **Code:** `src/evi/models/ml.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Hs2dt_stormHAT_m2h, E_Pflux_storm_GJ_m, peak_hs, hat_exceed_hours_storm, n_clusters, dsls, interval_days, season_code, V_anom_past, berm_volume_pre, intertidal_slope_pre
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** {"n_estimators": 300, "learning_rate": 0.03, "max_depth": 2, "min_child_weight": 6, "subsample": 0.8, "colsample_bytree": 0.8, "reg_lambda": 2.0, "random_state": 0, "n_jobs": 1}; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** XGBoost
* **Known failure modes:** As LightGBM.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 10.4 [8.5, 12.2] | 0.24 [-0.17, 0.46] | 0.27 [-0.10, 0.49] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 8.8 [5.6, 11.6] | 0.37 [-0.12, 0.62] | 0.50 [0.24, 0.67] |
| dV_upper | all | lowo | 51 | 11.4 [8.8, 13.9] | 0.19 [-0.16, 0.40] | 0.22 [-0.10, 0.43] |
| dV_upper | all | holdout_2013-14 | 12 | 10.3 [5.7, 15.0] | 0.14 [-0.88, 0.69] | 0.33 [-0.33, 0.74] |
| dV_total_fixed | resolvable | lowo | 48 | 18.4 [13.9, 22.6] | 0.32 [-0.08, 0.55] | 0.33 [-0.01, 0.57] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 8.6 [5.9, 11.0] | 0.85 [0.63, 0.90] | 0.85 [0.72, 0.91] |
| dV_total_fixed | all | lowo | 51 | 23.7 [16.3, 31.1] | 0.18 [-0.17, 0.44] | 0.19 [-0.12, 0.46] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 10.2 [6.2, 14.1] | 0.79 [0.20, 0.90] | 0.79 [0.39, 0.91] |
