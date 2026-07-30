# Profile 3: The Extended Hub — RAMP truth file (protocol-applied)

> Derivation authority: `parameter_derivation_protocol.md` (§3.3.1.1). Every parameter below carries its
> derivation tag — **[SPEC]**, **[WINDOW]**, **[FREQ-XW]**, **[RIG-XW]**, **[RIG-XW → func_time]**,
> **[DECLARED DEFAULT]**. No value is left without a declared basis.

```
Population: N_survey = 14 (ids 7, 13, 15, 29, 30, 31, 33, 38, 49, 61, 67, 69, 75, 78; classified via
            family_type/occupation/children_in_school/migration/portability_shs, per
            `classifications_oficial.csv`, the protocol's canonical classification source)
            N_interview = 9 (Apolina Vallejos 7, Bonifacio Molina 13, Isabel Zurita/Teófilo Vallejos 29,
            Marcelino Sánchez 33, Primitivo Agreda 38 [respondent: la nuera, who does not reside there],
            Basilio Salazar 61 [interviewed twice, 2024 + 2026], Dionisio Vargas Castro 67,
            Felipe Rivera 69 [+esposa], Martín Salazar 78 [respondents: son + wife].
            Not interviewed: ids 15, 30, 31, 49, 75.)
            Coverage 64% (9/14) — the "load-bearing hub" reading applies to a genuine subset (see §1),
            not the profile as a whole; two of the nine interviews are thin (38: respondent does not
            live in the household; a testimonial from Apolina's household, id 7, adds a second-order
            structural-absence anchor rather than routine timing detail — see R-E).
Generalization: all qualitative parameters below (Windows, Rigidity, occasional_use, and
Extreme/Structural bin assignment) are inferred from N_interview and applied uniformly to
all N_survey households at simulation time. There is no survey-only shortcut for any of
these — dual-household/structural-absence status requires interview evidence, the same as
ordinary timing and frequency parameters.
```

---

## Methodological basis

No outdoor luminaire VA is modeled: the SHS deploys two indoor bulbs and a USB port, with no
outdoor-light field in the survey and every interview mention of outdoor light naming a handheld
flashlight, not a fixed bulb. VA9 (charging) reflects an undersupplied system, not a stacked-demand
one — several households report the SHS cannot keep up with even one large phone — with `func_time`
scaled by the profile's own phone-ownership count (mean 1.8 among owners) rather than a single-device
figure. The evening VA (VA3) is grounded in the true modal survey window (18:00–22:00) and held below
1.0 for a supply-side reason (unreliable generation, R-D), not treated as a fixed, non-negotiable
block. The overnight VA (VA4) is framed as "hacer amanecer" with no stated cause, not a security
practice — no respondent gives a security rationale, and Felipe's scorpion/vinchuca remark is
retrospective (the light lets them notice one, not a stated reason to leave it on). Seasonality runs
through structural absence (migration) and supply (rainy-season outages), not per-VA `occasional_use`
edits, since no measured season→behavior link exists in this study. `func_time` throughout is derived
via `window_width × (1 − random_var_w)`, consistent with Protocol §4 and independently supported here:
the sum of a household's reported morning+night window widths matches its reported `light_bulb_1_time`
almost exactly (10/14 households), reproducing Profile 1's empirical finding.

---

## 1. Demographic summary

Households classified by **extended / numerous family structure** — 13 of 14 carry an *Extendido* or
*numeroso* family type — with a mean household size of **6.4** (range 3–11) and low monthly income
(mean ≈ 320 Bs). Eleven of fourteen heads are agriculturalists. On paper this is the study's most
populous profile, and for a genuine subset that populousness is real and energetically visible: Felipe
Rivera (id 69, eight children) and Martín Salazar (id 78, five residents including four school-age
children) run the profile's longest and latest indoor loads. Apolina Vallejos (id 7) represents a
distinct extended-family pattern within the same label: a grandmother-headed household where the
working-age parents (her son Rodolfo and his wife) live and work elsewhere, visiting only occasionally
(*"a veces salen una vez al mes... Domingos en las tardes se van también a la mina"*) — extended by
generational structure, not by co-residence density.

> **The label describes family *structure*, not co-residence — and this matters for the "hub" reading.**
> The classifier keys on family type, so it admits households that are *extended on paper but emptied in
> practice*. Basilio Salazar (id 61, "Extendido sin hijos") lives with his wife alone — *"Con mi mujer
> nomás vivo; somos dos"* — his six children long since out-migrated (*"están en la ciudad todos… vienen
> a visitarme, después se van nomás"*). Marcelino Sánchez (id 33) reports three residents. Dionisio
> Vargas Castro (id 67) is similar again: a couple living alone (*"nosotros solo vivimos... esposo y
> esposa"*), with an adult daughter in Cochabamba visiting occasionally. Across the interviewed set the
> survey's `fam_members` count routinely exceeds the number actually *present* (id 61: 4 vs 2; id 33: 5
> vs 3; id 67: 5 vs 2–3; id 78: 8 vs 5), because members are frequently away. **The "load-stacking,
> never-dormant hub" is therefore true of a minority of these households, not the profile.** For the rest,
> the energy signature is closer to Profile 2 (out-migrated kin, a single phone, a broken radio, an
> overnight bulb) than to a bustling multi-generational hub.

