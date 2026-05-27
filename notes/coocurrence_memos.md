A report is generated in Qualcoder to explore co-occurrences among the
codes, considering categories: Practices, Norms, Material and
Socioeconomics. In this file, I will draft interesting memos I get from
these occurrences.

### **Theme 1: The Daily Baselines (Predictable Anchors)**

*These rules define the rigid, highly probable load curve shapes that
occur almost every single day, unaffected by minor weather changes.*

**Rule 1: The Educational Anchor**

-   **Formula:** \[NOR\_education / DEMO\_youth\_male &
    > DEMO\_youth\_female\] drives \[PR\_act\_school\_homework /
    > PR\_use\_lights\_time\_evening\_routine\] under
    > \[MAT\_appliance\_priority / limited battery capacity\].

-   **The Narrative:** The cultural priority of intergenerational
    > academic progress dictates that the evening lighting window is
    > non-negotiable. Parents will actively restrict daytime appliance
    > use or unplug radios to ensure enough battery remains for children
    > to study safely under LED lights until 22:00.

-   **RAMP Modeling Implication (Temporal & Reliability):** Protects the
    > \"Critical Discharge Window.\" In the simulation, the evening
    > lighting load (18:00--22:00) is highly inelastic (Probability of
    > Use = \~1.0) and receives the highest priority in the
    > load-shedding hierarchy.

**Rule 2: The Agricultural Dictate**

-   **Formula:** \[NOR\_labor\_activity\_constraint / DEMO\_male\_adult
    > & DEMO\_female\_adult\] drives \[PR\_cooking\_routine\_daily /
    > PR\_use\_lights\_time\_morning\_routine\] under
    > \[SOC\_livelihood\_agriculture / rigorous agricultural
    > schedules\].

-   **The Narrative:** The necessity of \"sun-up to sun-down\"
    > agricultural labor forces households to wake well before dawn.
    > Energy behavior is constrained by this survival routine,
    > necessitating an early period of lighting for meal preparation
    > before the family abandons the house.

-   **RAMP Modeling Implication (Temporal & Shape):** Establishes a
    > short, sharp early morning demand spike (e.g., 04:00 to 06:00)
    > followed immediately by a massive \"demand valley\" where
    > household load drops to absolute zero during daylight hours.

**Rule 3: The Gendered Anchor of Domestic Operations**

-   **Formula:** \[NOR\_gendered\_energy\_roles / DEMO\_female\_adult\]
    > drives \[PR\_act\_meals\] under \[MAT\_appliance\_priority / fixed
    > LED lighting\].

-   **The Narrative:** Social norms dictate that adult women are
    > primarily responsible for the kitchen and evening meal
    > preparation. This routine acts as the temporal anchor for the
    > household, defining the start of the evening active period.

-   **RAMP Modeling Implication (Magnitude & Temporal):** The presence
    > of DEMO\_female\_adult guarantees the most consistent evening
    > lighting demand window, directly dictating the daily depth of
    > discharge (DoD) of the battery.

**Rule 4: The Connectivity Lifeline**

-   **Formula:** \[NOR\_value\_of\_connectivity / DEMO\_female\_senior &
    > DEMO\_male\_senior\] drives \[PR\_act\_information\_communication
    > / PR\_use\_ict\_day\_charging\] under
    > \[SOC\_migration\_permanent\_outflux / permanent migration of
    > children\].

-   **The Narrative:** For elderly populations left behind by
    > rural-urban migration, the cell phone is an emotional lifeline,
    > not a luxury. Maintaining a charged phone to communicate with
    > children in the Chapare or cities is prioritized over personal
    > lighting.

-   **RAMP Modeling Implication (Reliability):** Device charging is
    > categorized as a \"critical load.\" Even at low battery levels,
    > the simulation should execute this draw, bypassing standard
    > energy-saving logic.

### **Theme 2: System Constraints & Coping Mechanisms**

*These rules define how users dynamically interact with the physical
limits of the environment and the battery.*

