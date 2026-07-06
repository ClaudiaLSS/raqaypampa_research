# **Profile 1: The educational and agriculture core**

**Demographic summary:** Nuclear and numerous families with working-age adults and school-aged children. Main economic activity is agriculture. The daily routine of these families consist on waking up early for preparing themselves to go to work to the fields and to prepare the children for school. Woman prepare food early to take and ead on the fields. Children come back to the house after school around 13:00 and head to the fields to help the parents. Once all go back to the house, the start doing homework and woman prepare food for diner around 18:00. These families exhibit a high valuation of education, often demonstrating strategic energy-rationing behaviors (load-shifting) to guarantee power availability for their children's evening studies. Flashlights use for night mobility is common. Leaving safety nights on during all night is moderate. Daytime use of energy is not common since they tend to be out of the household during the day.

## **The Driving Social Rules:**

-   **Rule 1 (The Educational Anchor):** The cultural priority of academic progress dictates that the evening lighting window is non-negotiable for homework.

-   **Rule 2 (The Agricultural Dictate):** The \"sun-up to sun-down\" labor requirement forces an early morning wake-up and creates a massive daytime \"demand valley\" where the house is empty.

-   **Rule 3 (The Gendered Anchor of Domestic Operations):** Adult women primarily control the kitchen, ensuring a strict lighting requirement during evening meal preparation.

-   **Rule 15 (The Productive Lighting Veto):** Adult women refuse to use SHS lights for weaving at night because the light attracts moths (polillas) that ruin wool, restricting productive labor to daylight hours.
  
## **Energy Signature & Metric Thresholds:**

-   **Peak Hour (18:00--19:00):** A rigid evening peak driven by the agricultural dictate (Rule 2). The load surges simultaneously when they return to cook and study.

-   **MRSD Chaos Index (1.20 - 1.30):** Moderate, predictable variability. User 72 and 74 show MRSDs of 1.262 and 1.252, respectively. The routine is highly structured around the agricultural calendar.

-   **Overall Mean Power (\> 1.25W):** High baseline energy footprints (User 72: 1.59W; User 74: 1.28W) indicative of sustained, multi-person consumption.

-   **Appliance Stacking Index (Moderate: 15% - 19%):** Because these are large families, users must strategically stagger their appliance use (e.g., charging phones before evening cooking), keeping simultaneous extreme loads manageable.

-   **Reliability & Blackouts:** Despite efficient battery use, the sheer volume of their evening demand creates high system stress. User 72 experienced the highest recorded blackout frequency (37 events, 60% of which were behaviorally induced). Standard 89 Wh batteries are frequently undersized for the intense evening surges of numerous families.

## **Appliance inventory:** 
- LED_1: Indoor light (main room)
- LED_2: Outdoor light 
- USB (phone chargers, radio charging and flashlight charging)

## **Daily social practices and anthropological windows**
*This section defines the socio-temporal envelopes that govern energy use for the Extended Hub profile. These are not periods of continuous power consumption; rather, they represent the broadest possible timeframes during which a specific social practice might occur. The RAMP algorithm is strictly constrained to generate the actual usage events only within these cultural boundaries.*

### Window 1: Morning agricultural and school preparation
**timeframe:** [300, 480] (05:00 – 08:00)
**Qualitative narrative:** Pre-dawn waking for indoor preparation (gathering tools, preparing food for the day, preparing children for school, brief morning tasks) before leaving the house. The routine is quick and efficient. Indoor lighbulb use is limited to brief, task-specific illumination. Outdoor lighting is used for brief, pre-dawn outdoor chores before the sun provides adequate visibility.
**Key social practices:**
- Preparing food for the day
- Preparing children for school
- Brief morning tasks before leaving the house
- Preparing the tools for the day

### Window 2: Daytime agricultural work and school attendance
**timeframe:** [480, 1020] (08:00 – 17:00)
**Qualitative narrative:** During standard agricultural workdays, indoor daytime electrical lighting is practically non-existent, as labor occurs predominantly outdoors and natural daylight suffices for basic indoor navigation. However, this baseline of zero-consumption is periodically interrupted by anomalous daytime events—such as severe weather (e.g., heavy rain forcing the family indoors), leaving devices charging while at work, periods of illness, or specific seasonal indoor chores (e.g., crop sorting, tool repair). Consequently, this energy load is fundamentally event-driven rather than routine-driven.
**Key social practices:**
- Agricultural work
- School attendance

