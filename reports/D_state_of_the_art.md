# D — State of the art, 2016–2026 (annotated bibliography)

**Agent D deliverable** for HANDOFF §3-D. Branch `revisit-2026`. Compiled 13 Oct 2026.

**Status:** COMPLETE (first pass). There are **74 annotated entries: 72 verified, 2 unverified**, plus closing sections. The open items are tagged **[verify]**. Most need the full text, which was not accessed. The most important ones are the ShoreShop 2.0 ranking claim, the exact predictors of Splinter et al. (2014), the content of BRGM report RP-67418-FR, and "COSI".

## How entries were verified

- `verified: yes` means two checks passed. First, the DOI was looked up in the **Crossref REST API** (`api.crossref.org/works/<doi>`), and the title, authors, year, journal, volume and pages shown here match that record. Second, `curl -I https://doi.org/<doi>` returned an HTTP 302 redirect to the publisher, which confirms the DOI is registered and resolves. All 72 DOIs of numbered entries in this file passed the second check on 13 Oct 2026.
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

---

## Theme 3 — Equilibrium and hybrid shoreline models

**Glossary.**
- **Equilibrium model**: the beach has an equilibrium state for a given wave climate. The rate of change is proportional to the *disequilibrium*, the mismatch between the current state and that equilibrium. This is the formal version of the thesis's "fat vs thin pre-storm profile" idea.
- **One-line model**: describes the coast by a single contour (the shoreline) per transect.
- **Hybrid**: physics-based structure plus data-driven components.

### 3.1 Yates, Guza & O'Reilly (2009) — equilibrium shoreline response
Yates, M.L., Guza, R.T., O'Reilly, W.C. (2009). Equilibrium shoreline response: Observations and modeling. *Journal of Geophysical Research: Oceans* 114, C09014 [verify article number]. DOI: 10.1029/2009JC005359. OA: bronze, https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2009JC005359

**Relevance.** This is baseline 4a in HANDOFF §3-C. In the model, dS/dt = C± · E^½ · ΔE, where ΔE is the wave-energy disequilibrium relative to an equilibrium energy that depends on the shoreline position. It uses **wave energy ∝ Hs²**, the same family as our forcing. Applied to volume instead of shoreline, it provides the physically principled continuous "antecedent-state" term that PPT's binary label approximated. Agent C should implement a **volume version** (V in place of S). Equation form: **[verify]** from the paper.

verified: yes

### 3.2 Davidson, Splinter & Turner (2013) — ShoreFor
Davidson, M.A., Splinter, K.D., Turner, I.L. (2013). A simple equilibrium model for predicting shoreline change. *Coastal Engineering* 73, 191–202. DOI: 10.1016/j.coastaleng.2012.11.002. OA: no. A corrigendum exists: *Coastal Engineering* 75, 91, DOI 10.1016/j.coastaleng.2013.01.005.

**Relevance.** This is the original ShoreFor model, where forcing is wave power × disequilibrium in dimensionless fall velocity Ω, with a memory window φ. Its **memory-weighted antecedent Ω** is a ready-made continuous "antecedent state" feature for our ML models. Cite the corrigendum too.

verified: yes

### 3.3 Splinter et al. (2014, JGR-ES) — generalised ShoreFor (includes Truc Vert) ★
Splinter, K.D., Turner, I.L., Davidson, M.A., Barnard, P., Castelle, B., Oltman-Shay, J. (2014). A generalized equilibrium model for predicting daily to interannual shoreline response. *Journal of Geophysical Research: Earth Surface* 119, 1936–1958. DOI: 10.1002/2014JF003106. OA: green, https://pearl.plymouth.ac.uk/cgi/viewcontent.cgi?article=1866&context=bms-research

**Relevance.** This calibrates ShoreFor on twelve 5+ year shoreline datasets worldwide and generalises the free parameters. Castelle is a co-author, and Truc Vert is very likely one of the 12 sites **[verify]**. It is the canonical ShoreFor reference for baseline 4b and gives a no-calibration prior for parameters such as φ, which is useful with small n.

verified: yes

### 3.4 Castelle et al. (2014) — equilibrium shoreline modelling at Truc Vert ★
Castelle, B., Marieu, V., Bujan, S., Ferreira, S., Parisot, J.-P., Capo, S., Sénéchal, N., Chouzenoux, T. (2014). Equilibrium shoreline modelling of a high-energy meso-macrotidal multiple-barred beach. *Marine Geology* 347, 85–94. DOI: 10.1016/j.margeo.2013.11.003. OA: no.

**Relevance.** This is the **Truc Vert-specific equilibrium model** using the same OCA/EPOC survey programme as our data. It is the direct physics competitor for our task, although it targets shoreline position rather than ΔV. Agent C should reuse its calibrated parameters as a prior and compare against it **[verify parameter values and period]**.

verified: yes

### 3.5 D'Anna et al. (2020) — free-parameter uncertainty, 20-yr Truc Vert hindcast
D'Anna, M., Idier, D., Castelle, B., Le Cozannet, G., Rohmer, J., Robinet, A. (2020). Impact of model free parameters and sea-level rise uncertainties on 20-years shoreline hindcast: the case of Truc Vert beach (SW France). *Earth Surface Processes and Landforms* 45, 1895–1907. DOI: 10.1002/esp.4854. OA: green (HAL-BRGM hal-02514976).

**Relevance.** This shows that equilibrium-model **parameter non-identifiability** at Truc Vert yields wide prediction spread. It supports reporting parameter and prediction uncertainty for our physics baselines as well, not only for ML.

verified: yes

