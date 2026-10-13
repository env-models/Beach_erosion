# Model card — PPT (binary state, all events) (`ppt_all`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_notebook_stormHAT_MJh_m2, binary state = V_pre_total > training-fold mean
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** 'Honest' PPT: binary pre-storm state (V_pre_total above/below the TRAINING-fold mean,
    i.e. fat/thin vs the mean profile) with a separate dV = a_s E + b_s per state, fitted on
    ALL training events (no filtering on dV). Falls back to pooled if a state has < 3 events.
* **Known failure modes:** Small n; see C_models.md limitations.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.0 [7.0, 10.7] | 0.44 [0.19, 0.61] | 0.45 [0.24, 0.63] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.3 [4.7, 9.7] | 0.57 [0.13, 0.80] | 0.65 [0.41, 0.83] |
| dV_upper | all | lowo | 51 | 11.8 [8.4, 15.1] | 0.13 [-0.43, 0.49] | 0.16 [-0.35, 0.52] |
| dV_upper | all | holdout_2013-14 | 12 | 9.9 [4.8, 14.0] | 0.20 [-0.69, 0.75] | 0.38 [0.01, 0.78] |
| dV_total_fixed | resolvable | lowo | 48 | 14.6 [11.4, 17.6] | 0.57 [0.31, 0.73] | 0.58 [0.33, 0.73] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 13.2 [6.9, 18.3] | 0.64 [-0.02, 0.85] | 0.65 [0.24, 0.85] |
| dV_total_fixed | all | lowo | 51 | 21.1 [13.8, 29.2] | 0.35 [0.05, 0.61] | 0.36 [0.10, 0.63] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 17.8 [9.5, 24.9] | 0.35 [-0.27, 0.70] | 0.37 [-0.05, 0.73] |