### Window 3: Evening core gathering and education
**timeframe:** [1020, 1440] (17:00 – 23:59)
**Qualitative narrative:** This is the most critical and highly structured period of the household's energy demand. Beginning around 18:00, the main living space becomes a multi-use focal point. Because hardware is severely constrained—typically limited to only one lightbulb for the entire household—the single main-room light is actively shared and an outdoor lighting is used for brief, essential nighttime movement between structures (main room, secondary, latrine) or to secure animals for the night.
**Key social practices:**
- Food preparation and dining
- Homework and study    
- Socializing

### Window 4: Nighttime sleep and pasive security
**timeframe:** [0, 300] (00:00 – 05:00)
**Qualitative narrative:** To provide a sense of security or comfort during the night, families will sometimes leave a light on while sleeping. This is not active task lighting; it is a passive, continuous background load. However, staying up during this period is not common, and the light is often turned off for sleep. 
**Key social practices:**
- Sleep

## **Virtual Appliances formulation and parameterization**
*This section translates the social practices defined above into specific Virtual Appliances for the RAMP engine. It bridges the qualitative anthropological windows with the quantitative survey data.*

### **Virtual Appliance 1: Indoor morning light** 
- **Narrative:** Pre-dawn waking for indoor preparation (gathering tools, preparing food for the day, preparing children for school, brief morning tasks) before leaving the house. The routine is quick and efficient.
- **power:** 3 W (nominal power)
- **w_1:** [300, 420] (05:00 – 07:00)
- **func_time:** 90 minutes (1.5 hours)
- **time_fraction_random_variability:** 0.2
- **random_var_w:** 0.3
- **func_cycle:** 60 minutes (1 hour, strict. Bounded by sunrise.)
- **occasional_use:** 0.42 (Casual/Seasonal, three times a week. It does not happen every day, suggesting this specific indoor morning routine might shift depending on the agricultural season or day of the week)


### **Virtual Appliance 2: Indoor occasional daytime light** 
- **Narrative:** During standard agricultural workdays, indoor daytime electrical lighting is practically non-existent, as labor occurs predominantly outdoors and natural daylight suffices for basic indoor navigation. However, this baseline of zero-consumption is periodically interrupted by anomalous daytime events—such as severe weather (e.g., heavy rain forcing the family indoors), leaving devices charging while at work, periods of illness, or specific seasonal indoor chores (e.g., crop sorting, tool repair). Consequently, this energy load is fundamentally event-driven rather than routine-driven.
  
- **power:** 3 W (nominal power)
- **w_1:** [420, 1020] (07:00 – 17:00)
- **func_time:** 60 minutes (1 hour)
- **time_fraction_random_variability:** 0.3
- -**random_var_w:** 0.3
- **func_cycle:** 30 minutes (High Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.)
- **occasional_use:** 0.57 (Rare / Intermittent, four times a week)


### **Virtual Appliance 3: Indoor task light for homework and dinner** 
- **Narrative:** This is the most critical and highly structured period of the household's energy demand. Beginning around 18:00, the main living space becomes a multi-use focal point. Because hardware is severely constrained—typically limited to only two lightbulbs for the entire household—the single main-room light is actively shared. Women utilize this centralized illumination for food preparation and dining (R3), while children simultaneously rely on it to complete their schoolwork (R1). Education is a profound priority; therefore, lighting during this window is considered absolutely non-negotiable. To guarantee sufficient battery capacity for this essential evening routine, families exhibit strategic load-shifting, consciously rationing their energy consumption throughout earlier parts of the day. This appliance gathers the family for inddor activities to end the day.

- **power:** 3 W (nominal power)
- **w_1:** [1020, 1320] (17:00 – 22:00)
- **func_time:** 180 minutes (3 hours)
- **time_fraction_random_variability:** 0.1
- **random_var_w:** 0.2
- **func_cycle:** 150 minutes (Non-negotiable / Highly Strict. The usage is continuous and essential)
- **occasional_use:** 1 (daily)

