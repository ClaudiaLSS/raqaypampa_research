# **Profile 2: The isolated elderly**

**Demographic summary:** Households consisting of single adults, isolated elderly individuals, or older couples living independently, defined primarily by the complete absence of working-age adults and school-aged dependents. This profile is a direct sociological consequence of systemic rural-to-urban out-migration. As younger generations relocate to urban centers for economic or educational opportunities, these aging populations remain in the village, aging in place (R18). They are frequently supported by a remittance economy, receiving intermittent financial assistance and casual visits from their migrated children. Consequently, their daily routines—and resulting energy demands—are distinctively less structured around rigid agricultural or educational schedules, leading to a lower overall energy intensity but a much higher reliance on passive companionship devices (like radios and phones) (R14, R4) and overnight security lighting (R6).

### **The Driving Social Rules:**

-   **Rule 6 (The Safety Baseline):** The culturally reinforced fear of venomous fauna (scorpions, vinchucas) prompts users to leave a light illuminated continuously.

-   **Rule 14 (Companionship in Isolation):** For elderly adults living alone, continuous radio or lighting serves as psychological comfort.

-   **Rule 4 (The Connectivity Lifeline):** Maintaining a charged phone to communicate with migrated children is prioritized over personal lighting.

-   **Rule 18 (The Sedentary Anchor):** Aging limits mobility; they do not participate in temporary migration to the "monte", resulting in a continuous 365-day baseline.


### **Energy Signature & Metric Thresholds:**

-   **Peak Hour (20:00 or Variable):** A later, less intense peak compared to the agricultural core. The morning wake-up is smoother, lacking the urgency of school preparation.

-   **Night Safety Probability (\> 75%):** The defining metric of this profile. User 11 exhibits an ultra-stable footprint with a continuous overnight safety light (75.8% probability). Energy is utilized primarily as a security anchor (Rule 6).

-   **MRSD Chaos Index (1.20 - 1.80):** Generally chaotic to moderately stable (User 11: 1.269; User 84: 1.717), reflecting isolated lives punctuated by occasional visits from non-resident children.

-   **Overall Mean Power (\~1.00W or lower):** Moderate to low volumetric baselines (User 11: 1.09W) with low peak-to-mean ratios.

-   **Appliance Stacking Index (\< 1.0%):** A solitary individual cannot physically occupy multiple rooms or utilize multiple devices simultaneously. This sequential usage pattern prevents extreme peak loads.

-   **Reliability & Blackouts:** Moderate blackout frequency (e.g., 6.25 per 100 days for User 11). Blackouts occur more frequently than in Profile 1 because continuous night lighting (Rule 6) constantly drains the battery, leaving it vulnerable to cloudy days.

### **Appliance inventory:** 
- LED_1: Indoor light (main room)
- LED_2: Outdoor light 
- USB (phone chargers, radio charging and flashlight charging)

## **Daily social practices and anthropological windows**
*This section defines the socio-temporal envelopes that govern energy use for the Extended Hub profile. These are not periods of continuous power consumption; rather, they represent the broadest possible timeframes during which a specific social practice might occur. The RAMP algorithm is strictly constrained to generate the actual usage events only within these cultural boundaries.*

### Window 1: Slow morning wake-up and indoor navigation
**timeframe:** [360, 480] (06:00 – 08:00)
**Qualitative description:** The elderly wake up slowly, often requiring light for indoor navigation and basic morning tasks. This period is characterized by a lack of urgency, as there are no school or work obligations.
**Key social practices:**
- Preparing food
- Navigating the home safely
- Engaging in light household chores


### Window 2: Daytime activities
**timeframe:** [480, 1020] (08:00 – 17:00)
**Qualitative description:** During the daytime, isolated elders engage in various activities that may require lighting, such as cooking, eating, feeding animals or other household tasks. This period is characterized by a more structured routine compared to the morning hours.
**Key social practices:**
- Socializing
- Preparing meals
- Taking care of animals

### Window 3: Evening activities
**timeframe:** [1020, 1260] (17:00 – 21:00)
**Qualitative description:** In the evening, isolated elders may engage in activities that require lighting such as preparing food. This period is characterized by a more relaxed pace and a focus on leisure activities. Elders tend to sleep earlier than younger populations, and their evening routines are often shorter and less intense.
**Key social practices:**
- Preparing food
- Engaging in leisure activities    

### Window 4: Nighttime safety and companionship
**timeframe:** [1260, 1440] (21:00 – 24:00) and [0, 360] (00:00 – 06:00)
**Qualitative description:** During the night, isolated elders prioritize safety and companionship. Most of the users with this profile claims health problems related to vision and hearing, consecuently, use of radios and phones is reduced to family communication. This period is characterized by a focus on safety and comfort, with lighting used to navigate the home and provide a sense of security.
**Key social practices:**
- Sleep

## **Virtual Appliances formulation and parameterization**
*This section translates the social practices defined above into specific Virtual Appliances for the RAMP engine. It bridges the qualitative anthropological windows with the quantitative survey data.*

