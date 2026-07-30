# Profile 1: The Educational and Agricultural Core — RAMP truth file (protocol-applied)

> Derivation authority: `parameter_derivation_protocol.md` (§3.3.1.1). Every parameter below carries its
> derivation tag — **[SPEC]**, **[WINDOW]**, **[FREQ-XW]**, **[RIG-XW]**, **[RIG-XW → func_time]**,
> **[DECLARED DEFAULT]** — and a `— source:` provenance trailer. No value is left without a declared basis.

```
Population: N_survey = 28 (ids 6, 8, 16, 17, 19, 20, 21, 26, 28, 32, 34, 44, 51, 53, 58, 62, 63, 72, 74,
            80, 81, 83, 88, 90, 94, 95, 99, 100; classified via family_type/occupation/
            children_in_school/migration/portability_shs, per `classifications_oficial.csv`.
            Ids 58 and 83 are held in Profile 1 by an analyst override rather than the official source,
            which places both in Profile 4 — see §8.)
            N_interview = 18 (Antonio Negrete 6, Arminda Reyes 8, Domingo Vallejos 19,
            Edelfrida Jiménez Salazar 20, Vicente Tapia Sanchez 44 [respondent: Natividad Sánchez,
            esposa], Albino Acosta 58, Calixto Negrete 62, Carlos Negrete 63, Guillermo Negrete 72
            [respondent: Teresa Claros, esposa], José Acosta Inturias 74, Miguel Meneses 80,
            Moises Acosta 81, Pascual Zurita 83, Vicente Inturias 88, Adrian Felipes 90, Eugenia
            Chambi 94, Guillermo Cordova 95, Olimpio Cordova 99. Not interviewed: ids 16, 17, 21,
            26, 28, 32, 34, 51, 53, 100.)
            Coverage 64% (18/28) — second-highest of the four profiles.
Generalization: all qualitative parameters below (Windows, Rigidity, occasional_use, and
Extreme/Structural bin assignment) are inferred from N_interview and applied uniformly to all
N_survey households at simulation time. There is no survey-only shortcut for any of these —
dual-household/structural-absence status requires interview evidence, the same as ordinary
timing and frequency parameters; `migration_label` is not used as the trigger, since it is true
for 9 of 28 households here without discriminating a genuine dual-residence pattern from
ordinary short-term labor migration by one member.
```

---

## Methodological basis

The hardware is two indoor bulbs' worth of light plus one outdoor fixture: **LED_1** (indoor, main room,
3 W) carries the profile's load-bearing evening and night practices; **LED_2** (outdoor, transit/yard
light, 2 W) carries brief pre-dawn and evening movement between structures. Daytime indoor light (VA2)
is real but event-driven rather than routine — the household is empty during standard fieldwork hours,
and use is anomalous (weather, illness, a device left charging) rather than a describable pattern, so it
is Chaos rather than a quantified conditional trigger: weather was never collected as a systematically
measured study variable, and a nameable-but-unmeasured cause receives the same treatment under the
protocol as a practice with no describable pattern at all. Daytime and overnight *outdoor* light (VA6,
VA8) carry no parameters at all: no respondent reports either practice, and using an exterior light in
full sun or during uneventful sleep hours has no plausible logic for a conservation-oriented household —
a hard zero is the evidenced output, not a gap to paper over. The resulting window-continuity gap this
would otherwise leave in the indoor-light schedule is closed by widening VA2's own window by one hour
(07:00–18:00 instead of 07:00–17:00) rather than by inventing a placeholder outdoor VA; the outdoor
schedule (VA5–VA7) needs no such fix, since VA6/VA8's silence sits between two functioning VAs without
leaving any hardware un-modeled.

The profile's one non-negotiable load is the evening indoor light (VA3): women prepare and serve dinner
while children do homework under the same bulb, and this is treated as a priority override
(`occasional_use = 1.0`, unchanged across seasons) rather than a frequency-crosswalk value, because
school attendance is a constraint on the household's behavior, not a target of seasonal variation. A
minority — 3 of 18 interviewed households — additionally leave an indoor light on through the night with
no stated cause (VA4); as in Profile 2, this is modeled as flat household-level heterogeneity, adequate
only because Tier 2 validation runs on the profile-averaged curve. Productive night work (weaving,
spinning) is explicitly *not* done under the SHS light in this profile — three independent households
describe doing this work outdoors or in daylight instead, citing the light's insufficient brightness for
fine handwork, not an external cause like moth damage. `func_time` throughout is derived via
`window_width × (1 − random_var_w)` (Protocol §3) except where a VA is explicitly Chaos/event-driven
within a wide window, in which case the margin formula would wrongly imply near-continuous use and a
narrative duration is used instead (VA2). VA9 (charging) carries `thermal_P_var = 0.3` **[DECLARED
DEFAULT]** per Protocol §9, reflecting CC-CV taper compounded by this profile's mixed device inventory
(feature phones, radios, flashlights sharing the same 5V supply).

One household — José Acosta Inturias (74) — describes a seasonal second residence with its own separate
panel, used for roughly a month each year: the survey's `migration` field records this household as
non-migrating (`migration = 0`), which the interview directly contradicts. This is the profile's only
account of anything resembling structural dual-residence, it is thin (a single respondent, one
recurring month), and it is not built into any VA parameter here — see §8.

---

## 1. Demographic summary

Nuclear and extended families with working-age adults and school-aged children, predominantly classified
as agricultural or domestic-labor households (`occupation` 1 or 2 for 27 of 28; id 88 unclassified). All
but three households (58, 83, 88 — `children_in_school = 0`) have at least one child currently in
school, which is the profile's defining structural feature and the anchor for its name. The daily
routine centers on waking before dawn to prepare for fieldwork and school: women prepare breakfast and
pack the midday meal, children are readied for school, and the household empties out shortly after first
light. Children return from school around 13:00 and rejoin fieldwork; by evening the whole household
regroups for a single, dense period of cooking, homework, and family time before an early bedtime.

