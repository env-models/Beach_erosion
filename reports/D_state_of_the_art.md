# D — State of the art, 2016–2026 (annotated bibliography)

**Agent D deliverable** for HANDOFF §3-D. Branch `revisit-2026`. Compiled 13 Oct 2026.

**Status:** IN PROGRESS. Themes 1–2 are written. Themes 3–5 and the closing sections are still to come.

## How entries were verified

- `verified: yes` means two checks passed. First, the DOI was looked up in the **Crossref REST API** (`api.crossref.org/works/<doi>`), and the title, authors, year, journal, volume and pages shown here match that record. Second, `curl -I https://doi.org/<doi>` returned an HTTP 302 redirect to the publisher, which confirms the DOI is registered and resolves. All 71 DOIs cited in this file passed the second check on 13 Oct 2026.
- Open-access (OA) status and links come from the OpenAlex `best_oa_location` field. They were not opened one by one, so treat "OA" as indicative.
- Relevance notes draw on the publisher abstract (via OpenAlex, Crossref or Semantic Scholar) where one was available. Claims that go beyond the abstract are tagged **[verify]**.
- Items without a DOI, or whose details could not be confirmed, are marked `verified: no` with **[verify]**.
- Citation format: Authors (year). Title. *Journal* volume, pages. DOI.

---

## Theme 1 — Storm erosion indicators and early-warning systems (EWS)

**Glossary.**
- **EWS** (early-warning system): forecasts hazard 1–3 days ahead so that someone can act.
- **TWL** (total water level): tide + surge + wave runup.
- **Indicator**: a cheap formula that maps forcing to an impact class or volume, as opposed to a full numerical model such as XBeach.

### 1.1 Nicolae Lerma et al. (2018) — the direct descendant of the 2017 EVI ★
Nicolae Lerma, A., Bulteau, T., Müller, H., Decarsin, C., **Gillet, R.**, Paris, F., Biausque, M., Sénéchal, N., Castelle, B. (2018). Towards the development of a storm erosion EWS for the French Aquitaine coast. *Journal of Coastal Research* SI 85 (Proc. ICS 2018, Busan), 666–670. DOI: 10.2112/SI85-134.1. OA: no (closed). Full author list confirmed via OpenAlex.

**Relevance.** This is the **most important prior-work item for this project**: the 2017 indicator has already been published, with Raphaël as co-author. The abstract describes an OCA-network EWS that alerts partners 2–3 days ahead so they can run pre- and post-storm surveys, and issues regional bulletins. It also tests two local indicators: a **Collision Regime Indicator (CRI)** and the **Eroded Volume Indicator (EVI)**. Both were calibrated and validated on bimonthly Truc Vert surveys (2009–2015) and on Biscarrosse surveys every 2–7 days during winters since 2015. The abstract says the EVI predicts "fairly accurate eroded sediment volume" and that more validation is needed for single storms and clusters across the whole coast.

Consequences for us:
- The new paper must cite this as the baseline publication of EVI and frame itself as "revisiting/auditing the EVI of Nicolae Lerma et al. (2018)", not as a first proposal.
- The audit findings in HANDOFF §2.1 (units, selecting on the target, leakage) have to be described tactfully, because this paper is co-signed by the internship supervisor (Nicolae Lerma) and by likely reviewers or co-authors (Castelle, Sénéchal).
- We have not seen the full text. Check which EVI variant and which skill metric (R or R²) were published **[verify]**.

verified: yes

### 1.2 Harley et al. (2016) — Safe Corridor Width / Emilia-Romagna EWS
Harley, M.D., Valentini, A., Armaroli, C., Perini, L., Calabrese, L., Ciavola, P. (2016). Can an early-warning system help minimize the impacts of coastal storms? A case study of the 2012 Halloween storm, northern Italy. *Natural Hazards and Earth System Sciences* 16, 209–222. DOI: 10.5194/nhess-16-209-2016. OA: gold, https://nhess.copernicus.org/articles/16/209/2016/nhess-16-209-2016.pdf