### **Virtual Appliance 4: Indoor safety light** 
- **Narrative:** To provide a sense of security or comfort during the night, families will sometimes leave a light on while sleeping. This is not active task lighting; it is a passive, continuous background load.

- **power:** 3 W (nominal power)
- **w_1:** [1320, 1440] (22:00 – 23:59)
- **w_2:** [0, 330] (00:00 – 05:30)
- **func_time:** 360 minutes (6 hours)
- **time_fraction_random_variability:** 0.1
- **random_var_w:** 0.2
- **func_cycle:** 100 minutes (Strict / Continuous. When utilized, the light is left on for extremely long, uninterrupted blocks while the household sleeps.)
- **occasional_use:** 0.28 (Intermittent. Used roughly two times a week, likely dependent on external factors like weather, perceived security, or remaining battery state of charge.)

### **Virtual Appliance 5: Outdoor transit morning light** 
- **Narrative:** Similar to the indoor morning routine, this represents brief, pre-dawn outdoor chores (e.g., feeding animals, preparing equipment in the yard) before the sun provides adequate visibility.

- **power:** 2 W (nominal power)
- **w_1:** [270, 450] (04:30 – 07:30) (it starts a bit later than the indoor morning light, as the household first completes indoor preparation before moving outside)
- **func_time:** 60 minutes (1 hour)
- **time_fraction_random_variability:** 0.2
- **random_var_w:** 0.3
- **func_cycle:** 50 minutes (Strict. Bounded by the sunrise.)
- **occasional_use:** 0.28 (highly frequent)

### **Virtual Appliance 6: Outdoor rare daytime light** 
- **Narrative:** not reported as a regular or daily habit. Not needed for standard agricultural work, but may be used during rare, specific daytime events (e.g., severe weather forcing outdoor tasks to be performed in low-light conditions, or a specific seasonal chore that requires outdoor illumination).

- **power:** 2 W (nominal power)
- **w_1:** [450, 1050] (07:00 – 17:30)
- **func_time:** 60 minutes (1 hour)
- **time_fraction_random_variability:** 0.3
- **random_var_w:** 0.3
- **func_cycle:** 30 minutes (High Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.)
- **occasional_use:** 0.14 (Rare / Intermittent, once a week)


### **Virtual Appliance 7: Outdoor night transit light** 
- **Narrative:** During the evening, family members move between structures (main room, secondary, latrine) or secure animals for the night. This light is used daily but operates in intermittent bursts rather than a continuous draw, reflecting transient outdoor movement rather than prolonged outdoor labor. People will remain often outside even for eating during summer or spring.

- **power:** 2 W (nominal power)
- **w_1:** [1050, 1290] (17:30 – 21:30) (Stopped at 21:30 because the household is generally settled for the night by this time, and outdoor movement is minimal after this hour.)
- **func_time:** 90 minutes (1,5 hour)
- **time_fraction_random_variability:** 0.2
- **random_var_w:** 0.3
- **func_cycle:** 70 minutes (Moderate. While the overall window is wide, the usage happens in distinct blocks (around 30 minutes at a time) as people move about before resting.)
- **occasional_use:** 1 (daily)

### **Virtual Appliance 8: Outdoor safety light** 
- **Narrative:** Not reported as a consistent, daily habit, but some families will occasionally leave an outdoor light on during the night for security or comfort. This is not active task lighting; it is a passive, continuous background load.

- **power:** 2 W (nominal power)
- **w_1:** [1230, 1440] (21:30 – 23:59)
- **w_2:** [0, 300] (00:00 – 05:00)
- **func_time:** 30 minutes (0.5 hours)
- **time_fraction_random_variability:** 0.3
- **random_var_w:** 0.3
- **func_cycle:** 15 minutes (Moderate. It is used for very specific, brief tasks (e.g., checking on animals, securing doors) rather than continuous illumination.  )
- **occasional_use:** 0 (Rare / Intermittent, once a week. It is not a daily habit, but rather a sporadic precautionary measure.)

### **Virtual Appliance 9: Portable devices charging** 
- **Narrative:** Information and communication are constant background needs, recently increased for education purposes. Devices are plugged in opportunistically whenever power is available. Because charging is passive, it is entirely decoupled from strict human behavioral windows and occurs throughout the entire day. In the surveys, people strugled to estimate the total time spent charging, but it was clear that it was a significant portion of the day. The total daily time spent charging is estimated to be nearly 7 hours, spread across multiple cycles and devices (including mobile phones, flashlights, and radios).