These families exhibit a high valuation of education, often demonstrating strategic energy-rationing
behavior (load-shifting earlier in the day) to guarantee power availability for their children's evening
studies. Flashlight use for night mobility is common, and leaving a safety light on overnight is a real
but household-specific minority practice, not a universal one. Daytime energy use is uncommon, since
households are typically away from the home during standard working hours. The profile's conservation
orientation extends to a full transition away from pre-SHS lighting: *"Antes usaba todo el tiempo
mechero; ahora ya no… Lo hemos botado"* (Albino Acosta, 58); *"Antes siempre usábamos vela para
alumbrarnos. Teníamos que ahorrar y gastar con cuidado la vela"* (Arminda Reyes, 8).

Sedentary residence is the norm — *"nosotros no vamos a ningún lado; aquí vivimos siempre"* (Arminda
Reyes, 8); *"todo el año nos quedamos aquí"* (Adrián Felipes, 90) — with `migration = 1` in 9 of 28
households describing an individual member's temporary labor absence (the household and its SHS stay
put) rather than a household-level relocation. The one documented exception — José Acosta Inturias (74),
whose household maintains and uses a second panel at a second residence for part of the year — is
addressed in §8 rather than folded into this generalization, since it is a single, thin account that the
survey's own `migration` field failed to capture for this household.

---

## 2. The driving social rules

- **Rule 1 — The Educational Anchor.** The evening lighting window is non-negotiable for homework: *"la
  necesitamos cada día por las noches; los chicos van haciendo sus tareas"* (Natividad Sánchez, esposa
  of household head Vicente Tapia Sanchez, 44, 24/02/2026); *"la luz es muy elemental para que realicen
  sus tareas"* (Edelfrida Jiménez Salazar, 20, 26/02/2026); *"Uno nomás [está en el colegio]. El otro ya
  irá al año"* (Albino Acosta, 58) — corroborating that school attendance, not merely its possibility, is
  what anchors the rule. **Model consequence:** drives the priority override on VA3's `occasional_use`
  (1.0, unchanged across seasons — school attendance constrains absence rather than being a target of
  it).
- **Rule 2 — The Agricultural Dictate.** "Sun-up to sun-down" labor creates an early wake-up and a
  daytime demand valley: *"nosotros no paramos en casa; siempre nos vamos al trabajo de campo"*
  (Edelfrida Jiménez Salazar, 20); *"Desde las 9 de la mañana ya empiezo a salir y regresamos como a las
  3 o 4 de la tarde"* (José Acosta Inturias, 74). **Model consequence:** grounds Window 2's structural
  (non-triangulated) daytime-empty bound and VA2's Chaos classification — there is no routine indoor
  daytime practice for the model to anchor to.
- **Rule 3 — The Gendered Anchor of Domestic Operations.** Women control the kitchen and the strict
  lighting requirement during evening meal preparation. Anchor quote as Rule 1 (Natividad Sánchez, shared
  evidence base); corroborated indirectly by Adrián Felipes' household, where the light is used
  specifically for his mother's cooking rather than her own charging needs (*"su luz nomas tiene, para
  cocinar usa"*, 90). **Model consequence:** feeds the same VA3 priority override as Rule 1 — the two
  rules are evidentially inseparable in this profile (same window, same respondents, same non-negotiable
  framing), which is why they share a single `occasional_use` treatment rather than being modeled as
  independent pressures.
- **Rule 15 — The Productive Lighting Veto.** Fine handwork (weaving, spinning wool) is done outdoors or
  in daylight, not under the SHS light, because the light is not bright enough for it — not because of an
  external cause like moth damage. *"No, durante el día tejemos; no utilizamos la luz... en la mañana
  nomás hilamos la lana"* (José Acosta Inturias, 74); *"yo no realizo ninguna actividad con la luz porque
  no es tan nítido. Si hago mis tejidos, siempre los estoy haciendo afuera"* (Teresa Claros, esposa of
  household head Guillermo Negrete, 72); *"No, no… nada. Ningún trabajo realizamos"* (Arminda Reyes, 8).
  Three independent households, consistent account. **Model consequence:** restricts productive labor to
  daylight hours, outside any modeled VA window — this is why VA3's evening load is exclusively
  homework/cooking rather than also carrying a task-lighting component, unlike what a generic "evening
  light" appliance might assume.

---

## 3. Appliance inventory — [SPEC]

| Device   | Count (survey, n=28)                                                                                                                 | Placement                          | Power                         |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- | ----------------------------- |
| LED_1    | 2 bulbs in 26/28 hh; 1 bulb (id 20 — conflicts with her own interview account of two, see below); 0 recorded (id 88, thin interview) | Main room (indoor)                 | 3 W                           |
| LED_2    | paired with LED_1 in the same 26/28 hh                                                                                               | Yard / transit point (**outdoor**) | 2 W                           |
| Radio    | present in 17/28 hh; absent in 11/28                                                                                                 | —                                  | folded into VA9 where present |
| USB port | phone(s) in 23/28 hh (0 phones: ids 16, 58, 80, 90, 100); flashlight                                                                 | —                                  | 3 W                           |

**Hardware is reduced in a visible minority of households**, not just missing outright: Adrián Felipes
(90) describes actively removing a second bulb rather than merely never owning one — *"solo uno nomas el
otro lo saque, porque no mantiene los dos"* — because the system could not sustain both. Edelfrida
Jiménez Salazar's survey record shows one bulb (`light_bulbs = 1`) despite her own interview statement
of two (*"Dos focos estamos usando"*, 20) — a direct data/interview conflict, left unresolved here and
flagged in §8 rather than silently picked one way. Ownership does not guarantee simultaneous use: *"Para
dos celulares no abastece; solo abastece para uno"* (Edelfrida Jiménez Salazar, 20) — households with
two phones frequently ration to charging one at a time, a constraint not separately modeled (per stated
decision, VA9 treats `number` as device count, not simultaneity).

---

## 4. Daily social practices and anthropological windows

*These are the socio-temporal envelopes within which RAMP may place events — not periods of continuous
consumption. Appliance-level detail (which light, how rigid the use is) lives in §5, not here.*

> **Modal code, defined once.** The survey does not record clock times for lighting; it records a
> **categorical period code** — `light_1_night`, for example, offers 13 pre-set windows (code 3 =
> 18:00–19:00, code 6 = 18:00–22:00, code 13 = 18:00–05:00, and so on), and each respondent picks one.
> The **modal code** is the code most respondents actually chose, taken whole, bounds and all — not a
> median or average of window widths, which would manufacture a window no respondent reported. Windows
> below are grounded this way per Protocol §3, with the crossing tier (nested / overlapping / no overlap)
> setting `random_var_w`: nested sources → high confidence (~0.1–0.2), overlapping-but-not-nested →
> moderate (~0.2–0.3), no overlap → low confidence, survey wins ties (~0.3–0.4).

