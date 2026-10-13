# HANDOFF — Revisiting the Eroded Volume Indicator (EVI) with modern ML

**Owner:** Raphaël Gillet (raphael.gillet1@gmail.com)
**Prepared:** 13 Oct 2026
**Audience:** AI coding/research agents working in VS Code on `github.com/env-models/Beach_erosion`
**Source material:** M2 thesis *"Élaboration d'un indicateur hydro-géomorphologique : un outil pour prévoir le risque d'érosion lors de tempêtes sur les plages sableuses aquitaines"* (Gillet, 2017, Master DYNARISK, Univ. Paris Diderot / BRGM), written in French. Put it at `docs/thesis/Memoire_Dynarisk_Gillet.pdf`.

---

## 0. Mission (read this first)

In 2017 Raphaël tried to predict **storm-induced beach erosion volume (m³/m)** at Truc Vert (Gironde, SW France) from the **cumulative wave energy delivered to the upper beach** during storms. The correlation was weak on the raw data and only became strong after aggressive filtering. Nine years on, the goal is to:

1. **Reproduce and audit** the 2017 pipeline honestly.
2. **Extend the data** with open datasets (longer Truc Vert record, buoy and hindcast waves, tide gauges).
3. **Build a better model** using physics baselines first, then ML and hybrid models, with an evaluation protocol that would survive peer review.
4. **Map the 2026 state of the art** and position the work within it.
5. **Produce a paper-ready package**: results, figures and a draft outline. The paper is meant to be co-written with the two former supervisors, so it should be framed with them in mind (see §8).

**End goal: a real, peer-reviewed publication** with Raphaël as first author. He doesn't hold a PhD and doesn't need one, because journals judge the manuscript, not the author's degree. Once the paper is accepted, it will be linked from his portfolio (https://env-models.github.io/Portfolio-Gillet/). Every workstream should optimise for what reviewers and editors require: reproducibility, verified references, honest metrics, and open data and code. See §7.

Success means one of two things. Either we show that a model using antecedent beach state and storm sequencing beats the 2017 linear EVI and the published equilibrium models on held-out winters, or we state clearly why it doesn't, which is also publishable.

---

## 1. The 2017 work in brief (English summary of the thesis)

**Site and data**
- Truc Vert beach, Cap-Ferret. Profiles are **longshore-averaged over 750 m (to 2011), then 1500 m**, with a point every 10 cm, surveyed roughly every 2 weeks and referenced to MSL (0 = +0.39 m IGN69).
- Waves came from the Ifremer **WaveWatch III (ATNE grid, GFS winds)** hindcast, 3-hourly, at the Cap Ferret CANDHIS buoy location (44.6525 N, −1.45 E, about 12 km offshore). Water levels came from **MARS2D** (tide + surge), hourly.
- Calibration ran from 2009 to 2013 (102 profiles, 51 storms, 37 resolvable events). Validation used 2014–2015, including the extreme **2013–14 winter** (Dirk, Hercules/Christina, Petra/Ruth, Andrea, Nadja…). An extrapolation was tried at **Biscarrosse** (4 profiles, high-frequency EPOC surveys by M. Biausque).

**Method**
1. **Storm definition** (after Splinter et al. 2014 and Masselink et al. 2014): a storm occurs when Hs > Hs95% (4.3 m) and is delimited by Hs75% (2.3 m).
2. **Runup**: R2% from Stockdon et al. (2006) via the Iribarren number. Beach slope comes from the current profile, and Hs is de-shoaled to deep water.
3. **Hydrodynamic threshold** (adapted from the *Safe Corridor Width* of Harley et al. 2016): only waves whose total water level (tide + surge + R2%) reaches **HAT** (*PHMA* = +2.14 m IGN69) count. HAT replaced the dune foot because the dune foot can't be picked systematically.
4. **Forcing variable**: E = Σ (1/16) ρ g Hs² Δt, summed over threshold-exceeding storm timesteps between two surveys.
5. **Response variable**: ΔV, the profile volume change between consecutive surveys, first above HAT and then over the whole profile.
6. **Fitting**: linear regression ΔV = a·E + b.

**Results**

