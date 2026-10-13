# S — Sand physics and process literature for storm erosion and recovery at Truc Vert

**Agent S deliverable**, branch `revisit-2026`, compiled 13–14 Oct 2026. Extends `reports/D_state_of_the_art.md` (74 entries, not duplicated here) with the **physical processes** that control storm erosion and recovery on high-energy meso-macrotidal barred beaches. It is written for the paper's Discussion: *why does a cumulative wave-energy indicator saturate at R² ≈ 0.25–0.5 (STATUS §2), and what physics should the next model encode?*

**Status:** 72 annotated entries — **71 verified**, 1 unverified (Masselink & Short 1993, no DOI). Closing sections: (A) ranked physics the indicator ignores, (B) 10 candidate physics-informed features/model forms, (C) "does anyone already do this?". New BibTeX for the 71 verified entries is appended to `reports/D_references.bib`.

## How entries were verified (same rule as D)

- `verified: yes` means two checks passed: (1) the DOI's **Crossref** record (`api.crossref.org/works/<doi>`) gives the title, authors, year, journal, volume and pages printed here (the citation lines were generated programmatically from that record, so they cannot drift from it); (2) `curl -I https://doi.org/<doi>` returned HTTP 302 (DOI registered and resolving). All 71 passed on 13–14 Oct 2026.
- OA links come from OpenAlex `best_oa_location` (indicative; not opened one by one). "no" means closed or none found.
- The **Mechanism** and **Implication** notes are based on abstracts (OpenAlex/Semantic Scholar) where available and otherwise on prior knowledge of these well-known papers; any specific number, site or functional form not confirmed against an abstract is tagged **[verify]**. Many Elsevier abstracts were not retrievable through the open APIs, so treat untagged details of those entries as "standard textbook reading" and check numbers before quoting them in the paper.
- No DOI was invented. Two candidates were dropped during verification because their study site could not be confirmed (Gallagher et al. 2011, Mar. Geol. 287; Splinter et al. 2018, CSR 159). One recalled DOI (Bertin infragravity review) resolved to an unrelated paper and was corrected through a Crossref search.
- Not duplicated from D: Stockdon 2006, Sénéchal 2011 (JGR runup), Nicolae Lerma 2017, Atkinson 2017, Castelle 2015, Sénéchal 2019, Splinter 2014a/b, Yates 2009, Davidson 2013, Burvingt 2017/2018, Dodet 2019, Angnuureng 2017, Eichentopf 2019, Karunarathna 2014, Dissanayake 2015, Harley 2017b, Beuzen 2019a, Biausque & Sénéchal 2019, Stockdon 2023, Leaman 2021, Mendoza 2011. They are cited below by "(D)".

## Synthesis in one paragraph (for the Discussion)

The cumulative energy E = ΣHs²Δt is a measure of *offshore* forcing. The literature below shows that upper-beach volume change at a meso-macrotidal, double-barred beach is controlled by what reaches the swash zone, when, and on which profile: (i) the profile's distance from its storm equilibrium, so successive storms erode less (Coco et al. 2014 at Truc Vert; Eichentopf et al. 2020; Kriebel & Dean 1993); (ii) the tide level during peak waves (Coco et al. 2014 found tidal range and IG energy, not just wave height, explain upper-beachface change at Truc Vert); (iii) recovery that starts within days of the storm and is mixed into fortnightly surveys (Phillips et al. 2017, 2019); (iv) the bar system that filters and redistributes energy (Castelle et al. 2007; Almar et al. 2010); (v) infragravity swash, which is set by period and spectral shape as well as Hs (Ruessink et al. 1998; Bertin et al. 2018, 2020); and (vi) the thresholded, quadratic dependence of dune erosion on runup exceedance (Larson et al. 2004). Swash transport is the small residual of large opposing fluxes (Masselink & Puleo 2006; Blenkinsopp et al. 2011), which sets a noise floor. Physics-informed probabilistic models of event-scale change reach R² ≈ 0.2–0.3 elsewhere (Plant & Stockdon 2012). An R² of 0.25–0.5 for a linear energy indicator is therefore what the physics predicts, not a failure of fitting. The way forward is a small number of physically named terms (section B), not more flexible regressors on E.

---

## Theme 1 — Swash-zone and upper-beach sediment transport; infragravity swash

Why it matters for us: ΔV_upper (above HAT) is, by definition, sand moved by the swash and by the inner surf zone at high tide. The swash literature says that net transport there is a small residual of large, opposite gross fluxes, controlled by bore turbulence, infiltration, beach slope and (on dissipative storm beaches like Truc Vert) by infragravity (IG) motions that Hs alone does not describe.

### S1.1 Masselink & Puleo (2006) — swash-zone morphodynamics review
Masselink, G., Puleo, J.A. (2006). Swash-zone morphodynamics. *Continental Shelf Research* 26(5), 661-680. DOI: 10.1016/j.csr.2006.01.015. OA: no (closed or not found).

**Mechanism.** Review of swash hydrodynamics and sediment transport: uprush is dominated by bore-generated turbulence and advected sediment, backwash by bed shear stress; infiltration/exfiltration (groundwater table) and the swash–surf interaction modulate the net direction; net foreshore change is the small difference of large uprush and backwash fluxes and is notoriously hard to predict with energetics (u³) models.

**Implication.** A single Hs²-type energy cannot capture the sign of upper-beach change: the same forcing can produce erosion (high water table, saturated beach, large IG backwash) or accretion (moderate swell, unsaturated beach). This is the first-order physical reason why ΔV_upper ~ E has a low R² and a non-zero intercept. Suggests features describing swash *asymmetry* (wave steepness H/L, Iribarren ξ) rather than energy alone.

verified: yes

### S1.2 Masselink & Hughes (1998) — field swash sediment transport
Masselink, G., Hughes, M. (1998). Field investigation of sediment transport in the swash zone. *Continental Shelf Research* 18(10), 1179-1199. DOI: 10.1016/S0278-4343(98)00027-2. OA: no (closed or not found).

**Mechanism.** Field measurements showing swash sediment transport scales with u³ (Bagnold energetics) in both uprush and backwash, but with different efficiency coefficients for each phase [verify], so net transport depends on the uprush/backwash asymmetry.

**Implication.** Supports writing the upper-beach forcing as a time integral of swash velocity cubed (∝ (g·R)^{3/2}, i.e. runup-based) rather than Hs², and allows a sign-changing term (k_up − k_back) that an all-positive energy sum cannot represent.

verified: yes

### S1.3 Puleo et al. (2000) — swash suspension and bore turbulence
Puleo, J.A., Beach, R.A., Holman, R.A., Allen, J.S. (2000). Swash zone sediment suspension and transport and the importance of bore‐generated turbulence. *Journal of Geophysical Research: Oceans* 105(C7), 17021-17044. DOI: 10.1029/2000JC900024. OA: no (closed or not found).

**Mechanism.** Gleneden Beach (Oregon) observations: uprush suspension is concentrated at the bore front and is largely turbulence-generated, sediment settles at flow reversal, then is re-suspended in backwash; energetics models need an acceleration/turbulence term.

**Implication.** Erosion on the upper beach depends on bore intensity reaching the swash (i.e. on what survives surf-zone dissipation over the bars), not on offshore energy. Argues for a nearshore-transformed forcing (breaking wave height at the shore, or IG swash height) instead of offshore Hs.

verified: yes

### S1.4 Blenkinsopp et al. (2011) — swash sediment fluxes, field observations
Blenkinsopp, C.E., Turner, I.L., Masselink, G., Russell, P.E. (2011). Swash zone sediment fluxes: Field observations. *Coastal Engineering* 58(1), 28-44. DOI: 10.1016/j.coastaleng.2010.08.002. OA: no (closed or not found).

**Mechanism.** Event-resolved field fluxes of sediment in the swash (UK macrotidal beach [verify site]) show net transport per swash event is a small residual of large gross fluxes and highly variable from one event to the next; a few large events dominate the net change.

**Implication.** The upper-beach response is intrinsically noisy at the event scale; together with ±0.1 m survey error and longshore averaging it sets an *irreducible-noise floor* on ΔV_upper. Our R² ≈ 0.25–0.5 should be discussed against that floor, not against 1.

verified: yes

### S1.5 Ruessink, Kleinhans & van den Beukel (1998) — swash under highly dissipative conditions
Ruessink, B.G., Kleinhans, M.G., van den Beukel, P.G.L. (1998). Observations of swash under highly dissipative conditions. *Journal of Geophysical Research: Oceans* 103(C2), 3111-3118. DOI: 10.1029/97JC02791. OA: no (closed or not found).

**Mechanism.** Video swash at Terschelling (multiple bars, ξ₀ < 0.2): IG motions make up ~85 % of total swash height; IG swash ≈ 30 % of H₀ and only weakly related to beach slope.

**Implication.** At Truc Vert in storms (dissipative, double-barred) the water level that reaches the dune foot is set by IG swash, which scales with √(H₀L₀) or H₀ rather than with the foreshore slope. Supports using the dissipative Stockdon branch (0.043√(H₀L₀)) in storms and explains why the slope definition caused the 15.6 m TWL artefact in STATUS §3.

verified: yes

### S1.6 Ruggiero, Holman & Beach (2004) — runup on a high-energy dissipative beach
Ruggiero, P., Holman, R.A., Beach, R.A. (2004). Wave run‐up on a high‐energy dissipative beach. *Journal of Geophysical Research: Oceans* 109(C6), 2003JC002160. DOI: 10.1029/2003JC002160. OA: no (closed or not found).

**Mechanism.** Oregon storm runup was IG-dominated and varied by a factor 2 alongshore (26–61 % of offshore Hs), linearly dependent on the local foreshore slope, which varied by a factor 5.

**Implication.** Alongshore-variable foreshore slope (megacusps, rips) makes runup, and hence dune-collision time, vary alongshore; our 750–1500 m longshore-averaged profile mixes collision and non-collision segments. A feature like the *alongshore fraction of profiles in collision* would be more physical than a single averaged TWL.

verified: yes

### S1.7 Guza & Feddersen (2012) — frequency and directional spread effects on runup
Guza, R.T., Feddersen, F. (2012). Effect of wave frequency and directional spread on shoreline runup. *Geophysical Research Letters* 39(11), 2012GL051959. DOI: 10.1029/2012GL051959. OA: no (closed or not found).

**Mechanism.** Numerical experiments show IG runup increases for narrow-banded (swell-like) and narrow-directional spectra; scatter in empirical runup formulas is partly due to spectral shape omitted from (H₀, L₀, β).

**Implication.** Long-period, narrow-banded Atlantic storm swell (Tp 15–20 s at Truc Vert) produces larger IG swash than Hs and Tp alone predict. Candidate feature: directional spread or spectral peakedness from RESOURCECODE/WW3 spectra, or simply Hs·Tp (∝ energy flux × period) as the IG proxy.