### 3.6 D'Anna et al. (2021) — shoreline projections to 2100 at Truc Vert
D'Anna, M., Castelle, B., Idier, D., Rohmer, J., Le Cozannet, G., Thieblemont, R., Bricheno, L. (2021). Uncertainties in shoreline projections to 2100 at Truc Vert beach (France): Role of sea-level rise and equilibrium model assumptions. *Journal of Geophysical Research: Earth Surface* 126, e2021JF006160. DOI: 10.1029/2021JF006160. OA: no (preprint on ESSOAr, DOI 10.1002/essoar.10506830.1).

**Relevance.** This is Truc Vert equilibrium modelling extended to projections. It is context for the discussion of how our event-scale model could feed long-term risk. BRGM co-authors (Idier, Rohmer, Le Cozannet) make it a natural link to Nicolae Lerma's institution.

verified: yes

### 3.7 Azorakos et al. (2024) — satellite-derived equilibrium modelling at Truc Vert ★
Azorakos, G., Castelle, B., Marieu, V., Idier, D. (2024). Satellite-derived equilibrium shoreline modelling at a high-energy meso-macrotidal beach. *Coastal Engineering* 191, 104536. DOI: 10.1016/j.coastaleng.2024.104536. OA: hybrid.

**Relevance.** This calibrates an equilibrium shoreline model at **Truc Vert** on 11 years (2009–2020) of satellite-derived shorelines. Even uncorrected satellite shorelines (RMSE about 30 m) give skill similar to in-situ calibration. The abstract notes that previous work showed equilibrium-model skill at Truc Vert "from hours (storms) to decades". This is the current state of the art at our site. Our paper must show what a **volume, event-scale** model adds beyond it. Azorakos is a ShoreShop 2.0 co-author (see 3.10).

verified: yes

### 3.8 Vitousek et al. (2017) — CoSMoS-COAST
Vitousek, S., Barnard, P.L., Limber, P., Erikson, L., Cole, B. (2017). A model integrating longshore and cross-shore processes for predicting long-term shoreline response to climate change. *Journal of Geophysical Research: Earth Surface* 122, 782–806. DOI: 10.1002/2016JF004065. OA: no.

**Relevance.** This is the transect-based one-line model with a Yates-type cross-shore term, longshore transport, sea-level rise and **data assimilation** (Kalman filter). It is relevant as the leading hybrid and assimilating model, and the reported ShoreShop 2.0 front-runner (see 3.10). It is not directly applicable to event-scale ΔV.

verified: yes

### 3.9 Montaño et al. (2020) — ShoreShop 1: blind testing of shoreline models
Montaño, J., Coco, G., Antolínez, J.A.A., Beuzen, T., Bryan, K.R., Cagigal, L., Castelle, B., Davidson, M.A., et al. (2020). Blind testing of shoreline evolution models. *Scientific Reports* 10, 2137. DOI: 10.1038/s41598-020-59018-y. OA: gold.

**Relevance.** This tested 19 models (shoreline and ML) at Tairua, NZ, on 18 years of video shorelines, with a calibration period of 1999–2014 and a blind forecast for 2014–2017. Skill dropped in the blind forecast period, "more evident for some of the machine learning algorithms", and **an ensemble beat individual models**. These are lessons for our protocol: blind hold-out, an ensemble baseline, and expecting ML degradation out of sample.

verified: yes

### 3.10 Mao et al. (2025) — ShoreShop 2.0 ★
Mao, Y., Coco, G., Vitousek, S., Antolínez, J.A.A., Azorakos, G., Banno, M., Bouvier, C., Bryan, K.R., et al. (2025). Benchmarking shoreline prediction models over multi-decadal timescales. *Communications Earth & Environment* 6, 581. DOI: 10.1038/s43247-025-02550-4. OA: gold, https://www.nature.com/articles/s43247-025-02550-4.pdf

**Relevance.** This was a blind competition with **34 groups** (confirmed in the abstract). Shorelines at an undisclosed site, "BeachX", were withheld over short (5-year) and medium (50-year) periods, with satellite-derived shorelines used for calibration and evaluation. The best models reached about 10 m accuracy, comparable to satellite shoreline error. The UNSW press release (Aug 2025) identifies BeachX as **Curl Curl, NSW**.

The HANDOFF claims that "CoSMoS-COAST narrowly won and ML models did well" (USGS news, 5 Aug 2025). That claim **could not be confirmed** from the abstract, the USGS publication page or the UNSW release: **[verify]** from the full-text ranking table before citing it. A short proceedings version also exists: Mao, Splinter, Coco (2026), "ShoreShop2.0: Blind testing of shoreline models", *Coastal Research Library* (Coastal Dynamics 2025), pp. 718–723, DOI 10.1007/978-3-032-15477-4_107 (Crossref metadata seen).

For us, the takeaway is to adopt the ShoreShop philosophy: a **pre-registered, blind hold-out** (the latest winters) and comparison against physics baselines.

verified: yes

### 3.11 Robinet et al. (2018) — LX-Shore
Robinet, A., Idier, D., Castelle, B., Marieu, V. (2018). A reduced-complexity shoreline change model combining longshore and cross-shore processes: The LX-Shore model. *Environmental Modelling & Software* 109, 1–16. DOI: 10.1016/j.envsoft.2018.08.010. OA: green, https://brgm.hal.science/hal-02734892v1/file/Manuscript_PostPrint.pdf

**Relevance.** This is the BRGM/EPOC reduced-complexity model (cross-shore via a ShoreFor-type term). It is the in-house regional modelling tool of the supervisors' institutions, so cite it when positioning the indicator within BRGM tools. A follow-on LX-ST model exists (Traboulsi et al., ICCE 2025, DOI 10.9753/icce.v38.currents.6; Crossref metadata seen, not opened).