| Model | Description | Calib. fit | Validation 2014–15 |
|---|---|---|---|
| General | All events, ΔV above HAT | ΔV = 10.2E − 3.2, R² = 0.26, RMSE 22.4 m³/m | poor (≈0.55 reported in abstract) |
| TPTE | Erosive events only, whole profile | ΔV = 18.7E + 2.1 | "0.61", RMSE 11.9 |
| PPT | TPTE plus a binary pre-storm state (fatter/thinner than the mean profile) | accreted: 20.9E + 2.6 · eroded: 14.9E + 2.7 | **"0.85"**, RMSE 7.5 m³/m, ~25% relative error on big storms |

**Author's own diagnosis of what went wrong** (thesis §III-3-2 and notebook "Discussion"):
- Survey spacing (~2 weeks, sometimes more than 2 months) merges several storms into one event, so storm impact can't be separated from post-storm recovery. The "post-Klaus" storm *accreted* 27 m³/m.
- Sand moves across the HAT boundary (Xynthia eroded the upper beach and fed the lower beach).
- There is **no bathymetry or sandbar information**, although the double-bar system controls where waves break.
- The **berm** matters: its absence before winter 2013–14 explains dune-front retreat.
- Antecedent state was used as a **binary** label and should be continuous.
- **Storm clustering** and sequencing weren't modelled.
- The Hs75% delimitation threshold is too permissive, so energy windows are too long for operational forecasting.
- The model didn't transfer to Biscarrosse, a managed and nourished beach in chronic erosion.
- Shoreline (HAT contour) prediction from energy failed: it predicted 40 m of retreat in winter 2013–14 against roughly 20 m observed.
- Other findings: there is no energy floor below which storms can't erode; every storm above 1.6 "MJ/m²" was erosive; calm-weather recovery runs at about 6 m³/m/month.

---

## 2. Repository inventory (`env-models/Beach_erosion`, last commit Dec 2020)

| Path | Content |
|---|---|
| `Storm Impact Indicator_2.ipynb` | Full 2020 Python port of the method (load → runup → indicator → storm selection → train/test → PPT model) |
| `datasets/Data_frame.csv` | 3-hourly `time` (unix s), `hs`, `tp`, `setup` (**actually the MARS2D still water level, not wave setup**), 2008-01-01 → 2014-12-31, 20,456 rows |
| `datasets/TrucVert_OCA.mat` | `x` (0–350 m, 0.1 m step), `date` (MATLAB datenum), `z` (168 × 3501), **168 profiles from 2005-04-08 to 2015-06-18** |
| `datasets/2010/ww3.2010MM_{hs,fp}.nc` | Raw WW3 monthly fields for 2010 |
| `datasets/Level/2010/*.nc` | MARS levels, March 2010 |
| `datasets/CANDHIS_03302_…2014.csv` | Cap Ferret buoy, Jan–Mar 2014 (h13d, hm0, tp, thetap, …) |
| `datasets/netbook.ipynb`, `folder_test/` | Scratch |
| `images/` | Method schematics. `Model_Resume` is an empty file |

### 2.1 Known issues to check during the audit (found during handoff prep, not yet verified by running)
1. **Energy units.** The code uses `(1/16)·ρ·g·Hs²·3` with Δt in *hours*, so the values labelled "MJ/m²" are really J·h·m⁻² ×10⁻⁶. The thesis equation writes ρgHs²Δt without the 1/16. Neither is an energy in J/m². Pick one physically named quantity and report it properly: Σ Hs²Δt (m²·h, as in Harley et al. 2009), time-integrated energy density, or **wave energy flux** P = ρg²Hs²Tp/(64π) integrated over time (J/m). Test all three as features.
2. **Threshold mismatch.** The notebook uses `beta = 3` (m above MSL) as the morphological threshold. HAT is +2.14 m IGN69, about **+1.75 m** in the MSL-referenced profiles. Reconcile this and document which one produced the thesis figures.
3. **Index misalignment risk.** `ELE = ELE[~isnull]` drops NaNs but `DIST = x` is not filtered. This is only safe if NaNs are trailing. Profiles have 1,400 to 2,980 valid points.
4. **`find_nearest` on non-monotonic profiles** (bars, berm) can return the wrong crossing. Use the landward-most crossing explicitly.
5. **Time conversion fudge**: `X*86400 + epoch − 365.242*86400 − 155491` is a magic offset. Replace it with a proper datenum conversion: `datetime.fromordinal(int(d)) + timedelta(d%1) − timedelta(366)`.
6. **Volume integration** runs up to `end` = the first NaN of the *mean* profile. A changing survey extent can alias into ΔV. Use a fixed common cross-shore window per comparison, or require both profiles to cover it.
7. **Selection on the target.** Dropping events with ΔV < 0 ("erosive-only" in TPTE/PPT) conditions on the dependent variable and inflates R. A paper can't use it as the headline metric. Keep it only as a secondary analysis, with a separate erosion/accretion classifier in front.
8. **Leakage.** The mean profile used for the "fat vs eroded" label is computed over the whole period, test included, and storm start/stop indices are computed on the full Hs series.
9. **Tiny test set.** The 85/15 chronological split leaves about 8 events. The notebook prints `R = 0.97` on test, while the thesis reports 0.85, and it is ambiguous whether those are **R or R²**. Bootstrap CIs are needed.
10. **Runup formula typo in the thesis.** The text gives the dissipative case as 0.016√(H₀L₀). That is Stockdon's *setup* term; R2% is 0.043√(H₀L₀). The code is correct.
11. The README links images from a different account (`Raph9989/Beach_erosion`). Fix the paths.

