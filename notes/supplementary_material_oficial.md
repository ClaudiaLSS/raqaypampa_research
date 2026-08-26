# Supplementary Material

**Title:** A Socio-Technical Framework for Modeling Household Energy Behavior in Remote Rural Electrification: A case in Raqaypampa, Bolivia
**Authors:** Claudia Sanchez-Solis, Jaime Zambrana, José Espinoza, Sergio Balderrama, Silvain Quoilin
**Journal:** Energy Research and Social Science

---

## Section S1: Extended Qualitative Methodology

*This section details the qualitative analysis process, bridging the gap between raw data and the quantitative parameters used in the modeling.*

### S1.1 Thematic coding protocol

1. Preparation and Familiarization
    - Objective: Immerse yourself in the socio-cultural context of the Indigenous Originary Peasant Territory (TIOC).
    - Action: Read each transcript fully without coding.
    - Journaling: Use the Journal tab in QualCoder to record initial impressions of Sumaq Kawsay (Living Well) and how it manifests in energy use.
    - File Memos: Document specific context for each household (e.g., Zone A vs. Zone B, or family composition).
1. Phase I: Deductive Coding (Structural)
    - Objective: Apply the Energy Cultures (EC) framework to categorize data into Material Culture, Norms, and Practices.
    - Procedure: Use the predefined codes from your operationalization table.
    - Code Memos: Every deductive code must have a definition in the "Edit Memo" section to prevent "code drift".
        - Example: MAT_Cooking: Only for mentions of firewood, traditional ovens, or specific cooking hardware.
2. Phase II: Inductive Coding (Emergent)
    - Objective: Capture unique Andean realities that the EC framework might miss.
    - Procedure: Identify concepts like Minka (communal work), specific rituals, or "expressions of pride/resistance" to technology.
    - Prefixing: Use a specific prefix for new codes (e.g., RQ_ for Raqaypampa) to distinguish them from the deductive framework.
3. Phase III: Fine-Grained Coding for RAMP Modeling
    - Objective: Extract precise technical parameters needed for the RAMP bottom-up model.
    - Targeted Codes:
        - Appliance Specifics: Create sub-codes for MAT_LED_Lighting, MAT_Radio, and MAT_Phone_Charging.
        - Time Windows: Code for PRAC_Timing_Morning, PRAC_Timing_Evening, and PRAC_Timing_Seasonal.
        - Priority: Code for "User narratives on appliance importance" to understand which loads are shed first during constraints.
4. Phase IV: Thematic Integration and Triangulation
    - Objective: Compare what people say with what the data loggers measure.
    - Action: Use QualCoder’s Reports to aggregate codes.
    - Mapping: Align qualitative themes (e.g., "Gender roles in energy budgeting") with quantitative load profiles.
    - Verification: Check if self-reported "Activity timing" matches the peaks in the measured electricity data.
5. Phase V: Quality Control (The Audit Trail)
    - Code Consistency: Periodically review the "Code Memos" to ensure a code’s meaning hasn't shifted over the 100-household sample.
    - GitHub Sync: Ensure QualCoder is closed before pushing updates to your repository to avoid database corruption.
    - Final Export: Export the Codebook as a CSV to include as a methodological appendix in your thesis.


### S1.2 The Codes

The complete coding tree exported from the QualCoder project (`qualcoder_analysis.qda`). It comprises **96 codes** organised under six top-level categories — Practices, Norms, Material culture, Socio-economics, Impact and Demographics — corresponding to the three core Energy Cultures dimensions (Material Culture, Norms, Practices) plus the socio-demographic and impact dimensions added for a different purpose than this study. The following shows the complete picture of the coding tree:

1. Practices

**Activities (19)**
`PR_act_information_communication`, `PR_act_knitting`, `PR_act_leisure_company`, `PR_act_meals`, `PR_act_mobility_out_of_community`, `PR_act_productive`, `PR_act_school_homework`, `PR_act_single_hh`, `PR_act_sleeping_prep`, `PR_act_socializing`, `PR_act_water_gathering`, `PR_act_work_out_hh`, `PR_dual_home_strategy`, `PR_energy_management`, `PR_fuel_stacking_cooking`, `PR_independent_acquisition`, `PR_substitution`, `PR_sys_maintenance`, `PR_system_mobility`

**Use — Cooking (1)**
`PR_cooking_routine_daily`

**Use — ICT (5)**
`PR_use_ict_day_charging`, `PR_use_ict_night_charging`, `PR_use_radio_continuous`, `PR_use_radio_evening`, `PR_use_TV_night`

**Use — Lighting (5)**
`PR_legacy_lighting_use`, `PR_lights_extreme_night_usage`, `PR_use_lights_time_evening_routine`, `PR_use_lights_time_morning_routine`, `PR_use_portable_lighting`

2. Norms (20)

`NOR_aging_energy_culture`, `NOR_app_aspiration`, `NOR_education`, `NOR_energy_experience_legacy`, `NOR_energy_gatekeeping`, `NOR_energy_savings`, `NOR_energy_sharing`, `NOR_environmental_fear`, `NOR_fear_of_tech_failure`, `NOR_gendered_energy_roles`, `NOR_grid_superiority_perception`, `NOR_labor_activity_constraint`, `NOR_ownership_duty`, `NOR_passive_maintenance`, `NOR_perception_sufficiency`, `NOR_safety`, `NOR_satisfaction`, `NOR_system_capacity_resignation`, `NOR_value_of_connectivity`, `NOR_willingness_to_pay`

3. Material

**Electric appliances (10)**
`MAT_app_blender`, `MAT_app_laptop`, `MAT_app_lighting_fixed`, `MAT_app_lighting_portable`, `MAT_app_phone`, `MAT_app_picolampara`, `MAT_app_radio`, `MAT_app_refrigerator`, `MAT_app_thermal_comfort`, `MAT_app_tv`

**Mobility (2)**
`MAT_transport_moto`, `MAT_transport_public_car`

**Traditional / legacy (5)**
`MAT_fuel_firewood`, `MAT_fuel_gas`, `MAT_legacy_batteries`, `MAT_legacy_candle`, `MAT_legacy_mechero`

**Infrastructure realities (6)**
`MAT_appliance_priority`, `MAT_environmental_vulnerability`, `MAT_geographical_infrastructure_gap`, `MAT_hardware_degradation`, `MAT_optimal_hardware_state`, `MAT_parallel_infrastructure`

4. Socioeconomics

**Demographic & livelihood tags (6)**
`SOC_hh_data_composition`, `SOC_hh_status_elderly_only`, `SOC_hh_status_school_children`, `SOC_livelihood_agriculture`, `SOC_livelihood_jornalero`, `SOC_livelihood_mina`

**Socioeconomic realities (4)**
`SOC_economic_precarity_and_remittances`, `SOC_environmental_hardship`, `SOC_migration_permanent_outflux`, `SOC_migration_temporary_labor`

5. Impact (6)

`IMP_avoided_drudgery`, `IMP_economic_savings`, `IMP_educational_advancement`, `IMP_enhanced_connectivity`, `IMP_extended_waking_hours`, `IMP_health_and_safety`

6. Demographics (7)

`DEMO_children`, `DEMO_female_adult`, `DEMO_female_senior`, `DEMO_male_adult`, `DEMO_male_senior`, `DEMO_youth_female`, `DEMO_youth_male`


In the following table, each entry lists the code label, *n* (the number of coded segments to which the code was applied across the interview corpus; 2,329 segments in total), and the code memo written in QualCoder. Memos follow the standard structure used during coding — **Definition** (what the code captures), **Energy context** (its sociological reading), **Modeling** (how it translates into a load-profile parameter), **Inclusion criteria** (when to apply it) and an **Example quote** (verbatim, in the original Spanish) — except for a small number of descriptive tags coded with free-text memos. Two low-frequency codes carry no memo and are flagged as such.

**Practices** (`1_practices`)

*Activities* (`activities`)