verified: yes

### S1.8 Fiedler et al. (2015) — runup and energy flux on a low-slope beach with long-period swell
Fiedler, J.W., Brodie, K.L., McNinch, J.E., Guza, R.T. (2015). Observations of runup and energy flux on a low‐slope beach with high‐energy, long‐period ocean swell. *Geophysical Research Letters* 42(22), 9933-9941. DOI: 10.1002/2015GL066124. OA: no (closed or not found).

**Mechanism.** On a 1/80 beach with H₀ up to >7 m, runup increased linearly with √(H₀L₀); no saturation of runup was observed; an IG energy balance (shoaling + nonlinear transfer + dissipation) closed the budget.

**Implication.** Runup (and TWL) keeps growing with storm intensity, so saturation of the erosion indicator at high E is *not* a runup saturation; it must come from morphological feedback (bar dissipation, profile flattening, dune scarping, sediment exhaustion). This is a useful argument in the Discussion.

verified: yes

### S1.9 Inch et al. (2017) — nearshore IG wave dynamics under energetic swell (Perranporth)
Inch, K., Davidson, M., Masselink, G., Russell, P. (2017). Observations of nearshore infragravity wave dynamics under high energy swell and wind-wave conditions. *Continental Shelf Research* 138, 19-31. DOI: 10.1016/j.csr.2017.02.010. OA: https://pearl.plymouth.ac.uk/context/bms-research/article/1550/viewcontent/Inch_20et_20al_FINAL.pdf.

**Mechanism.** Macrotidal, dissipative Perranporth (UK): under energetic long-period swell, IG waves dominate the inner surf zone; IG energy depends on offshore short-wave energy and period, and is dissipated near the shoreline on the gentle slope [verify details].

**Implication.** Closest analogue in tide range and exposure to Truc Vert. Supports an IG proxy (Hs·Tp or Hs·Tp²) as a forcing feature separate from Hs², and tide-level dependence of IG at the shoreline (the beach slope seen by IG changes with tide on a barred macrotidal profile).

verified: yes

### S1.10 Bertin et al. (2018) — infragravity waves: from driving mechanisms to impacts (review)
Bertin, X., de Bakker, A., van Dongeren, A., Coco, G., André, G., Ardhuin, F., et al. (2018). Infragravity waves: From driving mechanisms to impacts. *Earth-Science Reviews* 177, 774-799. DOI: 10.1016/j.earscirev.2018.01.002. OA: https://amu.hal.science/hal-01731110v1/document.

**Mechanism.** Review of IG generation (bound-wave release, breakpoint forcing, bore merging), dissipation and reflection, and impacts: IG waves dominate swash on dissipative beaches, drive dune erosion and overwash, harbour seiching and sediment transport. Co-authored by the Bordeaux group (Bonneton, Castelle) and BRGM (Muller).

**Implication.** The authoritative citation for why runup at Truc Vert in storms is IG-controlled and why an Hs-only energy is incomplete. OA (HAL).

verified: yes

### S1.11 Bertin et al. (2020) — IG energy transfers and reflection at a dissipative beach under storm waves
Bertin, X., Martins, K., de Bakker, A., Chataigner, T., Guérin, T., Coulombier, T., de Viron, O. (2020). Energy Transfers and Reflection of Infragravity Waves at a Dissipative Beach Under Storm Waves. *Journal of Geophysical Research: Oceans* 125(5), e2019JC015714. DOI: 10.1029/2019jc015714. OA: no (closed or not found).

**Mechanism.** Storm Kurt (Feb 2017) at Saint-Trojan (Oléron, Bay of Biscay): incident Hs up to 9.5 m and Tp up to 22 s produced IG waves of up to 1.85 m near shore; XBeach reproduced them; generation mainly by the bound-wave mechanism.

**Implication.** Same storm climate as Truc Vert (≈150 km north). Demonstrates that during the very storms that dominate our ΔV, the shoreline water level is IG-dominated and period-sensitive. Strong case for including Tp (or Hs·Tp) explicitly and for XBeach-surfbeat as the process benchmark.

verified: yes

### S1.12 de Bakker et al. (2016) — cross-shore sand transport by IG waves vs beach steepness
de Bakker, A.T.M., Brinkkemper, J.A., van der Steen, F., Tissier, M.F.S., Ruessink, B.G. (2016). Cross-shore sand transport by infragravity waves as a function of beach steepness. *Journal of Geophysical Research: Earth Surface* 121(10), 1786-1799. DOI: 10.1002/2016jf003878. OA: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2016JF003878.

**Mechanism.** Field data show the IG sand flux direction depends on the correlation between IG orbital velocity and the short-wave envelope and on beach steepness: on gentle beaches with large H_IG/H_SW, IG motions themselves suspend and move sand and can reverse the net flux [verify direction per site].

**Implication.** IG contribution to transport is not just 'more energy' — its sign depends on profile slope, which is itself the antecedent state. Supports an interaction feature E × slope (or E × ξ) rather than E alone.

verified: yes

## Theme 2 — Berm, upper-beach morphodynamics and tidal modulation

Why it matters for us: the thesis itself blamed the missing berm before 2013–14 for dune-front retreat. On a meso-macrotidal beach (spring range ≈ 3.7–4 m at Truc Vert [verify]), the tide decides *which part of the profile* the storm swash attacks and for how long; a cumulative energy sum ignores both.

### S2.1 Phillips et al. (2019) — modes of berm and beachface recovery after storm reset (lidar)
Phillips, M.S., Blenkinsopp, C.E., Splinter, K.D., Harley, M.D., Turner, I.L. (2019). Modes of Berm and Beachface Recovery Following Storm Reset: Observations Using a Continuously Scanning Lidar. *Journal of Geophysical Research: Earth Surface* 124(3), 720-736. DOI: 10.1029/2018JF004895. OA: https://researchportal.bath.ac.uk/files/189954387/Phillips_et_al_2019_Journal_of_Geophysical_Research_Earth_Surface.pdf.

**Mechanism.** 5 Hz lidar at Narrabeen during 76 days of berm rebuilding after a storm removed it: recovery proceeds in distinct modes (beachface steepening, berm growth by overtopping swash at high/spring tides, berm-crest vertical accretion), each controlled by swash reach relative to the berm crest, i.e. by tide level and wave height together.

**Implication.** (i) Recovery is gated by water level, not just by low energy — so 'calm-weather recovery ≈ 6 m³/m/month' (thesis) should be modelled as a function of spring–neap phase and swash height. (ii) Pre-storm berm volume is a measurable state variable (sand above the berm crest/HAT) and a natural 'buffer' gate for dune erosion.

verified: yes

### S2.2 Almar et al. (2008) — video observations of beach cusp morphodynamics
Almar, R., Coco, G., Bryan, K.R., Huntley, D.A., Short, A.D., Senechal, N. (2008). Video observations of beach cusp morphodynamics. *Marine Geology* 254(3-4), 216-223. DOI: 10.1016/j.margeo.2008.05.008. OA: no (closed or not found).

**Mechanism.** Video-derived cusp formation, growth and destruction on an energetic French Atlantic beach (Truc Vert video system [verify site]); cusps develop under moderate shore-normal swell and are erased by storms; their spacing scales with swash excursion.

**Implication.** Cusps and megacusps redistribute upper-beach sand alongshore without net loss; with 750–1500 m alongshore averaging they mostly cancel, but at the scale of Castelle 2015 megacusp embayments they create hot-spots where the dune is reached first. An alongshore-variability metric (std of the HAT contour position) is a candidate state feature.

verified: yes

### S2.3 Masselink, Kroon & Davidson-Arnott (2006) — intertidal bar morphodynamics review
Masselink, G., Kroon, A., Davidson-Arnott, R.G.D. (2006). Morphodynamics of intertidal bars in wave-dominated coastal settings — A review. *Geomorphology* 73(1-2), 33-49. DOI: 10.1016/j.geomorph.2005.06.007. OA: no (closed or not found).

**Mechanism.** On meso-macrotidal beaches, the tide translates swash, surf and shoaling zones across the profile; intertidal bars (ridge–runnel, slip-face bars) respond to the time each elevation spends under each process; the stationary high-tide and low-tide positions receive disproportionate work.

**Implication.** The relevant forcing for ΔV above HAT is the energy delivered *while the water level is high*: a tide-weighted energy E_tide = Σ Hs² Δt · w(η_tide) (or the time the swash spends above a given elevation) is physically motivated. The 2017 HAT filter is a crude binary version of this weighting, which explains why it is 'weak by construction' (STATUS §2).

verified: yes

### S2.4 Short (2020) — wave-dominated, tide-modified and tide-dominated continuum (book chapter)
Short, A.D. (2020). Wave-dominated, tide-modified and tide-dominated continuum. *Sandy Beach Morphodynamics* , 363-389. DOI: 10.1016/b978-0-08-102927-5.00016-3. OA: no (closed or not found).

**Mechanism.** Updated beach-type classification by relative tide range RTR = TR/H_b combined with Ω: wave-dominated (RTR < 3), tide-modified (3–10), tide-dominated (> 10); tide-modified beaches have a reflective high-tide beach and a dissipative low-tide terrace.

**Implication.** Truc Vert sits near the wave-dominated/tide-modified boundary (storm H_b ~ 3–5 m, spring range ~ 4 m ⇒ RTR ≈ 1 in storms, ≈ 3–4 in summer [verify]). So the beach *changes type* between storms and calm periods, which is a physical argument for state-dependent (regime-switching) models. Verified citable substitute for Masselink & Short (1993).

verified: yes

### S2.5 Masselink & Short (1993) — the effect of tide range on beach morphodynamics (RTR conceptual model)
Masselink, G., Short, A.D. (1993). The effect of tide range on beach morphodynamics and morphology: a conceptual beach model. *Journal of Coastal Research* 9(3), 785–800. No DOI in Crossref (JSTOR item). OA: not determined.

**Mechanism.** Introduces RTR = TR/H_b with Ω to classify beaches; tidal translation reduces the time any single profile position is under swash/surf, reducing bar and berm development.

**Implication.** The classic citation for tide–wave phasing on macrotidal beaches; cite with Short (2020) for the verified version.

verified: no [verify — no DOI; check JSTOR page numbers]

### S2.6 Sénéchal et al. (2015) — storm impact on seasonal shoreline dynamics (Biscarrosse)
Senechal, N., Coco, G., Castelle, B., Marieu, V. (2015). Storm impact on the seasonal shoreline dynamics of a meso- to macrotidal open sandy beach (Biscarrosse, France). *Geomorphology* 228, 448-461. DOI: 10.1016/j.geomorph.2014.09.025. OA: no (closed or not found).

**Mechanism.** Multi-year video shorelines at Biscarrosse (same coast, 60 km south): storms are superimposed on the seasonal cycle; shoreline response to a storm depends on the antecedent position in the seasonal cycle and on storm timing/sequence, and some energetic events produce little retreat [verify specifics].

