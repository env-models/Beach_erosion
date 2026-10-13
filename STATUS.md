# STATUS.md — branch `revisit-2026` (session of 2026-10-13, ~22:40 → 00:40)

Autonomous orchestration (owner away). Every decision is logged with its rationale in `reports/DECISIONS.md` (D-1 … D-2x). Per-agent reports: `reports/A_audit.md`, `reports/B_data.md`, `reports/C_models.md`, `reports/D_state_of_the_art.md`, `reports/E_supervisors.md`, `reports/R_review_A.md`; paper material: `paper/outline.md`, `paper/publication_checklist.md`.

## Resume
```bash
git checkout revisit-2026
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -r requirements.lock.txt && uv pip install -e .
pytest -q                                   # 24 tests (A) — expected: all pass
python -m evi.events && python -m evi.events_v2 && python -m evi.reproduce   # regenerate event tables + audit numbers
python -m evi.models.run_all                # Agent C pipeline (see reports/C_models.md "Reproduce")
```
Raw data are not committed; `scripts/download_*.py` fetch them (see `data/README.md`). Processed parquet files ARE committed.

## 1. What got done

| Workstream | State | Key outputs |
|---|---|---|
| Setup | done | branch, `src/` layout, Python 3.12 env + lockfile, thesis text extraction, `.gitignore` |
| A — audit & reproduce | **done** (+ reviewed) | `src/evi/` (11 modules), 24 tests, `data/processed/events_trucvert.{parquet,csv}` (v1, 51 events), `events_trucvert_v2.*` (98 events), `intervals_*`, `*_hat175.*` sensitivity copies, `reports/A_audit.md`, `docs/thesis/thesis_key_sections_en.md` |
| B — data expansion | **done** | Castelle 2020 (OSF, CC0) 325 surveys 2003–2019 → profiles/volumes; RESOURCECODE + Castelle hourly directional waves; SHOM gauges + UTide residuals; Castelle tide; NAO; SHOM RAM datums; `data/README.md`, `reports/B_data.md`, 9 scripts |
| C — modelling | **done** (stages 1–6; PySR not run) | `src/evi/models/`, `figures/`, `reports/C_models.md`, `reports/C_model_cards/` |
| D — state of the art | **done** | 74 entries (72 Crossref-verified), `reports/D_state_of_the_art.md` + `D_references.bib` |
| E — supervisors | **done** | 14/14 seed items verified, ~40 added, lineage resolved, outreach material (EN/FR) in `reports/E_supervisors.md` Part 4 |
| R — independent review of A | **done** | no blocker/major; 10 minor/notes, `reports/R_review_A.md`, `tests/review_time_alignment.py` |
| F — paper package | **done (v1)** | `paper/outline.md` (titles, abstract, sections, figures, journals), `paper/publication_checklist.md` |

## 2. Key results (all computed or verified this session; thesis/paper numbers quoted as such)

**Lineage (E, D).** The 2017 EVI was published as Nicolae Lerma, Bulteau, Muller, Decarsin, **Gillet**, Paris, Biausque, Sénéchal & Castelle (2018), *J. Coastal Research* SI85:666–670, doi:10.2112/SI85-134.1 (open PDF HAL hal-01719953): R² 0.83 / RMSE 7.7 m³/m with pre-storm state, 0.70 / 10.3 without, 39 erosive calibration events 2009–13, 13 validation events 2013–15. BRGM report RP-67418-FR (2019, OCA storm network) cites "Gillet, 2017" but replaced the volume regression by a threshold matrix (wave power 100/200 kW/m, spring tide, dune foot, Stockdon runup) and says linking it to observed erosion was not possible. **The paper is a revisit/audit/extension of a published, co-authored indicator.** No ML event-scale storm-erosion-volume model exists for Truc Vert/Aquitaine (closest: Narrabeen — Simmons & Splinter 2022, Harley 2023, Calcraft 2025; GP template Beuzen 2019).

