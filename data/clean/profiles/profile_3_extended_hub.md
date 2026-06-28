# **Profile 3: Extended/Multi-tasking hub**

**Demographic summary:**  Households characterized by high occupancy, extended and multi-generational family structures, or functioning as central social hubs within the community. These households exhibit overlapping, parallel daily routines, leading to a phenomenon of "load stacking" where multiple physical devices are heavily utilized simultaneously. The energy demand is intense, consistent, and prolonged, reflecting a vibrant, multi-tasking domestic environment with significant communication and social activities.

### **The Driving Social Rules:**

-   **Rule 3 (The Gendered Anchor / Kitchen Dictate):** Extended cooking times are required to prepare meals for large groups (e.g., *mote* or *lawa*).

-   **Rule 12 (Community Override):** Normal energy conservation routines are suspended during community events or when relatives visit, causing stochastic spikes.
  
### **Energy Signature & Metric Thresholds:**

-   **Peak Hour (18:00 - 19:00):** The most brutal load curve in the dataset. The evening peak is sustained over longer durations.

-   **Night Safety Probability (High: 72% - 84.9%):** User 63 exhibits 84.9% safety light probability and User 69 exhibits 72.0%, indicating consistent overnight lighting for family safety.

-   **MRSD Chaos Index (Moderate: 0.887 - 1.298):** User 63 (0.887) and User 69 (1.298) show moderate predictability. The routine is structured around extended family activities.

-   **Relative Mean Power (Evening: \> 1.7x):** Extreme evening stress multipliers. For example, User 63\'s evening power draw is 1.758 times higher than their 24-hour baseline.

-   **Overall Mean Power (\> 1.20W):** High volumetric consumption (User 63: 1.93W; User 69: 1.22W) representing a heavy, continuous drain on the 89 Wh battery.

-   **Appliance Stacking Index (High: 27.1% - 35.3%):** User 63 exhibits 27.1% stacking and User 69 exhibits 35.3%, the highest recorded. Intense competition for USB ports and simultaneous multi-device usage defines this profile.

-   **Reliability & Blackouts:** Surprisingly high reliability (98-99%), suggesting these specific users have learned to tightly control their baselines despite the heavy loads, likely due to hardware resignation or the presence of secondary systems (as seen in User 69).

### **Appliance inventory:** 
- LED_1: Indoor light (main room)
- LED_2: Outdoor light 
- USB (phone chargers, radio charging and flashlight charging)

## **Daily social practices and anthropological windows**
*This section defines the socio-temporal envelopes that govern energy use for the Extended Hub profile. These are not periods of continuous power consumption; rather, they represent the broadest possible timeframes during which a specific social practice might occur. The RAMP algorithm is strictly constrained to generate the actual usage events only within these cultural boundaries.*

### Window 1: Morning preparation and staggered waking
**timeframe:** [300, 480] (05:00 – 08:00)
**Qualitative narrative:** The household experiences "staggered waking" with agricultural members rising pre-dawn for field preparation, followed by other family members preparing for the day and other morning activities. Some may leave the house for work or school, while others remain inside for breakfast and household chores. 
**Key social practices:** 
- Morning meal preparation
- Preparing children for school
- Brief morning tasks before leaving the house
- Preparing the tools for the day

### Window 2: Daytime activity and household traffic
**timeframe:** [480, 1020] (08:00 – 17:00)
**Qualitative narrative:** The household can be occupied throughout the day, with multiple members engaged in various tasks, including agricultural work, domestic chores, and social interactions. The main indoor space is rarely dormant.
**Key social practices:**
- Agricultural work
- Household chores
- Social interactions
- School attendance

### Window 3: Evening communal gathering and extended activity
**timeframe:** [1020, 1440] (17:00 – 23:59)
**Qualitative narrative:** The main indoor space serves as a highly active, communal gathering point well into the night. Activities such as dining, doing homework, socializing, and shared tasks stretch the illumination requirement.
**Key social practices:**
- Evening meal preparation and consumption
- Socializing and communal activities   
- Homework and study

### Window 4: Nighttime safety and security
**timeframe:** [0, 300] (00:00 – 05:00)
**Qualitative narrative:** With higher occupancy and more household assets, there is a strong, consistent need for overnight security and visibility. This light remains active through the entirety of the night and into the early morning, functioning as a continuous background load. However, it is not a daily practice.
**Key social practices:**
- Sleep
- Socializing and communal activities

## **Virtual Appliances formulation and parameterization**
*This section translates the social practices defined above into specific Virtual Appliances for the RAMP engine. It bridges the qualitative anthropological windows with the quantitative survey data.*