**Rule 5: Weather-Driven Load Shedding**

-   **Formula:** \[NOR\_system\_capacity\_resignation /
    > DEMO\_female\_adult & DEMO\_male\_adult\] drives
    > \[PR\_energy\_management / PR\_use\_ict\_day\_charging\] under
    > \[MAT\_environmental\_vulnerability / cloudy or rainy weather\].

-   **The Narrative:** Users exhibit high technical literacy regarding
    > their system\'s limits. When weather conditions prevent full
    > charging, users proactively \"load shed\" by rationing light and
    > aggressively shifting their mobile charging strictly to peak
    > daylight hours to protect the battery's state of charge.

-   **RAMP Modeling Implication (Temporal):** Shifts the charging load
    > profile to perfectly coincide with the solar generation curve
    > (e.g., 10:00 to 16:00), effectively \"clipping\" demand off the
    > battery.

**Rule 6: The Safety Baseline**

-   **Formula:** \[NOR\_safety / DEMO\_female\_adult &
    > DEMO\_female\_senior\] drives
    > \[PR\_lights\_extreme\_night\_usage\] under
    > \[IMP\_health\_and\_safety / presence of venomous insects and
    > physical hazards\].

-   **The Narrative:** The culturally reinforced fear of venomous fauna
    > (scorpions, vinchucas) and tripping hazards overrides general
    > conservation habits, prompting users (especially mothers and the
    > elderly) to leave at least one light illuminated until dawn.

-   **RAMP Modeling Implication (Shape & Magnitude):** Radically alters
    > the load curve. Instead of dropping to zero after 22:00, the
    > simulation must apply a continuous 12-hour base load (1--5W),
    > drastically impacting the starting State of Charge (SoC) for the
    > following day.

**Rule 7: Infrastructure Mobility**

