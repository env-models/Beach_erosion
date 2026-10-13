# reports/ — index

[← back to the project README](../README.md) · jargon: [`docs/GLOSSARY.md`](../docs/GLOSSARY.md)

One report per workstream of [`HANDOFF.md`](../HANDOFF.md) §3, written by the agent named in its first line, plus
the orchestrator's decision log. Suggested reading order: [`STATUS.md`](../STATUS.md) → [`DECISIONS.md`](DECISIONS.md)
→ A → C → B → E → D → R → session-2 reports (F, S, N, G).

Numbers in reports were computed in the 2026-10-13 session unless marked "thesis:" or "2018 paper:"; anything an
agent could not check is tagged `[verify]`. All "Reproduce" commands assume the repository root and an active venv
(`source .venv/bin/activate`).

## Session 1 (workstreams A–E, review R)

| report | purpose | status | key result (one line) | reproduce |
|---|---|---|---|---|
| [`A_audit.md`](A_audit.md) | Reproduce and audit the 2017/2020 EVI pipeline; HANDOFF §2.1 issue table; clean event tables | done, reviewed by R | Notebook reproduced exactly (PPT test R 0.97, n = 8) but fragile (→ 0.47 after fixing the profile crossing); clean EVI calibration R² 0.24 (n = 35), validation 0.53 [0.07, 0.70] (n = 11) | `make tables audit` (= `python -m evi.events`, `evi.events_v2`, `evi.slopefix`, `evi.reproduce`); `pytest -q` |
| [`B_data.md`](B_data.md) | Find, licence-check, download and harmonise open data (surveys, waves, tides, climate indices) | done | Castelle et al. 2020 (CC0): 325 surveys 2003–2019, a superset of the legacy profiles; HAT = +2.14 m MSL from SHOM RAM; CANDHIS, CMEMS, ERA5 and WEPA blocked | `make download process` (scripts listed in [`../scripts/README.md`](../scripts/README.md)) |
| [`C_models.md`](C_models.md) | Fixed evaluation protocol (event unit, leave-one-winter-out, 2013–14 stress test, bootstrap CIs), baselines, ML, ablations, intervals, SHAP | done (stages 1–6; PySR not run) | No model beats the 2017/2018 EVI beyond its CI; equilibrium-type models give a small, consistent, non-significant gain; trees/GP never win at n ≈ 50–90 | `make models report` (= `python -m evi.models.run_all --data v1\|v2\|v2C\|v1s\|v2s`, `python -m evi.models.report v1 v2 v2C`) |
| [`C_model_cards/`](C_model_cards/) | One card per model (see below) | generated | Description, failure modes and cross-validated results per model (data v1) | `python -m evi.models.report v1 v2 v2C` |
| [`D_state_of_the_art.md`](D_state_of_the_art.md) + [`D_references.bib`](D_references.bib) | Annotated bibliography 2016–2026 in 5 themes (indicators/EWS, clustering, equilibrium models, ML, remote sensing) | complete (first pass) | 74 entries, 72 Crossref-verified; no ML event-scale storm-erosion-volume model exists for Truc Vert/Aquitaine | Crossref/OpenAlex API calls listed in the report's "Reproduce" (network) |
| [`E_supervisors.md`](E_supervisors.md) | Supervisors' recent work, lineage of the 2017 internship, hooks, outreach material (EN/FR) | Parts 1–4 complete | The EVI was published as Nicolae Lerma et al. (2018), JCR SI 85, with Gillet as co-author; BRGM RP-67418-FR (2019) cites Gillet (2017) but dropped the volume regression | `curl` commands in the report's "Reproduce" (network) |
| [`R_review_A.md`](R_review_A.md) | Independent review of Agent A's code, tables and audit | done | No blocker or major error; 10 minor findings/notes (F1–F10) with file:line pointers; tables regenerate byte-identically | `pytest tests/review_time_alignment.py` (fails on purpose: finding F1) |
| [`DECISIONS.md`](DECISIONS.md) | Orchestrator log: every autonomous decision (D-1 …) with time and rationale | living document | Key ones: D-3 legacy files stay in place, D-7 `~/CLAUDE.md` scope, D-22 HAT = 2.14 m, D-30 results frozen | — |

## Session 2 (launched 23:50, DECISIONS D-31)

These reports were being written concurrently with this index; check each file's own status line.

