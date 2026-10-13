# Model card — Equilibrium A (dV ~ E(V-Veq)) (`eq_a`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Hs2dt_stormHAT_m2h × (V_pre_total − V_eq), V_eq = training-fold mean
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Ordinary least squares on a list of columns or callables (intercept included).
* **Known failure modes:** No main energy term: the disequilibrium product alone cannot predict erosion of a 'normal' beach.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 12.7 [9.6, 15.3] | -0.11 [-0.68, 0.26] | -0.08 [-0.53, 0.29] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 16.9 [9.3, 23.0] | -1.31 [-4.06, 0.10] | -0.86 [-2.42, 0.21] |
| dV_upper | all | lowo | 51 | 12.6 [10.1, 14.9] | 0.01 [-0.35, 0.25] | 0.04 [-0.26, 0.28] |
| dV_upper | all | holdout_2013-14 | 12 | 13.6 [8.3, 17.7] | -0.49 [-1.87, 0.08] | -0.16 [-0.63, 0.18] |
| dV_total_fixed | resolvable | lowo | 48 | 23.1 [16.7, 29.2] | -0.07 [-0.80, 0.35] | -0.06 [-0.69, 0.36] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 31.9 [16.7, 45.6] | -1.09 [-3.41, 0.18] | -1.04 [-2.87, 0.23] |
| dV_total_fixed | all | lowo | 51 | 26.2 [18.7, 33.8] | -0.01 [-0.51, 0.27] | 0.01 [-0.45, 0.29] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 23.8 [14.1, 31.4] | -0.17 [-1.11, 0.10] | -0.12 [-0.48, 0.14] |