**Implication.** Same-coast evidence that response = f(forcing, antecedent state). Also relevant to the Biscarrosse transfer failure noted in the thesis (managed, nourished, chronically eroding beach).

verified: yes

## Theme 3 — Nearshore bar and rip dynamics at Truc Vert (bar state as the missing predictor)

Why it matters for us: the double-bar system decides where storm waves break and how much energy (and IG) reaches the beach; bar state also sets where the sand goes during and after storms. We have no bathymetry in the event table; this section collects the evidence on how large the missing-predictor effect is.

### S3.1 Castelle et al. (2007) — double-bar dynamics on the meso-macrotidal Aquitanian coast (review)
Castelle, B., Bonneton, P., Dupuis, H., Sénéchal, N. (2007). Double bar beach dynamics on the high-energy meso-macrotidal French Aquitanian Coast: A review. *Marine Geology* 245(1-4), 141-159. DOI: 10.1016/j.margeo.2007.06.001. OA: no (closed or not found).

**Mechanism.** Reference description of Truc Vert: inner intertidal bar in low-tide-terrace / transverse bar-and-rip states with rips spaced ~400 m; subtidal outer bar crescentic (wavelength ~700 m [verify]); mean Hs ≈ 1.4 m, Tp ≈ 6.5 s [verify], spring tidal range ≈ 4 m; medium sand (D50 ≈ 0.35 mm [verify]); outer bar can be straightened by storms; tide modulates breaking over the inner bar.

**Implication.** The site-description citation (grain size, tide, bar states). It establishes that storm energy passes through a *time-varying, alongshore non-uniform filter* (the bars), which is the most plausible missing predictor of ΔV for given offshore E.

verified: yes

### S3.2 Sénéchal et al. (2009) — morphodynamic response of a meso-macrotidal intermediate beach (long-term Truc Vert data)
Sénéchal, N., Gouriou, T., Castelle, B., Parisot, J.P., Capo, S., Bujan, S., Howa, H. (2009). Morphodynamic response of a meso- to macro-tidal intermediate beach based on a long-term data set. *Geomorphology* 107(3-4), 263-274. DOI: 10.1016/j.geomorph.2008.12.016. OA: no (closed or not found).

**Mechanism.** Multi-year topographic surveys at Truc Vert link inner-bar and upper-beach volume changes to wave forcing; seasonality is visible but strongly modulated by storm sequence and bar state [verify specifics].

**Implication.** Earliest analysis of the very survey series we use; check its reported correlations between wave forcing and profile volume to put our R² in context.

verified: yes

### S3.3 Sénéchal et al. (2011) — ECORS-Truc Vert'08 nearshore field experiment
Senechal, N., Abadie, S., Gallagher, E., MacMahan, J., Masselink, G., Michallet, H., et al. (2011). The ECORS-Truc Vert’08 nearshore field experiment: presentation of a three-dimensional morphologic system in a macro-tidal environment during consecutive extreme storm conditions. *Ocean Dynamics* 61(12), 2073-2098. DOI: 10.1007/s10236-011-0472-x. OA: http://dspace.library.uu.nl:8080/handle/1874/249154.

**Mechanism.** Six-week 2008 campaign (storms with offshore Hs up to ~8 m [verify]) documenting a 3D double-bar system, rips, wave transformation, IG waves and morphological change.

**Implication.** The data-rich reference period for Truc Vert storm processes (bathymetry, runup, currents). Any process-based benchmark (XBeach) of our events should be validated on ECORS 2008 first. OA (Utrecht repository).

verified: yes

### S3.4 Almar et al. (2010) — 2D/3D double-sandbar behaviour under intense wave forcing and meso-macro tidal range
Almar, R., Castelle, B., Ruessink, B.G., Sénéchal, N., Bonneton, P., Marieu, V. (2010). Two- and three-dimensional double-sandbar system behaviour under intense wave forcing and a meso–macro tidal range. *Continental Shelf Research* 30(7), 781-792. DOI: 10.1016/j.csr.2010.02.001. OA: no (closed or not found).

**Mechanism.** Video at Truc Vert: inner and outer bars respond differently to storms; high-energy events can straighten (2D reset) or reshape crescentic patterns; tide range modulates the inner-bar response [verify specifics].

**Implication.** Bar 'reset' events change the dissipation of later storms: a storm hitting a straightened outer bar transmits more energy to the beach than one hitting a well-developed crescentic bar with deep rips. A bar-state category (from Argus/satellite) or 'days since last bar reset' is a candidate feature.

verified: yes

### S3.5 Bruneau et al. (2009) — evolving rip current on a meso-macrotidal bar–rip beach (Truc Vert)
Bruneau, N., Castelle, B., Bonneton, P., Pedreros, R., Almar, R., Bonneton, N., et al. (2009). Field observations of an evolving rip current on a meso-macrotidal well-developed inner bar and rip morphology. *Continental Shelf Research* 29(14), 1650-1662. DOI: 10.1016/j.csr.2009.05.005. OA: no (closed or not found).

**Mechanism.** Field rip-current measurements during ECORS: rip flow is strongly tidally modulated (strongest at low/mid tide when breaking concentrates on the inner bar) and increases with wave height; rip channels evolve over days.

**Implication.** Shows that storm–tide phasing changes surf-zone circulation and offshore sand export from the beach; a storm peak at low tide moves sand from the inner bar while a storm peak at high tide attacks the upper beach. Supports tide-phase features.

verified: yes

### S3.6 Lafon et al. (2004) — rhythmic sandbars in SW France from satellite imagery
Lafon, V., De Melo Apoluceno, D., Dupuis, H., Michel, D., Howa, H., Froidefond, J.M. (2004). Morphodynamics of nearshore rhythmic sandbars in a mixed-energy environment (SW France): I. Mapping beach changes using visible satellite imagery. *Estuarine, Coastal and Shelf Science* 61(2), 289-299. DOI: 10.1016/j.ecss.2004.05.006. OA: no (closed or not found).

**Mechanism.** SPOT imagery maps inner- and outer-bar crescentic/rhythmic patterns along the Aquitaine coast and their migration and alongshore wavelength variability.

**Implication.** Shows that bar state can be retrieved from optical satellite imagery along this coast, which makes a bar-state feature (e.g. crescentic amplitude, distance of outer bar from shore) feasible for 2003–2019 via Sentinel-2/Landsat (cf. Lubac 2022 in D).

verified: yes

### S3.7 Price & Ruessink (2011) — state dynamics of a double sandbar system
Price, T.D., Ruessink, B.G. (2011). State dynamics of a double sandbar system. *Continental Shelf Research* 31(6), 659-674. DOI: 10.1016/j.csr.2010.12.018. OA: no (closed or not found).

**Mechanism.** Multi-year video of a double-barred beach: bars move between Wright–Short states; 'upstate' (towards 2D, reset) transitions are rapid in storms and 'downstate' transitions are slow; the two bars are coupled.

**Implication.** Asymmetric fast-reset/slow-recovery dynamics of the bars mirrors the beach volume (rapid erosion, slow recovery). A two-timescale or state-machine model with the bar state as latent variable is physically justified. Also suggests a simple feature: number of days since the last upstate transition (proxy: last storm above a high Hs threshold).

verified: yes

### S3.8 Masselink et al. (2014) — wave forcing, storms and NAO in outer-bar dynamics (macrotidal Perranporth)
Masselink, G., Austin, M., Scott, T., Poate, T., Russell, P. (2014). Role of wave forcing, storms and NAO in outer bar dynamics on a high-energy, macro-tidal beach. *Geomorphology* 226, 76-93. DOI: 10.1016/j.geomorph.2014.07.025. OA: http://hdl.handle.net/10026.1/3093.

**Mechanism.** On a high-energy macrotidal beach the outer bar migrates offshore during energetic periods and onshore during calm periods, following an equilibrium-type relation with wave forcing, and interannual bar position correlates with winter NAO [verify].

**Implication.** Bar position itself is predictable from antecedent forcing with an equilibrium model; we can build a *latent bar-position proxy* from wave history (Plant 1999-type) and use it as a feature when no bathymetry exists.

verified: yes

### S3.9 Hoefel & Elgar (2003) — wave-induced sediment transport and sandbar migration
Hoefel, F., Elgar, S. (2003). Wave-Induced Sediment Transport and Sandbar Migration. *Science* 299(5614), 1885-1887. DOI: 10.1126/science.1081448. OA: no (closed or not found).

**Mechanism.** Onshore bar migration is driven by acceleration skewness of near-breaking waves; offshore migration by undertow during breaking; the location of maximum transport moves with the bar, giving morphological feedback.

**Implication.** The physics of post-storm recovery (onshore bar migration) is driven by moderate, skewed swell — an energy *range*, not low energy. Recovery features should use moderate-wave energy (e.g. Σ Hs²Δt for Hs between ~1 and 2.5 m) rather than 'time without storms'.

verified: yes

### S3.10 Ruessink et al. (2007) — modelling cross-shore sandbar behaviour over weeks
Ruessink, B.G., Kuriyama, Y., Reniers, A.J.H.M., Roelvink, J.A., Walstra, D.J.R. (2007). Modeling cross‐shore sandbar behavior on the timescale of weeks. *Journal of Geophysical Research: Earth Surface* 112(F3), 2006JF000730. DOI: 10.1029/2006JF000730. OA: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2006JF000730.

**Mechanism.** A wave-averaged cross-shore model with skewness/asymmetry and undertow reproduces onshore and offshore bar migration at Duck, Hasaki and Egmond, with skill 0.5–0.8 after calibration.

**Implication.** Gives an order of magnitude for what a calibrated process model achieves on bar position over weeks; our event-scale statistical skill (~0.4–0.5) is in the same range, which is a fair comparison for the Discussion.

verified: yes

### S3.11 Dubarbier et al. (2015) — process-based modelling of cross-shore sandbar behaviour
Dubarbier, B., Castelle, B., Marieu, V., Ruessink, G. (2015). Process-based modeling of cross-shore sandbar behavior. *Coastal Engineering* 95, 35-50. DOI: 10.1016/j.coastaleng.2014.09.004. OA: https://www.sciencedirect.com/science/article/pii/S0378383914001781.

**Mechanism.** Coupled wave–current–sediment profile model separating four transport modes (velocity skewness, acceleration skewness, mean currents, slope): acceleration skewness gives slow onshore bar migration; undertow drives rapid offshore migration in storms. Bordeaux group (Castelle).

**Implication.** The process model already available in the Truc Vert group for the cross-shore problem; the sign of net transport depends on wave nonlinearity (Ursell number, i.e. Hs, T and depth) — another reason to include Tp and a nonlinearity proxy beside Hs². OA.

verified: yes

