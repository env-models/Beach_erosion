# Key thesis passages in English (Gillet 2017, M2 DYNARISK) — working translation

Agent A, 2026-10-13. Translated by the agent from `docs/thesis/thesis_text_extracted.txt`, not checked by the
author [verify]. Page numbers are the thesis's printed page numbers. Translator's notes are in [square brackets].
Glossary: PHMA = HAT (Highest Astronomical Tide); haut / bas de plage = upper / lower beach; pied de dune = dune
toe; engraissée = accreted ("fat"); surcote = surge; jet de rive = swash; levé = survey.

## Method (Part II)

**Thresholds (p. 20).** "[…] the choice was made to use a tidal datum, an unchanging altimetric reference
available at every point of the coast. The Highest Astronomical Tide (PHMA) was used as the threshold. Sometimes
used as a shoreline indicator, it is the elevation reached by the water level only during the highest tidal
coefficients. This selects a limit that waves rarely exceed and restricts the analysis to the potentially most
erosive conditions (water level + waves). We can now set the two thresholds that bound the observation window:
a **topographic threshold** — we look at beach volumes eroded *above the PHMA*; a **hydrodynamic threshold** — we
look at the energy of waves whose runup reaches at least the PHMA."

**Model variants (pp. 21–22).** "[…] a marked erosion of the dune front that redistributes sand and feeds the
lower beach will not be correctly captured by our indicator, which only looks at upper-beach erosion. To address
this we will assess how considering erosion on both the upper and the lower beach improves the model. […] The
equilibrium profile […] will be approximated by the **mean profile**, the time average of all beach profiles used
to calibrate the model. When a storm approaches, one can then determine whether the (pre-storm) profile is more or
less eroded than this mean profile, hence more or less resilient. […] Some storms recharge the beach with sand.
Including these events (associated by the model with negative eroded volumes) inevitably increases the scatter.
To reduce it, and since we specifically aim at erosion risk, we will restrict ourselves, in an annex part, to
purely erosive storms." [This is the selection on the target audited in `reports/A_audit.md`, item 7.]

**Storm definition (p. 23).** "Storm-definition threshold: a storm occurs when Hs exceeds a value exceeded by only
5% of waves over the year; at the study site Hs95% = 4.3 m. Storm-delimitation threshold: the value exceeded by
only 25% of waves, Hs75% = 2.3 m, which sets the start and end of each storm."

**Runup (p. 24).** "To select the energy of waves that reached the PHMA, we need the level reached by waves on the
beach, i.e. the runup exceeded by only 2% of waves (R2%), from the empirical equations of Stockdon et al. (2006),
which depend on the Iribarren number ε = β/√(Hs/L0), β being the intertidal beach slope. If ε < 0.3 the beach is
dissipative: Runup = 0.016√(Hs L0); if ε > 0.3: Runup = 1.1(0.35β√(Hs L0) + ½[√(Hs L0(0.563β² + 0.004))])."
[0.016 is Stockdon's dissipative *setup*; R2% is 0.043√(H0L0). The code uses 0.043 and deep-water H0 — audit item 10.]

**Variables (pp. 10, 19).** ΔV, in m³ per metre of shoreline, "can be positive (eroded volumes) or negative
(deposited volumes)". E, "the energy released by the storm, proportional to storm duration and to the square of
wave height, […] the time integral over the storm of the energy density, expressed in J/m²". The flux equation
(p. 10) is P = ∫ ρg²Hs²Tp/(64π) Δt with ρ = 1030 kg/m³, g = 9.81 m/s², "Δt the time step, in hours".
[Units audited in item 1.]

**Data (p. 26).** Profiles averaged longshore over 750 m (2008–2011) then 1500 m (from 2012), one point every
10 cm, about one profile every 2 weeks, "102 profiles over 2009–2012" [p. 28 says 9 Feb 2009 – 2 Jan 2014],
referenced to mean sea level; "the profile zero is +0.39 m IGN69".

## Results (Part III)

**General model, calibration 2009–2013 (pp. 28–35).** "We used 102 beach profiles […] surveyed from 9 February
2009 to 2 January 2014. Over this period 51 storm episodes were identified […]; the shortest lasted 22 hours, the
longest is a storm series during which Hs did not drop below 2.4 m for more than 12 days (28 Oct – 9 Nov 2009).
[…] Several distinct storms sometimes occur between two surveys; their individual impacts cannot be separated and
the model treats them as a single event. Of the 51 storms, the profiles limit us to 37 events. […] Of the 37 events,
22 eroded the upper beach (ΔV > 0) and 15 recharged it (ΔV < 0). Upper-beach (above PHMA) eroded volumes reach
30 m³/m and recharge 27 m³/m." Conclusions: "All storms can be erosive — there is no energy threshold below which
there is no erosion. All storms are erosive beyond 1.6 MJ/m². The recharge rate in calm conditions is about
6 m³/m/month (the regression intercept multiplied by 2, since there are on average two profiles per month)."
"For the general model: Eroded volume = 10.2 × Energy − 3.2 […] a very weak correlation coefficient (R² = 0.26)
and a large error (RMSE = 22.4 m³/m)."

**Case studies.** Xynthia (24–28 Feb 2010, cluster of 3 storms, Hs ≈ 7 m): upper-beach erosion and dune-toe
retreat > 5 m, part of the sand fed the lower beach — a "two-storey" dynamic the above-PHMA model misses. Joachim
(11–18 Dec 2011): highest energy, erased a well-developed summer berm, no dune-toe retreat; "the 3.5 MJ/m² retained
by the model also includes a second storm a few weeks later in the same survey interval"; "illustrates the crucial
role of the berm in protecting the dune front". "Post-Klaus" storm (early March 2009, Hs 8 m, 1.58 MJ/m²): the
largest recharge (+27 m³/m), but the surveys are more than 2 months apart with calm seas in between, so the recharge
may have happened after the storm.

**Modified models (pp. 35–38).** TPTE (*Tout le Profil – Tempêtes Erosives*): erosive storms only, volumes on the
whole profile: ΔV = 18.7E + 2.1. PPT (*Profil Pré-Tempête*): TPTE plus the pre-storm state relative to the mean
2009–2013 profile: accreted beach ΔV = 20.9E + 2.6; eroded beach ΔV = 14.9E + 2.7.

**Validation 2014–2015 (pp. 38–40).** "To include the first storm of the winter (Dirk), validation starts on
1 December 2013." Christina+Hercules and Petra+Ruth are not separable and are summed. "These 8 storms caused a
cumulative erosion of 185 m³/m". "The TPTE and PPT models capture the erosive dynamics much better, with a
**correlation coefficient** of 0.61 and 0.85 respectively (RMSE 11.9 and 7.5 m³/m)." [The abstract reports the
same 0.85 as "R²" — audit item 9.] "PPT has a relative error of about 25% for the largest storms; Andrea is
reproduced with < 2% error; […] for Nadja the model overestimates eroded volume by nearly 100%."

**Author's limitations (pp. 50–52).** The Hs75% = 2.3 m delimitation threshold is too low (e.g. Klaus) and
overestimates storm energy, and leads to windows too long for weather forecasts; the pre-storm state requirement
restricts the EVI to monitored beaches; transfer to Biscarrosse failed; model forcing (ATNE hindcast) should be
regressed against CANDHIS buoy data.
