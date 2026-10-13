# figures/ — model figures and result tables (Agent C)

[← back to the project README](../README.md) · report: [`../reports/C_models.md`](../reports/C_models.md) ·
jargon: [`../docs/GLOSSARY.md`](../docs/GLOSSARY.md)

Every figure is drawn by `src/evi/models/figures.py` (`make_all`, called at the end of
`python -m evi.models.run_all --data <tag>`). Each PNG has a **CSV twin with exactly the plotted data**, so a figure
can be checked or redrawn without refitting any model.

**Suffixes (data version):** none = **v1** (legacy repo data, 51 events, 2008–2014) · `_v2` = Agent A's extended
table (98 events, 2008–2019) · `_v2C` = Agent C's independent v2 build (128 events, 2003–2019, robustness check
only). The slope-fix sensitivity runs (`v1s`, `v2s`) were made with `--no-figs`, so they have tables but no figures.
Sign convention everywhere: **ΔV > 0 = erosion**.

## Figures

| figure (`.png` + `.csv`; also `_v2`, `_v2C`) | what it shows | used in |
|---|---|---|
| [`fig_skill_comparison`](fig_skill_comparison.png) ([csv](fig_skill_comparison.csv)) | Skill vs climatology (1 − MSE/MSE_clim) with 95 % bootstrap CIs for every model, resolvable events, two panels (ΔV upper beach, ΔV total fixed window); blue = leave-one-winter-out, orange = hold-out winter 2013–14 | `C_models.md` §3–4; paper skill figure |
| [`fig_energy_vs_dV`](fig_energy_vs_dV.png) ([csv](fig_energy_vs_dV.csv)) | Scatter of ΣHs²Δt over storm samples with TWL ≥ HAT (m²·h) against ΔV upper / ΔV total, coloured by past-only antecedent state (accreted vs eroded); crosses and labels mark intervals > 45 d | `C_models.md` §3; paper energy-vs-ΔV figure |
| [`fig_shap_summary`](fig_shap_summary.png) ([csv](fig_shap_summary.csv)) | SHAP summary (beeswarm) of a LightGBM fit on ΔV upper beach, all resolvable events (**in-sample** explanation) | `C_models.md` §7 |
| [`fig_shap_dependence`](fig_shap_dependence.png) ([csv](fig_shap_dependence.csv)) | SHAP dependence of the 3 most important features (m³/m per feature value) | `C_models.md` §7 |
| [`fig_winter_2013_14`](fig_winter_2013_14.png) ([csv](fig_winter_2013_14.csv)) | Hold-out winter 2013–14 (trained on winters ≤ 2012–13): cumulative observed ΔV vs EVI General, thesis-style PPT, Equilibrium B and random forest | `C_models.md` §3.4, §4.4 |
| [`fig_calibration`](fig_calibration.png) ([csv](fig_calibration.csv)) | Prediction-interval calibration: nominal vs empirical coverage (LOWO, resolvable) for the GP posterior and CV+ conformal intervals of several models | `C_models.md` §6 |
| [`fig_event_timeline`](fig_event_timeline.png) ([csv](fig_event_timeline.csv)) | Top: Hs time series with the Hs95 storm threshold. Bottom: ΔV upper beach for every survey interval (bar width = interval length; orange = event with ≥ 1 storm, grey = storm-free) | `C_models.md` §1; paper data figure |

The `_v2` and `_v2C` variants are next to each file (e.g. [`fig_skill_comparison_v2.png`](fig_skill_comparison_v2.png),
[`fig_skill_comparison_v2C.png`](fig_skill_comparison_v2C.png)). The method schematic of the paper is the legacy
[`../images/Schema_english.jpg`](../images/Schema_english.jpg).

## `tables/` — every number behind `reports/C_models.md`

Written by `python -m evi.models.run_all --data <tag>` unless stated; `<tag>` ∈ {v1, v2, v2C, v1s, v2s}.

| file pattern | content | written by |
|---|---|---|
| `C_results_<tag>.csv` | One row per model × target × subset × split: n, RMSE, MAE, bias, R², skill vs climatology / interval-scaled climatology / thesis PPT, each with 95 % CI | `run_all.run` |
| `C_pred_<tag>_<target>_<subset>_<split>.csv` | Out-of-fold predictions per event for every model; `<target>` ∈ {dV_upper, dV_total_fixed}, `<subset>` ∈ {resolvable, all}, `<split>` ∈ {lowo, holdout, recent (v2/v2s only)} | `run_all.run` |
| `C_coverage_<tag>.csv` | Empirical coverage and mean width of prediction intervals at each nominal level | `run_all.run` |
| `C_ablations_<tag>.csv` | One-question-at-a-time ablations (antecedent state, clusters, energy flux, HAT filter, …): paired-bootstrap ΔRMSE with CI | `run_all.run_ablations` |
| `C_ablation_target_<tag>.csv` | EVI skill on each target / subset (upper vs total ΔV, resolvable vs all events) | `run_all.run_ablations` |
| `C_datainfo_<tag>.json` | Path, modification time and row count of the input tables (provenance stamp) | `run_all.run` |
| `C_shap_importance_<tag>.csv` | Mean absolute SHAP value per feature (v1, v2, v2C) | `figures.make_all` |
| `C_hat_sensitivity.csv` | Key models on HAT = 2.14 m vs superseded 1.75 m tables | `run_all.hat_sensitivity()` |
| `C_ablation_direction_v2.csv` | Does wave direction or winter NAO add skill (v2)? | `run_all.direction_ablation()` |
| `C_slopefix_comparison.csv` | Side-by-side v1/v2 vs v1s/v2s (runup-slope fix) skill table | assembled by Agent C for `C_models.md` §8b (no generator in `src/`) |
| `C_events_v2C.csv`, `C_intervals_v2C.csv`, `C_events_v2C_meta.txt` | Agent C's own v2C event / interval tables and their thresholds and counts | `python -m evi.models.events_v2` |

Reproduce: `make models` (v1 and v2 with figures, then v1s/v2s without) and `make report` to refresh the tables
pasted into `reports/C_models.md`. Re-running overwrites the committed files; check `git diff`.