What genuinely distinguishes Profile 3 from Profile 2 is **later, longer evenings** (sleep mode 22:00 vs
Profile 2's 20:00, driven by homework in the child-bearing households) and **real mobility** — unlike the
sedentary Profile 2, Profile 3 households leave for the *monte*, the mine, Saipina, or Chapare, sometimes
for months (§6), and Apolina's own household shows this directly: a recent three-month stay in Chapare
during which the SHS light was never used (*"Estuve durante tres meses y no hice alumbrar, no
prendimos la luz"*). The profile is best read as *"large extended families with intermittent
occupancy,"* not as a uniform high-intensity hub.

---

## 2. The driving social rules (re-anchored to P3 evidence only)

- **R-A — The extended evening (later, homework-anchored where children are present).** The evening is the
  load-bearing practice and runs later than in any elderly profile. *"Desde las 6 de la tarde alumbra por
  mis hijos, hasta las 10 de la noche"* (Felipe, 20/11/24); *"cuando hacemos las tareas… no la apagamos
  mucho"* (esposa de Martín, 25/03/26); homework is *"generalmente por las noches"* (Teófilo, 24/02/26).
  **Model consequence:** VA3 window extends to 22:00 (vs Profile 2's 20:00). Where school-age children are
  present the evening approaches Profile 1's Strict homework anchor; where they are not (ids 33, 38, 49, 61)
  it is shorter and looser — the profile-level bin (Flexible) is the compromise, with the asymmetry named
  in §5.4.

- **R-B — "Hacer amanecer": overnight illumination, with no consistent stated cause.** A stable minority
  leaves a bulb on until dawn. *"…hasta la madrugada… no se apaga; amanece alumbrando"* (Basilio); *"no la
  apagamos… al amanecer apagamos, como a las 6 de la mañana"* (Martín's household); *"a veces amanece
  prendido con luz… no se apaga"* (Felipe). **No security rationale is offered.** Felipe's scorpion/vinchuca
  remark is retrospective — the light lets them *notice* one (*"ya con esta iluminación nos dimos cuenta"*) —
  not a reason to burn a bulb overnight. **Model consequence:** the protocol's *household-level behavioural
  heterogeneity (no stated cause)* pattern — a stable between-household difference modelled as a flat
  `occasional_use`, adequate only under the profile-averaged Tier-2 validation design in use.

- **R-C — Cooking is a biomass, not an electrical, load.** Every household cooks on the *fogón* with firewood
  (`cooking_fuel_biomass` = 1 in 14/14), including large-batch *lawa* and *mote* (Basilio) — the "Kitchen
  Dictate." **Model consequence:** cooking produces **no separate electrical VA**. Cooking's only
  electrical footprint is the *light* used to cook before dawn or after dusk (*"Generalmente para cocinar…
  encendemos la luz de 7:00 a 10:00 de la mañana"* — Primitivo's household), which is already carried by
  VA1 and VA3.

- **R-D — Supply scarcity suppresses load, and here it is severe.** Beyond the cloud-suppression common to
  all profiles (*"cuando se nubla o hay lluvia, no nos brinda el alumbramiento"* — Teófilo), Profile 3
  contains the study's worst reliability report: *"ya se apagó tres veces por sí mismo. A veces demora
  semanas en recuperarse"* (Isabel Zurita's household, id 29). **Model consequence:** no weather-driven
  *uplift* anywhere; a conservation-logic veto on any daytime lighting VA; and a supply-side discount that
  holds evening `occasional_use` below 1.0 (VA3). This is a *supply* fact, handled outside Table B — it is
  not a rigidity bin and not "Extreme."

- **R-E — Intermittent occupancy (real mobility).** Unlike sedentary Profile 2, these households leave —
  to the *monte* (Marcelino), the mine (Primitivo's family), Saipina (Basilio), or Chapare (Rivera's kin),
  and Martín Salazar's household is absent *"a veces seis meses."* Apolina Vallejos (id 7) gives the
  profile's most concrete single-household anchor: a recent three-month stay in Chapare during which the
  SHS was left completely unused (*"Estuve durante tres meses y no hice alumbrar, no prendimos la luz"*)
  — an explicit, dated account of the household-level suppression this axis is meant to capture, not an
  inference from `migration_label`. **[FIELD MEMO, caseid 53]** independently corroborates her household
  structure (grandmother managing the home for her son Rodolfo while the parents work in the mines) and
  her own frequent migration to Chapare. **Model consequence:** invokes the
  protocol's household-level **structural-absence** mechanism (suppresses *every* VA during absence, §6),
  which is the intended target of the deferred occupancy feature — not a per-appliance parameter.

---

## 3. Appliance inventory — [SPEC]

| Device | Count (survey) | Placement (interview) | Power |
|---|---|---|---|
| LED_1 | 2 bulbs in 13/14 hh (4 bulbs id 38, two panels) | Main room | 3 W (`serie_led_3w`) |
| LED_2 | as above | Second room / kitchen — **indoor** | 2 W (`serie_led_2w`) |
| USB port | phone in 12/14 hh **by survey count** (`phones` = 0: ids 29, 61); flashlight; residual radio | — | 2.5 W |

> **A note on ids 29 and 61, since the survey and interview evidence diverge and both are used below, for
> different things.** The survey's `phones` field reads 0 for both, but both households state directly, in
> interview, that they own and charge a phone (Basilio, id 61: *"carga siempre"*; Teófilo's household, id 29:
> *"Cargamos un celular"*). **`func_time`'s device-count scaling (VA9, §5) deliberately keeps the raw survey
> count** (12/14, mean 2.0 among owners) — it is a [SPEC]-tier structural figure the survey is positioned to
> answer precisely, and interview language ("un celular," "el celular") doesn't give a reliable *count* to
> substitute in. **VA9's `occasional_use` (§5), by contrast, is revised using the interview** — a behavioural
> question (does charging happen) that the interview *is* positioned to answer, and where both households
> answer unambiguously yes. The two derivations are allowed to disagree on which households "have zero
> phones" because they are answering different questions from different evidence tiers; this is stated
> explicitly rather than left as an apparent inconsistency.

**No outdoor luminaire.** The SHS ships two indoor LEDs (one 3 W, one 2 W) and a USB port; there is no
exterior fixture in the hardware, and `other_illum = flashlight` (11/14) is the survey's own confirmation
that outdoor/mobile lighting is done by torch. The second bulb is genuinely used more here than in Profile 2
(`light_bulb_2_time` mean 5.0 h vs `light_bulb_1_time` 6.0 h; active second bulb — `light_bulb_2_time` > 0 —
in 13/14 households), so LED_2's `occasional_use` is scaled by **13/14 ≈ 0.93** relative to LED_1 (vs
Profile 2's harsher 0.64), rather than duplicated.

---

## 4. Daily social practices and anthropological windows

*Socio-temporal envelopes within which RAMP may place events — not periods of continuous consumption.*

> **Modal code, defined once.** The survey does not record clock times for lighting; it records a
> **categorical period code** — each respondent picks one of a set of pre-defined windows (e.g.
> `light_1_night` code 6 = 18:00–22:00, code 13 = 18:00–05:00). The **modal code** is the code most
> respondents actually chose, taken whole, bounds and all — not a median or average of window widths,
> which would manufacture a window no respondent reported (Protocol §3). Windows below are grounded this
> way, with the crossing tier (nested / overlapping / no overlap) setting `random_var_w`.

### Window 1 — Pre-dawn / early morning (04:00 – 07:00) → `[240, 420]`
Waking is early (`wakeup_time_after` mode = **05:00**, range 04:00–06:00) and, unlike Profile 2, morning
lighting is *reported by nearly every household*: a morning period code is present in **13/14** survey
records, modal code **05:00–07:00** (`0507`, 7×), with 04:00 starts (`0407`/`0408`/`0409`) behind it.
Interviews temper the *frequency* rather than the window — *"muy pocas veces por las mañanas"* (Teófilo) —
which is a frequency statement (→ `occasional_use`), not evidence the window is unstable.
Window = union of the 04:00 interview/survey starts and the 07:00 modal end → **04:00–07:00**.
*Practices: rising, lighting the fogón for breakfast, preparing children and tools before departure.*

### Window 2 — Field day (07:00 – 18:00) → `[420, 1080]`
**No behavioural lighting load.** Agricultural households are outdoors (*"vamos al monte a trabajar"* —
Marcelino), daylight suffices, and the conservation orientation is strong (R-D). There is no survey
daytime-light field. This window exists in the model **only** to satisfy LED window-continuity — see VA2's `status: placeholder_artifact` note in §5.

### Window 3 — Extended evening (18:00 – 22:00) → `[1080, 1320]`
The profile's principal load, and its distinguishing feature: it starts at sunset and runs *late*. Survey
night codes start at **18:00** in almost every record; the end is genuinely variable (20:00 / 21:00 / 22:00,
no single dominant code); `sleep_time_after` mode = **22:00** (8/12 valid responses; missing for ids 7, 69). *"Desde las 7:00 de la noche o cuando
el sol se pone… hasta las 8:00"* (Marcelino, the short end); *"aproximadamente hasta las 10:00 de la noche"*
(Teófilo); *"hasta las 10 de la noche"* (Felipe). Window taken as the envelope **18:00–22:00**, with the
variable end carried as higher `random_var_w`.
*Practices: cooking, dinner, homework (where children present), conversation.*

### Window 4 — Overnight "hacer amanecer" (22:00 – 05:00) → `[1320, 1440] ∪ [0, 300]`
A **minority but stable** practice — a bulb left on until dawn, in a solid continuous block where it occurs.
No stated cause (R-B). Grounded on survey code 13 (18:00–05:00) and interview accounts terminating at dawn
(*"al amanecer apagamos, como a las 6 de la mañana"*).
*Practice: none — a passive background load, not an activity.*

---

## 5. Virtual Appliance parameterisation

### Parameter summary

| VA | Hardware | Window (min) | Rigidity [RIG-XW] | power | func_time | func_cycle | t_f_r_v | random_var_w | occasional_use [FREQ-XW] |
|---|---|---|---|---|---|---|---|---|---|
| VA1 Morning indoor light | LED_1 | [240, 420] | Flexible (engine-constrained) | 3 W | 126 | 63 | 0.20 | 0.30 | 0.60 |
| VA2 Daytime placeholder | LED_1 | [420, 1080] | — (engine artifact) | 3 W | 30 | 15 | 0.30 | 0.35 | **0** ⚠ |
| VA3 Evening indoor light | LED_1 | [1080, 1320] | Flexible (engine-constrained) | 3 W | 168 | 84 | 0.20 | 0.30 | 0.90 |
| VA4 Overnight "hacer amanecer" | LED_1 | [1320, 1440] ∪ [0, 240] | Strict (engine-constrained) | 3 W | 288 | 70 | 0.10 | **0.10** ✎ (was 0.20) | 0.33 |
| VA5 Second-room morning light | LED_2 | [240, 420] | Flexible (engine-constrained) | 2 W | 126 | 63 | 0.20 | 0.30 | 0.56 |
| VA6 Second-room daytime placeholder | LED_2 | [420, 1080] | — (engine artifact) | 2 W | 30 | 15 | 0.30 | 0.35 | **0** ⚠ |
| VA7 Second-room evening light | LED_2 | [1080, 1320] | Flexible (engine-constrained) | 2 W | 168 | 84 | 0.20 | 0.30 | 0.84 |
| VA8 Second-room overnight | LED_2 | [1320, 1440] ∪ [0, 240] | Strict (engine-constrained) | 2 W | 288 | 70 | 0.10 | **0.10** ✎ (was 0.20) | 0.31 |
| VA9 Portable-device charging | USB | [0, 1440] | Chaos | 2.5 W | 480 | 240 | 0.30 | **0** (structural) | 1.00 |

VA9 additionally carries `thermal_P_var = 0.2` **[DECLARED DEFAULT]**.

---

### VA1 — Morning indoor light (LED_1)

```yaml
power: 3
num_windows: 1
window_1: [240, 420]
func_time: 126
func_cycle: 63
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.35
```

**Narrative.** Households wake early (mode 05:00) and, in contrast to Profile 2, most *do* light the
morning — a period code is present for 13/14, clustered at 05:00–07:00. The interview language is about how
*often*, not about the shape: Teófilo reports morning use as *"muy pocas veces,"* Primitivo's household as
*"de 7:00 a 10:00 de la mañana… para cocinar."* Respondents can describe a bounded, mildly shifting window
(rise, light the fogón, prepare to leave), which is the Flexible signature — not Chaos.

- **power:** 3 W — **[SPEC]**
- **w_1:** `[240, 420]` (04:00–07:00) — **[WINDOW]**; modal code `0507` unioned with the 04:00 interview/survey starts
- **func_time:** **126 min** — **[WINDOW→margin]**: 180 × (1 − 0.30). Convergent with the survey morning-code widths (≈2 h)
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 63 min, not the Flexible ratio.** The canonical
  derivation (Flexible ≈0.6 × func_time = 76 min) is what the rigidity crosswalk assigns. But RAMP's
  switch-on placement requires `func_cycle` to fit inside this VA's single window even under worst-case
  jitter, and at `random_var_w=0.30` this 180-minute window has a hard floor of 72 min
  (`180 − 2×⌊0.30×180⌋`). At 76 min the window could shrink below that floor on an unlucky day, crashing
  the simulation. `func_cycle=63` keeps a safe margin below the 72-minute floor. This pulls the ratio to
  func_time down to ≈0.5, below the Flexible band, following the same fix already applied to Profile 1's
  structurally-identical VA1/VA5.
- **time_fraction_random_variability:** **0.20** — **[RIG-XW]** Flexible
- **random_var_w:** **0.30** — **[RIG-XW]** Flexible; a survey mode exists (evidence tier moderate–high) but the interview frequency hedging keeps it off the low bin — rigidity and evidence tier agree (Protocol §3's evidence-tier consistency check)
- **occasional_use:** **0.60** — **[FREQ-XW]** *High frequency* bin, **trimmed to the floor 2026-07-28**
  (from 0.65). Morning code present in 13/14 (window is common), so the practice stays in the High bin —
  Apolina and Primitivo's routine-use evidence isn't discarded — but the floor leans further into Teófilo's
  explicit hedge (*"muy pocas veces por las mañanas"*) than the previous mid-bin value did. Driver: genuine
  skip/variability, not physical capacity.

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep), provisional.** §6 point 3 states seasonality for
this profile runs primarily through structural absence, not per-VA behavioral tuning; this override is
recorded as an explicit, flagged sensitivity variant for full-year visualization, following the same
pattern as Profile 1, not as a re-derived finding.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.28
```

### VA2 — Daytime indoor light (LED_1) ⚠ **structural placeholder, not a behavioural estimate**

```yaml
power: 3
num_windows: 1
window_1: [420, 1080]
func_time: 30
func_cycle: 15
time_fraction_random_variability: 0.30
random_var_w: 0.35
occasional_use: 0
status: placeholder_artifact   # window-continuity filler only — see narrative; not a behavioral estimate
```

**Narrative.** There is **no evidence of a daytime indoor lighting practice, and good evidence against one**:
agricultural households out in the fields, sufficient daylight, an explicit conservation orientation, and no
survey daytime-light field to ground a window. Under the conservation-logic check this VA would be **retired
outright**. It is retained *only* so LED_1's VA windows tile 1440 minutes and RAMP does not cut a hard
artificial notch into the aggregate curve between 07:00 and 18:00.

- **occasional_use = 0**, **confirmed 2026-07-28**: the extraction pipeline drops `occasional_use = 0` appliances before they reach RAMP, so this VA is never actually simulated — it exists in the markdown purely so LED_1's windows read as continuous, not as a behavioural claim. Previously held at a token `0.02` on the (now-confirmed-unnecessary) assumption that a hard zero would reopen the 07:00–18:00 gap; that workaround is no longer needed.
- All other parameters are set to minimise the placeholder's energetic footprint (func_time 30 min) while keeping the window continuous.

**Seasonal override — removed 2026-07-28.** Previously raised the token to 0.28 for these months; now that
the baseline is confirmed `0` (dropped from RAMP entirely, see above), keeping a nonzero seasonal override
would have made this placeholder swing from "never simulated" to "simulated" for exactly these two seasons,
which was never a real behavioral finding. Override removed so VA2 stays a non-event year-round, consistent
with its own baseline.

### VA3 — Evening indoor light (LED_1)

```yaml
power: 3
num_windows: 1
window_1: [1080, 1320]
func_time: 168
func_cycle: 84
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.90
```

**Narrative.** The load-bearing VA of the profile, and what most separates Profile 3's curve from Profile 2's:
it runs *late*. It begins at sunset — the one hard physical anchor — and, in the households with school-age
children, is held there by homework (*"alumbra por mis hijos, hasta las 10 de la noche"* — Felipe). But the
end is not fixed: Marcelino, with no school-age children, closes at 20:00 (*"Hasta las 8:00 de la noche, más
o menos"*), while Teófilo and Felipe run to 22:00. Respondents *can* describe the pattern; it simply shifts
with the household — the Flexible signature.

> **Methodological note worth surfacing in §5.4.** The *start* is Strict (sunset, 18:00 in almost every
> survey code) and the *end* is genuinely variable. In the homework-bearing subset (ids 29, 69, 78) the
> whole practice tightens toward Profile 1's Strict homework anchor; in the childless *extendido* households
> (33, 61) it is short and loose. Table B forces one bin per VA, so this VA is binned **Flexible** as the
> profile-level compromise — the same single-bin limitation the protocol names for Profile 2's VA3, here
> arising from *between-household* heterogeneity rather than a within-account start/end split. Name it, do
> not smooth it.

- **power:** 3 W — **[SPEC]**
- **w_1:** `[1080, 1320]` (18:00–22:00) — **[WINDOW]**; 18:00 start is near-universal in the night codes, end taken as the modal envelope terminus (`sleep_time_after` mode 22:00), corroborated by three interview accounts (Teófilo, Felipe, and Marcelino at the short end)
- **func_time:** **168 min** — **[WINDOW→margin]**: 240 × (1 − 0.30)
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 84 min, not the Flexible ratio.** The canonical
  derivation (Flexible ≈0.6 × func_time = 101 min) is what the rigidity crosswalk assigns. But at this VA's
  `random_var_w=0.30`, its 240-minute window has a hard worst-case floor of 96 min
  (`240 − 2×⌊0.30×240⌋`), and 101 min exceeds that floor — the window could shrink below it on an unlucky
  day, crashing the simulation. `func_cycle=84` keeps a safe margin below the 96-minute floor, pulling the
  ratio to func_time down to 0.5 — the same fix already applied to Profile 1's structurally-identical VA3.
- **time_fraction_random_variability:** **0.20** — **[RIG-XW]** Flexible
- **random_var_w:** **0.30** — **[RIG-XW]** Flexible; the variable end is exactly the loosely-bounded window the tier expects
- **occasional_use:** **0.90** — **[FREQ-XW]** *Daily/Fixed* bin. Every interviewed household lights the evening; held below 1.0 for a **supply**-side reason (R-D): cloud takes the SHS down, and one household reports outages lasting *"semanas"* (id 29). This is a supply-side, not a preference-side, discount and is labelled as such.

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep), provisional.** A large drop from the 0.90 baseline
(daily/fixed to rare/intermittent) — flagged as the most visually dramatic of Profile 3's provisional
seasonal deltas; same status caveat as VA1 applies (visualization sensitivity variant, not a re-derived
finding per §6 point 3).

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.28
```

### VA4 — Overnight "hacer amanecer" (LED_1)

```yaml
power: 3
num_windows: 2
window_1: [1320, 1440]
window_2: [0, 240]
func_time: 288
func_cycle: 70
time_fraction_random_variability: 0.10
random_var_w: 0
occasional_use: 0.33
```

**2026-07-28 — `random_var_w` experiment: 0.20 → 0.10, testing the midnight-seam dip.** RAMP splits any
overnight-spanning appliance into two independently-jittered windows (`window_1`/`window_2`); each day, the
two edges that meet at midnight are only "bridged" into a single continuous block when the random jitter
happens to land exactly at the true boundary — roughly a coin flip regardless of `random_var_w`'s size,
which is why the simulated average load dips sharply right at hour 0/24 relative to the measured curve.
Empirically (isolated 300-day test, same window/func_time/func_cycle): at 0.20, minute-0 average load is
~41% of mid-window; at 0.10, ~42% — barely different, because the jitter only needs to be ≥1 minute for the
coin-flip dynamic to apply. This is being tried anyway to check its effect against real validation data, not
because the isolated test predicted a large improvement. `func_cycle=70` stays valid either way: at
`random_var_w=0.10` the 120-min evening-tail window's worst-case floor loosens from 72 min to 96 min
(`120 − 2×⌊0.10×120⌋`), so the existing 2-minute-buffer margin is, if anything, more comfortable than before.

**2026-07-28 — single-overnight-light merge with VA8 tried, then reverted.** VA4 and VA8 were briefly
consolidated into one "whichever bulb" VA (`occasional_use` the union, 0.54), mirroring Profile 2's fix.
Since Extended Hub households can plausibly run two overnight lights at once (unlike a lone-elder
household), the merge was an experiment rather than a correction — reverted back to the split two-bulb
version below.

**Narrative.** A bulb left burning until dawn — more prevalent here than in Profile 2. Basilio describes it
across both interview waves (*"desde las 7 de la noche hasta la madrugada… no se apaga; amanece alumbrando"*),
Martín's household ties it to homework periods (*"no la apagamos… al amanecer apagamos, como a las 6 de la
mañana"*), and Felipe reports it intermittently (*"a veces amanece prendido con luz"*). **None gives a
security rationale.** Felipe's scorpion/vinchuca remark is retrospective — the light lets them *see* one, not
a reason to run a bulb overnight — so it is not modeled with a "safety/security" framing.

> **Frequency and rigidity are orthogonal here.** *Whether* a given night gets the treatment is uncertain
> (`occasional_use = 0.33`); but *when it happens*, it is the most rigid practice in the profile — one
> switch, one unbroken block, ended by dawn. Hence **Strict**, not Chaos, despite the low frequency.

- **power:** 3 W — **[SPEC]**
- **w_1:** `[1320, 1440]`, **w_2:** `[0, 240]` (22:00–04:00) — **[WINDOW]**; grounded on survey code 13 (18:00–05:00), truncated at 22:00 to avoid double-counting VA3. **Terminus moved 2026-07-28 from 05:00 to 04:00**: VA1 (and its LED_2 mirror VA5) start at 04:00, so a 05:00 terminus overlapped them by 60 min on the *same hardware* (LED_1) — two VAs claiming the same minute on one bulb. ⚠ Carried caveat: the *evidenced* terminus is dawn itself — *"al amanecer apagamos, como a las 6 de la mañana"* — closer to 05:00/06:00 than 04:00; this is a modeling-consistency choice, not a re-derivation from new evidence.
- **func_time:** **288 min** — **[WINDOW→margin]**: 360 × (1 − 0.20). Previously 336 min (420 × (1 − 0.20)) before the window-overlap fix above shortened the combined window from 420 to 360 min. The two longest reported bulb durations (`light_bulb_1_time` = 10 h for id 78, 8 h for id 69) remain directionally consistent with a long overnight block, though no longer an exact corroboration of the specific minute count.
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 70 min, not the Strict ratio.** The canonical
  derivation (Strict ≈0.83 × func_time = 280 min) correctly reflects the practice — nobody rises mid-night
  to toggle a light they deliberately left on. But this VA's two windows straddle midnight and are very
  unequal in width (120 min evening tail vs. 300 min early-morning block). RAMP's switch-on placement
  (`rand_switch_on_window`) requires `func_cycle` to fit inside *each* window independently, not just the
  combined 420-minute total. At the original `random_var_w=0.20`, the 120-minute evening window had a hard
  floor of 72 min (`120 − 2×⌊0.20×120⌋`); at the now-lowered `random_var_w=0.10` (2026-07-28 experiment,
  see above) that floor loosens to 96 min (`120 − 2×⌊0.10×120⌋`). At `func_cycle=280` the evening window was
  *never* eligible for a switch-on under either value — confirmed by isolated 200-day testing on Profile 1's
  structurally-identical VA4 (same window shape): zero real on-minutes in the evening block, 7% of days
  with no activity at all. `func_cycle=70` was chosen as a 2-minute buffer below the original 72-min floor;
  it's now a comfortable 26 min below the loosened 96-min floor, so no change was needed to `func_cycle`
  itself when `random_var_w` moved. This pulls the ratio to func_time down to ≈0.24 — well below the Strict
  band — so nightly usage is reached via several shorter bursts across both windows rather than one long
  unbroken block; total nightly on-time (`func_time=288`) is unchanged.
- **time_fraction_random_variability:** **0.10** — **[RIG-XW]** Strict
- **random_var_w:** **0.10** — **[RIG-XW]** Strict; **lowered from 0.20, 2026-07-28, as a midnight-seam-dip
  experiment** (see note above). Survey code 13 ⊃ interview statements still supports Strict-tier rigidity;
  this specific value within the tier is now a validation-driven trial rather than a re-derivation from new
  evidence — revert to 0.20 if the fit doesn't actually improve.
- **occasional_use:** **0.33** — **[FREQ-XW]**, *household-level heterogeneity, no stated cause*,
  **moved to the interview-only reading, 2026-07-28** (from 0.25). **Underlying evidence:** survey code 13
  (1805, 18:00–05:00) in **2 of 14** households (ids 69, 78 → 0.14), plus Basilio in interview but *not* in
  his survey codes (a textbook single-period-question limitation — a categorical code cannot express
  "usually 19:00–21:00, but sometimes all night" — hence **enrichment, not a Say–Do conflict**; the tier-4
  survey-wins tiebreak is *not* invoked). Neither Apolina (7, code 10 = 1922) nor Dionisio (67, code 4 =
  1820) reports an overnight code. Any-source prevalence = **3/14 ≈ 0.21**; interview-only = **3/9 ≈ 0.33**.
  The file's previous implementation value (0.25) sat between these two already-cited numbers as a stated
  practical compromise; 0.33 is not a new derivation but the top end of that same cited range — the
  interview-only reading — now used directly instead of split down the middle.
  *(Cross-profile context: the overnight code appears in 7/65 households overall — ids 52, 69, 72, 78, 84,
  86, 95 — so this is a study-wide minority practice, not a Profile-3 signature; it is simply commoner here
  than in Profile 2.)*

### LED_2 (second-room bulb) — shared derivation rule for VA5–VA8

The second bulb is **indoor** (second room or kitchen), not outdoor. It shadows LED_1's practices — the
four VAs below inherit their windows, rigidity, `func_time`, `func_cycle`, and both variability parameters
unchanged from the corresponding LED_1 VA (VA1, VA2, VA3, VA4 respectively). Only two things differ, and
both are stated once here rather than repeated four times:

- **Power = 2 W — [SPEC]** (`serie_led_2w`), against LED_1's 3 W.
- **`occasional_use`(LED_2, w) = `occasional_use`(LED_1, w) × 0.93**, where **0.93 ≈ 13/14** is the
  survey-derived share of households with an *active* second bulb. A stable minority runs a single bulb
  (Marcelino's second bulb is burned out, Q33-2; id 49 reports `light_bulb_2_time` = 0). Where the second
  bulb *is* used it is used comparably (`light_bulb_2_time` 5.0 h vs `light_bulb_1_time` 6.0 h), so the
  difference belongs in `occasional_use`, not `func_time`.

### VA5 — Second-room morning light (LED_2)

```yaml
power: 2
num_windows: 1
window_1: [240, 420]
func_time: 126
func_cycle: 63
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.33
```

**Narrative.** Shadows VA1: the same pre-dawn/early-morning rise, in the second room or kitchen, switched
on less often because not every household lights both bulbs.

- **power:** 2 W — **[SPEC]** (`serie_led_2w`)
- **w_1:** `[240, 420]` (04:00–07:00) — **[WINDOW]**, inherited from VA1
- **func_time:** **126 min** — **[WINDOW→margin]**, inherited from VA1: 180 × (1 − 0.30)
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 63 min, not the Flexible ratio.** Same RAMP
  per-window eligibility issue as VA1 above (identical window shape and `random_var_w`) — see VA1's note
  for the full derivation.
- **time_fraction_random_variability:** **0.20** — **[RIG-XW]** Flexible
- **random_var_w:** **0.30** — **[RIG-XW]** Flexible
- **occasional_use:** **0.56** — **[FREQ-XW]** = VA1 (0.60) × 0.93 (active-second-bulb share), **propagated
  2026-07-28** from VA1's own trim to its bin floor (see VA1)

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep), provisional.** Same status as VA1's override; not
re-derived via the ×0.93 shadow rule for the seasonal case (i.e. not 0.28×0.93), matching the flat
0.28 figure given for every LED VA in this seasonal set.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.28
```

### VA6 — Second-room daytime light (LED_2) ⚠ **structural placeholder, not a behavioural estimate**

```yaml
power: 2
num_windows: 1
window_1: [420, 1080]
func_time: 30
func_cycle: 15
time_fraction_random_variability: 0.30
random_var_w: 0.35
occasional_use: 0
status: placeholder_artifact   # window-continuity filler only — see narrative; not a behavioral estimate
```

**Narrative.** Shadows VA2. There is no daytime indoor lighting practice to represent (conservation-logic
veto; households out in the fields), and this VA exists **only** to keep LED_2's windows continuous across
07:00–18:00 so RAMP does not cut a hard artificial notch in the second bulb's aggregate curve.

- **power:** 2 W — **[SPEC]** (`serie_led_2w`)
- **w_1:** `[420, 1080]` (07:00–18:00) — **[WINDOW]**, inherited from VA2
- **func_time:** **30 min** — set to minimise the placeholder's footprint (as VA2)
- **func_cycle:** **15 min**
- **time_fraction_random_variability:** **0.30**
- **random_var_w:** **0.35**
- **occasional_use = 0**, **confirmed 2026-07-28**: same basis as VA2 — the extraction pipeline drops `occasional_use = 0` appliances before they reach RAMP, so this VA is never actually simulated; it exists only to keep LED_2's windows continuous. Previously held at a token `0.02`, now confirmed unnecessary.

**Seasonal override — removed 2026-07-28.** Same reasoning as VA2: with the baseline confirmed `0`, a
nonzero seasonal override would have made this placeholder swing from "never simulated" to "simulated" for
Growing & Free Grazing only. Removed so VA6 stays a non-event year-round, consistent with its own baseline.

### VA7 — Second-room evening light (LED_2)

```yaml
power: 2
num_windows: 1
window_1: [1080, 1320]
func_time: 168
func_cycle: 84
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.84
```

**Narrative.** Shadows VA3, the profile's principal load, in the second room or kitchen — the extended
18:00–22:00 evening, switched on somewhat less often than the main-room bulb.

- **power:** 2 W — **[SPEC]** (`serie_led_2w`)
- **w_1:** `[1080, 1320]` (18:00–22:00) — **[WINDOW]**, inherited from VA3
- **func_time:** **168 min** — **[WINDOW→margin]**, inherited from VA3: 240 × (1 − 0.30)
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 84 min, not the Flexible ratio.** Same RAMP
  per-window eligibility issue as VA3 above (identical window shape and `random_var_w`) — see VA3's note
  for the full derivation.
- **time_fraction_random_variability:** **0.20** — **[RIG-XW]** Flexible
- **random_var_w:** **0.30** — **[RIG-XW]** Flexible
- **occasional_use:** **0.84** — **[FREQ-XW]** = VA3 (0.90) × 0.93 (active-second-bulb share)

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep), provisional.** Same status as the other LED
overrides in this profile; not shadowed via ×0.93 for the seasonal case, matching the flat figure given
for every LED VA in this set.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.28
```

### VA8 — Second-room overnight "hacer amanecer" (LED_2)

```yaml
power: 2
num_windows: 2
window_1: [1320, 1440]
window_2: [0, 240]
func_time: 288
func_cycle: 70
time_fraction_random_variability: 0.10
random_var_w: 0
occasional_use: 0.31
```

**2026-07-28 — briefly retired to a placeholder as part of the VA4 merge experiment, reverted.** See VA4:
the single-overnight-light consolidation was tried and reverted, so VA8 is a real, independent VA again,
shadowing VA4 as before. **`random_var_w` lowered 0.20→0.10 alongside VA4's own change**, same midnight-seam
experiment (see VA4) — kept identical since VA8 inherits its rigidity parameters unchanged from VA4.

**Narrative.** Shadows VA4: where a household leaves a bulb on until dawn, the second bulb participates in
that overnight block less often than the main-room bulb. Same Strict rigidity (one unbroken block ended by
dawn), same no-stated-cause status.

- **power:** 2 W — **[SPEC]** (`serie_led_2w`)
- **w_1:** `[1320, 1440]`, **w_2:** `[0, 240]` (22:00–04:00) — **[WINDOW]**, inherited from VA4. **Moved
  2026-07-28** alongside VA4's own terminus change (see VA4), keeping the two bulbs' overnight boundary
  identical to VA1/VA5's morning boundary.
- **func_time:** **288 min** — **[WINDOW→margin]**, inherited from VA4: 360 × (1 − 0.20)
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 70 min, not the Strict ratio.** Same
  RAMP per-window eligibility issue as VA4 above (identical window shape and `random_var_w`) — see VA4's
  note for the full derivation.
- **time_fraction_random_variability:** **0.10** — **[RIG-XW]** Strict
- **random_var_w:** **0.10** — **[RIG-XW]** Strict, **lowered from 0.20, 2026-07-28**, mirroring VA4's
  midnight-seam-dip experiment (see VA4)
- **occasional_use:** **0.31** — **[FREQ-XW]** = VA4 (0.33) × 0.93 (active-second-bulb share), **propagated
  2026-07-28** from VA4's move to the interview-only reading (see VA4)

### VA9 — Portable-device charging (USB: phone, flashlight, residual radio)

```yaml
power: 2.5
num_windows: 1
window_1: [0, 1440]
func_time: 480
func_cycle: 240
time_fraction_random_variability: 0.30
random_var_w: 0
occasional_use: 1.00
thermal_p_var: 0.2   # DECLARED DEFAULT, pending measurement — see narrative
```

**Narrative.** Charging is the system's core purpose — *"lo utilizamos para cargar el celular"* (Teófilo),
*"el celular es importante para informarse y comunicarse"* (Basilio) — the household routinely charges phones, but not by stacking multiple devices at once. The hardware struggles to charge *one* modern phone
(*"A los celulares grandes no puede cargar… no abastece"* — Basilio; *"no quiere hacer cargar celulares"* —
Felipe), households own 0–3 phones (mean 1.5), and visitors are turned away from charging, not stacked in
(*"Si alguien viene, no hacen cargar"* — Basilio). Timing is unconstrained (*"a veces en la noche, a veces
en el día"* — Basilio), so the window is the whole day and the *quantity* is what varies.

**Radio folded in, not modelled separately.** Radios are broken, missing, or battery-only in most
interviewed households (Bonifacio: sound dead since delivery; Marcelino: *"no me duró ni un mes… se
arruinó"*; Basilio: cable cut for batteries; Felipe: *"la radio se ha roto"*). The exceptions (Martín's
rechargeable radio; Vicente listens) leave a residual charging load that sits inside this VA.

- **power:** 2.5 W — **[SPEC]**. The survey hardware is a single 2.5 W USB port; interviews report undersupply, not the stacked multi-device demand a splitter-based reading would imply.
- **w_1:** `[0, 1440]` (00:00–24:00) — **[WINDOW]**; charging is explicitly unconstrained in time
- **func_time:** **432 min** — **[WINDOW→margin fallback, device-count scaled]**. Base value: the
  interview duration statement — *"Tarda mucho, a veces 4 horas"* (Teófilo) = **240 min**. Protocol §4's fallback
  applies because the margin formula is undefined for a full-day window; ⚠ **do not** substitute the survey
  `phone_N_time` field, which the codebook defines as average daily *use* in hours, not charging hours.
  **Scaling step, made explicit rather than left implicit:** Teófilo's own household charges exactly **one**
  phone (*"Cargamos un celular"*, Q29-11), so 240 min is a **per-device**, not a per-household, figure. VA9
  is a single shared VA standing in for every phone charged through the household's one USB port; where a
  household owns more than one phone, those devices charge **sequentially through the same 2.5 W port**, so
  their durations are structurally additive within the VA's daily on-time — this is not extra dispersion
  (that's `time_fraction_random_variability`, unchanged below), it is a shift in the *typical* total. The
  survey's own ownership data gives the scaling factor: among the **12/14 Profile-3 households that own at
  least one phone**, `phones` averages **2.0** (24 phones ÷ 12 owning households — `phones`: 7=2, 13=2,
  15=3, 30=3, 31=3, 33=2, 38=1, 49=1, 67=2, 69=1, 75=2, 78=2), not 1.0. `func_time = 240 × 2.0 = 480 min`.
  **[SPEC]-tier ownership evidence, full N_survey**, per the protocol's population table — this is a
  structural fact, not a qualitative one, so it draws on all 14 households rather than only the 9
  interviewed.
- **func_cycle:** **240 min** — **[RIG-XW → func_time]**: Chaos ≈ 0.5 × func_time, recomputed from the
  scaled figure; still coherent with a single-device charge cycle repeated across ≈2.0 devices rather than one longer session
- **time_fraction_random_variability:** **0.30** — **[RIG-XW]** Chaos: timing unpinnable and quantity contested by supply. Unchanged — this governs day-to-day *dispersion* around the mean, a separate axis from the ownership-driven shift in the mean itself
- **random_var_w:** **0** — **[RIG-XW], structurally forced.** A 24 h window has no width left to randomise — the protocol's decisive case for why the two variability parameters are decoupled (0 vs 0.30), reproduced here
- **occasional_use:** **1.0** — **[FREQ-XW]** *Daily/Fixed* bin, taken at the ceiling. The survey's `phones`
  field reads 0 for two households (ids 29, 61), but **both are directly contradicted by their own
  interview**, not merely under-specified by it: Basilio explicitly confirms personal phone ownership and
  daily use — *"¿Usas celular, Don Basilio? ¿Haces cargar? ¿Carga bien?"* → **"Sí, normal; carga siempre"**,
  and *"todos hacemos cargar el celular"* (id 61, 19/11/24) — and Teófilo's household states plainly
  *"Cargamos un celular"* (id 29, 24/02/26). Unlike the protocol's usual single-period-question limitation
  (a categorical code that structurally cannot express a nuance), a phone-count field has no such structural
  excuse to be wrong — this reads as a survey data-entry or timing artifact, not a genuine ownership gap, and
  is treated here as a **Say-Do conflict resolved toward the interview**, a deliberate departure from the
  protocol's default tier-4 survey-wins tiebreak, stated explicitly as the judgment call it is (protocol
  §9's spirit: "document whichever choice is made, and why, at the point it's made"). With that reading,
  **9 of 9 interviewed households** report charging a phone — including Apolina (7, *"En cualquier hora que
  sea conveniente"*) and Dionisio (67, *"en cuanto se termina su batería, lo hacemos cargar"*) — two of them
  (Basilio, id 61; the wife, id 69: *"Yo hago cargar mi celular siempre porque lo necesito para linterna"*)
  with the explicit **"siempre"** marker that is Table A's own Daily/Fixed anchor language, and **no
  interviewed household states a skip pattern for charging itself** (as distinct from supply-side outages, a
  separate axis — see the caveat below).
  > **Recorded tension, not resolved by this change.** VA3 (evening light, same profile) was deliberately
  > held at 0.90 rather than 1.0 for a *supply*-side reason (R-D: cloud/rain outages, including weeks-long
  > loss for id 29). Charging is, if anything, *more* exposed to that same supply constraint — Teófilo
  > states outright that *"el panel solo se activa para cargar a través de la radiación solar."* Internal
  > consistency with VA3 would argue for the same ~0.90 ceiling here rather than a literal 1.0. This file
  > implements **1.0** as a stated preference — the intent/routine is genuinely universal in the interviewed
  > sample and is not itself in question — while flagging that a supply-side discount analogous to VA3's is
  > the more internally consistent alternative if RAMP's own generation model does not already suppress
  > charging events during real outages. Revisit together with VA3 if the two are found to diverge in
  > practice.
- **thermal_P_var:** **0.2** — **[DECLARED DEFAULT]**, pending measurement. RAMP's parameter name references thermal variability; the mechanism invoked here is **CC-CV current taper** as a battery approaches full charge, compounded by device-type heterogeneity — now more clearly motivated, since a typical household is cycling ~1.8 devices of different types (phones, and occasionally a rechargeable radio or flashlight) through the same port. Not measured; flag any downstream result sensitive to the figure.

> **Why this is not the same move as Profile 2.** Profile 2 (isolated elderly) genuinely clusters near
> one phone per household and 2/11 households own none — device-count scaling there would multiply by
> ≈1.0 and change nothing, which is why Profile 2's file leaves `func_time` at the single-device figure.
> Profile 3's 1.8-device mean is a real, profile-specific difference (larger, more populous households),
> not a uniform assumption applied across profiles — consistent with the user's original intuition that
> more people plausibly means more phones, checked here against the actual ownership counts rather than
> assumed from household size directly (the correlation between `fam_members` and `phones` is in fact weak
> across individual P3 households — id 69 has 7 members but only 1 phone, id 13 has 4 members and 2 phones —
> so the scaling is anchored to the survey's ownership field itself, not to occupancy as a proxy for it).

**Seasonal override — Growing & Free Grazing (Feb–Apr, Jul–Sep), provisional.** Duration effect only, consistent
with the same treatment used for the equivalent VA in Profiles 1 and 2; frequency (`occasional_use`)
stays at baseline.

```yaml
seasons: [growing, free_grazing]
func_time: 360
```

---

## 6. Seasonality

The four-season agricultural calendar (planting Oct–Jan; growing/early harvest Feb–Apr; harvest May–Jun;
free grazing & migration Jul–Sep) is retained as **context**, but its energetic consequences are re-derived,
because per-VA `occasional_use` edits (0.71, 0.14, …) would imply a measured season→behaviour
link the study never collected.

1. **The dominant seasonal mechanism is *structural absence*, not behavioural tuning.** Profile 3 is
   genuinely mobile: 10/14 migrate, and the interviews describe departures to the *monte* (Marcelino), the
   mine (Primitivo's family), Saipina (Basilio), and Chapare (Rivera's kin). Martín Salazar's household is
   absent *"a veces seis meses"* — the protocol's named Profile-3 structural-absence anchor. During the
   Jul–Sep grazing/migration window these households empty, and the correct model response is the
   **household-level structural-absence mechanism** (suppress *all* VAs for the absent period), **not** a
   dozen edited `occasional_use` values. This is the intended target of the deferred occupancy feature.

2. **No *evidenced* behavioural seasonal VA variant exists.** Kin visits and community events — the only
   plausible uplift — were never measured, and are treated as **Chaos**, already carried in VA3's and
   VA9's variability. §5 nonetheless carries a **provisional** Feb–Jun override set (VA1/2/3/5/6/7
   `occasional_use` → 0.28, VA9 `func_time` → 360 min) for full-year visualization purposes, following
   the same pattern used for Profile 1 — each flagged individually in §5 as a sensitivity variant, not a
   re-derived finding. The position stated in point 1 above is unchanged by adding it: the mechanism that
   actually matters for this profile is structural absence, not per-VA tuning.

3. **The remaining defensible seasonal effect runs through *supply*.** The rainy season (Dec–Mar) suppresses
   generation for days-to-weeks at a time (*"a veces demora semanas en recuperarse"* — id 29), already
   reflected in VA3's supply-discounted `occasional_use = 0.90`. If seasonality is modelled explicitly for
   this profile, it belongs on the **generation** side, not in behavioural parameters.

---

## 7. Provenance (anchor quotes → parameters)

| Respondent (id, date) | Anchor | Feeds |
|---|---|---|
| Teófilo Vallejos / Isabel Zurita (29, 24/02/26) | *"aproximadamente hasta las 10:00 de la noche, y muy pocas veces por las mañanas"* | VA3 `w_2`; VA1 `occasional_use` discount |
| Teófilo (29) | *"para ir a terminar el trabajo de campo, utilizamos linterna"* | Outdoor-LED retirement |
| Teófilo (29) | *"ya se apagó tres veces… a veces demora semanas en recuperarse"* | R-D; VA3 supply discount; resolves protocol open item |
| Teófilo (29) | *"Tarda mucho, a veces 4 horas"* | VA9 `func_time` |
| Marcelino Sánchez (33, 25/03/26) | *"Desde las 7:00 de la noche… hasta las 8:00"* | VA3 short-end evidence (Flexible bin) |
| Marcelino (33) | *"Nosotros vamos al monte a trabajar"* | R-E structural absence; daytime veto |
| Apolina Vallejos (7, 25/03/26) | *"Estuve durante tres meses y no hice alumbrar, no prendimos la luz"* | R-E structural absence (concrete household-level anchor) |
| Apolina (7) | *"A veces desde las 5 o 6 de la mañana generalmente; y desde las 7 de la noche hasta las 8, a veces 9 o 10"* | VA1/VA3 window corroboration |
| Apolina (7) | *"En cualquier hora que sea conveniente"* | VA9 full-day window; occasional_use |
| **[FIELD MEMO, caseid 53]** Apolina manages the household for her son Rodolfo while the parents work in the mines; frequent migration to Chapare | corroborates R-E structural-absence pattern and household composition |
| Dionisio Vargas Castro (67, 25/02/26) | *"Nosotros solo vivimos... esposo y esposa... aquí viene de vez en cuando"* (re: adult daughter) | family-structure evidence (extended-on-paper, emptied-in-practice, §1) |
| Dionisio (67) | *"Nosotros generalmente la usamos en las noches, todo el año"* | VA3 window/frequency corroboration |
| Dionisio (67) | *"A veces lo cargamos en el día o en la noche... en cuanto se termina su batería, lo hacemos cargar"* | VA9 full-day window; Chaos timing |
| Dionisio (67) | *"No, no; constantemente está aquí, no lo trajino a ningún lado"* | Rule 7-equivalent: hardware kept at home, not transported |
| Basilio Salazar (61, 25/02/26) | *"desde las 7 de la noche hasta la madrugada… no se apaga; amanece alumbrando"* | VA4 existence (Strict overnight) |
| Basilio (61) | *"A los celulares grandes no puede cargar… no abastece. Si alguien viene, no hacen cargar"* | VA9 undersupply |
| Basilio (61, 19/11/24) | *"El celular lo hago cargar durante el día"* / *"a veces en la noche, a veces en el día"* | VA9 full-day window; Chaos timing |
| Felipe Rivera (69, 20/11/24) | *"Desde las 6 de la tarde alumbra por mis hijos, hasta las 10 de la noche"* | R-A extended evening; VA3 window |
| Felipe (69) | *"a veces amanece prendido con luz… no se apaga"* | VA4 corroboration (survey code 13) |
| Felipe (69) | *"Antes había vinchuca… ya con esta iluminación nos dimos cuenta"* | VA4 = *no* stated overnight cause (rules out the "security" framing) |
| Felipe (69) | *"lo necesito para linterna, para alumbrar"* | Outdoor-LED retirement |
| Martín Salazar household (78, 25/03/26) | *"cuando hacemos las tareas… no la apagamos… al amanecer apagamos, como a las 6 de la mañana"* | VA4 dawn terminus; homework-anchored evening |
| Martín Salazar household (78) | *"a veces seis meses, algo así"* | R-E; §6 structural absence (profile anchor) |
| Primitivo Agreda household (38, 25/03/26) | *"encendemos la luz de 7:00 a 10:00 de la mañana… para cocinar"* | VA1 morning corroboration (thin: respondent non-resident) |
| Bonifacio Molina (13, 21/11/23); Marcelino (33) | radio dead since delivery / *"no me duró ni un mes"* | Radio retirement (folded into VA9) |

Survey fields used: `light_1/2_morning`, `light_1/2/3_night` (modal codes), `light_bulb_1/2_time`,
`wakeup_time_after`, `sleep_time_after`, `light_bulbs`, `radios`, `phones`, `other_illum`, `occupation`,
`family_type`, `fam_members`, `adults_mas_60`, `migration`/`summer_migration`, `cooking_fuel_biomass`,
`serie_led_2w`/`serie_led_3w`.

**Field-memo coverage (Protocol §2.1).** In addition to Apolina's memo (caseid 53, cited above), seven
other interviewed households have a corroborating field memo: Bonifacio (13, caseid 11), Teófilo/Isabel
(29, caseid 2), Marcelino (33, caseid 13), Primitivo (38, caseid 22), Basilio (61, caseid 35), Felipe
(69, caseid 52), Martín (78, caseid 8). Dionisio (67) has no memo on file. None of the memos contradict
the transcript-based values above; they corroborate household composition, migration pattern, and
hardware inventory, consistent with their role under the protocol's evidence-tier rules.

---

## 8. Open items carried forward

- [x] **2026-07-28 — VA4/VA8 overnight terminus moved from 05:00 to 04:00, fixing a same-hardware overlap.**
      VA1 (and its LED_2 mirror VA5) start at 04:00 (`[240,420]`), but VA4/VA8's overnight tail ran to 05:00
      (`window_2: [0,300]`) — a 60-minute overlap on each bulb between the overnight VA and the morning VA
      sharing it. Tails shortened to `[0,240]`; combined window narrows 420→360 min, so `func_time` drops
      336→288 for both VA4 and VA8 (`func_cycle` unchanged at 70, since it's constrained by the untouched
      120-min evening-tail window, not the pre-dawn one). ⚠ Caveat carried forward: the evidenced terminus
      is dawn itself (≈05:00–06:00 per interview quotes), so this is a modeling-consistency fix, not a
      re-derivation from new evidence.
- [x] **2026-07-28 — confirmed: `occasional_use = 0` VAs are dropped before reaching RAMP.** VA2 and VA6
      moved from their token `0.02` to a literal `0`; both remain in the markdown only for window-continuity
      documentation, no longer actually simulated. Their Growing & Free Grazing seasonal overrides (which
      had set `occasional_use = 0.28` for those months) were removed the same day for consistency — both
      VAs now stay a non-event year-round rather than swinging to "simulated" for two seasons only.
- [x] **2026-07-28 — VA1 trimmed to its bin floor (0.65→0.60); VA4 moved to the interview-only reading
      already cited in its own text (0.25→0.33).** Neither is a new derivation: VA1 stays in the High
      frequency bin but leans further into Teófilo's hedge; VA4 moves from a stated compromise between
      3/14≈0.21 and 3/9≈0.33 to the top of that same cited range. VA5/VA8 (LED_2 shadows, ×0.93) propagated
      accordingly: VA5 0.60→0.56, VA8 0.23→0.31.
- [x] **2026-07-28 — VA4/VA8 single-overnight-light merge tried, then reverted same day.** VA4/VA8 were
      briefly consolidated into one "whichever bulb" VA (`occasional_use` union ≈ 0.54, at LED_1's 3 W),
      mirroring Profile 2's fix, then reverted back to the independent two-bulb version (VA4 = 0.33,
      VA8 = 0.31) — unlike Profile 2, Extended Hub households can plausibly run two overnight lights at
      once, so the merge was an experiment, not a correction of an implausibility, and the split version
      was kept.
- [x] **2026-07-28 — VA4/VA8 `random_var_w` lowered 0.20→0.10, testing the RAMP midnight-seam dip.**
      Overnight-spanning appliances split into two independently-jittered windows in RAMP; the two edges
      meeting at midnight only bridge into one continuous block on days where jitter happens to land
      exactly at the true boundary — close to a coin flip regardless of `random_var_w`'s magnitude, which
      an isolated 300-day test confirmed (minute-0 coverage ~41% of mid-window at 0.20 vs ~42% at 0.10 in
      that isolated test — real improvement only appears much closer to 0). Testing 0.10 against actual
      validation data anyway, since the isolated test isn't the same as checking against the real baseline.
      `func_cycle=70` remains valid (floor loosens from 72→96 min at the 120-min evening-tail window).
      **Revert to 0.20 if validation doesn't show a real improvement** — 0.20 was the original Strict-tier
      value, not a value chosen incorrectly.
- [ ] **VA4 seasonal-override spec conflict, not resolved here.** The instruction this seasonal set was built from states VA4 stays at baseline during Growing & Harvesting, then separately lists an explicit value (0.57) for it that does not match VA4's actual baseline (0.33). No VA4 override was added, following the stated rule rather than the numeric value — confirm which was intended before treating VA4 as settled for the seasonal case.
- [ ] **Name the between-household asymmetric-anchor limitation in §5.4** (VA3: Strict-anchored evening in the school-child subset, loose/short in the childless *extendido* subset, one Flexible bin). Distinct from Profile 2's *within-account* version; both are limitations of a single-bin rigidity crosswalk.
- [ ] **Reconsider the profile name / criterion.** "Extended Hub" describes family structure, but co-residence and load intensity are frequently much lower than the label implies (ids 33, 61, 67 behave like Profile 2; id 7 behaves like a generational-relay household). Consider reporting occupancy as intermittent, and stating that only a subset (ids 69, 78, and the larger *numeroso* households) realise the "hub" load in practice.
- [ ] **VA4's flat `occasional_use` is a category mismatch at household level** (a stable minority practice modelled as a uniform daily probability). Confirmed adequate under the current profile-averaged Tier-2 design; revisit if per-household metrics are introduced.
- [ ] **Structural-absence occupancy feature** — Profile 3 is the clearest test case (real, multi-month, interview-attested absence in ids 7 and 78). When the deferred occupancy feature lands, wire it here first rather than editing behavioural parameters (§6).
- [ ] **Check the not-interviewed households (ids 15, 30, 31, 49, 75)** for representativeness on overnight-light and migration prevalence — there is no survey field that independently verifies dual-residence, so the interview subset's pattern is inherited without a check (protocol limitation).
- [ ] **VA9 `occasional_use = 1.0` vs VA3's supply-side 0.90 — resolve jointly.** Both VAs draw on the same
      PV supply, and R-D documents the same reliability issue (id 29's weeks-long outages) for both. VA3 is
      discounted to 0.90 for this reason; VA9 is deliberately left at 1.0 despite the same reasoning applying,
      per a stated preference. If a supply/generation-side mechanism is introduced instead of
      folding reliability into `occasional_use`, both values should be revisited together rather than
      independently.