**Audit (A, confirmed by R).** Notebook numbers reproduced exactly (PPT train R 0.83/RMSE 11.73; test R 0.97/RMSE 8.08, n = 8). 10 of 11 HANDOFF §2.1 issues confirmed (item 3 latent only). New findings: the forcing CSV clock is CET (+1 h fix verified against raw WW3/MARS files); the notebook is not the thesis pipeline (whole-profile ΔV, +3 m threshold, 85/15 split on the 3-hourly series); the 0.97 is an n-weighted mean of two per-group Pearson R with one group of n = 2 — correcting the profile-crossing routine alone flips it to 0.47 (pooled R 0.91–0.94). Removing the erosive-only filter: TPTE train R 0.68 → 0.54; PPT RMSE 11.7 → 19.3.
Clean, leakage-free linear EVI (HAT = 2.14 m, thesis split, no ΔV filter): General ΔV_upper = 7.58E − 2.28, **calibration R² = 0.24** (n = 35; thesis 0.26), validation R² 0.53 [0.07, 0.70] (n = 11, 9 of them in winter 2013–14). Closest analogues of the 2018 paper's validation numbers (erosive-only, secondary): single model R² 0.74 / RMSE 10.1 (paper 0.70 / 10.3); two-model 0.88 / 6.7 (paper 0.83 / 7.7). Energy "units": ΣHs²Δt, Σ(1/16)ρgHs²Δt and the notebook unit are exact rescalings (identical skill); energy flux differs marginally.