---

## 3. Workstreams and agent roles

Run A and D in parallel from day one. B depends on A's audited loader. C depends on A and B. E is independent. F comes last.

### Agent A — Reproduce and audit (baseline)
- Create a clean package (`src/evi/`) that reproduces the General, TPTE and PPT models from the repo data **without** the notebook's hidden state.
- Fix or flag every item in §2.1 and write `reports/A_audit.md` with a table of each issue, its fix, and its effect on the metrics.
- Report thesis numbers next to reproduced numbers. Where they don't match, explain why.
- Output a tidy **event table** (`data/processed/events_trucvert.parquet`). Columns: survey_start, survey_end, n_storms, storm durations, E variants, peak Hs, mean Tp, mean direction (if available), hours of HAT exceedance, max TWL, pre-storm volumes (total / above HAT / below HAT), berm volume, intertidal slope, ΔV (total / upper / lower), days since last storm, season.

### Agent B — Data expansion
Find, download (respecting licences), and harmonise the sources below. **Verify every source exists and note its licence and DOI before use.** The list was compiled during handoff and is not guaranteed.
- **Truc Vert long-term topography**: Castelle et al. (2020) *Scientific Data*, "16 years of topographic surveys of rip-channelled high-energy meso-macrotidal sandy beach" (2003–2019, 3D DGPS surveys roughly monthly, with higher frequency in storms). This could roughly double the number of events and add 2015–2019. Check for any post-2019 updates (SNO DYNALIT / OCA).
- **Waves**: CANDHIS buoy 03302 Cap Ferret (candhis.cerema.fr). Ifremer WW3 hindcasts (HOMERE / RESOURCECODE, Bay of Biscay). ERA5 waves. Copernicus Marine IBI wave reanalysis. Get **direction** as well; the 2017 work had none.
- **Water levels**: SHOM/REFMAR tide gauges (Arcachon-Eyrac, Socoa/Boucau) and SHOM predicted tide for decomposing surge.
- **Shorelines and DEMs**: CoastSat satellite-derived shorelines (Vos et al. 2019), Observatoire de la Côte de Nouvelle-Aquitaine LiDAR (dune/beach DEMs), and Pléiades DEMs (Burvingt et al. 2025).
- **Climate indices**: NAO and WEPA (West Europe Pressure Anomaly, Castelle et al. 2017), used to explain winter-scale variance.
- **Biscarrosse** (EPOC, Biausque) as an out-of-site test.
- Deliverables: `data/README.md` (provenance, licence, DOI, processing) and xarray/parquet outputs under `data/processed/`.

### Agent C — Modelling (physics-first, then ML)
**Evaluation protocol (fixed before modelling):**
- The unit is the **event**: one survey-to-survey interval containing at least one storm.
- Cross-validation is **leave-one-winter-out**, plus a final hold-out of the most recent winters. Report 2013–14 separately, as both a stress test and a headline case.
- Never filter on ΔV. If erosion-only results are shown, they sit downstream of a classifier and are clearly labelled.
- Metrics: RMSE, MAE, R², bias, Brier skill vs (i) climatology and (ii) the thesis PPT model, with **bootstrap 95% CIs**. Report n.
- Predict **uncertainty** (intervals) as well as point values, because an early-warning system needs it.

