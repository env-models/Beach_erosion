# F — Publishing guide: from this repository to an accepted paper

**For:** Raphaël Gillet (independent researcher, first author). **Written by:** Agent P (publishing path), 13 Oct 2026, branch `revisit-2026`.
**Inputs read:** `HANDOFF.md` §0, §3-F, §7, §8; `STATUS.md`; `paper/outline.md`; `paper/publication_checklist.md`; `reports/E_supervisors.md` (§2.2 on *Géomorphologie*, Part 4 on authorship).

**Verification rule used here.** Every fee, policy or number comes from the journal's or publisher's own site, with the URL and the date checked (all checks were on **2026-10-13**, between 23:46 and 00:30 CEST). Some publisher sites (Elsevier/ScienceDirect journal pages, Springer, MDPI, AGU, Wiley Online Library, COPE) returned **HTTP 403 to automated fetching**. Where a figure was only visible through a search-engine index of the publisher's own page, it is marked **[verify live]**: it probably holds, but you should open the page in a browser before relying on it. Anything I could not check at all is marked **[verify]**. Impact factors from third-party aggregators were left out on purpose. Timelines marked "planning estimate" are my own judgement and are **not** journal statistics.

> **Instruction-conflict note (same as STATUS §3, D-7).** `~/CLAUDE.md` is a read-only, no-network brief for a Mac security audit. As every other agent did, I treated it as scoped to that other project, because this task explicitly required web verification. I only *read* public web pages: nothing was submitted, nobody was contacted, nothing was pushed.

---

## 0. The short version