### S3.12 Dubarbier et al. (2017) — mechanisms of the complete accretionary beach state sequence
Dubarbier, B., Castelle, B., Ruessink, G., Marieu, V. (2017). Mechanisms controlling the complete accretionary beach state sequence. *Geophysical Research Letters* 44(11), 5645-5654. DOI: 10.1002/2017GL073094. OA: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2017GL073094.

**Mechanism.** First process-based simulation of the full downstate sequence from a storm-reset alongshore-uniform bar to a shore-welded terrace via crescentic and transverse-bar/rip states; contributions of different transport modes vary through the sequence.

**Implication.** Recovery after a storm is a multi-week morphological sequence whose stage sets the beach's vulnerability to the next storm. 'Time since last reset' and the moderate-energy integral since reset are physically meaningful antecedent features.

verified: yes

## Theme 4 — Dune erosion physics (impact/collision models, avalanching, dune-toe retreat)

Why it matters for us: the largest ΔV events (2013–14) are dune-scarping events. Collision-regime models say erosion is proportional not to wave energy but to how far and how long the runup exceeds the dune toe — a quadratic, thresholded functional of TWL. This is the most direct physical replacement for E.

### S4.1 Overton, Fisher & Young (1988) — laboratory investigation of dune erosion
Overton, M.F., Fisher, J.S., Young, M.A. (1988). Laboratory Investigation of Dune Erosion. *Journal of Waterway, Port, Coastal, and Ocean Engineering* 114(3), 367-373. DOI: 10.1061/(ASCE)0733-950X(1988)114:3(367). OA: no (closed or not found).

**Mechanism.** Single-uprush tank experiments on a vertical dune: eroded volume per uprush correlates strongly with the uprush force (momentum flux) at the dune.

**Implication.** Foundation of impact models: erosion ∝ swash force at the dune toe, i.e. ∝ (R − z_toe)-dependent, not ∝ Hs² offshore.

verified: yes

### S4.2 Larson, Erikson & Hanson (2004) — analytical model of dune erosion due to wave impact
Larson, M., Erikson, L., Hanson, H. (2004). An analytical model to predict dune erosion due to wave impact. *Coastal Engineering* 51(8-9), 675-696. DOI: 10.1016/j.coastaleng.2004.07.003. OA: no (closed or not found).

**Mechanism.** Wave-impact theory: per-swash dune erosion is proportional to the impact force, leading to ΔV = 4 C_s (R − z_toe)² (t/T) for R > z_toe (C_s an empirical coefficient ~10⁻⁴–10⁻³ [verify], T wave period, t duration), with dune-toe rise and slope updates.

**Implication.** Directly computable from our forcing: **I_Larson = Σ_{TWL>z_toe} (TWL − z_toe)² Δt / Tp**. It is thresholded, quadratic in exceedance and inversely weighted by period — very different from E = ΣHs²Δt. The obvious first physics-informed feature (needs a dune-toe elevation per survey, or HAT as fallback).

verified: yes

### S4.3 Erikson, Larson & Hanson (2007) — beach scarp and dune recession by notching and failure
Erikson, L.H., Larson, M., Hanson, H. (2007). Laboratory investigation of beach scarp and dune recession due to notching and subsequent failure. *Marine Geology* 245(1-4), 1-19. DOI: 10.1016/j.margeo.2007.04.006. OA: https://www.sciencedirect.com/science/article/pii/S0025322707001016.

**Mechanism.** Laboratory: swash notches the dune base, the overhang fails by slumping/avalanching; recession proceeds in discrete failures; the impact coefficient C_s was calibrated.

**Implication.** Dune erosion is episodic and partly delayed (slumps after the high tide), adding noise at the event scale; the eroded dune sand is deposited on the upper beach, so ΔV above HAT can *under-represent* dune loss (mass is moved, not exported). Argues for reporting dune volume and beach volume separately.

verified: yes

### S4.4 Palmsten & Holman (2012) — laboratory dune erosion with stereo video
Palmsten, M.L., Holman, R.A. (2012). Laboratory investigation of dune erosion using stereo video. *Coastal Engineering* 60, 123-135. DOI: 10.1016/j.coastaleng.2011.09.003. OA: no (closed or not found).

**Mechanism.** Large-flume stereo-video dune erosion: erosion rate relates to the water level/runup exceedance of the dune toe; the dune toe rises during erosion, reducing exceedance (self-limiting feedback) [verify].

**Implication.** Self-limitation (toe rise ⇒ less exceedance) is a mechanism for **saturation of erosion at high energy**: the indicator should include a decaying efficiency, e.g. exceedance computed relative to an evolving toe, or a concave transform of E.

verified: yes

### S4.5 Palmsten & Splinter (2016) — runup during a laboratory dune erosion experiment
Palmsten, M.L., Splinter, K.D. (2016). Observations and simulations of wave runup during a laboratory dune erosion experiment. *Coastal Engineering* 115, 58-66. DOI: 10.1016/j.coastaleng.2016.01.007. OA: https://doi.org/10.1016/j.coastaleng.2016.01.007.

**Mechanism.** Measured runup during dune erosion compared with empirical formulas and XBeach; the runup on an eroding dune deviates from formulas built for natural beach slopes; the definition of the slope matters [verify specifics].

**Implication.** Mirrors our own runup-slope artefact (STATUS §3, scarped profile ⇒ reflective Stockdon branch ⇒ 15.6 m TWL). Justifies using a fixed foreshore slope or the dissipative form in storms.

verified: yes

### S4.6 van Rijn (2009) — prediction of dune erosion due to storms
van Rijn, L.C. (2009). Prediction of dune erosion due to storms. *Coastal Engineering* 56(4), 441-457. DOI: 10.1016/j.coastaleng.2008.10.006. OA: no (closed or not found).

**Mechanism.** Parametric dune-erosion model fitted to the DUROSTA process model and lab data: dune erosion above storm surge level increases with surge level, Hs, wave period and storm duration and decreases with grain size [verify functional form]; profile slope and initial profile matter.

**Implication.** Shows that period and water level enter separately from Hs, and that duration enters sub-linearly. Our Σ Hs²Δt imposes linear duration dependence; a test of E^p (p < 1) or duration-saturating forms is warranted.

verified: yes

### S4.7 Kriebel & Dean (1993) — convolution method for time-dependent beach-profile response
Kriebel, D.L., Dean, R.G. (1993). Convolution Method for Time‐Dependent Beach‐Profile Response. *Journal of Waterway, Port, Coastal, and Ocean Engineering* 119(2), 204-226. DOI: 10.1061/(ASCE)0733-950X(1993)119:2(204). OA: no (closed or not found).

**Mechanism.** Profile erosion relaxes exponentially toward an equilibrium erosion set by water level and breaking height; the response is a convolution of forcing with an exponential kernel of time scale T_s (hours to tens of hours); short storms realise only a fraction of their potential erosion.

**Implication.** Explicit physics for **saturation**: ΔV = V_∞(TWL,H_b)·[1 − exp(−t_storm/T_s)] (for constant forcing). With T_s ~ 10–30 h [verify], long storms saturate, which bends the ΔV–E relation and caps R² of a linear fit. Candidate model form for C.

verified: yes

### S4.8 Stockdon et al. (2007) — simple model for spatially variable coastal response to hurricanes
Stockdon, H.F., Sallenger, A.H., Holman, R.A., Howd, P.A. (2007). A simple model for the spatially-variable coastal response to hurricanes. *Marine Geology* 238(1-4), 1-20. DOI: 10.1016/j.margeo.2006.11.004. OA: no (closed or not found).

**Mechanism.** Implements the Sallenger (2000) storm impact scale (swash / collision / overwash / inundation) by comparing R_high and R_low (setup + runup) with dune toe and crest elevations; predicted regimes match observed response alongshore.

**Implication.** The regime framework behind the CRI of Nicolae Lerma et al. (2018). Feature: **hours in collision regime** (R2% + η > z_toe) per event. Sallenger, A.H. (2000), *J. Coastal Res.* 16(3), 890–895 has no DOI (see D, verified: no).

verified: yes

### S4.9 Mull & Ruggiero (2014) — storm-induced dune erosion and overtopping, US West Coast
Mull, J., Ruggiero, P. (2014). Estimating Storm-Induced Dune Erosion and Overtopping along U.S. West Coast Beaches. *Journal of Coastal Research* 298, 1173-1187. DOI: 10.2112/JCOASTRES-D-13-00178.1. OA: no (closed or not found).

**Mechanism.** Compares geometric and impact-type dune-erosion models (including a Larson-type wave-impact model) on high-energy, dissipative US West Coast beaches; models need regional calibration of the impact coefficient and slope handling.

**Implication.** Closest high-energy dissipative analogue for applying Larson-type models; supports calibrating one C_s on our events and reporting its uncertainty.

verified: yes

### S4.10 Cohn et al. (2019) — environmental and morphologic controls on wave-induced dune response
Cohn, N., Ruggiero, P., García-Medina, G., Anderson, D., Serafin, K.A., Biel, R. (2019). Environmental and morphologic controls on wave-induced dune response. *Geomorphology* 329, 108-128. DOI: 10.1016/j.geomorph.2018.12.023. OA: https://doi.org/10.1016/j.geomorph.2018.12.023.

**Mechanism.** Pacific Northwest dune volume change during high-water storms increases with backshore beach slope; on low-sloping dissipative beaches wave processes can even *build* the lower dune.

**Implication.** Same TWL can erode or accrete the dune depending on backshore slope: include slope (or its interaction with exceedance) as a state feature; ΔV of mixed sign at given E is physically expected.

verified: yes

### S4.11 Splinter, Kearney & Turner (2018) — drivers of alongshore-variable dune erosion
Splinter, K.D., Kearney, E.T., Turner, I.L. (2018). Drivers of alongshore variable dune erosion during a storm event: Observations and modelling. *Coastal Engineering* 131, 31-41. DOI: 10.1016/j.coastaleng.2017.10.011. OA: http://hdl.handle.net/1959.4/unsworks_52023.

**Mechanism.** Daily lidar of a 2011 storm at Narrabeen: alongshore variation in pre-storm beach width/slope, dune-toe elevation and dune height explained much of the variable dune erosion; a Larson-type model with local pre-storm morphology reproduced it [verify skill].

**Implication.** Pre-storm subaerial morphology (dune toe elevation, beach width) is a first-order predictor alongside forcing; our continuous antecedent anomaly is a scalar proxy for it and could be replaced by toe elevation + beach width above HAT.

verified: yes

### S4.12 de Winter, Gongriep & Ruessink (2015) — alongshore variability in dune erosion at Egmond aan Zee
de Winter, R.C., Gongriep, F., Ruessink, B.G. (2015). Observations and modeling of alongshore variability in dune erosion at Egmond aan Zee, the Netherlands. *Coastal Engineering* 99, 167-175. DOI: 10.1016/j.coastaleng.2015.02.005. OA: https://www.sciencedirect.com/science/article/pii/S0378383915000307.