**Relevance.** This is the source of the "Safe Corridor Width" idea that the 2017 thesis adapted into the HAT exceedance threshold. The ER-EWS chains COSMO, ROMS, SWAN and XBeach to forecast storm impact indicators at 8 sites. Cite it as the methodological ancestor of the threshold step, and note that our indicator is a statistical shortcut to what ER-EWS does with XBeach.

verified: yes

### 1.3 Ciavola et al. (2011) — MICORE lessons (pre-2016 anchor)
Ciavola, P., Ferreira, O., Haerens, P., Van Koningsveld, M., Armaroli, C. (2011). Storm impacts along European coastlines. Part 2: lessons learned from the MICORE project. *Environmental Science & Policy* 14, 924–933. DOI: 10.1016/j.envsci.2011.05.009. OA: green, http://hdl.handle.net/10400.1/10352

**Relevance.** This is the European EWS lineage that the HANDOFF calls "MICORE successors". It is useful in the introduction to place the OCA/BRGM network within the European tradition of storm-impact indicators. It falls outside the 2016–2026 window but is the canonical reference.

verified: yes

### 1.4 Stockdon et al. (2023) — operational TWL / storm-impact forecasts (USGS)
Stockdon, H.F., Long, J.W., Palmsten, M.L., Van der Westhuysen, A., Doran, K.S., Snell, R.J. (2023). Operational forecasts of wave-driven water levels and coastal hazards for US Gulf and Atlantic coasts. *Communications Earth & Environment* 4, 169. DOI: 10.1038/s43247-023-00817-2. OA: gold, https://www.nature.com/articles/s43247-023-00817-2.pdf

**Relevance.** This is the state-of-the-art national operational system. It adds parameterised runup to NOAA forecasts and converts TWL relative to dune toe and crest into Sallenger-type impact regimes. It is the strongest example that **runup-based exceedance indicators** (our HAT threshold) are operational practice, and it supports our framing of "indicator for an EWS".

verified: yes

### 1.5 Leaman et al. (2021) — storm hazard matrix (erosion × flooding)
Leaman, C.K., Harley, M.D., Splinter, K.D., Thran, M.C., Kinsela, M.A., Turner, I.L. (2021). A storm hazard matrix combining coastal flooding and beach erosion. *Coastal Engineering* 170, 104001. DOI: 10.1016/j.coastaleng.2021.104001. OA: hybrid (publisher).

**Relevance.** This is a recent and well-cited way to communicate combined erosion and flooding hazard for EWS. If our model outputs a predictive interval of ΔV, the interval can be mapped into such a matrix for the OCA bulletin use case, which would be a nice "operational" figure.

verified: yes

### 1.6 Mendoza, Jiménez & Mateo (2011) — storm power intensity scale
Mendoza, E.T., Jiménez, J.A., Mateo, J. (2011). A coastal storms intensity scale for the Catalan sea (NW Mediterranean). *Natural Hazards and Earth System Sciences* 11, 2453–2462. DOI: 10.5194/nhess-11-2453-2011. OA: gold.

**Relevance.** This paper builds a 5-class scale on a Dolan & Davis-type **storm power index** (Hs² × duration). It is the standard reference for "storm energy content" as a classification variable and directly supports one of our energy feature variants. It is outside the window but foundational.

verified: yes

### 1.7 Miller & Livermont (2009) — Storm Erosion Index (SEI)
Miller, J.K., Livermont, E. (2009). A predictive index for wave and storm surge induced erosion. In *Coastal Engineering 2008* (Proc. 31st ICCE), 4143–4153. World Scientific. DOI: 10.1142/9789814277426_0344. OA: listed as diamond by OpenAlex.

**Relevance.** SEI integrates excess water level and wave energy over a storm. It is conceptually the closest US analogue to the 2017 EVI (an exceedance-weighted, time-integrated forcing). It must be cited as prior art for "cumulative exceedance energy". A companion proceedings paper exists (Miller & Livermont 2008, *Solutions to Coastal Disasters*, DOI 10.1061/40968(312)51; Crossref metadata seen, not opened).

verified: yes