verified: yes

### 3.12 Davidson et al. (2017) — annual prediction of erosion and recovery
Davidson, M.A., Turner, I.L., Splinter, K.D., Harley, M.D. (2017). Annual prediction of shoreline erosion and subsequent recovery. *Coastal Engineering* 130, 14–25. DOI: 10.1016/j.coastaleng.2017.09.008. OA: green, http://hdl.handle.net/10026.1/10259

**Relevance.** This is an equilibrium-model-based forecast of seasonal erosion and recovery with ensembles of wave scenarios. It is a template for turning our event model into a probabilistic seasonal outlook for the OCA network.

verified: yes

### 3.13 Splinter & Coco (2021) — challenges and opportunities in shoreline prediction
Splinter, K.D., Coco, G. (2021). Challenges and opportunities in coastal shoreline prediction. *Frontiers in Marine Science* 8, 788657. DOI: 10.3389/fmars.2021.788657. OA: gold.

**Relevance.** This perspective sets the agenda: data, model abstraction, hybrid and ML models, and benchmarking. It is good for the introduction.

verified: yes

### 3.14 Splinter, Turner & Davidson (2013) — how much data is enough?
Splinter, K.D., Turner, I.L., Davidson, M.A. (2013). How much data is enough? The importance of morphological sampling interval and duration for calibration of empirical shoreline models. *Coastal Engineering* 77, 14–27. DOI: 10.1016/j.coastaleng.2013.02.009. OA: no.

**Relevance.** This paper is directly about **survey interval and record length**, the 2017 thesis's main self-diagnosed weakness (2-week to 2-month gaps merging storms). Cite it to justify why the event definition depends on survey spacing and why the extended 2003–2019 record matters.

verified: yes

---

## Theme 4 — Machine learning for coastal morphodynamics

**Glossary.**
- **GP** (Gaussian process): a non-parametric regression that returns a mean and an uncertainty band. Well suited to small datasets.
- **Bayesian network**: a probabilistic graph linking variables through conditional probability tables.
- **LSTM/CNN**: deep-learning architectures for sequences and images.
- **SHAP**: a method that attributes each prediction to its input features.
- **Symbolic regression / GEP**: searches for an explicit equation that fits the data.
- **Mixture of experts**: several sub-models with a "gate" choosing which one to apply.

### 4.1 Goldstein, Coco & Plant (2019) — review of ML in coastal morphodynamics
Goldstein, E.B., Coco, G., Plant, N.G. (2019). A review of machine learning applications to coastal sediment transport and morphodynamics. *Earth-Science Reviews* 194, 97–108. DOI: 10.1016/j.earscirev.2019.04.022. OA: green (EarthArXiv).

**Relevance.** This is the standard review and our starting citation for "why ML". It discusses best practice for small data: train/test separation, overfitting, interpretability, and reporting.

verified: yes

### 4.2 Beuzen, Goldstein & Splinter (2019) — GP ensembles for runup and dune erosion ★
Beuzen, T., Goldstein, E.B., Splinter, K.D. (2019). Ensemble models from machine learning: an example of wave runup and coastal dune erosion. *Natural Hazards and Earth System Sciences* 19, 2295–2309. DOI: 10.5194/nhess-19-2295-2019. OA: gold, https://nhess.copernicus.org/articles/19/2295/2019/nhess-19-2295-2019.pdf

**Relevance.** This uses a **Gaussian-process** runup predictor, ensembled to give probabilistic runup, and then drives a dune-erosion model with it. It shows that "scatter is meaningful" and can be turned into prediction intervals. It is the exact template for (a) a probabilistic TWL/HAT exceedance in our forcing and (b) GP regression on our event table. The dune-erosion data source is **[verify]**.

verified: yes

### 4.3 Beuzen et al. (2018) — Bayesian networks, descriptive vs predictive
Beuzen, T., Splinter, K.D., Marshall, L.A., Turner, I.L., Harley, M.D., Palmsten, M.L. (2018). Bayesian Networks in coastal engineering: Distinguishing descriptive and predictive applications. *Coastal Engineering* 135, 16–30. DOI: 10.1016/j.coastaleng.2018.01.005. OA: no.

**Relevance.** This is a methodological warning that a Bayesian network fitted and evaluated on the same data is *descriptive*, not *predictive*. It parallels the 2017 PPT issue (mean profile computed on all data, selection on the target). Cite it in the audit narrative and the evaluation protocol.

verified: yes

### 4.4 Plant & Holland (2011) — Bayesian network for surf-zone prediction
Plant, N.G., Holland, K.T. (2011). Prediction and assimilation of surf-zone processes using a Bayesian network (Part I) **[verify part title]**. *Coastal Engineering* 58, 119–130. DOI: 10.1016/j.coastaleng.2010.09.003. OA: no. A companion paper with the same base title appears in *Coastal Engineering* 58, 256–266 (DOI 10.1016/j.coastaleng.2010.11.002).

**Relevance.** This is the USGS lineage of probabilistic coastal-change prediction (Plant/Stockdon). It is background for the probabilistic framing, and outside the window.

verified: yes

### 4.5 Simmons & Splinter (2022) — multi-model ensemble for storm erosion ★
Simmons, J.A., Splinter, K.D. (2022). A multi-model ensemble approach to coastal storm erosion prediction. *Environmental Modelling & Software* 150, 105356. DOI: 10.1016/j.envsoft.2022.105356. OA: no. A precursor is Simmons & Splinter (2020), "Combining data-driven and numerical modelling approaches to storm erosion prediction", *Coastal Engineering Proceedings* 36v, sediment.38, DOI 10.9753/icce.v36v.sediment.38 (Crossref metadata seen).

