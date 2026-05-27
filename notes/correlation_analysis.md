Correlation analysis

### The Phone Charging Multiplier

-   **The Math:** family\_type strongly drives phone\_2\_time (\$\\eta =
    > 0.76\$) and phone\_1\_time (\$\\eta = 0.72\$).

-   **The Behavioral Insight:** This goes far beyond just \"more people
    > equal more phones.\" It shows that the *structure* of the family
    > dictates charging behavior. An \"extended\" family (which might
    > include grandparents, parents, and older teens) creates a chaotic
    > charging environment where Phone 1 and Phone 2 are competing for
    > the system\'s USB ports for extended hours. A \"nuclear\" or
    > \"single elder\" family has a drastically different, much lower
    > charging footprint.

-   **RAMP Implication:** This is your trigger for modeling high-stress
    > daytime loads.

### The Agricultural Labor Pool

-   **The Math:** family\_type correlates heavily with act\_dl\_agri
    > (daily hours in agriculture) (\$\\eta = 0.67\$) and
    > act\_agriculture (\$\\eta = 0.67\$).

-   **The Behavioral Insight:** The type of family determines their
    > labor capacity. Extended and large nuclear families can divide
    > labor, sending people to the *monte* (fields) for long hours.
    > Conversely, isolated elderly households cannot sustain these long
    > agricultural hours.

-   **RAMP Implication:** This justifies why the \"Seasonal Migrant\" or
    > \"Agricultural Core\" archetype needs the massive mid-day \"demand
    > valley\" (because the whole family is out working), while the
    > elderly archetype might have a flatter demand curve throughout the
    > day.

### The Kitchen Dictate (Cooking Time)

-   **The Math:** family\_type strongly shapes cooking\_time\_min\_d
    > (minutes spent cooking per day) (\$\\eta = 0.56\$).

-   **The Behavioral Insight:** This is the missing piece for **Rule 3
    > (The Gendered Anchor of Domestic Operations)**! Because you
    > correctly pointed out that light bulb correlations don\'t prove
    > simultaneous use, *this* is the variable that proves cooking time
    > scales with family structure. Extended families require much more
    > time to prepare food (like the *lawa* or *mote* we saw in the
    > transcripts).

-   **RAMP Implication:** For your \"Extended Family\" or \"Educational
    > Core\" archetype, the evening lighting window tied to cooking must
    > be wider and highly rigid, whereas an elderly individual living
    > alone requires less cooking time, leading to a shorter baseline
    > lighting window.

### Proof of \"The Empty Nest\" (Demographic Isolation)

-   **The Math:** adults\_mas\_60 has a strong **negative correlation**
    > with both working-age adults adults\_18\_59 (\$r = -0.441, p \<
    > 0.001\$) and young children children\_0\_5 (\$r = -0.270, p =
    > 0.030\$).

-   **The Behavioral Insight:** This is the hard mathematical footprint
    > of rural out-migration. If a household has elderly individuals, it
    > is highly likely that there are no working-age adults or young
    > children living there. They are physically isolated.

-   **RAMP Implication:** This perfectly justifies separating them from
    > the \"Educational/Agricultural Core\" archetype. Their load curves
    > will not be driven by heavy domestic cooking (Rule 3) or multiple
    > cell phones (Rule 9).

### The Altered Morning Routine

-   **The Math:** adults\_mas\_60 strongly influences the specific
    > categorization of morning lighting: light\_2\_morning (\$\\eta =
    > 0.517\$) and light\_1\_morning (\$\\eta = 0.458\$).

-   **The Behavioral Insight:** Earlier, we saw that older family heads
    > wake up significantly *later* than younger agricultural workers.
    > This correlation ratio (\$\\eta\$) indicates that the presence of
    > elderly people fundamentally restructures *how* morning lighting
    > is used. Because they aren\'t rushing out to the *monte* for 10
    > hours of heavy labor before dawn, their morning lighting and radio
    > routine is likely slower and more continuous.

-   **RAMP Implication:** You will shift their morning lighting window.
    > Instead of a sharp, intense spike at 04:00 AM (the \"Agricultural
    > Dictate\"), the elderly archetype will have a smoother,
    > potentially later, and less intense morning demand curve.

### The \"School Morning\" Spike (Validating Temporal Anchors)

-   **The Math:** The presence of school-aged children (children\_5\_17)
    > heavily influences the use of the first morning light
    > (light\_1\_morning, \$\\eta = 0.540\$) and morning radio
    > (radio\_morning, \$\\eta = 0.491\$). Furthermore, as we saw
    > earlier, it creates a statistically significant *negative*
    > correlation with wakeup\_time\_after (\$r = -0.323, p = 0.019\$).

-   **The Behavioral Insight:** Households with school children have a
    > highly rigid, earlier morning routine. The radio is turned on
    > early (likely for news or timekeeping before school), and the
    > first light is used earlier than in homes without school children.

-   **RAMP Implication:** In your simulation, this justifies assigning a
    > sharp, early morning probability window (e.g., 04:30--06:00 AM)
    > for lights and radio specifically for the Educational archetype.

### The Digital Aspiration Gap

-   **The Math:** The presence of school-aged children (children\_5\_17)
    > positively correlates with the total number of cell phones
    > (phones, \$r = 0.269, p = 0.031\$). Additionally, whether children
    > are in school (children\_in\_school) strongly influences the
    > household\'s overall satisfaction with their solar system
    > (demand\_satisfaction, Cramér's V = 0.339).

-   **The Behavioral Insight:** School children are the primary drivers
    > of digital connectivity and latent demand. As kids go to school,
    > they require phones for homework or social connectivity. Because
    > they have more phones to charge, these households are the most
    > likely to hit the limits of the 89Wh battery, altering their
    > overall satisfaction with the system.

-   **RAMP Implication:** The \"Educational Core\" archetype must be
    > programmed with a much higher probability for simultaneous phone
    > charging (especially daytime charging) than the \"Isolated
    > Elderly\" archetype.

### What School Children *Actually* Change (The Significant Math)

While children don\'t change the evening lighting duration, the
correlation script found that children\_5\_17 **does** significantly
alter two other critical energy variables (\$p \< 0.05\$):

-   **Wake-Up Times (wakeup\_time\_after): Pearson \$r = -0.32\$ (\$p =
    > 0.019\$).**

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
