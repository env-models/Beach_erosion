# Glossary — jargon used across the reports

[← docs index](README.md) · [project README](../README.md)

One line per term, then where it is defined (file and section, or code symbol). Units: ΔV and volumes in m³ per
metre of beach (m³/m); elevations in m above the profile datum (MSL at Truc Vert) unless stated.

## Indicator and thesis models

| term | definition | defined in |
|---|---|---|
| **EVI** | Eroded Volume Indicator: the 2017 linear storm-erosion model ΔV = a·E + b, E = storm energy reaching HAT; published as Nicolae Lerma et al. (2018) | `HANDOFF.md` §1; `reports/E_supervisors.md` headline; model key `evi_general` in `reports/C_models.md` §2 |
| **General model** | EVI fitted on all events, ΔV above HAT (thesis: 10.2E − 3.2, R² 0.26) | `docs/thesis/thesis_key_sections_en.md` "Results"; `reports/A_audit.md` §1 |
| **TPTE** | *Tout le Profil – Tempêtes Érosives*: erosive events only, ΔV over the whole profile (selection on the target, so secondary only) | `HANDOFF.md` §1, §2.1 item 7; `tpte_2stage` in `reports/C_models.md` §2 |
| **PPT** | *Profil Pré-Tempête*: TPTE plus a binary pre-storm state (beach fatter/thinner than the mean profile), one fit per state | `HANDOFF.md` §1; `ppt_all`, `ppt_2stage` in `reports/C_models.md` §2 |
| **EWS** | Early-warning system (forecast hazard 1–3 days ahead) | `reports/D_state_of_the_art.md` Theme 1 glossary |
| **OCA** / **RP-67418-FR** | Observatoire de la Côte de Nouvelle-Aquitaine; its 2019 BRGM report on the operational storm network (wave power 100/200 kW/m threshold matrix) | `reports/E_supervisors.md` §1.1(b) |

## Water levels, waves and datums

| term | definition | defined in |
|---|---|---|
| **HAT / PHMA** | Highest astronomical tide (*plus hautes mers astronomiques*): the morphological and hydrodynamic threshold; **+2.14 m above MSL** at Cap Ferret (SHOM RAM) | `src/evi/constants.py` `HAT_MSL`; `reports/B_data.md` §3b; DECISIONS D-22 |
| **MSL / NM / ZH / IGN69** | Mean sea level (*niveau moyen*), chart datum (*zéro hydrographique*), French land levelling datum; profile datum 0 = +0.39 m IGN69 | `data/README.md` §3a'; `data/processed/events_trucvert_schema.md` "Conventions" |
| **TWL** | Total water level = still water level (tide + surge) + runup R2%; a time step "reaches HAT" when TWL ≥ HAT | `src/evi/features.py` `timestep_features`; schema "Conventions" |
| **R2%** | 2 % exceedance wave runup, Stockdon et al. (2006), from deep-water H0, L0 and the foreshore slope β | `src/evi/runup.py` `stockdon_r2`; `HANDOFF.md` §1 |
| **Hs, Tp, Hs95 / Hs75** | Significant wave height, peak period; storm = run of Hs > Hs75 containing Hs > Hs95 (v1: 4.22 / 2.37 m) | `src/evi/storms.py`; schema "Conventions" |
| **ΣHs²Δt** | Harley et al. (2009)-style storm "energy" in m²·h; the notebook energy and Σ(1/16)ρgHs²Δt are exact rescalings of it | `src/evi/energy.py` `e_hs2dt`; `reports/A_audit.md` §1.2; schema columns `E_Hs2dt_*` |
| **E_notebook / E_dens / E_Pflux** | Energy variants: notebook "MJ/m²" (really 10⁶ J·h·m⁻²), time-integrated energy density, time-integrated energy flux | schema "Columns"; `src/evi/energy.py` |
| **`_storm` / `_stormHAT`** | Column suffixes: summed over all storm samples / only over storm samples with TWL ≥ HAT | schema "Columns" |
| **wave power P** | ρg²Hs²Tp/(64π) in kW/m; OCA thresholds 100 / 200 kW/m | schema columns `max_P_kWm_*`, `hours_P_gt*` |

## Volumes and events

