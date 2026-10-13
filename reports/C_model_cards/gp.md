# Model card — Gaussian process (RBF-ARD + White) (`gp`)

* **Code:** `src/evi/models/ml.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Hs2dt_stormHAT_m2h, V_anom_past, berm_volume_pre, interval_days (energy as log1p; all standardised)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** ConstantKernel·RBF(ARD)+White, normalize_y, 5 optimizer restarts; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** GP regression, ConstantKernel*RBF(ARD) + White on standardised inputs, normalize_y.
    energy enters as log1p (heavy right tail).
* **Known failure modes:** Posterior intervals under-cover (overconfident) with n ≈ 40 training events.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 12.7 [10.3, 15.0] | -0.13 [-0.48, 0.05] | -0.09 [-0.38, 0.12] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 11.6 [7.9, 14.6] | -0.09 [-1.12, 0.39] | 0.12 [-0.72, 0.51] |
| dV_upper | all | lowo | 51 | 12.8 [10.5, 15.2] | -0.02 [-0.30, 0.16] | 0.01 [-0.24, 0.21] |
| dV_upper | all | holdout_2013-14 | 12 | 11.7 [8.1, 14.5] | -0.11 [-1.22, 0.38] | 0.14 [-0.81, 0.52] |
| dV_total_fixed | resolvable | lowo | 48 | 19.6 [14.6, 24.3] | 0.23 [-0.07, 0.43] | 0.24 [-0.02, 0.45] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 17.5 [10.5, 22.9] | 0.37 [-0.10, 0.50] | 0.38 [0.25, 0.53] |
| dV_total_fixed | all | lowo | 51 | 21.0 [14.4, 28.4] | 0.35 [0.05, 0.60] | 0.36 [0.08, 0.61] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 17.4 [10.3, 22.7] | 0.38 [-0.09, 0.53] | 0.40 [0.27, 0.55] |