**Relevance.** This is the **closest methodological analogue** to our task: event-scale storm erosion prediction at Narrabeen combining ML and process models. A web search snippet of the proceedings says the combined model clearly beats either alone on the top-10% storms **[verify in the 2022 paper]**. Our paper must position against it, and its evaluation design is a model for ours.

verified: yes

### 4.6 Harley et al. (2023) — data-driven modelling of storm erosion at Narrabeen
Harley, M.D., Ibaceta, R., Leaman, C., Splinter, K.D., Turner, I.L. (2023). Data-driven modeling of coastal storm erosion: Narrabeen Beach, Australia. In *Coastal Sediments 2023*, World Scientific, 314–320. DOI: 10.1142/9789811275135_0028. OA: no.

**Relevance.** This is a direct ML storm-erosion model at a long-term monitored beach, the Australian analogue of what we propose for Truc Vert. Its method and features are **[verify]** (full text not accessed).

verified: yes

### 4.7 Itzkin et al. (2022) — process-based + data-driven forecasts of beach and dune change
Itzkin, M., Moore, L.J., Ruggiero, P., Hovenga, P.A., Hacker, S.D. (2022). Combining process-based and data-driven approaches to forecast beach and dune change. *Environmental Modelling & Software* 153, 105404. DOI: 10.1016/j.envsoft.2022.105404. OA: bronze.

**Relevance.** This is a hybrid (process + ML) precedent for beach and dune change. It supports our "physics baseline + ML residual" design. Details **[verify]**.

verified: yes

### 4.8 Gomez-de la Peña et al. (2023) — CNN / CNN-LSTM shoreline prediction
Gomez-de la Peña, E., Coco, G., Whittaker, C., Montaño, J. (2023). On the use of convolutional deep learning to predict shoreline change. *Earth Surface Dynamics* 11, 1145–1160. DOI: 10.5194/esurf-11-1145-2023. OA: gold.

**Relevance.** This applies CNN and CNN-LSTM to interannual shoreline change (Tairua NZ dataset), outperforming reference models. It needs **long, dense series**, whereas our event table (~37 to ~120 rows) does not support such architectures. Cite it in the "why we did not use deep sequence models" paragraph.

verified: yes

### 4.9 Adusumilli et al. (2024) — deep learning on satellite shorelines, California
Adusumilli, S., Cirrito, N., Engeman, L., Fiedler, J., Guza, R.T., Lange, A., Merrifield, M., O'Reilly, W., et al. (2024). Predicting shoreline changes along the California coast using deep learning applied to satellite observations. *JGR: Machine Learning and Computation* 1, e2024JH000172. DOI: 10.1029/2024JH000172. OA: gold.

**Relevance.** This combines 23 years of satellite waterlines with wave and tide model outputs and ground-truths against in-situ surveys. It shows satellite data can substitute for missing surveys, which is relevant for densifying our event timeline (see 5.1 and 5.4). *JGR-MLC* is also a candidate venue.

verified: yes

### 4.10 Calcraft et al. (2025) — mixture of experts for storm-dominated shorelines ★
Calcraft, K., Simmons, J.A., Marshall, L.A., Splinter, K.D. (2025). A mixture of experts approach to sandy shoreline modelling in storm dominated systems. *Coastal Engineering* 201, 104813. DOI: 10.1016/j.coastaleng.2025.104813. OA: hybrid.

**Relevance.** An LSTM is combined with a **specialised linear-regression storm model**, switched by a **peak-over-threshold gate**. Reported MSE skill scores are 0.37 (Narrabeen) and 0.63 (Gold Coast) relative to a standalone LSTM. This is strikingly close to our idea: a simple linear storm law (like EVI) inside a gated hybrid. It also shows the **skill-score-vs-baseline** reporting convention we should copy. The conference version is Calcraft et al., ICCE 2025, DOI 10.9753/icce.v38.management.44.

verified: yes

### 4.11 Calcraft et al. (2026) — generalised data-driven regional shoreline model
Calcraft, K., Simmons, J.A., Marshall, L.A., Splinter, K.D. (2026). A generalized data-driven shoreline model at the regional scale. *JGR: Machine Learning and Computation* 3, e2025JH000989. DOI: 10.1029/2025JH000989. OA: gold.

**Relevance.** This Temporal Fusion Transformer is trained across 2,000 km of SE Australia and tested on 30 unseen sites with a 5-year spatio-temporal hold-out (median RMSE 12.9 m). It shows the field is moving to **spatial generalisation**, which is relevant to our Biscarrosse/Aquitaine transfer test and to stating limits honestly.

verified: yes

### 4.12 Thilakarathne et al. (2024) — explainable AI (XGBoost + SHAP) for post-storm recovery
Thilakarathne, S., Suzuki, T., Mäll, M., Banno, M. (2024). Identifying key morphometrics to post-storm beach recovery through explainable AI. *Scientific Reports* 14, 14261. DOI: 10.1038/s41598-024-64023-6. OA: gold.

**Relevance.** This uses 104 storm events at Hasaki (Japan), four sandbar-based profile types, and XGBoost with SHAP for 10-day recovery. Its **event-table + gradient boosting + SHAP** design, at the same n-scale as ours, is the closest published template for our interpretability analysis. Note that the target is recovery, not erosion.

verified: yes