### 1.8 Harley (2017) — Coastal storm definition (book chapter)
Harley, M. (2017). Coastal storm definition. In Ciavola, P., Coco, G. (eds.) *Coastal Storms: Processes and Impacts*, Wiley, pp. 1–21. DOI: 10.1002/9781118937099.ch1. OA: no.

**Relevance.** This is the reference for **storm definitions** (peak-over-threshold, minimum duration, independence/meeting time). Our storm detection (Hs95% peak, Hs75% bounds) should be justified against it, and a sensitivity analysis on the thresholds should be reported. Editor names for the volume: **[verify]**.

verified: yes

### 1.9 Harley et al. (2017) — wave direction amplifies storm erosion
Harley, M.D., Turner, I.L., Kinsela, M.A., Middleton, J.H., Mumford, P.J., Splinter, K.D., Phillips, M.S., Simmons, J.A., et al. (2017). Extreme coastal erosion enhanced by anomalous extratropical storm wave direction. *Scientific Reports* 7, 6033. DOI: 10.1038/s41598-017-05792-1. OA: gold.

**Relevance.** This is evidence that **direction** matters as much as energy for storm erosion. It directly motivates the "does direction matter?" ablation in HANDOFF §3-C, which the 2017 work could not test because WW3 direction was missing.

verified: yes

### 1.10 Beuzen et al. (2019) — controls of berm vs dune storm erosion
Beuzen, T., Harley, M.D., Splinter, K.D., Turner, I.L. (2019). Controls of variability in berm and dune storm erosion. *Journal of Geophysical Research: Earth Surface* 124, 2647–2665. DOI: 10.1029/2019JF005184. OA: bronze, https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2019JF005184

**Relevance.** This study uses pre- and post-storm LiDAR across more than 1,700 transects and separates **berm** from **dune** erosion and their controls. That maps exactly onto the thesis finding that "berm absence explains dune retreat in 2013–14". It supports berm volume as a feature and splitting ΔV into upper and lower parts.

verified: yes

### 1.11 Simmons et al. (2019) — how much calibration data storm-erosion models need
Simmons, J.A., Splinter, K.D., Harley, M.D., Turner, I.L. (2019). Calibration data requirements for modelling subaerial beach storm erosion. *Coastal Engineering* 152, 103507. DOI: 10.1016/j.coastaleng.2019.103507. OA: no.

**Relevance.** This compares two commonly used storm-erosion models and quantifies how many calibration storms are needed (exact models: **[verify]**). It is directly relevant to our small-n reality (~37 to ~120 events) and to justifying the learning-curve analysis in Agent C.

verified: yes

---

## Theme 2 — Storm clustering and recovery (Truc Vert / Aquitaine 2013–14 and beyond)

**Glossary.**
- **Storm clustering / sequencing**: several storms in close succession, so the beach cannot recover in between and cumulative erosion can exceed that of a single larger storm.
- **Recovery**: the slow return of sand to the upper beach in calm weather.
- **WEPA**: a climate index based on a sea-level pressure gradient.

### 2.1 Castelle et al. (2015) — 2013–14 winter on the Gironde coast ★
Castelle, B., Marieu, V., Bujan, S., Splinter, K.D., Robinet, A., Sénéchal, N., Ferreira, S. (2015). Impact of the winter 2013–2014 series of severe Western Europe storms on a double-barred sandy coast: Beach and dune erosion and megacusp embayments. *Geomorphology* 238, 135–148. DOI: 10.1016/j.geomorph.2015.03.006. OA: no.

**Relevance.** This is the reference description of our validation winter at the regional scale. The 2-month mean Hs exceeded 3.6 m, with 4 storms of 10-year return period and Hs > 9 m, the most energetic conditions in 18 years. Dune scarps often exceeded 10 m, with megacusp embayments about 1,000 m apart. It is essential for the 2013–14 "stress test", and the megacusp (3D) result warns that **longshore-averaged profiles hide rip/megacusp variability**, which is a limitation to state.

verified: yes