**HAT datum (B, A).** SHOM RAM Cap Ferret: ZH = −1.98 m IGN69, PHMA = +2.53 m IGN69, NM = +0.39 m IGN69 ⇒ **HAT = 2.14 m above MSL**, not 1.75 m (HANDOFF double-subtracted the 0.39 m; the thesis's "IGN69" label was wrong). All final tables use 2.14 m. Residual issue (R-F4): the predicted tide at Truc Vert still exceeds 2.14 m in 0.41 % of hours (max +2.45 m) → 0.31 m site/datum mismatch [verify]. TWL ≥ HAT in 27 % (v1) / 21 % (v2) of steps even at 2.14 m, so the "HAT filter" is weak by construction and runup is the dominant uncertainty.

**Data (B).** Castelle 2020 is a superset of the legacy profiles (165/168 dates; RMSE 0.09 m after a 40 m shift); +157 surveys (2003–04, ECORS'08, 2015–19). Event table v2: 98 events / 201 intervals, 2008-02 → 2019-12, window w740, Castelle buoy-corrected hourly waves (Hs95/Hs75 = 3.56/2.04 m on 2009–13 — lower than the legacy node's 4.22/2.37), water level = Castelle tide + Arcachon residual (15 % hours without surge, flagged), `mean_dir` filled (median 289°).

**Models (C).** Protocol as fixed in HANDOFF §3-C: event unit; *resolvable* = interval ≤ 45 d, chosen a priori from survey spacing (v1 48/51 events, v2 91/98); leave-one-winter-out (LOWO, July–June winters); 2013–14 stress test (train ≤ 2012–13); v2 recent hold-out 2015–16 → 2019–20; MSE skill vs climatology and vs the thesis-style PPT; 1000-resample bootstrap CIs (seed 0); antecedent anomaly past-only; never filtered on ΔV. A clean-clone rerun reproduced the v1 table exactly.

LOWO skill vs climatology on resolvable events [95 % CI] (RMSE m³/m):

| model | v1 ΔV_upper (n = 48) | v1 ΔV_total (48) | v2 ΔV_upper (91) | v2 ΔV_total (76) |
|---|---|---|---|---|
| 2017/2018 EVI (linear, HAT-filtered E) | 0.46 [0.24, 0.62], 9.0 | 0.57 [0.35, 0.72], 14.7 | 0.37 [0.06, 0.58], 8.5 | 0.39 [0.10, 0.59], 14.3 |
| Harley-type (ΣHs²Δt, all storm hours) | **0.48** [0.26, 0.63] | **0.63** [0.41, 0.76] | 0.40 | 0.43 |
| Equilibrium B (a·E + c·E·(V − V_eq)) | 0.45 | 0.61 | **0.46** [0.27, 0.63] | **0.51** [0.33, 0.65] |
| ShoreFor-flavoured | 0.32 | 0.32 | 0.44 | 0.46 |
| RF / XGBoost / LightGBM | 0.41 / 0.27 / 0.22 | 0.51 / 0.33 / 0.33 | 0.38 / 0.31 / 0.31 | 0.39 / 0.40 / 0.36 |
| Gaussian process | −0.09 | 0.24 | 0.33 | 0.37 |
| Two-stage ML / hybrid residual | 0.43 / 0.38 | 0.58 / 0.51 | 0.38 / 0.44 | 0.39 / 0.48 |

- Keeping the long intervals destroys the skill (v1 ΔV_upper −0.21 [−1.30, 0.29], n = 51): survey spacing, not the model, is the first-order limit.
- Winter 2013–14 (v1 ΔV_upper, n = 12): EVI skill 0.63 [0.18, 0.83], RMSE 7.6; thesis-style PPT R² 0.56 [0.06, 0.73], RMSE 7.4 — the thesis "0.85 / 7.5" (erosive-only) is not reproduced as an all-events R². On v2 the EVI scores −0.08 [−6.44, 0.76], driven by one event (TV20140131: observed 5.2, predicted 39.7 m³/m); rankings on 2013–14 alone are unstable (lower CI bounds all < 0).
- v2 recent hold-out (2015–16 → 2019–20, n = 38, ΔV_upper): Equilibrium B 0.47 [0.13, 0.75], ShoreFor-flavoured 0.46, EVI 0.38 [0.04, 0.64], LightGBM −0.17.
- Ablations (paired bootstrap of ΔRMSE): continuous vs binary antecedent state — no effect on ΔV_upper, small gain on v1 ΔV_total only; cluster count — no gain (slightly worse in v1, last in SHAP rank); energy flux — not better than ΣHs²Δt; HAT-filtered energy — never helps (worse for v1 ΔV_total); direction (v2) — none; winter NAO — small gain inside LightGBM only; HAT 2.14 vs 1.75 m — negligible; fixed-window total ΔV is more predictable than upper-beach ΔV in v1.
- Intervals: CV+ conformal near nominal (0.92 at 90 %) but wide (34–40 m³/m vs observed SD 12.1); GP posterior over-confident in v1 (0.73 at 90 %), ≈0.86 in v2.
- **Conclusion: nothing beats the 2017/2018 EVI by more than its CI on held-out winters; equilibrium-type models give a small, consistent (v1, v2, v2C) but non-significant gain; tree/GP models never win on LOWO with n ≈ 50–90.** This is the honest "why it doesn't" outcome HANDOFF §0 anticipated, and it is publishable as such.

## 3. What failed or is blocked
- CANDHIS raw buoy data: API key must be requested by email (nobody was contacted). CMEMS IBI and ERA5: no credentials on this machine. WEPA index: bot-check 403 and CC BY-NC-ND (download manually, never commit). No post-2019 Truc Vert topography found openly. OCA LiDAR, Pléiades DEMs, CoastSat, Biscarrosse (EPOC): recorded only.
- Exact thesis coefficients cannot be reproduced: the 2017 code (MATLAB? [verify]) is not in the repo and the 2020 notebook differs in method. Thesis, 2018 paper and clean table disagree on event counts (22 / 39 / 27 erosive) → ask the co-authors.
- Agent A's early directory-level `git add` swept B's and C's files into A-labelled commits (content unchanged; no history rewrite on a shared tree).
- PySR (symbolic regression) not run: first import downloads Julia (network/time). Splinter 2014 and Harley 2009 are "flavoured" stand-ins pending the exact published equations [verify]. SHAP is in-sample. Bootstrap CIs ignore within-winter dependence.
- C's data flags for A: implausible `max_twl_all` (15.6 m MSL in v2 TV20140303; 8.7 / 8.3 m in v1) → runup slope definition (R-F8); Klaus peak Hs 14.23 m is a single-sample spike (Castelle 9.32 m, RESOURCECODE 12.3 m); legacy WW3 node runs 1.5–2.5 m above B's series at storm peaks. A's diagnostic (23:32, `A_audit.md` §2.2 "Runup slope definition"): the v2 15.6 m case is β = 0.324 measured over 3.8 m of a scarped post-2013–14 profile (the +4 m and water-level crossings almost coincide), which flips Stockdon to the non-dissipative branch (R2% 12.8 m); the v1 8.7 m cases come from the inflated legacy waves (Hs 9.1 m, Tp 16.7 s). Alternative tables with a least-squares foreshore slope over 0 to +3 m MSL (cap 0.2, never binding; max β 0.125) are committed as `events_trucvert_slopefix.*` and `events_trucvert_v2_slopefix.*` (+ intervals): max TWL 7.9 m (v1) / 6.7 m (v2); events with TWL > 6 m fall from 12 → 3 (v1) and 9 → 2 (v2); General calibration R² 0.24 → 0.36 but validation R² 0.53 [0.07, 0.70] → 0.60 [0.17, 0.77] (CIs overlap: no demonstrated out-of-sample gain). Default tables untouched (md5 identical). A sensitivity rerun of C on these tables was launched at 23:33 (result: see "Slope sensitivity" in `reports/C_models.md` if it finished).
- Instruction conflict noted by every agent: `~/CLAUDE.md` (a read-only Mac-security-audit brief) says "no network, wait for go-ahead"; it was treated as scoped to that other project because this session's explicit brief required downloads, web lookups and pushes (D-7). Please confirm.

## 4. Prioritised to-do for the next session
1. **Confirm HAT with the co-authors** and the thesis p. 20 wording; resolve the 0.31 m residual (local Truc Vert HAT ≈ 2.45 m vs Cap Ferret RAM) — decides the hydrodynamic-threshold story (R-F4).
2. **Apply reviewer R's minor fixes** in `src/evi`: interval boundary side (F1, `side="right"`), pin the fixed volume window from calibration surveys only (F3), equal-n comparison for the HAT-filter claim (F5), `period` label for 2008 / long-gap flag (F6), `n_storms_whole` + cross-survey cluster id (F9), document slope definition and 50 m de-shoaling depth (F8, F10); make `tests/review_time_alignment.py` pass and rename it `test_*`.
3. **Modelling follow-ups (C):** rerun `run_all` on the `*_slopefix.*` tables if A delivers them; install Julia offline and run PySR; replace the Splinter 2014 / Harley 2009 stand-ins with the exact published forms; block bootstrap by winter; nested-CV hyper-parameter search (only if n grows); out-of-sample SHAP; learning curve; a two-stage classifier with calibrated erosion probability for the OCA bulletin.
4. **Runup sensitivity**: Stockdon 2006 vs Sénéchal 2011 (Truc Vert storm runup) vs Atkinson 2017; the "Nicolae-Lerma 2018" runup form in RP-67418-FR Table 6 [verify] — E's hook #4.
5. **OCA threshold matrix vs observed ΔV** (wave power 100/200 kW/m columns exist in the tables): answers RP-67418-FR Annex 3 directly — E's hook #2.
6. **v2 storm-threshold harmonisation**: Castelle waves run 0.35 m lower than the legacy node; decide whether to use RESOURCECODE or bias-correct, and recompute quantiles; test Hs95/Hs75 sensitivity (D "must-haves").
7. Surge proxy check: Arcachon residual vs legacy MARS2D 2008–14; Boucau as alternative; fill the 2013–14 Arcachon gap.
8. Learning-curve analysis (skill vs n calibration events), as Splinter 2013 / Simmons 2019 suggest.
9. Dune-foot retreat / dune volume as a second response (E's hook #3, connects to Nicolae Lerma's dune work).
10. Paper: pick title/venue with the supervisors; send E Part 4 material (owner's call); ORCID; fix README image paths (HANDOFF item 11); Zenodo release plan (`paper/publication_checklist.md`).

## 5. Git
Branch `revisit-2026`, pushed to `origin`. Local commits are authored as `R Gillet <rgillet@zetaglobal.com>` (pre-existing config; consider `raphael.gillet1@gmail.com` for this repo). Legacy files (`Storm Impact Indicator_2.ipynb`, `datasets/`, `README.md`, `images/`) untouched.
