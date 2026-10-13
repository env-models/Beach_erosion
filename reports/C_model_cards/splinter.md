# Model card — Splinter-flavoured (dV ~ sum P dt + n_clusters) (`splinter`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Pflux_storm_GJ_m, n_clusters
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Ordinary least squares on a list of columns or callables (intercept included).
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.2 [7.5, 10.7] | 0.41 [0.12, 0.58] | 0.43 [0.18, 0.60] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.2 [4.3, 9.4] | 0.58 [0.13, 0.80] | 0.66 [0.36, 0.83] |
| dV_upper | all | lowo | 51 | 12.2 [8.8, 15.9] | 0.07 [-0.61, 0.42] | 0.10 [-0.55, 0.46] |
| dV_upper | all | holdout_2013-14 | 12 | 7.5 [5.2, 9.3] | 0.55 [0.11, 0.72] | 0.65 [0.38, 0.78] |
| dV_total_fixed | resolvable | lowo | 48 | 15.1 [11.9, 18.2] | 0.54 [0.21, 0.71] | 0.55 [0.26, 0.72] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 10.1 [6.4, 13.3] | 0.79 [0.30, 0.90] | 0.79 [0.49, 0.91] |
| dV_total_fixed | all | lowo | 51 | 23.0 [14.1, 31.7] | 0.23 [-0.17, 0.55] | 0.23 [-0.11, 0.57] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 12.3 [7.7, 16.1] | 0.69 [0.16, 0.83] | 0.70 [0.37, 0.85] |