| Code | *n* | Memo |
|:---|---:|:---|
| `PR_act_information_communication` | 10 | **Definition:** The use of energy to power radios or charge cellphones for the purpose of staying informed or communicating.<br>**Energy context:** Sociological: Radios provide vital companionship and local news, while cellphones connect geographically isolated families.<br>**Modeling:** Represents the primary daytime or continuous low-power baseline load (charging phones, running radios).<br>**Inclusion criteria:** Apply when users discuss listening to the radio for news/company, or the critical need to charge phones to talk to migrated family members.<br>**Example quote:** "Acabo de comprarme una radio... ya qué necesito informarme poder escuchar es buena compañía también." |
| `PR_act_knitting` | 2 | They say they use light to knit |
| `PR_act_leisure_company` | 2 | **Definition:** The continuous use of the radio (or the desire for TV) to provide background noise, entertainment, and companionship, especially for adults working alone or pasturing animals.<br>**Energy context:** Sociological: In highly isolated, silent rural environments, the radio acts as a psychological comfort.<br>**Modeling:** Unlike active tasks (cooking, homework) which have defined time windows, "companionship" radio use creates a constant, low-wattage continuous baseline load that can run from 05:00 AM until nighttime.<br>**Inclusion criteria:** Apply when users mention leaving the radio on all day, using it while alone, explicitly calling it "company", or expressing a desire to watch DVDs/TV for entertainment.<br>**Example quote:** "Acabo de comprarme una radio con 200 bolivianas ya qué necesito informarme poder escuchar es buena compañía también." |
| `PR_act_meals` | 20 | **Definition:** The use of SHS energy (primarily lighting) to prepare food, cook, and consume meals as a household.<br>**Energy context:** Sociological: Meal preparation is a core domestic anchor that defines the start and end of the active day, often dictated by agricultural schedules.<br>**Modeling:** This practice creates the two most predictable and inelastic load profile peaks: a brief, early morning peak (e.g., 04:00–06:00) and a longer evening peak (18:00–20:00).<br>**Inclusion criteria:** Apply when users mention using the light specifically to cook, prepare food ("fogón", "cocina"), serve dinner, or eat.<br>**Example quote:** "A veces encendemos la luz de 7:00 a 10:00 de la mañana. Generalmente para cocinar." |
| `PR_act_mobility_out_of_community` | 19 | Residents only leave their communities for essential purchases or urgent needs due to a critical lack of public transportation. For those without private vehicles (motorcycles or cars), the journey requires a three-hour walk each way. |
| `PR_act_productive` | 4 | **Definition:** The use of SHS energy to directly support income-generating activities or specific productive domestic tasks.<br>**Energy context:** Sociological: The SHS transitions from a basic domestic utility to an economic asset.<br>**Modeling:** Introduces specific, potentially high-duration lighting loads or alternative appliance loads (e.g., charging a flashlight for night work).<br>**Inclusion criteria:** Apply when users describe using the light for productive tasks, processing harvests at night, weaving, or specific income-generating chores.<br>**Example quote:** "Esto se hace en la noche con la luz. También se hacen esas frazadas; cuestan como 400 o 500 bolivianos." (Note: Keep PRAC_act_knitting separate only if you want to track knitting specifically versus all productive work). |
| `PR_act_school_homework` | 27 | **Definition:** The use of SHS energy (lighting and occasionally device charging) specifically to support children's schooling and academic homework.<br>**Energy context:** Sociological: The SHS is viewed as a critical educational tool, enabling children to study safely at night without inhaling smoke from candles or mecheros.<br>**Modeling:** Extends the evening lighting load window significantly (often until 22:00 or midnight) and increases priority demand that resists load shedding.<br>**Inclusion criteria:** Apply when participants explicitly mention children doing homework ("tareas", "deberes") under the light, staying up late to study, or the presence of students driving energy use.<br>**Example quote:** "Como están en la secundaria, a veces hacen hasta las 12 de la noche." |
| `PR_act_single_hh` | 24 | **Definition:** The household maintains continuous, year-round residency at the SHS location without engaging in seasonal migration.<br>**Energy context:** Sociological: The system represents the sole, continuous source of modern energy for the household.<br>**Modeling:** Establishes a baseline 365-day continuous load profile without long-term seasonal interruptions.<br>**Inclusion criteria:** Apply when users explicitly state they "never leave," "live here all year," or do not migrate for work.<br>**Example quote:** "Nosotros vivimos solo aquí, aquí me mantengo." |
| `PR_act_sleeping_prep` | 5 | **Definition:** The brief period of lighting used exclusively to transition from evening activities to sleeping.<br>**Energy context:** Sociological: A functional necessity for safety and organization before sleep in rural environments.<br>**Modeling:** Represents the final, often brief, lighting load of the day, defining the end of the evening load window (usually around 21:00–22:00).<br>**Inclusion criteria:** Apply when users state the light is used just to get ready for bed, make the beds, or turn off the system immediately after dinner.<br>**Example quote:** "Solo lo que es necesario para cocinar, cenar y luego prepararse para dormir." |
| `PR_act_socializing` | 18 | **Definition:** Temporary deviations from normal energy routines due to the presence of external visitors, returning family members, neighbour visits or community parties.<br>**Energy context:** Sociological: Energy takes on a communal and hospitable function; providing light and charging ports for guests is a social expectation.<br>**Modeling:** Introduces stochastic (random) "load spikes" where lighting hours are extended (sometimes all night) and charging demand multiplies temporarily.<br>**Inclusion criteria:** Apply when users describe keeping lights on longer, charging more devices, or draining the battery because children are visiting from the city, neighbors come over, or there is a party/wake ("velorio").<br>**Example quote:** "Una vez se apagó la luz cuando había velorio. Como dos noches enteras utilizamos el alumbrado y después se apagó." |
| `PR_act_water_gathering` | 3 | When the memberos of the families go gather water because it is not available on the house. This does not have direct relation with energy. |
| `PR_act_work_out_hh` | 23 | **Definition:** Daily routines where household members leave the home for extended daytime hours to engage in agricultural labor or livestock grazing.<br>**Energy context:** Sociological: The rigorous demands of rural agriculture dictate a "sun-up to sun-down" absence from the home.<br>**Modeling:** Creates a massive "demand valley" or period of zero lighting load during the entire day (e.g., 07:00 to 18:00), restricting energy use strictly to the early morning and night.<br>**Inclusion criteria:** Apply when users mention spending the entire day in the fields, pasturing animals ("pastear", "chacras"), or being away from home during daylight hours.<br>**Example quote:** "Generalmente los agricultores salimos a las 9:00 de la mañana y volvemos a las 5:00 de la tarde." |
| `PR_dual_home_strategy` | 9 | **Definition:** A "bivocational" lifestyle where a family splits their time and activities between a rural/agricultural home (with an SHS) and a more urbanized home (with grid access/ELFEC).<br>**Energy context:** Sociological: The SHS home is zoned for basic survival (eating/sleeping), while the grid home is zoned for economic productivity and modern connectivity.<br>**Modeling:** Creates a complex load profile where the SHS demand appears artificially low, not because the family lacks needs, but because they physically displace heavy loads (weaving, device charging) to the grid-connected home.<br>**Inclusion criteria:** Apply when users describe moving between two houses and specifically delegating certain energy tasks to the house with grid power.<br>**Example quote:** "La radio la hacemos cargar a veces, pero si es en la otra casa donde hay luz de ELFEC, ahí nos vamos para hacer eso." |
| `PR_energy_management` | 11 | **Definition:** Conscious, voluntary actions taken by the user to limit, shift, or optimize energy consumption based on battery state-of-charge or weather conditions.<br>**Energy context:** Sociological: Users demonstrate technical literacy and proactive adaptation to energy scarcity, treating energy as a finite, weather-dependent resource rather than an unlimited utility.<br>**Modeling:** Introduces dynamic load shedding parameters; loads (especially device charging) are shifted from night to day, or dropped entirely, when cloud cover ("nublado") is present.<br>**Inclusion criteria:** Apply when users describe charging phones only when the sun is out, turning off lights to save battery, taking turns charging devices, or avoiding use on rainy days.<br>**Example quote:** "Como la energía es poca, mis hijos se turnan: un día carga uno y al día siguiente el otro para que no nos falte luz." |
| `PR_fuel_stacking_cooking` | 9 | **Definition:** The practice of alternating between traditional biomass (firewood/fogón) and modern fuels (LPG gas) based on environmental conditions or logistical constraints.<br>**Energy context:** Sociological: Users prefer or rely on firewood due to the high cost and extreme difficulty of transporting gas cylinders without roads. Gas is hoarded as a backup for when rain makes firewood unusable.<br>**Modeling:** While this doesn't directly draw electricity from the SHS, capturing this behavior provides vital context for thermal energy modeling and proves that weather dictates all energy choices in the household, not just solar generation.<br>**Inclusion criteria:** Apply when users mention switching to gas only when it rains, or describe the difficulty/cost of buying gas in Raqaypampa.<br>**Example quote:** "Generalmente usamos fogón a leña para preparar nuestra alimentación. Cuando llueve, a veces usamos un poco de cocina con gas; muy poco, porque es difícil ir a comprar el gas." |
| `PR_independent_acquisition` | 10 | **Definition:** The proactive purchase of supplemental or completely independent solar panels/batteries outside of the official NGO or government project.<br>**Energy context:** Sociological: Demonstrates high energy valuation and the limits of the standard project SHS; users seek to upgrade their capacity through private markets.<br>**Modeling:** Indicates that the observed household load might be split across multiple, unmonitored systems, meaning the project SHS datalogger only captures a fraction of the actual household demand.<br>**Inclusion criteria:** Apply when a user mentions buying a "picolámpara," a second panel, a larger battery, or utilizing a legacy system alongside the project SHS.<br>**Example quote:** "Ese otro panel grande que he comprado, con eso hago cargar el celular." |
| `PR_substitution` | 38 | **Definition:** The complete or partial replacement of traditional, precarious, or expensive energy sources (candles, kerosene/mecheros, dry-cell batteries) with the SHS.<br>**Energy context:** Sociological: Represents a leap in energy access, eliminating respiratory hazards (smoke) and ongoing fuel costs.<br>**Modeling:** While this doesn't create a load profile parameter, it justifies the value of the SHS and explains why users might aggressively defend or ration their SHS energy (they do not want to return to buying candles).<br>**Inclusion criteria:** Apply when users talk about what they used before the panel, or explicitly mention that they no longer buy batteries ("pilas") or candles ("velas").<br>**Example quote:** "Antes siempre usábamos vela para alumbrarnos. Teníamos que ahorrar y gastar con cuidado la vela comprando... ya no compro desde que tenemos este panel." |
| `PR_sys_maintenance` | 20 | **Definition:** The physical actions taken (or intentionally avoided) by the user to upkeep the SHS hardware, including cleaning the panel, fixing broken cables, or adding distilled water to batteries.<br>**Energy context:** Sociological: Highlights the technical literacy gap. Some users actively fix wires, while others are terrified to touch the panel.<br>**Modeling:** Panel cleaning practices directly impact the efficiency yield factor in your solar generation model. A panel that is only "washed by the rain" will have a lower generation curve during the dry, dusty season compared to one wiped down weekly.<br>**Inclusion criteria:** Apply when users discuss wiping the panel, letting the rain wash it, fixing broken USB cables/sockets, or avoiding touching the system out of fear of breaking it or lightning strikes.<br>**Example quote:** "A veces hacemos la limpieza cuando vemos que está empolvado. Pero en épocas de lluvia, la lluvia es lo que lo lava, así que vemos que no hay necesidad." |
| `PR_system_mobility` | 21 | **Definition:** The physical dismantling, transportation, and reinstallation of the solar panel and battery to a temporary geographic location (e.g., the monte, agricultural camps, or laguna) for seasonal work.<br>**Energy context:** Sociological: The SHS is not treated as fixed household infrastructure (like grid wiring) but as a portable survival and labor tool.<br>**Modeling:** For load profile generation, this means the load doesn't disappear when the user migrates; instead, the load profile shifts geographically and potentially changes in shape (e.g., different waking/sleeping hours in the monte compared to the main village).<br>**Inclusion criteria:** Apply when users describe packing up the panel, putting it in a backpack, or taking the battery to the fields or another temporary house for weeks/months at a time.<br>**Example quote:** "Ahorita, por ejemplo, voy a ir dentro de tres semanas a trabajar hasta Carnaval. Por eso lo llevo, porque cuando voy allá no hay luz y necesito que me alumbre a donde voy a trabajar." |

*Use* (`use`)

  *Cooking* (`cooking`)

| Code | *n* | Memo |
|:---|---:|:---|
| `PR_cooking_routine_daily` | 14 | **Definition:** The frequency and timing of meal preparation, typically occurring two to three times a day (early morning before the sun rises, and evening after returning from the fields).<br>**Energy context:** Sociological: Cooking is the temporal anchor of the household; it defines the start and end of the active day and dictates when the family gathers.<br>**Modeling:** This routine directly correlates with the "Morning" and "Evening" lighting load windows. Because pre-dawn and post-dusk cooking require illumination, this code establishes the highest probability windows for lighting demand.<br>**Inclusion criteria:** Apply this code when users mention cooking 2 or 3 times a day, waking up early to cook, preparing food to take to the fields as a "merienda", or cooking immediately upon returning home.<br>**Example quote:** "Cocinamos dos veces, a veces tres. En la mañanita cocinamos, luego nos llevamos (la comida) y, por la tarde, retornando, cocinamos para la cena." |

  *ICT* (`ICT`)

| Code | *n* | Memo |
|:---|---:|:---|
| `PR_use_ict_day_charging` | 24 | **Definition:** The intentional practice of plugging in cellphones or rechargeable radios during daylight hours while the solar panel is actively generating power.<br>**Energy context:** Sociological: Shows technical adaptation; users understand that charging during the day prevents depleting the battery needed for nighttime lighting.<br>**Modeling:** This shifts the charging load to coincide with the solar generation curve (e.g., 10:00 to 16:00), effectively "clipping" the load off the battery and using direct solar yield.<br>**Inclusion criteria:** Apply when users mention charging phones/radios during the day, "cuando hay sol," or specifically avoiding nighttime charging.<br>**Example quote:** "El celular lo hago cargar durante el día... Igual, cuando ya carga completamente lo desenchufo para que no se arruine." |
| `PR_use_ict_night_charging` | 14 | **Definition:** The practice of charging cellphones or devices during the evening or overnight hours.<br>**Energy context:** Sociological: Often driven by necessity—devices are used during the day in the fields and can only be charged when the user returns home.<br>**Modeling:** This stacks the charging load on top of the evening lighting load, causing the sharpest drop in the battery's State of Charge (SoC).<br>**Inclusion criteria:** Apply when users mention plugging in their phones when they get home from work, or leaving them plugged in overnight.<br>**Example quote:** "A veces lo cargo en las noches también, hasta el amanecer." |
| `PR_use_radio_continuous` | 4 | **Definition:** The practice of leaving the radio powered on for extended, uninterrupted periods, often spanning the entire workday.<br>**Energy context:** Sociological: The radio serves as constant companionship rather than a tool for brief, targeted information gathering.<br>**Modeling:** Instead of a probabilistic "use window," the radio represents a continuous, flat load profile (e.g., 3-5 watts constantly drawn from 06:00 to 18:00).<br>**Inclusion criteria:** Apply when users say the radio is on "todo el día," or that they take it with them and it plays constantly.<br>**Example quote:** "Escucho la radio desde las 5 de la mañana, todo el día hasta la noche." |
| `PR_use_radio_evening` | 1 | *(no memo recorded)* |
| `PR_use_TV_night` | 1 | **Definition:** The practice of using the Solar Home System to power high-draw visual entertainment appliances, specifically small televisions and CD/DVD players, for brief periods of leisure during the night<br>**Energy context:** Sociological: In geographically isolated communities without broadcast signals, users still highly value visual entertainment, purchasing TVs strictly to watch physical media (CDs/DVDs). However, because standard SHS batteries struggle to sustain this heavy load, this practice is often short-lived and eventually abandoned due to hardware failure or battery depletion.<br>**Modeling:** This introduces a high-wattage, short-duration load spike (typically late in the evening, e.g., 21:00 to 22:00). Because the system struggles to sustain it, your load profile generator should apply a high "failure/abandonment probability" to this variable, meaning the load curve will feature this TV spike for a simulated period before permanently dropping to zero as the appliance breaks or is discarded.<br>**Inclusion criteria:** Apply this code when users explicitly state they actually used, owned, or powered a TV or CD/DVD player using their solar system. (Note: Do not use this code for users who simply state they "wish" they had a TV; those segments should go into the PR_unmet_appliance_demand code).<br>**Example quote:** "Teníamos una TV de 500 bolivianos para ver CDs, porque aquí no llegan canales, pero ya no funciona; antes 'levantaba' con la batería, pero ahora no la ocupamos." (Alternative quote: "Solo por las noches, a partir de las 9, una hora aproximadamente; luego apagamos y ya a descansar. Este otro que tengo también tiene batería.") |

  *Lighting* (`lighting`)

| Code | *n* | Memo |
|:---|---:|:---|
| `PR_legacy_lighting_use` | 1 | **Definition:** The continued, albeit reduced, use of traditional lighting sources like candles ("velas"), kerosene lamps ("mecheros"), or dry-cell battery flashlights despite having an SHS.<br>**Energy context:** Sociological: Highlights that the transition to modern energy is rarely instantaneous or complete. Users may retain traditional methods as backups for when the SHS fails (due to weather or broken components) or for specific tasks where they fear damaging the SHS equipment.<br>**Modeling:** This indicates periods where the household's lighting demand drops to zero on the SHS load profile, not because the household is asleep, but because they have reverted to non-electric alternatives (often during system outages or extreme energy rationing).<br>**Inclusion criteria:** Apply when users mention still using candles, mecheros, or buying dry-cell batteries ("pilas") for lighting, even occasionally.<br>**Example quote:** "A veces usamos linterna con pilas, que aún la utilizo, pero desde que hay luz nos favorece bastante. Cuando caminamos en la oscuridad a veces llevamos vela..." |
| `PR_lights_extreme_night_usage` | 15 | **Definition:** The practice of leaving at least one SHS light illuminated throughout the entire night until dawn, without turning it off.<br>**Energy context:** Sociological: This is often a safety or comfort behavior (e.g., fear of insects/scorpions, or feeling secure).<br>**Modeling:** This fundamentally changes the load profile from a "bell curve" that drops to zero at night to a constant, continuous base load of 1-5 watts (depending on the bulb) from 18:00 to 06:00, significantly draining the battery capacity for the next day.<br>**Inclusion criteria:** Apply when users explicitly state they do not turn the light off when sleeping, or that the light "amanece prendida."<br>**Example quote:** "Por la noche nomás yo enciendo la luz; a veces hago amanecer (la dejo prendida toda la noche)." |
| `PR_use_lights_time_evening_routine` | 62 | **Definition:** The primary period of SHS lighting use, beginning at sunset and ending when the household goes to sleep.<br>**Energy context:** Sociological: This is the core period of family congregation, cooking, eating, and homework.<br>**Modeling:** This establishes the "Evening Load Window" (typically 18:00 to 21:00/22:00). This is the highest probability period for maximum lighting load in the simulation.<br>**Inclusion criteria:** Apply when users describe turning on the light "cuando se pone el sol," returning from the fields, or using it from 6 PM or 7 PM until bedtime.<br>**Example quote:** "Nosotros la usamos una vez que se esté poniendo el sol y la usamos durante toda la noche; apagamos al amanecer." |
| `PR_use_lights_time_morning_routine` | 28 | **Definition:** The practice of utilizing SHS lighting in the early pre-dawn hours to begin the day's activities.<br>**Energy context:** Sociological: Rural agricultural schedules require waking well before sunrise to prepare meals and tend to livestock before heading to the fields.<br>**Modeling:** This establishes the "Morning Load Window" (typically 04:00 to 06:00). In a probabilistic model, this creates a short, sharp spike in early morning demand.<br>**Inclusion criteria:** Apply when users mention turning on the light in the morning, "madrugada", "al amanecer", or waking up at 4:00/5:00 AM to use the light.<br>**Example quote:** "En la madrugada encendemos las luces desde las 4:00 de la mañana, a veces hasta las 10:00, pero generalmente hasta las 7:00 a.m." |
| `PR_use_portable_lighting` | 3 | **Definition:** The practice of using the SHS to charge portable, battery-operated devices like "linternas" (flashlights) or "picolámparas" for mobility outside the main illuminated rooms.<br>**Energy context:** Sociological: Fixed indoor lighting (1 or 2 bulbs) does not solve the need to navigate the dark rural environment—whether to walk to an outdoor latrine, check on livestock, or travel between houses at night. Portable lighting is a necessity for safety and functionality.<br>**Modeling:** This introduces a secondary charging load. It is usually stacked during the daytime charging window alongside cellphones, representing an additional, consistent draw on the system's capacity.<br>**Inclusion criteria:** Apply when users explicitly mention charging or using a "linterna," "picolámpara," or occasionally using their cellphone's flashlight function for outdoor mobility at night.<br>**Example quote:** "Generalmente usamos la luz en casa y, para ir a terminar el trabajo de campo, utilizamos linterna." (Alternative quote: "Sí, usamos linterna. A veces para escoger la papa o desgranar el maíz; para eso a veces uso la linterna en tiempos de cosecha.") |

