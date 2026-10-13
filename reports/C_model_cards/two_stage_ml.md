# Model card — Two-stage (logit -> OLS per branch, expected value) (`two_stage_ml`)

* **Code:** `src/evi/models/ml.py`; run via `python -m evi.models.run_all`.
* **Inputs:** classifier: E_Hs2dt_stormHAT, V_anom_past, berm_volume_pre; regressors: E_Hs2dt_stormHAT
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Classifier (logistic on standardised E_HAT, V_anom_past, berm) -> P(erode); regressors
    per branch (OLS on E_HAT within training events of that sign). Prediction = expected value
    p*mu_ero + (1-p)*mu_acc. Branch fitting uses TRAINING labels only (never test dV).
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.2 [7.4, 10.8] | 0.41 [0.17, 0.57] | 0.43 [0.23, 0.60] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 8.4 [5.3, 11.3] | 0.43 [-0.14, 0.74] | 0.54 [0.16, 0.78] |
| dV_upper | all | lowo | 51 | 14.4 [10.7, 18.3] | -0.30 [-1.10, 0.07] | -0.26 [-1.00, 0.11] |
| dV_upper | all | holdout_2013-14 | 12 | 13.5 [7.8, 18.6] | -0.47 [-1.82, 0.15] | -0.15 [-0.67, 0.23] |
| dV_total_fixed | resolvable | lowo | 48 | 14.6 [11.4, 17.9] | 0.57 [0.34, 0.71] | 0.58 [0.38, 0.72] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 11.7 [7.3, 15.1] | 0.72 [0.28, 0.84] | 0.73 [0.44, 0.86] |
| dV_total_fixed | all | lowo | 51 | 26.1 [18.0, 34.5] | 0.00 [-0.28, 0.25] | 0.01 [-0.23, 0.27] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 23.0 [13.5, 30.4] | -0.09 [-1.88, 0.40] | -0.05 [-1.27, 0.44] |
