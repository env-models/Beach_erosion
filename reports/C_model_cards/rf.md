# Model card — Random forest (`rf`)

* **Code:** `src/evi/models/ml.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Hs2dt_stormHAT_m2h, E_Pflux_storm_GJ_m, peak_hs, hat_exceed_hours_storm, n_clusters, dsls, interval_days, season_code, V_anom_past, berm_volume_pre, intertidal_slope_pre
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** {"n_estimators": 500, "max_depth": 3, "min_samples_leaf": 4, "max_features": 0.5, "random_state": 0, "n_jobs": 1}; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Random forest
* **Known failure modes:** Flat extrapolation beyond the training energy range (e.g. Klaus-type storms).

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.3 [7.6, 11.0] | 0.39 [0.13, 0.54] | 0.41 [0.18, 0.56] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.5 [4.5, 9.9] | 0.55 [0.22, 0.72] | 0.64 [0.49, 0.77] |
| dV_upper | all | lowo | 51 | 10.9 [8.1, 13.8] | 0.26 [-0.01, 0.45] | 0.29 [0.05, 0.48] |
| dV_upper | all | holdout_2013-14 | 12 | 8.6 [5.0, 12.0] | 0.40 [-0.19, 0.70] | 0.53 [0.24, 0.74] |
| dV_total_fixed | resolvable | lowo | 48 | 15.7 [12.1, 18.9] | 0.51 [0.23, 0.64] | 0.51 [0.28, 0.65] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 9.3 [5.7, 12.2] | 0.82 [0.53, 0.89] | 0.83 [0.66, 0.91] |
| dV_total_fixed | all | lowo | 51 | 20.9 [13.9, 29.4] | 0.36 [0.06, 0.60] | 0.37 [0.11, 0.62] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 8.3 [5.6, 10.6] | 0.86 [0.63, 0.91] | 0.86 [0.73, 0.93] |