### Window 1 — Morning agricultural and school preparation (04:00 – 08:00) → `[300, 480]`

Pre-dawn waking. Household members gather tools and prepare food to carry to the fields; women prepare
breakfast and pack the midday meal, children are readied for school. The routine is quick, and the
household empties out shortly after first light.

**Grounding (nested → high confidence):** survey `wakeup_time_after` (n=25 of 28 valid): mode 04:00
(15/25, 60%), mean ≈4:29, tail to 06:00 (2/25); corroborated by interview, including Pascual Zurita's
*"Prendo por la noche a las 6 de la tarde, y en las madrugadas a las 4 de la mañana"* (83), which sits
exactly on the survey mode.

*Practices: preparing food for the day, preparing children for school, gathering tools and equipment,
brief pre-dawn outdoor chores (tending animals) before leaving the house.*

### Window 2 — Daytime agricultural work and school attendance (08:00 – 17:00) → `[480, 1020]`

The household is largely empty during the standard workday: adults are in the fields, children are at
school. This is the profile's daytime demand valley (Rule 2). The routine is occasionally interrupted by
severe weather, illness, or seasonal indoor chores (crop sorting, tool repair), but these are anomalous,
not part of the standard daily pattern.

**Grounding (structural, not independently triangulated):** unlike Windows 1, 3, and 4, no survey period
code or interview duration statement directly targets daytime hours — daytime light use is expected to
be near-zero and wasn't asked about as a routine practice. The bound is set as the complement of Window
1's end and Window 3's start, anchored to Rule 2 ("sun-up to sun-down" labor) and physical daylight
bounds. *"Nosotros no paramos en casa; siempre nos vamos al trabajo de campo"* (Edelfrida Jiménez
Salazar, 20); *"Desde las 9 de la mañana ya empiezo a salir y regresamos como a las 3 o 4 de la tarde"*
(José Acosta Inturias, 74) — both consistent with, though not independently anchoring, the 08:00–17:00
bound. Read as a lower-confidence, structurally-derived window relative to Windows 1, 3, and 4.

*Practices: agricultural fieldwork, school attendance, occasional at-home indoor activity triggered by
weather, illness, or seasonal chores.*

### Window 3 — Evening core gathering and education (17:00 – 24:00) → `[1020, 1440]`

The most socially dense period of the household's day. Beginning around 18:00, the main living space
becomes a multi-use focal point: women prepare and serve dinner (Rule 3) while children do homework in
the same space (Rule 1) — a non-negotiable gathering, since education is a profound family priority.
Family members also move briefly between structures or step out to secure animals for the night.

**Grounding (nested → high confidence):** survey `light_1_night` modal code (n=28): **18:00–22:00 (code
6), 8/28 households (29%)** — the single most common code, not a width average — independently
corroborated by five interview accounts converging on the same span: *"la necesitamos cada día por las
noches; los chicos van haciendo sus tareas"* (Natividad Sánchez, 44); *"Hago alumbrar desde las 6 de la
tarde hasta las 10 de la noche"* (Carlos Negrete, 63); *"desde las 6 de la tarde hasta las 10 de la
noche; no amanezco con la luz prendida"* (José Acosta Inturias, 74); *"A partir de las 6 o 7 hasta las 10
de la noche, algo así; ocupamos siempre la luz"* (Calixto Negrete, 62); *"desde las 6 de la tarde hasta
las 10 de la noche"* (Pascual Zurita, 83); *"por las noches desde las 6:00 a las 10:00 p.m."* (Edelfrida
Jiménez Salazar, 20). Six independent interview accounts landing on the same span is the tightest
survey×interview convergence in this profile.

*Practices: food preparation and family dinner, homework and study, family socializing, brief movement
between structures / securing animals for the night.*

### Window 4 — Nighttime sleep and passive security (00:00 – 05:00) → `[0, 300]`

The household sleeps. For a minority this is accompanied by a passive comfort/security practice, but
staying awake through this period is not common — most households simply go dark for the night.

**Grounding (overlapping, not nested → moderate confidence):** survey `sleep_time_after` (n=25 of 28):
mode 22:00 (12/25), tail to 24:00 (4/25) — most households are asleep well before midnight, so Window
4's 00:00 start captures uncontested sleep continuing from Window 3's tail. The 05:00 end is anchored to
`wakeup_time_after` (n=25): mode 04:00 (15/25), tail to 06:00 (2/25) — this tail, extending past Window
4's own bound into Window 1, is what sets the crossing tier to overlapping rather than nested. *"Ahora
duermen como a las 9:00 o 10:00 de la noche"* (Domingo Vallejos, 19) sits inside Window 3's tail rather
than Window 4 itself, consistent with the survey mode. Indirect corroboration: VA4's overnight-light
quotes describe the light staying on roughly "desde las 7 de la noche hasta el amanecer" (Guillermo
Cordova) — an appliance practice, not sleep itself, so not used to set this window's bounds, but
consistent with a night running from evening through dawn.

*Practices: sleep; passive household security (minority; see VA4).*

---

## 5. Virtual Appliance parameterisation

### Parameter summary

| VA                           | Hardware | Window (min)            | Rigidity                    | power | func_time | func_cycle | t_f_r_v | random_var_w       | occasional_use |
| ---------------------------- | -------- | ----------------------- | --------------------------- | ----- | --------- | ---------- | ------- | ------------------ | -------------- |
| VA1 Indoor morning light     | LED_1    | [300, 420]              | Flexible                    | 3 W   | 84        | 42         | 0.20    | 0.30               | 0.20           |
| VA2 Indoor daytime light     | LED_1    | [420, 1080]             | Chaos                       | 3 W   | 60        | 30         | 0.30    | 0.35               | 0.57           |
| VA3 Indoor evening light     | LED_1    | [1080, 1320]            | Strict                      | 3 W   | 192       | 130        | 0.10    | 0.20               | 1.00           |
| VA4 Indoor overnight light   | LED_1    | [1320, 1440] ∪ [0, 300] | Strict (engine-constrained) | 3 W   | 336       | 70         | 0.10    | 0.20               | 0.14           |
| VA5 Outdoor morning light    | LED_2    | [300, 420]              | Flexible                    | 2 W   | 84        | 42         | 0.20    | 0.30               | 0.20           |
| VA6 Outdoor daytime light    | —        | **retired**             | —                           | —     | —         | —          | —       | —                  | —              |
| VA7 Outdoor evening light    | LED_2    | [1080, 1320]            | Chaos                       | 2 W   | 156       | 78         | 0.30    | 0.35               | 1.00           |
| VA8 Outdoor overnight light  | —        | **retired**             | —                           | —     | —         | —          | —       | —                  | —              |
| VA9 Portable-device charging | USB      | [0, 1440]               | n/a (structural)            | 3 W   | 300       | 120        | 0.20    | **0** (structural) | 1.00           |

