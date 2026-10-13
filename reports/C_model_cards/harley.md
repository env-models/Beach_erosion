# Model card — Harley-type (dV ~ sum Hs2 dt) (`harley`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Hs2dt_storm_m2h (all storm samples, no HAT filter)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Ordinary least squares on a list of columns or callables (intercept included).
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 8.8 [7.1, 10.2] | 0.47 [0.21, 0.62] | 0.48 [0.26, 0.63] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.1 [4.5, 9.0] | 0.60 [0.15, 0.78] | 0.68 [0.38, 0.82] |
| dV_upper | all | lowo | 51 | 12.8 [9.1, 16.8] | -0.02 [-0.81, 0.34] | 0.01 [-0.71, 0.37] |
| dV_upper | all | holdout_2013-14 | 12 | 9.8 [5.1, 13.0] | 0.22 [-0.41, 0.58] | 0.40 [0.25, 0.62] |
| dV_total_fixed | resolvable | lowo | 48 | 13.7 [11.0, 16.3] | 0.62 [0.37, 0.75] | 0.63 [0.41, 0.76] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 11.2 [7.0, 14.6] | 0.74 [0.22, 0.86] | 0.75 [0.44, 0.88] |
| dV_total_fixed | all | lowo | 51 | 22.3 [14.0, 30.6] | 0.27 [-0.01, 0.53] | 0.28 [0.03, 0.54] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 13.2 [7.0, 18.4] | 0.64 [0.35, 0.83] | 0.65 [0.50, 0.84] |
