# Supplementary Material

Qualitative analysis and supporting notes for the qualitative phase, including the coding protocol, logic memos, profile definitions, and appliance templates used in the paper.

## Qualitative Analysis

### Thematic Coding Protocol

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

### Logic Analysis in QualCoder

**Step 1: Identify the "Anchor" Practices (The "What")**

First, identify the core energy events that define the load profile.
  - Action in QualCoder: Run a Code Frequencies report strictly on your 1_practices category.
  - What to look for: Identify the practices with the highest counts. Based on your codebook, these will likely be PR_use_lights_time_evening_routine (count: 56), PR_act_school_homework (count: 21), and PR_use_ict_day_charging (count: 17). These high-frequency practices are your temporal anchors.

**Step 2: Run Co-occurrence Queries (The "Who" and the "Why")**

An energy practice doesn't exist in a vacuum; it is driven by specific people and cultural rules.
   - Action in QualCoder: Use the Code Co-occurrence / Matrix Tool to overlap your anchor practices with your Demographics, Norms, and Material constraints.
   - Key queries to run:
        - Query A: Overlap PR_use_lights_time_evening_routine with DEMO codes to see exactly who is driving the evening peak.
  
**Step 3: Write "Logic Memos" (Formulating the Rule)**

Once you see which codes frequently overlap, you must translate these intersections into narrative rules.
   - Action in QualCoder: Open a new Memo for each major theme and use a standard formula to write the behavioral logic.
   - The Formula: [Norm/Demographic] drives [Practice] under [Material Constraint].
   - Example Output: "The deep cultural value placed on intergenerational advancement (NOR_education) dictates that the evening lighting window (PR_act_school_homework) is non-negotiable, even when the battery is physically depleted due to bad weather (MAT_environmental_vulnerability)".
  
**Step 4: Map the Logic to RAMP Indicators**

The final step is to look at your logic memos and ask: Which part of the electrical simulation does this rule alter?
   - Action: Assign each behavioral logic to one of the four expected load curve indicator groups from your framework.
    - Does it dictate when a load happens? -> Temporal (e.g., Coincidence factor).

	- Does it dictate how big the load is? -> Magnitude (e.g., Peak Load).
	- Does it dictate if a load disappears? -> Reliability/Shape (e.g., Mean Outage Duration).
		
The report below explores co-occurrences among the codes, considering categories: Practices, Norms, Material and Socioeconomics. In this file, I draft interesting memos I got from these occurrences.

### **Theme 1: The Daily Baselines (Predictable Anchors)**

*These rules define the rigid, highly probable load curve shapes that
occur almost every single day, unaffected by minor weather changes.*

**Rule 1: The Educational Anchor**

-   **Formula:** \[NOR\_education / DEMO\_youth\_male & DEMO\_youth\_female\] drives \[PR\_act\_school\_homework / PR\_use\_lights\_time\_evening\_routine\] under \[MAT\_appliance\_priority / limited battery capacity\].

-   **The Narrative:** The cultural priority of intergenerational academic progress dictates that the evening lighting window is non-negotiable. Parents will actively restrict daytime appliance use or unplug radios to ensure enough battery remains for children to study safely under LED lights until 22:00.

-   **RAMP Modeling Implication (Temporal & Reliability):** Protects the "Critical Discharge Window. In the simulation, the evening lighting load (18:00--22:00) is highly inelastic (Probability of Use = \~1.0) and receives the highest priority in the load-shedding hierarchy.

**Rule 2: The Agricultural Dictate**

-   **Formula:** \[NOR\_labor\_activity\_constraint / DEMO\_male\_adult & DEMO\_female\_adult\] drives \[PR\_cooking\_routine\_daily /
PR\_use\_lights\_time\_morning\_routine\] under \[SOC\_livelihood\_agriculture / rigorous agricultural schedules\].

-   **The Narrative:** The necessity of "sun-up to sun-down" agricultural labor forces households to wake well before dawn. Energy behavior is constrained by this survival routine, necessitating an early period of lighting for meal preparation before the family abandons the house.

-   **RAMP Modeling Implication (Temporal & Shape):** Establishes a short, sharp early morning demand spike (e.g., 04:00 to 06:00) followed immediately by a massive \"demand valley\" where household load drops to absolute zero during daylight hours.

**Rule 3: The Gendered Anchor of Domestic Operations**

-   **Formula:** \[NOR\_gendered\_energy\_roles / DEMO\_female\_adult\] drives \[PR\_act\_meals\] under \[MAT\_appliance\_priority / fixed LED lighting\].

-   **The Narrative:** Social norms dictate that adult women are primarily responsible for the kitchen and evening meal preparation. This routine acts as the temporal anchor for the household, defining the start of the evening active period.

-   **RAMP Modeling Implication (Magnitude & Temporal):** The presence of DEMO\_female\_adult guarantees the most consistent evening lighting demand window, directly dictating the daily depth of discharge (DoD) of the battery.

**Rule 4: The Connectivity Lifeline**

-   **Formula:** \[NOR\_value\_of\_connectivity / DEMO\_female\_senior & DEMO\_male\_senior\] drives \[PR\_act\_information\_communication /PR\_use\_ict\_day\_charging\] under \[SOC\_migration\_permanent\_outflux / permanent migration of children\].

-   **The Narrative:** For elderly populations left behind by rural-urban migration, the cell phone is an emotional lifeline, not a luxury. Maintaining a charged phone to communicate with children in the Chapare or cities is prioritized over personal lighting.