VA9 additionally carries `thermal_P_var = 0.3` **[DECLARED DEFAULT]**.

---

### VA1 — Indoor morning light (LED_1)

```yaml
power: 3
num_windows: 1
window_1: [300, 420]
func_time: 84
func_cycle: 42
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.20
```

**Narrative.** Waking is early, but lighting it is optional: natural pre-dawn light and the household's
own momentum usually suffice, and the SHS bulb supplements only when circumstances call for it.

**Rigidity [RIG-XW]: Flexible.** *"Generalmente en la mañana lo usamos muy poco o a veces; con más
frecuencia la usamos por la noche"* (Antonio Negrete, 25/02/2026); *"Sí, la usamos frecuentemente por las
noches; muy poco por las mañanas"* (Arminda Reyes, 25/02/2026). Both respondents describe a consistent,
describable pattern (natural light usually suffices), which is what separates Flexible from Chaos — the
respondent *can* characterize the practice, just as secondary and low-frequency.

- **w_1 [WINDOW]:** survey `light_1_morning` modal code, tied between 04:00–07:00 and 05:00–07:00 (6/26
  households each); 05:00–07:00 used.
- **func_time [WINDOW→margin]:** 120 × (1 − 0.30) = 84 min.
- **func_cycle [RIG-XW→func_time]:** ≈0.5 × func_time (Flexible ratio, reduced from the canonical 0.6 to
  keep RAMP's window-jitter engine constraint satisfied at this VA's `random_var_w=0.30` — see Protocol
  §5 note) ≈ 42 min.
- **occasional_use [FREQ-XW]:** Low/Sporadic bin — the quotes above support infrequent use.

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep).** Floor to the profile's stated
Growing & Grazing `occasional_use` floor (§6) — households are away from the home for more of the day
during these lower-labor-intensity-but-still-active seasons.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.14
```

### VA2 — Indoor daytime light (LED_1)

```yaml
power: 3
num_windows: 1
window_1: [420, 1080]
func_time: 60
func_cycle: 30
time_fraction_random_variability: 0.30
random_var_w: 0.35
occasional_use: 0.57
```

**Narrative.** During standard workdays, indoor daytime lighting is practically non-existent — labor is
outdoors and natural daylight suffices. This baseline of zero-consumption is periodically interrupted by
anomalous daytime events: severe weather, a device left charging, illness, or seasonal indoor chores. No
respondent reports this specific use directly; the closest related material — cloudy-weather panel
performance discussed by Antonio Negrete and José Acosta Inturias — explains *why* this VA is Chaos
(a weather-linked but never systematically tracked trigger) without supplying its own frequency value.

**Rigidity [RIG-XW]: Chaos.** The household is normally empty during this window; any use is a genuine
anomaly, not a describable pattern.

- **w_1 [WINDOW]:** [420, 1080] (07:00–18:00) — widened by one hour from the Window 2 bound (07:00–17:00)
  specifically to close the indoor window-continuity gap between VA1 and VA3; the extra hour absorbs the
  workday-to-evening transition rather than leaving it unclaimed by any indoor VA.
- **func_time [narrative, margin rule does not apply]:** 60 min — Chaos/event-driven within a wide
  window; the margin formula would wrongly imply hours of near-continuous use.
- **func_cycle [RIG-XW→func_time]:** 0.5 × func_time (Chaos, fragmented use) = 30 min.
- **occasional_use [FREQ-XW]:** 0.57 (4/7, explicit count) — no direct anchor quote for this VA
  specifically; left at the crosswalk's Chaos-appropriate value rather than forcing an indirect fit to
  the weather material above.

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep).** Same stated floor as VA1/VA5 (§6) —
even the already-low daytime anomaly rate drops further as households spend more of the day away.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.14
```

### VA3 — Indoor evening light for homework and dinner (LED_1)

```yaml
power: 3
num_windows: 1
window_1: [1080, 1320]
func_time: 192
func_cycle: 130
time_fraction_random_variability: 0.10
random_var_w: 0.20
occasional_use: 1.00
```

**Narrative.** The most critical, structured period of the household's energy demand. Hardware is
severely constrained — typically one or two bulbs for the whole household — so the single main-room
light is actively shared: women use it for food preparation and dining (Rule 3) while children rely on
it for schoolwork (Rule 1) at the same time. Families exhibit strategic load-shifting earlier in the day
to guarantee sufficient battery capacity for this window.

**Rigidity [RIG-XW]: Strict.** Anchored to Rule 1 (Educational) and Rule 3 (Kitchen), both
non-negotiable. *"la necesitamos cada día por las noches; los chicos van haciendo sus tareas"* (Natividad
Sánchez, esposa of Vicente Tapia Sanchez, 44, 24/02/2026).

- **w_1 [WINDOW]:** true modal survey code (`light_1_night`, 18:00–22:00, 8/28 households) and
  independently corroborated by six interview accounts (see §4, Window 3) — a clean nested case,
  consistent with Strict rigidity and the low `random_var_w` already assigned.
- **func_time [WINDOW→margin]:** 240 × (1 − 0.20) = 192 min.
- **func_cycle [RIG-XW→func_time]:** ≈0.70 × func_time (Strict, reduced from the canonical 0.83 to keep
  RAMP's window-jitter engine constraint satisfied at this VA's `random_var_w=0.20` — see Protocol §5
  note) = 130 min.
