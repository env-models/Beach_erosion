# Model card — ShoreFor-flavoured (phi by train fit) (`shorefor`)

* **Code:** `src/evi/models/baselines.py`; run via `python -m evi.models.run_all`.
* **Inputs:** daily Hs, Tp from datasets/Data_frame.csv → Ω, Ω_eq(φ), P^0.5 ΔΩ summed per interval; φ ∈ {15,30,60,120,240} d
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** none / closed-form least squares; fixed a priori, not tuned on test folds.
* **Seed:** 0 (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** dV = a*F_ero + c*F_acc + b, phi chosen per training fold by in-sample RMSE.
* **Known failure modes:** Designed for shoreline position with continuous forcing; φ chosen in-sample; only 7 years of forcing (spin-up 2008).

## Cross-validated results (data v1; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
| dV_upper | resolvable | lowo | 48 | 10.1 [8.1, 12.0] | 0.29 [-0.07, 0.52] | 0.32 [0.01, 0.53] |
| dV_upper | resolvable | holdout_2013-14 | 12 | 10.5 [5.5, 13.9] | 0.11 [-0.70, 0.50] | 0.29 [0.03, 0.52] |
| dV_upper | all | lowo | 51 | 13.5 [8.9, 18.7] | -0.13 [-1.40, 0.47] | -0.10 [-1.26, 0.49] |
| dV_upper | all | holdout_2013-14 | 12 | 8.5 [4.6, 11.4] | 0.42 [-0.09, 0.68] | 0.55 [0.37, 0.73] |
| dV_total_fixed | resolvable | lowo | 48 | 18.6 [12.9, 24.2] | 0.30 [-0.08, 0.59] | 0.32 [-0.03, 0.60] |
| dV_total_fixed | resolvable | holdout_2013-14 | 12 | 19.3 [10.0, 26.3] | 0.23 [-0.31, 0.47] | 0.25 [0.10, 0.52] |
| dV_total_fixed | all | lowo | 51 | 27.3 [13.6, 38.5] | -0.09 [-0.86, 0.57] | -0.08 [-0.79, 0.58] |
| dV_total_fixed | all | holdout_2013-14 | 12 | 14.5 [6.5, 20.5] | 0.57 [0.13, 0.86] | 0.58 [0.23, 0.87] |