- **power:** 3 W (nominal power)
- **w_1:** [240, 1440] (00:00 – 23:59)
- **func_time:** 420 minutes (7 hours)
- **time_fraction_random_variability:** 0.3
- **random_var_w:** 0.2
- **func_cycle:** 120 minutes (Changing cycles for the phones are around 2 hours, but the total daily time spent charging is estimated to be nearly 6 hours, spread across multiple cycles and devices (including mobile phones, flashlights, and radios).)
- **occasional_use:** 1 (daily)


## Seasonality and Agricultural Calendar in Raqaypampa

PLANTING SEASON (October-January):
        - Planting begins Oct-Nov (staple crops: potatoes, maize)
        - Wheat sowing in January
        - Mama Rosario festival (October) marks seasonal beginning
        - Livestock actively controlled to protect newly sown fields
        - High labor demands, families stay home to tend crops
        - Expected Energy Impact: MODERATE-HIGH (field work, animal tending)

    GROWING & EARLY HARVEST (February-April):
        - Constant labor and crop care throughout rainy season
        - Carnival (Feb-Mar): rituals to thank Mother Earth for growing crops
        - Harvesting begins in March, continues through season
        - Peak labor intensity beginning
        - Expected Energy Impact: HIGH (ongoing field work, harvest preparation)

    HARVESTING SEASON (May-June):
        - Heavy harvesting work across the entire community
        - Ends June 24 with San Juan festival (marks end of harvest, start of Andean New Year)
        - Chhalaku: traditional bartering of highland products for valley goods
        - Highest physical labor demands
        - Expected Energy Impact: VERY HIGH (intensive harvesting)

    FREE GRAZING & MIGRATION (July-September):
        - June 24-October: Territory becomes communal pasture
        - Animals released to graze freely on crop stubble (rastrojos)
        - Temporary migration to regions like Chapare for supplementary income
        - Families may be absent for extended periods
        - Lowest agricultural labor demands
        - Expected Energy Impact: LOW (minimal field work, household absence possible)

According to observations, the energy consumption from the Solar Home Systems cannot vary significantly due to its technical limitations. However, seasonality is primarily friven by family mobility and the agricultural calendar. In the specific case of Profile 1, the above parametrization corresponds to the baseline, where family remains in the household and the energy consumption is stable. However, during the Growing and Grazing season, the family may be absent for extended periods, which would result in a significant reduction of energy consumption. Families tend to move temporarily near to the lands where they are working or if not moving, they stay longer periods of time there. These periods of absense are highly constrained by children attending to school, which is a non-negotiable priority for the family, causing partial absence. Therefore, the energy consumption during these periods of absense is expected to be lower than the baseline, but not zero. To achieve this representation in the model, the Virtual Appliances 1, 2, 3, 5, 6 and 7 will be parametrized with a lower occasional_use value during the Growing and Grazing season. The Virtual Appliances 4 and 8 will be parametrized with a the same occasional_use value as the baseline during the Growing and Grazing season. The Virtual Appliance 9 will be parametrized with a lower func_time value during the Growing and Grazing season.

Parameters that change during the Growing and Grazing season:
- Virtual Appliance 1: Indoor morning light
    - occasional_use: 0.28 (Rare / Intermittent, twice a week)
- Virtual Appliance 2: Indoor occasional daytime light
    - occasional_use: 0.14 (Rare / Intermittent, once a week)
- Virtual Appliance 3: Indoor task light for homework and dinner
    - occasional_use: 1 (Casual / Seasonal, five times a week)
- Virtual Appliance 5: Outdoor transit morning light
    - occasional_use: 0.71 (Rare / Intermittent, once a week)
- Virtual Appliance 6: Outdoor rare daytime light
    - occasional_use: 0.14 (Rare / Intermittent, once a week)
- Virtual Appliance 7: Outdoor night transit light
    - occasional_use: 0.71 (Casual / Seasonal, five times a week)
- Virtual Appliance 9: Portable devices charging
    - func_time: 300 minutes (5 hours)