**Norms** (`2_norms`)

| Code | *n* | Memo |
|:---|---:|:---|
| `NOR_aging_energy_culture` | 7 | **Definition:** The belief that modern appliances (specifically cellphones) belong to, and are only understood by, the youth or children in the household. Also, the belief that senior people uses less energy.<br>**Energy context:** Sociological: Digital exclusion based on age.<br>**Modeling:** Links cellphone charging loads directly to the demographic presence of teenagers/young adults. A house with only elderly adults will have near-zero phone charging demand.<br>**Inclusion criteria:** Apply when users state that only the young people use or know how to charge phones.<br>**Example quote:** "Los dos estudiantes que están estudiando, ellos son los que cargan porque ellos son jóvenes y utilizan más la luz." |
| `NOR_app_aspiration` | 39 | **Definition:** The explicit desire to own higher-tier, modern appliances (such as TVs, refrigerators, or blenders) to improve quality of life and access to entertainment.<br>**Energy context:** Sociological: Reflects a desire to move beyond basic survival energy (lighting/phones) toward modern domestic comfort.<br>**Modeling:** Represents the "latent load" of the household. If modeling a scenario where grid access arrives or SHS capacity is doubled, these heavy loads (e.g., a 50W–100W spike for a TV) must be immediately introduced into the generated profile.<br>**Inclusion criteria:** Apply when users explicitly state they want to buy a TV, refrigerator, or other appliances if they had more power.<br>**Example quote:** "La verdad es que quisiéramos contar con un refrigerador, una licuadora o algo... una televisión podría ser también." |
| `NOR_education` | 28 | **Definition:** The shared cultural value that SHS lighting is primarily a tool to enable children’s academic progress and homework.<br>**Energy context:** Sociological: Lighting is an investment in intergenerational social mobility.<br>**Modeling:** Creates a highly inelastic evening load window (e.g., 19:00 to 22:00) that strongly resists load shedding; parents will sacrifice other energy uses to keep the homework light on.<br>**Inclusion criteria:** Apply when users prioritize light for doing homework ("tareas", "deberes"), or explicitly state the system is for the students.<br>**Example quote:** "La luz es muy elemental para que realicen sus tareas... nos ayuda mucho porque en las noches hacen sus deberes de escuela." |
| `NOR_energy_experience_legacy` | 33 | **Definition:** The psychological and behavioral foundation built upon a user's historical baseline of energy access—encompassing both the hardship of relying on traditional fuels (candles, mecheros, smoke) and prior exposure to other off-grid technologies (privately purchased solar panels, 'picolámparas', car batteries, or legacy NGO projects).<br>**Energy context:** Sociological: This legacy acts as an "Expectation Anchor." Users transitioning directly from candles exhibit extreme conservation habits and profound gratitude, treating the new energy as a finite, precious resource. Conversely, users who previously owned larger legacy systems often exhibit higher technical literacy (e.g., understanding battery degradation) and evaluate the new system's capacity comparatively against their past setups.<br>**Modeling:** This variable helps explain behavioral anomalies in load profiles. It justifies applying a highly conservative probability of use (P) multiplier for users rooted in traditional scarcity, while also explaining why certain households might confidently hack or integrate older infrastructure (like a legacy 120Ah battery) into the new system, creating unexpected load and generation capacities.<br>**Inclusion criteria:** Apply when users compare their current SHS to their past reliance on traditional fuels (candles, kerosene, batteries), OR when they mention owning, buying, or operating older/different solar panels and batteries before the current project system arrived.<br>**Example quote:** "Antes usábamos mechero. Después, a lo posterior, nos compramos un panel solar; había un panel muy grande y su batería también estaba muy bien adaptada." (Alternative quote highlighting the poverty aspect: "Antes siempre usábamos vela para alumbrarnos. Teníamos que ahorrar y gastar con cuidado... ahora ya no compro desde que tenemos este panel.") |
| `NOR_energy_gatekeeping` | 2 | **Definition:** The protective, anxious refusal to share energy or charging ports with outsiders to prevent battery degradation or hardware damage.<br>**Energy context:** Sociological: The protective instinct over a fragile asset overriding communal sharing norms.<br>**Modeling:** Suppresses the formation of informal "mini-grids." Explains why a household with a broken system cannot reliably offload its demand onto a neighbor's working system.<br>**Inclusion criteria:** Apply when users explicitly state they refuse to lend the system, hide it, or dislike others using it to protect it.<br>**Example quote:** "Sí vienen, pero a veces pienso que lo pueden arruinar y por eso a veces no quiero prestarlo... aunque se disgustan o se enojan, ¿qué puedo hacer? Lo tengo que cuidar." |
| `NOR_energy_savings` | 11 | **Definition:** The ingrained habit of turning off systems to "save" energy even when the battery is full, treating solar energy as if it were a consumable, finite resource (like candle wax).<br>**Energy context:** Sociological: Internalized scarcity dictates behavior.<br>**Modeling:** Lowers the theoretical maximum load duration. In the probabilistic model, this justifies using a highly conservative probability of use multiplier for lighting durations.<br>**Inclusion criteria:** Apply when users mention turning off the light to "save" or "no malgastar" energy out of habit, or restricting usage strictly to brief moments.<br>**Example quote:** "Sí, cuidamos. Si no lo utilizamos, pues apagamos la luz... Hasta a veces riño a mis hijos para que cuiden muy bien y no malgasten." |
| `NOR_energy_sharing` | 8 | **Definition:** The cultural expectation and social pressure to provide light and charging access to visiting family, neighbors, or during community events (such as wakes/parties).<br>**Energy context:** Sociological: Energy acts as a communal resource and a tool for hospitality, temporarily superseding individual conservation rules.<br>**Modeling:** Creates massive, unpredictable stochastic load spikes where demand exceeds the system's safe design limits (e.g., lights left on for 48 hours straight).<br>**Inclusion criteria:** Apply when users describe neighbors asking to charge phones, or keeping lights on unusually late to accommodate visitors or community events.<br>**Example quote:** "Una vez se apagó la luz cuando había velorio. Como dos noches enteras utilizamos el alumbrado y después se apagó." |
| `NOR_environmental_fear` | 3 | **Definition:** The specific, culturally reinforced fear that the solar panel attracts deadly lightning ("rayos") or thunder during storms, leading to behavioral changes in how the system is handled.<br>**Energy context:** Sociological: Nature is viewed as an active threat to the new technology.<br>**Modeling:** Introduces a severe seasonal variable. During the rainy season, the probability of the system being physically disconnected by the user increases, drastically altering both the generation (yield) and load profiles.<br>**Inclusion criteria:** Apply when users express fears about lightning hitting the panel, avoiding cleaning it during storms, or wanting to buy "protectores/fusibles" out of fear.<br>**Example quote:** "En épocas de lluvia no limpiamos porque el trueno y el rayo nos asusta. Escuché también que mató a gente... por eso nosotros no limpiamos." |
| `NOR_fear_of_tech_failure` | 11 | **Definition:** Anxiety about interacting with, cleaning, moving, or adjusting the SHS hardware due to a lack of technical literacy and fear of breaking an expensive, irreplaceable asset.<br>**Energy context:** Sociological: A barrier to system optimization.<br>**Modeling:** Explains why broken components (like a loose USB port) remain broken indefinitely, creating permanent drops in the household's load profile (e.g., the radio load permanently disappears).<br>**Inclusion criteria:** Apply when users state they don't touch the panel, are afraid to move it, or avoid maintaining it because they don't know how or fear ruining it.<br>**Example quote:** "No lo reviso tanto. A veces no me ubico bien... No lo llevamos a ningún lado; tememos que se pueda arruinar." |
| `NOR_gendered_energy_roles` | 11 | **Definition:** Social rules dictating that energy access and appliance control are divided by gender (e.g., women prioritize cooking light; men control the radio and mobility of the panel).<br>**Energy context:** Sociological: Energy needs and control are not uniform across the household.<br>**Modeling:** Allows for demographic-based load profiling. If the men migrate to the monte, the radio load drops to zero, but the evening lighting load (for women cooking) remains constant.<br>**Inclusion criteria:** Apply when highlighting that women use the light primarily for the kitchen, while men carry the radio or manage the battery.<br>**Example quote:** "Solo para cocinar utilizan la luz [las mujeres], y la radio también... Los hombres son los que más manejan [la radio]." |
| `NOR_grid_superiority_perception` | 4 | **Definition:** The internalized belief that grid-connected electricity (ELFEC) is the only "real" or "complete" form of energy, making the SHS feel like a temporary or second-class solution.<br>**Energy context:** Sociological: Creates an "Aspiration Gap" where the SHS is never truly viewed as ultimate development.<br>**Modeling:** Drives the dual-home strategy practice, causing users to physically displace heavy loads (weaving, large appliance charging) to grid-connected towns, resulting in an artificially low load profile at the SHS site.<br>**Inclusion criteria:** Apply when users unfavorably compare their solar panel to grid electricity, or express that true development will only happen when "la luz" arrives.<br>**Example quote:** "Están diciendo que la luz va a llegar, pero no sé cuándo llegará... Sería genial porque la corriente carga muy bien." |
| `NOR_labor_activity_constraint` | 6 | **Definition:** The expectation that rural life is entirely structured around constant, exhausting agricultural work, blurring the lines between weekdays and weekends or not allowing performing additional activities.<br>**Energy context:** Sociological: Energy use is strictly utilitarian and subordinated to survival.<br>**Modeling:** Flattens the load profile across all 7 days of the week. Unlike urban energy models that feature distinct "weekend leisure" load shapes, this rural model will use the same load profile every day.<br>**Inclusion criteria:** Apply when users state they work every single day, that weekends are the same as weekdays, or that they are too tired/busy for leisure activities.<br>**Example quote:** "Sábado y domingo lo utilizo como los demás días; normal... la vida en el campo es escasa y hay que trabajar mucho. Los flojos no creo que puedan vivir aquí." |
| `NOR_ownership_duty` | 26 | **Definition:** The internalized sense of duty to protect, maintain, and supervise the SHS hardware because it represents a significant personal and communal financial investment.<br>**Energy context:** Sociological: The system is viewed as a fragile, valuable asset that must be actively stewarded.<br>**Modeling:** This norm acts as a counterweight to hardware degradation. In your model, high ownership duty extends the "useful life" parameter of the battery and panel.<br>**Inclusion criteria:** Apply when users mention actively monitoring the system, scolding children to not touch cables, or expressing that it is their duty to care for it because it cost them money.<br>**Example quote:** "Si el dueño no cuida, ¿quién va a cuidar? Nosotros nomás tenemos que cuidarlo... lo cuidamos mucho porque nos costó dinero." |
| `NOR_passive_maintenance` | 8 | **Definition:** The belief that natural elements (specifically rain) are sufficient to clean and maintain the solar panel, absolving the user of physical maintenance duties.<br>**Energy context:** Sociological: Offloading technical maintenance to environmental patterns.<br>**Modeling:** Directly impacts the solar yield equation. Panels reliant on "passive maintenance" will suffer high "soiling losses" (dust accumulation reducing efficiency by 10-20%) specifically during the dry season.<br>**Inclusion criteria:** Apply when users state they do not clean the panel because the rain washes it.<br>**Example quote:** "Yo pienso que la lluvia nomás tiene que lavarlo; muy poco lo limpio." |
| `NOR_perception_sufficiency` | 3 | **Definition:** The genuine, internalized belief that the basic services provided by the SHS (1-2 lights and phone charging) are completely "enough" for their current rural lifestyle.<br>**Energy context:** Sociological: A mindset where energy needs are defined strictly by basic functionality rather than modern accumulation.<br>**Modeling:** Validates a highly stable, low-variance baseline load profile for specific households.<br>**Inclusion criteria:** Apply when users reject the idea of needing more appliances or explicitly state that their current setup is fine for their needs.<br>**Example quote:** "No creo que pueda abastecer; yo pienso que nada. Con lo que hay, estoy bien." |
| `NOR_safety` | 6 | **Definition:** The belief that the primary value of the SHS is physical security—protecting the family from tripping in the dark or being bitten by venomous insects.<br>**Energy context:** Sociological: Lighting is a barrier against rural physical hazards.<br>**Modeling:** Drives the continuous night lighting practice. This norm provides the behavioral justification for programming a continuous 12-hour base lighting load in the simulation.<br>**Inclusion criteria:** Apply when users describe feeling safe from the dark, scorpions (alacranes), vinchucas, or tripping hazards.<br>**Example quote:** "Una vez me picó un bicho, creo que era alacrán... Ahora que hay luz, ya no hay bichos que nos piquen. Antes por la oscuridad no se veía... nuestros hijos a veces pisan algo." |
| `NOR_satisfaction` | 43 | **Definition:** Expressions of deep contentment, relief, or positive evaluation regarding the SHS, often stemming from a comparison to past hardships rather than objective technical perfection.<br>**Energy context:** Sociological: Satisfaction in rural contexts is often relative to absence (zero energy), not abundance.<br>**Modeling:** Justifies why users do not abandon the system or resort to tampering even when it experiences minor blackouts. It ensures a low "abandonment rate" in your model.<br>**Inclusion criteria:** Apply when users explicitly express thanks, state they are happy/content, or say "nos favorece bastante" despite noting technical flaws.<br>**Example quote:** "Sí, estamos felices y contentos porque antes, cuando era niño y hacía las tareas, era todo oscuro, no se veía nada... me ayuda mucho." |
| `NOR_system_capacity_resignation` | 49 | **Definition:** The user’s pragmatic, often frustrated acknowledgment that the SHS cannot support their desired appliances, leading them to intentionally suppress their energy demands and purchases.<br>**Energy context:** Sociological: Users exhibit high technical awareness of their system's limits, prioritizing battery health over modern comfort.<br>**Modeling:** Explains the "flatness" of the baseline demand over time. It justifies why the algorithm should NOT organically grow the household's appliance ownership over simulated years.<br>**Inclusion criteria:** Apply when users express a desire for an appliance but immediately follow up by saying they won't buy it because the system "no abastece", "no levanta", or the battery would drain.<br>**Example quote:** "Yo quisiera comprarme [una TV], pero no creo que pueda abastecer la carga porque es muy escasa a veces." |
| `NOR_value_of_connectivity` | 0 | **Definition:** The shared belief that the primary value of device charging is to maintain family ties and monitor the safety of children who have geographically migrated for work or school.<br>**Energy context:** Sociological: The cellphone is not a luxury gadget; it is an emotional lifeline bridging the rural-urban divide.<br>**Modeling:** Makes cellphone charging a "critical, inelastic load." Even if the battery is dangerously low, users will prioritize charging the phone over other activities to ensure they can receive calls from migrated family members.<br>**Inclusion criteria:** Apply when users mention charging phones specifically to talk to their children/family in other regions, or highlighting distance as the reason for needing the phone.<br>**Example quote:** "El celular es importante para informarse y comunicarse... cuando uno está a distancias separadas. Yo también tengo dos nietos... ellos ahora están en el Chapare." |
| `NOR_willingness_to_pay` | 4 | **Definition:** Expressions of financial readiness, explicit intent, or willingness to spend out-of-pocket cash to purchase replacement parts (cables, bulbs), new appliances, or system upgrades for the Solar Home System. It also includes explicit statements validating the financial cost of the current system as "worth it."<br>**Energy context:** Sociological: In cash-scarce rural environments, willingness to pay is the ultimate proof of energy valuation. It shows the transition of the SHS from a "project gift" to a critical household utility that the family is willing to financially defend and maintain.<br>**Modeling:** This is a predictive variable. Households tagged with high NOR_willingness_to_pay have a higher probability of recovering from MAT_hardware_degradation (because they will buy replacement parts) and a higher probability of organically growing their load profile over time (by purchasing new appliances).<br>**Inclusion criteria:** Apply when users ask the interviewers where they can buy parts, offer to buy components directly from the interviewers, discuss saving money for an appliance, or explicitly state that the contraparte (the fee they paid for the panel) was a good price and they would pay it again.<br>**Example quote:** "Cuánto no quisiera que pudiesen traer focos; por lo menos un foco necesitamos. Se los puedo comprar a ustedes; quizás lo que falte lo pueden traer y nosotros se lo compramos." (Don Remigio, User 6)<br>**Alternative quote:** "Ahora, ¿será que hay para comprar? Así estaba pensando... Solo el problema es su punta, que se rompió." (Celestina Inturias, User 64) |