**Mechanism.** Observations plus XBeach show substantial alongshore variability in dune erosion during a storm, attributed to alongshore variability in pre-storm beach/dune morphology [verify role of bars].

**Implication.** Longshore averaging over 750–1500 m hides this variability; supports reporting the alongshore std of ΔV as part of the uncertainty.

verified: yes

### S4.13 Splinter & Palmsten (2012) — modelling dune response to an East Coast Low
Splinter, K.D., Palmsten, M.L. (2012). Modeling dune response to an East Coast Low. *Marine Geology* 329-331, 46-57. DOI: 10.1016/j.margeo.2012.09.005. OA: no (closed or not found).

**Mechanism.** Compares a Larson-type wave-impact model and XBeach on a 2009 Gold Coast storm; both reproduce dune erosion when calibrated; impact-model skill depends on the runup estimate and C_s.

**Implication.** Precedent for using a simple impact model as a physics baseline next to a process model; the dominant uncertainty is the runup estimate, as in our TWL analysis.

verified: yes

## Theme 5 — Recovery, aeolian supply and equilibrium/disequilibrium physics

Why it matters for us: every ΔV between two surveys is storm erosion *plus* recovery (or further erosion) during the non-storm days. Survey spacing is our binding limit (STATUS §2); this section gives the physics and timescales needed to model the recovery term explicitly instead of treating it as noise.

### S5.1 Phillips et al. (2017) — shoreline recovery and the role of sandbar morphodynamics
Phillips, M.S., Harley, M.D., Turner, I.L., Splinter, K.D., Cox, R.J. (2017). Shoreline recovery on wave-dominated sandy coastlines: the role of sandbar morphodynamics and nearshore wave parameters. *Marine Geology* 385, 146-159. DOI: 10.1016/j.margeo.2017.01.005. OA: http://handle.unsw.edu.au/1959.4/unsworks_47171.

**Mechanism.** 10 years of daily video at Narrabeen, 82 storms: mean recovery rate ~0.2 m/day, highest in the first 1–2 weeks; recovery is fastest when the bar migrates onshore and welds, and depends on post-storm wave height/steepness.

**Implication.** Recovery is front-loaded (exponential-like) and bar-mediated: a post-storm recovery term R(Δt) = R_max·(1 − exp(−Δt_post/τ)) with τ ~ 1–2 weeks, modulated by moderate-wave energy, is a defensible way to correct ΔV for the time between storm end and the next survey.

verified: yes

### S5.2 Scott et al. (2016) — 2013/14 storms: beach recovery along SW England
Scott, T., Masselink, G., O'Hare, T., Saulter, A., Poate, T., Russell, P., Davidson, M., Conley, D. (2016). The extreme 2013/2014 winter storms: Beach recovery along the southwest coast of England. *Marine Geology* 382, 224-241. DOI: 10.1016/j.margeo.2016.10.011. OA: https://www.sciencedirect.com/science/article/pii/S0025322716302766/pdf.

**Mechanism.** Post-2013/14 recovery was spatially variable and incomplete after ~2 years at many sites; recovery rates depend on post-storm wave climate and on where the sand went (bars offshore vs alongshore).

**Implication.** Recovery depends on *where* storm sediment is stored; extreme winters can push sand beyond the active bar zone, which means a temporarily reduced sand supply for later recovery — a reason why the beach's 'memory' outlasts single-winter models.

verified: yes

### S5.3 Castelle et al. (2017) — foredune changes and beach recovery after 2013/14 at Truc Vert
Castelle, B., Bujan, S., Ferreira, S., Dodet, G. (2017). Foredune morphological changes and beach recovery from the extreme 2013/2014 winter at a high-energy sandy coast. *Marine Geology* 385, 41-55. DOI: 10.1016/j.margeo.2016.12.006. OA: no (closed or not found).

**Mechanism.** At Truc Vert, the 2013/14 winter scarped the foredune; the beach recovered over the following ~2 years while the foredune recovered more slowly via aeolian supply and slumping; recovery was alongshore variable (megacusp embayments) [verify numbers].

**Implication.** The most site-specific recovery reference. Provides the dune vs beach timescale separation (beach: months; dune: years) for a two-reservoir model and supports using dune-toe position as an antecedent state (a scarped, retreated dune toe is more exposed in the next winters).

verified: yes

### S5.4 Guillot et al. (2018) — UAV monitoring of 3-year foredune partial recovery at Truc Vert
Guillot, B., Castelle, B., Marieu, V., Bujan, S., Rosebery, D. (2018). UAV monitoring of 3-year Foredune Partial Recovery from a Severe Winter: Truc Vert Beach, SW France. *Journal of Coastal Research* 85, 276-280. DOI: 10.2112/si85-056.1. OA: no (closed or not found).

**Mechanism.** UAV photogrammetry shows only partial foredune recovery three years after 2013/14 at Truc Vert, with alongshore variable aeolian accretion.

**Implication.** Confirms multi-year dune memory: a dune-volume deficit relative to pre-2013 is a slowly decaying state variable that modulates the effect of later storms.

verified: yes

### S5.5 Laporte-Fauret et al. (2020) — dune morphology evolution from lidar and UAV, Truc Vert 2011–2019
Laporte-Fauret, Q., Castelle, B., Marieu, V., Bujan, S., Michalet, R., Rosebery, D. (2020). Coastal Dune Morphology Evolution Combining Lidar and UAV Surveys, Truc Vert beach 2011-2019. *Journal of Coastal Research* 95(sp1), 163. DOI: 10.2112/si95-032.1. OA: no (closed or not found).

**Mechanism.** Lidar and UAV DEMs quantify dune volume changes 2011–2019 at Truc Vert, showing erosion in 2013/14 and subsequent aeolian-driven recovery with strong alongshore variability.

**Implication.** Source of a second response variable (dune volume) for 2011–2019 matching our event period; cited in D only inline.

verified: yes

### S5.6 Walker et al. (2017) — scale-dependent perspectives on beach–dune systems
Walker, I.J., Davidson-Arnott, R.G.D., Bauer, B.O., Hesp, P.A., Delgado-Fernandez, I., Ollerhead, J., Smyth, T.A.G. (2017). Scale-dependent perspectives on the geomorphology and evolution of beach-dune systems. *Earth-Science Reviews* 171, 220-253. DOI: 10.1016/j.earscirev.2017.04.011. OA: https://doi.org/10.1016/j.earscirev.2017.04.011.

**Mechanism.** Review of beach–dune sediment exchange across scales: storm erosion (wave-driven, beach → nearshore) vs aeolian supply (beach → dune), supply-limited vs transport-limited regimes, vegetation feedback.

**Implication.** Frames ΔV above HAT as the sum of wave- and wind-driven fluxes; aeolian export of upper-beach sand to the dune during energetic, onshore-wind storms can make ΔV_upper negative without any wave erosion.

verified: yes

### S5.7 Bauer et al. (2009) — aeolian transport on a beach: moisture, fetch and mean transport
Bauer, B.O., Davidson-Arnott, R.G.D., Hesp, P.A., Namikas, S.L., Ollerhead, J., Walker, I.J. (2009). Aeolian sediment transport on a beach: Surface moisture, wind fetch, and mean transport. *Geomorphology* 105(1-2), 106-116. DOI: 10.1016/j.geomorph.2008.02.016. OA: no (closed or not found).

**Mechanism.** Field experiment showing beach aeolian transport is limited by surface moisture and fetch geometry (wind angle × beach width), so it is rarely at its potential rate.

**Implication.** Aeolian supply to the dune increases with beach width above HAT and onshore wind, both of which a berm provides; recovery features should include wind (e.g. ERA5 onshore wind-speed exceedance) and beach width.

verified: yes

### S5.8 Delgado-Fernandez (2010) — fetch effect and sand supply to foredunes
Delgado-Fernandez, I. (2010). A review of the application of the fetch effect to modelling sand supply to coastal foredunes. *Aeolian Research* 2(2-3), 61-70. DOI: 10.1016/j.aeolia.2010.04.001. OA: https://research.edgehill.ac.uk/en/publications/fccb7207-933e-46d1-8f3d-04d703150200.

**Mechanism.** Review of the fetch effect: transport increases with downwind distance up to a critical fetch (metres in wind tunnels, >100 m in the field).

**Implication.** At Truc Vert (dry beach widths ~50–100 m), fetch is often limiting; a narrow post-storm beach supplies little sand to the dune, so dune recovery lags beach recovery — a mechanistic basis for the two-timescale recovery term.

verified: yes

### S5.9 Houser (2009) — synchronisation of transport and supply in beach–dune interaction
Houser, C. (2009). Synchronization of transport and supply in beach-dune interaction. *Progress in Physical Geography: Earth and Environment* 33(6), 733-746. DOI: 10.1177/0309133309350120. OA: no (closed or not found).

**Mechanism.** Dune growth requires the synchronisation of sediment supply to the backshore (nearshore bar welding, berm building) and wind transport events.

**Implication.** Supports a gated recovery model: aeolian dune recovery only when berm/beach volume is above a threshold. Same 'gate' idea as the mixture-of-experts gate in D (Calcraft 2025).

verified: yes

### S5.10 Wright & Short (1984) — morphodynamic variability of surf zones and beaches
Wright, L.D., Short, A.D. (1984). Morphodynamic variability of surf zones and beaches: A synthesis. *Marine Geology* 56(1-4), 93-118. DOI: 10.1016/0025-3227(84)90008-2. OA: no (closed or not found).

**Mechanism.** Beach-state model (dissipative → intermediate → reflective) organised by the dimensionless fall velocity Ω = H_b/(w_s T); erosion/accretion and bar states follow changes in Ω.

**Implication.** Ω, not E, is the classical control on erosion vs accretion (Ω > Ω_eq ⇒ erosion). With D50 ≈ 0.35 mm (w_s ≈ 0.04–0.05 m/s [verify]) Ω is computable from our Hs and Tp; a storm-mean Ω and its anomaly vs a weighted antecedent Ω are candidate features.

verified: yes

### S5.11 Wright, Short & Green (1985) — short-term changes in beach state: empirical predictive model
Wright, L.D., Short, A.D., Green, M.O. (1985). Short-term changes in the morphodynamic states of beaches and surf zones: An empirical predictive model. *Marine Geology* 62(3-4), 339-364. DOI: 10.1016/0025-3227(85)90123-9. OA: no (closed or not found).

**Mechanism.** Beach state changes at a rate proportional to the disequilibrium between the current Ω and a weighted antecedent Ω (exponential memory with a decay of days to weeks).

**Implication.** The physical origin of ShoreFor's weighted Ω (Davidson 2013, in D). Event feature: ΔΩ = Ω_storm − Ω_eq(φ), with φ the memory (fit or ~ 5–30 days), used in a disequilibrium term c·P^{1/2}·ΔΩ. Directly links to our Equilibrium-B model, which gave the small consistent gain.

verified: yes