**Baselines (implement first):**
1. The 2017 EVI variants (from A).
2. Harley et al. (2009)-style empirical storm-energy vs erosion fit.
3. **Splinter et al. (2014)** storm-cluster cumulative erosion relationship.
4. Equilibrium shoreline/volume models: Yates et al. (2009) and **ShoreFor** (Davidson et al. 2013; Splinter et al. 2014). These capture the "beach state vs forcing disequilibrium" idea the thesis approximated with the mean profile.
5. Optional process reference: XBeach or a Larson et al. (2004)-type dune-impact model on 2–3 storms.

**ML / hybrid (small-n friendly first):**
- Gradient-boosted trees and random forests on the event table, with SHAP for interpretation. Candidate features: continuous antecedent volume anomaly, berm volume, slope, energy variants, HAT-exceedance hours, cluster count, inter-storm gap, season, direction, NAO/WEPA.
- **Gaussian processes / Bayesian regression** for calibrated uncertainty with small n (cf. Beuzen et al. 2019, NHESS 19:2295).
- **Symbolic regression** (e.g., PySR) to recover a compact, physically interpretable law. This is the natural "successor equation" to ΔV = aE + b.
- **Hybrid residual learning**: physics/equilibrium model plus ML on the residuals, or physics-informed ML (cf. Holzenthal et al., Coastal Dynamics 2025).
- Sequence models (LSTM/CNN, cf. Gomez-de la Peña et al. 2023 ESurf) **only if** the expanded dataset supports them. Otherwise document why they were not used.
- Two-stage model: classifier (erode / accrete) followed by a regressor, which addresses the "post-Klaus" problem.
- Ablations should answer the thesis's open questions one at a time: does a continuous antecedent state beat the binary one? Does clustering matter? Does direction matter? Is energy flux better than Hs²?
- Deliverables: `reports/C_models.md`, model cards, and figures under `figures/`.

### Agent D — State of the art, 2016–2026
Produce `reports/D_state_of_the_art.md`, an annotated bibliography of 30–60 entries grouped by theme. Each entry gives the citation, DOI, one-paragraph relevance, and **verified: yes/no**. The themes are:
1. Storm erosion indicators and EWS (MICORE successors, SCW, SEI, COSI, Storm Impact Scale updates).
2. Storm clustering and recovery: Truc Vert / Aquitaine 2013–14 literature (Castelle, Masselink, Burvingt, Nicolae Lerma) and recent clustering papers.
3. Equilibrium and hybrid shoreline models: ShoreFor, CoSMoS-COAST, and **ShoreShop 2.0** (blind benchmark of 34 models, Communications Earth & Environment, 2025; USGS news 5 Aug 2025, where ML models did well and CoSMoS-COAST narrowly won).
4. ML for coastal morphodynamics: CNN/LSTM shoreline prediction (Gomez-de la Peña 2023; Adusumilli et al. 2024 JGR-MLC); Bayesian/GP storm erosion (Beuzen 2019); explainable AI for post-storm recovery; mixture-of-experts shoreline modelling in storm-dominated systems (Coastal Engineering, 2025); physics-informed ML (Coastal Dynamics 2025).
5. Remote sensing that unlocks data: CoastSat, satellite-derived bathymetry (Lubac et al. 2022), Pléiades DEMs, video monitoring.

Rules: no citation goes into the paper unless it is verified against the publisher or DOI. Prefer open-access PDFs. Note anything that already does what we plan to do.

### Agent E — Supervisors' recent work (for science and reconnection)
Produce `reports/E_supervisors.md`: recent output, current themes, and **specific hooks** connecting each person to this project. Seed list (compiled 13 Oct 2026, verify all):

