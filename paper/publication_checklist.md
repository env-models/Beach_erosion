# Publication checklist (HANDOFF §7) — owner: Raphaël Gillet

Status key: ☐ not started · ◐ prepared/draft · ☑ done. First version 2026-10-13 by the orchestrator (Agent F). **Updated 2026-10-13/14 by Agent P** against journal and publisher websites (all checks dated 2026-10-13). **The full reasoning, sources, URLs and templates are in [`reports/F_publishing_guide.md`](../reports/F_publishing_guide.md).** Nothing here has been sent to anyone.

## 0. Gates to clear before submission (guide §1)
- ☐ **AI-use rules.** Copernicus: *"Generative AI must not be used for text or interpretations"*; generative use must be declared in Methods or Acknowledgements and certified at registration (https://www.earth-surface-dynamics.net/policies/ai_policy.html). Elsevier requires a separate AI declaration statement. → **Write the manuscript text yourself**; declare the AI-assisted code/analysis (template in guide §5).
- ☐ **Open science items** (STATUS §3–4): HAT 0.31 m residual (R-F4), 2018 event-set question (22/39/27), R's minor fixes, **block bootstrap by winter**, out-of-fold SHAP, learning curve, exact Splinter 2014 / Harley 2009 forms.
- ☐ **Duplication framing vs Nicolae Lerma et al. 2018**: disclose the relationship, write all text fresh, redraw all figures (never reuse the CERF-copyrighted 2018 figures). COPE text-recycling: cited methods overlap can be acceptable; results/discussion overlap is not.
- ☐ **Data rights**: v1 event tables derive from OCA/BRGM legacy data with **no known licence** → written permission from BRGM/OCA before release; v2 (open data) can be released now.

## 1. Author identity
- ☐ Create an **ORCID iD** (https://orcid.org/register). Add the 2018 JCR paper (doi:10.2112/SI85-134.1). EarthArXiv requires the submitter's ORCID to show education and recent affiliations, and the ORCID email to match the submitter email (verified).
- ☐ Affiliation line: default *"Independent researcher, [city], France"*. Use an associate affiliation only if a supervisor offers one. No journal page that could be read requires an institutional email. *Géomorphologie* asks for a **professional phone number** for the corresponding author (verified).
- ◐ CRediT statement drafted (guide §5; ICMJE four criteria verified). Supervisors: Conceptualization (2017–18), Supervision (2017), Resources, Validation, Writing – review & editing. Data providers only if they actually contribute.

## 2. Venue choice — decided recommendation (guide §2–3)
- ☑ Scope, APC, OA, data policy checked on the journals' own sites where they were reachable (several Elsevier/Wiley/Springer/MDPI/AGU pages block automated fetching → still [verify live]).
- ◐ **Recommendation: 1. NHESS** (or ESurf with the same manuscript if the framing is process, not EWS). **2. *Coastal Engineering*.** **3. *Géomorphologie*.** Plan C: *JCR*. Avoid MDPI/Frontiers (JUFO level 0 from 2025, verified).
- Verified figures (2026-10-13):
  - **NHESS / ESurf APC €1,800 net** (full article, submissions from 1 Jan 2025); €900 short; **€1,620 for EGU members**. A discretionary waiver is possible, with "authors without research funds" a priority criterion, but it **must be requested at manuscript registration**. No submission fee.
  - Desk rejection in 2025: ESurf 15/70, NHESS 143/535; approval after discussion 91.8 % / 89.5 %. CiteScore 2025: ESurf 5.4, NHESS 8.2.
  - **Coastal Engineering** hybrid, OA APC **USD 4,040 / EUR 3,680**; Geomorphology USD 3,500 / EUR 3,190; Marine Geology USD 3,520 / EUR 3,210; OCM USD 4,130 / EUR 3,770 (Elsevier APC list dated 05-Oct-2026, excl. tax). Subscription publication €0.
  - ***Géomorphologie***: no APC mentioned; site says "OpenEdition Freemium" (HTML free, PDF for subscribers); recent articles are CC BY-SA 4.0 per Crossref → **"diamond" still [verify]**. Double-blind review, ≥ 2 referees. 15–20 pages incl. figures. Bilingual abstracts (≤ 250 words) + ~7,000-character abridged version. Native-English revision required.
  - ***JCR***: **mandatory non-refundable submission fee** (amount [verify]); page charges voluntary; OA on request.
  - **Frontiers Mar. Sci.** CHF 3,150 (A-type). MDPI JMSE/Water CHF 2,600 [verify live]. ESPL USD 5,600 / EUR 4,650 [verify live]. AGU JGR OA USD 4,190 (or 3,880) + USD 1,000 base fee if not OA [verify live].
- ☐ **Corresponding-author decision.** French national agreements key on the **corresponding author's affiliation**:
  - Couperin–Elsevier 2024–2027 gives no APC in eligible hybrid/gold journals; the 2026 pool of 11,410 is shared, and some society titles are excluded.
  - Couperin–Wiley 2026–2028 makes hybrid OA unlimited; gold journals get only −10 %.
  - If Raphaël (independent) is corresponding author, neither applies. For €0 OA in *Coastal Engineering*/ESPL, a BRGM/UPCité co-author must be corresponding author.
  - Still [verify]: BRGM participation and *Coastal Engineering* on the eligible list.
- ☐ Decide with the supervisors.

## 3. Preprint
- ☐ **Copernicus route: no separate preprint.** The discussion paper on EGUsphere is the citable preprint (6-week open discussion, verified). Treat it as public permanently.
- ☐ Elsevier route: "Authors can share their preprint anywhere at any time", **except** some society titles and double-anonymised journals (verified). Check the *Coastal Engineering* review model [verify] before posting to EarthArXiv.
- ☐ *Géomorphologie* (double-blind): ask the editor before posting any preprint.
- EarthArXiv (verified): preprints under review accepted, labelled "non-peer reviewed preprint submitted to EarthArXiv" + target journal; DOI assigned; English, single PDF; embargoed postprints refused.

## 4. Code and data release
- ☐ Add a **LICENSE** (code: MIT or BSD-3; none exists yet) and `data/processed/LICENSE`.
- ☐ Event table v2: **CC BY-SA 4.0** if any column derives from RESOURCECODE (CC BY-SA 4.0 per Sextant, B; the share-alike clause applies to shared Adapted Material) — check `mean_dir` provenance. Otherwise CC BY 4.0. Castelle 2020 OSF is **CC0 1.0** (re-verified via OSF API). SHOM/REFMAR/RAM and CANDHIS are **Licence Ouverte 2.0**: compatible with CC BY; attribution = source + date of last update (licence text verified).
- ☐ Event table v1 (OCA/BRGM legacy data): release **only with written permission**.
- ☐ WEPA (CC BY-NC-ND): never redistribute, not even derived.
- ☐ Tag the GitHub release (`v1.0-submitted`) → Zenodo DOI; add `CITATION.cff`; cite software packages.
- ☐ Third-party raw data are NOT redistributed; download scripts + `data/README.md` instead (already in place).
- ☑ README image paths (HANDOFF §2.1 item 11): `README.md` no longer references `Raph9989` (checked 2026-10-14 after the H README overhaul, commit cd40eca).
- **Copernicus**: "Data availability" section **mandatory**; code deposit with DOI encouraged; data needed to replicate figures must be public (verified).

## 5. Co-authors
- ◐ One-page project summary (EN/FR) and authorship proposal: `reports/E_supervisors.md` Part 4 — Raphaël sends it himself.
- ☐ Written agreement on: author order, **corresponding author**, affiliation line, journal, OCA data permission, timeline. If a supervisor declines: acknowledgement with written permission, and no use of data only they provided (guide §1-b).
- ☐ Co-author review round (≥ 3 weeks) + an explicit final-approval email from each (ICMJE criterion 3).

## 6. Submission pack (drafts in guide §4–5)
- ◐ Cover letter for NHESS (1 page) — guide §4.
- ◐ Highlights (5, all ≤ 73 characters; Elsevier route only; limit [verify]) — guide §4.
- ☐ Graphical abstract (method schematic + skill-with-CI figure).
- ◐ Data availability, code availability, CRediT, competing interests (declare BRGM employment as a relevant non-financial interest), acknowledgements (OCA/BRGM, EPOC/Castelle et al., SHOM, Ifremer/RESOURCECODE, Cerema/CANDHIS, NOAA CPC), funding ("no specific grant"), AI-use statement — guide §5.
- ☐ Suggested reviewers: 3–5, no co-authorship with any author in 5 years, ≥ 2 countries, none from BRGM/EPOC/UPCité (start from `reports/E_supervisors.md` Part 3).
- ☐ If *Géomorphologie*: request a handling editor without recent collaboration with Arnaud-Fassetta (Gautier, Lissak and Suanez are associate editors and his co-authors).

## 7. Response-to-reviewers template
- ◐ Table template in guide §4 (reviewer | comment | response | change with line numbers). Keep a running "anticipated objections" list (guide §1-e and `reports/D_state_of_the_art.md` "methodological must-haves"). For Copernicus, the responses are public.

## 8. On acceptance
- ☐ Portfolio PR in `env-models/Portfolio-Gillet`: citation, DOI badge, Zenodo link, plain-language paragraph (≤ 120 words), key figure; add the paper and the dataset DOI to ORCID.

## 9. Still [verify] (full list in guide §6)
BRGM in Couperin–Elsevier and *Coastal Engineering* eligibility; Copernicus agreements for BRGM/UPCité and VAT for private payers; *Géomorphologie* diamond status and preprint policy; Copernicus median times and the post-rejection visibility of discussion papers; the *Coastal Engineering* Guide for Authors (review model, limits, embargo, JIF); live ESPL/AGU/MDPI/Springer APCs; *JCR* submission-fee amount; the RESOURCECODE dual licence wording, REFMAR, NOAA CPC and OCA legacy licences; ORCID mandates; editing-service prices; EGU membership fee.
