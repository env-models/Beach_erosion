# Paper outline — revisiting the Eroded Volume Indicator (EVI) at Truc Vert

Draft v1, 2026-10-13 (orchestrator / Agent F). Sources: `reports/A_audit.md`, `reports/B_data.md`, `reports/C_models.md`, `reports/D_state_of_the_art.md`, `reports/E_supervisors.md`. Numbers below are from those reports (all computed or verified this session) unless quoted as "thesis:" or "2018 paper:". Placeholders `{{C: …}}` are filled from Agent C's final results in STATUS.md / C_models.md. Anything an agent could not verify keeps its `[verify]` tag.

## 0. Framing decision (changed during this session)
The EVI is **already published**: Nicolae Lerma, Bulteau, Muller, Decarsin, **Gillet**, Paris, Biausque, Sénéchal & Castelle (2018), *Towards the Development of a Storm Erosion EWS for the French Aquitaine Coast*, J. Coastal Research SI 85:666–670, doi:10.2112/SI85-134.1 (open PDF: HAL hal-01719953; verified via Crossref). The operational OCA storm network (BRGM report RP-67418-FR, 2019) cites "Gillet, 2017" but replaced the volume regression by a threshold matrix (wave power 100/200 kW/m, spring high water, dune-foot elevation, Stockdon runup) and states (Annex 3) that linking the indicator to observed erosion was not possible because few surveys bracket single storms.
**Therefore the paper is a *revisit, audit and extension* of a published indicator, co-signed by its original authors, not a first proposal.** This is the strongest possible hook for Nicolae Lerma (the 2018 conclusion explicitly asks for validation on more storms and on storm clusters).

## 1. Working titles
1. *Revisiting the Eroded Volume Indicator: antecedent beach state, storm sequencing and the limits of energy-based storm-erosion prediction at Truc Vert (France)*
2. *From a linear storm-energy indicator to interpretable, uncertainty-aware models: an audited re-analysis of storm erosion at Truc Vert, 2003–2019*
3. *How much storm-driven beach volume change is predictable from wave energy alone? A leakage-free re-evaluation of the Aquitaine Eroded Volume Indicator* (honest-negative-result variant)
4. *Audit, extend, compare: lessons from re-analysing a 2017 storm-erosion indicator with ten more years of data* (short-communication variant for *Géomorphologie* / NHESS brief)

## 2. Abstract draft (~260 words)
Operational storm-erosion warnings on the high-energy, meso-macrotidal Aquitaine coast (SW France) rely on simple forcing indicators, but predicting the eroded volume per storm remains weakly skilful. An *Eroded Volume Indicator* (EVI) was proposed in 2017–2018 for Truc Vert beach: the cumulative wave energy delivered during storm hours whose total water level reached the highest astronomical tide (HAT), regressed linearly on the upper-beach volume change between surveys, with a binary pre-storm beach-state label (2018 paper: R² 0.83, RMSE 7.7 m³/m on 13 erosive validation events). Here we (i) reproduce and audit the original pipeline from the original data (168 profiles 2005–2015; 3-hourly WaveWatch III and MARS2D forcing), confirming 10 of 11 suspected issues (energy units that are not an energy, a +3 m instead of +1.75 m threshold in the 2020 code, a 1-hour clock offset, leakage of the test period into the storm thresholds and the mean profile, selection on the target, and a headline correlation driven by a two-event subgroup) and showing that without filtering on erosion the linear EVI explains about a quarter of calibration variance (R² = 0.23, n = 35; thesis: 0.26); (ii) rebuild a leakage-free event table of 51 storm-containing survey intervals (2008–2014) and extend it to {{A/B: n_v2}} intervals over 2008–2019 using the open Castelle et al. (2020) survey dataset, a directional wave hindcast and tide-gauge residuals; and (iii) compare physics baselines (Harley-type energy fit, Splinter et al. 2014 cluster relation, Yates-type disequilibrium) with interpretable machine-learning models (gradient boosting with SHAP, Gaussian-process regression with prediction intervals, symbolic regression) under a pre-specified protocol: event-level, leave-one-winter-out cross-validation, no filtering on the target, bootstrap 95 % confidence intervals. {{C: headline result sentence with numbers and CIs; 2013–14 winter; which features matter}}. {{C: verdict sentence: do antecedent state and storm sequencing add skill over energy alone, with CI}}. We release the event table, code and download scripts to support the Observatoire de la Côte de Nouvelle-Aquitaine storm network.

