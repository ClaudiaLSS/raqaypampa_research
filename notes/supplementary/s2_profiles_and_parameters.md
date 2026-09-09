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

### **S2.3 Household classification tree**