### 4.13 Holzenthal et al. (2026) — physics-informed ML for beach morphodynamics (Coastal Dynamics 2025)
Holzenthal, E.R., Anderson, D.L., Cohn, N., Johnson, B.D., Brodie, K.L. (2026). Physics-informed machine learning for beach morphodynamics prediction. In *Proceedings of Coastal Dynamics 2025*, Coastal Research Library, Springer, 69–75. DOI: 10.1007/978-3-032-15473-6_11. OA: hybrid (Springer PDF).

**Relevance.** This ML emulator predicts the Δz(x) profile at Duck FRF with **spatial and temporal dependence and sediment-conservation constraints**. Mass conservation is the natural physics constraint for our upper/lower ΔV split (sand crossing HAT). This is the "Holzenthal, Coastal Dynamics 2025" item in the HANDOFF, now confirmed (published 2026 in the proceedings volume).

verified: yes

### 4.14 Sénéchal & Coco (2024) — ANN shoreline prediction with sparse video data
Sénéchal, N., Coco, G. (2024). On the role of hydrodynamic and morphologic variables on neural network prediction of shoreline dynamics. *Geomorphology* 451, 109084. DOI: 10.1016/j.geomorph.2024.109084. OA: hybrid.

**Relevance.** A shallow ANN (one hidden layer, 10 inputs) on 3 years of video-derived shoreline and morphology data predicts 1-year shoreline with RMSE about 6.7 m. Deeper nets did not help. Varying inputs reveals the **bar's mitigating role during storms**. This matters for us in three ways: (a) Sénéchal is from the Bordeaux group, and the site is SW France (probably Biscarrosse or Truc Vert, **[verify]**); (b) it supports "small models for small data"; (c) it supports adding bar or beach-state variables if available. A Coastal Sediments 2023 precursor exists (Sénéchal, Peron, Coco; DOI 10.1142/9789811275135_0036).

verified: yes

### 4.15 Power et al. (2019) — Gene-Expression Programming for runup (symbolic regression)
Power, H.E., Gharabaghi, B., Bonakdari, H., Robertson, B., Atkinson, A.L., Baldock, T.E. (2019). Prediction of wave runup on beaches using Gene-Expression Programming and empirical relationships. *Coastal Engineering* 144, 47–61. DOI: 10.1016/j.coastaleng.2018.10.006. OA: green (figshare).

**Relevance.** This is the clearest coastal precedent for **symbolic regression** (GEP evolves explicit formulas). It benchmarks 7 empirical runup models and shows they err badly on unseen data (min RMSE 1.05 m) unless re-optimised. Two uses for us: it justifies the PySR "successor equation" idea, and it argues against blindly trusting Stockdon at Truc Vert. No published symbolic-regression law for **storm erosion volume** was found (see Gaps).

verified: yes

### 4.16 Montaño et al. (2021) — multiscale shoreline prediction
Montaño, J., Coco, G., Cagigal, L., Mendez, F., Rueda, A., Bryan, K.R., Harley, M.D. (2021). A multiscale approach to shoreline prediction. *Geophysical Research Letters* 48, e2020GL090587. DOI: 10.1029/2020GL090587. OA: not determined.

**Relevance.** This decomposes shoreline signals by timescale and models each separately. That supports separating storm-scale ΔV from seasonal recovery (our two-stage, classifier + regressor framing).

verified: yes

---

## Theme 5 — Remote sensing and datasets that unlock more events

### 5.1 Vos et al. (2019) — CoastSat
Vos, K., Splinter, K.D., Harley, M.D., Simmons, J.A., Turner, I.L. (2019). CoastSat: A Google Earth Engine-enabled Python toolkit to extract shorelines from publicly available satellite imagery. *Environmental Modelling & Software* 122, 104528. DOI: 10.1016/j.envsoft.2019.104528. OA: not determined (code is open on GitHub).

**Relevance.** This is the standard open toolkit for satellite-derived shorelines (Landsat/Sentinel-2). It can add shoreline observations between surveys to flag post-storm states. Its errors are about 10–30 m on meso-macrotidal beaches (see 5.4), too coarse for volume but useful as a classifier feature.

verified: yes

### 5.2 Vos et al. (2023) — benchmarking satellite-derived shoreline algorithms
Vos, K., Splinter, K.D., Palomar-Vázquez, J., Pardo-Pascual, J.E., Almonacid-Caballer, J., Cabezas-Rabadán, C., Kras, E.C., Luijendijk, A.P., et al. (2023). Benchmarking satellite-derived shoreline mapping algorithms. *Communications Earth & Environment* 4, 345. DOI: 10.1038/s43247-023-01001-2. OA: gold **[verify OA]**.

**Relevance.** This quantifies the accuracy of satellite-derived shoreline algorithms. Cite it to justify the error bars on any satellite-derived features.

verified: yes

### 5.3 Castelle et al. (2020) — 16 years of Truc Vert surveys (Scientific Data) ★
Castelle, B., Bujan, S., Marieu, V., Ferreira, S. (2020). 16 years of topographic surveys of rip-channelled high-energy meso-macrotidal sandy beach. *Scientific Data* 7, 410. DOI: 10.1038/s41597-020-00750-5. OA: gold.

**Relevance.** This is **the** data paper for our extended dataset (2003–2019 Truc Vert DGPS surveys). It is required both as a citation and as the basis for Agent B. It roughly doubles the events and adds 2015–2019. The data repository DOI and licence are to be taken from the paper by Agent B **[verify]**.

verified: yes