### S5.12 Ludka et al. (2015) — field evidence of beach profile evolution toward equilibrium
Ludka, B.C., Guza, R.T., O'Reilly, W.C., Yates, M.L. (2015). Field evidence of beach profile evolution toward equilibrium. *Journal of Geophysical Research: Oceans* 120(11), 7574-7597. DOI: 10.1002/2015jc010893. OA: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2015JC010893.

**Mechanism.** Quarterly profiles (back beach to 8 m depth) at five southern-California beaches: first-EOF profile amplitude evolves toward an equilibrium with wave energy (Yates-type), with sand exchanged cross-shore between the subaerial beach and the 4–8 m depth zone.

**Implication.** Equilibrium models work for *profile volume*, not only shoreline, when the profile is surveyed deeply enough; supports our volume-adapted equilibrium model and highlights that our subaerial-only volume misses the offshore storage. OA.

verified: yes

## Theme 6 — Sediment properties and budgets

Why it matters for us: m³/m volumes need a porosity convention, grain size controls Ω and w_s, and the Aquitaine coast has strong longshore drift — so a closed cross-shore budget cannot be assumed.

### S6.1 Beard & Weyl (1973) — texture, porosity and permeability of unconsolidated sand
Beard, D.C., Weyl, P.K. (1973). Influence of Texture on Porosity and Permeability of Unconsolidated Sand. *AAPG Bulletin* 57(2), 349-369. DOI: 10.1306/819a4272-16c5-11d7-8645000102c1865d. OA: no (closed or not found).

**Mechanism.** Packing experiments: wet-packed porosity ≈ 42 % for extremely well-sorted sand down to ≈ 28 % for very poorly sorted sand, nearly independent of grain size.

**Implication.** Our ΔV is a bulk volume (sand + pores). For a well-sorted medium beach sand use porosity ≈ 0.35–0.40 to convert to solid volume or mass (×(1 − n)·ρ_s ≈ 1.6–1.7 t per m³ bulk). State this explicitly in Methods if volumes are compared with transport models (which predict solid volumes).

verified: yes

### S6.2 Abadie et al. (2006) — wave climate and longshore drift on the South Aquitaine coast
Abadie, S., Butel, R., Mauriet, S., Morichon, D., Dupuis, H. (2006). Wave climate and longshore drift on the South Aquitaine coast. *Continental Shelf Research* 26(16), 1924-1939. DOI: 10.1016/j.csr.2006.06.005. OA: no (closed or not found).

**Mechanism.** Wave-climate analysis and longshore transport formulas give a net southward drift along the Aquitaine coast driven by WNW–NW swells, with large interannual variability (order 10⁵ m³/yr [verify]).

**Implication.** Storm-scale longshore gradients can add or remove sand at the profile independently of cross-shore energy. Direction × Hs (longshore energy flux P_l ∝ Hs^{5/2} sin 2θ) is the physical feature; its gradient, not its magnitude, matters, so a single-profile model will only capture it through local shoreline orientation changes (megacusps). Our null direction ablation is consistent with this.

verified: yes

### S6.3 Castelle et al. (2018) — shoreline change of the 280-km Aquitaine coast, 1950–2014
Castelle, B., Guillot, B., Marieu, V., Chaumillon, E., Hanquiez, V., Bujan, S., Poppeschi, C. (2018). Spatial and temporal patterns of shoreline change of a 280-km high-energy disrupted sandy coast from 1950 to 2014: SW France. *Estuarine, Coastal and Shelf Science* 200, 212-223. DOI: 10.1016/j.ecss.2017.11.005. OA: no (closed or not found).

**Mechanism.** Long-term shoreline change along the Gironde/Landes coast is alongshore variable, with chronic erosion hot-spots and stable/accreting sectors, explained by longshore-transport gradients, headland/inlet effects and wave-climate variability.

**Implication.** Truc Vert is in a near-stable sector [verify], so the long-term trend can be neglected at event scale but not at decadal scale; Biscarrosse (thesis transfer failure) is in a different budget context. Use as justification that cross-site transfer needs a budget term.

verified: yes

### S6.4 Valiente et al. (2019) — waves, tides and depth of closure
Valiente, N.G., Masselink, G., Scott, T., Conley, D., McCarroll, R.J. (2019). Role of waves and tides on depth of closure and potential for headland bypassing. *Marine Geology* 407, 60-75. DOI: 10.1016/j.margeo.2018.10.009. OA: https://www.sciencedirect.com/science/article/pii/S0025322718302342/pdf.

**Mechanism.** Macrotidal, high-energy SW England: depth of closure at event to multi-annual scales is deeper than microtidal formulas predict because tides shift the wave action across depths; storms move sand to depths beyond the surveyed profile.

**Implication.** Part of the storm-eroded sand at Truc Vert may leave the 0–350 m topographic profile entirely (to the outer bar or beyond), so ΔV_total is not conserved — recovery then depends on shoreface supply over months to years. Supports treating 'sand exported beyond the profile' as an unobserved state.

verified: yes

## Theme 7 — Storm hydrodynamic forcing: energy vs flux vs TWL, sequence and surge

Why it matters for us: these papers justify which forcing quantity is physically meaningful and why the order of storms matters.

### S7.1 Mendoza & Jiménez (2006) — storm classification based on beach-erosion potential (Catalonia)
Mendoza, E.T., Jiménez, J.A. (2006). A Storm Classification Based on the Beach Erosion Potential in the Catalonian Coast. *Coastal Dynamics 2005* , 1-11. DOI: 10.1061/40855(214)98. OA: no (closed or not found).

**Mechanism.** Storms classed by energy content were re-classified by SBEACH-simulated erosion (retreat, eroded volume); a parametric erosion potential based on storm characteristics (Hs, duration, period) reproduces SBEACH bulk erosion.

**Implication.** Precedent for an energy-based storm index *calibrated on a process model* rather than on noisy surveys; it shows that erosion potential is not proportional to energy content alone (period and duration enter separately). Mendoza et al. (2011) in D is the follow-up.

verified: yes

### S7.2 Coco et al. (2014) — beach response to a sequence of extreme storms (Truc Vert, ECORS'08) ★
Coco, G., Senechal, N., Rejas, A., Bryan, K.R., Capo, S., Parisot, J.P., Brown, J.A., MacMahan, J.H.M. (2014). Beach response to a sequence of extreme storms. *Geomorphology* 204, 493-501. DOI: 10.1016/j.geomorph.2013.08.028. OA: http://hdl.handle.net/10261/403474.

**Mechanism.** Daily surveys over one month (>100 000 m²) at Truc Vert during ECORS'08: **no cumulative storm effect** appeared; a ~10-year return-period storm (Hs 8.1 m) eroded far less than its wave height suggested, which the authors attribute to neap tides, shore-normal short waves or low IG energy; regression links upper-beachface volume change to offshore wave characteristics, **tidal range** and **inner-surf-zone IG energy** (abstract, via NPS open copy).

**Implication.** The single most important site-specific citation for our Discussion: at Truc Vert, upper-beach ΔV at storm scale is controlled by tide range and IG energy as much as by offshore wave energy, so an Hs²-sum indicator must saturate. Directly motivates the tide-weighted and IG-proxy features in section B. Co-authored by Sénéchal (supervisor-side). Online 2013, print 2014. OA copy: https://calhoun.nps.edu/bitstream/10945/41277/1/Coco%20et%20al.%2c%202013%20Geomorpho.pdf

verified: yes

### S7.3 Vousdoukas, Almeida & Ferreira (2012) — erosion and recovery during consecutive storms (meso-tidal Faro)
Vousdoukas, M.I., Almeida, L.P.M., Ferreira, Ó. (2012). Beach erosion and recovery during consecutive storms at a steep‐sloping, meso‐tidal beach. *Earth Surface Processes and Landforms* 37(6), 583-593. DOI: 10.1002/esp.2264. OA: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/esp.2264.

**Mechanism.** Six consecutive storms on a steep meso-tidal beach: antecedent morphology initially dominated the response, then storm wave/tide conditions; recovery occurred between storms; tide level during peak waves mattered.

**Implication.** Meso-tidal evidence for both the antecedent-state effect and the storm–tide phasing effect. OA.

verified: yes

### S7.4 Eichentopf et al. (2020) — storm sequencing in large-scale experiments
Eichentopf, S., van der Zanden, J., Cáceres, I., Baldock, T.E., Alsina, J.M. (2020). Influence of storm sequencing on breaker bar and shoreline evolution in large-scale experiments. *Coastal Engineering* 157, 103659. DOI: 10.1016/j.coastaleng.2020.103659. OA: https://www.sciencedirect.com/science/article/pii/S0378383919303023.

**Mechanism.** Large-wave-flume sequences of two storms of different energy plus recovery phases: bar and shoreline evolve towards an equilibrium for each wave condition; the order of storms and the recovery-wave energy and duration change the final profile.

**Implication.** Controlled evidence that ΔV for a storm depends on the profile left by the previous storm — i.e. a state-space (equilibrium) model, not an energy sum, is the correct structure. OA.

verified: yes

### S7.5 Gomes da Silva et al. (2020) — prediction of runup, setup and swash on beaches (review)
Gomes da Silva, P., Coco, G., Garnier, R., Klein, A.H.F. (2020). On the prediction of runup, setup and swash on beaches. *Earth-Science Reviews* 204, 103148. DOI: 10.1016/j.earscirev.2020.103148. OA: http://dspace.azti.es/handle/24689/1130.

**Mechanism.** Review and re-test of empirical runup/setup/swash models on a large field database; nearshore bathymetry (bars) is an important source of error; slope definitions and IG dominance on dissipative beaches explain much of the scatter.

**Implication.** Justifies the runup sensitivity test (STATUS §4 item 4) and quantifies the TWL uncertainty that propagates into any exceedance-based feature (≈ ±30 % on R2% [verify]).

verified: yes

### S7.6 Bertin et al. (2015) — contribution of short waves to storm surges in the Bay of Biscay
Bertin, X., Li, K., Roland, A., Bidlot, J.R. (2015). The contribution of short-waves in storm surges: Two case studies in the Bay of Biscay. *Continental Shelf Research* 96, 1-15. DOI: 10.1016/j.csr.2015.01.005. OA: no (closed or not found).

**Mechanism.** Coupled wave–circulation modelling of two Bay of Biscay storms (incl. Xynthia [verify]) shows wave setup and wave-dependent surface stress add tens of cm to the surge near the coast.

**Implication.** Our water level = tide + tide-gauge residual (Arcachon) omits shoreline wave setup (taken from Stockdon) but the residual at Arcachon inlet may include some setup; avoid double counting and note that surge on the open Aquitaine coast is modest (~0.3–0.8 m [verify]) so tide phase dominates TWL variability.

verified: yes

## Theme 8 — Process-based models of storm erosion and what they say about energy → erosion

Why it matters for us: process models are the reference against which a statistical indicator must be positioned; their calibration experience also tells us how much skill to expect.