-   **Formula:** \[NOR\_ownership\_duty / DEMO\_male\_adult\] drives
    > \[PR\_system\_mobility\] under \[SOC\_migration\_temporary\_labor
    > / seasonal agricultural work in the \"monte\"\].

-   **The Narrative:** Due to extreme geographical isolation and the
    > necessity of seasonal agricultural migration, the SHS is treated
    > as a portable survival tool rather than fixed household
    > infrastructure. Men actively dismantle and transport the system to
    > temporary camps.

-   **RAMP Modeling Implication (Reliability & Shape):** Introduces
    > \"seasonal absences.\" The algorithm must probabilistically drop
    > the baseline load to zero for periods ranging from weeks to months
    > at the primary geographic coordinate.

**Rule 8: Nature as a Threat (Environmental Fear)**

-   **Formula:** \[NOR\_environmental\_fear / DEMO\_female\_senior\]
    > drives \[Avoidance of PR\_sys\_maintenance\] under
    > \[MAT\_environmental\_vulnerability / thunderstorms and
    > lightning\].

-   **The Narrative:** Culturally reinforced fears that solar panels
    > attract deadly lightning strikes lead users to physically
    > disconnect the system or actively avoid touching/cleaning it
    > during the rainy season.

-   **RAMP Modeling Implication (Generation/Yield Model):** Introduces a
    > severe seasonal variable. Increases the probability of complete
    > physical disconnection during stormy months and increases
    > \"soiling losses\" (dust accumulation) due to reliance strictly on
    > passive rain-washing.

**Rule 9: The Aspiration Gap and Dual-Home Displacement**

-   **Formula:** \[NOR\_app\_aspiration / DEMO\_male\_adult\] drives
    > \[PR\_dual\_home\_strategy\] under
    > \[MAT\_geographical\_infrastructure\_gap / lack of grid
    > connectivity at the SHS location\].

-   **The Narrative:** The desire for modern comfort (TVs, blenders)
    > cannot be met by the SHS. Rather than abandoning the desire,
    > families maintain a bivocational lifestyle, delegating heavy
    > energy tasks to a secondary, grid-connected home while zoning the
    > SHS home strictly for basic survival.

-   **RAMP Modeling Implication (Magnitude / Latent Demand):** Explains
    > why the current load curve is artificially flat. It provides the
    > mathematical parameters for a \"grid-arrival\" or \"capacity
    > doubling\" simulation, triggering immediate high-wattage spikes
    > (50W--100W) that are currently suppressed.

### **Theme 3: The System Breakers (Anomalies & Stochastic Events)**

*These rules explain the chaotic, unpredictable data points in the
datalogger that traditional engineering models fail to simulate.*

**Rule 10: Energy Bricolage (Hacking)**

-   **Formula:** \[NOR\_energy\_experience\_legacy / DEMO\_male\_adult\]
    > drives \[PR\_independent\_acquisition\] under
    > \[MAT\_parallel\_infrastructure\].

-   **The Narrative:** Users with previous technical exposure to legacy
    > systems refuse to be constrained by the project SHS. They actively
    > hack together independent infrastructure, wiring old panels to
    > motorcycle batteries to run parallel charging stations.

-   **RAMP Modeling Implication (Magnitude Validation):** Acts as a
    > critical data correction rule. It alerts the simulation that the
    > measured SHS datalogger load is a false baseline, representing
    > only a fraction of the actual total domestic demand.

**Rule 11: Protective Gatekeeping**

-   **Formula:** \[NOR\_ownership\_duty & NOR\_fear\_of\_tech\_failure\]
    > drives \[NOR\_energy\_gatekeeping\] under
    > \[MAT\_hardware\_degradation (fear of)\].

-   **The Narrative:** The intense fear of breaking a fragile,
    > irreplaceable financial asset overrides indigenous communal
    > sharing norms. Users actively refuse to let neighbors charge
    > devices to protect their USB ports from damage.

-   **RAMP Modeling Implication (Reliability):** Prevents peer-to-peer
    > load dumping. In the simulation, if Household A\'s system fails,
    > the algorithm cannot assume Household A\'s demand safely shifts to
    > Household B\'s profile.

**Rule 12: Community Override (Stochastic Spikes)**

-   **Formula:** \[NOR\_energy\_sharing\] drives
    > \[PR\_act\_socializing\] under \[IMP\_extended\_waking\_hours /
    > Community Events\].

-   **The Narrative:** Normal routines of strict energy conservation are
    > temporarily suspended during major community events (e.g.,
    > *velorios* or visiting relatives). Energy becomes a tool for
    > communal hospitality.

-   **RAMP Modeling Implication (Variability):** Explains massive,
    > unpredictable standard deviations. Provides the behavioral logic
    > to program low-probability, high-impact \"stochastic spikes\"
    > where lighting is drawn continuously for 48 hours, fully depleting
    > the system.

**Rule 13: Hardware Resignation (The Silent Drop)**

-   **Formula:** \[NOR\_fear\_of\_tech\_failure\] drives \[Permanent
    > load reduction\] under \[MAT\_hardware\_degradation\].

-   **The Narrative:** Due to a lack of technical literacy and missing
    > supply chains, minor hardware failures (e.g., a snapped jack or
    > loose USB port) result in the permanent abandonment of the
    > appliance rather than a repair.

-   **RAMP Modeling Implication (Shape & Reliability):** Introduces a
    > \"hardware decay rate\" to the model. Load curves must simulate
    > permanent, step-wise drops to zero for specific appliances (like
    > the continuous 3W radio load disappearing mid-year).

**Rule 14: Companionship in Isolation**

-   **Formula:** \[NOR\_aging\_energy\_culture / DEMO\_male\_senior\]
    > drives \[PR\_use\_lights\_time\_evening\_routine /
    > PR\_act\_leisure\_company\] under
    > \[MAT\_geographical\_infrastructure\_gap / living alone in
    > isolated rural areas\].

-   **The Narrative:** For elderly adults living entirely alone due to
    > migration, the continuous use of the radio or lighting serves
    > primarily as psychological comfort and companionship rather than
    > utilitarian necessity.

-   **RAMP Modeling Implication (Magnitude & Shape):** Flattens the
    > probabilistic \"use windows\" associated with active tasks,
    > converting the radio into a continuous, flat load profile (drawing
    > power constantly from 06:00 to 18:00).

### **Theme 4: Productive Labor & Multi-Energy Realities**

**Rule 15: The Productive Lighting Veto (The Weaving Constraint)**

-   **Formula:** \[NOR\_labor\_activity\_constraint /
    > DEMO\_female\_adult\] restricts \[PR\_act\_productive /
    > PR\_act\_knitting\] under \[MAT\_appliance\_priority (low lumens)
    > & IMP\_health\_and\_safety (insects/polillas)\].

-   **The Narrative:** Despite having evening illumination, adult women
    > actively *refuse* to use the SHS light for income-generating
    > textile work (weaving/spinning). They cite two physical
    > constraints: the LED light is not \"nítida\" (clear/bright) enough
    > for detailed work, and the light attracts moths (*polillas*) which
    > ruin the valuable wool. Thus, productive textile labor remains
    > strictly anchored to daylight hours. *(Found in transcripts: Users
    > 72, 81, 85).*

-   **RAMP Modeling Implication (Shape/Magnitude Constraint):** Prevents
    > the algorithm from artificially extending the evening lighting
    > load window for productive tasks. It proves that simply providing
    > a basic 2W bulb does *not* automatically trigger nighttime
    > economic productivity in the simulation.

**Rule 16: The Thermal Weather Switch (Fuel Stacking)**

-   **Formula:** \[MAT\_geographical\_infrastructure\_gap / lack of
    > roads\] drives \[PR\_fuel\_stacking\_cooking\] under
    > \[MAT\_environmental\_vulnerability / Rain\].

-   **The Narrative:** While this does not draw electricity, it is vital
    > for multi-energy modeling. Users default to gathered firewood for
    > cooking because the lack of roads makes carrying heavy LPG gas
    > cylinders on foot grueling. However, when it rains and firewood
    > gets wet, users immediately switch to their hoarded LPG gas.

-   **RAMP Modeling Implication (Multi-Energy Profiling):** If you are
    > running RAMP as a multi-energy simulator (thermal + electrical),
    > this rule dictates the thermal load switch. It proves that
    > *weather* is the master variable in Raqaypampa, dictating not just
    > solar generation, but also the choice of cooking fuel.

**Rule 17: The Gratitude/Scarcity Baseline** (11--17 overlaps)

-   **Formula:** \[NOR\_energy\_experience\_legacy\] defines
    > \[PR\_substitution / MAT\_legacy\_candle / MAT\_legacy\_mechero\].

-   **RAMP Implication:** The memory of toxic smoke and buying candles
    > creates a highly conservative behavioral baseline. This justifies
    > assigning a lower-than-average relative mean power factor, as
    > users treat the LED light as a precious commodity, not an infinite
    > utility.

**Rule 18 The Sedentary Anchor / Aging in Place**

-   **Formula:** \[MAT\_physical\_constraint / DEMO\_male\_senior &
    > DEMO\_female\_senior\] restricts \[PR\_system\_mobility\] under
    > \[SOC\_migration\_temporary\_labor\].

-   **The Narrative:** Due to the physical limitations of aging, elderly
    > households do not participate in the temporary, labor-intensive
    > migration to the *monte*. They remain anchored to the primary
    > residence year-round, serving as caretakers of the permanent
    > household infrastructure.

-   **RAMP Modeling Implication:** Protects \"Profile 2: Isolated
    > Elderly\" from seasonal load-shedding. The simulation must
    > maintain a continuous 365-day baseline for this demographic,
    > completely blocking the stochastic \"Absence/Vacation\" modifier
    > that is applied to younger, agriculturally active profiles.
