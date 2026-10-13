# Model card — EVI General (dV ~ E_nbHAT) (`evi_general`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_notebook_stormHAT_MJh_m2 (≡ ρg/16·ΣHs²Δt over storm samples with TWL ≥ HAT)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Ordinary least squares on a list of columns or callables (intercept included).
* **Known failure modes:** Long survey intervals (> 45 d) mix storms and recovery; skill collapses when they are included.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.0 [7.3, 10.5] | 0.44 [0.19, 0.61] | 0.46 [0.24, 0.62] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.6 [4.6, 10.2] | 0.53 [-0.13, 0.80] | 0.63 [0.18, 0.83] |
| dV_upper | all | lowo | 51 | 14.1 [9.6, 19.3] | -0.24 [-1.43, 0.26] | -0.21 [-1.30, 0.29] |
| dV_upper | all | holdout_2013-14 | 12 | 10.4 [5.8, 13.8] | 0.12 [-0.56, 0.47] | 0.32 [0.18, 0.53] |
| dV_total_fixed | resolvable | lowo | 48 | 14.7 [11.4, 17.9] | 0.57 [0.31, 0.72] | 0.57 [0.35, 0.72] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 13.0 [7.2, 17.5] | 0.65 [0.02, 0.85] | 0.66 [0.28, 0.86] |
| dV_total_fixed | all | lowo | 51 | 25.1 [15.4, 34.7] | 0.07 [-0.37, 0.45] | 0.08 [-0.33, 0.46] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 15.0 [8.3, 20.6] | 0.54 [0.17, 0.76] | 0.56 [0.39, 0.77] |