### S8.1 Roelvink et al. (2009) — XBeach: modelling storm impacts on beaches, dunes and barrier islands
Roelvink, D., Reniers, A., van Dongeren, A., van Thiel de Vries, J., McCall, R., Lescinski, J. (2009). Modelling storm impacts on beaches, dunes and barrier islands. *Coastal Engineering* 56(11-12), 1133-1152. DOI: 10.1016/j.coastaleng.2009.08.006. OA: https://zenodo.org/record/3416271.

**Mechanism.** XBeach resolves wave-group (surfbeat) IG motions, avalanching of the dune face (critical wet/dry slopes), and swash/collision/overwash regimes; dune erosion is driven by IG swash plus avalanching rather than by mean energy.

**Implication.** The process benchmark: an XBeach-1D hindcast of the 2013–14 events at Truc Vert (bathymetry from ECORS/Castelle) would give a physics-based ΔV to compare with the EVI. OA (Zenodo).

verified: yes

### S8.2 Kobayashi (2016) — coastal sediment transport modelling for engineering (CSHORE)
Kobayashi, N. (2016). Coastal Sediment Transport Modeling for Engineering Applications. *Journal of Waterway, Port, Coastal, and Ocean Engineering* 142(6), 03116001. DOI: 10.1061/(ASCE)WW.1943-5460.0000347. OA: no (closed or not found).

**Mechanism.** CSHORE: time-averaged cross-shore model with roller, probabilistic swash zone and wet/dry transitions, bed- and suspended-load, permeable layer; designed to be fast and robust for dune erosion.

**Implication.** A cheaper process model than XBeach for running hundreds of events; could be used to generate a *physics-simulated* erosion feature for each event (hybrid physics-ML).

verified: yes

### S8.3 Callaghan, Ranasinghe & Roelvink (2013) — probabilistic storm erosion with analytical, semi-empirical and process models
Callaghan, D.P., Ranasinghe, R., Roelvink, D. (2013). Probabilistic estimation of storm erosion using analytical, semi-empirical, and process based storm erosion models. *Coastal Engineering* 82, 64-75. DOI: 10.1016/j.coastaleng.2013.08.007. OA: no (closed or not found).

**Mechanism.** Compares Kriebel–Dean-type analytical, Larson-type semi-empirical (SBEACH-like) and XBeach estimates of storm-erosion exceedance probabilities at Narrabeen; models agree on order of magnitude but differ substantially in the tails.

**Implication.** Even process models disagree by a factor ~2 on extreme-event erosion; a statistical indicator with RMSE ~9 m³/m on ΔV_upper is in a comparable uncertainty band. Useful framing for 'why R² saturates' and for an ensemble of physics features.

verified: yes

### S8.4 Simmons et al. (2017) — calibrating and assessing uncertainty in coastal numerical models (GLUE)
Simmons, J.A., Harley, M.D., Marshall, L.A., Turner, I.L., Splinter, K.D., Cox, R.J. (2017). Calibrating and assessing uncertainty in coastal numerical models. *Coastal Engineering* 125, 28-41. DOI: 10.1016/j.coastaleng.2017.04.005. OA: http://handle.unsw.edu.au/1959.4/unsworks_46950.

**Mechanism.** GLUE calibration of XBeach (and a simpler model) for storm erosion shows strong parameter equifinality and parameter-induced uncertainty.

