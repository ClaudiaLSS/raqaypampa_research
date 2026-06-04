# **Profile 1: The educational and agriculture core**

**Demographic summary:** Nuclear and numerous families with working-age adults and school-aged children. Main economic activity is agriculture. The daily routine of these families consist on waking up early for preparing themselves to go to work to the fields and to prepare the children for school. Woman prepare food early to take and ead on the fields. Children come back to the house after school around 13:00 and head to the fields to help the parents. Once all go back to the house, the start doing homework and woman prepare food for diner around 18:00. These families exhibit a high valuation of education, often demonstrating strategic energy-rationing behaviors (load-shifting) to guarantee power availability for their children's evening studies. Flashlights use for night mobility is common. Leaving safety nights on during all night is moderate. Daytime use of energy is not common since they tend to be out of the household during the day.

**Appliance inventory:** 
- LED_1: Indoor light (main room)
- LED_2: Outdoor light 
- USB (phone chargers, radio charging and flashlight charging)

### **Virtual Appliance 1: Indoor task light for homework and dinner** 
- **Narrative:** This is the most critical and highly structured period of the household's energy demand. Beginning around 18:00, the main living space becomes a multi-use focal point. Because hardware is severely constrained—typically limited to only two lightbulbs for the entire household—the single main-room light is actively shared. Women utilize this centralized illumination for food preparation and dining (R3), while children simultaneously rely on it to complete their schoolwork (R1). Education is a profound priority; therefore, lighting during this window is considered absolutely non-negotiable. To guarantee sufficient battery capacity for this essential evening routine, families exhibit strategic load-shifting, consciously rationing their energy consumption throughout earlier parts of the day. This appliance gathers the family for inddor activities to end the day.
- **Anthropological window:** [1020, 1440] (17:00 – 23:59)
- **Rigidity:** Non-negotiable / Highly Strict. The usage is continuous and essential, meaning the coefficient of variation for the duration will be extremely low.
- **Frequency:** Daily

### **Virtual Appliance 2: Outdoor transit light** 
- **Narrative:** During the evening, family members move between structures (main room, secondary, latrine) or secure animals for the night. This light is used daily but operates in intermittent bursts rather than a continuous draw, reflecting transient outdoor movement rather than prolonged outdoor labor.
- **Anthropological window:** [1020, 1440] (17:00 – 23:59)
- **Rigidity:** Moderate. While the overall window is wide, the usage happens in distinct blocks (around 40 minutes at a time) as people move about before resting.
- **Frequency:** Daily

### **Virtual Appliance 3: Indoor safety light** 
- **Narrative:** To provide a sense of security or comfort during the night, families will sometimes leave a light on while sleeping. This is not active task lighting; it is a passive, continuous background load.
- **Anthropological window:** [0, 300] (00:00 – 05:00)
- **Rigidity:** Strict / Continuous. When utilized, the light is left on for extremely long, uninterrupted blocks while the household sleeps.
- **Frequency:** Intermittent. Used roughly half the time, likely dependent on external factors like weather, perceived security, or remaining battery state of charge.

### **Virtual Appliance 4: Indoor occasional daytime light** 
- **Narrative:** During standard agricultural workdays, indoor daytime electrical lighting is practically non-existent, as labor occurs predominantly outdoors and natural daylight suffices for basic indoor navigation. However, this baseline of zero-consumption is periodically interrupted by anomalous daytime events—such as severe weather (e.g., heavy rain forcing the family indoors), leaving devices charging while at work, periods of illness, or specific seasonal indoor chores (e.g., crop sorting, tool repair). Consequently, this energy load is fundamentally event-driven rather than routine-driven.
- **Anthropological window:** [480, 1020] (08:00 – 17:00)
- **Rigidity:** High Chaos. Because the usage is triggered by unpredictable external factors (weather, health, specific chores) rather than scheduled daily habits, both the start times and the durations will exhibit extreme variability.
- **Frequency:** Rare / Intermittent

### **Virtual Appliance 5: Indoor morning light** 
- **Narrative:** Pre-dawn waking for indoor preparation (gathering tools, preparing food for the day, preparing children for school, brief morning tasks) before leaving the house. The routine is quick and efficient.
- **Anthropological window:** [300, 480] (05:00 – 08:00)
- **Rigidity:** Strict. Bounded by sunrise.
- **Frequency:** Casual/Seasonal. It does not happen every day, suggesting this specific indoor morning routine might shift depending on the agricultural season or day of the week.


### **Virtual Appliance 6: Outdoor transit morning light** 
- **Narrative:** Similar to the indoor morning routine, this represents brief, pre-dawn outdoor chores (e.g., feeding animals, preparing equipment in the yard) before the sun provides adequate visibility.
- **Anthropological window:** [300, 480] (05:00 – 08:00)
- **Rigidity:** Strict. Bounded by the sunrise.
- **Frequency:** Casual/Seasonal

### **Virtual Appliance 7: Portable devices charging** 
- **Narrative:** Information and communication are constant background needs, recently increased for education purposes. Devices are plugged in opportunistically whenever power is available. Because charging is passive, it is entirely decoupled from strict human behavioral windows and occurs throughout the entire day.
- **Anthropological window:** [0, 1440] (24 Hours)
- **Rigidity:** [300, 420] (05:00 – 07:00)
- **Frequency:** Daily, drawing significant total daily time (nearly 8 hours of total charging spread across multiple cycles/devices including mobile phones, flashlights and radio).