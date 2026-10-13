# Model card — Equilibrium B (dV ~ E + E(V-Veq)) (`eq_b`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_Hs2dt_stormHAT_m2h, E × (V_pre_total − V_eq)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Ordinary least squares on a list of columns or callables (intercept included).
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.1 [7.1, 10.8] | 0.43 [0.19, 0.58] | 0.45 [0.25, 0.60] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.7 [3.9, 11.5] | 0.52 [-0.07, 0.83] | 0.61 [0.26, 0.87] |
| dV_upper | all | lowo | 51 | 12.6 [9.2, 16.2] | 0.00 [-0.64, 0.37] | 0.04 [-0.56, 0.40] |
| dV_upper | all | holdout_2013-14 | 12 | 11.7 [6.5, 17.1] | -0.11 [-1.46, 0.62] | 0.13 [-0.63, 0.69] |
| dV_total_fixed | resolvable | lowo | 48 | 14.1 [11.0, 17.1] | 0.60 [0.39, 0.71] | 0.61 [0.43, 0.72] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 11.2 [6.1, 15.3] | 0.74 [0.21, 0.89] | 0.75 [0.38, 0.91] |
| dV_total_fixed | all | lowo | 51 | 22.0 [15.1, 29.3] | 0.29 [0.09, 0.46] | 0.30 [0.11, 0.48] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 17.9 [10.8, 23.6] | 0.34 [-0.87, 0.70] | 0.36 [-0.40, 0.72] |