**Implication.** Process models need event-scale calibration data of exactly the type we have; their posterior uncertainty is a fair yardstick for our prediction intervals (C's conformal widths 34–40 m³/m).

verified: yes

### S8.5 Pender & Karunarathna (2013) — statistical-process approach for beach profile variability
Pender, D., Karunarathna, H. (2013). A statistical-process based approach for modelling beach profile variability. *Coastal Engineering* 81, 19-29. DOI: 10.1016/j.coastaleng.2013.06.006. OA: https://www.sciencedirect.com/science/article/pii/S0378383913001142/pdf.

**Mechanism.** Combines statistical storm-climate simulation with XBeach for storms and an empirical recovery model between storms to simulate annual–decadal profile variability (Narrabeen).

**Implication.** Template for a hybrid model separating storm erosion (process/indicator) and inter-storm recovery (empirical), exactly the decomposition our survey spacing requires. OA.

verified: yes

### S8.6 den Heijer, Baart & van Koningsveld (2012) — probabilistic dune failure along the Dutch coast
den Heijer, C.(., Baart, F., van Koningsveld, M. (2012). Assessment of dune failure along the Dutch coast using a fully probabilistic approach. *Geomorphology* 143-144, 95-103. DOI: 10.1016/j.geomorph.2011.09.010. OA: https://zenodo.org/record/3418389.

**Mechanism.** Fully probabilistic (Monte-Carlo) assessment of dune failure using the DUROS+ parametric dune-erosion model with joint surge/wave statistics.

**Implication.** Operational precedent for using a parametric, physics-based erosion volume (not an energy regression) in hazard assessment; DUROS-type volumes depend on surge level, Hs, Tp and D50. OA.

verified: yes

### S8.7 Plant & Stockdon (2012) — probabilistic prediction of barrier-island response to hurricanes
Plant, N.G., Stockdon, H.F. (2012). Probabilistic prediction of barrier‐island response to hurricanes. *Journal of Geophysical Research: Earth Surface* 117(F3), 2011JF002326. DOI: 10.1029/2011JF002326. OA: no (closed or not found).

**Mechanism.** Recasts the Sallenger impact-scale conceptual model as a Bayesian network with TWL, dune height and pre-storm morphology; dune-crest elevation change predicted with ~20–30 % explained variance (Santa Rosa Island).

**Implication.** A physics-informed probabilistic model achieving R² ≈ 0.2–0.3 — the same ballpark as our EVI. Strong external evidence that event-scale morphological change is only partly predictable from forcing + simple state.

verified: yes
---

## A. Physics the energy indicator ignores (ranked)

Ranking = (strength of evidence that the mechanism changes event-scale ΔV for a given E) × (relevance to a meso-macrotidal, double-barred, high-energy beach). The column "our evidence" quotes STATUS §2 / C ablations; where we found nothing, it is often because the feature was a crude proxy, not because the physics is absent.

| # | Mechanism | What it does to ΔV for a given E | Papers that quantify it | Data we would need | Our evidence so far |
|---|---|---|---|---|---|
| 1 | **Morphological feedback / storm equilibrium (sequence saturation)** | Once the profile approaches its storm-equilibrium shape, extra energy produces little extra erosion; the 2nd/3rd storm of a cluster erodes less (concave ΔV–E, saturation). | Coco et al. 2014 (Truc Vert: no cumulative effect); Eichentopf et al. 2020 (lab); Kriebel & Dean 1993 (exponential response); Wright, Short & Green 1985; Vousdoukas et al. 2012; D: Splinter 2014, Davidson 2013, Yates 2009 | Pre-storm profile (have); a profile-equilibrium target (fit) | Equilibrium-B gives the only consistent (non-significant) gain; cluster *count* gave none ⇒ encode sequence through state, not counts |
| 2 | **Tide–storm phasing (water level during peak waves)** | The same storm at spring high tide attacks the upper beach/dune; at neap or low tide it works on the inner bar. RTR changes the beach type. | Coco et al. 2014 (tidal range in regression); Masselink, Kroon & Davidson-Arnott 2006; Bruneau et al. 2009; Short 2020; Masselink & Short 1993 [verify]; Vousdoukas et al. 2012 | Hourly tide + surge (have) | Only tested as a binary HAT gate, which is weak by construction (TWL ≥ HAT 21–27 % of steps) ⇒ untested as a continuous weight |
| 3 | **Post-storm recovery inside the survey interval** | Onshore bar migration and berm rebuilding start within days at rates ~0.2 m/day shoreline (Narrabeen) and refill the upper beach before the next survey. | Phillips et al. 2017, 2019; Hoefel & Elgar 2003; Dubarbier et al. 2015, 2017; Scott et al. 2016; Castelle et al. 2017 | Storm-end-to-survey lag and moderate-wave energy (have); higher-frequency surveys (Biscarrosse EPOC, video) | Keeping long intervals destroys skill (−0.21) ⇒ first-order; not yet modelled explicitly |
| 4 | **Nearshore bar state (dissipation filter)** | Outer/inner bar position and 3D state set how much energy and IG reaches the beach and where rips focus erosion (megacusps). | Castelle et al. 2007; Almar et al. 2010; Sénéchal et al. 2011; Price & Ruessink 2011; Masselink et al. 2014; Gomes da Silva et al. 2020; Castelle 2015 (D) | Bar crest distance/depth or bar state per event (satellite: Lafon 2004, Lubac 2022 in D; Argus video); or a latent bar proxy from wave history | Not testable with current data (no bathymetry) |
| 5 | **Infragravity swash / wave period and spectral shape** | On dissipative storm beaches IG swash sets runup (Rig/R ≈ 0.85); long-period narrow-band swell gives larger runup and erosion than Hs² implies. | Ruessink et al. 1998; Ruggiero et al. 2004; Guza & Feddersen 2012; Fiedler et al. 2015; Inch et al. 2017; Bertin et al. 2018, 2020; de Bakker et al. 2016; Coco et al. 2014 | Tp (have), spectra/directional spread (RESOURCECODE), IG measurements (ECORS only) | Energy flux (∝ Hs²Tp) "not better" than ΣHs²Δt — but flux is a weak IG proxy; Hs·Tp and exceedance forms untested |
| 6 | **Berm presence and dune-toe elevation (buffer + threshold)** | A berm absorbs the storm and must be removed before the dune is attacked; dune erosion ∝ (R − z_toe)² only when R > z_toe. | Larson et al. 2004; Overton et al. 1988; Palmsten & Holman 2012; Stockdon et al. 2007; Splinter, Kearney & Turner 2018; Cohn et al. 2019; Phillips et al. 2019; D: Beuzen 2019a | Dune-toe elevation and berm volume per survey (extractable from profiles; needs a robust toe-picking routine — the thesis gave up and used HAT) | Binary pre-state (PPT) helps in-sample only; continuous anomaly no effect on ΔV_upper ⇒ the *right* state variable (toe, berm) not yet tried |
| 7 | **Sediment supply/export and aeolian exchange** | Sand pushed beyond the profile (outer bar, below closure) is unavailable for recovery; wind moves upper-beach sand into the dune (ΔV_upper < 0 without wave erosion). | Valiente et al. 2019; Ludka et al. 2015; Castelle et al. 2017; Guillot et al. 2018; Walker et al. 2017; Bauer et al. 2009; Houser 2009; Delgado-Fernandez 2010 | Dune volume (LiDAR/UAV: Laporte-Fauret 2020), wind (ERA5 — no credentials yet), deeper bathymetry | Not tested |
| 8 | **Wave direction / longshore gradients** | Longshore transport gradients add/remove sand locally; oblique storms erode embayment sectors more. | Abadie et al. 2006; Castelle et al. 2018 (ECSS); Ruggiero et al. 2004; D: Harley 2017b | Direction (have); alongshore-resolved profiles/DEMs | Direction ablation: none (consistent with a straight, longshore-averaged profile) |

Reading of the table for the Discussion: mechanisms 1–3 act *in time* (state, phase, recovery) and are partly computable from data we already hold; 4–5 act *in space through the nearshore* and need bathymetry or spectra; 6 is a profile-derived state we have but have not extracted; 7–8 are budget terms that a single longshore-averaged profile cannot close. A linear energy sum captures none of them, which is sufficient to explain an R² ceiling of ~0.25–0.5 together with the survey-noise floor (Blenkinsopp et al. 2011; ±0.1 m survey error) and the external benchmark that physics-informed Bayesian models of event-scale change reach R² ≈ 0.2–0.3 (Plant & Stockdon 2012).

---

## B. Candidate physics-informed features and model forms (computable now unless stated)

Notation: η(t) = tide + residual (m MSL); R2%(t) from Stockdon (dissipative branch in storms, or least-squares foreshore slope as in `*_slopefix`); TWL = η + R2%; z_toe = dune-toe elevation of the pre-storm survey (fallback: HAT = 2.14 m); Δt = 1 h; sums over the storm window or over the whole survey interval.

1. **Tide-weighted (water-level-gated) energy** — E_η = Σ Hs² Δt · w(η), with w(η) = clip((η − z_lo)/(z_hi − z_lo), 0, 1), e.g. z_lo = MSL, z_hi = MHWS. Continuous replacement for the binary HAT gate; captures storm–tide phasing (mechanism 2). Refs: Coco et al. 2014; Masselink, Kroon & Davidson-Arnott 2006; Short 2020. *Computable now.*
2. **Larson wave-impact integral** — I_L = Σ_{TWL > z_toe} (TWL − z_toe)² Δt / Tp; model ΔV_dune = 4 C_s I_L (one fitted C_s). Thresholded, quadratic in exceedance, period-weighted. Refs: Larson et al. 2004; Overton et al. 1988; Erikson et al. 2007; Splinter & Palmsten 2012; Mull & Ruggiero 2014. *Computable now with HAT; better with z_toe extraction.*
3. **Collision-regime duration** — T_coll = Σ Δt · 1[TWL > z_toe] (and T_ow with dune crest). Ties the EVI to the CRI of Nicolae Lerma et al. (2018) and to the Sallenger/Stockdon regimes. Refs: Stockdon et al. 2007; D: Stockdon 2023, Leaman 2021. *Computable now.*
4. **Ω disequilibrium** — Ω = H_b/(w_s Tp) with w_s for D50 ≈ 0.35 mm [verify]; Ω_eq(φ) = weighted antecedent mean with memory φ (days); feature ΔΩ_storm = max or mean of (Ω − Ω_eq) during the storm; model term c·P^{1/2}·ΔΩ (ShoreFor-type, but on volume). Refs: Wright & Short 1984; Wright, Short & Green 1985; D: Davidson 2013, Splinter 2014. *Computable now.*
5. **Saturating (Kriebel–Dean) response** — ΔV = V_∞ (1 − exp(−t_exc/T_s)), V_∞ ∝ max(TWL − z_ref) or ∝ E_η; or simply a concave transform ΔV = a·E/(1 + E/E_sat). Encodes response lag and saturation at high energy. Refs: Kriebel & Dean 1993; Palmsten & Holman 2012; van Rijn 2009; Coco et al. 2014. *Computable now (2 parameters).*
6. **Sequence depletion** — E_eff,k = E_k · exp(−E_prev/E_mem), E_prev = energy of earlier storms within the same erosion phase not followed by recovery (reset by a recovery-energy threshold). Refs: Coco et al. 2014; Eichentopf et al. 2020; Vousdoukas et al. 2012; D: Splinter 2014a, Karunarathna 2014. *Computable now.*
7. **Berm/buffer gate** — V_berm = pre-storm volume above z_toe − 1 m (or above HAT) seaward of the toe; ΔV = a·E·[1 + b·1(V_berm < V_crit)] or a piecewise model where dune erosion starts only after V_berm is exhausted. Refs: Phillips et al. 2019; Splinter, Kearney & Turner 2018; Cohn et al. 2019; D: Beuzen 2019a. *Needs profile extraction (have profiles).*
8. **Post-storm recovery correction** — R = R_max (1 − exp(−Δt_post/τ)) or R = k·Σ_{Hs∈[1, 2.5] m} Hs²Δt between storm end and the second survey (moderate, skewed swell drives onshore bar migration and berm building); include spring–neap phase. Fit ΔV_obs = ΔV_storm − R. Refs: Phillips et al. 2017, 2019; Hoefel & Elgar 2003; Dubarbier et al. 2017; Scott et al. 2016. *Computable now; addresses the binding survey-spacing limit.*
9. **IG / runup proxy** — Σ √(H₀L₀) Δt or Σ Hs·Tp Δt (above a threshold), optionally × spectral narrowness from RESOURCECODE. Refs: Ruessink et al. 1998; Guza & Feddersen 2012; Fiedler et al. 2015; Bertin et al. 2018, 2020; Inch et al. 2017. *Computable now (spectral term needs spectra).*
10. **Latent bar proxy** — equilibrium bar position from wave history, dx_b/dt = α (x_eq(Hs) − x_b) (fit α, x_eq from satellite bar positions where available), used as a dissipation covariate. Refs: Masselink et al. 2014; Price & Ruessink 2011; Lafon et al. 2004. *Needs a few bar observations to calibrate (Sentinel-2 / Lubac 2022 in D).*

Suggested next-model structure (for C): ΔV_obs = f_storm(E_η, I_L or T_coll, ΔΩ | V_berm, z_toe) − f_recovery(E_moderate, Δt_post) with saturation (form 5) — i.e. a two-term physics model with 4–6 parameters, fitted on LOWO exactly like the EVI, before any ML on its residual.

---

## C. Does anyone already do this?

Question: does any paper predict **event-scale erosion volume** with **physics-informed features** on **meso-macrotidal** beaches?

| Paper | What it does | Verdict |
|---|---|---|
| Coco et al. 2014 (Truc Vert, ECORS'08) | Regresses daily upper-beachface volume change on offshore waves, **tidal range** and **IG energy** over one month | **Closest match at our site** — physics-informed volume regression, but one storm cluster, in-sample, IG measured in situ (not available operationally). Our feature set B1/B9 is its operational generalisation over 16 years. |
| Nicolae Lerma et al. 2018 (in D) | EVI (energy) + CRI (collision regime) for the Aquitaine EWS | Has the collision regime, but only as an alert class; does not use the collision *integral* to predict volume. Gap = B2/B3. |
| Larson et al. 2004; Splinter & Palmsten 2012; Mull & Ruggiero 2014; Splinter, Kearney & Turner 2018 | Wave-impact models predicting dune-erosion volume per storm | Physics-informed event volume, but micro/meso-tidal dune-only cases; not tested on a macrotidal beach with ~fortnightly surveys. |
| Plant & Stockdon 2012 | Bayesian network on TWL + morphology for dune change | Physics-informed and probabilistic; R² ≈ 0.2–0.3 — same ceiling as our EVI. Microtidal Gulf coast. |
| Mendoza & Jiménez 2006 | Storm erosion-potential index calibrated on SBEACH | Physics-calibrated volume index, but trained on model output and microtidal (NW Mediterranean). |
| den Heijer et al. 2012 | DUROS+ parametric dune erosion in a probabilistic framework | Operational physics-based volume (Dutch meso-tidal coast [verify range]); a design tool, not validated event by event against surveys. |
| Callaghan et al. 2013; Pender & Karunarathna 2013 | Analytical/semi-empirical/process models (+ empirical recovery) for storm erosion | Hybrid physics framing; microtidal Narrabeen; not event-volume skill on held-out storms. |
| Vousdoukas et al. 2012; Sénéchal et al. 2015 | Descriptive analyses of consecutive storms (meso-tidal Faro; macrotidal Biscarrosse) | Identify the same mechanisms (antecedent state, tide), no predictive volume model. |
| D entries: Beuzen 2019, Simmons & Splinter 2022, Harley 2023, Calcraft 2025 | ML/GP/ensembles with physical features for storm erosion | Event-scale volume, physics-informed inputs, held-out testing — but microtidal Narrabeen. |

**Bottom line.** We found no paper that predicts event-scale storm-erosion *volume* on a meso-macrotidal barred beach with physics-informed features (tide-phase weighting, impact integral, Ω disequilibrium, recovery correction) under held-out evaluation. The ingredients exist separately (Coco 2014 at Truc Vert; Larson-type models elsewhere; equilibrium models for shorelines at Truc Vert in D). Searches were Crossref keyword queries and targeted web searches only; this is not a systematic review **[verify with a Scopus/WoS query before submission]**.

---

## Summary counts

- Annotated entries: **72** — 71 verified (Crossref metadata generated + doi.org 302), 1 unverified (Masselink & Short 1993, JSTOR, no DOI).
- By theme: T1 swash/IG 12 · T2 berm/tide 6 (1 unverified) · T3 bars/rips 12 · T4 dune erosion 13 · T5 recovery/aeolian/equilibrium 12 · T6 sediment/budget 4 · T7 forcing 6 · T8 process models 7.
- No-DOI items mentioned inline only: Sallenger (2000), Dolan & Davis (1992) (both already "verified: no" in D).
- Main open **[verify]** items: Truc Vert D50 (≈0.35 mm) and tidal-range values from Castelle et al. (2007) full text; Larson C_s range; Kriebel–Dean T_s; Blenkinsopp et al. (2011) site; Almar et al. (2008) site; specific numbers in Castelle et al. (2017) and Abadie et al. (2006).

## Reproduce

Crossref record: `curl -s https://api.crossref.org/works/<doi>`; DOI check: `curl -s -o /dev/null -w '%{http_code}' -I https://doi.org/<doi>` (expect 302); OA: `https://api.openalex.org/works/doi:<doi>` (`best_oa_location`); abstracts: OpenAlex `abstract_inverted_index` and Semantic Scholar `/graph/v1/paper/batch`; BibTeX: `https://api.crossref.org/works/<doi>/transform/application/x-bibtex`. Candidate searches: `api.crossref.org/works?query.bibliographic=...&rows=4`.
- BibTeX: 71 entries appended to `reports/D_references.bib` under a `% ---- Appended by Agent S` comment. Five Crossref default keys collided with existing ones and got an `S` suffix: `Senechal_2011S` (ECORS'08), `Eichentopf_2020S` (flume experiments), `Castelle_2018S` (ECSS shoreline change), `Castelle_2017S` (Mar. Geol. foredune), `Masselink_2006S` (intertidal bars; `Masselink_2006` is Masselink & Puleo).