### 5.4 Castelle et al. (2021) — satellite-derived shorelines at Truc Vert
Castelle, B., Masselink, G., Scott, T., Stokes, C., Konstantinou, A., Marieu, V., Bujan, S. (2021). Satellite-derived shoreline detection at a high-energy meso-macrotidal beach. *Geomorphology* 383, 107707. DOI: 10.1016/j.geomorph.2021.107707. OA: not determined.

**Relevance.** This validates CoastSat-type satellite shorelines **at Truc Vert** against the survey record, including the effect of tide and runup corrections. It is the key reference for whether satellite data can extend our event timeline at this site.

verified: yes

### 5.5 Lubac et al. (2022) — satellite-derived bathymetry (SDB) in an energetic environment
Lubac, B., Burvingt, O., Nicolae Lerma, A., Sénéchal, N. (2022). Performance and uncertainty of satellite-derived bathymetry empirical approaches in an energetic coastal environment. *Remote Sensing* 14, 2350. DOI: 10.3390/rs14102350. OA: gold (MDPI).

**Relevance.** The 2017 thesis named the lack of **bar or bathymetry information** as a key gap. SDB in Aquitaine (with Nicolae Lerma as co-author) is the only scalable route to a bar-position feature. Whether the temporal coverage matches our events is **[verify]**.

verified: yes

### 5.6 Burvingt et al. (2025) — Pléiades stereo DEMs for dune change
Burvingt, O., Castelle, B., Marieu, V., Lubac, B., Nicolae Lerma, A., Robin, N. (2025). Using Pleiades satellite imagery to monitor multi-annual coastal dune morphological changes. *Remote Sensing* 17, 1522. DOI: 10.3390/rs17091522. OA: gold (MDPI).

**Relevance.** Satellite DEMs of the Aquitaine dune system are relevant to dune-volume targets and spatial transfer. Their temporal resolution is multi-annual, so they are not event-scale. Co-authored by Nicolae Lerma (connects to Agent E).

verified: yes

### 5.7 Laporte-Fauret et al. (2019) — low-cost UAV photogrammetry at Truc Vert
Laporte-Fauret, Q., Marieu, V., Castelle, B., Michalet, R., Bujan, S., Rosebery, D. (2019). Low-cost UAV for high-resolution and large-scale coastal dune change monitoring using photogrammetry. *Journal of Marine Science and Engineering* 7, 63. DOI: 10.3390/jmse7030063. OA: gold (MDPI).

**Relevance.** This covers UAV DEMs at Truc Vert (dune-focused), a possible extra data source for post-2019 events. Related: Laporte-Fauret et al. (2020), *JCR* SI 95, 163 (LiDAR + UAV, Truc Vert 2011–2019, DOI 10.2112/SI95-032.1; Crossref metadata seen).

verified: yes

### 5.8 Konstantinou et al. (2023) — satellite shorelines on high-energy macrotidal coasts and beach state
Konstantinou, A., Scott, T., Masselink, G., Stokes, K., Conley, D., Castelle, B. (2023). Satellite-based shoreline detection along high-energy macrotidal coasts and influence of beach state. *Marine Geology* 462, 107082. DOI: 10.1016/j.margeo.2023.107082. OA: not determined.

**Relevance.** This shows that satellite shoreline error depends on beach state (bars, rips). That is a caution if satellite-derived features are used for Truc Vert's rip-channelled beach.

verified: yes

### 5.9 Video monitoring at Truc Vert (via Angnuureng 2017, Sénéchal & Coco 2024)
No standalone data paper for the Truc Vert video system was found and verified. Its outputs are documented through Angnuureng et al. (2017) (entry 2.9) and the Bordeaux ANN work (entry 4.14). The camera details and period are **[verify]**.

verified: no (no single citable source identified)