### 2.2 Masselink et al. (2016, GRL) — Atlantic-Europe 2013–14 winter
Masselink, G., Castelle, B., Scott, T., Dodet, G., Suanez, S., Jackson, D., Floc'h, F. (2016). Extreme wave activity during 2013/2014 winter and morphological impacts along the Atlantic coast of Europe. *Geophysical Research Letters* 43, 2135–2143. DOI: 10.1002/2015GL067492. OA: hybrid, https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2015GL067492

**Relevance.** This shows the 2013–14 winter was the most energetic since at least 1948 along most of the Atlantic coast of Europe. It quantifies the extremeness of our test winter, which is out-of-distribution for a model calibrated on 2009–2013. This must be stated when reporting held-out skill.

verified: yes

### 2.3 Masselink et al. (2016, ESPL) — SW England forcing and response
Masselink, G., Scott, T., Poate, T., Russell, P., Davidson, M., Conley, D. (2016). The extreme 2013/2014 winter storms: hydrodynamic forcing and coastal response along the southwest coast of England. *Earth Surface Processes and Landforms* 41, 378–391. DOI: 10.1002/esp.3836. OA: no.

**Relevance.** This links storm forcing (including wave power and direction) to coastal response for the same storm sequence on another coast. It is useful for comparing how they parameterise storm energy, and as a cross-site check on our energy metric.

verified: yes

### 2.4 Dodet et al. (2019) — post-2013–14 recovery along Atlantic Europe
Dodet, G., Castelle, B., Masselink, G., Scott, T., Davidson, M., Floc'h, F., Jackson, D., Suanez, S. (2019). Beach recovery from extreme storm activity during the 2013–14 winter along the Atlantic coast of Europe. *Earth Surface Processes and Landforms* 44, 393–401. DOI: 10.1002/esp.4500. OA: bronze, https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/esp.4500

**Relevance.** This decadal multi-site analysis of recovery includes Truc Vert **[verify site list]**. Recovery happens between surveys and therefore contaminates our ΔV (the "post-Klaus accreted" problem). It also supports including the **post-storm wave climate** (recovery-favourable conditions) as a feature, and a classifier stage.

verified: yes

### 2.5 Castelle et al. (2017, GRL) — WEPA climate index
Castelle, B., Dodet, G., Masselink, G., Scott, T. (2017). A new climate index controlling winter wave activity along the Atlantic coast of Europe: The West Europe Pressure Anomaly. *Geophysical Research Letters* 44, 1384–1392. DOI: 10.1002/2016GL072379. OA: bronze, https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2016GL072379

**Relevance.** WEPA (the Valentia–Santa Cruz de Tenerife SLP gradient) explains winter Hs variability from Portugal to the UK better than the NAO. It is a candidate winter-scale covariate, but it is collinear with the wave forcing we already have. Use it to explain inter-winter variance, not as an event-scale predictor.

verified: yes

### 2.6 Castelle et al. (2018, GRL) — increasing winter wave height 1949–2017
Castelle, B., Dodet, G., Masselink, G., Scott, T. (2018). Increased winter-mean wave height, variability, and periodicity in the northeast Atlantic over 1949–2017. *Geophysical Research Letters* 45, 3586–3596. DOI: 10.1002/2017GL076884. OA: not determined.

**Relevance.** This provides non-stationarity context: the forcing distribution shifts over decades. It justifies leave-one-winter-out evaluation and caution in extrapolating a linear indicator.

verified: yes

### 2.7 Burvingt et al. (2017) — classification of beach response to extreme storms
Burvingt, O., Masselink, G., Russell, P., Scott, T. (2017). Classification of beach response to extreme storms. *Geomorphology* 295, 722–737. DOI: 10.1016/j.geomorph.2017.07.022. OA: hybrid.

**Relevance.** This classifies beach responses to the 2013–14 storms on SW England from LiDAR. It is a precedent for a **response-type classifier** (erode, accrete, rotate) ahead of regression, which is our two-stage design. Burvingt later moved to Bordeaux (EPOC) and co-authors the Pléiades and SDB work (see 5.5 and 5.6), so he is a likely reviewer or co-author.

verified: yes