### **Virtual Appliance 1: Indoor morning light** 
- **Narrative:** Isolated elders frequently exhibit altered sleep architectures, which can include waking well before dawn for unhurried indoor routines such as warmth preparation (e.g., lighting a stove) or basic navigation. However, qualitative interviews explicitly reveal that physical limitations, fatigue, and environmental factors (like cold weather) often prevent them from rising early. Because this household completely lacks external structural constraints—such as communal harvesting shifts or school start times—they can accommodate these physical limitations. Consequently, morning lighting is not a daily guarantee; it is dictated by the intersection of biological rhythm and day-to-day physical capacity.

- **power:** 3 W (nominal power)
- **w_1:** [360, 480] (06:00 – 08:00)
- **func_time:** 60 minutes (1 hours)
- **func_cycle:** 30 minutes (High Chaos. The absence of strict external deadlines, compounded by fluctuating physical health, means the exact waking hour drifts significantly.)
- **occasional_use:** 0.42 (Intermittent. three times a week. It does not happen every day, suggesting this specific indoor morning routine might shift depending on natural light conditions, physical health, or day of the week)

### **Virtual Appliance 2: Indoor occasional daytime light** 
- **Narrative:** Unlike active agricultural families who spend the majority of the day outdoors, isolated elders experience prolonged indoor residency. While natural daylight is generally sufficient, their specific physical needs (e.g., declining visual acuity) and specific localized tasks (e.g., sewing, sorting seeds, cooking) necessitate occasional supplementary lighting during the day. Furthermore, overcast weather significantly drives this load, as elders are more likely to remain indoors and require light for safety and comfort. However, energy poverty legacy limits the usage of lights during the day, and they are used only when absolutely necessary. This is a highly variable, non-daily practice, reflecting the intersection of physical health, task requirements, and environmental conditions.

- **power:** 3 W (nominal power)
- **w_1:** [480, 1080] (08:00 – 18:00)
- **func_time:** 60 minutes (1 hour)
- **func_cycle:** 30 minutes (High Chaos. Usage is inherently reactive—triggered by fluctuating daylight conditions, specific visual tasks, or intermittent indoor chores rather than a rigid daily schedule.)
- **occasional_use:** 0.28 (Rare/intermitent, twice a week.)

### **Virtual Appliance 3: Indoor evening task light** 
- **Narrative:** Active late-night task lighting is generally uncharacteristic for this demographic, as their daily rhythms are anchored by early resting times. However, this baseline is punctuated by high behavioral variability. Occasional usage spikes are driven by two distinct sociological factors: disrupted sleep architectures (such as waking briefly in the night for specific necessities) and, crucially, intermittent visits from out-migrated family members. During these social visits, the elder's standard isolated routine is temporarily disrupted, significantly extending both the duration and the temporal window of lighting use as the household momentarily mimics the energy behavior of a larger, active family unit.
- **Anthropological window:** [1020, 1440] (17:00 – 23:59)
- **Rigidity:** High Chaos. The start times and durations are highly variable, representing unpredictable wakefulness rather than a scheduled routine.
- **Frequency:** Daily, but highly variable.

- **power:** 3 W (nominal power)
- **w_1:** [1060, 1260] (18:00 – 21:00)
- **func_time:** 120 minutes (2 hours)
- **func_cycle:** 60 minutes (High Chaos. The start times and durations are highly variable, representing unpredictable wakefulness rather than a scheduled routine.)
- **occasional_use:** 1 (daily)

### **Virtual Appliance 4: Indoor safety light** 
- **Narrative:** There is a deep psychological need for overnight visibility for safety, comfort, and early morning navigation (due to altered sleep architectures common in elderly populations). The light acts as a constant nighttime companion. Lights are not used for morning tasks since there is no need for early wake-up.
- **Anthropological window:** [0, 300] (00:00 – 05:00)
- **Rigidity:** Strict. The usage is massive and continuous, running in solid 4-hour blocks while the user rests or wakes early.
- **Frequency:** Highly frequent

- **power:** 3 W (nominal power)
- **w_1:** [1260, 1440] (21:00 – 23:59)
- **w_2:** [0, 360] (00:00 – 06:00)
- **func_time:** 480 minutes (8 hours)
- **func_cycle:** 150 minutes (Strict. The usage is massive and continuous, running in solid 7-hour blocks while the user rests or wakes early.)
- **occasional_use:** 0.57 (Highly frequent, 4 times a week)

### **Virtual Appliance 5: Outdoor transit morning light** 

- **Narrative:** Isolated elders rarely leave the physical confines of the homestead after dark due to mobility constraints or safety concerns. When this light is used, it is for very brief, essential outdoor tasks (like a short trip to a latrine).

- **power:** 2 W (nominal power)
- **w_1:** [390, 480] (06:30 – 08:00) (it starts a bit later than the indoor morning light, as the household first completes indoor preparation before moving outside)
- **func_time:** 60 minutes (1 hour)
- **func_cycle:** 15 minutes (Moderate. While the window is tight, the usage is extremely brief, cycles of only 15 minutes)
- **occasional_use:** 0.14 (Very rare, once a week. Since elders wake up later than younger populations, this outdoor light is used only when absolutely necessary, and not every day.)