-   **RAMP Modeling Implication (Reliability):** Device charging is categorized as a \"critical load.\" Even at low battery levels, the simulation should execute this draw, bypassing standard energy-saving logic.

### **Theme 2: System Constraints & Coping Mechanisms**

*These rules define how users dynamically interact with the physical limits of the environment and the battery.*

**Rule 5: Weather-Driven Load Shedding**

-   **Formula:** \[NOR\_system\_capacity\_resignation / DEMO\_female\_adult & DEMO\_male\_adult\] drives \[PR\_energy\_management / PR\_use\_ict\_day\_charging\] under \[MAT\_environmental\_vulnerability / cloudy or rainy weather\].

-   **The Narrative:** Users exhibit high technical literacy regarding their system\'s limits. When weather conditions prevent full charging, users proactively \"load shed\" by rationing light and aggressively shifting their mobile charging strictly to peak daylight hours to protect the battery's state of charge.

-   **RAMP Modeling Implication (Temporal):** Shifts the charging load profile to perfectly coincide with the solar generation curve (e.g., 10:00 to 16:00), effectively \"clipping\" demand off the battery.

**Rule 6: The Safety Baseline**

-   **Formula:** \[NOR\_safety / DEMO\_female\_adult & DEMO\_female\_senior\] drives \[PR\_lights\_extreme\_night\_usage\] under \[IMP\_health\_and\_safety / presence of venomous insects and physical hazards\].

-   **The Narrative:** The culturally reinforced fear of venomous fauna (scorpions, vinchucas) and tripping hazards overrides general conservation habits, prompting users (especially mothers and the elderly) to leave at least one light illuminated until dawn.

-   **RAMP Modeling Implication (Shape & Magnitude):** Radically alters the load curve. Instead of dropping to zero after 22:00, the simulation must apply a continuous 12-hour base load (1--5W), drastically impacting the starting State of Charge (SoC) for the following day.

**Rule 7: Infrastructure Mobility**