**Alexandre NICOLAE LERMA** (internship supervisor), BRGM Nouvelle-Aquitaine (Pessac). Works on coastal geomorphology, wave hydrodynamics and sea-level rise, and is a core figure of the Observatoire de la Côte de Nouvelle-Aquitaine.
- Recent work is a strong shift to **coastal dune dynamics**:
  - Nicolae Lerma et al., "From Fixed to Transgressive Dunes, the Conditions and Timing of the Transition Along the Aquitaine Coast, France", *Coastal Dynamics 2025* (Springer, 2026), with Burvingt, Ayache, Robin, Rosebery and Castelle.
  - "Multi-annual evolution of coastal dunes: Transition from fixed to transgressive dunes state", *Catena* (2026). He is listed on the HAL record; confirm the authors.
  - Burvingt, Castelle, Marieu, Lubac, Nicolae Lerma, Robin (2025), "Using Pleiades Satellite Imagery to Monitor Multi-Annual Coastal Dune Morphological Changes", *Remote Sensing* 17(9):1522, doi:10.3390/rs17091522.
  - Lecacheux et al. (2024), Arcachon lagoon coastal-flood crisis atlas, *LHB Hydroscience Journal*, doi:10.1080/27678490.2024.2325692.
  - Nicolae-Lerma et al. (2022), "Decadal beach-dune profile monitoring along a 230-km high-energy sandy coast: Aquitaine", *Applied Geography* 139:102645.
  - Laporte-Fauret et al. (2022), *Geomorphology* 414 (foredune blowouts).
  - Lubac et al. (2022), *Remote Sensing* 14:2350 (satellite-derived bathymetry).
  - He co-supervises a BRGM/Univ. Bordeaux PhD with Bruno Castelle on guided foredune remobilisation.