### **Virtual Appliance 1: Indoor task and communal morning light** 
- **Narrative:** The main indoor space is a hub of activity during the morning, with multiple family members preparing for the day. This light is used for specific tasks in darker corners of the home, or occasionally left on unintentionally due to the overlapping, chaotic routines of multiple family members moving through the space.

- **power:** 3 W (nominal power)
- **w_1:** [300, 480] (05:00 – 08:00)
- **func_time:** 90 minutes (1.5 hours)
- **func_cycle:** 70 minutes (Moderate. The start time is relatively stable, but the extended duration reflects a flexible social environment rather than a strict task-based schedule.)
- **occasional_use:** 0.42 (Casual/Seasonal, three times a week. It does not happen every day, suggesting this specific indoor morning routine might shift depending on the agricultural season or day of the week)

### **Virtual Appliance 2: Indoor occasional daytime light** 
- **Narrative:** Due to the high, continuous occupancy of this extended household (which may include infants, the elderly, or rotating agricultural workers returning for meals), the main indoor space is essentially never dormant. Daytime lighting in this profile is driven by "household traffic." It is utilized for specific tasks in darker corners of the home, or occasionally left on unintentionally due to the overlapping, chaotic routines of multiple family members moving through the space.


- **power:** 3 W (nominal power)
- **w_1:** [480, 1020] (08:00 – 17:00)
- **func_time:** 60 minutes (1 hour)
- **func_cycle:** 30 minutes (High Chaos. The start times and durations are highly unpredictable, scaling directly with the density of household traffic on any given day.)
- **occasional_use:** 0.42 (Rare / Intermittent, trice a week)

### **Virtual Appliance 3: Indoor evening light**
- **Narrative:** The main indoor space serves as a highly active, communal gathering point well into the night. Activities such as dining, doing homework, socializing, and shared tasks stretch the illumination requirement.

- **power:** 3 W (nominal power)
- **w_1:** [1020, 1380] (17:00 – 23:00)
- **func_time:** 180 minutes (3 hours)
- **func_cycle:** 150 minutes (Non-negotiable / Highly Strict. The usage is continuous and essential)
- **occasional_use:** 1 (daily)

### **Virtual Appliance 4: Indoor safety light** 
- **Narrative:** With higher occupancy and more household assets, there is a strong, consistent need for overnight security and visibility. This light remains active through the entirety of the night and into the early morning, functioning as a continuous background load. However, it does not accur every day, as it is not a daily practice.
- 
- **power:** 3 W (nominal power)
- **w_1:** [1380, 1440] (23:00 – 23:59)
- **w_2:** [0, 300] (00:00 – 05:00)
- **func_time:** 300 minutes (5 hours)
- **func_cycle:** 50 minutes (Strict / Continuous. When utilized, the light is left on for extremely long, uninterrupted blocks while the household sleeps.)
- **occasional_use:** 0.57 (Highly frequent, 4 times a week.)


### **Virtual Appliance 5: Outdoor transit morning light** 
- **Narrative:** In a high-occupancy extended household, outdoor morning activity is dense and multi-layered. Because the household experiences "staggered waking," there is a steady stream of pre-dawn exterior movement. Agricultural workers depart for the fields, older adults may perform early outdoor domestic chores (such as feeding livestock or organizing tools), and multiple individuals require transit lighting for latrine access. Consequently, this outdoor light acts as a critical infrastructural bridge, illuminating the high-traffic perimeter of the home. It is either left on continuously through the pre-dawn hours to support this steady egress, or it experiences multiple overlapping activation cycles.

- **power:** 2 W (nominal power)
- **w_1:** [330, 480] (05:30 – 08:00) (it starts a bit later than the indoor morning light, as the household first completes indoor preparation before moving outside)
- **func_time:** 60 minutes (1 hour)
- **func_cycle:** 50 minutes (Moderate Chaos. While the overall demand for outdoor illumination is a daily certainty, the exact timing and duration of each cycle fluctuate wildly based on the intersecting departure schedules of the various demographic cohorts within the home.)
- **occasional_use:** 0.42 (Highly Frequent, three times a week. It does not happen every day, suggesting this specific outdoor morning routine might shift depending on the agricultural season or day of the week.)


### **Virtual Appliance 6: Outdoor rare daytime light**
- **Narrative:** Not reported as a regular or daily habit. Not needed for standard agricultural work, but may be used during rare, specific daytime events (e.g., severe weather forcing outdoor tasks to be performed in low-light conditions, or a specific seasonal chore that requires outdoor illumination).
- **Anthropological window:** [480, 1020] (08:00 – 17:00)
- **Rigidity:** High Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.
- **Frequency:** Super rare / Intermittent

- **power:** 2 W (nominal power)
- **w_1:** [480, 1020] (08:00 – 17:00)
- **func_time:** 60 minutes (1 hour)
- **func_cycle:** 30 minutes (High Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.)
- **occasional_use:** 0.28 (Rare / Intermittent, twice a week)