-   **Formula:** \[NOR\_ownership\_duty / DEMO\_male\_adult\] drives \[PR\_system\_mobility\] under \[SOC\_migration\_temporary\_labor / seasonal agricultural work in the \"monte\"\].

-   **The Narrative:** Due to extreme geographical isolation and the necessity of seasonal agricultural migration, the SHS is treated as a portable survival tool rather than fixed household infrastructure. Men actively dismantle and transport the system to temporary camps.

-   **RAMP Modeling Implication (Reliability & Shape):** Introduces "seasonal absences". The algorithm must probabilistically drop the baseline load to zero for periods ranging from weeks to months at the primary geographic coordinate.

**Rule 8: Nature as a Threat (Environmental Fear)**

-   **Formula:** \[NOR\_environmental\_fear / DEMO\_female\_senior\] drives \[Avoidance of PR\_sys\_maintenance\] under \[MAT\_environmental\_vulnerability / thunderstorms and lightning\].

-   **The Narrative:** Culturally reinforced fears that solar panels attract deadly lightning strikes lead users to physically disconnect the system or actively avoid touching/cleaning it during the rainy season.

-   **RAMP Modeling Implication (Generation/Yield Model):** Introduces a severe seasonal variable. Increases the probability of complete physical disconnection during stormy months and increases \"soiling losses\" (dust accumulation) due to reliance strictly on passive rain-washing.

**Rule 9: The Aspiration Gap and Dual-Home Displacement**

-   **Formula:** \[NOR\_app\_aspiration / DEMO\_male\_adult\] drives \[PR\_dual\_home\_strategy\] under \[MAT\_geographical\_infrastructure\_gap / lack of grid connectivity at the SHS location\].

-   **The Narrative:** The desire for modern comfort (TVs, blenders) cannot be met by the SHS. Rather than abandoning the desire, families maintain a bivocational lifestyle, delegating heavy energy tasks to a secondary, grid-connected home while zoning the SHS home strictly for basic survival.

-   **RAMP Modeling Implication (Magnitude / Latent Demand):** Explains why the current load curve is artificially flat. It provides the mathematical parameters for a \"grid-arrival\" or \"capacity doubling\" simulation, triggering immediate high-wattage spikes (50W--100W) that are currently suppressed.

### **Theme 3: The System Breakers (Anomalies & Stochastic Events)**

*These rules explain the chaotic, unpredictable data points in the
datalogger that traditional engineering models fail to simulate.*

**Rule 10: Energy Bricolage (Hacking)**

-   **Formula:** \[NOR\_energy\_experience\_legacy / DEMO\_male\_adult\] drives \[PR\_independent\_acquisition\] under \[MAT\_parallel\_infrastructure\].

-   **The Narrative:** Users with previous technical exposure to legacy systems refuse to be constrained by the project SHS. They actively hack together independent infrastructure, wiring old panels to motorcycle batteries to run parallel charging stations.

-   **RAMP Modeling Implication (Magnitude Validation):** Acts as a critical data correction rule. It alerts the simulation that the measured SHS datalogger load is a false baseline, representing only a fraction of the actual total domestic demand.

**Rule 11: Protective Gatekeeping**

-   **Formula:** \[NOR\_ownership\_duty & NOR\_fear\_of\_tech\_failure\] drives \[NOR\_energy\_gatekeeping\] under \[MAT\_hardware\_degradation (fear of)\].

-   **The Narrative:** The intense fear of breaking a fragile, irreplaceable financial asset overrides indigenous communal sharing norms. Users actively refuse to let neighbors charge devices to protect their USB ports from damage.

-   **RAMP Modeling Implication (Reliability):** Prevents peer-to-peer load dumping. In the simulation, if Household A\'s system fails, the algorithm cannot assume Household A\'s demand safely shifts to Household B\'s profile.

**Rule 12: Community Override (Stochastic Spikes)**

-   **Formula:** \[NOR\_energy\_sharing\] drives \[PR\_act\_socializing\] under \[IMP\_extended\_waking\_hours / Community Events\].

-   **The Narrative:** Normal routines of strict energy conservation are temporarily suspended during major community events (e.g., *velorios* or visiting relatives). Energy becomes a tool for communal hospitality.

-   **RAMP Modeling Implication (Variability):** Explains massive, unpredictable standard deviations. Provides the behavioral logic to program low-probability, high-impact \"stochastic spikes\" where lighting is drawn continuously for 48 hours, fully depleting the system.

**Rule 13: Hardware Resignation (The Silent Drop)**

-   **Formula:** \[NOR\_fear\_of\_tech\_failure\] drives \[Permanent load reduction\] under \[MAT\_hardware\_degradation\].

-   **The Narrative:** Due to a lack of technical literacy and missing supply chains, minor hardware failures (e.g., a snapped jack or loose USB port) result in the permanent abandonment of the appliance rather than a repair.

-   **RAMP Modeling Implication (Shape & Reliability):** Introduces a \"hardware decay rate\" to the model. Load curves must simulate permanent, step-wise drops to zero for specific appliances (like the continuous 3W radio load disappearing mid-year).

**Rule 14: Companionship in Isolation**

-   **Formula:** \[NOR\_aging\_energy\_culture / DEMO\_male\_senior\] drives \[PR\_use\_lights\_time\_evening\_routine / PR\_act\_leisure\_company\] under \[MAT\_geographical\_infrastructure\_gap / living alone in isolated rural areas\].

-   **The Narrative:** For elderly adults living entirely alone due to migration, the continuous use of the radio or lighting serves primarily as psychological comfort and companionship rather than utilitarian necessity.

-   **RAMP Modeling Implication (Magnitude & Shape):** Flattens the probabilistic "use windows" associated with active tasks, converting the radio into a continuous, flat load profile (drawing power constantly from 06:00 to 18:00).

### **Theme 4: Productive Labor & Multi-Energy Realities**

**Rule 15: The Productive Lighting Veto (The Weaving Constraint)**

-   **Formula:** \[NOR\_labor\_activity\_constraint / DEMO\_female\_adult\] restricts \[PR\_act\_productive / PR\_act\_knitting\] under \[MAT\_appliance\_priority (low lumens) & IMP\_health\_and\_safety (insects/polillas)\].

-   **The Narrative:** Despite having evening illumination, adult women actively *refuse* to use the SHS light for income-generating textile work (weaving/spinning). They cite two physical constraints: the LED light is not \"nítida\" (clear/bright) enough for detailed work, and the light attracts moths (*polillas*) which ruin the valuable wool. Thus, productive textile labor remains strictly anchored to daylight hours. *(Found in transcripts: Users 72, 81, 85).*

-   **RAMP Modeling Implication (Shape/Magnitude Constraint):** Prevents the algorithm from artificially extending the evening lighting load window for productive tasks. It proves that simply providing a basic 2W bulb does *not* automatically trigger nighttime economic productivity in the simulation.

**Rule 16: The Thermal Weather Switch (Fuel Stacking)**

-   **Formula:** \[MAT\_geographical\_infrastructure\_gap / lack of roads\] drives \[PR\_fuel\_stacking\_cooking\] under \[MAT\_environmental\_vulnerability / Rain\].

-   **The Narrative:** While this does not draw electricity, it is vital for multi-energy modeling. Users default to gathered firewood for cooking because the lack of roads makes carrying heavy LPG gas cylinders on foot grueling. However, when it rains and firewood gets wet, users immediately switch to their hoarded LPG gas.

-   **RAMP Modeling Implication (Multi-Energy Profiling):** If you are running RAMP as a multi-energy simulator (thermal + electrical), this rule dictates the thermal load switch. It proves that *weather* is the master variable in Raqaypampa, dictating not just solar generation, but also the choice of cooking fuel.

**Rule 17: The Gratitude/Scarcity Baseline** (11--17 overlaps)

-   **Formula:** \[NOR\_energy\_experience\_legacy\] defines \[PR\_substitution / MAT\_legacy\_candle / MAT\_legacy\_mechero\].

-   **RAMP Implication:** The memory of toxic smoke and buying candles creates a highly conservative behavioral baseline. This justifies assigning a lower-than-average relative mean power factor, as users treat the LED light as a precious commodity, not an infinite utility.

**Rule 18 The Sedentary Anchor / Aging in Place**

-   **Formula:** \[MAT\_physical\_constraint / DEMO\_male\_senior & DEMO\_female\_senior\] restricts \[PR\_system\_mobility\] under \[SOC\_migration\_temporary\_labor\].

-   **The Narrative:** Due to the physical limitations of aging, elderly households do not participate in the temporary, labor-intensive migration to the *monte*. They remain anchored to the primary residence year-round, serving as caretakers of the permanent household infrastructure.

-   **RAMP Modeling Implication:** Protects \"Profile 2: Isolated Elderly\" from seasonal load-shedding. The simulation must maintain a continuous 365-day baseline for this demographic, completely blocking the stochastic \"Absence/Vacation\" modifier that is applied to younger, agriculturally active profiles.
    
## Correlation Analysis from Quantitative Surveys

### The Phone Charging Multiplier

-   **The Math:** family\_type strongly drives phone\_2\_time (\$\\eta => 0.76\$) and phone\_1\_time (\$\\eta = 0.72\$).

-   **The Behavioral Insight:** This goes far beyond just "more people equal more phones". It shows that the *structure* of the family dictates charging behavior. An \"extended\" family (which might include grandparents, parents, and older teens) creates a chaotic charging environment where Phone 1 and Phone 2 are competing for the system\'s USB ports for extended hours. A \"nuclear\" or \"single elder\" family has a drastically different, much lower charging footprint.

-   **RAMP Implication:** This is your trigger for modeling high-stress daytime loads.

### The Agricultural Labor Pool

-   **The Math:** family\_type correlates heavily with act\_dl\_agri (daily hours in agriculture) (\$\\eta = 0.67\$) and act\_agriculture (\$\\eta = 0.67\$).

-   **The Behavioral Insight:** The type of family determines their labor capacity. Extended and large nuclear families can divide labor, sending people to the *monte* (fields) for long hours. Conversely, isolated elderly households cannot sustain these long agricultural hours.

-   **RAMP Implication:** This justifies why the \"Seasonal Migrant\" or \"Agricultural Core\" archetype needs the massive mid-day \"demand valley\" (because the whole family is out working), while the elderly archetype might have a flatter demand curve throughout the day.

### The Kitchen Dictate (Cooking Time)

-   **The Math:** family\_type strongly shapes cooking\_time\_min\_d (minutes spent cooking per day) (\$\\eta = 0.56\$).

-   **The Behavioral Insight:** This is the missing piece for **Rule 3 (The Gendered Anchor of Domestic Operations)**! Because you correctly pointed out that light bulb correlations don\'t prove simultaneous use, *this* is the variable that proves cooking time scales with family structure. Extended families require much more time to prepare food (like the *lawa* or *mote* we saw in the transcripts).

-   **RAMP Implication:** For your "Extended Family" or "Educational Core" archetype, the evening lighting window tied to cooking must be wider and highly rigid, whereas an elderly individual living alone requires less cooking time, leading to a shorter baseline lighting window.

### Proof of \"The Empty Nest\" (Demographic Isolation)

-   **The Math:** adults\_mas\_60 has a strong **negative correlation** with both working-age adults adults\_18\_59 (\$r = -0.441, p \< 0.001\$) and young children children\_0\_5 (\$r = -0.270, p = 0.030\$).

-   **The Behavioral Insight:** This is the hard mathematical footprint of rural out-migration. If a household has elderly individuals, it is highly likely that there are no working-age adults or young children living there. They are physically isolated.

-   **RAMP Implication:** This perfectly justifies separating them from the "Educational/Agricultural Core" archetype. Their load curves will not be driven by heavy domestic cooking (Rule 3) or multiple cell phones (Rule 9).

### The Altered Morning Routine

-   **The Math:** adults\_mas\_60 strongly influences the specific categorization of morning lighting: light\_2\_morning (\$\\eta = 0.517\$) and light\_1\_morning (\$\\eta = 0.458\$).

-   **The Behavioral Insight:** Earlier, we saw that older family heads wake up significantly *later* than younger agricultural workers. This correlation ratio (\$\\eta\$) indicates that the presence of elderly people fundamentally restructures *how* morning lighting is used. Because they aren\'t rushing out to the *monte* for 10 hours of heavy labor before dawn, their morning lighting and radio routine is likely slower and more continuous.

-   **RAMP Implication:** You will shift their morning lighting window. Instead of a sharp, intense spike at 04:00 AM (the \"Agricultural Dictate\"), the elderly archetype will have a smoother, potentially later, and less intense morning demand curve.

### The \"School Morning\" Spike (Validating Temporal Anchors)

-   **The Math:** The presence of school-aged children (children\_5\_17) heavily influences the use of the first morning light (light\_1\_morning, \$\\eta = 0.540\$) and morning radio (radio\_morning, \$\\eta = 0.491\$). Furthermore, as we saw earlier, it creates a statistically significant *negative* correlation with wakeup\_time\_after (\$r = -0.323, p = 0.019\$).

-   **The Behavioral Insight:** Households with school children have a highly rigid, earlier morning routine. The radio is turned on early (likely for news or timekeeping before school), and the first light is used earlier than in homes without school children.

-   **RAMP Implication:** In your simulation, this justifies assigning a sharp, early morning probability window (e.g., 04:30--06:00 AM) for lights and radio specifically for the Educational archetype.

### The Digital Aspiration Gap

-   **The Math:** The presence of school-aged children (children\_5\_17) positively correlates with the total number of cell phones (phones, \$r = 0.269, p = 0.031\$). Additionally, whether children are in school (children\_in\_school) strongly influences the household\'s overall satisfaction with their solar system (demand\_satisfaction, Cramér's V = 0.339).

-   **The Behavioral Insight:** School children are the primary drivers of digital connectivity and latent demand. As kids go to school, they require phones for homework or social connectivity. Because they have more phones to charge, these households are the most likely to hit the limits of the 89Wh battery, altering their overall satisfaction with the system.

-   **RAMP Implication:** The \"Educational Core\" archetype must be programmed with a much higher probability for simultaneous phone charging (especially daytime charging) than the \"Isolated Elderly\" archetype.

### What School Children *Actually* Change (The Significant Math)

While children don\'t change the evening lighting duration, the
correlation script found that children\_5\_17 **does** significantly
alter two other critical energy variables (\$p \< 0.05\$):

-   **Wake-Up Times (wakeup\_time\_after): Pearson \$r = -0.32\$ (\$p = 0.019\$).**

    There is a significant negative correlation between school children
    and wake-up times. This means **households with school-aged children
    wake up significantly earlier** than households without them.

-   **Phone Ownership (phones): Pearson \$r = 0.26\$ (\$p = 0.031\$).**

    Households with school-aged children have a significantly higher
    concentration of cell phones. In the interviews, parents mentioned
    children needing phones for schoolwork or communication.

**The Elderly Influence:** The age of the family head (fam\_head\_age,
\$\\eta = 0.566\$) and the presence of older adults (adults\_mas\_60,
\$\\eta = 0.453\$) strongly shape evening light use. This validates
**Rule 14 (Companionship in Isolation)** and **Rule 6 (The Safety
Baseline)**. Older adults are driving specific evening lighting
profiles, likely leaving it on longer for safety or comfort.
    
## Profiles Definition

The population is systematically clustered into distinct Energy Behavior Profiles (EBPs). This is achieved by cross-referencing the demographic "Splitter Variables" (Stream B) with the qualitative socio rules (Stream A), generating specific behavioral archetypes defined by their distinct daily routines and cultural constraints.


#### **Profile 1: The Educational / Agricultural Core (The Standard)**

-   **The Demographic:** Nuclear families with working-age adults and school-aged children.

-   **The Driving Rules:** Rule 1 (Educational Anchor), Rule 2 (Agricultural Dictate), Rule 3 (Kitchen Dictate), Rule 9 (Aspiration Gap).

-   **Energy Signature:**

    -   Sharp, early morning lighting spike (04:30 AM) because they must wake up for the fields/school.

    -   Absolute \"demand valley\" during the day (the house is empty).

    -   Heavy evening peak (18:00--22:00) driven by simultaneous cooking and homework.

    -   High daytime/evening phone charging load (multiple phones).

#### **Profile 2: The Isolated Elderly (The Companionship Baseline)**

-   **The Demographic:** Single elders or older couples living alone without working-age adults or young children.

-   **The Driving Rules:** Rule 6 (Safety Baseline), Rule 14 (Companionship in Isolation).

-   **Energy Signature:**

    -   Smoother, later morning wake-up (no agricultural rush).

    -   Continuous, flat radio load running for hours during the day.

    -   Lower evening peak, but a continuous 1W--3W lighting draw that stays on all night for safety/comfort.

    -   Minimal phone charging (only 1 phone for the \"Connectivity Lifeline\").

#### **Profile 3: The Extended / Multi-Tasking Hub (High Stress)**

-   **The Demographic:** Extended families living together (grandparents, parents, children) under one roof.

-   **The Driving Rules:** Rule 3 (Kitchen Dictate - extended cooking times), Rule 12 (Community Override).

-   **Energy Signature:**

    -   The most brutal load curve.

    -   Longest evening lighting duration (to cook large meals like *mote* or *lawa*).

    -   Extreme USB port competition during the day (charging 3+ cell phones simultaneously).

    -   Highest probability of fully depleting the battery by 20:00.

#### **Profile 4: The System Breakers (The Stochastic Nodes)**

-   **The Demographic:** Users who actively subvert the intended use of the SHS.

-   **The Driving Rules:** Rule 7 (Infrastructure Mobility), Rule 10 (Energy Bricolage / Hacking), Rule 13 (Hardware Resignation).

-   **Energy Signature:**

    -   **The Nomads:** Load curve drops to absolute zero for weeks at a time when they take the panel to the *monte*.
        
### **Comprehensive Analysis of Energy Behavior Profiles (EBP)**

This analysis triangulates high-resolution datalogger telemetry with socio-economic surveys and qualitative interviews (all\_transcripts.txt). It utilizes the conceptual framework of \"Social Rules\" (coocurrence\_memos.docx) to explain *why* the mathematical
thresholds (MRSD, Peak Hour, Appliance Stacking, Blackout Frequency) behave the way they do in the physical world.

#### Profile 1: The Educational / Agricultural Core (The Standard)

**The Demographic:** Nuclear and numerous families with working-age adults and school-aged children. These households represent the intended target demographic for standard Solar Home System (SHS) deployment. 
**Identified Users:** 72 (OLD/TPDIN) and 74 (TPDIN).

**Socioeconomic Triangulation:** Interviews confirmed these are large,
active households. User 74, for example, underreported their household
size in the survey (claiming 5 members), while the interview confirmed 7
permanent residents with 3 children in school. User 72 represents a
moderate extended family where older children migrate to the city but
return frequently, anchoring the household's economy to the rural
homestead.

**The Driving Social Rules:**

-   **Rule 1 (The Educational Anchor):** The cultural priority of academic progress dictates that the evening lighting window is non-negotiable for homework.

-   **Rule 2 (The Agricultural Dictate):** The \"sun-up to sun-down\" labor requirement forces an early morning wake-up and creates a massive daytime \"demand valley\" where the house is empty.

-   **Rule 3 (The Gendered Anchor of Domestic Operations):** Adult women primarily control the kitchen, ensuring a strict lighting requirement during evening meal preparation.

-   **Rule 15 (The Productive Lighting Veto):** Adult women refuse to use SHS lights for weaving at night because the light attracts moths (polillas) that ruin wool, restricting productive labor to daylight hours.

**Energy Signature & Metric Thresholds:**

-   **Peak Hour (18:00--19:00):** A rigid evening peak driven by the agricultural dictate (Rule 2). The load surges simultaneously when they return to cook and study.

-   **MRSD Chaos Index (1.20 - 1.30):** Moderate, predictable variability. User 72 and 74 show MRSDs of 1.262 and 1.252, respectively. The routine is highly structured around the agricultural calendar.

-   **Overall Mean Power (\> 1.25W):** High baseline energy footprints (User 72: 1.59W; User 74: 1.28W) indicative of sustained, multi-person consumption.

-   **Appliance Stacking Index (Moderate: 15% - 19%):** Because these are large families, users must strategically stagger their appliance use (e.g., charging phones before evening cooking), keeping simultaneous extreme loads manageable.

-   **Reliability & Blackouts:** Despite efficient battery use, the sheer volume of their evening demand creates high system stress. User 72 experienced the highest recorded blackout frequency (37 events, 60% of which were behaviorally induced). Standard 89 Wh batteries are frequently undersized for the intense evening surges of numerous families.

#### Profile 2: The Isolated Elderly / Unipersonal Households (The Companionship Baseline)

**The Demographic:** Single elders, older couples, or single adults living alone. They lack working-age adults or school-aged children.
**Identified Users:** 11 (TPDIN) and 84 (OLD).

**Socioeconomic Triangulation:** This profile highlights the most severe "Say-Do" gaps in the dataset. User 11 claimed a family of 5 with a student to secure the panel. However, his interview confirmed he lives entirely alone (*"Yo vivo solo"*). User 84 honestly reported a 2-person household, living solely to care for his elderly mother after his 8 siblings migrated to Santa Cruz.

**The Driving Social Rules:**

-   **Rule 6 (The Safety Baseline):** The culturally reinforced fear of venomous fauna (scorpions, vinchucas) prompts users to leave a light illuminated continuously.

-   **Rule 14 (Companionship in Isolation):** For elderly adults living alone, continuous radio or lighting serves as psychological comfort.

-   **Rule 4 (The Connectivity Lifeline):** Maintaining a charged phone to communicate with migrated children is prioritized over personal lighting.

-   **Rule 18 (The Sedentary Anchor):** Aging limits mobility; they do not participate in temporary migration to the "monte", resulting in a continuous 365-day baseline.

**Energy Signature & Metric Thresholds:**

-   **Peak Hour (20:00 or Variable):** A later, less intense peak compared to the agricultural core. The morning wake-up is smoother, lacking the urgency of school preparation.

-   **Night Safety Probability (\> 75%):** The defining metric of this profile. User 11 exhibits an ultra-stable footprint with a continuous overnight safety light (75.8% probability). Energy is utilized primarily as a security anchor (Rule 6).

-   **MRSD Chaos Index (1.20 - 1.80):** Generally chaotic to moderately stable (User 11: 1.269; User 84: 1.717), reflecting isolated lives punctuated by occasional visits from non-resident children.

-   **Overall Mean Power (\~1.00W or lower):** Moderate to low volumetric baselines (User 11: 1.09W) with low peak-to-mean ratios.

-   **Appliance Stacking Index (\< 1.0%):** A solitary individual cannot physically occupy multiple rooms or utilize multiple devices simultaneously. This sequential usage pattern prevents extreme peak loads.

-   **Reliability & Blackouts:** Moderate blackout frequency (e.g., 6.25 per 100 days for User 11). Blackouts occur more frequently than in Profile 1 because continuous night lighting (Rule 6) constantly drains the battery, leaving it vulnerable to cloudy days.

#### Profile 3: The Extended / Multi-Tasking Hub (High Stress)

**The Demographic:** Dense, multi-generational families (grandparents, parents, children) living under one roof, often functioning as a generational basecamp for returning relatives. 
**Identified Users:** 63(OLD) and 69 (OLD).

**Socioeconomic Triangulation:** These households possess high demographic mass. User 63 perfectly matched their survey, acting as a massive nuclear family with 3 children in school. User 69 revealed a hidden strategy: despite high seasonal migration, they purchased a second SHS system to handle their communal load.

**The Driving Social Rules:**

-   **Rule 3 (The Gendered Anchor / Kitchen Dictate):** Extended cooking times are required to prepare meals for large groups (e.g., *mote* or *lawa*).

-   **Rule 12 (Community Override):** Normal energy conservation routines are suspended during community events or when relatives visit, causing stochastic spikes.

**Energy Signature & Metric Thresholds:**

-   **Peak Hour (18:00 - 19:00):** The most brutal load curve in the dataset. The evening peak is sustained over longer durations.

-   **Night Safety Probability (High: 72% - 84.9%):** User 63 exhibits 84.9% safety light probability and User 69 exhibits 72.0%, indicating consistent overnight lighting for family safety.

-   **MRSD Chaos Index (Moderate: 0.887 - 1.298):** User 63 (0.887) and User 69 (1.298) show moderate predictability. The routine is structured around extended family activities.

-   **Relative Mean Power (Evening: \> 1.7x):** Extreme evening stress multipliers. For example, User 63\'s evening power draw is 1.758 times higher than their 24-hour baseline.

-   **Overall Mean Power (\> 1.20W):** High volumetric consumption (User 63: 1.93W; User 69: 1.22W) representing a heavy, continuous drain on the 89 Wh battery.

-   **Appliance Stacking Index (High: 27.1% - 35.3%):** User 63 exhibits 27.1% stacking and User 69 exhibits 35.3%, the highest recorded. Intense competition for USB ports and simultaneous multi-device usage defines this profile.

-   **Reliability & Blackouts:** Surprisingly high reliability (98-99%), suggesting these specific users have learned to tightly control their baselines despite the heavy loads, likely due to hardware resignation or the presence of secondary systems (as seen in User 69).

#### Profile 4: The System Breakers (The Stochastic Nodes)

**The Demographic:** Highly nomadic users, split-households, or
individuals who actively subvert the intended spatial constraints of the
SHS. **Identified Users:** 64 (OLD) and 96 (TPDIN). *(User 15 also
mathematically aligns here).*

**Socioeconomic Triangulation:** Surveys completely failed to capture
the spatial reality of these users. User 64 claimed to be a standard
7-person household, but the interview revealed she actively maintains
two separate households due to water scarcity, physically unbolting and
relocating the solar panel as she moves (*\"voy siempre a mi otra
casa\"*). User 96 claimed extreme poverty and permanent residency, but
the interview revealed an income 5x higher and a split-household dynamic
where his wife lives permanently in the peri-urban center of Raqay
Pampa.

**The Driving Social Rules:**

-   **Rule 7 (Infrastructure Mobility):** Extreme geographical isolation and seasonal agricultural work (\"monte\") force users to dismantle and transport the system.

-   **Rule 9 (The Aspiration Gap and Dual-Home Displacement):** Families maintain a bivocational lifestyle, delegating heavy energy tasks to a secondary, grid-connected home while treating the SHS home as a temporary base.

-   **Rule 13 (Hardware Resignation):** Minor failures (a snapped jack) lead to permanent appliance abandonment rather than repair.

**Energy Signature & Metric Thresholds:**

-   **Peak Hour (18:00 - 20:00):** User 64 peaks at 19:00 while User 96 peaks at 20:00. Both show highly erratic timing due to nomadic patterns.

-   **Night Safety Probability (Low: 23.5% - 33.5%):** User 64 exhibits 33.5% and User 96 exhibits 23.5%. Minimal overnight safety lighting reflects their nomadic lifestyles and lower safety baseline priorities.

-   **MRSD Chaos Index (\> 2.00):** The defining mathematical signature of temporal migration. Both User 64 (2.394) and User 96 (3.016) exhibit maximum chaos. The load curve drops to absolute zero for weeks when the house is abandoned, followed by massive usage spikes when the user returns.

-   **Relative Mean Power (Extreme Peaks):** When they are home, their energy use is violent. User 64's evening routine requires 2.838x more power than her baseline average.

-   **Overall Mean Power (\< 0.70W):** Because the house is frequently empty, the 24-hour average is deceivingly tiny (User 64: 0.68W; User 96: 0.43W).

-   **Appliance Stacking Index (Moderate: 20.2% - 21.1%):** User 64 exhibits 21.1% stacking and User 96 exhibits 20.2%. Despite low overall consumption, simultaneous device usage occurs when households are occupied.

-   **Reliability & Blackouts:** High behavioral blackout rates relative to their low mean power (User 64: 1.56; User 96: 1.34). Because their demand timing is completely unpredictable, the battery cannot effectively pre-charge, resulting in frequent, behaviorally-induced Low Voltage Disconnects (LVD).
    
    
## Virtual Appliance Definition

This part defines virtual appliance templates used to generate RAMP inputs for each Energy Behavior Profile (EBP). Below each human-facing parameter we show the exact RAMP key used in the code (in parentheses) so the template can be translated to RAMP JSON without ambiguity.

## Profile 1 — Educational / Agricultural Core

User 74 shows high predictability, strong evening peaks, and a moderate overnight safety baseline (~56.8%).

### 1. Indoor Task Light — Cooking & Homework (LED_2)
- **P:** 3 W  (RAMP key: `power`) — nominal; user observations: 3.87 W / 2.6 W for similar units
- **Occasional_use:** 1.0 (RAMP key: `occasional_use`)
- **func_time:** 150 min (RAMP key: `func_time`)
- **num_windows:** 1 (RAMP key: `num_windows`)
- **window_1:** [1020, 1380] (RAMP key: `window_1`) — 17:00–23:00
- **func_cycle:** 90 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.35 (RAMP key: `time_fraction_random_variability`)
- **random_var_w:** 0.20 (RAMP key: `random_var_w`)

### 2. Outdoor Night Transit Light
- **P:** 2 W (RAMP key: `power`) — nominal LED_1
- **Occasional_use:** 1.0 (RAMP key: `occasional_use`)
- **func_time:** 100 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [1080, 1380] (RAMP key: `window_1`) — 18:00–23:00
- **func_cycle:** 40 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.35
- **random_var_w:** 0.20

### 3. Indoor Safety Light
- **P:** 2 W (RAMP key: `power`)
- **Occasional_use:** 0.50 (RAMP key: `occasional_use`) — safety probability-derived
- **func_time:** 300 min (RAMP key: `func_time`) — continuous overnight
- **num_windows:** 2
- **window_1:** [1381, 1440] (RAMP key: `window_1`) — 23:01–24:00
- **window_2:** [0, 240] (RAMP key: `window_2`) — 00:00–04:00
- **func_cycle:** 200 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.35
- **random_var_w:** 0.20

### 4. Indoor Morning Light
- **P:** 3 W (RAMP key: `power`)
- **Occasional_use:** 0.40 (RAMP key: `occasional_use`)
- **func_time:** 50 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [300, 420] (RAMP key: `window_1`) — 05:00–07:00
- **func_cycle:** 30 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 5. Outdoor Morning Light
- **P:** 2 W (RAMP key: `power`)
- **Occasional_use:** 0.30 (RAMP key: `occasional_use`)
- **func_time:** 50 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [300, 420] (RAMP key: `window_1`) — 05:00–07:00
- **func_cycle:** 30 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 6. Cellphone & Radio Charging (USB)
- **P:** 2.00 W (RAMP key: `power`)
- **Occasional_use:** 1.0 (RAMP key: `occasional_use`)
- **func_time:** 470 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [0, 1440] (RAMP key: `window_1`) — anytime
- **func_cycle:** 70 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.35
- **random_var_w:** 0.00

---

## Profile 2 — The Isolated Elderly

User 11 demonstrates a strong companionship/radio load and a high safety-light probability (~75.8%).

### 1. Indoor Task Light (LED_2)
- **P:** 2.64 W (RAMP key: `power`)
- **Occasional_use:** 0.26 (RAMP key: `occasional_use`)
- **func_time:** 100 min (RAMP key: `func_time`)
- **num_windows:** 2
- **window_1:** [1140, 1440] (RAMP key: `window_1`) — 19:00–24:00
- **window_2:** [0, 60] (RAMP key: `window_2`) — 00:00–01:00
- **func_cycle:** 60 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.35
- **random_var_w:** 0.20

### 2. Indoor Safety Light / Morning (LED_1)
- **P:** 2.64 W (RAMP key: `power`)
- **Occasional_use:** 0.70 (RAMP key: `occasional_use`) — ≈75.8% safety
- **func_time:** 300 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [0, 300] (RAMP key: `window_1`) — 00:00–05:00
- **func_cycle:** 240 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.35
- **random_var_w:** 0.20

### 3. Outdoor Night Transit Light
- **P:** 2 W (RAMP key: `power`)
- **Occasional_use:** 0.10 (RAMP key: `occasional_use`)
- **func_time:** 50 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [1200, 1320] (RAMP key: `window_1`)
- **func_cycle:** 10 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.35
- **random_var_w:** 0.20

### 4. Cellphone & Radio Charging (USB)
- **P:** 3.00 W (RAMP key: `power`)
- **Occasional_use:** 1.0 (RAMP key: `occasional_use`)
- **func_time:** 550 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [0, 1440] (RAMP key: `window_1`) — always-available
- **func_cycle:** 85 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.40
- **random_var_w:** 0.00

---

## Profile 3 — Extended / Multi-Tasking Hub

High stacking, long USB durations, and elevated probabilities across loads.

### 1. Indoor Task / Communal Light (LED_2)
- **P:** 3 W (RAMP key: `power`)
- **Occasional_use:** 1.00 (RAMP key: `occasional_use`)
- **func_time:** 240 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [1020, 1440] (RAMP key: `window_1`) — 17:00–24:00
- **func_cycle:** 180 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 2. Indoor Safety Light
- **P:** 3 W (RAMP key: `power`)
- **Occasional_use:** 0.85 (RAMP key: `occasional_use`)
- **func_time:** 420 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [0, 420] (RAMP key: `window_1`) — 00:00–07:00
- **func_cycle:** 300 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 3. Outdoor Social / Transit Light
- **P:** 2 W (RAMP key: `power`)
- **Occasional_use:** 0.60 (RAMP key: `occasional_use`)
- **func_time:** 45 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [1080, 1260] (RAMP key: `window_1`)
- **func_cycle:** 20 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 4. Stacked Phone & Radio Charging (USB)
- **P:** 5 W (RAMP key: `power`) — simulates multiple devices / splitter; observed max ≈5.10 W
- **Occasional_use:** 1.00 (RAMP key: `occasional_use`)
- **func_time:** 900 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [0, 1440] (RAMP key: `window_1`)
- **func_cycle:** 300 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.00

---

## Profile 4 — System Breakers (based on Users 96 & 64)

High MRSD/chaos, low daily probabilities for some loads, and large timing variability.

### 1. Erratic Indoor Evening Task Light (LED_2)
- **P:** 3 W (RAMP key: `power`)
- **Occasional_use:** 0.90 (RAMP key: `occasional_use`)
- **func_time:** 100 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [1080, 1380] (RAMP key: `window_1`) — 18:00–23:00
- **time_fraction_random_variability:** 0.35
- **random_var_w:** 0.30

### 2. Indoor Morning Light
- **P:** 3 W (RAMP key: `power`)
- **Occasional_use:** 0.30
- **func_time:** 60 min
- **num_windows:** 1
- **window_1:** [300, 420]
- **func_cycle:** 40 min
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 3. Indoor Safety Light (LED_1)
- **P:** 2 W (RAMP key: `power`)
- **Occasional_use:** 0.35 (RAMP key: `occasional_use`)
- **func_time:** 350 min (RAMP key: `func_time`)
- **num_windows:** 2
- **window_1:** [0, 419] (RAMP key: `window_1`)
- **window_2:** [1381, 1440] (RAMP key: `window_2`)
- **func_cycle:** 240 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 4. Outdoor Transit Light
- **P:** 2 W (RAMP key: `power`)
- **Occasional_use:** 0.10
- **func_time:** (use-case dependent)
- **num_windows:** 1
- **window_1:** [1080, 1320]
- **func_cycle:** 60–90 min (example range)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

### 5. Burst Phone & Radio Charging (USB)
- **P:** 3.29 W (RAMP key: `power`)
- **Occasional_use:** 0.44 (RAMP key: `occasional_use`)
- **func_time:** 300 min (RAMP key: `func_time`)
- **num_windows:** 1
- **window_1:** [0, 1440] (RAMP key: `window_1`)
- **func_cycle:** 180 min (RAMP key: `func_cycle`)
- **time_fraction_random_variability:** 0.20
- **random_var_w:** 0.35

