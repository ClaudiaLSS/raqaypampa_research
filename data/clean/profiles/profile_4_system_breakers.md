# **Profile 4: System breakers**

**Demographic summary:**  Households defined by extreme behavioral irregularity, structural fragmentation, and high chaos. This profile likely represents transient workers, fragmented households managing split-location labor (R7, R9), or idividuals with non-traditional, unpredictable daily rhythms. Their routines completely defy standard agricultural or educational schedules. Consequently, their energy usage is sporadic, characterized by days of total dormancy punctuated by intense, unpredictable bursts of consumption. While basic activities are similar to profile one when users are present (wake up time, sleep, cooking, eating), household occupancy is an important factor for this profile. 

### **The Driving Social Rules:**

-   **Rule 7 (Infrastructure Mobility):** Extreme geographical isolation and seasonal agricultural work (\"monte\") force users to dismantle and transport the system.

-   **Rule 9 (The Aspiration Gap and Dual-Home Displacement):** Families maintain a bivocational lifestyle, delegating heavy energy tasks to a secondary, grid-connected home while treating the SHS home as a temporary base.

-   **Rule 13 (Hardware Resignation):** Minor failures (a snapped jack) lead to permanent appliance abandonment rather than repair.


### **Energy Signature & Metric Thresholds:**

-   **Peak Hour (18:00 - 20:00):** User 64 peaks at 19:00 while User 96 peaks at 20:00. Both show highly erratic timing due to nomadic patterns.

-   **Night Safety Probability (Low: 23.5% - 33.5%):** User 64 exhibits 33.5% and User 96 exhibits 23.5%. Minimal overnight safety lighting reflects their nomadic lifestyles and lower safety baseline priorities.

-   **MRSD Chaos Index (\> 2.00):** The defining mathematical signature of temporal migration. Both User 64 (2.394) and User 96 (3.016) exhibit maximum chaos. The load curve drops to absolute zero for weeks when the house is abandoned, followed by massive usage spikes when the user returns.

-   **Relative Mean Power (Extreme Peaks):** When they are home, their energy use is violent. User 64's evening routine requires 2.838x more power than her baseline average.

-   **Overall Mean Power (\< 0.70W):** Because the house is frequently empty, the 24-hour average is deceivingly tiny (User 64: 0.68W; User 96: 0.43W).

-   **Appliance Stacking Index (Moderate: 20.2% - 21.1%):** User 64 exhibits 21.1% stacking and User 96 exhibits 20.2%. Despite low overall consumption, simultaneous device usage occurs when households are occupied.

-   **Reliability & Blackouts:** High behavioral blackout rates relative to their low mean power (User 64: 1.56; User 96: 1.34). Because their demand timing is completely unpredictable, the battery cannot effectively pre-charge, resulting in frequent, behaviorally-induced Low Voltage Disconnects (LVD).


### **Appliance inventory:** 
- LED_1: Indoor light (main room)
- LED_2: Outdoor light 
- USB (phone chargers, radio charging and flashlight charging)

## **Daily social practices and anthropological windows**
*This section defines the socio-temporal envelopes that govern energy use for the System breakers profile. These are not periods of continuous power consumption; rather, they represent the broadest possible timeframes during which a specific social practice might occur. The RAMP algorithm is strictly constrained to generate the actual usage events only within these cultural boundaries.*

### Window 1: Morning preparation  
**timeframe:** [300, 480] (05:00 – 08:00)
**Qualitative narrative:** Pre-dawn waking for indoor preparation (gathering tools, preparing food for the day, preparing children for school, brief morning tasks) before leaving the house. The routine is quick and efficient. Indoor lighbulb use is limited to brief, task-specific illumination. Outdoor lighting is used for brief, pre-dawn outdoor chores before the sun provides adequate visibility. These activities are not daily habits, but rather sporadic, irregular events that occur only when the household is occupied.
**Key social practices:**
- Preparing food for the day
- Preparing children for school
- Brief morning tasks before leaving the house
- Preparing the tools for the day

### Window 2: Daytime agricultural work and school attendance
**timeframe:** [480, 1020] (08:00 – 17:00)
**Qualitative narrative:** During standard agricultural workdays, indoor daytime electrical lighting is practically non-existent, as labor occurs predominantly outdoors and natural daylight suffices for basic indoor navigation. However, this baseline of zero-consumption is periodically interrupted by anomalous daytime events—such as severe weather (e.g., heavy rain forcing the family indoors), leaving devices charging while at work, periods of illness, or specific seasonal indoor chores (e.g., crop sorting, tool repair). Consequently, this energy load is fundamentally event-driven rather than routine-driven. Normally, system breakers have other kind of jobs that do not depend on the agricultural schedule, and they may be absent from the household for days or weeks at a time. When they are home, they may engage in agricultural work, but it is not a daily habit. Or they may return home to perform important agricultural tasks.
**Key social practices:**
- Agricultural work
- School attendance

### Window 3: Evening core gathering and education
**timeframe:** [1020, 1440] (17:00 – 23:59)
**Qualitative narrative:** This is the most critical and highly structured period of the household's energy demand. Beginning around 18:00, the main living space becomes a multi-use focal point. Because hardware is severely constrained—typically limited to only one lightbulb for the entire household—the single main-room light is actively shared and an outdoor lighting is used for brief, essential nighttime movement between structures (main room, secondary, latrine) or to secure animals for the night. As in the last window, this period is not a daily habit, but rather a sporadic, irregular event that occurs only when the household is occupied. The evening routine is highly structured and socially coordinated, with specific tasks and activities occurring in a predictable sequence. However, the timing of these activities is highly variable and dependent on the household's specific circumstances (e.g., work schedules, school attendance, social obligations).
**Key social practices:**
- Food preparation and dining
- Homework and study    
- Socializing

### Window 4: Nighttime sleep and pasive security
**timeframe:** [0, 300] (00:00 – 05:00)
**Qualitative narrative:** To provide a sense of security or comfort during the night, families will sometimes leave a light on while sleeping. This is not active task lighting; it is a passive, continuous background load. However, staying up during this period is not common, and the light is often turned off for sleep. The household may also use outdoor lighting for brief, essential nighttime movement between structures (main room, secondary, latrine) or to secure animals for the night. As in the last window, this period is not a daily habit, but rather a sporadic, irregular event that occurs only when the household is occupied.
**Key social practices:**
- Sleep

## **Virtual Appliances formulation and parameterization**
*This section translates the social practices defined above into specific Virtual Appliances for the RAMP engine. It bridges the qualitative anthropological windows with the quantitative survey data.*

### **Virtual Appliance 1: Indoor morning light** 
- **Narrative:** Pre-dawn waking is not a normalized, daily requirement for this household. It occurs sporadically, likely tied to specific, irregular labor demands or travel needs rather than a steady agricultural routine.

- **power:** 3 W (nominal power)
- **w_1:** [300, 420] (05:00 – 07:00)
- **func_time:** 90 minutes (1.5 hours)
- **func_cycle:** 60 minutes (1 hour, strict. Bounded by sunrise.)
- **occasional_use:** 0.42 (Casual/Seasonal, three times a week. It does not happen every day, suggesting this specific indoor morning routine might shift depending on the agricultural season or day of the week)

### **Virtual Appliance 2: Indoor occasional daytime light** 
- **Narrative:** Because this demographic operates entirely outside of standard community diurnal rhythms, their use of daytime lighting is fundamentally anomalous. It may represent a transient worker returning home at unpredictable hours, someone resting during the day and requiring brief light upon waking, or entirely fragmented, non-traditional behavioral spikes. It completely lacks a cohesive routine.

- **power:** 3 W (nominal power)
- **w_1:** [420, 1020] (07:00 – 17:00)
- **func_time:** 60 minutes (1 hour)
- **func_cycle:** 30 minutes (Extreme Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.)
- **occasional_use:** 0.28 (Rare but volatile)
  
### **Virtual Appliance 3: Erratic indoor evening task light** 
- **Narrative:** While the household generally requires lighting in the evening, the timing and duration are entirely disconnected from standard community norms. Return times fluctuate wildly, and the light may be used for brief, hurried tasks one night, and extended periods the next.

- **power:** 3 W (nominal power)
- **w_1:** [1020, 1320] (17:00 – 22:00)
- **func_time:** 120 minutes (2 hours)
- **func_cycle:** 100 minutes (Non-negotiable / Highly Strict. The usage is continuous and essential)
- **occasional_use:** 1 (daily)

### **Virtual Appliance 4: Indoor safety light** 
- **Narrative:** The use of overnight security lighting is inconsistent. It may be deployed only during specific circumstances—such as when a household member is away traveling, or during periods of perceived vulnerability—rather than as a daily habit.

- **power:** 3 W (nominal power)
- **w_1:** [1320, 1440] (22:00 – 23:59)
- **w_2:** [0, 300] (00:00 – 05:00)
- **func_time:** 360 minutes (6 hours)
- **func_cycle:** 100 minutes (Highly Variable. The blocks of use are long, but the implementation is erratic.)
- **occasional_use:** 0.43 (Intermittent. Used roughly three times a week, likely dependent on external factors like weather, perceived security, or remaining battery state of charge.)


### **Virtual Appliance 5: Erratic Outdoor transit morning light** 
- **Narrative:** Because this demographic operates entirely outside of standard community diurnal rhythms, pre-dawn outdoor movement is fundamentally anomalous. They lack the stable, daily anchors of communal agricultural shifts or school departures. If this exterior light is utilized during the early morning, it is driven by highly irregular events—such as a transient worker departing for a multi-day off-grid job, an unpredictable return from travel, or a fragmented, non-traditional labor shift. Consequently, this appliance usage completely defies the cohesive, daily cadence observed in standard farming households.

- **power:** 2 W (nominal power)
- **w_1:** [330, 480] (05:30 – 08:00) (it starts a bit later than the indoor morning light, as the household first completes indoor preparation before moving outside)
- **func_time:** 60 minutes (1 hour, )
- **func_cycle:** 50 minutes (Extreme Chaos. There is absolutely no underlying pattern to its implementation. Start times, when they do occur, are wildly unpredictable and unanchored to sunrise or community norms.)
- **occasional_use:** 0.33 (Rare ans sporadic)



### **Virtual Appliance 6: Outdoor evening transit light** 
- **Narrative:** Outdoor evening movement is extremely minimal or actively avoided. The light is essentially abandoned, used only during rare, specific emergencies or highly unusual late-night tasks.

- **power:** 2 W (nominal power)
- **w_1:** [420, 1020] (07:00 – 17:00)
- **func_time:** 60 minutes (1 hour)
- **func_cycle:** 30 minutes (High Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.)
- **occasional_use:** 0.14 (Rare / Intermittent, once a week)



### **Virtual Appliance 7: Burst Phone & Radio Charging (USB)** 
- **Narrative:** Unlike the daily charging habits of other profiles, these users interact with their devices sporadically. A device may be allowed to completely die, or the user may return from a multi-day absence, resulting in intense, prolonged "burst" charging sessions to replenish deeply depleted batteries, followed by days of zero USB usage.

- **power:** 2 W (nominal power)
- **w_1:** [0, 1440] (00:00 – 23:59)
- **func_time:** 420 minutes (7 hours)
- **func_cycle:** 180 minutes (Changing cycles for the phones are around 3 hours, but the total daily time spent charging is estimated to be nearly 8 hours, spread across multiple cycles and devices (including mobile phones, flashlights, and radios).)
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

According to observations, the energy consumption from the Solar Home Systems cannot vary significantly due to its technical limitations. However, seasonality is primarily friven by family mobility and the agricultural calendar. In the specific case of Profile 4, the system breakers, since they tend to have a chaotic life, employing double household strategies or not having agriculture as the main mean of livelihood, the energy consumtion is affected by the agricultural calendar, as they may be absent from the household for extended periods during the planting, growing, and harvesting seasons. When they are home, they may engage in agricultural work, but it is not a daily habit. Or they may return home to perform important agricultural tasks. Overall, while seasonality plays a significant role in the energy consumption of agricultural households, it has a less pronounced effect on the system breakers, whose energy use is more consistent and less tied to external factors. In this sense, contrary to the case of Profile 1, the activity withinh the household may increase during planting and harvesting seasons, but it is not guaranteed that they will be home during these periods which add even more chaos to the energy profile. Virtual appliances may increase occacional_use during these periods and phone charging increases also the func_time. 

Parameters that change during the Planting and Harvesting seasons:
- **Virtual Appliance 1: Indoor morning light**
    - occasional_use: 0.55 (Casual/Seasonal, three times a week. It does not happen every day, suggesting this specific indoor morning routine might shift depending on the agricultural season or day of the week)
- **Virtual Appliance 2: Indoor occasional daytime light**
    - occasional_use: 0.35 (Rare but volatile)
- **Virtual Appliance 3: Erratic indoor evening task light**
    - occasional_use: 1 (daily)
- **Virtual Appliance 4: Indoor safety light**
    - occasional_use: 0.55 (Intermittent. Used roughly three times a week, likely dependent on external factors like weather, perceived security, or remaining battery state of charge.)    
- **Virtual Appliance 5: Erratic Outdoor transit morning light**
    - occasional_use: 0.45 (Rare ans sporadic)
- **Virtual Appliance 6: Outdoor evening transit light**
    - occasional_use: 0.25 (Rare / Intermittent, once a week)
- **Virtual Appliance 7: Burst Phone & Radio Charging (USB)**
    - func_time: 480 minutes (8 hours)