**Material culture** (`3_material`)

*Appliance and infrastructure tags (descriptive)* (`appliance_and_infraestructure_tags_descriptive`)

  *Electric appliances* (`electric_appliances`)

| Code | *n* | Memo |
|:---|---:|:---|
| `MAT_app_blender` | 1 | Tracks exactly which object is being used, desired, or degraded. In this case, blenders. |
| `MAT_app_laptop` | 1 | Tracks the ownership, presence, and usage of portable laptops. Unlike fixed LED bulbs, these represent a mobile energy demand that can be disconnected from the main system. |
| `MAT_app_lighting_fixed` | 117 | Tracks the ownership, presence, and usage of Permanent LED bulbs installed in the household structure. |
| `MAT_app_lighting_portable` | 26 | Tracks the physical presence, usage, explicit desire for, or hardware degradation of portable rechargeable lighting devices (such as "linternas" and "picolámparas"). |
| `MAT_app_phone` | 85 | Tracks the ownership, presence, and usage of mobile phones. Unlike fixed LED bulbs, these represent a mobile energy demand that can be disconnected from the main system. |
| `MAT_app_picolampara` | 7 | *(no memo recorded)* |
| `MAT_app_radio` | 70 | Tracks the ownership, presence, and usage of rechargeable radios. Unlike fixed LED bulbs, these represent a mobile energy demand that can be disconnected from the main system. |
| `MAT_app_refrigerator` | 5 | Tracks the physical presence, usage, explicit desire for, or hardware degradation of refrigerators. |
| `MAT_app_thermal_comfort` | 0 | Tracks the physical presence, usage, explicit desire for, or hardware degradation of thermal comfort devices (such as "ventiladores" and "calentadores"). |
| `MAT_app_tv` | 20 | Tracks the ownership, presence, and usage of TV or DVD players. |

  *Mobility* (`mobility`)

| Code | *n* | Memo |
|:---|---:|:---|
| `MAT_transport_moto` | 3 | Private motorcycles. |
| `MAT_transport_public_car` | 7 | Public transit, buses, or community trucks. |

  *Traditional* (`traditional`)

| Code | *n* | Memo |
|:---|---:|:---|
| `MAT_fuel_firewood` | 20 | Biomass used in a fogón for cooking. |
| `MAT_fuel_gas` | 10 | Propane/LPG gas cylinders for cooking. |
| `MAT_legacy_batteries` | 10 | "Pilas" (disposable dry-cell batteries). |
| `MAT_legacy_candle` | 25 | Velas |
| `MAT_legacy_mechero` | 25 | Mecheros and kerosene lamps. |

*Infrastructure realities* (`infraestrucure_realities`)

| Code | *n* | Memo |
|:---|---:|:---|
| `MAT_appliance_priority` | 19 | **Definition:** The ranking or explicit valuation of specific physical appliances (typically LED lights vs. cellphones vs. radios) regarding which piece of hardware is most essential to the household's daily survival.<br>**Energy context:** Sociological: In extreme energy scarcity, users rank hardware based on its immediate impact on safety, connectivity, or labor.<br>**Modeling:** Establishes a "Load Shedding Hierarchy" for your simulation. When the battery's SoC drops, the model needs a rule for which appliance to turn off first (e.g., sacrifice radio to save the lights).<br>**Inclusion criteria:** Apply when users explicitly state which device is the "most important," or describe consciously unplugging one device to ensure another has enough battery.<br>**Example quote:** "Utilizamos más para cargar el celular, porque es importante... [pero] solo para el alumbrado de los focos y celulares." |
| `MAT_environmental_vulnerability` | 20 | **Definition:** The physical susceptibility of the material infrastructure to environmental factors, specifically reduced battery capacity due to cloud cover or physical damage from rain/lightning.<br>**Energy context:** Sociological: The infrastructure is not isolated from nature; the physical battery dictates what is possible on any given day.<br>**Modeling:** Directly correlates solar yield to the physical state of the battery. Justifies algorithms where continuous cloudy days trigger immediate load shedding in the simulation.<br>**Inclusion criteria:** Apply when users describe the physical battery draining instantly, lights shutting off due to clouds, or hardware struggling during the rainy season.<br>**Example quote:** "Pasa que la batería de este panel solar se agota de forma inmediata cuando se nubla o llueve... hasta dos o tres días deja de funcionar." |
| `MAT_geographical_infrastructure_gap` | 11 | **Definition:** The physical reality of geographical isolation, lack of roads, and the necessity of maintaining multiple physical residences (or migrating) due to environmental constraints (lack of water/arable land).<br>**Energy context:** Sociological: The lack of physical infrastructure forces mobility, which in turn forces energy to be mobile.<br>**Modeling:** Explains the PR_system_mobility practice. If a house has no water, the family moves, and the load profile drops to zero (or shifts geographically if they take the panel).<br>**Inclusion criteria:** Apply when users mention the lack of roads ("camino"), the difficulty of transporting gas/water, or the physical necessity of moving between two houses.<br>**Example quote:** "Para comprar gas ni siquiera hay camino para que pueda ingresar el auto... es una situación complicada." |
| `MAT_hardware_degradation` | 47 | **Definition:** Segments detailing the physical deterioration, fragility, or literal breakage of the SHS infrastructure, appliances, or connecting cables.<br>**Energy context:** Sociological: Hardware in rural environments is subjected to dust, rain, and physical stress. Because supply chains for parts are non-existent, minor failures result in permanent loss of access.<br>**Modeling:** Introduces a "hardware decay rate" to the simulation. Explains why a household's load profile might inexplicably drop to zero for a specific appliance (e.g., the radio load disappears forever because the USB port broke).<br>**Inclusion criteria:** Apply when users describe broken screens, snapped cables, burnt-out LED filaments, loose USB ports, or radios that no longer emit sound.<br>**Example quote:** "Se había roto esta parte y la radio tampoco está funcionando... ya no funciona." |
| `MAT_optimal_hardware_state` | 29 | **Definition:** Explicit confirmation that the physical components of the SHS (panel, battery, lights, charging ports) or the appliances are functioning as designed.<br>**Energy context:** Sociological: Confirms successful technology adoption and baseline satisfaction.<br>**Modeling:** Establishes the baseline control group for your load profiles (i.e., what the load curve looks like when everything is working perfectly).<br>**Inclusion criteria:** Apply when users confirm the lights do not turn off unexpectedly, the battery holds a charge all night, and devices plug in without issue.<br>**Example quote:** "Sí, está muy bien el alumbrado; respecto al panel, está bien también." |
| `MAT_parallel_infrastructure` | 28 | **Definition:** The physical presence and utilization of secondary energy hardware (such as legacy NGO solar panels, privately purchased panels, or car batteries) operating alongside the main project SHS.<br>**Energy context:** Sociological: Households patch together "bricolage" energy systems to survive, stacking multiple generations of technology.<br>**Modeling:** Critical for load profiling. If the datalogger is only attached to the project SHS, it is missing data. Identifies households where the total domestic load is split across multiple physical systems.<br>**Inclusion criteria:** Apply when users mention plugging things into a different panel, hooking a TV up to a car/motorcycle battery, or referencing owning a second SHS.<br>**Example quote:** "Ese otro panel grande que he comprado, con eso hago cargar el celular... a veces le pongo la batería de la moto, así lo uso." |

**Socio-economics** (`4_socioeconomics`)

*Demographic and livelihood tags* (`demographic_and_livelihood_tags`)

| Code | *n* | Memo |
|:---|---:|:---|
| `SOC_hh_data_composition` | 42 | Use this anytime the user lists who lives in the house (e.g., "I live with my wife and two kids"). |
| `SOC_hh_status_elderly_only` | 0 | Tag indicating the household consists solely of aging |
| `SOC_hh_status_school_children` | 20 | Tag indicating school-aged children live in the home. |
| `SOC_livelihood_agriculture` | 52 | The household's primary subsistence is farming/livestock. |
| `SOC_livelihood_jornalero` | 4 | Members perform temporary day-labor for cash ('jornalero'). |
| `SOC_livelihood_mina` | 3 | Members work in mining sectors. |

*Socio-economic realities* (`socioeconomic_realities`)