- **occasional_use [FREQ-XW]: priority override, 1.00.** Non-negotiable Educational/Kitchen rule; does
  not decrease during Growing & Grazing, since school attendance is a constraint on absence, not a
  target of it.

### VA4 — Indoor overnight light, household-level heterogeneity (LED_1)

```yaml
power: 3
num_windows: 2
window_1: [1320, 1440]
window_2: [0, 300]
func_time: 336
func_cycle: 70
time_fraction_random_variability: 0.10
random_var_w: 0.20
occasional_use: 0.14
```

**Narrative.** A minority of families leave a light on through the night for a sense of security or
comfort. This is a passive, continuous background load, not active task lighting. None of the three
households evidencing this practice states a reason for it — no fear, no safety, no tiredness is
mentioned; the practice is real, but its cause is not established by the data, so none is asserted.

**Rigidity [RIG-XW]: Strict, for the households that do this.** All three confirmed accounts describe a
highly rigid, near-continuous nightly pattern: *"La usamos durante toda la noche; apagamos al amanecer"*
(Teresa Claros, esposa of household head Guillermo Negrete, 72, 25/02/2026); *"Desde las 7 de la noche
hasta el amanecer; toda la noche está prendido"* (Guillermo Cordova, 95, 20/11/2024); *"Alumbra desde las
6 de la tarde, a veces hasta el amanecer, pero no se apaga"* (Albino Acosta, 58, 20/11/2024).

- **w_1, w_2 [WINDOW]:** [1320, 1440] ∪ [0, 300] (22:00–05:00, 420 min) — matches AW4's own bound
  exactly, closing the loop with VA1's start (300) with no overlap or gap.
- **func_time [WINDOW→margin]:** 420 × (1 − 0.20) = 336 min.
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 70 min, not the Strict ratio.** This VA's two
  windows straddle midnight and are very unequal in width (120 min evening tail vs. 300 min early-morning
  block). RAMP's switch-on placement (`rand_switch_on_window`) requires `func_cycle` to fit inside *each*
  window independently, not just the combined 420-minute total — and under this VA's own `random_var_w
  =0.20` jitter, the 120-minute evening window can shrink to a hard floor of 72 min on any given day
  (`120 − 2×⌊0.20×120⌋`). Verified directly: with the profile's originally-derived func_cycle (280, later
  230 under the Strict-ratio fix applied to VA3/VA4 together), the evening window was *never* eligible —
  isolated 200-day testing showed zero real switch-on minutes in [22:00, 24:00) and 7% of days with no
  activity at all, despite `occasional_use=1.0` in that test. `func_cycle=70` keeps a 2-minute buffer
  below the 72-minute floor so the evening window is eligible every day. This pulls the func_cycle/func_time
  ratio down to ≈0.21 — well below the Strict band (~0.7–0.83) used elsewhere — so nightly usage is now
  reached via several shorter switch-on bursts across both windows rather than one long unbroken block;
  the total nightly on-time (`func_time=336`) and the "runs most of the night" narrative are preserved,
  only the single-continuous-block texture is not.
- **occasional_use [household-level heterogeneity]: 0.14.** 3 of 18 interviewed households (≈17%), or 3
  of 28 using the full survey population (≈11%). Rounded to 0.14 (1/7) for consistency with the
  crosswalk's day-fraction convention — a stated practical choice, not a re-derived value. Albino
  Acosta's account is independently corroborated by his field memo (a household of six, fully
  transitioned from mecheros to solar, with no dual-home signal). Flat value is adequate for this
  paper's validation, since Tier 2 metrics run on the profile-averaged curve, not per-household. Held at
  0.14 unchanged for the seasonal case too — nothing in the evidence suggests seasonal variation.

### VA5 — Outdoor morning light (LED_2)

```yaml
power: 2
num_windows: 1
window_1: [300, 420]
func_time: 84
func_cycle: 42
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.20
```

**Narrative.** Brief, pre-dawn outdoor chores — feeding animals, preparing equipment in the yard — before
the sun provides adequate visibility. Similar to VA1's indoor routine.

**Rigidity [RIG-XW]: Flexible.** No interview material differentiates indoor from outdoor morning light
use, so VA1's evidence (infrequent, daylight-supplementing, not a fixed necessity) is assumed to apply
equally here — a parity assumption between VA1 and VA5, not independently confirmed for the outdoor
light specifically.

- **w_1 [WINDOW]:** survey `light_2_morning` modal code (7/24 households, the single most common
  reported window).
- **func_time [WINDOW→margin]:** 120 × (1 − 0.30) = 84 min.
- **func_cycle [RIG-XW→func_time]:** ≈0.5 × func_time (Flexible ratio, reduced from the canonical 0.6 for
  the same RAMP engine-constraint reason as VA1 above) = 42 min.
- **occasional_use [FREQ-XW]:** Low/Sporadic, per VA1's quotes, assumed to apply equally.

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep).** Same stated floor as VA1/VA2 (§6),
by the same parity assumption used for the baseline value.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.14
```

### VA6 — Outdoor daytime light (LED_2) — **retired, no parameters**

No YAML block — this VA carries no parameters and is not passed to RAMP.

**Narrative.** Outdoor daytime lighting is behaviorally non-existent for this profile, not merely rare:
using an exterior light in full sunlight has no plausible logic for a conservation-minded household, and
no respondent reports it. Its 07:00–18:00 span sits between two functioning VAs (VA5 and VA7), but this
is not a continuity problem — the window is genuinely unused, and a hard zero is the evidenced output,
not a gap to explain away. Kept as a numbered slot only so "VA6" denotes the same practice-type across
profiles.

### VA7 — Outdoor evening light (LED_2)

```yaml
power: 2
num_windows: 1
window_1: [1080, 1320]
func_time: 156
func_cycle: 78
time_fraction_random_variability: 0.1
random_var_w: 0.2
occasional_use: 1.00
```
Note: func_cycle was reduced due to model constraints, but the underlying evidence supports a longer cycle; see narrative.
**Narrative.** During the evening, family members move between structures (main room, secondary,
latrine) or secure animals for the night. Used daily, but in intermittent bursts rather than a continuous
draw, reflecting transient movement rather than prolonged outdoor labor.

