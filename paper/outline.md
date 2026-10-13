# Paper outline — EVI revisited (draft v0, 2026-10-13, orchestrator / Agent F)

> Status: skeleton written while Wave 1 agents run; placeholders `{{...}}` are filled from `reports/A_audit.md`, `reports/C_models.md`, `reports/D_state_of_the_art.md`, `reports/E_supervisors.md` at the end of the session. Nothing in this file is a verified result until the placeholder is replaced. Numbers quoted as "thesis:" come from Gillet (2017).

## 1. Working titles (pick one)
1. *Antecedent beach state and storm sequencing control storm-erosion predictability: revisiting an energy-based indicator at Truc Vert with interpretable machine learning*
2. *From a linear storm-energy indicator to hybrid ML: a decade of storm-erosion prediction on the Aquitaine coast*
3. *How much of storm-driven beach volume change is predictable from wave energy alone? An audited, extended re-analysis at Truc Vert (France)* — honest-negative-result variant.
4. *Re-analysing a 2017 storm-erosion indicator for the Aquitaine coast: units, leakage, and what interpretable models add* — audit-forward variant, fits *Géomorphologie* / NHESS "brief communication".

## 2. Abstract draft (≈250 words; numbers are placeholders)
Storm-driven beach erosion on the high-energy, meso-macrotidal Aquitaine coast (SW France) is monitored operationally, but simple predictors of eroded volume per storm remain weakly skilful. In 2017 an *Eroded Volume Indicator* (EVI) was proposed for Truc Vert beach: the cumulative wave energy delivered during storm hours whose total water level reached the highest astronomical tide (HAT) was regressed linearly against the upper-beach volume change between surveys. Its reported skill (thesis: R² 0.26 → 0.85) depended on erosion-only filtering and on a binary antecedent-state label. Here we (i) audit and reproduce the 2017 pipeline from the original data (168 profiles 2005–2015; 3-hourly WW3 hindcast and MARS2D water levels), correcting {{A: n}} issues including energy units, the HAT threshold, index alignment and leakage; (ii) rebuild an event table of {{A: n_events}} storm-containing survey intervals ({{B: extended to n with Castelle et al. 2020, 2003–2019}}); and (iii) compare physics baselines (Harley-type energy fit, Splinter et al. 2014 cluster relation, equilibrium volume model) with interpretable machine-learning models (gradient boosting with SHAP, Gaussian-process regression, symbolic regression) under a fixed, leakage-free protocol: event-level, leave-one-winter-out cross-validation, no filtering on the target, bootstrap 95 % confidence intervals. {{C: headline sentence: best model, RMSE/R² with CI vs 2017 PPT and vs climatology; whether continuous antecedent state and cluster count add skill; 2013–14 winter hindcast}}. {{C/D: one sentence on direction/energy-flux ablation}}. The results {{support / do not support}} the hypothesis that antecedent beach state and storm sequencing, rather than cumulative energy alone, control storm-erosion predictability at this site, and provide an open, reproducible event table and code base for the Observatoire de la Côte de Nouvelle-Aquitaine storm network.

## 3. Section plan
1. **Introduction** (1.5 p) — storm erosion EWS need on the Aquitaine coast (OCA, BRGM lineage); indicator approaches (SCW, SEI, Storm Impact Scale); the 2017 EVI and its known weaknesses; the 2013–14 winter cluster; what modern data + ML add; objectives (audit, extend, compare, position). Cite: HANDOFF §3-D themes 1–2; `D_state_of_the_art.md` top picks.
2. **Study site and data** (1.5 p) — Truc Vert (double-bar, meso-macrotidal, HAT +2.14 m IGN69); legacy data (OCA profiles 2005–2015, WW3/MARS2D 2008–2014); extended data (Castelle et al. 2020 surveys 2003–2019; CANDHIS / hindcast waves with direction; SHOM tide gauge; NAO/WEPA) — `B_data.md`. Table 1: data sources, periods, licences, DOIs.
3. **The 2017 indicator: reproduction and audit** (2 p) — method recap (storm definition Hs95/Hs75, Stockdon R2 %, HAT threshold, E = Σ…, ΔV); reproduction table (thesis vs notebook vs clean reimplementation); audit table of the 11 issues (HANDOFF §2.1) with their effect on metrics; glossary (PHMA = HAT, etc.). Key message: the 0.85 is R, on erosion-only events, on ~8 test events; corrected skill is {{A}}.
4. **Event table and evaluation protocol** (1 p) — event definition, features (energy variants, HAT-exceedance hours, TWL, antecedent volumes continuous, berm proxy, slope, cluster count, inter-storm gap, season, direction, climate indices), targets (ΔV total/upper/lower), leave-one-winter-out + recent-winter hold-out, 2013–14 as stress test, metrics + bootstrap CIs, baselines (climatology, 2017 PPT, Harley 2009, Splinter 2014, equilibrium).
5. **Models** (1 p) — baselines; gradient boosting + SHAP; GP regression (calibrated intervals); symbolic regression (PySR) as "successor equation"; two-stage classify-then-regress; hybrid residual learning. Why no sequence models (small n).
6. **Results** (3 p) — 6.1 reproduction and audit effects; 6.2 skill comparison with CIs (Table 2, Fig. 4); 6.3 ablations answering the 2017 open questions (continuous vs binary antecedent state; clustering; direction; energy flux vs Hs²); 6.4 2013–14 winter hindcast; 6.5 interpretability (SHAP, symbolic law); 6.6 uncertainty calibration; 6.7 Biscarrosse transfer (if data).
7. **Discussion** (2 p) — what controls predictability at Truc Vert; survey-spacing limit (storm vs recovery aliasing); missing bathymetry/bars; implications for OCA/BRGM EWS; comparison with ShoreShop 2.0 and equilibrium-model literature; limits of n ≈ {{n}}; honest statement if ML does not beat baselines.
8. **Conclusions** (0.5 p).
9. **Data and code availability** — Zenodo DOI, download scripts, licences.
10. **Author contributions (CRediT), competing interests, acknowledgements** (OCA, BRGM, Castelle et al. data, SHOM, CANDHIS, Ifremer).