## 3. Section plan (target 8,000–10,000 words for ESurf/NHESS; 15–20 pages incl. figures for *Géomorphologie*)
1. **Introduction** — storm-erosion EWS on the Aquitaine coast (OCA, BRGM RP-67418-FR; Ferreira et al. 2026 review lists the 2018 EVI in its Table 1 [verify]); indicator approaches (Safe Corridor Width, SEI, Storm Impact Scale); the 2017/2018 EVI and its stated limits (2018 conclusion: more storms, clusters); 2013–14 winter cluster (Castelle 2015, Masselink 2016); what changed in ten years (open data: Castelle 2020; ML: Narrabeen lineage Simmons & Splinter 2022, Harley 2023, Calcraft 2025; GP intervals Beuzen 2019; ShoreShop 2.0 benchmark culture); objectives.
2. **Study site and data** — Truc Vert; HAT = +2.14 m IGN69 = +1.75 m MSL (datum verification: `B_data.md` "Vertical datums" {{B}}); legacy data (OCA 2005–2015 profiles; WW3 nearest 0.25° node 44.667N −1.5E; MARS2D AQUI250 at 44.641N −1.290E; CSV clock in CET, fixed +1 h); extended data: Castelle et al. 2020 (OSF, CC0, 325 surveys 2003-09 → 2019-12; legacy set is a subset: 165/168 dates present, profile RMSE 0.09 m after a 40 m cross-shore shift), RESOURCECODE WW3 node 94337 (hourly 1994–2025, directional; vs CANDHIS 2014 r = 0.965, bias −0.11 m), Castelle 2020 buoy-corrected waves 2000–2019, Castelle 2020 astronomical tide, SHOM/REFMAR Arcachon-Eyrac residual as surge proxy (UTide), NAO. Blocked/not used: CANDHIS raw (API key by email), CMEMS/ERA5 (credentials), WEPA (manual download, CC BY-NC-ND). Table 1.
3. **The 2017/2018 indicator: reproduction and audit** — method recap; reproduction table (thesis | notebook | exact port | corrected): notebook numbers reproduced exactly (PPT train R 0.83 / RMSE 11.73; test R 0.97 / RMSE 8.08, n = 8); the 0.97 is an n-weighted mean of two per-group Pearson R, one group having n = 2 (R = ±1 by construction) and flips to 0.47 when the profile-crossing routine is corrected; audit table of 11 items with effect on metrics (removing the erosive-only filter: TPTE train R 0.68 → 0.54, PPT RMSE 11.7 → 19.3); thesis vs 2018 paper vs this study disagree (0.85/7.5 "correlation" vs R² 0.83/7.7 vs clean-table numbers) and the original 2017 code is not available → state plainly. Glossary (PHMA = HAT, haut/bas de plage, pied de dune, engraissée, surcote, jet de rive).
4. **Event table and evaluation protocol** — event = survey-to-survey interval with ≥1 storm (Hs > Hs95 = 4.22 m, delimited by Hs75 = 2.37 m, quantiles on 2009-01→2013-12 only); v1: 51 events, 128 intervals, 83 storms, 2008-01 → 2014-11 (38 storm intervals within the thesis window vs thesis 37); v2: {{A: n events 2008–2019}}; features (four named energy variants: ΣHs²Δt, Σ(1/16)ρgHs²Δt, ∫P dt with P = ρg²Hs²Tp/(64π), each over storm hours and over HAT-exceeding storm hours — for a linear model the first three are exact rescalings; HAT-exceedance hours; max TWL; continuous antecedent volume anomaly; berm proxy; intertidal slope; cluster count with 72 h gap; days since last storm; season; direction (v2); NAO; OCA operational wave-power thresholds 100/200 kW/m); targets ΔV_total (fixed 0–139.9 m window) and ΔV_upper (above HAT plane), positive = erosion; resolvability rule for long intervals (307-day interval excluded) {{C}}; leave-one-winter-out + most-recent-winters hold-out; 2013–14 as stress test; metrics RMSE/MAE/R²/bias + skill vs climatology and vs the 2018 EVI, bootstrap 95 % CIs (seeded), n reported; prediction intervals and coverage.
5. **Models** — 2017/2018 EVI variants; Harley-type energy fit; Splinter 2014 cluster relation [verify exact form]; Yates-type disequilibrium; gradient boosting + RF (shallow, regularised, n ≈ 50–100) with SHAP; GP regression; two-stage classifier→regressor; hybrid residual; symbolic regression (PySR) if run. Why no LSTM/CNN (n too small; Gomez-de la Peña 2023 needs thousands of steps).
6. **Results** — 6.1 audit effects; 6.2 skill table with CIs (v1 and v2) {{C}}; 6.3 ablations: continuous vs binary antecedent state, cluster count, energy flux vs Hs²Δt, HAT-filtered vs all storm hours (A: HAT filter did *not* help on v1, R²_cal 0.23 vs 0.31 all-hours ΔV_total; TWL ≥ HAT in 37 % of 3-h steps → datum question), direction (v2) {{C}}; 6.4 2013–14 winter hindcast {{C}}; 6.5 interpretability (SHAP, symbolic law) {{C}}; 6.6 interval coverage {{C}}; 6.7 OCA threshold matrix vs observed ΔV (new, answers RP-67418-FR Annex 3) {{C if done}}.
7. **Discussion** — what controls event-scale predictability at Truc Vert; survey spacing vs storm/recovery aliasing (median gap 16 days in Castelle data; ECORS'08 daily surveys split storms); no bathymetry/bar state; HAT datum and the meaning of a hydrodynamic threshold; comparison with Narrabeen ML work and with Truc Vert equilibrium *shoreline* models (Castelle 2014, D'Anna 2020/21, Azorakos 2024: they predict shoreline, not volume); implications for the OCA bulletin (mapping GP intervals to alert classes, cf. Leaman 2021); small-n honesty.
8. **Conclusions**; 9. **Data and code availability** (Zenodo; OSF CC0; RESOURCECODE CC BY-SA; SHOM Licence Ouverte; no raw redistribution); 10. **CRediT, competing interests, acknowledgements**.