| Code | *n* | Memo |
|:---|---:|:---|
| `SOC_economic_precarity_and_remittances` | 9 | **Definition:** The absolute constraint of cash scarcity in a subsistence farming environment, occasionally alleviated by financial support (remittances) or gifts from migrated family members.<br>**Energy context:** Sociological: Cash is rare. The ability to climb the "energy ladder" (buying a TV or a better panel) is blocked not by a lack of desire, but a lack of capital. Conversely, when new appliances do arrive, they are often gifts from urban children.<br>**Modeling:** Explains the gap between NORM_appliance_aspiration and actual ownership. It confirms that the standard load profile should not artificially inflate with new appliance purchases over time unless an external financial injection is simulated.<br>**Inclusion criteria:** Apply when users state they cannot afford appliances, or when they mention that their migrated children send them money, cellphones, or radios as gifts.<br>**Example quote:** "La economía no da para comprar [una TV]... a veces los hijos que están en el Chapare nos ayudan con alguito para la comida o nos traen una radio." |
| `SOC_environmental_hardship` | 10 | **Definition:** The severe geographical and environmental constraints of the region, specifically droughts, lack of potable water, and poor agricultural yields.<br>**Energy context:** Sociological: Nature pushes the family out of the house. You cannot stay in a house with electric lighting if there is no water to drink.<br>**Modeling:** This is the environmental trigger for MAT_geographical_infrastructure_gap. It justifies probabilistic modeling rules where severe dry seasons correlate with a higher probability of household abandonment (and thus, energy demand dropping).<br>**Inclusion criteria:** Apply when users mention lack of water, failed crops, or difficult geographic conditions forcing them to change their daily routines or locations.<br>**Example quote:** "Ahora mismo, como no hay agua aquí, es un poco difícil quedarse... por eso a veces voy arriba. No hay agua para tomar ni para los animales." |
| `SOC_migration_permanent_outflux` | 30 | **Definition:** The permanent out-migration of younger family members (children/grandchildren) to urban centers (Cochabamba, Santa Cruz) or other regions (Chapare) in search of education or better economic conditions.<br>**Energy context:** Sociological: Leaves behind an aging rural population. It physically removes the "tech-savvy" generation from the SHS infrastructure.<br>**Modeling:** This socio-economic reality creates the NOR_value_of_connectivity norm. It guarantees a highly inelastic, continuous demand for cellphone charging among the elderly who remain, specifically to receive calls from these migrated children.<br>**Inclusion criteria:** Apply when users mention their children or relatives moving away permanently to study or live, even if they visit occasionally.<br>**Example quote:** "Mis hijos ya son mayores, ya tienen su familia, ellos ya viven en otro lado... se fueron a Santa Cruz a buscar vida." |
| `SOC_migration_temporary_labor` | 32 | **Definition:** The cyclical, temporary relocation of household members (often men, but sometimes the whole family) for days, weeks, or months to engage in agricultural work in the monte, mining, or day labor (jornalero).<br>**Energy context:** Sociological: Rural survival requires spatial fluidity; the "home" is not continuously occupied.<br>**Modeling:** This is the root cause of the PR_system_mobility practice. When this code overlaps with a household, your load profile generator must account for "seasonal absences" where the baseline load drops to zero (if the family leaves the system behind) or shifts to a different geographic node (if they pack the panel in a backpack).<br>**Inclusion criteria:** Apply when users describe leaving their main house temporarily to work, go to the monte, or seek wage labor elsewhere.<br>**Example quote:** "Ahorita, por ejemplo, voy a ir dentro de tres semanas a trabajar hasta Carnaval. Por eso lo llevo [el panel], porque cuando voy allá no hay luz." |

**Impact** (`5_impact`)

| Code | *n* | Memo |
|:---|---:|:---|
| `IMP_avoided_drudgery` | 4 | **Definition:** The elimination of physical travel, logistical planning, and time wasted specifically to procure basic energy services (e.g., walking for hours solely to charge a phone). Sociological context: Captures the "time poverty" alleviation. Time previously spent walking to grid-connected towns for basic services can now be redirected to rest or labor.<br>**Inclusion criteria:** Apply when users mention the hardship of how they used to acquire energy or charging services before the SHS.<br>**Example quote:** "Porque antes íbamos a hacer cargar hasta Raqaypampa, porque hay pues la luz ahí... Como no había, entonces ¿qué podíamos hacer? Íbamos lejos. Ahora actualmente ya no es necesario ir; en ese sentido nos favorece bastante." |
| `IMP_economic_savings` | 11 | **Definition:** The direct retention of household cash due to the complete or partial cessation of purchasing precarious energy sources like candles, kerosene, and disposable dry-cell batteries. Sociological context: In a subsistence farming economy where cash is extremely scarce, freeing up 10 to 40 Bolivianos a week from the family budget is a massive economic relief.<br>**Inclusion criteria:** Apply when users explicitly state they no longer spend money on candles (velas), kerosene, or batteries (pilas), or when they mention the high cost of those items.<br>**Example quote:** "Ya no compro desde que tenemos este panel. Ya no compramos... Ahora también se escucha que las pilas están caras para comprar, creo que tienen un costo de 10 Bs. el par de pilas." |
| `IMP_educational_advancement` | 3 | **Definition:** The facilitation of children's academic responsibilities, allowing them to study, read, and complete homework after the agricultural workday ends. Sociological context: Represents the intergenerational impact of the project. Energy access directly supports human capital development.<br>**Inclusion criteria:** Apply when users state the system helps their children or grandchildren do their homework (tareas / deberes).<br>**Example quote:** "Nuestros hijos a veces en la oscuridad pisan algo... Cuando empezó a tener esta iluminación, todo mejoró... La luz es muy elemental para que realicen sus tareas." |
| `IMP_enhanced_connectivity` | 2 | **Definition:** The enhanced ability to maintain relationships with migrated family members and access external information due to reliable, at-home device charging. Sociological context: In communities hollowed out by migration, the SHS powers the emotional lifeline (the cellphone) that keeps fractured families connected across the country.<br>**Inclusion criteria:** Apply when users cite the ability to call family, stay informed, or coordinate work/visits because their phone is now reliably charged.<br>**Example quote:** "Yo veo que utilizan bastantes celulares; es tan necesario para comunicarnos cuando uno está a distancias separadas. Yo también tengo dos nietos... ellos ahora están en el Chapare." |
| `IMP_extended_waking_hours` | 4 | **Definition:** The alteration of the household's temporal boundaries, allowing for nighttime productive tasks, communal socializing, or safe cooking well past sunset. Sociological context: Overcomes the natural limits of the sun. It allows adults to shift non-agricultural labor (like weaving) into the nighttime, or simply enjoy a well-lit dinner together.<br>**Inclusion criteria:** Apply when users mention doing tasks at night that would be impossible without the LED light (weaving, late cooking, hosting visitors/parties).<br>**Example quote:** "Sí, a veces realizo el tejido hasta la 1 de la mañana... Es muy bueno la luz para avanzar así alguna de nuestras actividades." |
| `IMP_health_and_safety` | 9 | **Definition:** The direct improvement of respiratory health due to the elimination of toxic smoke from traditional fuels, coupled with enhanced physical safety from rural hazards (e.g., avoiding tripping, seeing venomous pests). Sociological context: Moves energy access from a "convenience" to a literal life-saving intervention. The elimination of kerosene smoke directly reduces respiratory illness, while LEDs protect against the local fauna.<br>**Inclusion criteria:** Apply when users mention no longer breathing smoke, no longer burning their hair with mecheros, or being able to see scorpions (alacranes), vinchucas, or tripping hazards.<br>**Example quote:** "Antes solo teníamos mechero, que desprendía mucho humo... Desde eso nos enfermamos. Una vez me picó un bicho, creo que era alacrán... Ahora que hay la luz, ya no hay bichos que nos piquen." |

**Demographics** (`6_demographics`)

| Code | *n* | Memo |
|:---|---:|:---|
| `DEMO_children` | 0 | **Definition:** Children under the age of 12. In the transcripts, this is identified by tags like [RMC] (Respondent Male Child) or [RFC] (Respondent Female Child).<br>**Energy context:** Sociological: Passive beneficiaries of electricity. While they don't buy the panels, their needs (doing homework, fear of darkness, breaking cables while playing) fundamentally drive the adults' energy behavior.<br>**Modeling:** Justifies the "inelasticity" of the evening lighting load; parents will not turn off the light if a child is studying, even if the battery is low.<br>**Inclusion criteria:** Apply to segments spoken by children ([RMC]), or when adults explicitly describe children's interactions with the light or hardware.<br>**Example quote:** "[R1]: ¿Vas al colegio? [RMC]: No. [R1]: ¿Al año vas a ir? [RMC]: Sí." |
| `DEMO_female_adult` | 207 | **Definition:** Women in their productive years (approx. 18–60). In the transcripts, this is explicitly identified by the tag [RFA] (Respondent Female Adult).<br>**Energy context:** Sociological: This group represents the "Time Poverty" dimension, managing domestic operations, cooking, and childcare.<br>**Modeling:** They are the primary drivers of the evening lighting load. Their usage patterns directly affect the daily depth of discharge (DoD) of the battery, as cooking and evening chores are non-negotiable energy demands.<br>**Inclusion criteria:** Apply to all text segments spoken by an [RFA], or when other users specifically describe the activities of the adult women in the house.<br>**Example quote:** "[RFA]: Solo para cocinar utilizan la luz [las mujeres], y la radio también..." |
| `DEMO_female_senior` | 61 | **Definition:** Older women (approx. 60+). In the transcripts, this is explicitly identified by the tag [RFS] (Respondent Female Senior).<br>**Energy context:** Sociological: This group is highly sensitive to the "Safety and Security" aspect of lighting and holds the deep historical memory of traditional fuel hardships.<br>**Modeling:** Their presence justifies continuous, low-wattage base loads, as they often leave lights on all night to prevent tripping or deter wildlife (venomous insects).<br>**Inclusion criteria:** Apply to all text segments spoken by an [RFS].<br>**Example quote:** "[RFS]: Antes solo caminábamos con vela, con mecherito. Yo cuando era niña solo conocía el mecherito y con eso alumbraba..." |
| `DEMO_male_adult` | 425 | **Definition:** Men in their productive years (approx. 18–60). In the transcripts, this is explicitly identified by the tag [RMA] (Respondent Male Adult).<br>**Energy context:** Sociological: This group often acts as the "technical gatekeeper." They are usually responsible for the initial purchase, installation, and physical transport of the system to the monte.<br>**Modeling:** Their presence or absence (due to temporary migration) dictates the mobility of the system and the use of heavy/continuous loads like the radio.<br>**Inclusion criteria:** Apply to all text segments spoken by an [RMA], or when others describe the male head of household's actions.<br>**Example quote:** "[RMA]: Aquí nomás paro; no voy a ningún lado. Por eso este [panel] cuido; no sé llevar a ningún lado." |
| `DEMO_male_senior` | 59 | **Definition:** Older men (approx. 60+). In the transcripts, this is explicitly identified by the tag [RMS] (Respondent Male Senior).<br>**Energy context:** Sociological: Traditional authority figures whose testimony provides the historical baseline of the community. They often exhibit a mix of deep gratitude for the system and "learned helplessness" regarding technical repairs.<br>**Modeling:** Generates a highly conservative energy usage profile characterized by strict rationing and early sleep schedules.<br>**Inclusion criteria:** Apply to all text segments spoken by an [RMS].<br>**Example quote:** "[RMS]: De noche nomás prendo la luz y se queda prendido hasta que amanezca... Si no estamos aquí, prendido lo dejamos la luz." |
| `DEMO_youth_female` | 4 | **Definition:** Female adolescents and young adults (approx. 12–21). In the transcripts, this is explicitly identified by the tag [RFY] (Respondent Female Youth).<br>**Energy context:** Sociological: This group bridges the gap between traditional domestic roles (weaving/cooking) and educational aspirations.<br>**Modeling:** Their presence creates a stacked load profile in the evening: they require light for domestic chores, followed immediately by light for homework, creating a sustained 4-to-5 hour lighting demand window.<br>**Inclusion criteria:** Apply to all text segments spoken by an [RFY].<br>**Example quote:** "[RFY]: No, en la mañana nomás hilamos la lana... Empezamos el miércoles de la anterior semana; ya llevamos una semana haciendo." |
| `DEMO_youth_male` | 8 | **Definition:** Male adolescents and young adults (approx. 12–21). In the transcripts, this is explicitly identified by the tag [RMY] (Respondent Male Youth).<br>**Energy context:** Sociological: They represent the "Modern Demand" profile, heavily focused on digital connectivity. They are also the group most likely to permanently migrate.<br>**Modeling:** Drives the highest frequency of daytime charging loads. A household with a [RMY] will consistently show a higher daily draw on the battery for USB charging compared to households without them.<br>**Inclusion criteria:** Apply to all text segments spoken by an [RMY].<br>**Example quote:** "[RMY]: A partir de las 7 de la noche, generalmente [encendemos la luz]... A veces sí [apagamos]; pero cuando hacemos las tareas, así en esas temporadas, no la apagamos mucho." |

### S1.3 Logic Analysis and Socio-Technical Rules

The following steps are used to identify the Socio-Technical Rules that govern the energy behavior of the households in the study. These rules are derived from the co-occurrence of practices, norms, demographics, and material constraints.

**Step 1: Identify the "Anchor" Practices (The "What")**

First, core energy events that define the load profile are identified.
- Action in QualCoder: Run a Code Frequencies report strictly on your 1_practices category.
- What to look for: Identify the practices with the highest counts. Based on the codebook, these will likely be `PR_use_lights_time_evening_routine` (count: 56), `PR_act_school_homework` (count: 21), and `PR_use_ict_day_charging` (count: 17). These high-frequency practices are your temporal anchors.

**Step 2: Run Co-occurrence Queries (The "Who" and the "Why")**

An energy practice doesn't exist in a vacuum; it is driven by specific people and cultural rules.
- Action in QualCoder: Use the Code Co-occurrence / Matrix Tool to overlap anchor practices with Demographics, Norms, and Material constraints.
- Example of query to run:
    - Query A: Overlap `PR_use_lights_time_evening_routine` with DEMO codes to see exactly who is driving the evening peak.

**Step 3: Write "Logic Memos" (Formulating the Rule)**

Once the frequently overlapping codes are identified, intersections must be translated into narrative rules.
- Action in QualCoder: Open a new Memo for each major theme and use a standard formula to write the behavioral logic.
- The Formula: [Norm/Demographic] drives [Practice] under [MaterialConstraint].
- Example Output: "The deep cultural value placed on intergenerational advancement (`NOR_education`) dictates that the evening lighting window (`PR_act_school_homework`) is non-negotiable, even when the battery is physically depleted due to bad weather (`MAT_environmental_vulnerability`)".

