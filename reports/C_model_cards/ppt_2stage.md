# Model card — PPT 2-stage (thesis-style) (`ppt_2stage`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_notebook_stormHAT_MJh_m2 + binary state (training-fold mean volume)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Thesis-style TPTE / PPT downstream of an erosion/accretion classifier.
* **Known failure modes:** Hard classification: a mis-classified erosive event is predicted as the mean accretion; positive bias.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.4 [7.6, 11.1] | 0.38 [0.09, 0.57] | 0.40 [0.15, 0.60] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.4 [5.7, 8.9] | 0.56 [0.06, 0.73] | 0.65 [0.10, 0.83] |
| dV_upper | all | lowo | 51 | 11.6 [8.8, 14.7] | 0.16 [-0.23, 0.44] | 0.19 [-0.16, 0.47] |
| dV_upper | all | holdout_2013-14 | 12 | 8.4 [5.9, 10.4] | 0.44 [-0.12, 0.67] | 0.56 [-0.07, 0.79] |
| dV_total_fixed | resolvable | lowo | 48 | 15.4 [12.2, 18.3] | 0.53 [0.19, 0.69] | 0.53 [0.26, 0.70] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 14.6 [8.3, 19.7] | 0.56 [-0.44, 0.80] | 0.57 [-0.00, 0.83] |
| dV_total_fixed | all | lowo | 51 | 20.7 [13.7, 28.9] | 0.37 [0.05, 0.63] | 0.38 [0.09, 0.65] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 16.5 [9.8, 22.1] | 0.44 [-0.48, 0.70] | 0.46 [-0.11, 0.74] |