### 5.10 SNO DYNALIT — national coastal observation service
SNO DYNALIT (Service National d'Observation "Dynamique du Littoral"), CNRS-INSU. This is the French national network of long-term monitored coastal sites. DYNALIT documents (IUEM Brest) describe 26 study sites and a label granted in 2014, and data cataloguing via ODATIS. Truc Vert is understood to be a DYNALIT site **[verify]**. No DOI was found. Cite through Castelle et al. (2020) and the DYNALIT web catalogue.

**Relevance.** The data-provenance and acknowledgement statement must cite DYNALIT and OCA correctly. Agent B should obtain the exact acknowledgement wording and dataset DOIs.

verified: no [verify]

---

## Methodological references (runup, TWL)

These are cited in the "must-haves" section below.

### M.1 Stockdon et al. (2006) — runup parameterisation
Stockdon, H.F., Holman, R.A., Howd, P.A., Sallenger, A.H. (2006). Empirical parameterization of setup, swash, and runup. *Coastal Engineering* 53, 573–588. DOI: 10.1016/j.coastaleng.2005.12.005. OA: no.

**Relevance.** This is the formula used in 2017. In the dissipative form, R2% = 0.043√(H₀L₀). The setup term contains 0.016√(H₀L₀), which is the source of the thesis typo noted in HANDOFF §2.1-10. The constant values follow the standard Stockdon (2006) form **[verify against the paper]**.

verified: yes

### M.2 Nicolae Lerma et al. (2017) — setup and runup on a complex barred beach (Truc Vert) ★
Nicolae Lerma, A., Pedreros, R., Robinet, A., Sénéchal, N. (2017). Simulating wave setup and runup during storm conditions on a complex barred beach. *Coastal Engineering* 123, 29–41. DOI: 10.1016/j.coastaleng.2017.01.011. OA: no.

**Relevance.** This is the supervisor's runup study at a **complex barred beach under storm conditions** (Truc Vert, **[verify]**). It is the natural replacement or sensitivity test for Stockdon in our TWL/HAT exceedance step. There is a 2016 *JCR* SI 75 precursor (DOI 10.2112/SI75-177.1).

verified: yes

### M.3 Atkinson et al. (2017) — runup model assessment
Atkinson, A.L., Power, H.E., Moura, T., Hammond, T., Callaghan, D.P., Baldock, T.E. (2017). Assessment of runup predictions by empirical models on non-truncated beaches on the south-east Australian coast. *Coastal Engineering* 119, 15–31. DOI: 10.1016/j.coastaleng.2016.10.001. OA: no.

**Relevance.** This is a multi-formula comparison showing the spread between runup formulas. It is used to justify reporting results under at least two runup formulas.

verified: yes

### M.4 Sénéchal et al. (2011) — runup during extreme storm conditions (Truc Vert)
Sénéchal, N., Coco, G., Bryan, K.R., Holman, R.A. (2011). Wave runup during extreme storm conditions. *Journal of Geophysical Research: Oceans* 116, C07032 [verify article number]. DOI: 10.1029/2010JC006819. OA: not determined.

**Relevance.** These are field runup observations at Truc Vert in an energetic storm (ECORS 2008 **[verify]**). As far as recalled, they show infragravity-dominated swash, with runup weakly dependent on the slope term **[verify]**. If confirmed, this means slope-dependent Stockdon terms are questionable in storms at our site. It is a key citation for the runup sensitivity test.

verified: yes

---

## Already done / closest prior work

**Bottom line.** No peer-reviewed paper was found that predicts **storm-erosion volume at Truc Vert (or anywhere on the Aquitaine coast) with machine learning** using forcing plus antecedent state.

Searches covered:
- Crossref bibliographic queries on combinations of Truc Vert, Aquitaine, Gironde, storm erosion, machine learning, neural network and random forest.
- Web searches on "machine learning storm erosion volume Truc Vert" and Aquitaine/Gironde ML erosion.

What exists:

1. **The 2017 EVI is already published.** Nicolae Lerma et al. (2018, *JCR* SI 85; entry 1.1), with R. Gillet as co-author, presents EVI and CRI inside the OCA storm EWS. They are calibrated on Truc Vert 2009–2015 and Biscarrosse, and EVI is said to give "fairly accurate eroded sediment volume". This is the honest baseline. The new paper is a **revisit and audit with extended data and modern models**, not a first proposal.
2. **Equilibrium models at Truc Vert predict shoreline, not volume.** These are Castelle et al. (2014), Splinter et al. (2014) **[verify Truc Vert inclusion]**, D'Anna et al. (2020, 2021) and Azorakos et al. (2024). They already encode the antecedent-disequilibrium idea at storm to decadal scales. Our contribution must be **event-scale volume** and an **EWS-oriented, uncertainty-aware** predictor, benchmarked against a volume-adapted equilibrium model.
3. **Truc Vert storm-cluster response is documented for the shoreline** from video (Angnuureng et al. 2017). A shallow ANN for shoreline exists in the same group (Sénéchal & Coco 2024; site **[verify]**). Neither targets ΔV per storm event.
4. **The closest ML storm-erosion-volume work is Australian (Narrabeen):** Simmons & Splinter (2022), Harley et al. (2023) and Calcraft et al. (2025, a gated linear-storm-model + LSTM). Beuzen et al. (2019) give the GP/probabilistic template. Thilakarathne et al. (2024, Hasaki) is the closest event-table + XGBoost + SHAP design, but for recovery.
5. **Grey literature to check.** BRGM report RP-67418-FR (2019, OCA storm network) is listed on the OCNA site, but its title and content could not be verified **[verify]**. It may contain an operational update of EVI and CRI after 2018. Agent E or Raphaël should obtain it before positioning claims are finalised.

---

## Methodological must-haves for a 2026 reviewer

### Evaluation protocol
- **Blind or held-out testing is now the norm.** ShoreShop 1 and 2 (Montaño et al. 2020; Mao et al. 2025) withheld data from modellers. Pre-register the hold-out (the most recent winters) and the metrics before fitting.
- Use **leave-one-winter-out** CV plus a final chronological hold-out (HANDOFF §3-C). Winter is the natural block, given the inter-annual forcing non-stationarity documented by Castelle et al. (2017, 2018).
- **Ensembles and baselines.** ShoreShop 1 found that an ensemble beat individual models and that ML degraded in the forecast period. Calcraft et al. (2025) report **MSE skill scores relative to a baseline**. Report skill vs (i) climatology, (ii) the 2017/2018 EVI, (iii) an equilibrium baseline (Yates 2009; ShoreFor via Davidson 2013 / Splinter 2014), and (iv) the Splinter et al. (2014) cluster relation.
- **Descriptive vs predictive.** Beuzen et al. (2018) warn against evaluating on the fitting data. Report only out-of-sample metrics as headline numbers.
- **Uncertainty.** Use GP/ensemble prediction intervals (Beuzen et al. 2019), and report bootstrap 95% CIs on metrics with n stated. The bootstrap is standard practice; no specific coastal citation was verified for it here.
- **Data requirements.** Splinter et al. (2013) and Simmons et al. (2019) justify a learning-curve analysis (skill vs number of calibration events).

### Units for storm energy (pick named quantities and test them as features)
- **Σ Hs² Δt** (m²·h): "storm power index" / Dolan & Davis (1992)-style. Dolan, R., Davis, R.E. (1992), "An intensity scale for Atlantic coast northeast storms", *Journal of Coastal Research* 8(4), 840–853. No DOI was found in Crossref (JSTOR item), so **verified: no [verify]**. It is used operationally by Mendoza et al. (2011, verified). The HANDOFF's "Harley 2009 ΣHs²Δt" could not be pinned to a DOI-registered paper. It is probably a Coasts & Ports 2009 proceedings paper by Harley, Turner, Short & Ranasinghe **[verify]**. Harley (2017, book chapter, verified) is a safer citation for storm metrics.
- **Time-integrated energy density** Σ (1/16) ρ g Hs² Δt (J·s/m², or J·h/m² if Δt is in hours). This is the 2017 quantity once units are fixed. It belongs to the same family as the Yates et al. (2009) energy forcing.
- **Time-integrated wave energy flux (power)** Σ ρ g² Hs² Tp/(64π) Δt (J/m). This is the forcing used by ShoreFor (Davidson et al. 2013), so it aligns our features with equilibrium baselines.
- **Exceedance-weighted variants** are SEI-like (Miller & Livermont 2009). They are only counted when TWL > threshold (HAT), which is the 2017 EVI concept.
- **Splinter et al. (2014, Coastal Eng.)** cluster relationship: the exact energy metric used is **[verify]** from the full text.

### Runup / TWL
- Report results under **Stockdon et al. (2006)** and at least one alternative.
- **Nicolae Lerma et al. (2017)** is the site-relevant storm runup study on a barred beach (supervisor's paper).
- **Atkinson et al. (2017)** and **Power et al. (2019)** quantify the spread across formulas and the poor transferability of uncalibrated formulas.
- **Sénéchal et al. (2011)** has Truc Vert storm runup observations. Check whether slope-dependence holds in storms **[verify]**.
- Fix the thesis typo: 0.016√(H₀L₀) is the setup term, not R2%.

### Storm definitions
- Use peak-over-threshold with explicit independence criteria (Harley 2017 chapter).
- Storm-sequence definitions vary by site (Eichentopf et al. 2019), so run a sensitivity analysis on the Hs95%/Hs75% choice.
- Storm Impact Scale (Sallenger 2000, *Journal of Coastal Research* 16(3), 890–895; no DOI found, **verified: no [verify]**). Use it with Stockdon et al. (2023) for collision/overwash regimes, which link to the CRI of Nicolae Lerma et al. (2018).
- **COSI**: no index by this name could be identified in Crossref or web searches. Ask the HANDOFF author what was meant **[verify]**.

---

## Gaps we can fill

- **An out-of-sample-evaluated, event-scale storm-erosion-volume model for Truc Vert does not exist.** The 2018 EVI is linear, calibrated and validated on overlapping or short periods, and (per HANDOFF §2.1) affected by units, leakage and selection on the target. A leave-one-winter-out, blind-hold-out benchmark on 2003–2019+ data is new.
- **Bridging indicator and equilibrium theory for volume.** Truc Vert equilibrium models target the shoreline. A *volume* disequilibrium term (Yates/ShoreFor style), used as a continuous antecedent-state feature in place of the 2017 binary label, has not been tested for event ΔV here.
- **Calibrated uncertainty for an EWS.** No Aquitaine storm-erosion predictor reports prediction intervals. GP or ensemble intervals (Beuzen 2019) can be mapped to OCA bulletin classes (cf. Leaman et al. 2021).
- **An interpretable successor law.** No symbolic-regression or SHAP study of storm-erosion *volume* was found. The closest are GEP for runup (Power et al. 2019) and SHAP for recovery (Thilakarathne et al. 2024). A compact PySR law with SHAP-checked drivers (energy, antecedent volume, berm, clustering, direction) would be novel.
- **Separating storm impact from inter-survey recovery** with a two-stage classifier→regressor. The mixture-of-experts gate idea (Calcraft et al. 2025) can be transposed to event tables. This addresses the "post-Klaus" problem explicitly.
- **Cross-site transfer on the same coast** (Truc Vert → Biscarrosse / OCA profiles; Nicolae Lerma et al. 2022; Biausque & Sénéchal 2019). The field is moving to generalisation (Calcraft et al. 2026), but not yet for event-scale volume in macrotidal Aquitaine.

---

## Summary counts

- Numbered annotated entries: **74** (30 in Themes 1–2, 14 in Theme 3, 16 in Theme 4, 10 in Theme 5, 4 methodological). **72 are verified** (Crossref metadata matched and DOI resolved via doi.org) and 2 are unverified (5.9 Truc Vert video, 5.10 SNO DYNALIT).
- Further references cited inline without their own entry (Crossref metadata seen, DOI not separately curl-checked unless listed in the .bib): Davidson 2013 corrigendum; Miller & Livermont 2008; Mao, Splinter & Coco 2026; Traboulsi 2025; Simmons & Splinter 2020; Calcraft ICCE 2025; Plant & Holland Part II; Sénéchal, Peron & Coco 2023; Laporte-Fauret 2020; Nicolae Lerma 2016.
- Unverified, no DOI: Dolan & Davis 1992; Sallenger 2000; "Harley 2009"; BRGM RP-67418-FR; COSI.
- BibTeX for all DOI-verified entries (generated from Crossref) is in `reports/D_references.bib`.

## Reproduce

Verification was done with the Crossref REST API (`https://api.crossref.org/works/<doi>`), OpenAlex (`https://api.openalex.org/works/doi:<doi>`) for abstracts and OA status, and `curl -s -o /dev/null -w '%{http_code}' -I https://doi.org/<doi>` (expect 302). BibTeX came from `https://api.crossref.org/works/<doi>/transform/application/x-bibtex`.