### **Virtual Appliance 7: Outdoor social and transit light** 
- **Narrative:** The extended nature of the household means individuals frequently move between outbuildings, or neighbors/family visiting. This outdoor illumination supports these transient social interactions and inter-household mobility.
- **Anthropological window:** [1020, 1440] (17:00 – 23:59)
- **Rigidity:** Highly Variable. Driven entirely by the spontaneous flow of people in and out of the primary dwelling.
- **Frequency:** Frequent

- **power:** 2 W (nominal power)
- **w_1:** [1020, 1380] (17:00 – 23:00) 
- **func_time:** 90 minutes (1,5 hour)
- **func_cycle:** 30 minutes (Highly Variable. Driven entirely by the spontaneous flow of people in and out of the primary dwelling.)
- **occasional_use:** 1 (daily)

### **Virtual Appliance 8: Outdoor safety light** 
- **Narrative:** Not reported as a consistent, daily habit, but some families will occasionally leave an outdoor light on during the night for security or comfort. This is not active task lighting; it is a passive, continuous background load.

- **power:** 2 W (nominal power)
- **w_1:** [1380, 1440] (23:00 – 23:59)
- **w_2:** [0, 300] (00:00 – 05:00)
- **func_time:** 30 minutes (0.5 hours)
- **func_cycle:** 15 minutes (Moderate. It is used for very specific, brief tasks (e.g., checking on animals, securing doors) rather than continuous illumination.  )
- **occasional_use:** 0.28 (Intermittent, twice a week. It is not a daily habit, but rather a sporadic precautionary measure.)

### **Virtual Appliance 9: Stacked Phone & Radio Charging** 
- **Narrative:** Multiple adults and adolescents reside in or visit the home, leading to a constant queue for device charging. The household often utilizes physical splitters to charge multiple phones and power radios simultaneously, pushing the hardware to its absolute maximum wattage limit (5 W). The USB port is essentially never idle.
- **Anthropological window:** [0, 1440] (24 Hours)
- **Rigidity:** Continuous. The physical port experiences an unending cycle of devices being plugged in and swapped out throughout the day and night.
- **Frequency:** Daily

- **power:** 2 W (nominal power)
- **w_1:** [0, 1440] (00:00 – 23:59)
- **func_time:** 480 minutes (8 hours)
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

According to observations, the energy consumption from the Solar Home Systems cannot vary significantly due to its technical limitations. However, seasonality is primarily friven by family mobility and the agricultural calendar. In the specific case of Profile 3, the extended/multi-tasking hub, the energy consumption is directly affected by the agricultural calendar, as they participate in farming activities. The energy use is more influenced by their daily routines and social practices, which remain relatively stable throughout the year. However, during the harvest season, when there is a high demand for labor and families stay home to tend crops, there may be an increase in energy consumption due to the increased use of lighting and other appliances. Overall, while seasonality plays a significant role in the energy consumption of agricultural households, it has a less pronounced effect on the extended/multi-tasking hub, whose energy use is more consistent and less tied to external factors. Since families with this profile are multi-generational and extended, they may have more resources and support to manage the seasonal demands of agriculture, which can help to mitigate the impact of seasonality on their energy consumption. As a consequence, the experimented changes are similar to Profile 1. Virtual Appliances 1, 2, 3, 5, 6 and 7 will be parametrized with a lower occasional_use value during the Growing and Grazing season. The Virtual Appliances 4 and 8 will be parametrized with a the same occasional_use value as the baseline during the Growing and Grazing season. The Virtual Appliance 9 will be parametrized with a lower func_time value during the Growing and Grazing season.

Parameters that change during the Growing and Early Harvest and Harvesting seasons (February-June) are as follows:

- Virtual Appliance 1: Indoor task and communal morning light
    - occasional_use: 0.28 (Rare / Intermittent, twice a week)
- Virtual Appliance 2: Indoor occasional daytime light
    - occasional_use: 0.28 (Rare / Intermittent, twice a week)
- Virtual Appliance 3: Indoor evening light
    - occasional_use: 0.28 (Rare / Intermittent, twice a week)
- Virtual Appliance 4: Indoor safety light
    - occasional_use: 0.57 (Highly frequent, 4 times a week)
- Virtual Appliance 5: Outdoor transit morning light
    - occasional_use: 0.28 (Rare / Intermittent, twice a week)
- Virtual Appliance 6: Outdoor rare daytime light
    - occasional_use: 0.28 (Rare / Intermittent, twice a week)
- Virtual Appliance 7: Outdoor social and transit light
    - occasional_use: 0.28 (Rare / Intermittent, twice a week)
- Virtual Appliance 9: Stacked Phone & Radio Charging
    - func_time: 360 minutes (6 hours)             