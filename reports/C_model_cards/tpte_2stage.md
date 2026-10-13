# Model card — TPTE 2-stage (thesis-style) (`tpte_2stage`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** E_notebook_stormHAT_MJh_m2 (classifier and erosive regression)
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** Thesis-style TPTE / PPT downstream of an erosion/accretion classifier.
* **Known failure modes:** Same as PPT 2-stage; erosive regression fitted on training dV > 0 only.

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 9.6 [7.9, 11.1] | 0.36 [0.03, 0.54] | 0.38 [0.13, 0.57] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 7.8 [5.6, 10.0] | 0.51 [-0.21, 0.75] | 0.60 [-0.11, 0.83] |
| dV_upper | all | lowo | 51 | 14.0 [10.4, 18.1] | -0.22 [-1.08, 0.19] | -0.18 [-0.96, 0.24] |
| dV_upper | all | holdout_2013-14 | 12 | 9.5 [7.2, 11.4] | 0.28 [-0.24, 0.35] | 0.44 [-0.15, 0.61] |
| dV_total_fixed | resolvable | lowo | 48 | 15.9 [12.7, 19.1] | 0.49 [0.17, 0.65] | 0.50 [0.23, 0.67] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 14.0 [9.2, 18.0] | 0.59 [-0.41, 0.78] | 0.60 [0.04, 0.82] |
| dV_total_fixed | all | lowo | 51 | 24.8 [16.5, 33.4] | 0.09 [-0.24, 0.37] | 0.11 [-0.18, 0.40] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 15.9 [11.0, 20.1] | 0.48 [-0.42, 0.67] | 0.50 [-0.10, 0.74] |