The extracted Socio-Technical rules are listed below, organized into four main themes:

**Theme 1: The Daily Baselines (Predictable Anchors)**

*These rules define the rigid, highly probable load curve shapes that occur almost every single day, unaffected by minor weather changes.*

*Rule 1: The Educational Anchor*

- **Formula:** [`NOR_education` / `DEMO_youth_male` & `DEMO_youth_female`] drives [`PR_act_school_homework` / `PR_use_lights_time_evening_routine`] under [`MAT_appliance_priority` / limited battery capacity].

- **The Narrative:** The cultural priority of intergenerational academic progress dictates that the evening lighting window is non-negotiable. Parents will actively restrict daytime appliance use or unplug radios to ensure enough battery remains for children to study safely under LED lights until 22:00.

- **RAMP Modeling Implication (Temporal & Reliability):** Protects the "Critical Discharge Window." In the simulation, the evening lighting load (18:00–22:00) is highly inelastic (Probability of Use = ~1.0) and receives the highest priority in the load-shedding hierarchy.

*Rule 2: The Agricultural Dictate*

- **Formula:** [`NOR_labor_activity_constraint` / `DEMO_male_adult` & `DEMO_female_adult`] drives [`PR_cooking_routine_daily` / `PR_use_lights_time_morning_routine`] under [`SOC_livelihood_agriculture` / rigorous agricultural schedules].

- **The Narrative:** The necessity of "sun-up to sun-down" agricultural labor forces households to wake well before dawn. Energy behavior is constrained by this survival routine, necessitating an early period of lighting for meal preparation before the family abandons the house.

- **RAMP Modeling Implication (Temporal & Shape):** Establishes a short, sharp early morning demand spike (e.g., 04:00 to 06:00) followed immediately by a massive "demand valley" where household load drops to absolute zero during daylight hours.

*Rule 3: The Gendered Anchor of Domestic Operations*

- **Formula:** [`NOR_gendered_energy_roles` / `DEMO_female_adult`] drives [`PR_act_meals`] under [`MAT_appliance_priority` / fixed LED lighting].

- **The Narrative:** Social norms dictate that adult women are primarily responsible for the kitchen and evening meal preparation. This routine acts as the temporal anchor for the household, defining the start of the evening active period.

- **RAMP Modeling Implication (Magnitude & Temporal):** The presence of `DEMO_female_adult` guarantees the most consistent evening lighting demand window, directly dictating the daily depth of discharge (DoD) of the battery.

*Rule 4: The Connectivity Lifeline*

- **Formula:** [`NOR_value_of_connectivity` / `DEMO_female_senior` & `DEMO_male_senior`] drives [`PR_act_information_communication` / `PR_use_ict_day_charging`] under [`SOC_migration_permanent_outflux` / permanent migration of children].

- **The Narrative:** For elderly populations left behind by rural-urban migration, the cell phone is an emotional lifeline, not a luxury. Maintaining a charged phone to communicate with children in the Chapare or cities is prioritized over personal lighting.

- **RAMP Modeling Implication (Reliability):** Device charging is categorized as a "critical load." Even at low battery levels, the simulation should execute this draw, bypassing standard energy-saving logic.

*Rule 5: The Digital Delegation*

- **Formula:** [`DEMO_youth_male` & `DEMO_youth_female`] operates [`PR_use_ict_day_charging`] on behalf of [`DEMO_female_senior` & `DEMO_male_senior` / `DEMO_female_adult` & `DEMO_male_adult`] under [`NOR_digital_literacy_gap` / generational device-operation divide].

- **The Narrative:** Even where an adult or elder is the nominal owner of the household's phone, day-to-day operation is routinely delegated to the youngest capable household member. Elders in particular disclaim operational competence outright rather than describing infrequent use: *"Mi hijo menor es el que utiliza el celular; yo no lo utilizo"* (my youngest son is the one who uses the phone; I don't use it), and *"Yo también tengo dos nietos; ellos son los que manejan celulares, yo no"* (I also have two grandchildren; they're the ones who handle phones, not me). This delegation is not confined to the home: *"Aquí nomás lo tengo; no sé manejarlo cuando salgo"* (I only have it here; I don't know how to operate it when I go out). This rule is distinct from Rule 4 (The Connectivity Lifeline): Rule 4 explains *why* a household values keeping a phone charged; Rule 5 explains *who* within the household actually operates it, and predicts that charging-event frequency will track the presence of a youth or school-aged member rather than the presence of the nominal phone owner.

- **RAMP Modeling Implication (Demand Attribution):** The `PR_use_ict_day_charging` load should not be probabilistically gated on adult or elder presence alone. In mixed-generation households, charging-event probability should instead be weighted toward the presence of a school-aged or youth resident, independent of who nominally owns the device.

**Theme 2: System Constraints & Coping Mechanisms**

*These rules define how users dynamically interact with the physical limits of the environment and the battery.*

*Rule 6: Weather-Driven Load Shedding*

- **Formula:** [`NOR_system_capacity_resignation` / `DEMO_female_adult` & `DEMO_male_adult`] drives [`PR_energy_management` / `PR_use_ict_day_charging`] under [`MAT_environmental_vulnerability` / cloudy or rainy weather].

- **The Narrative:** Users exhibit high technical literacy regarding their system's limits. When weather conditions prevent full charging, users proactively "load shed" by rationing light and aggressively shifting their mobile charging strictly to peak daylight hours to protect the battery's state of charge.

- **RAMP Modeling Implication (Temporal):** Shifts the charging load profile to perfectly coincide with the solar generation curve (e.g., 10:00 to 16:00), effectively "clipping" demand off the battery.

*Rule 7: The Safety Baseline*

- **Formula:** [`NOR_safety` / `DEMO_female_adult` & `DEMO_female_senior`] drives [`PR_lights_extreme_night_usage`] under [`IMP_health_and_safety` / presence of venomous insects and physical hazards].

- **The Narrative:** The culturally reinforced fear of venomous fauna (scorpions, vinchucas) and tripping hazards overrides general conservation habits, prompting users (especially mothers and the elderly) to leave at least one light illuminated until dawn.

- **RAMP Modeling Implication (Shape & Magnitude):** Radically alters the load curve. Instead of dropping to zero after 22:00, the simulation must apply a continuous 12-hour base load (1–5 W), drastically impacting the starting State of Charge (SoC) for the following day.

*Rule 8: Infrastructure Mobility*

- **Formula:** [`NOR_ownership_duty` / `DEMO_male_adult`] drives [`PR_system_mobility`] under [`SOC_migration_temporary_labor` / seasonal agricultural work in the "monte"].

- **The Narrative:** Due to extreme geographical isolation and the necessity of seasonal agricultural migration, the SHS is treated as a portable survival tool rather than fixed household infrastructure. Men actively dismantle and transport the system to temporary camps.

- **RAMP Modeling Implication (Reliability & Shape):** Introduces "seasonal absences." The algorithm must probabilistically drop the baseline load to zero for periods ranging from weeks to months at the primary geographic coordinate.

*Rule 9: Nature as a Threat (Environmental Fear)*

- **Formula:** [`NOR_environmental_fear` / `DEMO_female_senior`] drives [Avoidance of `PR_sys_maintenance`] under [`MAT_environmental_vulnerability` / thunderstorms and lightning].

- **The Narrative:** Culturally reinforced fears that solar panels attract deadly lightning strikes lead users to physically disconnect the system or actively avoid touching/cleaning it during the rainy season.

- **RAMP Modeling Implication (Generation/Yield Model):** Introduces a severe seasonal variable. Increases the probability of complete physical disconnection during stormy months and increases "soiling losses" (dust accumulation) due to reliance strictly on passive rain-washing.

**Theme 3: Structural Anomalies**

*These rules explain the chaotic, unpredictable data points in the datalogger that traditional engineering models fail to simulate.*

*Rule 10: The Aspiration Gap and Dual-Home Displacement*

- **Formula:** [`NOR_app_aspiration` / `DEMO_male_adult`] drives [`PR_dual_home_strategy`] under [`MAT_geographical_infrastructure_gap` / lack of grid connectivity at the SHS location].

- **The Narrative:** The desire for modern comfort (TVs, blenders) cannot be met by the SHS. Rather than abandoning the desire, families maintain a bivocational lifestyle, delegating heavy energy tasks to a secondary, grid-connected home while zoning the SHS home strictly for basic survival.

- **RAMP Modeling Implication (Magnitude / Latent Demand):** Explains why the current load curve is artificially flat. It provides the mathematical parameters for a "grid-arrival" or "capacity doubling" simulation, triggering immediate high-wattage spikes (50–100 W) that are currently suppressed.

*Rule 11: Protective Gatekeeping*

- **Formula:** [`NOR_ownership_duty` & `NOR_fear_of_tech_failure`] drives [`NOR_energy_gatekeeping`] under [`MAT_hardware_degradation` (fear of)].

- **The Narrative:** The intense fear of breaking a fragile, irreplaceable financial asset overrides indigenous communal sharing norms. Users actively refuse to let neighbors charge devices to protect their USB ports from damage.

- **RAMP Modeling Implication (Reliability):** Prevents peer-to-peer load dumping. In the simulation, if Household A's system fails, the algorithm cannot assume Household A's demand safely shifts to Household B's profile.

*Rule 12: Community Override (Stochastic Spikes)*

- **Formula:** [`NOR_energy_sharing`] drives [`PR_act_socializing`] under [`IMP_extended_waking_hours` / Community Events].

- **The Narrative:** Normal routines of strict energy conservation are temporarily suspended during major community events (e.g., *velorios* or visiting relatives). Energy becomes a tool for communal hospitality.

- **RAMP Modeling Implication (Variability):** Explains massive, unpredictable standard deviations. Provides the behavioral logic to program low-probability, high-impact "stochastic spikes" where lighting is drawn continuously for 48 hours, fully depleting the system.

*Rule 13: Hardware Resignation (The Silent Drop)*

- **Formula:** [`NOR_fear_of_tech_failure`] drives [Permanent load reduction] under [`MAT_hardware_degradation`].

- **The Narrative:** Due to a lack of technical literacy and missing supply chains, minor hardware failures (e.g., a snapped jack or loose USB port) result in the permanent abandonment of the appliance rather than a repair.

- **RAMP Modeling Implication (Shape & Reliability):** Introduces a "hardware decay rate" to the model. Load curves must simulate permanent, step-wise drops to zero for specific appliances (like the continuous 3 W radio load disappearing mid-year).

**Theme 4: Productive Labor & Multi-Energy Realities**

*Rule 14: The Productive Lighting Veto (The Weaving Constraint)*

- **Formula:** [`NOR_labor_activity_constraint` / `DEMO_female_adult`] restricts [`PR_act_productive` / `PR_act_knitting`] under [`MAT_appliance_priority` (low lumens) & `IMP_health_and_safety` (insects/polillas)].

- **The Narrative:** Despite having evening illumination, adult women actively *refuse* to use the SHS light for income-generating textile work (weaving/spinning). They cite two physical constraints: the LED light is not "nítida" (clear/bright) enough for detailed work, and the light attracts moths (*polillas*) which ruin the valuable wool. Thus, productive textile labor remains strictly anchored to daylight hours. *(Found in transcripts: Users 72, 81, 85).*

- **RAMP Modeling Implication (Shape/Magnitude Constraint):** Prevents the algorithm from artificially extending the evening lighting load window for productive tasks. It proves that simply providing a basic 2 W bulb does *not* automatically trigger nighttime economic productivity in the simulation.

*Rule 15: Fuel Stacking*

- **Formula:** [`MAT_geographical_infrastructure_gap` / lack of roads] drives [`PR_fuel_stacking_cooking`] under [`MAT_environmental_vulnerability` / Rain].

- **The Narrative:** While this does not draw electricity, it is vital for multi-energy modeling. Users default to gathered firewood for cooking because the lack of roads makes carrying heavy LPG gas cylinders on foot grueling. However, when it rains and firewood gets wet, users immediately switch to their hoarded LPG gas.

- **RAMP Modeling Implication (Multi-Energy Profiling):** If you are running RAMP as a multi-energy simulator (thermal + electrical), this rule dictates the thermal load switch. It proves that *weather* is the master variable in Raqaypampa, dictating not just solar generation, but also the choice of cooking fuel.

*Rule 16: The Gratitude/Scarcity Baseline

- **Formula:** [`NOR_energy_experience_legacy`] defines [`PR_substitution` / `MAT_legacy_candle` / `MAT_legacy_mechero`].

- **The Narrative:** Users' baseline relationship to electricity is shaped less by the SHS itself than by memory of what came before it. Having lived for years with candles or the mechero — a rudimentary wick lamp that produces heavy, irritating smoke — respondents describe the transition in explicitly medical terms, not just financial ones: "Antes solo teníamos mechero, que desprendía mucho humo... Desde eso nos enfermamos, porque es mucho humo" (before we only had a mechero, which gave off a lot of smoke... we got sick from it, because it's a lot of smoke). This lived hardship produces a durable sense of gratitude that tempers consumption: users treat the LED light as a hard-won substitution for a harmful past, not as a baseline utility to be used freely, and this restraint persists independently of how much capacity the system actually has available.

- **RAMP Implication:** The memory of toxic smoke and buying candles creates a highly conservative behavioral baseline. This justifies assigning a lower-than-average relative mean power factor, as users treat the LED light as a precious commodity, not an infinite utility.

*Rule 17: The Sedentary Anchor / Aging in Place*

- **Formula:** [`MAT_physical_constraint` / `DEMO_male_senior` & `DEMO_female_senior`] restricts [`PR_system_mobility`] under [`SOC_migration_temporary_labor`].