## 4. Figures
| # | Figure | Status / file |
|---|---|---|
| 1 | Method schematic 2017 vs 2026 pipelines | legacy `images/Schema_english.jpg` + new panel ☐ |
| 2 | Event timeline 2008–2014 (v1) and 2003–2019 (v2): surveys, storms, clusters, ΔV | `figures/fig_event_timeline.png` (C, v1) ◐ |
| 3 | Energy vs ΔV, corrected units, all events, coloured by antecedent state | `figures/fig_energy_vs_dV.png` (C) ◐ |
| 4 | Model skill comparison with bootstrap CIs (LOWO + hold-out) | `figures/fig_skill_comparison.png` (C) ◐ |
| 5 | SHAP summary + dependence; symbolic law if any | `figures/fig_shap_summary.png`, `fig_shap_dependence.png` (C) ◐ |
| 6 | Winter 2013–14 hindcast with intervals | `figures/fig_winter_2013_14.png` (C) ◐ |
| 7 | Prediction-interval calibration | `figures/fig_calibration.png` (C) ◐ |
| 8 | Reproduction: the 0.97 artefact (two-point group) and audit ablation steps | from `reports/A_audit.md` §1.1 ☐ |
| S1 | Legacy vs Castelle profile agreement (RMSE 0.09 m) | from `B_data.md` ☐ |

## 5. Tables
1 Data sources (B). 2 Reproduction (A §1). 3 Audit items and effects (A §2). 4 Event-table schema (A). 5 Model skill with CIs and n (C). 6 Ablations (C). 7 Interval coverage (C).