### 2.8 Burvingt et al. (2018) — climate forcing of regionally coherent storm impact and recovery
Burvingt, O., Masselink, G., Scott, T., Davidson, M., Russell, P. (2018). Climate forcing of regionally-coherent extreme storm impact and recovery on embayed beaches. *Marine Geology* 401, 112–128. DOI: 10.1016/j.margeo.2018.04.004. OA: green (Plymouth PEARL).

**Relevance.** This connects storm impact and recovery to climate indices (NAO/WEPA). It is supporting evidence for including WEPA as a winter covariate (see 2.5).

verified: yes

### 2.9 Angnuureng et al. (2017) — shoreline resilience to storm clusters at Truc Vert ★
Angnuureng, D.B., Almar, R., Sénéchal, N., Castelle, B., Addo, K.A., Marieu, V., Ranasinghe, R. (2017). Shoreline resilience to individual storms and storm clusters on a meso-macrotidal barred beach. *Geomorphology* 290, 265–276. DOI: 10.1016/j.geomorph.2017.04.007. OA: bronze.

**Relevance.** This is the key **Truc Vert storm-cluster** study, based on video-derived daily shorelines (the Truc Vert video system). It quantifies the response of the shoreline (not the volume) to individual storms versus clusters. It is closest in spirit to our clustering ablation, so we must compare our "cluster count / inter-storm gap" features with their cluster definition **[verify their definition and metrics]**.

verified: yes

### 2.10 Splinter et al. (2014, Coastal Eng.) — cumulative impact of storm clusters
Splinter, K.D., Carley, J.T., Golshani, A., Tomlinson, R. (2014). A relationship to describe the cumulative impact of storm clusters on beach erosion. *Coastal Engineering* 83, 49–55. DOI: 10.1016/j.coastaleng.2013.10.001. OA: no.

**Relevance.** This is the **Splinter 2014 cluster baseline** named in HANDOFF §3-C. They calibrated XBeach on the 1967 Gold Coast cyclone sequence, reproducing dry-beach erosion volume within 21%, then ran 17 storm-order permutations and derived a relationship for cumulative erosion. The exact predictors (likely storm energy and inter-storm interval) are **[verify]** from the full text before Agent C implements it. Our storm definition in the 2017 thesis cites this paper.

verified: yes

### 2.11 Karunarathna et al. (2014) — storm clustering and profile variability
Karunarathna, H., Pender, D., Ranasinghe, R., Short, A.D., Reeve, D.E. (2014). The effects of storm clustering on beach profile variability. *Marine Geology* 348, 103–112. DOI: 10.1016/j.margeo.2013.12.007. OA: no.

**Relevance.** This early observational study of clustering (Narrabeen) finds that cluster erosion can exceed that of a single storm of equal energy **[verify phrasing]**. It supports the "clustering" feature family.

verified: yes

### 2.12 Dissanayake et al. (2015) — storm clustering on beach/dune evolution (XBeach)
Dissanayake, P., Brown, J., Wisse, P., Karunarathna, H. (2015). Effects of storm clustering on beach/dune evolution. *Marine Geology* 370, 63–75. DOI: 10.1016/j.margeo.2015.10.010. OA: hybrid.

**Relevance.** This XBeach study of the Dec 2013–Jan 2014 cluster at Formby Point (UK) is the same storm winter as our test set. It shows that the order and intensity of the first storm condition later impacts. It is useful for the discussion of path-dependence, which an event-wise model can only capture via antecedent-state features.

verified: yes

### 2.13 Eichentopf, Karunarathna & Alsina (2019) — review of storm-sequence morphodynamics
Eichentopf, S., Karunarathna, H., Alsina, J.M. (2019). Morphodynamics of sandy beaches under the influence of storm sequences: Current research status and future needs. *Water Science and Engineering* 12, 221–234. DOI: 10.1016/j.wse.2019.09.007. OA: diamond.

**Relevance.** This review shows that **definitions of storm sequences differ between sites**. It is the go-to citation for justifying our cluster definition and running a sensitivity analysis on it.

verified: yes