## 4. Figure list
| # | Figure | Source | Status |
|---|---|---|---|
| 1 | Method schematic (2017 vs 2026 pipeline, side by side) | `images/Schema_english.jpg` (legacy) + new panel | ☐ |
| 2 | Event table summary: timeline of surveys, storms, clusters, ΔV, 2005–2015 (and 2003–2019 if B delivers) | `figures/` (C) | ☐ |
| 3 | Energy vs ΔV: 2017 units vs corrected units, all events (no filtering), coloured by antecedent state | `figures/` (A/C) | ☐ |
| 4 | Model skill comparison with bootstrap 95 % CIs (RMSE, R², Brier skill vs climatology and vs PPT), leave-one-winter-out | `figures/` (C) | ☐ |
| 5 | SHAP summary + symbolic-regression law | `figures/` (C) | ☐ |
| 6 | Winter 2013–14 hindcast: observed vs predicted ΔV per event with intervals | `figures/` (C) | ☐ |
| 7 | Biscarrosse transfer (only if data) | — | ☐ |
| S1 | Audit: effect of each fix on the reproduction metrics | `reports/A_audit.md` | ☐ |

## 5. Tables
1. Data sources (period, resolution, licence, DOI). 2. Reproduction table (thesis / notebook / clean). 3. Audit items and effects. 4. Model skill with CIs and n. 5. Ablations.

## 6. Journal shortlist and fit rationale
| Journal | Fit | OA / fees | Notes |
|---|---|---|---|
| **Earth Surface Dynamics (ESurf, Copernicus)** | Strong: data-driven geomorphology, methods audits welcome, open discussion gives visibility to an independent author | Gold OA, APC (Copernicus page charges; waivers exist) [verify current rate] | Preprint = discussion paper; code/data policy strict (good for us) |
| **NHESS (Copernicus)** | Strong if framed as EWS / risk indicator for storm erosion | Gold OA, APC [verify] | Beuzen et al. 2019 (GP storm erosion) is here; public discussion |
| **Géomorphologie: relief, processus, environnement** | Strong social fit: Arnaud-Fassetta's home journal, French/English, hydrogeomorphological framing; diamond OA | No APC | Smaller audience; good for a FR/EN version with both supervisors |
| Coastal Engineering (Elsevier) | Good for the modelling/EWS content; Nicolae Lerma 2017 and Splinter 2014 are here | Subscription + green OA or APC | Expects engineering rigour; reviewers from the ShoreFor/CoSMoS community |
| Geomorphology (Elsevier) | Good: Castelle 2015 Truc Vert 2013–14 paper is here | Subscription + green OA | Broad audience |
| JGR: Earth Surface (AGU) | Good if the ML/physics comparison is the core | APC | High bar on novelty |
| JGR: Machine Learning and Computation (AGU) | Niche fit for the interpretable-ML angle (Adusumilli 2024) | APC | Newer journal; less geomorphology audience |

**Recommendation (to be confirmed with supervisors):** ESurf as primary target if the result is a clean model comparison; *Géomorphologie* if the result is mainly an audit + modest skill gain and the aim is the joint FR/EN publication; NHESS if the EWS framing dominates.

## 7. "What changed since 2017" (honest section)
- **Data length**: thesis 102 profiles 2009–2013 (+2014–15 validation) → repo 168 profiles 2005–2015 → {{B: Castelle 2020, 2003–2019, n surveys}}.
- **Units**: notebook "MJ/m²" = (1/16)ρgHs²·Δt[h]/1e6 (not an energy); replaced by named quantities (ΣHs²Δt, time-integrated energy density, energy flux ∫P dt) — `A_audit.md` item 1.
- **Threshold**: beta = 3 m MSL in code vs HAT = +1.75 m MSL — `A_audit.md` item 2.
- **Protocol**: 85/15 chronological split with erosion-only filtering and full-period mean profile → leave-one-winter-out, no filtering on the target, bootstrap CIs, antecedent state from past-only data.
- **Models**: single linear fit → physics baselines + interpretable ML + uncertainty.
- **Direction and clustering**: absent → included {{B/C}}.