## 6. Journal shortlist and fit rationale
| Journal | Fit | OA / fees | Notes |
|---|---|---|---|
| **Earth Surface Dynamics (Copernicus)** | Strong: data-driven geomorphology, audits and negative results acceptable, public discussion | Gold OA, APC [verify] | Code/data policy strict (good); preprint = discussion paper |
| **NHESS (Copernicus)** | Strong if EWS framing leads; Beuzen 2019 (GP storm erosion) is here | Gold OA, APC [verify] | Public discussion |
| **Géomorphologie: relief, processus, environnement** (GFG, OpenEdition) | Strong social fit: Arnaud-Fassetta's home journal (he is not on the board; co-authors Gautier, Lissak, Suanez are associate editors); FR or EN with bilingual abstracts; 15–20 pages max; IF 0.3 | No APC found; CC BY-SA per Crossref ("diamond" plausible) [verify] | Best for the joint FR/EN version with both supervisors |
| Coastal Engineering (Elsevier) | Good for the modelling/EWS content (Splinter 2014, Nicolae Lerma 2017, Calcraft 2025 are here) | Subscription + green OA / APC | Engineering rigour; ShoreFor/CoSMoS reviewer pool |
| Geomorphology (Elsevier) | Good: Castelle 2015 Truc Vert 2013–14 paper is here | Subscription + green OA | Broad audience |
| JGR: Earth Surface | Good if ML/physics comparison is the core | APC | High novelty bar |
| JGR: Machine Learning and Computation | Niche: interpretable-ML angle (Adusumilli 2024) | APC | Smaller geomorphology audience |
**Recommendation:** ESurf if Agent C's comparison is clean and the v2 table holds up; *Géomorphologie* for the co-supervised FR/EN version or if the result is mainly the audit; NHESS if the EWS/interval mapping leads. Decide with the supervisors (E Part 4 material).

## 7. "What changed since 2017" (honest section)
- **Data**: thesis 102 profiles (2009–13) + 2014–15 → repo 168 (2005–15) → Castelle 2020 superset 325 surveys (2003–19), +157 surveys; waves now hourly and directional (RESOURCECODE, Castelle 2020); surge from SHOM gauge residuals.
- **Units**: "MJ/m²" in 2017/2018 is 1e6 J·h·m⁻²; replaced by named quantities (pure rescaling for linear fits; flux variant tested).
- **Threshold and datum**: 2020 code used +3 m; HAT = +1.75 m MSL; TWL ≥ HAT in 37 % of steps questions the datum {{B}}.
- **Clock**: forcing CSV was in CET; +1 h fix verified against raw WW3/MARS files.
- **Protocol**: 85/15 chronological split + erosion-only filter + full-period mean profile → leave-one-winter-out, no target filtering, past-only antecedent state, bootstrap CIs, prediction intervals.
- **Headline metric**: weighted per-group R (0.97, n = 8, one group n = 2) → pooled R² with CI and n.
- **Models**: one linear fit → physics baselines + interpretable ML + uncertainty {{C}}.
- **Positioning**: first ML, out-of-sample, event-scale storm-erosion-volume benchmark at Truc Vert (none found by Agent D); closest prior work at Narrabeen.

## 8. Open [verify] items that must be closed before submission
- HAT/PHMA datum at Cap Ferret (SHOM RAM) and MARS2D/Castelle tide datum consistency {{B}}.
- Exact form of the Splinter et al. 2014 cluster relation and energy metric (full text).
- Thesis vs 2018 paper event counts (37/22 erosive vs 39 erosive) — ask the co-authors which event set produced 0.83/7.7.
- Berm proxy (+1.75 to +4 m band), 72 h cluster gap, ±1.5 m intertidal band: sensitivity analysis.
- Whether RESOURCECODE `wlv` is tide-only; Arcachon residual as open-coast surge proxy (compare with MARS2D 2008–14).
- Translation of thesis passages (`docs/thesis/thesis_key_sections_en.md`) checked by the author.
