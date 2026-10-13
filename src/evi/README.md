# `evi` — the Python package

[← back to the project README](../../README.md) · tests: `../../tests/` · glossary:
[`../../docs/GLOSSARY.md`](../../docs/GLOSSARY.md)

Clean, notebook-free re-implementation of the 2017 EVI pipeline (Agent A) and the 2026 modelling pipeline
(Agent C, `models/`). Installed editable with `uv pip install -e .` (`pyproject.toml`, `src/` layout). Elevations
are metres above the profile datum (MSL at Truc Vert); sign convention ΔV > 0 = erosion.

## How the modules chain

```
datasets/ (legacy)          data/processed/ (Agent B: Castelle surveys, waves, tide)
      │                                   │
   io.py ──────────────┐          events_v2.py (load_profiles_v2, load_hydro_v2)
                       ▼                  │
  storms.py  runup.py  energy.py  profiles.py
        └──────┬───────┴──────────┘
          features.py  (per-timestep slope, R2%, TWL, HAT exceedance)
               ▼
          events.py  build_intervals / build_events  ──►  data/processed/{events,intervals}_trucvert*.{parquet,csv}
               │                                           ▲
               ├──► slopefix.py (same builders, band slope) ┘  *_slopefix tables
               ▼
          reproduce.py (+ legacy.py notebook port, metrics.py)  ──►  data/processed/reproduction_A.json
               
data/processed/events_* ──► models/protocol.py (load, prepare, splits, metrics)
                                 ▼
             models/baselines.py + models/ml.py  (fit/predict models)
                                 ▼
                     models/run_all.py  ──► figures/tables/C_*.csv ──► models/report.py ──► reports/C_models.md
                                 └──────► models/figures.py ──► figures/fig_*.{png,csv}
```

## Core modules (Agent A)

| module | what it does | public entry points |
|---|---|---|
| `constants.py` | Physical constants and site datums: ρ, g, HAT = +2.14 m MSL (and superseded 1.75), notebook threshold 3 m, Δt = 3 h, de-shoaling depth 50 m, calibration dates | `HAT_MSL`, `HAT_MSL_SUPERSEDED`, `RHO`, `G`, `CALIB_START`, `CALIB_END` |
| `io.py` | Read-only loaders for the legacy `datasets/Data_frame.csv` (with the +1 h clock fix) and `TrucVert_OCA.mat`; exact MATLAB datenum conversion | `load_hydro()`, `load_profiles()`, `Profiles`, `datenum_to_datetime()` |
| `storms.py` | Storm detection: runs of Hs > Hs75 containing Hs > Hs95, thresholds on a given period only; cluster counting; exact port of the notebook's version | `storm_thresholds()`, `detect_storms()`, `count_clusters()`, `storm_mask()`, `detect_storms_notebook()` |
| `runup.py` | Linear de-shoaling to deep water and Stockdon et al. (2006) R2% | `deshoal()`, `stockdon_r2()`, `iribarren()`, `deep_water_wavelength()` |
| `energy.py` | Storm "energy" variants with explicit units: ΣHs²Δt, energy density, energy flux, the notebook quantity | `e_hs2dt()`, `e_density_dt()`, `p_flux_dt()`, `e_notebook()`, `energy_flux()` |
| `profiles.py` | Profile geometry: landward-most crossing, volumes, ΔV split at the HAT plane, berm proxy, intertidal and foreshore slopes | `volume_change()`, `volume()`, `landward_crossing()`, `berm_volume()`, `intertidal_slope()`, `foreshore_slope()`, `foreshore_slope_band()` |
| `features.py` | Per-timestep hydrodynamics: profile in force (no look-ahead), slope β, H0/L0, R2%, TWL, HAT exceedance | `timestep_features()`, `profile_in_force()` |
| `events.py` | Builds the v1 interval and event tables (one row per survey pair; events = ≥ 1 storm) | `build_intervals()`, `build_events()`; **`python -m evi.events`** |
| `events_v2.py` | Same builders on Agent B's data (Castelle w740 profiles, hourly waves with direction, tide + Arcachon surge) | `load_profiles_v2()`, `load_hydro_v2()`; **`python -m evi.events_v2`** |
| `slopefix.py` | Alternative v1/v2 tables with the fixed-band (0 to +3 m) runup slope; default tables untouched | **`python -m evi.slopefix`** |
| `legacy.py` | Faithful, parameterised port of the 2020 notebook; each option switches one audited issue to its fix | `run_notebook(NotebookOptions())`, `ablation()` |
| `metrics.py` | R, R², RMSE, bias and seeded bootstrap CIs | `metrics()`, `bootstrap_ci()` |
| `reproduce.py` | Audit tables: notebook as-is, cumulative ablation of fixes, corrected EVI models, energy variants | `corrected_models()`, `energy_variants()`; **`python -m evi.reproduce`** |

## `models/` (Agent C)

| module | what it does | public entry points |
|---|---|---|
| `protocol.py` | The fixed evaluation protocol: seeds (0), resolvable ≤ 45 d, past-only antecedent anomaly, LOWO and hold-out splits, point and bootstrap metrics, paired ΔRMSE, interval coverage | `load_events()`, `prepare()`, `lowo_splits()`, `holdout_split()`, `bootstrap_metrics()`, `paired_delta_rmse()`, `coverage()` |
| `baselines.py` | Climatologies, 2017 EVI (General, honest PPT, thesis-style TPTE/PPT two-stage), Harley-type, Splinter-flavoured, Equilibrium A/B, ShoreFor-flavoured; every model has `fit(df, ctx)` / `predict(df)` | `baseline_models()`, `OLS`, `Ctx` |
| `ml.py` | Small-n ML with fixed, heavily regularised hyper-parameters: LightGBM, XGBoost, random forest, GP, two-stage ML, hybrid residual | `ml_models()`, `Tree`, `GP`, `TwoStageML`, `HybridResidual` |
| `run_all.py` | Runs every model under the protocol for one data version, ablations, intervals, figures | **`python -m evi.models.run_all --data v1\|v2\|v2C\|v1s\|v2s [--no-figs]`**; `hat_sensitivity()`, `direction_ablation()` |
| `figures.py` | The 7 figure families; each PNG saved with a CSV of the plotted data | `make_all(...)` (called by `run_all`) |
| `report.py` | Replaces the `<!-- AUTO:key -->` blocks of `reports/C_models.md` with tables from `figures/tables/` and rewrites `reports/C_model_cards/` | **`python -m evi.models.report v1 v2 v2C`** |
| `events_v2.py` | Agent C's independent v2C build (core300 window, 2003–2019), robustness check only | **`python -m evi.models.events_v2`** → `figures/tables/C_{events,intervals}_v2C.csv` |

Note: two modules are named `events_v2.py`. `evi.events_v2` (Agent A) builds the official v2 tables in
`data/processed/`; `evi.models.events_v2` (Agent C) builds the v2C robustness tables in `figures/tables/`.

## Tests

`pytest -q` runs the 24 tests in `tests/test_*.py` (runup, energy units, storm detection, volume integration,
datenum conversion, event table, notebook regression). `tests/review_time_alignment.py` is reviewer R's
deliberately failing test for finding F1 (`reports/R_review_A.md`); it is not collected by default
(`python_files = ["test_*.py"]` in `pyproject.toml`) and is run explicitly with
`pytest tests/review_time_alignment.py`.
