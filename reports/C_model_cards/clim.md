# Model card — Climatology (train mean) (`clim`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** none (training-fold mean of the target)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Climatology (train mean)
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 12.2 [9.8, 14.3] | -0.03 [-0.15, -0.01] | 0.00 [0.00, 0.00] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 12.4 [7.7, 16.1] | -0.24 [-1.14, -0.00] | 0.00 [0.00, 0.00] |
| dV_upper | all | lowo | 51 | 12.9 [10.2, 15.5] | -0.03 [-0.14, -0.01] | 0.00 [0.00, 0.00] |
| dV_upper | all | holdout_2013-14 | 12 | 12.6 [7.6, 16.4] | -0.28 [-1.23, -0.01] | 0.00 [0.00, 0.00] |
| dV_total_fixed | resolvable | lowo | 48 | 22.5 [16.6, 27.6] | -0.02 [-0.14, -0.00] | 0.00 [0.00, 0.00] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 22.3 [13.8, 29.1] | -0.03 [-0.80, -0.00] | 0.00 [0.00, 0.00] |
| dV_total_fixed | all | lowo | 51 | 26.3 [19.4, 33.5] | -0.01 [-0.11, -0.00] | 0.00 [0.00, 0.00] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 22.4 [13.5, 29.4] | -0.04 [-0.81, -0.00] | 0.00 [0.00, 0.00] |
