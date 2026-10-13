# Publication checklist (HANDOFF §7) — owner: Raphaël Gillet

Status key: ☐ not started · ◐ prepared/draft · ☑ done. Prepared 2026-10-13 by the orchestrator (Agent F). Nothing here has been sent to anyone.

## 1. Author identity
- ☐ Create an **ORCID iD** (https://orcid.org, free). Add it to the portfolio.
- ☐ Affiliation line: default *"Independent researcher, [city], France"*. Only use a BRGM / Université Paris Cité associate affiliation if a supervisor explicitly offers it (ask, don't assume).
- ◐ CRediT roles draft (see `reports/E_supervisors.md` Part 4 once delivered): RG — Conceptualization, Methodology, Software, Formal analysis, Data curation, Writing – original draft, Visualization. Supervisors — Supervision (2017), Resources (OCA/BRGM data), Validation, Writing – review & editing. Castelle/OCA data providers — Resources, Data curation (if they join).

## 2. Venue choice (3-journal shortlist, see `paper/outline.md` §Journals)
- ☐ Confirm scope + APC + OA policy + open-data policy + median review time for each of the 3 shortlisted journals on the journal website (figures in outline.md are from memory and tagged [verify]).
- ☐ Decide: Copernicus (ESurf / NHESS, public discussion, APC) vs *Géomorphologie: relief, processus, environnement* (diamond OA, no APC, co-supervisor's home journal) vs Elsevier *Coastal Engineering* / *Geomorphology* (subscription + green OA).

## 3. Preprint
- ☐ EarthArXiv (https://eartharxiv.org) or ESS Open Archive at submission; check the chosen journal's preprint policy (Copernicus journals *are* the preprint via the discussion paper).

## 4. Code and data release
- ☐ Tag a GitHub release of `env-models/Beach_erosion` (branch `revisit-2026` merged) and archive on **Zenodo** (GitHub–Zenodo integration gives a DOI).
- ☐ Release contents: `src/evi/`, `tests/`, `scripts/download_*.py`, `data/processed/events_trucvert*.parquet` (derived event table — check OCA/Castelle 2020 licence allows derived products), `requirements.lock.txt`, `figures/`.
- ☐ Third-party raw data are NOT redistributed; download scripts + `data/README.md` instead.
- ☐ Fix README image paths (currently point at `Raph9989/Beach_erosion`, HANDOFF §2.1 item 11).

## 5. Co-authors
- ◐ One-page project summary (EN/FR) and authorship proposal: drafted by Agent E in `reports/E_supervisors.md` Part 4 — Raphaël sends it himself.
- ☐ Agree contributions and author order before submission. Proposed: Gillet (first), Nicolae Lerma, Arnaud-Fassetta (+ data providers if they contribute).

## 6. Submission pack
- ☐ Cover letter (1 page: question, result, why this journal).
- ☐ Highlights (3–5 bullets, ≤85 chars each, if the journal asks).
- ☐ Graphical abstract (reuse method schematic + skill figure).
- ☐ Data & code availability statement (Zenodo DOI, OCA licence, CANDHIS/SHOM/Ifremer terms).
- ☐ Competing interests: none.
- ☐ Suggested reviewers: 3–5 names NOT close collaborators of the co-authors (candidates in `reports/E_supervisors.md` Part 3 with the "likely reviewer" flag).

## 7. Response-to-reviewers template
- ☐ Table: reviewer comment | response | change made (page/line). Keep a running "anticipated objections" list from `reports/D_state_of_the_art.md` ("methodological must-haves").

## 8. On acceptance
- ☐ Portfolio PR in `env-models/Portfolio-Gillet`: citation, DOI badge, Zenodo link, plain-language paragraph, key figure.