1. **Top choice: NHESS (Copernicus).** Coastal hazards and early-warning systems are named in its scope. Review is public, with a 6-week open discussion. APC is **€1,800 net** (list price), or €1,620 for EGU members. If you are the corresponding author and have no funds, you can apply at registration for a **discretionary waiver**: "authors without research funds" is a stated priority criterion.
2. **Second: *Coastal Engineering* (Elsevier).** It has the highest prestige in the field. Publishing as a subscription (non-OA) article costs **€0**. Gold OA costs **USD 4,040 / EUR 3,680** (excluding tax), and that APC becomes **€0** if a co-author at a participating French institution is the **corresponding author** under the Couperin–Elsevier 2024–2027 agreement.
3. **Third: *Géomorphologie : relief, processus, environnement*.** No APC was found, it is bilingual, and it sits in the supervisor's network. The costs are low visibility (IF 0.3, per the supervisor's site) and extra work (a ~7,000-character abridged version in the other language).
4. **The five biggest gates:** (i) the **AI-use rules**: Copernicus says *"Generative AI must not be used for text or interpretations"*, so you must write the manuscript yourself and declare the AI-assisted code/analysis; (ii) **co-author consent and the corresponding-author role**, which decides who pays the APC; (iii) **open science issues still unresolved in the repo** (HAT datum, event-count mismatch, reviewer R's minor fixes, block bootstrap by winter); (iv) **data redistribution rights**: the OCA legacy profiles behind event table v1 have no known licence, and RESOURCECODE's CC BY-SA would make any derived column share-alike; (v) **framing against the 2018 paper**, which needs explicit disclosure, no recycled text and no reused figures.

---

## 1. Gates against publishing, and how to clear each

### (a) Novelty and duplication vs Nicolae Lerma et al. (2018)

**Risk.** Editors run similarity checks (iThenticate/Crossref Similarity Check). A paper that "revisits" a published indicator using some of the same 2009–2015 events and the same author group may look like duplicate or redundant publication if the overlap is not declared.

**Rules.**
- COPE's *Text recycling guidelines* (with BioMed Central) tell editors to weigh how much text is reused, where it appears, whether the source is acknowledged, and copyright. Overlap in a **methods** section that cites the original "may be entirely appropriate", but undisclosed overlap, or overlap in **results, discussion or conclusions**, "is unlikely to be acceptable". Source: https://publicationethics.org/guidance/guideline/text-recycling-guidelines (the page returned 403 to direct fetch; content checked through the COPE PDF excerpt indexed by search, 2026-10-13) **[verify live]**.
- **Copyright on the 2018 figures.** The 2018 paper is published by CERF/BioOne. Do **not** reuse its figures. Redraw everything from the data (the repo already does). Re-using a figure would need written permission from CERF [verify].

**How to clear it.**
1. In the abstract, introduction and cover letter, say plainly that the paper is a **re-analysis and extension of the indicator published in Nicolae Lerma et al. (2018)**, and that three of its authors are on the new paper.
2. Write every sentence fresh, the methods recap included. Cite 2018 for the original method rather than paraphrasing it closely.
3. State what is new, in numbers: 325 surveys 2003–2019 (vs 39 + 13 events in 2018), a leakage-free leave-one-winter-out protocol, bootstrap CIs, corrected energy units/datum/clock, and model comparison. `paper/outline.md` §7 is the template.
4. Report the 2018 numbers (R² 0.83 / RMSE 7.7 m³/m) as the **published baseline**, and the closest re-computation (0.88 / 6.7, erosive-only, secondary) as *reproduction*, not as a new result.
5. Cite the 2017 M2 thesis as an unpublished report. If it is on HAL/DUMAS [verify], cite it with that ID. A master's thesis is not prior publication.
6. Upload the 2018 PDF (HAL hal-01719953) as a "related manuscript" if the submission system asks for one. Copernicus and Elsevier both ask about related work at submission [verify the field name].

### (b) Co-author consent and authorship disputes

**Rules.** ICMJE requires all four criteria for authorship: (1) substantial contribution to conception/design or to data acquisition/analysis/interpretation; (2) drafting the work or critically revising it; (3) final approval; (4) agreement to be accountable. "Contributors who meet fewer than all 4 … should not be listed as authors", and they go in the Acknowledgements, with **written permission from each acknowledged person**. Source: https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html (checked 2026-10-13). CRediT (14 contributor roles) is described at https://credit.niso.org/ (HTTP 200, 2026-10-13).

**How to clear it.**
1. Send the one-page summary (E Part 4, EN/FR) and **ask, don't assume**. Get a written "yes" from each co-author by email, with the proposed author order, corresponding author and affiliation line.
2. Agree on the **corresponding author** at this point. It decides who can use institutional APC agreements (§3).
3. **Co-authors need something to do.** Each one must at least critically revise the draft and approve the final version. Send a near-final draft and leave a deadline of at least 3 weeks.
4. **If a supervisor declines:** thank them, offer an acknowledgement (with their written permission), and go ahead as sole author or with the remaining co-authors. You may **not** use non-public data that only they provided (OCA legacy profiles in `datasets/`) without permission. The v2 analysis on Castelle 2020 (CC0) plus open forcing can stand alone (STATUS §2: 98 events, 2008–2019). Keep the v1 reproduction as "described in the 2018 paper", using published numbers only.
5. **If someone asks to be added late or wants a different order:** use the CRediT table as the neutral basis. COPE has flowcharts for authorship disputes (https://publicationethics.org, [verify the specific flowchart URL]).
6. **Data providers (Castelle/EPOC).** The CC0 licence asks for no authorship. Offer co-authorship only if they actually contribute (interpretation, revision). Otherwise acknowledge them and cite the dataset.

### (c) Data licences: what you may redistribute, and how to attribute it

| Source | Licence (verified where) | Can the derived event table be redistributed? | Attribution required |
|---|---|---|---|
| Castelle et al. 2020 Truc Vert surveys, OSF `jftw8` | **CC0 1.0 Universal**, re-checked via `api.osf.io/v2/nodes/jftw8/?embed=license` on 2026-10-13 | **Yes**, with no conditions | None legally required. Cite the paper (doi:10.1038/s41597-020-00750-5) and the OSF DOI 10.17605/OSF.IO/JFTW8 anyway (scientific norm). |
| Castelle 2020 wave and tide files (same OSF node) | CC0 (same node) | Yes | Same as above |
| RESOURCECODE WW3 hindcast (Ifremer Sextant, doi:10.12770/d089a801-…) | Agent B read **"CC BY-SA 4.0"** on the Sextant record on 2026-10-13. The record *also* says "Copyright". The Sextant API returned HTTP 500 when I re-checked → **[verify the dual wording]** | **Yes, but share-alike.** Under CC BY-SA 4.0 §3(b), if you share *Adapted Material* you must license it under BY-SA. Under §4, a database that includes a *substantial part* of the licensed database is Adapted Material (legal code read at https://creativecommons.org/licenses/by-sa/4.0/legalcode.en, 2026-10-13). Per-event sums of Hs² are arguably facts, not a substantial extraction, but **the safe choice is to license any table containing RESOURCECODE-derived columns as CC BY-SA 4.0** | Name RESOURCECODE/Ifremer, give the DOI, and link to the licence. |
| SHOM/REFMAR tide gauges (Arcachon, Boucau, Socoa) and SHOM RAM datums | **Licence Ouverte 2.0** (RAM on data.gouv.fr, per B; REFMAR "presumed" per `data/README.md` → **[verify REFMAR]**) | **Yes.** LO 2.0 states it is compatible with CC BY and ODC-BY (licence text, https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf, read 2026-10-13) | LO 2.0 requires you to "mentionner la paternité … sa source (au moins le nom du Concédant) et la date de dernière mise à jour". Example: "SHOM, REFMAR, data downloaded on 2026-10-13". |
| CANDHIS buoy 03302 (Cerema) | Etalab Licence Ouverte 2.0 (per `doc/01_Utilisation.fr.pdf`, B) | Yes (only a 2014 sample is in the repo) | "Candhis/Cerema" + date |
| OCA legacy profiles and forcing (`datasets/TrucVert_OCA.mat`, `Data_frame.csv`, WW3/MARS2D extractions from BRGM) | **Unknown.** They were obtained during the 2017 internship. The repo has been public since 2020 | **Not without permission.** v1 tables (`events_trucvert*.parquet`) are derived from them → **ask BRGM/OCA in writing**. Until then, release only v2 (open data) | As OCA/BRGM require [verify] |
| NOAA CPC NAO index | presumed US public domain (`data/README.md`) **[verify CPC wording]** | Yes, if public domain | Cite NOAA CPC |
| WEPA index (Scott et al.) | **CC BY-NC-ND 4.0** (B) | **No.** A reformatted or derived copy is questionable under ND. Do not redistribute it; give a download script | Cite the DOI |

**Practical rule for the Zenodo release.** (1) Code under a permissive licence (MIT or BSD-3). There is **no LICENSE file in the repo yet**, so add one. (2) `events_trucvert_v2.*` under **CC BY-SA 4.0** if any column comes from RESOURCECODE, otherwise CC BY 4.0. The provenance of `mean_dir` in v2 is the column to check: A noted it was NaN in the legacy data and filled by B. (3) v1 tables only after OCA/BRGM permission. (4) Raw third-party files are never committed; ship `scripts/download_*.py` instead (already the case).

### (d) Negative or modest results: who welcomes them?

The honest result is: nothing beats the linear EVI beyond its CI; equilibrium-type models give a small consistent gain; survey spacing is the binding limit. None of the journals checked says in its scope that it **explicitly** welcomes negative results:
- ESurf aims & scope: "prioritizes studies with general implications for Earth surface science" (https://www.earth-surface-dynamics.net/about/aims_and_scope.html, 2026-10-13). Negative results are not mentioned.
- NHESS aims & scope: names "sea, ocean, and coastal hazards" and "early warning systems". Localised case studies must show broader implications (https://www.natural-hazards-and-earth-system-sciences.net/about/aims_and_scope.html, 2026-10-13). Negative results are not mentioned.
- The others: [verify] (most of their pages were blocked).

**How to clear it.** Frame the result as a **positive finding about predictability limits**, not as "our ML failed". That is: (1) a quantified skill ceiling for event-scale volume prediction from wave energy at a well-surveyed site; (2) survey spacing identified as the first-order limit (EVI skill vs climatology on v1 ΔV_upper drops from 0.46 [0.24, 0.62] on resolvable events to −0.21 [−1.30, 0.29] when the 57–307-day intervals are kept; `reports/C_models.md` §3.3); (3) a benchmark protocol and open event table that others can beat. Put "why the simple model is hard to beat" in the title (outline title 3 is the right register). Copernicus's public discussion actually helps here: a constructive community comment on a well-argued negative result counts in your favour.

### (e) Statistical rigour: what reviewers will expect with n ≈ 50–90

Typical objections to small-n ML papers, each with the answer that is already in the repo (or still missing):

| Likely objection | Status / answer |
|---|---|
| "Data leakage / temporal leakage." | LOWO by July–June winters, past-only antecedent state, no ΔV filtering (STATUS §2). Write this as a pre-specified protocol section. |
| "Hyper-parameters tuned on the test folds." | Pre-fixed shallow models. Nested CV only "if n grows" → state explicitly that there is no tuning on held-out folds. |
| "Bootstrap CIs ignore within-winter dependence." | **Open** (STATUS §3). Implement a **block bootstrap by winter** before submission. Reviewers will ask. |
| "Multiple comparisons: 10 models × 4 targets." | Pre-declare the primary comparison (EVI vs Equilibrium B on v2 ΔV_upper, LOWO). Report the rest as secondary. Use paired bootstrap of ΔRMSE (already done for ablations). |
| "SHAP in-sample is not evidence." | **Open**: compute out-of-fold SHAP, or present SHAP as descriptive only. |
| "The 2013–14 result hinges on one event." | Already documented (TV20140131). Report it with and without that event. |
| "Why not deep learning?" | n too small. Cite Gomez-de la Peña 2023 (needs thousands of steps), as in outline §5. |
| "Is the threshold / datum choice post hoc?" | HAT 2.14 m from SHOM RAM, with 1.75 m kept as sensitivity. The 0.31 m residual (R-F4) is **open**. Confirm with co-authors. |
| "Event-count mismatch with 2018 (22/39/27)." | **Open**: ask the co-authors which event set produced 0.83/7.7. |
| "Learning curve?" | **Open**: STATUS §4 item 8. A short learning-curve figure pre-empts "more data would help ML". |
| "Stand-in model forms (Splinter 2014, Harley 2009 'flavoured')." | **Open**: replace them with the exact published equations, or rename them honestly as "Splinter-type". |

**Pre-registration.** It isn't required anywhere I checked. You can make the protocol *verifiable* by tagging the commit that fixed it (the protocol was fixed in HANDOFF §3-C before modelling) and citing that tag in the Methods.

### (f) Affiliation, independent-researcher status, ORCID

- **No journal page I could read requires an institutional email.** Two concrete constraints did turn up:
  - *Géomorphologie* asks the corresponding author for postal address, email and **"un numéro de téléphone professionnel"**, not a personal one (https://journals.openedition.org/geomorphologie/701, 2026-10-13). An independent author can use a professional/business number. Otherwise it is one more reason to make a supervisor the corresponding author there.
  - **EarthArXiv** requires the submitter to be a listed author with an **ORCID** profile that "must include educational history and current or recent work affiliations", and "the ORCID email address must match the submittor's email address" (https://eartharxiv.github.io/moderation.html, 2026-10-13).
- **ORCID mandatory?** It is mandatory for EarthArXiv submitters (above). For Copernicus, Elsevier, Wiley and AGU **[verify]**: in practice most of these submission systems now ask for an ORCID. Create one now (free, https://orcid.org/register, HTTP 200 checked) and add the 2018 JCR paper to it.
- **Affiliation line:** "Independent Researcher, [city], France" is accepted practice. The default is still to ask whether a co-author lab offers an associate affiliation (HANDOFF §7). That changes nothing in the science, but it could change APC coverage **only if you become the corresponding author under that affiliation**, which requires the institution to treat you as affiliated [verify with the library].
- **Evidence that independent researchers publish in each journal:** I did not find authoritative evidence for any of them in this session → **[verify]**. Searching each journal's site for "Independent researcher" in affiliations is a 10-minute job.

### (g) Language and editing

- *Géomorphologie*: French-speaking authors **must have their English revised by a native English speaker**, and every article needs an extended abridged version (~7,000 characters with spaces) in the other language (https://journals.openedition.org/geomorphologie/701, 2026-10-13).
- Copernicus journals: copy-editing and typesetting are part of production. Whether that includes substantive language editing is **[verify]**.
- **Costs of commercial editing services:** not verified this session → **[verify]**. Get two written quotes (per-word pricing for ~8,000–10,000 words) before deciding. A free alternative: ask a co-author to do the English revision pass, and note it in CRediT as "Writing – review & editing".
- **AI tools and language.** Copernicus allows assistive grammar and spelling use without declaration. Anything beyond that is "generative" and must be declared, and *"Generative AI must not be used for text or interpretations"* (https://www.earth-surface-dynamics.net/policies/ai_policy.html, 2026-10-13). Elsevier requires a **separate AI declaration statement** naming the tool, its purpose and the extent of oversight. Grammar/spelling checks are exempt, but "substantive changes to sentence structure or organization" must be disclosed (https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals, 2026-10-13). **The consequence for this project:** the repository's reports were drafted by AI agents. The manuscript text and the interpretations must be **written by you and the co-authors**. The AI-assisted code and analysis must be declared in Methods/Acknowledgements (template in §5).

### (h) Desk rejection: typical reasons and how to avoid them

Copernicus publishes its desk-rejection counts ("rejected prior to discussion"), taken from the journal statistics pages, 2026-10-13:
- ESurf 2025: 70 submissions, 15 rejected before discussion (~21 %), 91.8 % approval after discussion (https://www.earth-surface-dynamics.net/about/journal_statistics.html).
- NHESS 2025: 535 submissions, 143 rejected before discussion (~27 %), 89.5 % approval after discussion (https://www.natural-hazards-and-earth-system-sciences.net/about/journal_statistics.html).

The main lesson: **in Copernicus journals the big filter is the access review.** Once a paper is in discussion, about 90 % are eventually published.

Avoid these reasons:
1. **Scope mismatch.** Use the journal's own scope words in the cover letter: "coastal hazards" and "early warning systems" for NHESS, "general implications for Earth surface science" for ESurf.
2. **Local case study with no general message.** Lead with the general finding: survey spacing bounds the predictability of event-scale volume change, plus a transferable protocol.
3. **Missing Data/Code availability section.** It is mandatory at Copernicus: "Authors are required to provide a statement on how their underlying research data can be accessed", in a final section titled "Data availability" (https://www.earth-surface-dynamics.net/policies/data_policy.html, 2026-10-13). Have the Zenodo DOI ready *before* submission.
4. **Length and format.** *Géomorphologie* allows 15–20 pages including figures. Longer needs the board's approval. ESurf Letters must be under 2,500 words. ESurf research articles have no stated limit.
5. **Language quality** (see g).
6. **Over-claiming.** Don't write "ML improves prediction" when the CIs overlap.
7. **AI-policy breach** (see g). Certifying falsely at registration is an ethics issue, not a formality.

### (i) Ethics and competing-interests statements
- There are no human/animal subjects. State "not applicable" where asked.
- **Competing interests:** declare co-authors' employment at BRGM (the operator of the OCA indicator being evaluated). It is not a financial conflict, but it is a relevant interest. Template in §5.
- **Editor conflicts at *Géomorphologie*:** several associate editors (Gautier, Lissak, Suanez) are recent co-authors of Arnaud-Fassetta (E §2.2). Ask in the cover letter that the manuscript be handled by an editor without recent collaboration with any author.
- **Suggested reviewers:** exclude everyone in E's co-author table and their recent co-authors, i.e. anyone who co-authored with any of you in the last 3–5 years. Check this in Crossref/OpenAlex.

### (j) Preprint policy conflicts
- **Copernicus (ESurf/NHESS):** the **discussion paper is itself a citable preprint**: it "appears as a preprint and is citable with a digital object identifier (DOI)" during a 6-week open discussion on EGUsphere (interactive review pages, 2026-10-13). → **Do not also post to EarthArXiv.** It is redundant, and Copernicus's stance on prior external preprints is [verify]. Important: a manuscript **rejected after discussion** stays publicly visible as a discussion paper with its reviews [verify exact wording]. Treat the discussion version as public from day one.
- **Elsevier (Coastal Engineering, Geomorphology, Marine Geology, OCM):** "Authors can share their preprint anywhere at any time". **Exception:** "Some society-owned titles and journals that operate double-anonymized peer review have different preprint policies — please check the journals' Guide for Authors" (https://www.elsevier.com/about/policies-and-standards/sharing, 2026-10-13). Whether *Coastal Engineering* uses double-anonymised review is **[verify]** in its Guide for Authors.
- ***Géomorphologie*:** review is **double-blind** ("évaluation en double aveugle", at least two external referees; https://journals.openedition.org/geomorphologie/32, 2026-10-13). A public preprint with your names on it undermines the anonymity → **ask the editor before posting a preprint** [verify their policy].
- **EarthArXiv:** accepts preprints under review, which must say "non-peer reviewed preprint submitted to EarthArXiv" and name the journal. Embargoed postprints are refused. Assigns a DOI. English only, single PDF (https://eartharxiv.github.io/moderation.html; https://eartharxiv.org/repository/about/, 2026-10-13).
- Wiley (ESPL), AGU, Springer, MDPI, Frontiers preprint policies: **[verify]**.

### (k) Reproducibility requirements
- **Copernicus:** a Data availability section is **mandatory**. Data should be in "reliable (public) data repositories" with DOIs. Code is "encouraged" to be deposited with a persistent identifier. "Data needed to replicate figures should in any case be public" (data policy page above). A **Code availability** section with a Zenodo DOI is the norm.
- **Elsevier, Wiley, AGU, Springer, MDPI, Frontiers:** **[verify]** per Guide for Authors. AGU is known for a strict data policy [verify].
- **What to ship** (all of it already exists except the licence, CITATION.cff and the DOI):
  1. a GitHub release tag, e.g. `v1.0-submitted`;
  2. Zenodo archiving through the GitHub integration (GitHub docs: https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content, HTTP 200);
  3. `LICENSE` (code) + `data/processed/LICENSE` (table);
  4. `CITATION.cff` (format: https://citation-file-format.github.io/, HTTP 200);
  5. `requirements.lock.txt`;
  6. `pytest` passing;
  7. one command that regenerates every figure and table (`python -m evi.models.run_all`).
- **Software citation:** cite the key packages (scikit-learn, XGBoost, LightGBM, SHAP, UTide, PySR if it is used) with their papers/DOIs in the reference list. Copernicus and AGU expect this [verify AGU].

### (l) Time: from submission to publication
- **Copernicus (verified process steps, 2026-10-13):** access review → **6-week public discussion** → final author response within **4 weeks (ESurf)** / **6 weeks (NHESS)** → revised manuscript → editor decision (possibly re-review) → production. **Median durations: not published on the metrics page → [verify]**. *Planning estimate:* 6–10 months submission → final publication, with a citable DOI ~1 month after submission.
- **Elsevier / Wiley / Springer / AGU:** journal "insights" pages were blocked (403) → **[verify]**. *Planning estimate:* 1–3 months to first decision, 6–12 months to publication.
- ***Géomorphologie*:** no statistics found → **[verify]**. It is quarterly, so expect issue-based delays. *Planning estimate:* 9–15 months.
- ***JCR*:** no statistics found → **[verify]**.
- **Before submission (realistic):** 2–4 months. That covers closing the open science items, writing the text yourself, co-author review rounds, and the English pass.

---

## 2. Journal comparison table

Legend: **Fit** = scope fit for *this* paper (1 = poor, 5 = excellent), my judgement with a one-line reason. "Checked" means read on the journal or publisher site on 2026-10-13. APCs are **list prices, net of tax**, unless stated.

### 2.1 Scope, article types, OA model, costs

| Journal | Fit (1–5) and reason | Article types / length | OA model | APC (list) and waivers/discounts | Submission fee |
|---|---|---|---|---|---|
| **Earth Surface Dynamics** (Copernicus/EGU) | **3**: values "general implications for Earth surface science"; coastal not named; a single-site, small-n study must argue generality | Research article (no stated limit); ESurf Letter < 2,500 words, abstract ≤ 200; short communication "a few pages"; LESSONS 1,000–2,000 words (https://www.earth-surface-dynamics.net/about/manuscript_types.html) | Gold OA (site content under CC BY 4.0) | **€1,800** full / **€900** short (submissions from 1 Jan 2025); EGU members **€1,620** / €810; EED countries −50 %; R4L waived; **discretionary waiver**, with "authors without research funds" a priority criterion, applied for **at registration only**; support budget = 10 % of previous year's output (https://www.earth-surface-dynamics.net/about/article_processing_charges.html; …/about/financial_support.html) | None mentioned ("Preprints are free of charge") |
| **NHESS** (Copernicus/EGU) | **4**: "sea, ocean, and coastal hazards" and "early warning systems" are named in scope; must show broader implications | Research article, review, brief communication, comments (aims & scope page) | Gold OA | **€1,800** full / **€900** brief communication; EGU **€1,620**; same EED/R4L/discretionary rules (https://www.natural-hazards-and-earth-system-sciences.net/about/article_processing_charges.html) | None mentioned |
| ***Géomorphologie : relief, processus, environnement*** (GFG, OpenEdition) | **3**: process geomorphology and natural risk; closest to the DYNARISK/PRODIG framing; small ML/modelling readership | Article ≤ 15–20 pages incl. figures; bilingual title/abstract (≤ 250 words)/keywords (≤ 6)/captions + **~7,000-character abridged version** in the other language (https://journals.openedition.org/geomorphologie/701) | "OpenEdition Freemium": HTML free, PDF for subscribers (https://journals.openedition.org/geomorphologie/32); Crossref gives **CC BY-SA 4.0** for 2025–26 articles (E §2.2) → **diamond not confirmed [verify with the editor]** | **No APC mentioned anywhere on the site** (checked) | None mentioned; submission by email |
| ***Coastal Engineering*** (Elsevier) | **4**: storm-erosion prediction and EWS; Nicolae Lerma (2017, 2024), Splinter 2014, Calcraft 2025 are here; engineering rigour expected | [verify] (Guide for Authors blocked) | **Hybrid** (Elsevier APC list) | **USD 4,040 / EUR 3,680** (Elsevier APC price list, "Prices as of date: 05-Oct-2026", excl. taxes; https://legacyfileshare.elsevier.com/els_com_pricing/article-publishing-charge.xlsx linked from https://www.elsevier.com/about/policies-and-standards/pricing). **€0 for subscription publication.** Couperin–Elsevier: no APC for eligible corresponding authors (§3) | [verify] |
| ***Geomorphology*** (Elsevier) | **3**: Castelle 2015 (Truc Vert 2013–14) and Burvingt & Castelle 2023 are here; ML/forecast angle is secondary for this readership | [verify] | Hybrid | **USD 3,500 / EUR 3,190** (same list) | [verify] |
| ***Journal of Coastal Research*** (CERF) | **4** on scope; continuity with the 2018 paper; lower prestige | Research articles, technical communications, reviews, discussions, etc.; abstract "not more than 3 % of the text or < 300 words" (JCR Author Instructions PDF, https://jcr.kglmeridian.com/fileasset/jcr/JCR_Author_Instructions.pdf) | Subscription; OA "by request" to cerf.jcr@gmail.com (same PDF) | Page charges "not mandatory … voluntary"; colour and OA quoted on request (same PDF). OA price **[verify]** | **Yes: "a required, non-refundable manuscript submission fee for all submissions"** (same PDF). **Amount [verify]** |
| ***Earth Surface Processes and Landforms*** (Wiley/BSG) | **4**: process-based coastal geomorphology; Azorakos et al. 2025 (Castelle group) is here | [verify] | Hybrid | **USD 5,600 / GBP 3,750 / EUR 4,650** per Wiley's ESPL OA page as indexed by search (https://onlinelibrary.wiley.com/page/journal/10969837/homepage/fundedaccess.html; direct fetch 403) **[verify live]**. Couperin–Wiley 2026–2028 covers **hybrid** OA for affiliated corresponding authors (§3). €0 for subscription publication | [verify] |
| ***Marine Geology*** (Elsevier) | **2**: sediment/morphology focus; event-scale forecasting is marginal | [verify] | Hybrid | **USD 3,520 / EUR 3,210** (Elsevier list, 05-Oct-2026) | [verify] |
| ***Ocean & Coastal Management*** (Elsevier) | **2**: management/policy; would need the OCA bulletin use as the main story | [verify] | Hybrid | **USD 4,130 / EUR 3,770** (Elsevier list, 05-Oct-2026) | [verify] |
| ***JGR: Earth Surface*** (AGU/Wiley) | **3**: model comparison fits, but the novelty bar is high and the honest-negative result may be judged incremental | [verify] | Hybrid | AGU fee table (as surfaced by search; https://www.agu.org/publications/authors/journals/publication-fees, direct fetch 403): JGR **base publication fee USD 1,000 + USD 125 per excess unit for non-OA**; **OA USD 4,190** (another AGU page shows USD 3,880); base/excess fees waived if OA → **[verify live]**. **Note: unlike Elsevier, non-OA publication is not free here** [verify] | [verify] |
| ***Natural Hazards*** (Springer) | **3**: hazards scope; less geomorphology | [verify] | Hybrid (Springer funding-eligibility page exists: https://link.springer.com/journal/11069/funding-eligibility) | **[verify]** (Springer pages blocked) | [verify] |
| ***J. Marine Science and Engineering*** (MDPI) | **2**: in scope, but see the reputation warning | [verify] | Gold OA | **CHF 2,600** per MDPI's JMSE APC page as indexed by search (https://www.mdpi.com/journal/jmse/apc; direct fetch 403) **[verify live]** | [verify] |
| ***Water*** (MDPI) | **1**: hydrology-centred; poor audience match | [verify] | Gold OA | **CHF 2,600** per MDPI's Water APC page as indexed by search (https://www.mdpi.com/journal/water/apc) **[verify live]**; an undated CHF 1,600 figure also appears (probably old) | [verify] |
| ***Frontiers in Marine Science*** | **2**: in scope (coastal ocean processes), but see the reputation warning | A-type (original research) vs B-type (brief research report etc.) | Gold OA | **CHF 3,150** (A-type), **CHF 2,500** (B-type); support through institutional partnerships, and discounts for World-Bank low/lower-middle-income countries (https://www.frontiersin.org/journals/marine-science/for-authors/publishing-fees, checked) | [verify] |

**MDPI / Frontiers warning (evidence).** Finland's Publication Forum (JUFO), the national journal classification used in research assessment, announced that **"MDPI and Frontiers journals, where publication cannot be recommended without reservation, will be downgraded to level 0"** from the beginning of 2025. It cited publisher models that seek "to increase the volume and rate of publication" (https://julkaisufoorumi.fi/en/news/grey-area-journals-level-0, news dated 23.10.2024, updated 27.11.2024; read 2026-10-13). This is one national classification, not a universal verdict, but it is the kind of signal that hiring panels and reviewers notice. Given that the paper's purpose includes credibility with two supervisors and a portfolio, **MDPI and Frontiers are not recommended**: you would pay CHF 2,600–3,150 for less credibility than a free subscription-route article in *Coastal Engineering* or a ~€1,800 Copernicus article.

### 2.2 Policies, speed, metrics, verdict

| Journal | Preprint policy | Open-data / code policy | Public peer review? | Time to first decision / publication | Metrics (source, year) | Language | Independent researchers? | Verdict for THIS paper |
|---|---|---|---|---|---|---|---|---|
| ESurf | Discussion paper = preprint with DOI (6-week EGUsphere discussion) | Data availability section **mandatory**; code deposit encouraged with DOI (data policy page) | **Yes**: open discussion; referees anonymous or named | Process verified (see §1-l); medians **[verify]** | CiteScore **5.4 (2025)**, SJR 1.17 (2025) (journal metrics page). JIF not shown on site [verify] | English | [verify] | Good if framed as "limits of predictability". The generality bar is the main risk |
| NHESS | Same as ESurf | Same (Copernicus data policy) [verify the NHESS page wording] | **Yes** | Same; final response within 6 weeks | CiteScore **8.2 (2025)**, SJR 1.42 (2025) (journal metrics page) | English | [verify] | **Best overall**: scope words match (coastal hazards + EWS); public discussion gives an independent author visibility |
| *Géomorphologie* | Double-blind → ask before posting a preprint | None stated | No (double-blind, ≥ 2 referees) | [verify] | IF **0.300 (2025, Q4)** per Arnaud-Fassetta's site (E §2.2) [verify in Clarivate]; indexed in SCIE/JCR per journal page | FR or EN, bilingual abstracts + abridged version; native-English revision required | [verify] | Safe home for a co-signed FR/EN version; low visibility for the ML/forecast audience |
| *Coastal Engineering* | Elsevier: preprint anywhere, **unless** double-anonymised review [verify] | [verify] | No | [verify] | [verify] (aggregator values not used) | English | [verify] | Prestige choice; €0 via subscription; OA free through Couperin if the corresponding author is eligible |
| *Geomorphology* | As Elsevier | [verify] | No | [verify] | [verify] | English | [verify] | Plausible fallback; slightly off-centre |
| *JCR* | [verify] | [verify] | No (single-anonymised re-review mentioned in the instructions) | [verify] | [verify] | English (other-language abstracts allowed) | [verify] | Continuity with 2018 is a double-edged sword: it invites the "duplicate" question and has lower prestige. Plan C only |
| ESPL | [verify] | [verify] | No | [verify] | [verify] | English | [verify] | Strong scientific fit; OA only through Couperin–Wiley |
| *Marine Geology* | As Elsevier | [verify] | No | [verify] | [verify] | English | [verify] | Not recommended (scope) |
| *OCM* | As Elsevier | [verify] | No | [verify] | [verify] | English | [verify] | Only for a management-led spin-off |
| JGR: Earth Surface | [verify] | AGU data policy [verify] | No | [verify] | [verify] | English | [verify] | High bar; costs money even without OA [verify] |
| *Natural Hazards* | [verify] | [verify] | No | [verify] | [verify] | English | [verify] | Possible fallback; little gain over NHESS |
| JMSE (MDPI) | [verify] | [verify] | Optional open reports [verify] | [verify] | [verify] | English | [verify] | **Avoid** (cost + JUFO level 0) |
| *Water* (MDPI) | [verify] | [verify] | [verify] | [verify] | [verify] | English | [verify] | **Avoid** |
| *Frontiers Mar. Sci.* | [verify] | [verify] | Reviewers named on publication [verify] | [verify] | [verify] | English | [verify] | **Avoid** (cost + JUFO level 0) |

---

## 3. Recommendation

### Ranked top 3

1. **NHESS** (Copernicus).
   - **Why:** the scope names coastal hazards and early-warning systems. That matches the OCA/BRGM operational lineage the supervisors care about (HANDOFF §8). The **public discussion** gives an independent first author a citable DOI within weeks and a visible, named record of how the paper was argued. About 90 % of papers that reach discussion are eventually published (2025: 89.5 %).
   - **Framing:** "How much of storm-driven beach volume change is predictable for an early-warning bulletin? A leakage-free re-evaluation of the Aquitaine EVI".
   - **Swap rule:** if the co-authors prefer the process/predictability framing to the EWS framing, submit the *same* manuscript to **ESurf** instead. Same publisher, same APC, same workflow. Never submit to both at once.
2. ***Coastal Engineering*** (Elsevier).
   - **Why:** the strongest prestige signal in this sub-field, and the supervisors already publish here. **Costs nothing** if published as a subscription article, and OA is free if a BRGM or Université Paris Cité co-author is the corresponding author and the Couperin pool still has credit.
   - **Risks:** the editorial bar for a modest/negative result is higher, review is closed, and the paywall cuts visibility unless OA is used. Green OA is possible: Elsevier lets authors post the accepted manuscript. The embargo for this title is **[verify]**.
3. ***Géomorphologie : relief, processus, environnement*.**
   - **Why:** no APC found, bilingual, a close fit to Arnaud-Fassetta's hydrogeomorphological framing, and the lowest rejection risk for an honest audit.
   - **Costs:** low visibility (IF 0.3, Q4, per his site), a small modelling readership, the ~7,000-character abridged translation, native-English revision, and editor-conflict handling (board members are his co-authors).

**Plan B / C.**
- If NHESS rejects **at access review**, the reasons are usually scope or generality. Revise the framing and go to *Coastal Engineering* (or ESPL if the process angle dominates).
- If NHESS rejects **after discussion**, the discussion paper stays public. Address the comments openly and go to *Coastal Engineering*, citing the discussion if appropriate [verify Elsevier's stance on a prior public discussion; the preprint rule suggests it is fine].
- If *Coastal Engineering* rejects, send it to *Géomorphologie* (FR/EN version) or *Geomorphology*.
- *JCR* is the last resort: it has a submission fee, and continuity with 2018 invites the duplication question.

### The explicit trade-off

| | *Géomorphologie* | ESurf / NHESS | *Coastal Engineering* |
|---|---|---|---|
| Cost to you | €0 (no APC found) + English revision + translation effort | €1,800 list (€1,620 EGU), or a waiver requested at registration | €0 subscription; €3,680 OA unless Couperin covers it |
| Visibility | Low (Q4; French-speaking geomorphology community) | High, plus a public discussion record and an immediate DOI | High in coastal engineering; paywalled unless OA |
| Review | Double-blind, closed | Public, citable; referees may sign | Closed |
| Rejection risk for a modest result | Lowest | Medium (21–27 % desk rejection in 2025; ~90 % approval after discussion) | Highest |
| Co-author politics | Best for Arnaud-Fassetta; editor-COI handling needed | Neutral; good for Nicolae Lerma (EWS framing) | Best for Nicolae Lerma (his venue) |
| Portfolio value | Modest | Strong (open, citable, the review record shows rigour) | Strong (brand) |

**Argument.** The paper's main asset is **honesty and openness**: an audit, a protocol, and a negative-but-informative result. Copernicus rewards exactly that, because reviewers' comments and your responses are public, and that showcases the rigour that compensates for having no institutional affiliation. *Coastal Engineering* gives the stronger brand but hides the review, and it is the venue most likely to say "not enough advance". *Géomorphologie* is the safe, free, socially aligned option, but few of the coastal-forecasting people who would cite the work will read it there. **Choose NHESS unless both supervisors prefer *Coastal Engineering* and one of them agrees to be corresponding author.** Keep *Géomorphologie* as a dedicated French-language synthesis later (a different paper, with a different emphasis and no recycled text) or as Plan C.

### APC cost scenarios for you (no institutional funding)

| Scenario | You pay | Conditions |
|---|---|---|
| NHESS/ESurf, you are corresponding author, no waiver | **€1,800 net** (+ VAT if charged to a private payer [verify]) | List price for submissions from 1 Jan 2025 |
| Same, EGU member | **€1,620 net** + EGU membership fee [verify amount] | 10 % discount if a corresponding author is an EGU member in the submission year |
| Same, discretionary waiver granted | **€0 – partial** | Apply **at manuscript registration** (later requests are refused). Priority to "authors without research funds". Annual budget = 10 % of the previous year's output. **Not guaranteed**: if refused, you pay or withdraw |
| NHESS/ESurf, corresponding author at an institution with a Copernicus agreement | Up to **€0** | Whether BRGM or Université Paris Cité has a Copernicus institutional agreement → **[verify]** with their libraries |
| *Coastal Engineering*, subscription | **€0** | Green OA via the accepted manuscript (embargo [verify]) |
| *Coastal Engineering*, OA, you are corresponding author | **€3,680 / USD 4,040** (excl. tax) | List price |
| *Coastal Engineering*, OA, **BRGM/UPCité co-author is corresponding author** | **€0** | Couperin–Elsevier 2024–2027 national agreement: corresponding authors at participating institutions publish OA in eligible hybrid and gold journals with no APC (https://agreements.journals.elsevier.com/couperin, 2026-10-13: "authors do not have to pay an article publishing charge"; the number of APCs is "fixed and will be allocated based on date of acceptance"). Strasbourg's page puts the 2026 consortium-wide pool at **11,410** and says it "has never been depleted", with Lancet, Cell Press and some society titles excluded (https://scienceouverte.unistra.fr/en/publish/agreements-with-open-science-clauses/, 2026-10-13). **Check that *Coastal Engineering* is on the eligible list** (the Elsevier tool loads by script; [verify]) and that **BRGM participates** ([verify] with the BRGM library; Université Paris Cité runs Couperin agreements, see https://u-paris.fr/science-ouverte/wiley-stock-apc-2025/) |
| ESPL (Wiley) OA, affiliated co-author is corresponding author | **€0** | Couperin–Wiley 2026–2028: hybrid OA "becomes unlimited" with no quota; full-gold journals get only −10 % (Strasbourg page above). ESPL is hybrid → covered. Under the 2022–2025 deal the stock ran out (UPCité, updated 12/09/2025) |
| *Géomorphologie* | **€0** | No APC found (diamond not confirmed) |

**Bottom line on the corresponding author:** institutional agreements (Couperin–Elsevier, Couperin–Wiley, Copernicus IAs) key on the **corresponding author's affiliation**. If you, as an independent researcher, are the corresponding author, **none of them applies**. For Elsevier/Wiley OA at €0, **the affiliated co-author (BRGM or Université Paris Cité) must be the corresponding author**. You stay first author, which is what the portfolio needs. For Copernicus, being your own corresponding author is fine if you take the waiver route.

---

## 4. Step-by-step submission plan

Owner: **RG** = Raphaël; **NL** = A. Nicolae Lerma (BRGM); **GAF** = G. Arnaud-Fassetta (UPCité); **Co** = all co-authors. Hours are estimates.

| # | Step | Owner | Est. h |
|---|---|---|---|
| 1 | **ORCID**: create one at https://orcid.org/register; add education, the 2018 JCR paper (doi:10.2112/SI85-134.1) and current status "Independent researcher". Use the same email you will submit with (EarthArXiv requires a match) | RG | 1 |
| 2 | **Contact co-authors** with E Part 4 material. Agree, in writing: author list and order, **corresponding author** (see §3), affiliation line, target journal (NHESS vs *Coastal Engineering*), data access (OCA v1 data), and timeline | RG → NL, GAF | 3 + waiting |
| 3 | **Close the science gates**: HAT residual (R-F4), 2018 event-set question, R's minor fixes, block bootstrap by winter, out-of-fold SHAP, learning curve, exact Splinter/Harley forms or renamed stand-ins (STATUS §4) | RG (+NL for HAT/event set) | 25–40 |
| 4 | **Write the manuscript yourself** (Copernicus AI policy). Use `paper/outline.md` and the reports as notes, not as text to paste. Keep a log of AI-assisted code/analysis for the declaration | RG | 40–60 |
| 5 | **Licences and repo hygiene**: add `LICENSE` (MIT/BSD-3) and `data/processed/LICENSE` (CC BY-SA 4.0 or CC BY 4.0, see §1-c); check the provenance of `mean_dir`; remove or keep v1 tables depending on OCA permission; add `CITATION.cff`; fix README image paths (HANDOFF item 11) | RG | 4 |
| 6 | **Zenodo release**: connect GitHub ↔ Zenodo; tag `v1.0-submitted`; check the Zenodo record (title, authors with ORCID, licence, related identifiers → the 2018 paper and Castelle 2020); reserve the DOI and put it in the manuscript | RG | 2 |
| 7 | **Preprint**: *Copernicus*: none needed, the discussion paper is the preprint. *Elsevier route*: post to EarthArXiv at submission **only if** the journal does not use double-anonymised review [verify]. *Géomorphologie*: ask the editor first | RG | 1–2 |
| 8 | **Data/code availability, CRediT, competing interests, funding, acknowledgements, AI statement**: paste from §5 and adapt | RG | 2 |
| 9 | **Co-author review round**, 3 weeks, then a final-approval email from each (ICMJE criterion 3) | Co | 6–10 each |
| 10 | **English pass**: co-author or paid editor (get quotes) | GAF/NL or service | 3–8 |
| 11 | **Cover letter** (template below) | RG | 2 |
| 12 | **Highlights** (Elsevier only; drafts below) | RG | 0.5 |
| 13 | **Suggested reviewers**: 3–5 people who have published on storm-erosion prediction/ML/equilibrium models at sites *other than* Aquitaine, with **no co-authorship with any of us in the last 5 years** (check OpenAlex), at least 2 countries, at least 1 early-career researcher, and none from BRGM/EPOC/UPCité. Use E Part 3's "likely reviewer" flags as the starting list | RG | 3 |
| 14 | **Graphical abstract** (Elsevier; optional elsewhere): left, the method schematic (2017 pipeline vs 2026 protocol); right, the skill comparison with CIs (Fig. 4), one headline sentence. Elsevier size requirements [verify] | RG | 3 |
| 15 | **Submit**. For Copernicus, apply for the **APC waiver at registration** if needed, and certify the AI declaration | corresponding author | 2 |
| 16 | **Discussion/review phase**: reply to every comment with the template below; Copernicus final response within 4 (ESurf) / 6 (NHESS) weeks | RG (+Co) | 15–30 |
| 17 | **Portfolio entry** on acceptance: a PR in `env-models/Portfolio-Gillet` with citation, DOI badge, Zenodo link, a plain-language paragraph (≤ 120 words) and the key figure. Add the paper and the dataset DOI to ORCID | RG | 3 |

### Cover letter template (top choice: NHESS), 1 page

> Dear Editor,
>
> Please consider our manuscript "[Title]" by R. Gillet, A. Nicolae Lerma, G. Arnaud-Fassetta [and …] for publication as a research article in *Natural Hazards and Earth System Sciences*.
>
> **Question.** Operational storm-erosion warnings on the Aquitaine coast (France) rely on simple forcing indicators. In 2018 several of us published an Eroded Volume Indicator (EVI) relating storm wave energy to beach volume loss at Truc Vert (Nicolae Lerma et al., 2018, *J. Coastal Res.* SI85, doi:10.2112/SI85-134.1), calibrated on 39 events and validated on 13. That paper called for validation on more storms and storm sequences. This manuscript provides it.
>
> **What we did.** We re-analysed the indicator with 325 open topographic surveys (2003–2019; Castelle et al., 2020), open wave hindcasts and tide-gauge data, under a pre-specified, leakage-free leave-one-winter-out protocol with bootstrap confidence intervals. We compared it with physics-based, equilibrium-type and machine-learning models.
>
> **What we found.** No model outperformed the linear indicator beyond its confidence interval on held-out winters. Equilibrium-type models gave a small, consistent but non-significant gain. Survey spacing, not model choice, was the first-order limit on event-scale predictability. We think this "limits of predictability" result is useful to agencies designing storm-erosion bulletins, and to modellers applying machine learning to small coastal datasets.
>
> **Why NHESS.** The work addresses coastal hazards and early-warning systems, both within the journal's scope, and its implications go beyond one site: a transferable evaluation protocol and an open, citable event table.
>
> **Relationship to prior work.** This is a re-analysis and extension of the 2018 indicator. All text and figures are new. Overlapping methods are cited, not reproduced. Code and data are archived at Zenodo (doi:[…]).
>
> **Declarations.** The manuscript is not under consideration elsewhere. All authors approved the submission. [AI-use statement as in the manuscript.] We have no financial competing interests. Two authors are employed by BRGM, which operates the regional storm-warning network discussed.
>
> Sincerely, Raphaël Gillet (Independent researcher, [city], France; ORCID […]), on behalf of all authors.

### Highlights (Elsevier: ≤ 85 characters each including spaces [verify limit in the Guide for Authors])
1. Leakage-free re-test of a published storm-erosion indicator at Truc Vert
2. No model beat the linear energy indicator beyond its confidence interval
3. Equilibrium-type models gave a small, consistent but non-significant gain
4. Survey spacing, not model choice, limits event-scale erosion prediction
5. Open code and 2003–2019 event table support early-warning benchmarking

### Response-to-reviewers template

```
Reviewer #  | Comment # | Comment (verbatim, quoted) | Response | Change in manuscript (section, line numbers in tracked version)
R1          | 1         | "..."                      | We agree/partly agree/respectfully disagree because ... [evidence, numbers with CI] | Sect. 4.2, L210–225: added block-bootstrap CIs; new Table S3
```
Rules: answer every point; quote the comment; lead with agreement where you can; give numbers rather than adjectives; when you disagree, give evidence and offer a compromise (a sentence in the Discussion); keep the tone the same for anonymous and named referees. For Copernicus, the responses are **public**.

---

## 5. Templates

### Data availability (Copernicus "Data availability" section; adapt for Elsevier "Data availability")
> The Truc Vert topographic surveys, wave and tide series of Castelle et al. (2020) are available under CC0 from the Open Science Framework (https://doi.org/10.17605/OSF.IO/JFTW8). RESOURCECODE wave hindcast data (Ifremer) are available at https://doi.org/10.12770/d089a801-c853-49bd-9064-dde5808ff8d8 under CC BY-SA 4.0. Tide-gauge records of Arcachon-Eyrac, Boucau and Socoa are distributed by SHOM/REFMAR (https://doi.org/10.17183/REFMAR#RONIM) under Licence Ouverte 2.0 (data downloaded on [date]). Vertical datum references are from SHOM's Références Altimétriques Maritimes (Licence Ouverte 2.0). The NAO index is from NOAA's Climate Prediction Center. [The 2008–2015 legacy profiles and forcing used to reproduce the 2018 indicator were provided by BRGM/OCA and are available from the corresponding author on reasonable request with the permission of BRGM.] The derived event tables (v2, 2008–2019) are archived with the code at https://doi.org/10.5281/zenodo.[…] under [CC BY-SA 4.0]. No third-party raw data are redistributed; scripts that download them are included.

### Code availability
> All code (Python 3.12) used to build the event tables, reproduce the 2018 indicator, and fit and evaluate the models, including the environment lockfile and tests, is archived at https://doi.org/10.5281/zenodo.[…] (release v1.0) under the [MIT] licence and developed at https://github.com/env-models/Beach_erosion.

### Author contributions (CRediT; adapt after the authorship agreement)
> **R. Gillet:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Visualization, Writing – original draft, Project administration. **A. Nicolae Lerma:** Conceptualization (2017–2018 indicator), Resources (OCA/BRGM data), Validation, Supervision (2017), Writing – review & editing. **G. Arnaud-Fassetta:** Conceptualization (hydrogeomorphological framing), Supervision (2017), Writing – review & editing. [**B. Castelle:** Resources (Truc Vert dataset), Writing – review & editing — only if he joins.]

### Competing interests
> The authors declare that they have no financial competing interests. A. Nicolae Lerma [and …] are employed by BRGM, which contributes to the regional storm-warning network (Observatoire de la Côte de Nouvelle-Aquitaine) whose indicator is evaluated here. [If a co-author is an editor of the journal: "X is a member of the editorial board of [journal]."]

### Acknowledgements
> We thank the Observatoire de la Côte de Nouvelle-Aquitaine (OCA) and BRGM for the 2008–2015 survey and forcing data used in the original indicator; B. Castelle and colleagues (UMR 5805 EPOC, Université de Bordeaux/CNRS) for making the 2003–2019 Truc Vert surveys openly available (Castelle et al., 2020) and the SNO DYNALIT/Truc Vert monitoring teams for the field surveys [verify the exact acknowledgement wording requested in Castelle et al. 2020]; SHOM for REFMAR tide-gauge data and datum references; Ifremer and the RESOURCECODE consortium for the wave hindcast; Cerema for CANDHIS buoy data; and NOAA's Climate Prediction Center for the NAO index. [Named individuals: only with their written permission.]
>
> **Use of AI tools.** AI-assisted coding and analysis tools ([name, version]) were used to [write and test data-processing and modelling scripts / search and check references]. All code was reviewed, tested (automated tests included in the archive) and run by the authors, and all numbers were verified by the authors. The manuscript text and interpretations were written by the authors. [Copernicus: put this in Methods or Acknowledgements. Elsevier: as a separate "Declaration of generative AI and AI-assisted technologies" statement.]

### Funding (unfunded independent author)
> This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors. R. Gillet carried out this work as an independent researcher without institutional funding. [Co-authors' time: "A. Nicolae Lerma's contribution was supported by BRGM [programme, if any]."]

---

## 6. Still [verify] (sorted by how much each blocks the decision)
1. Whether **BRGM** participates in the Couperin–Elsevier 2024–2027 agreement, and whether ***Coastal Engineering*** is on the eligible list.
2. Whether BRGM or Université Paris Cité has a **Copernicus institutional agreement** (none found by search on 2026-10-13: the agreements found were ETH Domain, Leibniz, Jisc, University of California; ask publications@copernicus.org or the libraries). Whether VAT is added for a private (non-VAT-registered) payer.
3. ***Géomorphologie*: diamond OA confirmation** and its preprint policy under double-blind review.
4. Copernicus median review/publication times (not on the metrics page). Whether a manuscript rejected after discussion stays public (exact wording). The stance on prior external preprints.
5. *Coastal Engineering*: review model (double-anonymised?), Guide for Authors items (length, highlights limit, graphical-abstract specs), green-OA embargo, time to first decision, JIF.
6. Live confirmation of ESPL APC (USD 5,600 / EUR 4,650), AGU JGR fees (USD 4,190 vs 3,880 OA; USD 1,000 base for non-OA), MDPI APCs (CHF 2,600), Springer *Natural Hazards* APC.
7. *JCR* submission-fee amount and OA price.
8. RESOURCECODE licence (dual "CC BY-SA 4.0" / "Copyright" wording); REFMAR licence; NOAA CPC wording; OCA legacy-data licence.
9. ORCID requirements at Copernicus/Elsevier/Wiley/AGU; evidence of independent-researcher authors per journal.
10. Editing-service prices; EGU membership fee.
11. COPE text-recycling page read live (403 to direct fetch); COPE authorship-dispute flowchart URL.