- **Direct lineage to check:** his ResearchGate lists *"Towards the Development of a Storm Erosion EWS for the French Aquitaine Coast"* and BRGM report RP-67418-FR (2019, *réseau tempêtes de l'OCA*). Find out whether these build on the 2017 EVI internship. This is the most important hook.
- His landmark runup paper (Nicolae Lerma et al. 2017, *Coastal Engineering* 123:29–41, setup/runup on a barred beach) can replace Stockdon in our TWL estimate.

**Gilles ARNAUD-FASSETTA** (university tutor), Professor of hydrogeomorphology and geoarchaeology, Université Paris Cité, UMR 8586 PRODIG. He led the DYNARISK master. His publication list is at gilles-arnaud-fassetta.org.
- His focus is fluvial floods and sediment cascades. Recent items:
  - (2026) "When geomorphological field data and systemic analysis help refine the uncertainties of numerical hydrometeorological models in extreme values: the Oct 2018 Aude flood", *Géomorphologie: relief, processus, environnement* 32(1).
  - (2026) Réunion Island 2024–25 flood risk, *Géomorphologie* 32(4).
  - Gautier et al. (2026), Loire and the "hungry rivers" concept, *Geomorphology* 511:110415.
  - Fort et al. (2025), Kagbeni flood (Nepal), *Géomorphologie* 31(4).
  - Fort, Bétard & Arnaud-Fassetta (2025), *Géomorphologie dynamique et environnement*, 2nd ed., Armand Colin.
- **Hook:** his 2026 Aude paper is about *field geomorphology constraining model uncertainty under extremes*. That is close to our framing: observed profiles constraining a data-driven erosion model under extreme storms. *Géomorphologie: relief, processus, environnement* (French/English, his home journal) is a natural venue for a version co-authored with him.

Also list likely co-author or reviewer names that recur (Castelle, Burvingt, Sénéchal, Robin, Bulteau, Mallet) and their recent ML-relevant work.

### Agent F — Paper package
- `paper/outline.md` with working title options:
  - *"Antecedent beach state and storm sequencing control storm-erosion predictability: revisiting an energy-based indicator at Truc Vert with interpretable machine learning"*
  - *"From a linear storm-energy indicator to hybrid ML: a decade of storm-erosion prediction on the Aquitaine coast"*
- Figures: method schematic, event table summary, energy-vs-ΔV (2017 vs corrected units), model skill comparison with CIs, SHAP / symbolic-regression law, 2013–14 winter hindcast, and Biscarrosse transfer.
- Candidate journals: *Coastal Engineering*, *Geomorphology*, *NHESS*, *Earth Surface Dynamics*, *JGR: Earth Surface*, *JGR: Machine Learning and Computation*, *Géomorphologie: relief, processus, environnement*. Write a one-line fit rationale for each.
- An honest "what changed since 2017" section: data length, units fix, protocol fix, models.

---

## 4. Suggested repo layout & conventions

```
Beach_erosion/
  HANDOFF.md            ← this file (can also be copied to AGENTS.md / CLAUDE.md)
  docs/thesis/          ← Memoire_Dynarisk_Gillet.pdf (+ an English translation of key sections, Agent A)
  legacy/               ← move original notebook + data here, untouched
  src/evi/              ← io.py, storms.py, runup.py, energy.py, profiles.py, features.py, models/
  data/raw/ data/processed/ data/README.md
  notebooks/            ← numbered, thin, call src/
  reports/              ← A_audit, B_data, C_models, D_state_of_the_art, E_supervisors
  figures/ paper/
  tests/                ← unit tests for runup, energy units, storm detection, volume integration
```
- Python 3.11+, `uv` or `pip` with a lockfile; numpy, pandas, xarray, scipy, scikit-learn, xgboost/lightgbm, shap, PySR, GPyTorch or scikit-learn GP, matplotlib.
- Seed every random process. Each report ends with a "reproduce" command.
- Work on branches and open PRs. Never rewrite `legacy/`.

## 5. Guardrails
- **No fabricated references or numbers.** Unverified items are tagged `[verify]`.
- The thesis is in French. Translate quoted passages and keep French technical terms in a glossary: PHMA = HAT; *haut/bas de plage* = upper/lower beach; *pied de dune* = dune toe; *engraissée* = accreted/"fat"; *surcote* = surge; *jet de rive* = swash.
- Respect data licences (SHOM, CANDHIS, OCA, Copernicus). Don't commit large raw data; script the downloads.
- Do **not** contact anyone. Outreach is Raphaël's call; Agent E only prepares material.
- Small-n reality: about 37 events in 2017, maybe 80–120 with extended data. Prefer simple and interpretable models, and say so.

## 6. Definition of done
- [ ] `A_audit.md`: reproduction table, every issue in §2.1 resolved or explained
- [ ] Event table v1 (repo data) and v2 (extended data)
- [ ] `B_data.md` with verified sources, licences and DOIs
- [ ] Baselines and at least 3 ML/hybrid models under the fixed protocol, with CIs
- [ ] `D_state_of_the_art.md` with ≥30 verified entries
- [ ] `E_supervisors.md` with verified recent publications and hooks
- [ ] `paper/outline.md` and draft figures

## 7. Publication path (independent researcher → accepted paper → portfolio)
Agent F owns this checklist.
- [ ] **Author identity**: Raphaël needs an ORCID iD and an affiliation line. Use "Independent researcher, [city], France" unless a supervisor's lab offers an associate affiliation; ask, don't assume. Use the CRediT contributor roles statement.
- [ ] **Venue choice**: shortlist 3 journals from §3-F. For each, check scope, APC/fees (prefer diamond/no-fee open access, or a subscription journal with green OA), the open-data policy, and typical review time. Copernicus journals (NHESS, ESurf) have **public open discussion**, which is good visibility for an independent author. *Géomorphologie: relief, processus, environnement* is diamond OA.
- [ ] **Preprint** on EarthArXiv or ESS Open Archive at submission, if the journal allows it. This gives a citable DOI immediately, which can go on the portfolio before acceptance.
- [ ] **Code and data release**: tag a GitHub release and archive it on **Zenodo** (DOI). Include the event table, scripts and environment lockfile. Respect third-party data licences by providing download scripts instead of redistributing.
- [ ] **Co-authors**: draft an authorship proposal and a one-page project summary for each supervisor, for Raphaël to send himself. Agree contributions before submission.
- [ ] **Submission pack**: cover letter, highlights, graphical abstract, data/code availability statement, competing interests, suggested reviewers (no close collaborators).
- [ ] **Response-to-reviewers template**.
- [ ] **On acceptance**: add the publication to the portfolio (`env-models/Portfolio-Gillet` repo: citation, DOI badge, link to the Zenodo code/data, one-paragraph plain-language summary and a key figure). Prepare that portfolio entry as a PR ready to merge.

## 8. Context for framing
This is a personal project with a social aim as well as a scientific one: reconnect with the two supervisors around a credible new result and aim for a joint publication. The work should be something both would recognise and want to sign. That means respect the BRGM/OCA operational lineage (early warning for local authorities) and the hydrogeomorphological framing of PRODIG/DYNARISK, and be scrupulously honest about the 2017 limitations.