- **The Narrative:** Due to the physical limitations of aging, elderly households do not participate in the temporary, labor-intensive migration to the *monte*. They remain anchored to the primary residence year-round, serving as caretakers of the permanent household infrastructure.

- **RAMP Modeling Implication:** Protects "Profile 2: Isolated Elderly" from seasonal load-shedding. The simulation must maintain a continuous 365-day baseline for this demographic, completely blocking the stochastic "Absence/Vacation" modifier that is applied to younger, agriculturally active profiles.

### S1.4 Language and Translation Notes

All interviews were conducted in the first language of the Raqaypampa communities, which is Quechua as spoken locally — a variety with substantial Spanish borrowing and frequent within-utterance code-switching, in which certain lexical domains (numerals, calendar and clock terms, and many frequency and timing expressions) are commonly rendered in Spanish even inside otherwise-Quechua speech. Respondents themselves comment on this mixing in the corpus. All interviews were audio-recorded in full. Transcription and translation were carried out as a single integrated step by a bilingual (Quechua–Spanish) research team member, who listened to each recording and produced a written Spanish transcript directly from the audio; this person also conducted a subset of the interviews personally and worked from the audio alone for the remainder. The resulting Spanish transcripts constitute the working corpus (all_transcripts.txt) on which all subsequent qualitative analysis was performed. Alongside the interview corpus, field memos (memos.csv) were written in Spanish by the main researcher, who participated in every field visit; the interviewers themselves rotated across visits according to team availability, so the memos are the one continuous authorial voice spanning the full fieldwork period. This is what licenses their status as a distinct, dated evidence tier in the derivation protocol (§2.1).

Because the interviews were held in Quechua and coded in Spanish, one act of translation sits between the spoken source and every coded segment, and we describe the transcripts as translated rather than verbatim on that ground. Two features of the local language situation reduce how much interpretive work that step actually does for the analysis. First, the expressions the crosswalks (Supplementary Material S1.2–S1.3) most depend on — frequency markers such as a veces, de vez en cuando, cada tres días, and timing markers such as hasta las 10 or al oscurecer — are precisely the lexical items most often spoken in Spanish in Raqaypampa, so for a substantial share of the anchor material the transcript reproduces the respondent's own words rather than a translated equivalent. Second, transcription and translation were performed together by a single Quechua-speaking listener working from the audio, rather than as a two-stage pipeline, so idiom and hedging in the genuinely Quechua stretches were interpreted in the context of the whole utterance. Coding was then performed directly on the Spanish transcripts, with no further re-translation; quotes reproduced in this paper in English were translated from the Spanish transcript for presentation only.

Using a single bilingual translator throughout ensured consistent handling of recurring terms and idiom across the entire corpus, at the cost of the independent back-translation or second-translator check a larger team would permit. Two features of the protocol mitigate this. First, the Spanish transcript is the primary (tier-1) evidence for every crosswalk anchor, is attributable to a named respondent and date, and remains open to re-inspection, so each classification decision can be traced back to a specific translated utterance. Second, the crosswalks deliberately map language onto coarse ordinal bins rather than fine numerical readings, so the analysis depends on the broad frequency or rigidity sense of an expression surviving translation — a lower bar than exact lexical fidelity — which further limits the leverage any single translation choice has on a final parameter value.

---

## Section S2: Energy Behavior Profiles (EBP) and Parameter Derivations

*This section corresponds to the items explicitly placed in "Supplementary Material S1" within the main manuscript.*

### **S2.1 Population Counts per Profile**

Each behavioral profile is defined over two nested subpopulations: the full survey-derived set of households assigned to the profile (N_survey), and the subset of those households for which a qualitative interview was conducted (N_interview). All qualitative parameters are inferred from N_interview and applied uniformly to N_survey at simulation time.

| Profile | Description | N_survey | N_interview | Interview coverage |
|---------|-------------|:--------:|:-----------:|:------------------:|
| 1 | Educational and Agricultural Core | 28 | 18 | 64% |
| 2 | Isolated Elderly | 11 | 9 | 82% |
| 3 | Extended Hub | 14 | 9 | 64% |
| 4 | System Breakers | 12 | 6 | 50% |
| **Total** | — | **65** | **42** | **65%** |

*Coverage is the share of survey-derived households in each profile that were also interviewed (N_interview / N_survey). Profile 2 is the best-covered profile in the study; Profile 4 carries the thinnest qualitative base.*

Households are identified by anonymous survey ID (matching `data_0.csv`). For
each profile, the interviewed subpopulation (N_interview) is a subset of the
survey-derived population (N_survey); the remaining IDs are survey-only.

| Profile | Survey-derived households (N_survey) | Interviewed subset (N_interview) | Survey-only (not interviewed) |
|---------|--------------------------------------|----------------------------------|-------------------------------|
| 1 — Educational and Agricultural Core | 6, 8, 16, 17, 19, 20, 21, 26, 28, 32, 34, 44, 51, 53, 58†, 62, 63, 72, 74, 80, 81, 83†, 88, 90, 94, 95, 99, 100 | 6, 8, 19, 20, 44, 58†, 62, 63, 72, 74, 80, 81, 83†, 88, 90, 94, 95, 99 | 16, 17, 21, 26, 28, 32, 34, 51, 53, 100 |
| 2 — Isolated Elderly | 4, 11, 14, 37, 48, 50, 52, 57, 84, 86, 91 | 4, 11, 14, 37, 48, 52, 57, 84, 91 | 50, 86 |
| 3 — Extended Hub | 7, 13, 15, 29, 30, 31, 33, 38, 49, 61, 67, 69, 75, 78 | 7, 13, 29, 33, 38, 61, 67, 69, 78 | 15, 30, 31, 49, 75 |
| 4 — System Breakers | 23, 25, 27, 40, 42, 54‡, 64‡, 65, 71, 76, 92, 96 | 23, 40, 54‡, 64‡, 76, 96 | 25, 27, 42, 65, 71, 92 |

† IDs 58 and 83 are placed in Profile 4 by the canonical classification source
(`classifications_oficial.csv`) but are held in Profile 1 by an analyst
override (Profile 1 truth file, §8).

‡ IDs 54 and 64 are placed in Profile 1 by the canonical classification source
but are held in Profile 4 by an analyst override (Profile 4 truth file, §2,
Rule 9).

*The four profiles together cover 65 of the 100 surveyed households; the
remaining 35 are unclassified or excluded and are not represented above.*

### **S2.2 Crosswalk Tables**
To understand the parameter derivation protocol, the crosswalks designed to translate qualitative evidence into quantitative simulation parameters are provided below. These are used to derive two main characteristics of appliance use: the probability of being used (occasiona_use) and the rigidity of each activity (main source for the randomization parameters).

This crosswalk was built inductively from the interview corpus and refined against it, in the following steps:

1. **Parameter-driven extraction.** Starting from what RAMP actually requires (`occasional_use`, `time_fraction_random_variability`, `random_var_w`), the interview transcripts for each of the four EBP profiles were searched for the language respondents use to express *frequency* (how often a practice occurs) and *temporal variability* (how stable its timing is). This yielded a corpus of naturally-occurring frequency and timing expressions in the respondents' own words (Spanish/Quechua-Spanish), each tied to a specific respondent, profile, and interview date.
   
2. **Inductive binning.** Recurring expressions were grouped into a small number of bins. Where respondents gave an explicit countable frequency ("tres veces por semana," "cada tres días"), these were handled by a direct formula rather than a bin (see Table 1). Where language was qualitative only ("a veces," "de vez en cuando," "siempre"), it was grouped into ordinal bins and assigned a representative probability/variability value.

3. **Cross-profile validation.** Each bin was checked against anchor quotes drawn from *multiple* profiles, not a single one, to confirm that a given expression carries approximately the same meaning regardless of who says it (e.g., that "a veces" implies a similar frequency whether spoken by an elderly single resident or a school-age household).

