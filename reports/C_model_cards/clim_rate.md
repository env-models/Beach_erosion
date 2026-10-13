# Model card — Climatology (rate x interval) (`clim_rate`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** interval_days; rate = Σ dV / Σ days over all training-winter survey intervals (storm-free included)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Interval-length-scaled climatology: (sum dV / sum days) over ALL training-winter
    survey intervals (incl. storm-free ones) x interval_days.
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 13.7 [10.6, 16.6] | -0.31 [-0.63, -0.10] | -0.26 [-0.49, 0.03] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 15.9 [9.6, 20.6] | -1.04 [-2.81, -0.40] | -0.64 [-0.90, -0.39] |
| dV_upper | all | lowo | 51 | 14.0 [10.9, 17.3] | -0.23 [-0.54, -0.04] | -0.19 [-0.41, 0.05] |
| dV_upper | all | holdout_2013-14 | 12 | 15.9 [9.6, 20.6] | -1.04 [-2.81, -0.40] | -0.59 [-0.83, -0.39] |
| dV_total_fixed | resolvable | lowo | 48 | 25.3 [18.3, 31.7] | -0.29 [-0.63, -0.10] | -0.27 [-0.52, -0.00] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 27.2 [13.5, 37.0] | -0.53 [-1.66, -0.07] | -0.49 [-0.85, 0.24] |
| dV_total_fixed | all | lowo | 51 | 27.9 [20.9, 34.9] | -0.14 [-0.46, 0.04] | -0.13 [-0.37, 0.08] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 27.2 [13.5, 37.0] | -0.53 [-1.66, -0.07] | -0.47 [-0.80, 0.21] |