### 2.14 Eichentopf et al. (2020) — storm sequencing at Hasaki
Eichentopf, S., Alsina, J.M., Christou, M., Kuriyama, Y., Karunarathna, H. (2020). Storm sequencing and beach profile variability at Hasaki, Japan. *Marine Geology* 424, 106153. DOI: 10.1016/j.margeo.2020.106153. OA: hybrid.

**Relevance.** This uses 25 years of weekly profiles and 2-hourly waves, an observational design close to ours (survey intervals plus wave series). It is a template for how to analyse supratidal vs intertidal response to sequences.

verified: yes

### 2.15 Nicolae Lerma et al. (2019) — Aquitaine LiDAR erosion/recovery sequences
Nicolae Lerma, A., Ayache, B., Ulvoas, B., Paris, F., Bernon, N., Bulteau, T., Mallet, C. (2019). Pluriannual beach-dune evolutions at regional scale: Erosion and recovery sequences analysis along the Aquitaine coast based on airborne LiDAR data. *Continental Shelf Research* 189, 103974. DOI: 10.1016/j.csr.2019.103974. OA: accepted manuscript via ScienceDirect.

**Relevance.** This is regional-scale context from the supervisor's group: LiDAR from 2011, 2014, 2016 and 2017 along the 230 km Aquitaine coast. It is relevant for transferring beyond Truc Vert and for describing alongshore variability around our site.

verified: yes

### 2.16 Nicolae Lerma et al. (2022) — decadal beach-dune profile monitoring, Aquitaine
Nicolae Lerma, A., Castelle, B., Marieu, V., Robinet, A., Bulteau, T., Bernon, N., Mallet, C. (2022). Decadal beach-dune profile monitoring along a 230-km high-energy sandy coast: Aquitaine, southwest France. *Applied Geography* 139, 102645. DOI: 10.1016/j.apgeog.2022.102645. OA: not determined.

**Relevance.** These are OCA profile datasets along the whole coast and a candidate source of **extra sites and events** for the transfer test (beyond Biscarrosse). Agent B should check data availability.

verified: yes

### 2.17 Biausque & Sénéchal (2019) — Biscarrosse winter response
Biausque, M., Sénéchal, N. (2019). Seasonal morphological response of an open sandy beach to winter wave conditions: The example of Biscarrosse beach, SW France. *Geomorphology* 332, 157–169. DOI: 10.1016/j.geomorph.2019.02.009. OA: accepted manuscript.

**Relevance.** This covers 18 months of at least bi-weekly surveys at Biscarrosse. Two winters with energy differing by a factor of 1.7 produced **similar sediment budgets**, explained by erosion/recovery sequences. This is direct evidence against a pure energy→volume law and for antecedent state and sequencing. It also describes the Biscarrosse data used for our out-of-site test.

verified: yes

### 2.18 Sénéchal et al. (2019) — seasonal recovery at Truc Vert
Sénéchal, N., Biausque, M., Bujan, S., Ferreira, S. (2019). Seasonal recovery of a sandy wave-dominated beach: the example of Truc Vert, France. In *Coastal Sediments 2019*, World Scientific, 722–732. DOI: 10.1142/9789811204487_0064. OA: no.

**Relevance.** This covers Truc Vert recovery rates and processes. Compare it with the thesis estimate of calm-weather recovery (~6 m³/m/month) and use it to parameterise recovery between storm and survey date **[verify reported rates]**.

verified: yes

### 2.19 Harley et al. (2022) — single extreme storm sequence and sediment budgets
Harley, M.D., Masselink, G., Ruiz de Alegría-Arzaburu, A., Valiente, N.G., Scott, T. (2022). Single extreme storm sequence can offset decades of shoreline retreat projected to result from sea-level rise. *Communications Earth & Environment* 3, 112. DOI: 10.1038/s43247-022-00437-2. OA: gold.

**Relevance.** Extreme sequences can **add** sand to the upper beach through cross-shore exchange. This is a physical explanation for "storms that accrete" (post-Klaus) and for sand moving across the HAT boundary. It justifies whole-profile ΔV plus the upper/lower split.

verified: yes

<!-- THEMES 3-5 AND CLOSING SECTIONS FOLLOW -->