4. **Iterative refinement where bins broke.** The scheme was revised wherever transcript evidence contradicted an initial definition. Two substantive revisions are recorded rather than hidden, because they demonstrate the crosswalk was tested against the data:
   - The **"Chaos" bin was redefined** from an outcome-based criterion (timing varies day to day) to an *epistemic* one (the respondent's own account signals they cannot specify a stable pattern — hedging language, self-contradiction, explicitly unanchored windows).
   - **Household-level structural absence** (dual residence, extended absence) was distinguished from practice-level variability and made a separate axis, triggered by **explicit dual-household or extended-absence language in the interview narrative** — not by the survey's `migration_label`, which is too common across the sample to discriminate (most households show some migration), and not by EBP profile membership either — because multi-month absence was found in a Profile 3 household, not only in Profile 4.
  
5. **Priority-override layer.** Practices anchored to a profile's non-negotiable social rules (education, subsistence cooking) are assigned Daily/Fixed frequency and Strict variability by default, overriding isolated hedging language, since such hedging typically concerns incidental detail rather than whether the practice occurs (see override note in Table 1).

**Provenance.** Every value applied in a truth file traces back through these tables to at least one anchor quote (respondent ID, profile, interview date). Anchor quotes shown here are representative; a full quote-by-quote mapping is maintained in the supplementary provenance file. This crosswalk is the single canonical source for both parameters; profile truth files reference it rather than reproducing it, so revisions propagate consistently.

---

**Table 1 — Frequency Language → `occasional_use`**

**Priority override (apply before any other rule below):** if a practice is anchored to an established non-negotiable social rule for the profile (e.g., education, subsistence cooking, or any other rule the profile's truth file defines as non-negotiable), default to **Daily/Fixed** frequency (`occasional_use` ≈ 1) and, on the variability table, **Strict** (0.1) — regardless of hedging language ("a veces," "depende") appearing in isolated quotes about that practice. Such hedging is almost always about an incidental detail (which exact task, whether the light stays on the full duration), not about whether the practice occurs that day. Override this default only with specific, explicit evidence of exception (a stated skip pattern — e.g., "solo cuando no hay tarea" — not just soft phrasing).

Example: Zenón García's *"la necesitamos cada día por las noches; los chicos van haciendo sus tareas"* (P1, 26/02/2026) already reflects this correctly — homework light is `occasional_use: 1`, Strict variability — because it is anchored to the Educational rule, not because every quote about it used "siempre."

**Primary rule (use whenever an explicit count is given, and the priority override doesn't apply):**

> occasional_use = active_days ÷ interval_days

This generalizes the simple weekly case (e.g., "tres veces por semana" → 3/7 = 0.42) to any stated interval (e.g., "cada tres días" → 1/3 = 0.33; "una vez al mes" → 1/30 ≈ 0.03).

**Fallback bins (use only when language is qualitative, with no explicit count to compute from):**

| Bin | Value | Markers | Example anchors |
|---|---|---|---|
| Daily / Fixed | 0.85–1.0 | "siempre," "todos los días," "cada día," "constantemente" | *"Nosotros cargamos siempre el celular"* — Edelfrida Jiménez Salazar, P1, 26/02/2026; *"Yo hago cargar mi celular siempre"* — Felipe Rivera, P3, 20/11/2024 |
| High frequency | 0.6–0.8 | "con frecuencia," "generalmente," "casi siempre" | *"con frecuencia usamos el fogón"* — Guillermo Negrete, P1, 25/02/2026; *"generalmente usamos la luz en casa"* — Isabel Zurita, P3, 24/02/2026 |
| Occasional / Moderate | 0.35–0.5 | "a veces," "depende" (standalone, no explicit count) | *"A veces lo cargamos en el día o en la noche"* — Dionisio Vargas Castro, P1, 25/02/2026 |
| Low / Sporadic | 0.15–0.3 | "de vez en cuando," "no muy seguido" | *"Lo limpiamos de vez en cuando"* — Domingo Vallejos, P1, 20/11/2024 |

**Documented exception — capacity-driven decline (resolved from B7):** where reduced frequency is attributed to the respondent's own physical capacity (age, hearing, mobility) rather than to the practice's inherent regularity, apply the same bins above based on the *resulting* frequency described, with an explicit narrative note on cause (for interpretive transparency, not a separate numeric treatment). E.g., *"estando mayores... casi no ocupamos en las madrugadas"* — Germán Calderón (esposa), P2, 25/03/2026 → Low/Sporadic, with a note that the driver is age-related, not seasonal or task-related.

---

**Table 2 — Rigidity → window-timing variability parameters (`time_fraction_random_variability` **and** `random_var_w`)**

**Scope and definitions (per RAMP documentation):** these are two *distinct* parameters, both driven by the same underlying rigidity judgment (Strict/Flexible/Chaos) but randomizing different things:
- `time_fraction_random_variability` — randomness applied to the appliance's **total functioning time** (`func_time`); i.e., how much the *quantity of daily use* varies.
- `random_var_w` — randomness applied to the **size of the functioning window** (the w_1/w_2 bounds); i.e., how much the *permissible time-envelope* stretches or contracts.

A single rigidity assessment sets a *pair* of values (one for each parameter), not one shared value. A more rigid practice receives lower values on both; a more chaotic one, higher on both — which is why the Strict evening practice (VA3) carries both a low `time_fraction_random_variability` and a low `random_var_w`. But the two values are recorded separately per appliance.

Representative paired values (`time_fraction_random_variability` / `random_var_w`):
- **Strict** → ~0.1 / ~0.2
- **Flexible** → ~0.2 / ~0.3
- **Chaos** → ~0.3 / ~0.35+

The bin criteria and anchor quotes below apply to the rigidity judgment itself; the paired values above follow from it.

| Bin | Value | Markers | Example anchors |
|---|---|---|---|
| Strict | 0.1 | Anchored to external, non-negotiable constraint (school, sunrise/sunset, fixed task) | *"la necesitamos cada día por las noches; los chicos van haciendo sus tareas"* — Zenón García (hija), P1, 26/02/2026; *"Desde las 6 de la tarde alumbra por mis hijos, hasta las 10 de la noche"* — Felipe Rivera, P3, 20/11/2024 |
| Flexible | 0.2 | Bounded window, shifts with daily circumstance; "depende," "algo así" | *"Dependiendo. A veces desde las 6:00... depende de a qué hora nos levantamos"* — Edelfrida Jiménez Salazar, P1, 26/02/2026 |
| Chaos | 0.3 | Practice's timing is genuinely unstable *and the respondent's own account signals this* — hedging/vague language ("es muy variado," "no se sabe," "depende de tantas cosas"), self-contradictory statements about timing, or an explicitly wide, unanchored window. Epistemic marker: low confidence visible in how the person describes it, not just variation in outcome | *"Dependiendo. A veces en las mañanas, una hora o algunas veces dos horas también. Por las noches usamos de 7:00 a 8:00, o a veces de 6:00 a 10:00 de la noche; es muy variado"* — Calixto Agreda Inturias, P2, 25/02/2026 |


**Chaos vs. Flexible boundary:** Flexible = respondent *can* describe a bounded pattern that shifts with circumstance ("depende de a qué hora nos levantamos"). Chaos = respondent *cannot* reliably describe a pattern at all. The distinguishing signal is in the report itself, not in the objective outcome.

---

### **S2.3 Parameter derivation protocol**

This section is the source describing how each RAMP parameter in the Model B (socio-technical) parametrization is derived. Profile truth files reference this section rather than reproducing it, so revisions propagate consistently.

Every parameter falls into one of six derivation sources, stated explicitly so that no value is left without a declared basis. Five of the six derive a **per-appliance** parameter; two of those five are **crosswalks** — classification steps that sort respondent language into bins. The sixth derives the one **household-level** parameter, which is not a property of any appliance:

- **[SPEC]** — technical hardware specification (not behavioral; no qualitative translation)
- **[WINDOW]** — derived from the Anthropological Window (interview × survey triangulation)
- **[FREQ-XW]** — frequency crosswalk (Table 1, Section S2.2): respondent frequency language → `occasional_use`
- **[RIG-XW]** — rigidity crosswalk (Table 2, Section S2.2): the qualitative account → a rigidity bin (Strict / Flexible / Chaos), which *is* the variability classification
- **[DECLARED DEFAULT]** — a stated, reasoned value used when neither qualitative nor quantitative data directly speaks to a parameter; flagged as pending real data, never presented as derived.
- **[OCC]** — occupancy derivation: stated absence durations → `prob_home`, the probability a household of the profile is present on a given day. Household-level, not per-appliance: one value per profile (optionally per season), gating *every* VA of that household at once.

A note on the two crosswalks, since they are the same kind of object: both **[FREQ-XW]** and **[RIG-XW]** are classification steps that read respondent language and assign a bin. The rigidity crosswalk (Table 2, Section S2.2) directly yields `time_fraction_random_variability` and `random_var_w` (they are the bin's assigned values). One parameter, `func_cycle`, is a **second-order derivation**: it takes the rigidity bin and applies a further rule (fraction of `func_time`), so it is marked [RIG-XW → func_time] to show it is one step removed rather than a direct crosswalk output.

**A further distinction governs citation, not derivation, and sits underneath [WINDOW]/[FREQ-XW]/[RIG-XW] rather than beside them.** §2.3.1 below defines a three-tier auditability hierarchy for the *qualitative material itself* — interview transcript, field memo, conversational recall. This hierarchy does not add a new kind of RAMP-parameter derivation; it governs how solidly a given [WINDOW]/[FREQ-XW]/[RIG-XW] value is sourced, and is recorded in the `— source:` trailer, not in the derivation tag.

One phenomenon is handled *outside* the per-appliance parameters: **household-level structural absence** (migration/dual-residence), which since 2026-08-18 is an applied model parameter rather than a documented-but-deferred one — it is derived via **[OCC]** into `prob_home` and simulated as RAMP's household-level occupancy mask. 

---

**Population and generalization (who the qualitative parameters actually describe)**

The `ebp_profile` classification is itself survey-derived (family_type, occupation, children_in_school, migration, portability_shs). This means **every classified household has survey data**, but only a subset was also interviewed. Each profile therefore has two population sizes, not one:

- **N_survey** — everyone classified into the profile (defines who counts as that EBP)
- **N_interview** — the subset also interviewed (the only source of qualitative material)

| Truth-file output | Population it draws from | Why |
|---|---|---|
| Windows (`window1`, `window2`) | **N_interview + N_survey** (triangulated) | Anthropological Windows are derived by triangulating interview accounts of practice timing with survey time-use data and hard physical anchors (sunrise/sunset) — survey and physical data alone can't supply the cultural framing, and interview accounts alone can't supply population-scale timing or fixed astronomical anchors |
| Rigidity classification (incl. Extreme/Structural), narrative, frequency-language `occasional_use` | **N_interview only** | Requires actual quotes — a household with no transcript can't supply timing statements, hedging language, or evidence of a dual-household strategy |
| `prob_home` — [OCC], household-level occupancy (§10) | **N_interview only** as the numerator *and* the denominator | Requires a stated absence duration, which only a transcript supplies. The denominator is the full interviewed base, so the value describes the profile rather than its mobile subset — and `migration_label` cannot substitute for the missing survey households |
| Ownership/appliance-count parameters | **N_survey (full)**, where the survey captured them | Structural, not behavioral |

#### S2.3.1 Evidence tiers within Stream A (QUAL): transcript, field memo, conversational recall

Not all qualitative material carries the same auditability. Three tiers, ranked by how independently checkable the claim is:

1. **Interview transcript** (`all_transcripts.txt`) — verbatim, dated, attributable to a named respondent. The primary source underlying N_interview and the sole source for Table A/B crosswalk anchors, since those require the respondent's *own phrasing* (hedging language, frequency markers, timing statements), not a paraphrase.
2. **[FIELD MEMO: caseid, date]** — a written, dated field note (`memos.csv`, authored by the field researcher, Claudia). Close to interview transcript in auditability — it is a specific, attributable, dated document, not recall — but it is a *summary*, not a verbatim quote, so it does not carry a respondent's own frequency/timing language. Field memos are the right evidence for **structural and demographic facts**: household composition, migration/dual-residence pattern, hardware inventory and ownership history, occupation. They should **corroborate or independently establish structural claims**, not substitute for a transcript anchor in Table A/B.
3. **[FIELD OBS: conversational]** — an undocumented exchange recalled by a researcher, with no dated written record. The weakest tier. Never used as the sole basis for a parameter; flag explicitly wherever it appears, and prefer corroboration from tier 1 or 2 before treating it as evidence at all.

**Practical rule:** a `— source:` trailer citing a field memo takes the form `[FIELD MEMO: caseid NN, DD/MM/YYYY]`; a trailer citing undocumented recall takes the form `[FIELD OBS: conversational]`. Do not fold the two into one tag — the split exists precisely so a reader can see which claims rest on a citable document and which rest on memory.

**Coverage check (this dataset).** Cross-referencing `memos.csv` (household `name` field = `user_<id>`) against `all_transcripts.txt` (`user_ID`) shows that in every profile, **every household with a field memo also has an interview transcript** — there is no household in this dataset whose only qualitative evidence is a memo. (The single near-exception is id 67, Dionisio Vargas Castro, Profile 3: interviewed, no memo on file — the reverse direction, not a memo-only case.) This means field memos do not, in this dataset, expand N_interview beyond what transcripts already establish; a hypothetical **N_memo** population (memo but no transcript) is currently empty and the population table below does not need a third column for it.

**Extreme/Structural is not a survey-derived exception.** The diagnostic signal is a **dual-household strategy** — a household genuinely alternating between two residences with two different energy setups (the clearest case being Guillermo Romero: off-grid panel at one residence, paying ELFEC at a second) — and that can only be identified from what a respondent describes in an interview, not from a survey checkbox. So Extreme/Structural assignment requires N_interview evidence, the same as every other rigidity-derived parameter, with **no exception**.

**Concrete example:** if household #50 in Profile 2 was never interviewed, you cannot know whether it practices dual-residence — there is no survey field that reliably tells you this. Its Extreme/Structural status, like its Windows and Rigidity, must be inherited from the profile's interviewed pattern (the generalization described below) rather than individually assigned.

**The honest consequence:** Windows and Rigidity — the qualitative heart of the model — describe a pattern inferred from N_interview, then applied as parametrization for the *entire* N_survey population at simulation time. This is standard qualitative practice (representative-case inference), but it must be stated explicitly rather than left implicit, so a reviewer sees how many actual voices stand behind each profile's model rather than assuming every simulated household was individually evidenced.

Each truth file requieres a header block formt shown bellow:

```
Population: N_survey = [X] (classified via family_type/occupation/migration/portability_shs)
            N_interview = [Y] (subset with transcript; source of all qualitative parameters,
            including Windows, Rigidity/variability bin — including Extreme/Structural —
            and occasional_use)
Generalization: all qualitative parameters below (Windows, Rigidity, occasional_use,
Extreme/Structural bin assignment, and the household-level prob_home) are inferred from
N_interview and applied uniformly to all N_survey households in this profile at simulation
time. There is no survey-only shortcut for any of these — dual-household/structural-absence
status requires interview evidence, the same as ordinary timing and frequency parameters.
```

Note what "applied uniformly" means for `prob_home` specifically: it is one probability per profile, so every one of the N_survey households carries the same *chance* of being absent, and each then draws independently day by day. A category of 30 households at `prob_home = 0.7` therefore has roughly nine absent households on a given day — not a 30% chance of all thirty emptying at once. The parameter generalizes a rate, not a schedule, which is the correct treatment given that the interviews establish how much absence occurs in the profile but not which of the un-interviewed households it belongs to.

Where a household's transcript is corroborated by a written field memo, cite both: `— source: [respondent, date; FIELD MEMO caseid NN]`.

## Data-completeness tiers (what to do when a source is missing or vague, per practice)

Not every interview mentions explicit time boundaries for every practice, and not every respondent gives comparable detail. This determines *which row* of the interview×survey crossing table is usable for a given practice:

| Data situation | What to do | Confidence / `random_var_w` |
|---|---|---|
| Both interview and survey give explicit clock times | Apply the 3-tier crossing rule as defined in §3 | As specified there |
| Only one source gives explicit times | Use that source's bounds directly | Moderate–high — one notch less confident than an agreeing pair, since there's nothing to corroborate against |
| Neither source gives clock times, only time-of-day language ("por la mañana") | Anchor to the Window's own pre-defined outer bounds (already grounded in physical anchors) rather than inventing precision from vague language | High (widest bin) |
| No timing information at all for this respondent, this practice | Do not derive an individual window from nothing. Pool across other N_interview respondents in the same profile who did report timing for that practice; use the pooled range | High, and explicitly flagged **pooled evidence** — a different epistemic status (profile-level generalization) than the other three (household-level triangulation) |

The pooled-evidence flag matters because it's a second, independent axis of "how much do we actually know" — distinct from the N_survey/N_interview generalization above. A VA can rest on solid individual evidence from a well-covered profile, or on pooled evidence from a thinly-covered one; both should be visible in the file.

**A related, more fundamental limitation: single-period survey questions structurally capture typical behavior, not occasional behavior.** A categorical period-code question (e.g., "when do you use light_1 at night?") can only record one representative window per respondent — it has no way to express "usually X, but sometimes Y under specific circumstances." This is not a data-quality problem or a respondent error; it is a structural limit of the question format itself. When a respondent's interview account describes something that appears to exceed or diverge from their own survey answer (e.g., an occasional, trigger-driven practice layered on top of an ordinary routine), the two sources are often not actually in conflict — they are answering different questions the survey was never built to distinguish. This is precisely the kind of layer interview material is positioned to add, and it should be read as *enrichment revealing an additional layer*, not as a Say-Do contradiction requiring the tier-4 "survey wins" tiebreak (§3). The tier-4 rule still applies to genuine disagreements about a practice's *typical* pattern; it should not be invoked reflexively whenever an interview describes something a survey's single-code answer could never have captured in the first place.

**Practical consequence:** a practice that is normally dormant and activates only around an identifiable trigger (a recent fear-inducing incident, a specific social event, an environmental condition) should not be forced into a flat `occasional_use` value that pretends the trigger doesn't exist. But — see the retirement note below — this does **not** mean building a separate conditional-trigger mechanism. Unless the trigger is itself a systematically measured study variable, the honest treatment is **Chaos**: the practice's variability is real and may even have a nameable real-world cause, but the study has no quantified basis for modeling that cause, so it is treated as unpredictable from the data's perspective.






**S2.4 Truth files**
*Insert the four final truth files here* 


---

## Section S3: Household Classification Corrections and Overrides

*This section corresponds to the items placed in "Supplementary Material S2" within the main manuscript.*

**S3.1 Classification Correction Log**
*Insert your log of source-code corrections here.* 
Detail the instances where a coded field was corrected at the source, providing the documented justification, the evidentiary basis, and the exact effect on final population counts.

**S3.2 Analyst Overrides of Survey-Derived Assignments**
*Insert your override log here.* 
Document the specific instances where survey-derived assignments were overridden based on corroborated qualitative evidence of a structural condition.

---

## Section S4: Survey Instruments and Interview Guides 

*Extensive survey instruments and interview guides.*

**S4.1 Structured Household Survey Instruments**
*Insert the baseline (Feb 2023) and follow-up (Nov 2023-Dec 2025) survey questionnaires here.* 

**S4.2 Semi-Structured Interview and Focus Group Guides**
*Insert your qualitative interview guides here.*