| term | definition | defined in |
|---|---|---|
| **ΔV (sign)** | Volume change between two surveys; **ΔV > 0 = erosion** | schema "Conventions" |
| **dV_upper / dV_lower / dV_total** | Change of sand above the HAT plane / below it / total, over the window covered by both profiles | schema "Columns"; `src/evi/profiles.py` `volume_change` |
| **dV_total_fixed** | Total ΔV over a fixed cross-shore window (v1: 0–139.9 m), comparable across events | schema "Columns" |
| **interval / event** | Interval = pair of consecutive surveys; event = interval with ≥ 1 storm (the modelling unit) | schema top; `src/evi/events.py` |
| **resolvable** | Event with interval ≤ 45 days, chosen a priori from survey spacing (v1 48/51, v2 91/98) | `src/evi/models/protocol.py`; `reports/C_models.md` §1 |
| **winter** | Storm year July–June of the interval midpoint, e.g. `2013-14` | schema "Columns"; `src/evi/events.py` `winter_label` |
| **V_anom_past** | Antecedent state: pre-storm volume minus its mean over the past year (past-only, no leakage) | `src/evi/models/protocol.py` `past_only_anomaly` |
| **berm_volume_pre** | Berm proxy: sand between HAT and +4 m MSL seaward of the dune-toe proxy | schema "Columns"; `src/evi/profiles.py` `berm_volume` |
| **w740 / core300 / w1500** | Alongshore averaging windows of the Castelle DEMs: 740 m (≈ thesis 750 m, used for v2), 280 m core present 2003–2019, 1500 m (from ~2013) | `data/README.md` §1 "Processing" |

## Evaluation

| term | definition | defined in |
|---|---|---|
| **LOWO** | Leave-one-winter-out cross-validation: each winter is predicted by a model trained on all other winters | `src/evi/models/protocol.py` `lowo_splits`; `reports/C_models.md` §1 |
| **hold-out / 2013–14 stress test** | Train on winters ≤ 2012–13, test on 2013–14 (and 2014–15); v2 also has a recent hold-out 2015–16 → 2019–20 | `reports/C_models.md` §1, §4.5 |
| **skill vs climatology** | 1 − MSE/MSE_clim (> 0 beats predicting the training mean); also vs the thesis-style PPT | `reports/C_models.md` §1; `src/evi/models/protocol.py` |
| **bootstrap 95 % CI** | Percentile interval from 1000 resamples of events (seed 0); ignores within-winter dependence | `src/evi/models/protocol.py` `bootstrap_metrics`; `src/evi/metrics.py` |
| **CV+ conformal** | Prediction intervals from inner leave-one-winter-out residuals | `src/evi/models/run_all.py` `conformal_halfwidths`; `reports/C_models.md` §6 |
| **Equilibrium A / B** | ΔV = a·E·(V_pre − V_eq) + b, and B adds a main a·E term (Yates 2009 flavour) | `reports/C_models.md` §2; `src/evi/models/baselines.py` |
| **ShoreFor-flavoured** | ΔV from disequilibrium-weighted wave power (Davidson 2013 form [verify]) | `reports/C_models.md` §2; `baselines.ShoreForFlavour` |
| **SHAP** | Per-feature contribution to a tree model's prediction (here in-sample) | `reports/C_models.md` §7 |
| **GP** | Gaussian-process regression with predictive uncertainty | `src/evi/models/ml.py` `GP` |
| **[verify]** | Tag for anything an agent could not check against a primary source | `HANDOFF.md` §5 |

## Data versions and table suffixes

| label | meaning | defined in |
|---|---|---|
| **v1** | Event table from the legacy repo data (`datasets/`), 51 events / 128 intervals, 2008–2014, 3-hourly WW3 + MARS2D | `data/processed/events_trucvert_schema.md`; `python -m evi.events` |
| **v2** | Agent A's extended table: Castelle 2020 profiles (w740), hourly Castelle waves with direction, tide + Arcachon surge proxy; 98 events / 201 intervals, 2008–2019 | schema "v2" section; `python -m evi.events_v2` |
| **v2C** | Agent C's independent v2 build (core300 window, 128 events, 2003–2019); robustness check only | `reports/C_models.md` §8; `src/evi/models/events_v2.py` |
| **v1s / v2s** | v1 / v2 rebuilt with the slope-fix runup slope (`*_slopefix` tables) | `reports/C_models.md` §8b; `run_all --data v1s\|v2s` |
| **slopefix** | Runup slope β = least-squares slope over 0 to +3 m MSL (cap 0.2) instead of the notebook's slope between water level and +4 m; removes implausible TWL (15.6 m) | `reports/A_audit.md` §2.2 "Runup slope definition"; `src/evi/slopefix.py`; `profiles.foreshore_slope_band` |
| **hat175** | Tables built with the superseded HAT = +1.75 m MSL, kept for sensitivity | schema "Conventions"; `figures/tables/C_hat_sensitivity.csv` |
| **2026-10-13b** | Data version stamp of the HAT = 2.14 m tables | schema title |