| report | purpose | status | key result (one line) | reproduce |
|---|---|---|---|---|
| [`F_publishing_guide.md`](F_publishing_guide.md) | How to publish as an independent researcher: gates, journal choice, preprint, data/code release (pairs with [`../paper/publication_checklist.md`](../paper/publication_checklist.md)) | done (session 2, fees/policies checked on journal sites 2026-10-13) | Top-3: NHESS (APC €1,800, waiver route, public review) > Coastal Engineering (€0 OA only via Couperin if an affiliated co-author is corresponding) > Géomorphologie (no APC found). Gates: journal AI-use rules, data rights on legacy OCA data, 2018-paper overlap disclosure, no LICENSE file yet | — |
| [`S_sand_physics.md`](S_sand_physics.md) | Sand-physics / process literature: swash, berm, bars, dune erosion, recovery, sediment budget, forcing, process models (72 entries, 71 verified) | done (session 2) | Ranked physics the energy indicator ignores (morphological feedback, tide–storm phasing, within-interval recovery, bar state, infragravity, dune toe, export, direction) + 5 computable physics-informed features; Coco et al. 2014 (Truc Vert, daily surveys) is the key site citation | — |
| [`N_recent_findings.md`](N_recent_findings.md) | 2024–2026 work and overlap check (≥22 overlap rows, 14 method groups, 13 datasets, search strings) | done (session 2, 71 verified) | No Truc Vert/Aquitaine event-volume model exists, but Ibaceta & Harley 2024, Thilakarathne 2024/2025, Waeles 2024 and BRGM RP-73737-FR 2024 cover most building blocks → narrow the novelty to: audited published indicator, macrotidal volume, leave-one-winter-out, calibrated intervals, OCNA index validation; submit by mid-2027 | — |
| [`G_el_nino_risks.md`](G_el_nino_risks.md) | El Niño 2026–27: ENSO state, teleconnection evidence for the Bay of Biscay, global hazards, risk register for Aquitaine | done (session 2, sources checked 2026-10-13) | Strong-to-very-strong El Niño under way (NOAA advisory 8 Oct 2026); no established ENSO link to Bay of Biscay winter storminess (Masselink et al. 2023); WEPA/NAO dominate; ENSO not added as a feature | — |

## `C_model_cards/`

Generated by `python -m evi.models.report` from `figures/tables/C_results_v1.csv` (do not edit by hand). One file
per model key used in `C_models.md` §2:

| card | model |
|---|---|
| [`clim.md`](C_model_cards/clim.md), [`clim_rate.md`](C_model_cards/clim_rate.md) | climatology (training mean) and interval-length-scaled climatology |
| [`evi_general.md`](C_model_cards/evi_general.md) | 2017/2018 EVI General: ΔV = a·E + b, E = notebook energy above HAT |
| [`ppt_all.md`](C_model_cards/ppt_all.md), [`ppt_2stage.md`](C_model_cards/ppt_2stage.md), [`tpte_2stage.md`](C_model_cards/tpte_2stage.md) | thesis PPT/TPTE variants: "honest" all-event PPT, and thesis-style two-stage versions behind an erode/accrete classifier |
| [`harley.md`](C_model_cards/harley.md), [`splinter.md`](C_model_cards/splinter.md) | Harley et al. (2009)-type ΣHs²Δt fit; Splinter-flavoured storm power + cluster term (stand-ins, [verify] published forms) |
| [`eq_a.md`](C_model_cards/eq_a.md), [`eq_b.md`](C_model_cards/eq_b.md), [`shorefor.md`](C_model_cards/shorefor.md) | equilibrium (disequilibrium-weighted energy) models and a ShoreFor-flavoured model |
| [`rf.md`](C_model_cards/rf.md), [`xgb.md`](C_model_cards/xgb.md), [`lgbm.md`](C_model_cards/lgbm.md), [`gp.md`](C_model_cards/gp.md) | random forest, XGBoost, LightGBM (depth-2, fixed hyper-parameters), Gaussian process |
| [`two_stage_ml.md`](C_model_cards/two_stage_ml.md), [`hybrid.md`](C_model_cards/hybrid.md) | logistic P(erode) × two regressors; Equilibrium B + LightGBM on its residuals |

## Related material outside `reports/`

* [`../paper/outline.md`](../paper/outline.md): paper plan built from these reports.
* [`../data/processed/events_trucvert_schema.md`](../data/processed/events_trucvert_schema.md): every column of the event/interval tables.
* [`../docs/thesis/thesis_key_sections_en.md`](../docs/thesis/thesis_key_sections_en.md): English translation of the thesis passages the reports quote.
* [`../figures/README.md`](../figures/README.md): what each figure and result table shows.
