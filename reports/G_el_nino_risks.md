# G — El Niño 2026–27: risks and hazards for storm-driven erosion at Truc Vert / Aquitaine, with the global picture

Agent G, branch `revisit-2026`, written 2026-10-13. Every source was checked on 2026-10-13 (see §6).
`[verify]` marks a claim I could not confirm against a primary source in this session. Numbers I computed
myself from public data are labelled **(computed here)** and the method is given.

**Bottom line.** A strong, possibly record El Niño is under way. Its link to winter storminess and wave energy in the
Bay of Biscay is **weak and its sign is uncertain** in the literature. The one study that tests ENSO directly against
European Atlantic beach data, which is co-authored by Castelle, finds winter waves and shoreline change "unrelated
to ENSO". The NAO, and above all WEPA, are the climate modes that matter locally. For winter 2026–27 at Truc Vert the
main risks are the usual ones, an energetic WEPA+/NAO+ winter or a cluster of storms on spring tides, landing on a
beach whose state since 2019 we cannot document from our data. El Niño changes the odds of these only a little, and we
don't know in which direction.

---

## 1. Current ENSO state and outlook (as of 13 October 2026)

**El Niño is present, strong, and still strengthening.** This is not a hypothetical question this year.

| Item | Value | Source (issued; checked 2026-10-13) |
|---|---|---|
| Official US status | **El Niño Advisory**. "El Niño continues to strengthen, with a strong-to-very strong El Niño likely through January-March 2027 (remaining greater than an 83% chance)." | NOAA CPC ENSO Diagnostic Discussion, 8 Oct 2026 |
| Monthly Niño indices (CPC discussion, September) | Niño-3.4 **+2.1 °C**, Niño-3 +3.0 °C, Niño-1+2 +3.9 °C. Eastern equatorial SST anomalies exceed +4 °C in places. Subsurface anomalies exceed +10 °C at depth. SOI "significantly negative". | same |
| Monthly OISST Niño-3.4, Sept 2026 (traditional, non-relative anomaly) | **+2.84 °C** (Niño-1+2 +4.69, Niño-3 +3.64, Niño-4 +0.95) | CPC `sstoi.indices` data file |
| Latest weekly OISST Niño-3.4 (week of 7 Oct 2026) | **+3.3 °C** (Niño-1+2 +5.2, Niño-3 +4.1, Niño-4 +1.3) | CPC `wksst9120.for` data file |
| RONI (relative ONI, CPC's official strength index) | JAS 2026 = **+1.69** | CPC `RONI.ascii.txt` |
| Traditional ONI | JAS 2026 = +2.16 | CPC `oni.ascii.txt` |
| Chance of a "historic" event (3-month RONI ≥ +2.5 °C) | SON 54 %, **OND 83 %**, NDJ 70 % | CPC discussion, 8 Oct 2026 |
| CPC strength probabilities (RONI) | NDJ: El Niño 100 % (very strong ≥2.0 °C 96 %). **DJF: 100 % (very strong 81 %, strong 16 %, moderate 3 %)**. **JFM: 100 % (very strong 46 %, strong 37 %, moderate 15 %, weak 2 %)**. FMA: 98 %. Neutral favoured from AMJ 2027 (54 %). | CPC ENSO Strength Probabilities, issued Oct 2026 |
| IRI plume | "El Niño probabilities remain at 100% from SON 2026 through FMA 2027". "nearly all dynamical and several statistical models forecasting the Niño3.4 index above +3.0°C from fall into winter." MAM 99 %, AMJ 90 %, MJJ 61 %. | IRI ENSO Forecast, **September 2026 issue** (21 Sep). The October issue was not yet online. |
| BoM (Australia) | "El Niño near record levels". Weekly relative Niño-3.4 **+2.81 °C** (week ending 11 Oct 2026), "the highest value on record" in BoM's GAMSSA weekly series (since 2008). All models forecast a peak around Nov–Dec and persistence into austral autumn 2027, "with most models indicating a peak monthly value above +3.0 °C" (relative). | BoM Climate Driver / ENSO page, issued 13 Oct 2026 |
| WMO | El Niño/La Niña Update, 3 Sep 2026: "exceptionally high likelihood of nearly 100%" that El Niño persists through Feb 2027, strengthening to "very strong intensity before peaking towards the end of this year". Global Seasonal Climate Update for OND 2026 (8 Oct 2026): the seasonal-mean Niño-3.4 anomaly is forecast to reach about **+3.7 °C** in OND, peaking around December. | WMO press release, 3 Sep 2026; WMO GSCU-OND2026 |
| C3S (Copernicus) | Oct 2026 issue (10 Oct): late autumn/early winter "near- or lower-than-average sea-level pressure across most of the continent". Higher-than-average pressure is likely to build "in polar regions and the far north of the continent as winter progresses". Above-average temperature and precipitation are favoured across most of Europe, with the weakest signals over Scandinavia and, for precipitation, the south. | C3S seasonal forecasts page |
| Météo-France | 2 Oct 2026: the peak is expected "en novembre ou décembre 2026, qui pourrait être inédit depuis 1950". Mean signal for Europe: early winter "un peu plus de pluie et des températures plus tempérées sur l'Europe de l'ouest", and lower North Atlantic surface pressure. Late winter: "un peu plus de pluie sur le Sud-Ouest de l'Europe". "Ces effets ne sont pas systématiques et ne sont pas directement associés à l'intensité des épisodes." "Les effets d'El Niño concernent donc surtout les territoires ultramarins." | Météo-France actualité, 2 Oct 2026 |

**Reading the numbers (why there are several "Niño-3.4" values).** CPC (RONI) and BoM now classify ENSO with
*relative* indices: the Niño-3.4 anomaly minus the tropical-mean SST anomaly, which removes the background warming
trend (exact switch dates `[verify]`). Relative values (+2.1 monthly at CPC, +2.81 weekly at BoM, RONI +1.69 for JAS) are lower than the traditional
OISST anomalies (+2.84 monthly, +3.3 weekly). The two kinds of index must not be mixed when comparing with 1982–83,
1997–98 or 2015–16. The CPC discussion's own Fig. 2 defines its monthly values, and I did not open the figure, so
the reading of +2.1 °C as a relative value is an inference `[verify]`. It fits the ≈0.7 °C gap between the two
families.

**Expected strength.** Every centre expects a **strong to very strong** event peaking in Nov–Dec 2026. CPC gives
**83 %** that OND 2026 will be the strongest since 1950 (RONI ≥ 2.5). The event is expected to decay through
spring 2027. For the Aquitaine winter (DJF/JFM), El Niño will almost certainly still be strong while the storm season
is under way.

**Note on centre statements and Europe.** None of the official ENSO bulletins (CPC, IRI, BoM, WMO) makes a statement
about NE Atlantic storminess or wave climate. Météo-France explicitly calls the effect on metropolitan France weak and
non-systematic. Secondary outlets and private forecasters ("super El Niño", "hiver très perturbé") go well beyond
what the centres say and are not used here.

---

## 2. Teleconnection to the NE Atlantic / Bay of Biscay winter wave climate

### 2.1 Atmospheric pathway: ENSO → jet / NAO / EA (climate-dynamics literature)

| Paper | What it shows | Sign for El Niño | Confidence / caveats |
|---|---|---|---|
| **Brönnimann (2007)**, *Rev. Geophys.*, doi:10.1029/2006RG000199 | Review. ENSO does affect European climate, but effects are seasonally modulated, nonlinear, possibly non-stationary over decades, with "large interevent variability". | Canonical late-winter pattern: negative NAO-like | Explicitly "discussed more controversially" than in the Pacific/N. America |
| **Toniazzo & Scaife (2006)**, *GRL*, doi:10.1029/2006GL027881 | Stratified by amplitude: "a highly non-linear yet robust response to ENSO that **changes sign** over the eastern North Atlantic as the amplitude of the El Niño anomaly increases." | **Moderate** El Niño → NAO−-like. **Strong** El Niño → different, opposite-signed response over the eastern N. Atlantic | Directly relevant this year: a very strong event is **not** expected to give the textbook NAO− |
| **Ineson & Scaife (2009)**, *Nat. Geosci.*, doi:10.1038/ngeo381 (Crossref issue year 2008/2009) | Stratospheric pathway: El Niño weakens the polar vortex, and the late-winter (Jan–Mar) European response (NAO−-like, cold N. Europe, wetter S. Europe) appears mainly in winters with a sudden stratospheric warming. | Late winter NAO− *conditional on* stratospheric events | Abstract not retrievable here (paywall). Summary from the paper's widely cited conclusion `[verify wording]` |
| **Jiménez-Esteve & Domeisen (2018)**, *J. Climate*, doi:10.1175/JCLI-D-17-0716.1 | Tropospheric pathway: more wave-activity flux from the Pacific to the Atlantic during El Niño → NAO−, Jan–Mar. "the stratosphere strongly modulates this response". | NAO− (Jan–Mar) | Reanalysis composites. Nonlinear and non-stationary |
| **Ayarzagüena et al. (2018)**, *J. Climate*, doi:10.1175/JCLI-D-18-0097.1 | An **intraseasonal shift**: the early-winter (Nov–Dec) ENSO signal over the N. Atlantic–Europe differs from the late-winter one. It is set up through the troposphere via Gulf of Mexico/Caribbean rainfall. Significant in observations and initialized forecasts, missing in free-running CMIP5. | Early winter differs from late winter (early winter tends to be the *opposite*, NAO+-like) `[verify sign in full text]` | Important for Biscay because Nov–Dec storms count |
| **Hardiman et al. (2019)**, *GRL*, doi:10.1029/2018GL081776 | Large-ensemble Met Office simulations: strong El Niño gives a "**wavelike response**" in Jan–Feb N. Atlantic MSLP, "very different" from the positive-NAO response to strong La Niña. The tropospheric pathway dominates for strong El Niño. | Not a clean NAO−. Wave-train pattern | Model-based, physically argued |
| **Domeisen, Garfinkel & Butler (2019)**, *Rev. Geophys.*, doi:10.1029/2018RG000596 | Review of the stratospheric pathway: El Niño warms and weakens the polar vortex. Open questions on nonlinearity and ENSO diversity. | Weaker vortex → NAO− tendency | Review |
| **Mezzina et al. (2020)**, *J. Climate*, doi:10.1175/JCLI-D-19-0192.1 | The late-winter ENSO SLP dipole *resembles* the NAO, but "there is no dynamical link between the phenomena". ENSO gives "modest but significant SLP skill" in the NAE midlatitudes. "caution is advised when interpreting the former in terms of the latter." | NAO-like dipole, but not the NAO | Warns against using ENSO as a NAO proxy |
| **Scaife et al. (2014)**, *GRL*, doi:10.1002/2014GL059637, and **Scaife et al. (2016)**, *QJRMS*, doi:10.1002/qj.2910 | Seasonal NAO forecasts have real skill. Tropical rainfall/Rossby waves (including ENSO) are among the sources. | — | The source of whatever seasonal NAO skill exists |

**What this means for the Bay of Biscay.** The established result is a **modest late-winter NAO−-like tendency for
moderate El Niño**. That result is nonlinear (Toniazzo & Scaife 2006: possible sign reversal for strong events), depends
on the stratosphere (Ineson & Scaife 2009), differs between early and late winter (Ayarzagüena et al. 2018), and may
not even be the NAO (Mezzina et al. 2020). For a very strong event such as 2026–27, the literature does **not** support
a confident sign over the eastern North Atlantic.

A second subtlety matters at 44.6 °N. A negative NAO weakens the main westerly storm track but shifts it **southward**,
which can bring individual storms to Biscay and Iberia. Winter 2009–10 is the textbook case: a moderate-to-strong El
Niño (DJF ONI +1.47) with a record-negative NAO (DJF mean −1.67, **computed here**), and storm Xynthia hit the French
Atlantic coast in Feb 2010. The thesis (HANDOFF §1) records that Xynthia eroded the Truc Vert upper beach. So even the
textbook "El Niño → NAO−" chain does not translate into "fewer storms in SW France".

### 2.2 Empirical check on the public record (computed here)

From CPC monthly NAO (`norm.nao.monthly.b5001.current.ascii`) and CPC ONI (`oni.ascii.txt`), 1951–2026 (n = 76 winters):

- Correlation of DJF ONI with DJF NAO: **r = −0.04** (r² ≈ 0.002). With JFM NAO: r = −0.12. Neither is
  distinguishable from zero.
- Mean DJF NAO in winters with ONI ≥ +1.0: +0.09 (n = 10). ONI ≤ −1.0: +0.21 (n = 10). Neutral: +0.12 (n = 25).
  Standard deviation of DJF NAO across all winters: 0.76.
- Strong El Niño winters (DJF ONI ≥ 1.5) and their DJF NAO: 1957–58 −0.49, 1972–73 +0.36, **1982–83 +0.95**,
  1991–92 +0.47, **1997–98 −0.23**, **2015–16 +1.31**, **2023–24 +1.08**. 5 of 7 are positive. That fits Toniazzo &
  Scaife's "sign change for strong events", but n = 7 cannot support inference.
- For reference: **2013–14 had DJF ONI −0.24 (ENSO-neutral)** and DJF NAO +0.86. 2025–26 had DJF ONI −0.39.

Caveat: these are linear seasonal-mean statistics. They ignore the early/late-winter split and the stratospheric
conditioning described above, and they say nothing about WEPA. They show that ENSO explains essentially none of the
interannual NAO variance in this record. They do **not** prove the absence of a conditional signal.

### 2.3 Wave climate and beach response on the European Atlantic coast

| Paper | Finding relevant to ENSO / climate modes | Sign / magnitude for ENSO | Confidence |
|---|---|---|---|
| **Masselink, Castelle, Scott & Konstantinou (2023)**, *GRL*, doi:10.1029/2023GL106019 | Three high-quality European Atlantic profile datasets. "WEPA explaining 50%–80% of the winter wave power variability" and "25% of the winter shoreline variability". "**Winter wave conditions and associated shoreline variability are both unrelated to El Nino Southern Oscillation.**" Antecedent shoreline position also matters strongly. | **No relationship** | The most direct test. Truc Vert is very likely one of the three sites (Castelle co-author), but I could not open the full text to confirm the site list or the ENSO index used `[verify]` |
| **Castelle et al. (2017)**, *GRL*, doi:10.1002/2016GL072379 (WEPA) | WEPA (Valentia − Santa Cruz de Tenerife SLP gradient) "outscores by 25–150% the other leading atmospheric modes in explaining winter-averaged significant wave height" from Portugal to the UK (36–52 °N). It is "the only index capturing the 2013/2014 extreme winter". | ENSO is not among the leading predictors `[verify whether ENSO was tested]` | High for WEPA |
| **Castelle et al. (2018)**, *GRL*, doi:10.1002/2017GL076884 | 1948–2017 hindcast: winter-mean Hs, its variability and its periodicity have all increased significantly in the NE Atlantic. The trend in the mean is explained mainly by NAO, periodicity by WEPA, and variability by both. "more frequent high-energy winters with high NAO and/or WEPA". | ENSO not invoked | High |
| **Castelle et al. (2019)**, *Coastal Sediments 2019*, doi:10.1142/9789811204487_0041 | Climate control on NE Atlantic winter waves and on beach erosion/recovery along W. Europe (WEPA/NAO). | — | Abstract not available `[verify content]` |
| **Dodet, Bertin & Taborda (2010)**, *Ocean Modelling*, doi:10.1016/j.ocemod.2009.10.010 | 1953–2009 NE Atlantic hindcast. Winter Hs variability and trends are tied mainly to the NAO, with stronger NAO control north of ~45 °N `[verify exact latitude and correlation values]`. | ENSO not a primary driver | Medium-high |
| **Dodet et al. (2019)**, *ESPL*, doi:10.1002/esp.4500 | Recovery after 2013–14 is site-specific and multi-annual: one beach recovered in 2 years, the others only partly after 4. "energetic winter conditions stall the recovery process". Interannual variability "well correlated with climate indices" (NAO/WEPA). | — | High |
| **Masselink et al. (2016)**, *GRL*, doi:10.1002/2015GL067492 | 2013–14 was "the most energetic along most of the Atlantic coast of Europe since at least 1948". | That winter was ENSO-neutral (DJF ONI −0.24) | High |
| **Malagon Santos, Haigh & Wahl (2017)**, *JMSE*, doi:10.3390/jmse5030028 | UK extreme wave events 2002–2016: "large inter-annual differences in the number of events per season associated with" WEPA. 2013–14 was an outlier. | ENSO not invoked | Medium (UK, not Biscay) |
| **Bromirski & Cayan (2015)**, *JGR Oceans*, doi:10.1002/2014JC010440 | Eastern North Atlantic wave power is "strongly influenced by" the NAO. ENSO/PNA influence is on the **western** Atlantic (US East Coast). | ENSO influence on the eastern Atlantic: not supported | High |
| **Odériz et al. (2020)**, *JGR Oceans*, doi:10.1029/2020JC016464 | Global classification of ENSO wave impacts (MEI correlation with wave power and direction). The strongest El Niño effects are on extra-tropical swells reaching the tropics, "particularly notable in the Pacific Basin". | Implies weak or no NE Atlantic signal `[verify their class for the Bay of Biscay]` | Medium |
| **Reguero, Losada & Méndez (2019)**, *Nat. Commun.*, doi:10.1038/s41467-018-08066-0 | Global wave power +0.4 %/yr since 1948, linked to SST warming (strongest link: tropical Atlantic SST ↔ Southern Ocean wave power). | Background trend, not ENSO | Medium-high |
| **Morim et al. (2019)**, *Nat. Clim. Change*, doi:10.1038/s41558-019-0542-5. **Lobeto et al. (2021)**, *Sci. Rep.*, doi:10.1038/s41598-021-86524-4. **Charles et al. (2012)**, *Ocean Dyn.*, doi:10.1007/s10236-012-0534-8 | Projections. Bay of Biscay mean Hs decreases and winter swell rotates clockwise under higher emissions (Charles). Global ensemble robustness (Morim). Extremes and means diverge (Lobeto). | Not about ENSO. Relevant to the long-term context only | Medium |
| **Mentaschi et al. (2017)**, *GRL*, doi:10.1002/2016GL072488 | Projected extreme wave energy flux trends are explained by intensified teleconnection patterns (AAO, ENSO, NAO). Large Northern Hemisphere coastal areas show *negative* trends. | Climate-change projection, not interannual | Medium |

**Answer to "does El Niño increase or decrease winter storminess / wave energy in SW France?"** There is **no
established sign**. Mechanistic studies give a modest late-winter NAO−-like tendency for *moderate* events, with a
possible reversal or a non-NAO pattern for *strong* events. The only direct beach-data test on this coast (Masselink et
al. 2023) finds winter waves and shoreline change **unrelated to ENSO**. Eastern-Atlantic wave power is NAO/WEPA-
controlled (Bromirski & Cayan 2015; Castelle et al. 2017, 2018). **Confidence that ENSO materially changes Truc Vert
winter erosion: low.** The extreme 2013–14 winter was ENSO-neutral. Locally, WEPA (50–80 % of winter wave-power
variance) and NAO explain far more than ENSO (≈0 % of NAO variance in §2.2).

### 2.4 What the seasonal forecasts say for DJF 2026–27

- **C3S (Oct 2026)**: lower-than-average SLP over most of Europe in late autumn/early winter. Higher pressure builds
  over polar regions and the far north as winter goes on. Wetter and milder than average across most of Europe.
- **Météo-France (2 Oct 2026)**: early-winter mean El Niño signal of slightly more rain and lower pressure over the
  North Atlantic, and late-winter slightly more rain in SW Europe. These are composites, "pas systématiques".
- **My reading `[speculation, not a forecast]`.** Low SLP over Europe early in the winter, with high-latitude blocking
  developing later, looks like an active, possibly southward-displaced storm track. That pattern is compatible with
  NAO− later in the winter and with WEPA+ (low over Ireland relative to the Canaries), the configuration that sends
  energetic waves into Biscay. **No centre publishes a WEPA forecast, and I found no official numerical NAO forecast
  for DJF 2026–27.** Seasonal NAO forecasts typically have correlation skill of about 0.5–0.6 with small signal-to-noise
  (Scaife et al. 2014) `[verify skill figure]`. Treat any seasonal storminess statement for Truc Vert as a slight
  tilt of the odds at most.
- **Next updates to watch:** CPC discussion 12 Nov 2026; C3S and Météo-France monthly seasonal updates (early Nov,
  early Dec); IRI October issue.

---

## 3. Global hazards where ENSO dominates coastal erosion (context for the introduction)

ENSO is the **dominant** interannual control on coastal erosion around the **Pacific** rim, not in the NE Atlantic.

- **Pan-Pacific.** *Barnard et al. (2015, Nat. Geosci., doi:10.1038/ngeo2539)*: multi-decadal beach records from sites
  around the Pacific basin show coastal vulnerability "dominated by ENSO". In the eastern Pacific (US West Coast) El
  Niño brings more winter wave energy and higher water levels, which raises erosion. In the western Pacific (e.g. SE
  Australia, NZ) La Niña tends to be erosive, with changes in wave direction and beach rotation. The site count and
  period (often quoted as 48 beaches, 1979–2012) are `[verify]`; the abstract was not retrievable (publisher-elided).
  *Vos et al. (2023, Nat. Geosci., doi:10.1038/s41561-022-01117-8)*: 35 years of Landsat, 72,000 Pacific Rim
  transects. "approximately one third of all beaches experience significant erosion during El Niño phases", the
  Eastern Pacific is "particularly vulnerable", "most notably during the large 1997/1998 event". La Niña coincides
  with accretion on about a quarter of beaches but "drives substantial erosion in south-east Australia".
- **US West Coast, 2015–16.** *Barnard et al. (2017, Nat. Commun., doi:10.1038/ncomms14365)*: winter wave energy flux
  "∼50% above normal averaged across all regions" and water levels +11 cm, giving winter shoreline retreat **"76% above
  normal"**, "27% higher than any other winter", eclipsing 2009–10 (+12 %) and 1997–98 (−9 %). Many California beaches
  reached their most landward position on record. Mean wave energy flux in 1997–98 was even higher (61 % above
  normal) over the 19-year record.
  *Young et al. (2018, JGR Earth Surface, doi:10.1029/2018JF004771)*: in **Southern California** the 2015–16 response
  was more muted. The shoreline moved landward 10 m on average (similar to 2009–10), with >80 m at a few spots, 27 % of
  the shoreline accreted, and only 12 % of cliffs eroded. The reasons were northerly swell direction, low rainfall and
  limited total water levels. **Lesson: event strength ≠ local impact; direction, tides and sediment supply matter.**
- **Central California, 1982–83 and 1997–98.** *Storlazzi & Griggs (2000, GSA Bull., doi:10.1130/0016-7606(2000)112<236:IOENOE>2.0.CO;2)*:
  wave height, sea level and precipitation "increase nonlinearly with increasing relative ENSO event intensity".
  "moderate- to high-intensity ENSO events cause the most sea-cliff erosion and shoreline recession over the course of
  a century". *Sallenger et al. (2002, Mar. Geol., doi:10.1016/S0025-3227(02)00316-X)*: 1997–98 sea-cliff erosion
  (Pacifica area) was controlled by beach lowering plus extreme runup `[verify specifics; abstract not retrieved]`.
- **Pacific Northwest (Oregon/Washington).** El Niño raises winter water levels and shifts storm tracks south, causing
  "hotspot" erosion (Komar, Allan, Ruggiero; e.g. Komar 2001, *Coastal Engineering 2000*, doi:10.1061/40549(276)189)
  `[verify magnitudes]`. Barnard et al. (2017): elevated wave energy flux in 2015–16 exceeded 1997–98 by 29 % in
  N. California and the PNW (+44 % off Washington).
- **Peru / Ecuador.** Coastal impacts there are dominated by rainfall, flooding and high sea level rather than wave
  erosion. **2026 so far:** a "Niño Costero" since January 2026 brought heavy rain, floods and landslides. UN OCHA
  counted 92 deaths and >23,000 displaced as of 17 Mar 2026 (ReliefWeb, quoting ECHO 24 Mar 2026), and Peru's national
  commission kept the Niño Costero alert active. Ecuadorian warnings say high sea level combined with swells and spring
  tides may favour flooding and erosion of low coasts. That is a warning, not an observed erosion report `[verify,
  primary source: ERFEN/INOCAR]`. Peruvian outlooks reportedly expect a strong Niño Costero in Dec 2026–Mar 2027
  `[verify, primary source: ENFEN]`.
- **SE Australia.** The sign is opposite. *Ranasinghe et al. (2004, Mar. Geol., doi:10.1016/S0025-3227(04)00002-7)*:
  the SOI controls wave direction and hence **beach rotation** in embayments (Narrabeen). *Mortlock & Goodwin (2016,
  Cont. Shelf Res., doi:10.1016/j.csr.2016.03.007)*: central-Pacific ENSO effects on wave climate and headland-bay
  beaches `[verify findings]`. *Harley et al. (2017, Sci. Rep., doi:10.1038/s41598-017-05792-1)*: the June 2016 East
  Coast Low caused extreme erosion through **anomalous wave direction**. In SE Australia, La Niña is the erosive phase
  (Vos et al. 2023).
- **Pacific islands.** Vos et al. (2023) and Barnard et al. (2015) include island sites. ENSO also modulates sea level
  in the western tropical Pacific (lower during El Niño) `[verify: island-specific erosion magnitudes not retrieved]`.
- **2023–24 El Niño.** I found no peer-reviewed regional synthesis of beach impacts. Press reports describe severe
  storm damage in Santa Cruz (West Cliff Drive, Jan 2024) `[verify; press source only]`. In Europe 2023–24 was a NAO+
  winter (DJF +1.08, computed here) with many named storms (e.g. Ciarán, Nov 2023). The OCNA (Observatoire de la Côte
  de Nouvelle-Aquitaine) published a page "L'hiver 2023-2024 sur le littoral néo-aquitain", which I could not open
  `[verify]`.
- **2026–27 preparations.** US local news reports sand placement ahead of the winter (e.g. Newport Beach, Sept 2026)
  `[verify; press only]`.

---

## 4. Risk register for the Aquitaine coast, winter 2026–27

Likelihood is the chance that the hazard materialises at Truc Vert this winter. ENSO confidence is the confidence that
ENSO shifts that chance.

| Hazard | Mechanism | ENSO-related evidence | Other drivers | Likelihood / confidence | What our model could / could not say | Monitoring sources |
|---|---|---|---|---|---|---|
| **1. Energetic winter (high cumulative wave energy) → large net upper-beach and dune-face loss** | Persistent WEPA+/NAO+ circulation sends long-period swell into Biscay. Cumulative ΣHs²Δt is what the EVI and equilibrium models respond to. | **Weak / unknown sign.** Masselink et al. 2023: unrelated to ENSO. Strong-El-Niño DJF NAO was positive in 5 of 7 winters (n tiny). C3S shows low early-winter SLP over Europe. | WEPA (50–80 % of winter wave-power variance), NAO, the multidecadal increase in winter Hs (Castelle 2018), +0.4 %/yr global wave power (Reguero 2019) | **Medium likelihood** (climatological: high-energy winters have become more frequent). **Low confidence** that El Niño shifts it | Can: once storms happen, convert observed E into ΔV (LOWO skill ≈0.4–0.5 vs climatology). With synthetic winter scenarios it could give a conditional seasonal range. Cannot: predict the winter's energy, since we have no skilful seasonal WEPA input, and `nao_winter` is concurrent/diagnostic only (C_models.md) | CANDHIS buoy Cap Ferret (Cerema); Météo-France seasonal; C3S; OCA bulletins |
| **2. Storm clusters on spring tides → dune-foot attack / scarping** (2013–14-type) | Short return intervals between storms prevent recovery. TWL (tide + surge + runup) exceeds the dune foot, giving dune retreat and megacusp embayments (Castelle et al. 2015). | **None established.** 2013–14 was ENSO-neutral. Clustering is linked to WEPA (Malagon Santos et al. 2017). | Tide phase (the meso-macrotidal range dominates TWL), surge, beach slope, berm presence (thesis), bar state | **Medium-low likelihood** for a 2013–14-scale sequence. **Low** ENSO confidence | Can: estimate per-event ΔV with intervals (conformal ±34–40 m³/m: wide). Cannot: resolve individual storms in a cluster with ~2-week surveys. Cluster count gave no skill (C_models.md) | Météo-France Vigilance vagues-submersion (with SHOM); SHOM tide predictions; OCA storm EWS |
| **3. Southern-track storms (Xynthia-type) → surge + waves at high tide** | NAO− with a southward-shifted jet brings deep lows into Biscay. Surge coincides with high tide. | **Plausible but speculative link:** moderate El Niño → late-winter NAO− (Ineson & Scaife 2009; Jiménez-Esteve & Domeisen 2018). 2009–10 analogue (El Niño + record NAO− + Xynthia). For **strong** events the pattern may differ (Toniazzo & Scaife 2006; Hardiman 2019). | Stratospheric polar-vortex state (watch for SSWs in Jan–Feb), tide phase | **Low-medium likelihood. Low confidence** | Can: the TWL/HAT filter and runup terms flag high-water exposure. Cannot: the surge input has 15 % gaps (B_data.md), and residual runup uncertainty dominates TWL | Météo-France Vigilance vagues-submersion; SHOM/Arcachon tide-gauge residuals (data.shom.fr) |
| **4. Low antecedent beach volume amplifies storm impact** | A beach that starts thin (no berm, eroded upper profile) suffers dune-front retreat for a given E (thesis; Masselink et al. 2023 antecedent-shoreline effect). | None | Recovery history after recent winters (Dodet et al. 2019: multi-annual recovery, stalled by energetic winters). Chronic retreat of the Aquitaine sandy coast (Castelle et al. 2018 ECSS; 1.7–2.5 m/yr in Gironde/Landes per a DREAL/OCA document `[verify]`). | **Unknown.** Our Castelle 2020 record ends 2019-12. No post-2019 Truc Vert surveys found (B_data.md). OCA 2023-24 winter page not opened | Can: equilibrium-type models (Equilibrium B) use antecedent anomaly, which is the only feature with a consistent small gain. Cannot: initialise winter 2026–27 without a recent survey | OCA annual bulletins / profile network; SNO DYNALIT; CoastSat satellite shorelines |
| **5. Elevated mean sea level → higher TWL baseline** | Background SLR plus seasonal/meteorological anomalies raise the TWL exceedance of HAT and the dune foot. | ENSO affects Pacific sea level strongly (Barnard 2017: +11 cm on the US West Coast in 2015–16). **No established ENSO sea-level signal in Biscay** `[verify]` | Global SLR trend; local wind/pressure setup in winter | **High** (trend, small per-winter increment). **Low** ENSO relevance | The model's HAT is fixed (2.14 m). It does not include a sea-level trend or anomaly | SHOM tide gauges (Arcachon/Eyrac, Socoa), data.shom.fr |
| **6. Mild, wet winter → more rainfall-driven dune/cliff runoff** | C3S/Météo-France favour wetter than average. Relevant to dune gullying, not beach volume. | Météo-France composite: a little more rain in SW Europe late winter | — | Medium. Low impact on our ΔV metric | Out of scope | Météo-France |

**Top three risks for winter 2026–27 (with confidence):**
1. **An energetic WEPA+/NAO+ winter on a beach of unknown antecedent state.** Medium likelihood. Low confidence in any
   El Niño modulation. The real blind spot is the beach state after 2019, not ENSO.
2. **Storm clusters coinciding with spring tides (dune-foot attack).** Medium-low likelihood. No ENSO signal.
3. **Southern-track, NAO−-type storms in late winter (Xynthia analogue), more plausible if a sudden stratospheric
   warming occurs.** Low-medium likelihood. Low confidence. This is the only pathway with a published (moderate-event)
   ENSO mechanism.

---

## 5. Implications for this project

### 5.1 Should an ENSO index be a feature? Recommendation: **no** (or only as a documented negative control)

- **Physical prior.** The only beach-data study on this coast finds no ENSO relationship (Masselink et al. 2023). The
  teleconnection is nonlinear, conditional and of uncertain sign (§2.1). Eastern-Atlantic wave power is NAO/WEPA-
  controlled (Bromirski & Cayan 2015; Castelle et al. 2017, 2018).
- **Statistical power.** We have 12–17 winters (v1/v2), and only a handful were El Niño winters. A winter-level ENSO
  feature in a model with n ≈ 50–90 events clustered in ~12 winters would add degrees of freedom with no plausible
  gain. Agent C already found that concurrent winter NAO helps only inside LightGBM, and that variable is diagnostic,
  not prospective.
- **Event-scale redundancy.** Our models use storm-integrated wave energy, so any climate-mode influence already
  flows through the forcing. A seasonal index can only enter as a prior on *how much* energy a winter delivers,
  which belongs in a seasonal outlook, not in the event regression.
- **Acceptable use.** One supplementary ablation (add DJF ONI/RONI, expect no gain) answers the obvious reviewer
  question ("did you consider ENSO?") with a pre-registered negative result. If any climate index is added, **WEPA**
  is the defensible choice (Castelle et al. 2017; Masselink et al. 2023), subject to its CC BY-NC-ND licence and
  manual download (B_data.md §4b).

### 5.2 How an EWS should communicate seasonal outlook vs event forecasts

- **Two products, two time scales, two confidence levels.**
  (a) *Seasonal context* (issued Oct/Nov, updated monthly): "the odds of an energetic winter are near/above/below
  climatology", based on C3S/Météo-France and, if one exists, a WEPA/NAO outlook. It should state that **ENSO
  provides little or no guidance for the Aquitaine coast**, even in a record El Niño year.
  (b) *Event forecast* (2–5 days): Hs, Tp, direction, surge and tide → TWL vs HAT/dune foot → EVI/Equilibrium-B ΔV with
  a prediction interval, mapped to OCA bulletin classes (cf. Leaman et al. 2021 in D_state_of_the_art.md).
- **Avoid false attribution.** Do not label a winter or a storm "El Niño-driven" in Aquitaine. If a big storm happens
  during a strong El Niño year, the bulletin should say the climate mode is not a demonstrated driver here.
- **Use the seasonal outlook only to set preparedness** (e.g. schedule pre-winter surveys, which are the binding
  constraint on our model skill), never to change event thresholds.
- **Antecedent state is the actionable seasonal variable.** A pre-winter survey in Oct–Nov 2026 would do more for
  forecast skill than any climate index.

### 5.3 Paragraph for the paper (introduction or discussion)

> Interannual variability in winter storm erosion along the exposed Atlantic coast of Europe is controlled primarily by
> North Atlantic atmospheric circulation rather than by tropical Pacific variability. Winter-mean and extreme wave
> heights from Portugal to the UK are best explained by the West Europe Pressure Anomaly (WEPA) and, to a lesser extent,
> the North Atlantic Oscillation (Castelle et al., 2017, 2018; Dodet et al., 2010). Across three European beach
> datasets, WEPA explains 50–80% of winter wave-power variability and about a quarter of winter shoreline variability,
> whereas winter waves and shoreline change are unrelated to ENSO (Masselink et al., 2023). This contrasts with the
> Pacific, where ENSO dominates coastal vulnerability (Barnard et al., 2015; Vos et al., 2023) and the 2015–16 El Niño
> drove winter shoreline retreat 76% above normal on the US West Coast (Barnard et al., 2017). ENSO's influence on the
> North Atlantic–European winter is real but nonlinear and conditional. It projects onto an NAO-like pattern mainly in
> late winter, partly through the stratosphere, and its sign over the eastern North Atlantic may change for strong
> events (Toniazzo and Scaife, 2006; Ineson and Scaife, 2009; Hardiman et al., 2019; Mezzina et al., 2020). The
> most erosive winter in the Truc Vert record, 2013–14 (Masselink et al., 2016; Castelle et al., 2015), occurred under
> ENSO-neutral conditions. For an event-scale erosion model at Truc Vert we therefore treat climate modes as
> modulators of the wave forcing, which the model ingests directly, and not as independent predictors. The practical
> limits on predictability are antecedent beach state, storm sequencing and survey spacing (Dodet et al., 2019;
> Masselink et al., 2023).

(Before the paper uses Masselink et al. 2023's site list and ENSO index, confirm them in the full text.)

---

## 6. Sources (all checked 2026-10-13)

### Climate-centre sources and data

| # | Source | URL | Verified |
|---|---|---|---|
| S1 | NOAA CPC, ENSO Diagnostic Discussion, issued 8 Oct 2026 | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso_advisory/ensodisc.shtml | yes (text downloaded and read) |
| S2 | NOAA CPC, Official ENSO Strength Probabilities, issued Oct 2026 | https://cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/strengths/ | yes (table read) |
| S3 | NOAA CPC weekly OISST Niño indices | https://www.cpc.ncep.noaa.gov/data/indices/wksst9120.for | yes (data) |
| S4 | NOAA CPC monthly OISST Niño indices | https://www.cpc.ncep.noaa.gov/data/indices/sstoi.indices | yes (data) |
| S5 | NOAA CPC RONI | https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt | yes (data) |
| S6 | NOAA CPC ONI | https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt | yes (data) |
| S7 | NOAA CPC monthly NAO | https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii | yes (data) |
| S8 | IRI ENSO Forecast (September 2026 issue) | https://iri.columbia.edu/our-expertise/climate/forecasts/enso/current/ | yes (Sept issue. October not yet published) |
| S9 | BoM Climate Driver Update / ENSO, issued 13 Oct 2026 | https://www.bom.gov.au/climate/enso/ | yes (text downloaded and read) |
| S10 | WMO press release, 3 Sep 2026, "El Niño set to become very strong…" | https://wmo.int/news/media-centre/el-nino-set-become-very-strong-raising-risks-of-extreme-weather-2027 | yes |
| S11 | WMO Global Seasonal Climate Update OND 2026 (8 Oct 2026) | https://wmo.int/resources/publication-series/global-seasonal-climate-updates/gscu-ond2026 | yes |
| S12 | Copernicus C3S seasonal forecasts (Oct 2026 issue) | https://climate.copernicus.eu/seasonal-forecasts | yes (summary text. Charts not inspected) |
| S13 | Météo-France, "Le phénomène El Niño s'intensifie…", 2 Oct 2026 | https://meteofrance.com/actualites/le-phenomene-el-nino-sintensifie-quelles-consequences-a-lechelle-planetaire | yes |
| S14 | ECMWF science blog, Stockdale, 10 Apr 2026 (spring ENSO forecast uncertainty) | https://www.ecmwf.int/en/about/media-centre/science-blog/2026/el-nino-2026 | yes (no Europe content) |
| S15 | ReliefWeb, Peru: Floods and Landslides – Feb 2026 | https://reliefweb.int/disaster/fl-2026-000038 | yes (page text read) |
| S16 | CANDHIS (Cerema) wave buoys | https://candhis.cerema.fr/ | yes (reachable. Cap Ferret buoy ID not checked) |
| S17 | Météo-France Vigilance (incl. vagues-submersion) | https://vigilance.meteofrance.fr/fr | yes (reachable) |
| S18 | Observatoire de la Côte de Nouvelle-Aquitaine | https://www.observatoire-cote-aquitaine.fr/ | yes (reachable. Winter 2023-24 page not read) |
| S19 | SHOM data portal | https://data.shom.fr/ | yes (reachable) |
| S20 | DREAL/OCA document on Aquitaine shoreline retreat rates (1.7–2.5 m/yr) | https://webissimo.developpement-durable.gouv.fr/IMG/pdf/5_18_l_evolution_du_trait_de_cote_cle04d1d3.pdf | no (search-result summary only) |
| S21 | California Coastal Commission El Niño 2023-24 memo | https://documents.coastal.ca.gov/assets/climate/extreme-weather/el-nino/Memo_El%20Nino_2023-24_FINAL_8.29.23.pdf | no (not opened) |

### Peer-reviewed literature. DOIs resolved via the Crossref API; abstracts read via OpenAlex/Europe PMC where noted

| Reference | DOI | Verified |
|---|---|---|
| Brönnimann 2007, Rev. Geophys. | https://doi.org/10.1029/2006RG000199 | yes (abstract) |
| Toniazzo & Scaife 2006, GRL | https://doi.org/10.1029/2006GL027881 | yes (abstract) |
| Ineson & Scaife 2009, Nat. Geosci. | https://doi.org/10.1038/ngeo381 | DOI yes. Content from prior knowledge `[verify]` |
| Jiménez-Esteve & Domeisen 2018, J. Climate | https://doi.org/10.1175/JCLI-D-17-0716.1 | yes (abstract) |
| Ayarzagüena et al. 2018, J. Climate | https://doi.org/10.1175/JCLI-D-18-0097.1 | yes (abstract). Early-winter sign `[verify]` |
| Hardiman et al. 2019, GRL | https://doi.org/10.1029/2018GL081776 | yes (abstract) |
| Domeisen, Garfinkel & Butler 2019, Rev. Geophys. | https://doi.org/10.1029/2018RG000596 | yes (abstract) |
| Mezzina et al. 2020, J. Climate | https://doi.org/10.1175/JCLI-D-19-0192.1 | yes (abstract) |
| Scaife et al. 2014, GRL | https://doi.org/10.1002/2014GL059637 | DOI yes. Skill number `[verify]` |
| Scaife et al. 2016, QJRMS | https://doi.org/10.1002/qj.2910 | DOI yes |
| Castelle et al. 2017, GRL (WEPA) | https://doi.org/10.1002/2016GL072379 | yes (abstract) |
| Castelle et al. 2018, GRL (1949–2017 winter waves) | https://doi.org/10.1002/2017GL076884 | yes (abstract) |
| Castelle et al. 2019, Coastal Sediments | https://doi.org/10.1142/9789811204487_0041 | DOI yes. Content `[verify]` |
| Castelle et al. 2015, Geomorphology (2013–14 at Truc Vert) | https://doi.org/10.1016/j.geomorph.2015.03.006 | DOI yes |
| Castelle et al. 2018, ECSS (SW France shoreline 1950–2014) | https://doi.org/10.1016/j.ecss.2017.11.005 | DOI yes. Content `[verify]` |
| Castelle et al. 2020, Sci. Data (Truc Vert 16 yr) | https://doi.org/10.1038/s41597-020-00750-5 | yes (abstract) |
| Dodet, Bertin & Taborda 2010, Ocean Modelling | https://doi.org/10.1016/j.ocemod.2009.10.010 | DOI yes. Numbers `[verify]` |
| Dodet et al. 2019, ESPL | https://doi.org/10.1002/esp.4500 | yes (abstract) |
| Masselink et al. 2016, GRL | https://doi.org/10.1002/2015GL067492 | yes (abstract) |
| Masselink, Castelle, Scott & Konstantinou 2023, GRL | https://doi.org/10.1029/2023GL106019 | yes (abstract). Site list and ENSO index `[verify]` |
| Malagon Santos, Haigh & Wahl 2017, JMSE | https://doi.org/10.3390/jmse5030028 | yes (abstract) |
| Bromirski & Cayan 2015, JGR Oceans | https://doi.org/10.1002/2014JC010440 | yes (abstract) |
| Odériz et al. 2020, JGR Oceans | https://doi.org/10.1029/2020JC016464 | yes (abstract) |
| Reguero, Losada & Méndez 2019, Nat. Commun. | https://doi.org/10.1038/s41467-018-08066-0 | yes (abstract) |
| Morim et al. 2019, Nat. Clim. Change | https://doi.org/10.1038/s41558-019-0542-5 | DOI yes |
| Lobeto, Menéndez & Losada 2021, Sci. Rep. | https://doi.org/10.1038/s41598-021-86524-4 | yes (abstract) |
| Charles et al. 2012, Ocean Dynamics | https://doi.org/10.1007/s10236-012-0534-8 | yes (abstract) |
| Mentaschi et al. 2017, GRL | https://doi.org/10.1002/2016GL072488 | yes (abstract) |
| Barnard et al. 2015, Nat. Geosci. | https://doi.org/10.1038/ngeo2539 | DOI yes. Site count/period `[verify]` |
| Barnard et al. 2017, Nat. Commun. | https://doi.org/10.1038/ncomms14365 | yes (full text via Europe PMC, PMC5316878) |
| Vos et al. 2023, Nat. Geosci. | https://doi.org/10.1038/s41561-022-01117-8 | yes (abstract) |
| Young et al. 2018, JGR Earth Surface | https://doi.org/10.1029/2018JF004771 | yes (abstract) |
| Storlazzi & Griggs 2000, GSA Bull. | https://doi.org/10.1130/0016-7606(2000)112<236:IOENOE>2.0.CO;2 | yes (abstract) |
| Sallenger et al. 2002, Mar. Geol. | https://doi.org/10.1016/S0025-3227(02)00316-X | DOI yes. Content `[verify]` |
| Komar 2001, Coastal Engineering 2000 | https://doi.org/10.1061/40549(276)189 | DOI yes. Content `[verify]` |
| Ranasinghe et al. 2004, Mar. Geol. | https://doi.org/10.1016/S0025-3227(04)00002-7 | DOI yes. Content `[verify]` |
| Mortlock & Goodwin 2016, Cont. Shelf Res. | https://doi.org/10.1016/j.csr.2016.03.007 | DOI yes. Content `[verify]` |
| Harley et al. 2017, Sci. Rep. | https://doi.org/10.1038/s41598-017-05792-1 | DOI yes |

DOI corrections found while checking (do not reuse the wrong forms): Ayarzagüena 2018 is `10.1175/JCLI-D-18-0097.1`
(not `-17-0862.1`). Storlazzi & Griggs 2000 ends `…:IOENOE…` (not `…:IOENOS…`). Mortlock & Goodwin 2016 is
`10.1016/j.csr.2016.03.007` (not `.04.007`). Sallenger 2002 is `S0025-3227(02)00316-X`. Ranasinghe 2004 is
`S0025-3227(04)00002-7`.

### Method note for computed numbers

CPC monthly NAO (DJF mean of Dec, Jan, Feb, labelled by the January year) was correlated with the CPC ONI DJF
value for 1951–2026 (n = 76), using Pearson r with no detrending. The script was not committed (scratch only). It is
reproducible from S6 and S7 in a few lines.