**Rigidity [RIG-XW]: Chaos.** Outdoor nighttime movement is need-triggered and irregular, not a bounded
schedule: *"Sí compramos para la linterna e ir afuera, ir al baño"* (Antonio Negrete, 20/11/2024); *"No
usamos con frecuencia la linterna; la usamos solo cuando es necesario por las noches para salir, a
veces"* (Miguel Meneses, 25/02/2026). "A veces," "cuando es necesario" — the respondent can't specify a
stable pattern, the Chaos signature. Caveat: both quotes describe the portable flashlight, not confirmed
identical to the fixed outdoor SHS light this VA represents, though plausibly the same underlying need. Change this to rigid!

- **w_1 [WINDOW]:** survey `light_2_night` modal code (6/26 households, excluding two 11-hour outlier
  households).
- **func_time [WINDOW→margin]:** 240 × (1 − 0.35) = 156 min.
- **func_cycle [RIG-XW→func_time]:** 0.5 × func_time (Chaos) = 78 min.
- **occasional_use [FREQ-XW]:** 1.00 (daily) — no direct evidence for this specific appliance's
  frequency; flashlight quotes are a plausible but unconfirmed analogy. Kept at 1.00 rather than lowered:
  no evidence means no revision, not a best guess.

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep).** Proportional decrease per §6
(1.00 → 0.71), rather than a floor — outdoor evening transit still happens most days, just less
uniformly, unlike the near-elimination pattern used for VA1/VA2/VA5.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.71
```

### VA8 — Outdoor overnight light (LED_2) — **retired, no parameters**

No YAML block — this VA carries no parameters and is not passed to RAMP.

**Narrative.** Same logic as VA6: no active transit or socializing happens outside during sleep hours, so
a conservation-minded household has no functional reason to use the outdoor light then. The real "leave a
light on" safety phenomenon is already captured indoors by VA4, evidenced by direct quotes from three
households — VA8 would otherwise represent an unevidenced, structurally redundant outdoor duplicate of
that same practice. Its 22:00–05:00 span sits between two functioning VAs (VA7 and VA5) but is genuinely
unused, not merely under-evidenced. Kept as a numbered slot only, matching VA6's treatment.

### VA9 — Portable-device charging (USB: phone, radio, flashlight)

```yaml
power: 3
num_windows: 1
window_1: [0, 1440]
func_time: 300
func_cycle: 120
time_fraction_random_variability: 0.20
random_var_w: 0
occasional_use: 1.00
thermal_p_var: 0.3   # DECLARED DEFAULT, pending measurement — see narrative
```

**Narrative.** Information and communication are constant background needs, recently sharpened by
education demands. Devices are plugged in opportunistically whenever power is available; charging is
decoupled from strict behavioral windows and occurs throughout the day. Ownership does not guarantee
simultaneous use: *"Para dos celulares no abastece; solo abastece para uno"* (Edelfrida Jiménez Salazar,
20) — households with two phones frequently ration to one at a time, a constraint not separately modeled
(`number` represents device count, not simultaneity, per stated decision). Weather suppresses supply
rather than driving demand: *"cuando se nubla, tampoco se puede recuperar (la carga)"* (Edelfrida Jiménez
Salazar, 20) — consistent with the conservation orientation documented throughout this profile.

- **number [DECLARED DEFAULT]:** 4 — average of 2 phones + 1 radio + 1 portable flashlight per household.
  Broadly consistent with survey `phones` data (mean 1.37, median 1; 0 phones in 5/28 households: ids 16,
  58, 80, 90, 100), extended to the full device mix by assumption rather than a directly surveyed
  combined count.
- **w_1 [WINDOW]:** [0, 1440] — full day; charging can occur at any daylight hour.
- **func_time [FREQ-XW→duration evidence]:** 300 min (5h) — grounded in *"Sí, a veces en el día hago
  cargar, a veces en la noche, entre 4 o 6 horas"* (Moises Acosta, 25/02/2026, midpoint of stated range).
- **func_cycle [SPEC-adjacent]:** 120 min — reflects device charge-cycle length (a hardware property),
  not a rigidity-derived fraction.
- **random_var_w [RIG-XW, structurally forced]:** 0 — the window already spans the full day, so there is
  no window-width left to randomize. *Source: "cuando hay bastante sol, hay bastante energía"* (Miguel
  Meneses).
- **occasional_use [FREQ-XW]:** 1.00 (daily) — corroborated by Albino Acosta's *"celulares nomás hacemos
  cargar, como cinco veces al día"* (58), this profile's cleanest frequency-specific charging anchor.
  Unchanged across seasons: charging itself remains daily; the seasonal effect is on duration, not
  frequency (`func_time` reduced to 200 min = 300 × 2/3 during Growing & Grazing — households spend less
  time at home, reducing the daily window available for charging even though the practice stays daily).
- **thermal_p_var [DECLARED DEFAULT]:** 0.3 — lithium-ion CC-CV charging tapers current substantially as
  a device nears full charge, and this profile's mixed inventory (radios, smartphones, older feature
  phones sharing the same 5V USB supply) adds further variability even within the same charge phase. A
  stated middle-ground figure — not lab-measured; flag any downstream result sensitive to it.

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep).** Duration effect, not frequency:
charging stays daily, but the daily window available for it shrinks as households spend more time away
from home (`func_time` = 300 × 2/3 = 200 min).

```yaml
seasons: [growing, free_grazing]
func_time: 200
```

---

## 6. Seasonality

The four-season agricultural calendar structures this profile's year:

**Planting (October–January).** Sowing begins Oct–Nov (potatoes, maize), wheat sowing in January; the
Mama Rosario festival marks the season's start. Livestock is actively controlled to protect newly sown
fields. High labor demand — families stay home to tend crops. *Expected energy impact: moderate–high.*

**Growing & early harvest (February–April).** Constant labor and crop care through the rainy season;
Carnival rituals thank Mother Earth for growing crops; harvesting begins in March. Peak labor intensity
begins here. *Expected energy impact: high.*

**Harvesting (May–June).** Heavy harvesting across the community, ending June 24 with the San Juan
festival (marking the Andean New Year). *Chhalaku* — traditional bartering of highland for valley goods —
also occurs. Highest physical labor demand of the year. *Expected energy impact: very high.*

**Free grazing & migration (July–September).** From June 24, community territory becomes communal
pasture; animals graze freely on crop stubble. Some households undertake temporary migration (e.g. to
Chapare) for supplementary income, and families may be absent for extended periods. Lowest agricultural
labor demand of the year, but energy use is lower than baseline, not zero — constrained by children's
non-negotiable school attendance (partial absence only). *Expected energy impact: low.*

**Seasonal treatment by VA:**
- VA3, VA4 stay at baseline — non-negotiable (VA3) or already minimal and cause-agnostic (VA4).
- VA1, VA2, VA5 sit at an explicit floor (0.14) during Growing & Grazing.
- VA7 decreases proportionally (1.00 → 0.71).
- VA9's seasonal effect is on duration (`func_time`, 300→200 min), not frequency.
- VA6 and VA8 carry no parameters at all (retired), so no seasonal effect applies.

---

## 7. Provenance (anchor quotes → parameters)

| Respondent (id, date)                                                                                                                     | Anchor                                                                                                                         | Feeds                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| Antonio Negrete (6, 25/02/2026)                                                                                                           | *"Generalmente en la mañana lo usamos muy poco o a veces; con más frecuencia la usamos por la noche"*                          | VA1 Rigidity (Flexible)                                                                           |
| Arminda Reyes (8, 25/02/2026)                                                                                                             | *"Sí, la usamos frecuentemente por las noches; muy poco por las mañanas"*                                                      | VA1 Rigidity (Flexible)                                                                           |
| Arminda Reyes (8)                                                                                                                         | *"No, no… nada. Ningún trabajo realizamos"*                                                                                    | Rule 15 (Productive Lighting Veto)                                                                |
| Arminda Reyes (8)                                                                                                                         | *"nosotros no vamos a ningún lado; aquí vivimos siempre"*                                                                      | §1 sedentary-residence generalization                                                             |
| Natividad Sánchez (esposa, household 44, 24/02/2026)                                                                                      | *"la necesitamos cada día por las noches; los chicos van haciendo sus tareas"*                                                 | Window 3 grounding; VA3 Rigidity (Strict) + priority-override `occasional_use`; Rules 1 & 3       |
| Carlos Negrete (63, 19/11/2024)                                                                                                           | *"Hago alumbrar desde las 6 de la tarde hasta las 10 de la noche"*                                                             | VA3 `w_1` corroboration                                                                           |
| José Acosta Inturias (74, 19/11/2024)                                                                                                     | *"desde las 6 de la tarde hasta las 10 de la noche; no amanezco con la luz prendida"*                                          | VA3 `w_1` corroboration                                                                           |
| José Acosta Inturias (74)                                                                                                                 | *"Desde las 9 de la mañana ya empiezo a salir y regresamos como a las 3 o 4 de la tarde"*                                      | Rule 2; Window 2                                                                                  |
| José Acosta Inturias (74)                                                                                                                 | *"No, durante el día tejemos; no utilizamos la luz… en la mañana nomás hilamos la lana"*                                       | Rule 15 (primary anchor)                                                                          |
| José Acosta Inturias (74)                                                                                                                 | *"Durante ese mes yo me voy a ir allá abajo, a mi otra casa… allá igual tenemos otro [panel]"*                                 | §8 — seasonal second-residence finding, not built into a VA                                       |
| Calixto Negrete (62, 25/03/2026)                                                                                                          | *"A partir de las 6 o 7 hasta las 10 de la noche, algo así; ocupamos siempre la luz"*                                          | VA3 `w_1` corroboration                                                                           |
| Pascual Zurita (83, 19/11/2024)                                                                                                           | *"desde las 6 de la tarde hasta las 10 de la noche"*                                                                           | VA3 `w_1` corroboration; Window 3 grounding                                                       |
| Pascual Zurita (83)                                                                                                                       | *"Prendo por la noche a las 6 de la tarde, y en las madrugadas a las 4 de la mañana"*                                          | Window 1 pre-dawn corroboration                                                                   |
| Pascual Zurita (83)                                                                                                                       | *"El menor es mi hijo y el otro es mi nieto"*; grandson *"faltan 3 años para que vaya al colegio"*                             | Rule 1 — corroborating demographic evidence                                                       |
| **[FIELD MEMO, caseid 33]** Permanent resident, same location his entire life, single SHS, ten children mostly migrated to Chapare/Mizque | corroborates Pascual's sedentary status                                                                                        |
| Teresa Claros (esposa of Guillermo Negrete, 72, 25/02/2026)                                                                               | *"La usamos durante toda la noche; apagamos al amanecer"*                                                                      | VA4 Rigidity (Strict) + `occasional_use` anchor                                                   |
| Teresa Claros (72)                                                                                                                        | *"yo no realizo ninguna actividad con la luz porque no es tan nítido. Si hago mis tejidos, siempre los estoy haciendo afuera"* | Rule 15                                                                                           |
| Guillermo Cordova (95, 20/11/2024)                                                                                                        | *"Desde las 7 de la noche hasta el amanecer; toda la noche está prendido"*                                                     | VA4 Rigidity (Strict) + `occasional_use` anchor; secondary corroboration for Window 4             |
| Albino Acosta (58, 20/11/2024)                                                                                                            | *"Alumbra desde las 6 de la tarde, a veces hasta el amanecer, pero no se apaga"*                                               | VA3 `w_1` corroboration; VA4 Rigidity (Strict) + `occasional_use` anchor (third household)        |
| Albino Acosta (58)                                                                                                                        | *"celulares nomás hacemos cargar, como cinco veces al día"*                                                                    | VA9 `occasional_use` (Daily/Fixed) — cleanest frequency-specific charging anchor in this profile  |
| Albino Acosta (58)                                                                                                                        | *"Uno nomás [está en el colegio]. El otro ya irá al año"*                                                                      | Rule 1 — corroborating demographic evidence                                                       |
| Albino Acosta (58)                                                                                                                        | *"Antes usaba todo el tiempo mechero; ahora ya no… Lo hemos botado"*                                                           | §1 conservation-orientation generalization                                                        |
| **[FIELD MEMO, caseid 44]** Household of six in Molle Orcko, one student, single SHS, fully transitioned from mecheros to solar           | corroborates Albino's single-residence status and conservation orientation                                                     |
| Antonio Negrete (6, 20/11/2024)                                                                                                           | *"Sí compramos para la linterna e ir afuera, ir al baño"*                                                                      | VA7 Rigidity (Chaos)                                                                              |
| Miguel Meneses (80, 25/02/2026)                                                                                                           | *"No usamos con frecuencia la linterna; la usamos solo cuando es necesario por las noches para salir, a veces"*                | VA7 Rigidity (Chaos)                                                                              |
| Miguel Meneses (80, P1)                                                                                                                   | *"cuando hay bastante sol, hay bastante energía"*                                                                              | VA9 `random_var_w` (illustrative; the value itself is structurally forced by the full-day window) |
| Moises Acosta (81, 25/02/2026)                                                                                                            | *"Sí, a veces en el día hago cargar, a veces en la noche, entre 4 o 6 horas"*                                                  | VA9 `func_time`                                                                                   |
| Edelfrida Jiménez Salazar (20, 26/02/2026)                                                                                                | *"por las noches desde las 6:00 a las 10:00 p.m."*                                                                             | Window 3 / VA3 `w_1` corroboration                                                                |
| Edelfrida Jiménez Salazar (20)                                                                                                            | *"la luz es muy elemental para que realicen sus tareas"*                                                                       | Rule 1                                                                                            |
| Edelfrida Jiménez Salazar (20)                                                                                                            | *"nosotros no paramos en casa; siempre nos vamos al trabajo de campo"*                                                         | Rule 2; Window 2                                                                                  |
| Edelfrida Jiménez Salazar (20)                                                                                                            | *"Para dos celulares no abastece; solo abastece para uno"*                                                                     | VA9 narrative — ownership vs. simultaneity                                                        |
| Edelfrida Jiménez Salazar (20)                                                                                                            | *"cuando se nubla, tampoco se puede recuperar (la carga)"*                                                                     | VA9 / VA2 narrative — supply-side weather suppression                                             |
| Edelfrida Jiménez Salazar (20)                                                                                                            | *"Dos focos estamos usando"* (vs. survey `light_bulbs = 1`)                                                                    | §3 — flagged data/interview conflict, not resolved                                                |
| Domingo Vallejos (19, 20/11/2024)                                                                                                         | *"Ahora duermen como a las 9:00 o 10:00 de la noche"*                                                                          | Window 3/4 boundary corroboration                                                                 |
| Domingo Vallejos (19)                                                                                                                     | *"linterna nomás cuando salimos"*                                                                                              | VA7 corroboration                                                                                 |
| Domingo Vallejos (19)                                                                                                                     | *"Mi mujer solamente se queda aquí y yo a veces voy a trabajar"*                                                               | §1 — individual labor absence vs. household relocation                                            |
| Adrián Felipes (90, 20/11/2024)                                                                                                           | *"solo uno nomas el otro lo saque, porque no mantiene los dos"*                                                                | §3 — hardware reduction, not just non-ownership                                                   |
| Adrián Felipes (90)                                                                                                                       | *"su luz nomas tiene, para cocinar usa"* (referring to his mother)                                                             | Rule 3 corroboration                                                                              |
| Adrián Felipes (90)                                                                                                                       | *"todo el año nos quedamos aquí"*                                                                                              | §1 sedentary-residence generalization                                                             |

Survey fields used: `light_1_morning`, `light_2_morning`, `light_1_night`, `light_2_night` (modal codes),
`wakeup_time_after`, `sleep_time_after`, `light_bulbs`, `radios`, `phones`, `family_type`, `occupation`,
`children_in_school`, `migration`, `portability_shs` (classification fields, `classifications_oficial.csv`).

**Field-memo coverage.** All 18 interviewed households have a corroborating field memo. None contradicts
the transcript-based values above; all corroborate household composition, hardware inventory, and
residence pattern, consistent with the transcript evidence — with the single exception of José Acosta
Inturias (74), whose memo (two on-site electricity sources, no mention of a second residence) does not
independently corroborate his own interview's second-residence statement, but does not contradict it
either; the two sources simply speak to different things.

---

## 8. Open items carried forward

- **José Acosta Inturias (74) describes a seasonal second residence with a separate panel** — the
  household's SHS is stored, not moved, during a roughly month-long annual absence ("allá abajo, a mi
  otra casa"). The survey's `migration` field records this household as non-migrating, which the
  interview directly contradicts. This is a single, thin account (one respondent, one recurring month)
  and is not built into any VA parameter here, consistent with how Profile 2 treats single-household
  detail without independent timing evidence. Worth a follow-up interview and worth stating explicitly in
  the paper's methods or limitations, since it is currently the profile's only instance of anything
  resembling structural dual-residence and the survey alone would never have surfaced it.
- **Edelfrida Jiménez Salazar (20): `light_bulbs = 1` in the survey vs. "Dos focos estamos usando" in her
  interview.** Left unresolved; flagged rather than silently picked one way. If per-household hardware
  inventories are ever used downstream, this household needs a direct follow-up.
- **Window 2 has no independent grounding.** Its bounds (08:00–17:00) are set structurally, as the
  complement of Window 1's end and Window 3's start, anchored to Rule 2 and daylight physical bounds —
  not to a dedicated survey or interview timing field the way Windows 1, 3, and 4 are. Doesn't change any
  parameter value, but the window's confidence should be read as structural-inference, not triangulated.
- **VA2 `occasional_use`** rests on narrative plausibility (weather-linked Chaos reasoning) rather than a
  direct frequency anchor quote — carried forward as a limitation on that specific value.
- **VA9 `thermal_P_var` (0.3) and the seasonal `func_time` reduction (2/3 factor)** are declared defaults
  pending real measurement or a more direct evidential source — flag any downstream result sensitive to
  these exact figures.
- **id 88 (Vicente Inturias) adds headcount, not evidence.** His interview is thin (general appreciative
  statements, no timing data) — no VA in this file currently rests on it.
- **Ids 58 and 83 are held in Profile 1 by an analyst override.** `classifications_oficial.csv` places
  both in Profile 4; the override rests on non-mobility interview language and a family-composition
  mismatch with Profile 4's definition (see population block). Both households also show a
  `children_in_school = 0` tension with this profile's Educational-Core framing (2 of the profile's 3
  such cases). This should be stated explicitly wherever the classification is cited in the paper's
  methods or limitations, not left as a silent disagreement with the source the paper otherwise treats as
  canonical.