### **Virtual Appliance 6: Outdoor rare daytime light** 
- **Narrative:** not reported as a regular or daily habit. Not needed for standard agricultural work, but may be used during rare, specific daytime events (e.g., severe weather forcing outdoor tasks to be performed in low-light conditions, or a specific seasonal chore that requires outdoor illumination).

- **power:** 2 W (nominal power)
- **w_1:** [480, 1020] (08:00 – 17:00)
- **func_time:** 30 minutes (0.5 hours)
- **func_cycle:** 10 minutes (High Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.)
- **occasional_use:** 0.14 (Super rare  / Intermittent, once a week)


### **Virtual Appliance 7: Outdoor night transit light** 
- **Narrative:** In stark contrast to active agricultural or extended households, isolated elders exhibit minimal outdoor mobility after dusk due to heightened physical vulnerability, declining visual acuity, and general safety concerns. Consequently, the utilization of outdoor illumination is entirely divested from social gathering or evening chores. It functions strictly as a necessity-driven transit light. When triggered, it is exclusively for very brief, essential movements (such as a short, necessary trip to an outdoor latrine or to secure an exterior door) before retiring early for the night.

- **power:** 2 W (nominal power)
- **w_1:** [1020, 1260] (17:00 – 21:00) (Stopped at 21:30 because the household is generally settled for the night by this time before going to sleep)
- **func_time:** 90 minutes (1,5 hour)
- **func_cycle:** 30 minutes (Moderate. While the overall window is wide, the usage happens in distinct blocks (around 30 minutes at a time) as people move about before resting.)
- **occasional_use:** 1 (daily)

### **Virtual Appliance 8: Outdoor safety light** 
- **Narrative:** Not reported as a consistent, daily habit, but some families will occasionally leave an outdoor light on during the night for security or comfort. This is not active task lighting; it is a passive, continuous background load.
- **Anthropological window:** [0, 300] (00:00 – 05:00)
- **Rigidity:** Strict / Continuous. When utilized, the light is left on for extremely long, uninterrupted blocks while the household sleeps.
- **Frequency:** Rare 

- **power:** 2 W (nominal power)
- **w_1:** [1260, 1440] (21:00 – 23:59)
- **w_2:** [0, 360] (00:00 – 06:00)
- **func_time:** 480 minutes (8 hours)
- **func_cycle:** 150 minutes (Strict. The usage is massive and continuous, running in solid 7-hour blocks while the user rests or wakes early.)
- **occasional_use:** 0 (Extremely rare, once a month or less. This is not a daily habit, but rather an occasional practice driven by specific security concerns or comfort needs.)


### **Virtual Appliance 9: Radio Companionship & Phone Charging** 
- **Narrative:** For isolated elders, the radio and/or the phone serves as a critical socio-psychological lifeline, providing constant background noise, news, and virtual companionship. Mobile phones are used to communicate with family. These devices are occasionally charged at any tiem of they, when needed. The time of use of phones or radios is reduced mainly due to health problems related to vision and hearing. Regarding phones, simpler hardware is reported, compared with younger populations.
- **power:** 2 W (nominal power)
- **w_1:** [0, 1440] (00:00 – 23:59)
- **func_time:** 240 minutes (4 hours)
- **func_cycle:** 210 minutes (Changing cycles for the phones are around 3.5 hours, but the total daily time spent charging is estimated to be nearly 4 hours, spread across multiple cycles and devices (including mobile phones, flashlights, and radios))
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

According to observations, the energy consumption from the Solar Home Systems cannot vary significantly due to its technical limitations. However, seasonality is primarily friven by family mobility and the agricultural calendar. In the specific case of Profile 2, the isolated elderly, the energy consumption is not directly affected by the agricultural calendar, as they do not participate in farming activities. Instead, their energy use is more influenced by their daily routines and social practices, which remain relatively stable throughout the year. Something that potentially affects their energy consumption is the occasional visits from their migrated children, which can lead to temporary increases in energy use. These events can be tied to agricultural cycle since it has been reported that the migrated children return to the village during the harvest season to help with the work and to celebrate the festivals. However, these visits are not guaranteed and can vary from year to year, making it difficult to predict their impact on energy consumption. Overall, while seasonality plays a significant role in the energy consumption of agricultural households, it has a less pronounced effect on the isolated elderly, whose energy use is more consistent and less tied to external factors.

To represent the seasonality in the energy consumption of Profile 2, Virtual appliances 1-8 remain the same, while Virtual Appliance 9 (Radio Companionship & Phone Charging) is adjusted to reflect the potential increase in energy use during the harvest season when migrated children may visit. The occasional use parameter for this appliance can be increased during this period to account for the temporary increase in energy consumption due to social visits.
Parameters that change during the Growing and Early Harvest and Harvesting seasons (February-June) are as follows:
- **Virtual Appliance 9: Radio Companionship & Phone Charging**
    - func_time: 420 minutes (6 hours)