# Profile 4: The System Breakers — RAMP truth file (protocol-applied)

> Derivation authority: `parameter_derivation_protocol.md` (§3.3.1.1). Every parameter below carries its
> derivation tag — **[SPEC]**, **[WINDOW]**, **[FREQ-XW]**, **[RIG-XW]**, **[RIG-XW → func_time]**,
> **[DECLARED DEFAULT]**. No value is left without a declared basis.

```
Population: N_survey = 12 (ids 23, 25, 27, 40, 42, 54, 64, 65, 71, 76, 92, 96; classified via
            family_type/occupation/children_in_school/migration/portability_shs, per
            `classifications_oficial.csv`. Ids 58 and 83 — which the official source places here —
            are held in Profile 1 instead, by an analyst override; ids 54 and 64 — which the official
            source places in Profile 1 — are held here instead, by the same kind of override. Both
            overrides are stated and reasoned in §2, Rule 9.)
            N_interview = 6 (Evangelino Coca 23 [respondent: Gregoria Inturias, esposa], Rodolfo
            Agreda 40 [respondent: Severino Agreda, hermano], Zenón García 54 [respondent: la hija],
            Celestina Inturias 64, Florencio Rivera 76 [respondents: esposa, then esposo], Guillermo
            Romero 96. Not interviewed: ids 25, 27, 42, 65, 71, 92.)
            Coverage 50% (6/12) — the thinnest qualitative base of the four profiles, and the profile
            carrying the dual-residence / structural-absence claims that most need it.
Generalization: all qualitative parameters below (Windows, Rigidity, occasional_use, and the
household-level structural-absence axis) are inferred from N_interview and applied uniformly to all
N_survey households at simulation time. `migration_label` is not used as the absence trigger — it is
true for 5 of 10 valid records here (missing for id 65) without discriminating a genuine dual-residence
pattern from ordinary short-term labor migration; the diagnostic signal is explicit dual-household or
extended-absence language in interview, per Protocol.
```

---

## Methodological basis

Two distinct phenomena sit inside this profile, and keeping them separate is the key to reading it
correctly. **Household-level structural discontinuity** — a subset of these households is intermittently
absent, transports the hardware seasonally, or splits life across two residences — is real and is the
profile's genuine distinguishing feature. Per the protocol it is a household-level axis that suppresses
*every* VA simultaneously during absence, handled by the (deferred) occupancy feature, not encoded as low
`occasional_use` inside each appliance — doing so would double-count the effect and mislabel a describable
routine as chaotic. **Per-appliance routine when the household IS present**, by contrast, is not chaotic:
across all six interviews the occupied-household rhythm is ordinary and describable — wake 04:00–06:00, an
evening light block 18:00/19:00–22:00 for dinner and homework, phone charging valued above all else, sleep
21:00–22:00. Rigidity is a property of *the practice when it occurs*, read from how the respondent
describes it, never inherited from the household's overall life-instability.

Daytime indoor and outdoor light (VA2, VA6) are retired as **true findings, not token placeholders**: no
respondent reports daytime electric lighting, daylight suffices, and daytime work (including weaving) is
done in natural light. The resulting 08:00–18:00 zero is physically real, so — unlike Profiles 2 and 3's
equivalent gap — no continuity placeholder value is used here; the window-continuity rule exists to
prevent *artificial* drops where real use continues, and this drop is correct, not artificial. VA3
(evening light) carries `occasional_use = 1.0` uniformly across all households by a stated decision, not a
re-derived crosswalk value: subsistence dinner alone is a nightly, non-negotiable need independent of
whether children are in school, which matters because `children_in_school` itself is unreliable for this
profile (it conflicts with the qualitative record for Guillermo — see §8) but that unreliability doesn't
touch this parameter, since the value no longer depends on the field. `func_time` values grounded in a
narrative duration rather than the window-margin formula are tagged **[NARRATIVE — margin rule does not
apply]** rather than [WINDOW→margin] — VA1, VA5, VA7, and VA8 describe brief, event-driven practices where
the margin formula would overstate duration by several multiples; VA9's `func_time` is grounded directly
in Guillermo's own two-session description (~1 hr morning + ~2–3 hrs night, midpoint 210 min), not an
interviewer's single-session paraphrase, which was explicitly not used since Guillermo pushed back on it
before giving the settled two-session answer. VA9 additionally carries a weather-linked component folded
into Chaos-level `time_fraction_random_variability` rather than a separate trigger mechanism, per the
protocol's retired conditional-VA resolution: Florencio ties daytime charging to rain directly, and
Zenón's household independently corroborates the same underlying supply unreliability with a dated
cloud-outage account. `migration_label` is non-diagnostic here, consistent with the protocol's general
finding — the discriminating signal is dual-household language (Guillermo) and explicit extended-absence
timeframes (Rodolfo), both interview-only. `thermal_P_var = 0.2` **[DECLARED DEFAULT]** per Protocol §9.

**Field-memo coverage.** All six N_interview households have a corroborating field memo, and several
resolve genuine ambiguities the transcript alone leaves open: Evangelino's household structure (single
residence, three accumulated panels, not a second house), Florencio's second-house power source (an
independent system, not carried equipment), an apparent second-interview discrepancy for Rodolfo
(confirmed only one transcript exists), and two structural readings this reconciliation itself surfaced —
Zenón's two-house energy strategy and Celestina's two-separate-systems residence pattern (see §2, Rule 9).

---

## 1. Demographic summary

This profile is best read as two overlapping populations rather than one uniform "chaotic" group. On
paper it is defined by mobility and hardware unreliability, but the appliance-level routine of a present
household is ordinary — the instability lives entirely in *whether* the household is home, not in how it
behaves when it is. All six interviewed households show genuine household-level mobility or absence
(Evangelino, Rodolfo, Florencio, Guillermo, Zenón, Celestina) — this is the profile's actual
distinguishing feature, not an artifact of a noisy sample. **Florencio (76)** is the clearest example:
conservation-oriented and rhythmically consistent when present (*"cuando no estamos utilizando la
apagamos… si no hay nadie no dejan la luz prendida"*), while the household genuinely empties during his
and his wife's time at their second house. **Zenón García's household (54)** and **Celestina Inturias's
household (64)** add two more instances of the same pattern from a different angle: Zenón's household does
its actual task-lighting and charging at a second, grid-connected house, not at the SHS house at all;
Celestina maintains two separate solar systems and alternates between them roughly every two weeks. The
"System Breaker" signature lives in the household-occupancy axis, not in the appliance parameters.

**Interviewed household night-window codes are tightly clustered** for the original four
(`light_1_night` ∈ {1821, 1822, 1922}); Zenón's and Celestina's households fit the same evening/dinner-
and-sleep pattern by interview account, though neither adds a matching night-window survey code (see §4,
Window 3, and §5 VA4).

---

## 2. The driving social rules

- **Rule 7 — Infrastructure mobility.** Applies to a subset, confirmed by interview and field memo, not
  universally. Transported: Evangelino/Gregoria (*"a veces lo llevo… por eso lo llevo, porque cuando voy
  allá no hay luz"*, 23) — **[FIELD MEMO, caseid 9]** confirms this is genuinely a Rule 7 case and closes
  an earlier open question about a possible second house: *"Gregoria is a seasonal migrant who works
  'below' from December to Carnival. They are 'power users' with three separate solar panels."* Three
  panels, one household, no second residence — the multiple panels mentioned in the transcript are
  accumulated hardware at a single home, not evidence of a second house. Firmly kept at home: Guillermo
  (*"No, siempre está aquí"*, 96). `portability_shs` corroborates the split (transported for 23; kept-home
  for 76, 96). Rodolfo (40) is **not** a Rule 7 case: the 2024 transcript's `portability_shs = 0` reflected
  his brother's seasonal comings-and-goings with a battery/chainsaw kit at the time, not the SHS itself
  moving; the household has since relocated wholesale (Rule 9), which supersedes the transport question
  entirely. Florencio (76) is also not a Rule 7 case: the field memo confirms two separate houses each
  with their own system — nothing physically travels between them.

- **Rule 9 — Dual-home displacement / relocation.** Confirmed for five households, each with a dated,
  attributable field memo in addition to interview evidence.

  **Guillermo Romero (96).** Interview: grid-connected second residence paying ELFEC — *"Generalmente yo
  estoy aquí; mi esposa a veces"* + *"Pagamos 18, 19, a veces 20 Bs"* (25/02/2026). **[FIELD MEMO, caseid
  57]** directly corroborates the dual residence and ELFEC payment, and independently corroborates several
  appliance-level details already in this file: the single school-aged child, the ~1-hour morning /
  few-hours-evening light use, the broken radio cable, and minimal panel-cleaning out of fear of damage.
  Not memo-sourced, remaining conversational-only: that his father and aunt maintain their own separate
  houses/systems at Sillar, and that Guillermo works as a salaried authority (internal transcript
  corroboration for the authority claim stands independently — A1/A3, 21/11/2023). Guillermo's Sillar
  house is genuinely empty during his absences — no resident kin sustain it.

  **Rodolfo Agreda (40).** The 2024 interview (with brother Severino standing in as respondent) describes
  a short seasonal labor trip — *"se quedará un mes… en enero ya va a estar aquí"*. **[FIELD MEMO, caseid
  47]** confirms the relocation directly and in writing: *"Rodolfo migrates for work to the mines and goes
  back rarely to his house in Raqaypampa… Domestic needs are met by one panel"* — superseding the 2024
  "back in January" account with a permanent relocation, and confirming the single-panel hardware already
  in this file. The memo's "first interview... second..." phrasing initially suggested a possible second
  transcript; checked directly against `all_transcripts.txt`, only one interview (20/11/2024) exists, so
  this is read as referring to something other than a missing data source. Still conversational-only: that
  the new job is in a contiguous grid-connected community, and that Severino's own household has since
  left too (not just Rodolfo's nuclear family).

  **Florencio Rivera (76).** The wife states plainly: *"una de mis casas está abajo. Tengo dos casas."*
  This meets the protocol's diagnostic bar directly — an explicit two-residence statement, not an inference
  from `migration_label`. The occupancy consequence is also interview-confirmed: asked who stays behind
  when she is at the second house, she answers *"Ah, no; lo voy a guardar"* — nobody remains. **[FIELD
  MEMO, caseid 48]** resolves the second house's power source: *"two systems in two separate houses...
  power at both their upper and lower residences"*, with a concrete seasonal window (**December–June**) —
  the most precisely dated occupancy pattern of the three, and the most fully resolved case (an
  independent system, not carried equipment).

  **Zenón García (54).** The daughter (respondent) describes a grid-connected second house where the
  household's actual task-lighting and charging happens: *"Sus tareas y algunos trabajos... los realizamos
  en nuestra otra casa generalmente... si es en la otra casa donde hay luz de ELFEC, ahí nos vamos para
  hacer eso."* The SHS house is minimal: *"Aquí no hacemos ninguna actividad; solo lo usamos para
  prepararnos la cena, comer y luego dormir."* **[FIELD MEMO, caseid 6]** independently corroborates this
  as a multi-source strategy across two houses. **Flagged tension, not resolved:** later in the same
  session, a second respondent ("Luis," unclear relationship to the household) states the panel never
  moves and the household never travels. Not treated as decisive against the daughter's earlier,
  memo-corroborated account, but a genuine ambiguity — and unlike Florencio's case, no independent evidence
  shows the SHS house standing genuinely empty during the household's time at the second house, so this
  may be a narrower "commute for tasks" pattern; treat the occupancy consequence as weaker than Florencio's
  until clarified.

  **Celestina Inturias (64).** Her own account describes alternating residence roughly every two weeks:
  *"Nosotros estamos aquí como dos semanas... Por eso llevamos el sistema y, cuando volvemos aquí, también
  lo traemos."* Read alone this suggests one system carried between houses (a Rule 7 pattern). **[FIELD
  MEMO, caseid 21]** gives a more precise structural account: *"she alternates residency between two
  houses every two weeks. She maintains two solar systems, one for each residence"* — adopted as the more
  reliable reading (a dated, dedicated visit note over a respondent's casual phrasing), making her case
  closer to Florencio's (two independent systems) than to Evangelino's (transported hardware). She also
  gives a direct overnight-light account with a stated cause, unlike the profile's other overnight case
  (see §4, Window 4) — *"con esa luz duermo tranquila y tampoco tengo miedo"* + *"me picó un bicho, creo
  que era alacrán... Ahora que hay luz, ya no hay bichos que nos piquen."* **Flagged tension:**
  `classifications_oficial.csv`'s `portability_shs = Yes` (kept mostly at home) conflicts with the
  alternating-residence pattern the transcript and memo both independently describe.

  **Model consequence for all five.** Self-reported presence is overstated relative to what actually
  happens: 3 of 6 interviewed households (Guillermo, Rodolfo, Florencio) are confirmed genuinely-empty-
  during-absence, all with a dated field memo, and zero show a resident-baseline offset (kin sustaining a
  load during the recipient's absence). Guillermo's father and aunt, for instance, maintain their own
  separate houses and systems, not his. The working assumption for occupancy modeling should therefore be
  a single directional bias — self-reports overstate presence — not an offsetting resident-use bias, and
  self-reported presence should be treated as an upper bound throughout. Zenón's and Celestina's households
  add two more dual-residence cases whose occupancy consequence is real but less precisely characterized,
  so the true genuinely-empty rate could run as high as 5/6 pending the two flagged tensions above. This is
  the household-level axis the (deferred) occupancy feature is meant to implement — it suppresses *every*
  VA simultaneously during absence and is never re-encoded as low `occasional_use` on individual
  appliances, which would double-count the effect and mislabel a describable routine as chaotic.

  **Ids 58 and 83, and why they are not here.** `classifications_oficial.csv` places Albino Acosta (58)
  and Pascual Zurita (83) in Profile 4. Both are treated here as Profile 1 members instead, per a
  documented qualitative override: both describe sustained, unqualified sedentariness with no
  dual-residence or extended-absence statement in either transcript, and both carry young,
  school-relevant children — Profile 1's defining demographic, not this profile's mobility signature.
  Their evidence is cited under Profile 1's file, not here; the conflicting survey fields behind the
  override (Albino's `migration = Yes`, tied to a son's nearby work rather than household relocation;
  Pascual's `portability_shs` value, which points toward Profile 4 against his own `migration = No`) are
  carried there as flagged, unresolved tensions.

- **Rule 13 — Hardware resignation.** Broken radios abandoned rather than repaired across the subset:
  *"solo funcionó un mes nomás"* (Rodolfo, 40); Evangelino, Florencio, and Guillermo all report dead or
  faulty radios still in place. **Model consequence:** radio charging load is near-zero for most of the
  profile; USB load is dominated by phones.

---

## 3. Appliance inventory — [SPEC]

| Device | Count / evidence | Placement | Power |
|---|---|---|---|
| LED_1 | ~2 focos reported by Evangelino, Rodolfo, Florencio, Guillermo; Zenón's household reports two as well, both indoors (*"aquí dentro solo en dos cuartos alumbramos"*, daughter, 54); Celestina's inventory not separately itemized in her transcript | Main room (indoor) | 3 W |
| LED_2 | as above (paired hardware) | Yard / transit point (outdoor) | 2 W |
| USB port | phone is the most-used device in every interview (*"el celular usamos más"* — Rodolfo 40; *"solo mi celular lo hago cargar"* — Guillermo 96); Zenón's household instead charges only the radio at the SHS house — larger modern phones explicitly *"no cargan"* there, with real phone charging happening at the second, grid-connected house | — | 2 W |

Radio hardware is a near-universal casualty (Rule 13): dead or faulty in four of six interviewed
households, leaving USB load dominated by phone charging rather than a mixed device inventory.

---

## 4. Daily social practices and anthropological windows

*Windows are the outer bounds of the Anthropological Window (interview × survey × physical anchors) —
the broadest cultural envelope RAMP may place events within, not periods of continuous draw.*

> **Modal code, defined once.** The survey does not record clock times for lighting; it records a
> **categorical period code**, and the modal code is the code most respondents actually chose, taken
> whole, bounds and all — not a median or average of window widths, which would manufacture a window no
> respondent reported (Protocol §3).

### Window 1 — Pre-dawn / morning preparation (04:00 – 08:00) → `[240, 480]`

Where used, a brief pre-dawn light for preparing food, readying school children, and gathering tools
before leaving — efficient and task-specific. **Not universal:** Florencio uses only phone/radio in the
morning (*"No hacemos alumbrar; lo único que utilizamos es el celular"*, 76), so morning indoor light
carries a below-1 `occasional_use`, not an education override.

**Grounding:** `light_1_morning` interviewed modal cluster (0306/0408/0508/0510 — start 03:00–05:00, end
06:00–08:00), union bounded below by the earliest credible pre-dawn code and above by sunrise;
`wakeup_time_after` 4–6.

*Practices: rising, lighting for food prep and school readiness, gathering tools.*

### Window 2 — Daytime work / school, near-zero electric lighting (08:00 – 18:00) → `[480, 1080]`

Labor is outdoors or in daylight; indoor and outdoor electric lighting is practically absent — this
window exists as a boundary between morning and evening use, not as a lighting load.

**Grounding:** interview day-work statements (Florencio away 09:00–15:00/16:00; general *"en el día vamos
a trabajar"*); daytime weaving/spinning done in natural light — *"durante el día tejemos; no utilizamos la
luz"* (76).

*Practices: agricultural labor, school, daytime handwork in natural light.*

### Window 3 — Evening core gathering and education (18:00 – 22:00) → `[1080, 1320]`

The main living space becomes a multi-use focus: dinner, homework, socializing. This is the most
structured and best-anchored period across all six households, not a chaotic one — `occasional_use =
1.0` uniformly, since evening cooking/dinner alone is treated as a nightly, non-negotiable need that
doesn't depend on whether children are in school.

**Grounding:** `light_1_night` modal **1822 (18:00–22:00)**, corroborated by two independent interview
quotes — *"hasta las 10 de la noche"* (Guillermo, 96); *"6 de la tarde hasta las 10"* (Rodolfo, 40) —
with Florencio slightly narrower (*"7… hasta las 9 o 10"*, code 1922).

*Practices: food preparation and dining, homework/study, socializing.*

### Window 4 — Nighttime sleep and passive overnight security (22:00 – 04:00) → `[1320, 1440] ∪ [0, 240]`

A subset leaves a light on overnight for security/comfort — a passive continuous load, not task lighting.
Household-level heterogeneity, prevalence 2 of 6 interviewed; real caution given the small N. **Not
uniformly "no stated cause":** Evangelino gives no reason, but Celestina gives an explicit one — *"me picó
un bicho, creo que era alacrán... Ahora que hay luz, ya no hay bichos que nos piquen"* — insect safety,
plus a direct denial of fear (*"tampoco tengo miedo"*), ruling out a companionship/fear framing for her
specifically. Modeled as a flat low `occasional_use`, adequate under this paper's profile-averaged
validation given the two-household evidence base is too thin to split into caused/uncaused sub-bins.

**Grounding:** minority overnight-on report — Evangelino *"no se apaga"* (23), Celestina *"No se apaga
para nada... con esa luz duermo tranquila"* (64) — against explicit contradiction from Florencio (*"si no
hay nadie no dejan la luz prendida"*, 76). Survey single-code fields do not capture overnight-on for any
household here — the same enrichment layer as Profile 1's VA4.

*Practices: sleep; passive security light (subset).*

---

## 5. Virtual Appliance parameterisation

*VA numbering follows the same 9-slot schema used across Profiles 1–3, so slot numbers are comparable
across profiles even where a slot is retired for this one.*

### Parameter summary

| VA | Hardware | Window (min) | Rigidity | power | func_time | func_cycle | t_f_r_v | random_var_w | occasional_use |
|---|---|---|---|---|---|---|---|---|---|
| VA1 Indoor morning light | LED_1 | [240, 480] | Flexible | 3 W | 90 | 55 | 0.20 | 0.30 | 0.42 |
| VA2 Indoor daytime light | LED_1 | — | **retired** | — | — | — | — | — | — |
| VA3 Indoor evening light | LED_1 | [1080, 1320] | Strict | 3 W | 192 | 134 | 0.10 | 0.20 | 1.00 |
| VA4 Indoor overnight light | LED_1 | [1320, 1440] ∪ [0, 240] | Strict (engine-constrained) | 3 W | 288 | 70 | 0.10 | 0.20 | 0.14 |
| VA5 Outdoor morning light | LED_2 | [270, 480] | Flexible→Chaos-leaning | 2 W | 45 | 25 | 0.20 | 0.30 | 0.28 |
| VA6 Outdoor daytime light | LED_2 | — | **retired** | — | — | — | — | — | — |
| VA7 Outdoor evening light | LED_2 | [1080, 1320] | Flexible | 2 W | 60 | 35 | 0.20 | 0.30 | 0.28 |
| VA8 Outdoor overnight light | LED_2 | [1320, 1440] ∪ [0, 240] | Strict (when practiced) | 2 W | 30 | 15 | 0.10 | 0.20 | 0.14 |
| VA9 Portable-device charging | USB | [0, 1440] | n/a (structural) | 2 W | 210 | 105 | 0.20 | **0** (structural) | 0.85 |

VA9 additionally carries `thermal_P_var = 0.2` **[DECLARED DEFAULT]**.

---

### VA1 — Indoor morning preparation light (LED_1)

```yaml
power: 3
num_windows: 1
window_1: [240, 480]
func_time: 90
func_cycle: 55
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.35
```

Era 42
**Narrative.** Respondents describe a bounded block that shifts with wake time (*"depende de a qué hora
nos levantamos"* pattern) — not externally clock-anchored, but describable, the Flexible signature.

**Rigidity [RIG-XW]: Flexible.**

- **w_1 [WINDOW]:** `light_1_morning` modal cluster.
- **func_time [NARRATIVE — margin rule does not apply]:** grounded directly in Guillermo's stated
  duration (*"una hora por la mañana"* ≈ 60 min, rounded up modestly to allow for cross-household
  variation) rather than the margin formula — `240 × (1−0.3) = 168 min` would overstate this to nearly
  three hours, matching no respondent's description of a brief pre-dawn block.
- **func_cycle [RIG-XW→func_time]:** ≈0.6 × func_time (Flexible) = 55 min.
- **occasional_use [FREQ-XW]:** 0.42 (3/7) — **not universal**: Florencio skips morning light entirely
  (*"No hacemos alumbrar; lo único que utilizamos es el celular"*); treated as ~3×/week at profile level.

**Seasonal override — Planting & Harvesting, provisional.** Represents a plausible uplift in household
activity during the two labor-peak seasons — but per §6, presence itself is not guaranteed during these
same seasons for this profile (Rule 9), so this override should be read as "if present, somewhat more
active," not as a claim that overall energy use rises; the occupancy question (unresolved — §6, §8) may
dominate in the opposite direction.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.25
```

### VA2 — Indoor daytime light (LED_1) — **retired, no parameters**

No YAML block — this VA carries no parameters and is not passed to RAMP. **No seasonal override either:**
the same conservation-logic zero that holds at baseline holds in every season — there is no evidence of a
seasonal daytime-lighting practice to represent, planting/harvesting included.

**Narrative.** Retired as a substantive finding, not a token-valued placeholder. No respondent reports
daytime electric lighting; daylight suffices and daytime work (including weaving/spinning) is done in
natural light. The resulting 08:00–18:00 zero on the indoor bulb is physically real, not an artifact, so
the window-continuity rule does not require a placeholder value here — that rule exists to prevent
artificial drops where real use continues, and this drop is correct. Kept as a numbered slot only for
cross-profile alignment.

### VA3 — Indoor evening gathering and homework light (LED_1)

```yaml
power: 3
num_windows: 1
window_1: [1080, 1320]
func_time: 192
func_cycle: 134
time_fraction_random_variability: 0.10
random_var_w: 0.20
occasional_use: 0.8
```

**Narrative.** The core, replacing what an earlier reading treated as an "erratic evening" — uniformly
Strict, not chaotic. The window is externally anchored (sunset → ~22:00) and well-corroborated.

**Rigidity [RIG-XW]: Strict, uniformly.**

- **w_1 [WINDOW]:** `light_1_night` modal 1822, plus quotes from Rodolfo (40) and Guillermo (96).
- **func_time [WINDOW→margin]:** 240 × (1 − 0.20) = 192 min; `light_bulb_1_time` (evening share) ≈ 5–8
  h/day is broadly consistent.
- **func_cycle [RIG-XW→func_time]:** ≈0.70 × func_time (Strict/continuous, reduced from the canonical
  0.83 to keep RAMP's window-jitter engine constraint satisfied at this VA's `random_var_w=0.20` — see
  Protocol §5 note) = 134 min.
- **occasional_use [stated decision, not re-derived from the frequency crosswalk]: 1.00, uniformly.**
  Evening cooking/dinner is treated as a nightly, non-negotiable need independent of whether children are
  in school — the education-override reasoning (Rule 1-equivalent) is *one* sufficient basis where it
  applies, but the subsistence-dining component alone justifies the same value for every household, so the
  parameter does not need to be resolved per household from `children_in_school` at simulation time. This
  matters because `children_in_school` is itself unreliable for this profile — it conflicts with the
  qualitative record for Guillermo (see §8) — but that unreliability doesn't touch this parameter, since
  the value no longer depends on the field. Zenón's household gives the profile's most explicit statement
  of the dinner-only baseline this parameter assumes: *"Aquí no hacemos ninguna actividad; solo lo usamos
  para prepararnos la cena, comer y luego dormir"* — no homework or other task lighting at the SHS house
  at all (that happens at the second, ELFEC-connected house instead), yet the household still needs and
  uses the evening block for the subsistence-dining reason alone. The Rodolfo/Severino homework anchor
  (*"les dan tarea siempre… usa esta luz"*) is retained only as one of several corroborating anchors, not
  load-bearing alone, since that household has since relocated.

**Seasonal override — Planting & Harvesting: no change.** The requested seasonal value (1.00) is
identical to baseline, so no override block is added — nothing to override. Consistent with the
uniform, non-negotiable treatment already given to this VA above.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.35
```

### VA4 — Indoor overnight safety light (LED_1)

```yaml
power: 3
num_windows: 2
window_1: [1320, 1440]
window_2: [0, 240]
func_time: 288
func_cycle: 70
time_fraction_random_variability: 0.10
random_var_w: 0
occasional_use: 0.20
```

**Narrative.** A minority practice, mixed stated/no-stated cause. Rigidity is Strict *when practiced* (on
continuously through the night), but present only in a household subset — the subset/non-subset split is
carried by `occasional_use`, not by variability.

**Rigidity [RIG-XW]: Strict when practiced.**

- **w_1, w_2 [WINDOW]:** [1320, 1440] ∪ [0, 240] (22:00–04:00).
- **func_time [WINDOW→margin]:** 360 × (1 − 0.20) = 288 min.
- **func_cycle [RIG-XW→func_time, RAMP engine-constrained]: 70 min, not the Strict ratio.** Same issue as
  Profile 1's VA4: these two windows straddle midnight and are unequal in width (120 min evening tail vs.
  240 min early-morning block). RAMP requires `func_cycle` to fit inside *each* window independently, and
  the 120-minute evening window has a hard worst-case floor of 72 min under this VA's `random_var_w=0.20`
  jitter (`120 − 2×⌊0.20×120⌋`). The profile's earlier values (280, then 202 under the Strict-ratio fix)
  both exceeded that floor, so the evening window was never eligible for a switch-on — confirmed by the
  same isolated-appliance test used for Profile 1's VA4. `func_cycle=70` keeps a 2-minute buffer below the
  72-minute floor so the evening window is used every day. Ratio to func_time drops to ≈0.24, well below
  the Strict band; nightly usage is now several shorter bursts across both windows rather than one long
  block, though total nightly on-time (`func_time=288`) is unchanged.
- **occasional_use [household-level heterogeneity]:** 0.14 (1/7, implementation value) — underlying
  prevalence 2/6 interviewed ≈ 0.33 raw (Evangelino 23, Celestina 64), kept at 0.14 for cross-profile
  consistency with Profile 1's VA4 convention rather than re-derived from the small sample. Adequate under
  profile-averaged validation, but a thin evidence base — do not mistake the implementation value for the
  underlying-prevalence estimate.

**Seasonal override — Planting & Harvesting, provisional.** A large jump from the 0.14 minority-practice
baseline (nearly ×4) — flagged as the most dramatic of this profile's provisional deltas, on a VA whose
baseline was already thin-evidence household-level heterogeneity rather than a well-anchored figure.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0
```

### VA5 — Outdoor morning transit light (LED_2)

```yaml
power: 2
num_windows: 1
window_1: [270, 480]
func_time: 45
func_cycle: 25
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0
```

**Narrative.** Brief pre-dawn outdoor movement / animal tasks, weather- and chore-driven — describable in
kind but not in exact timing, a Flexible-leaning-Chaos signature.

**Rigidity [RIG-XW]: Flexible.**

- **w_1 [WINDOW]:** [270, 480] (04:30–08:00), starting just after indoor prep (Window 1 offset).
- **func_time [NARRATIVE — margin rule does not apply]:** a brief, event-driven outdoor chore block; the
  margin formula (`210 × (1−0.3) = 147 min`) would wrongly imply a long near-continuous outdoor presence,
  when the actual practice is a short task before daylight — same logic as Profile 1's parallel VA2.
- **func_cycle [RIG-XW→func_time]:** ≈0.55 × func_time = 25 min.
- **occasional_use [FREQ-XW]:** 0.28 (2/7), Low/Sporadic — brief outdoor-chore statements.

**Seasonal override — Planting & Harvesting, provisional.** Same status as VA1's and VA4's overrides —
a plausible presence-conditional uplift, not a re-derived finding.



```yaml
seasons: [growing, free_grazing]
occasional_use: 0.14
```

### VA6 — Outdoor daytime light (LED_2) — **retired, no parameters**

No YAML block — this VA carries no parameters and is not passed to RAMP. **No seasonal override
either**, for the same reason as VA2: the conservation-logic zero is not season-dependent.

**Narrative.** Retired on the same conservation-logic grounds as VA2. No respondent reports daytime
outdoor lighting; full daylight makes it implausible for this energy-conservation-oriented population.
Kept as a numbered slot only for cross-profile alignment.

### VA7 — Outdoor evening transit light (LED_2)

```yaml
power: 2
num_windows: 1
window_1: [1080, 1320]
func_time: 60
func_cycle: 35
time_fraction_random_variability: 0.20
random_var_w: 0.30
occasional_use: 0.28
```

**Narrative.** Dusk movement between structures, securing animals — describable, intermittent bursts
rather than a continuous draw.

**Rigidity [RIG-XW]: Flexible.**

- **w_1 [WINDOW]:** [1080, 1320] (18:00–22:00), inherited from Window 3.
- **func_time [NARRATIVE — margin rule does not apply]:** brief, event-driven outdoor transit; the margin
  formula (`240 × (1−0.3) = 168 min`) would wrongly imply nearly three hours of near-continuous outdoor
  presence each evening, when the actual practice is short intermittent bursts within the window — same
  logic as VA5.
- **func_cycle [RIG-XW→func_time]:** ≈0.6 × func_time = 35 min.
- **occasional_use [FREQ-XW]:** 0.28 (2/7), Low/Sporadic — brief nighttime movement reports.

**Seasonal override — Planting & Harvesting: none provided.** Not covered by the seasonal-override
request this set was built from. Worth a second look: the request's dropped "VA6: Outdoor evening
transit light, occasional_use: 0.25" entry (excluded per instruction, since that number corresponds to
this profile's retired VA6) shares this VA's exact name — possibly intended for VA7 rather than VA6 and
lost in the renumbering mismatch. Flagged here rather than applied, since that's a guess, not a
confirmed correction.

```yaml
seasons: [growing, free_grazing]
occasional_use: 0.14
```

### VA8 — Outdoor overnight safety light (LED_2)

```yaml
power: 2
num_windows: 2
window_1: [1320, 1440]
window_2: [0, 240]
func_time: 30
func_cycle: 15
time_fraction_random_variability: 0.10
random_var_w: 0.20
occasional_use: 0
```

**Narrative.** Minority, no stated cause. Strict when practiced, minority prevalence carried entirely by
`occasional_use`.

**Rigidity [RIG-XW]: Strict when practiced.**

- **w_1, w_2 [WINDOW]:** [1320, 1440] ∪ [0, 240], inherited from Window 4.
- **func_time [NARRATIVE — margin rule does not apply]:** a brief precautionary outdoor check, not
  continuous overnight illumination the way VA4's indoor counterpart is; the margin formula
  (`360 × (1−0.2) = 288 min`) would wrongly imply the outdoor light stays on nearly the whole night, which
  no respondent describes.
- **func_cycle [RIG-XW→func_time]:** 15 min.
- **occasional_use [household-level heterogeneity]:** 0.14 (1/7, rounded implementation value), resting on
  a single respondent (Evangelino, 23).

**Seasonal override — Planting & Harvesting: none provided.** Not covered by the seasonal-override
request this set was built from.

### VA9 — Phone / radio charging (USB)

```yaml
power: 2
num_windows: 1
window_1: [0, 1440]
func_time: 240
func_cycle: 120
time_fraction_random_variability: 0.20
random_var_w: 0
occasional_use: 0.85
thermal_p_var: 0.2   # DECLARED DEFAULT, pending measurement — see narrative
```

**Narrative.** Routine-daily when the household is present; the "burst" pattern sometimes visible in the
data is absence-driven, not appliance behavior — a multi-day-depletion-then-long-charge pattern is the
structural-absence effect (device dies while the owner is away, big charge on return), not a per-appliance
Chaos property. When the household is present, charging is routine and daily; `occasional_use` here
reflects present-household behavior (high), not a chaotic low value. The "burst" pattern belongs to the
occupancy axis (§2, Rule 9), not to this VA's parameters.

- **Rigidity:** the same decoupled-pair case as Profile 1's VA9 — full-day window ⇒ `random_var_w = 0` (no
  width left to randomize); quantity still varies ⇒ `time_fraction_random_variability = 0.2`.
- **w_1 [WINDOW]:** [0, 1440] — charging can occur any hour.
- **time_fraction_random_variability [RIG-XW]:** 0.2 — SoC / device count / supply variation.
  **Includes a weather-linked component, treated as Chaos per the protocol's retired-conditional-VA
  resolution, not a separate mechanism:** Florencio explicitly ties daytime charging to weather —
  *"hago cargar durante el día también; cuando llueve, pues, no hago cargar"* — a nameable but unmeasured
  trigger (no rainfall log exists for this study), so per protocol it folds into the same Chaos-level
  `t_f_r_v` rather than a weighted trigger formula. Zenón's household corroborates the supply-side half
  independently: *"antes de ayer estaba nublado y se apagó... se apagó como por 10 a 20 minutos"* — a
  direct, dated cloud-triggered outage, distinct from Florencio's demand-side framing but pointing at the
  same underlying weather-linked unreliability.
- **func_time [FREQ-XW→duration evidence]:** 240 min. Guillermo describes two separate daily sessions —
  *"como una hora por la mañana"* (~1 hr) + *"como dos, a veces tres horas"* (~2–3 hrs at night), a
  combined range of 180–240 min. Following the same midpoint-of-stated-range convention Profile 1's own
  VA9 uses, the midpoint is 240 min. This is Guillermo's own settled answer; an interviewer's paraphrase of
  one specific day's example (*"hice cargar desde las 11 de la mañana hasta las 3 de la tarde"*) is not
  used, since Guillermo pushed back on it (*"No hago cargar mucho"*) before giving the two-session routine.
- **func_cycle [RIG-XW→func_time]:** ≈0.5 × func_time = 120 min — fires in cycles across devices.
- **occasional_use [FREQ-XW]:** 0.85, Daily/Fixed — phone is the most-valued device and charges near-daily
  *when the household is present*: *"el celular usamos más"* (Rodolfo, 40); *"solo mi celular lo hago
  cargar"* (Guillermo, 96). **Evidence flagged as thin:** neither quote gives a specific daily count; both
  establish phone priority over other devices, not frequency. The Daily/Fixed bin and 0.85 figure are the
  best available reading given that, not a re-derived value.
- **thermal_p_var [DECLARED DEFAULT]:** 0.2 — CC-CV current taper near full charge; pending real
  measurement, flag downstream sensitivity.
- **Supply-side note, distinct from the demand-side trigger above.** Guillermo separately confirms his
  battery depletes on heavily cloudy days (*"¿Quizás es en los días que está muy nublado? — Sí"*,
  independently corroborated in his field memo). This describes reduced *available* charge under cloud
  cover, not a behavioral choice about *when* to use the appliance — it belongs to the system's
  supply/battery-state-of-charge dynamics downstream of RAMP's demand-side VA parameters, not to
  `occasional_use` or `t_f_r_v` here. Noted for completeness, not folded into this VA's parameters.

**Seasonal override — Planting & Harvesting, provisional.** Duration effect only, consistent with the
equivalent VA's treatment in Profiles 1–3; frequency (`occasional_use`) stays at baseline. Same caveat
as VA1/VA4/VA5's overrides applies here too: a duration uplift assumes presence, which §6/Rule 9 make
clear is not guaranteed in this profile even during labor-peak seasons.

```yaml
seasons: [growing, free_grazing]
func_time: 120
```

---

## 6. Seasonality

The SHS load ceiling is fixed by hardware; seasonality acts through **family mobility and occupancy**, not
through large per-appliance intensity swings. The agricultural calendar drives *presence* erratically:
households may be absent during planting/growing/harvest (migration to Chapare, monte logging, dual-home)
or return for key tasks — so, unlike Profile 1, increased in-home activity during these seasons is not
guaranteed. The cleanest representation is therefore the **occupancy mask** (present vs. absent), applied
at household level, rather than season-specific `occasional_use` edits per VA.

If a non-occupancy sensitivity variant is still wanted for the seasonal case, keep it minimal and
present-conditional (values apply only on days the household is home): VA3 (evening gathering) is already
at/near 1.0 when present, no change; VA9 (charging) `func_time` could rise modestly around labor peaks (more
devices charged), capped and flagged as a sensitivity knob, not a derived value. §5 now carries exactly
this kind of variant — a **provisional** Planting & Harvesting override set (VA1/4/5 `occasional_use` up,
VA9 `func_time` up; VA2/6 excluded as retired; VA3 unchanged since the requested value equalled baseline;
VA7/8 not covered by the request that produced this set) — added for full-year visualization, each
flagged individually in §5 as a sensitivity variant rather than a re-derived finding. The position stated
above is unchanged by adding it: occupancy, not per-VA tuning, is the seasonal effect that actually
matters here, and a duration/frequency uplift on a day the household isn't home is not meaningful — this
override set assumes presence, which this profile's own evidence says is the opposite of guaranteed.

---

## 7. Provenance (anchor quotes → parameters)

*Organized by household rather than by parameter, so a reviewer can audit everything this file claims
about a given household in one place. `[FIELD MEMO]` entries cite `memos.csv` by caseid.*

### Evangelino Coca (id 23) — interviewee: Gregoria Inturias (esposa), 20/11/2024

| Quote | Feeds |
|---|---|
| *"a veces lo llevo a donde estoy yendo"* | Rule 7 transport |
| *"por eso lo llevo, porque cuando voy allá no hay luz"* | Rule 7 rationale (no power at work site) |
| *"vivimos aquí siempre"* | single-residence baseline (weighed against the "otra casa" ambiguity below, resolved by memo) |
| *"tiene dos paneles… tres paneles aquí"* | initially raised second-house ambiguity |
| **[FIELD MEMO, caseid 9]** three separate solar panels accumulated at one home; seasonal migration "below" Dec–Carnival | resolves the ambiguity above: single residence, accumulated hardware, confirms Rule 7 not Rule 9 |
| *"no se apaga"* | VA4 overnight-light minority case |

### Rodolfo Agreda (id 40) — interviewee: Severino Agreda (hermano), 20/11/2024

| Quote | Feeds |
|---|---|
| *"se quedará un mes… en enero ya va a estar aquí"* | short-absence account, superseded by the field memo (permanent relocation) |
| *"les dan tarea siempre"* (re: prekínder niece/nephew) | VA3 corroborating anchor — household since relocated, retained only as one of several corroborating quotes |
| *"solo funcionó un mes nomás"* (radio) | Rule 13 hardware resignation |
| *"el celular usamos más"* | VA9 phone-priority anchor |
| *"Mi hermano enciende a partir de las 6:00 de la tarde hasta las 10:00 de la noche… en la madrugada, desde las 3:00 hasta las 6:00"* | Window 3 evening + Window 1 pre-dawn corroboration |
| **[FIELD MEMO, caseid 47]** migrates for mining work, rarely returns; domestic needs met by one panel | confirms relocation (supersedes "back in January"); single-panel hardware |

### Florencio Rivera (id 76) — interviewees: esposa, then esposo, 19/11/2024

| Quote | Feeds |
|---|---|
| *"desde las 7 de la noche hasta las 9 o 10 de la noche"* | Window 3 (narrower variant, code 1922) |
| *"cuando no estamos utilizando la apagamos… hasta a veces riño a mis hijos"* | conservation-oriented behavior when present |
| *"una de mis casas está abajo. Tengo dos casas"* | Rule 9 diagnostic — explicit second residence |
| *"Ah, no; lo voy a guardar"* (asked who stays behind) | confirms genuinely-empty-during-absence |
| *"vamos a llevarlo abajo hasta el mes de junio… le damos el mismo uso"* | Dec–June migration window; read as arrival at an already-functioning second system, not equipment transport |
| *"durante el día tejemos; no utilizamos la luz"* | VA2/VA6 daytime-retirement evidence |
| *"No hacemos alumbrar; lo único que utilizamos es el celular"* | VA1 non-universal — morning light not used |
| *"hago cargar durante el día también; cuando llueve, pues, no hago cargar"* | VA9 weather trigger, Chaos-classified |
| *"si no hay nadie no dejan la luz prendida"* | keeps overnight-safety-light minority classification |
| **[FIELD MEMO, caseid 48]** two systems in two separate houses, seasonal Dec–June migration | resolves second-house power source; confirms window independently of the quote above |

**Albino Acosta (58) and Pascual Zurita (83)** are classified in `classifications_oficial.csv` as Profile
4 households but are treated as Profile 1 members per a documented override (§2, Rule 9 population note).
Their evidence is cited in Profile 1's file, not here.

### Guillermo Romero (id 96) — interviewee: Guillermo Romero, 25/02/2026; also A1/A3 *Autoridad*, 21/11/2023

| Quote | Feeds |
|---|---|
| *"Generalmente yo estoy aquí; mi esposa a veces"* | Rule 9 diagnostic — dual residence |
| *"Pagamos 18, 19, a veces 20 Bs"* | ELFEC grid payment at second residence |
| *"No, siempre está aquí"* (re: SHS panel) | Rule 7 — firmly kept at home |
| *"como una hora por la mañana"*; *"hasta las 10 de la noche"*; wake *"a las 6 de la mañana"* | VA1/VA3 windows and func_time |
| *"como una hora por la mañana"* + *"como dos, a veces tres horas"* (charging) | VA9 func_time = 210 min, two-session evidence |
| *"el problema es la conexión de la radio"* | Rule 13 hardware resignation |
| *"No lo voy revisando tanto; tengo miedo de que se arruine"* | minimal, cautious panel maintenance |
| *"¿Quizás es en los días que está muy nublado? — Sí"* | VA9 supply-side note, not a demand parameter |
| *"solo mi celular lo hago cargar"* | VA9 phone-priority anchor |
| **[FIELD MEMO, caseid 57]** dual residence + ELFEC; corroborates light-use durations, broken radio cable, cautious maintenance | directly corroborates dual-residence and several appliance-level details above |

### Zenón García (id 54) — interviewee: la hija, 26/02/2026; second respondent "Luis" later in session

| Quote | Feeds |
|---|---|
| *"Sus tareas y algunos trabajos... los realizamos en nuestra otra casa generalmente"* | Rule 9 diagnostic — dual residence, task-lighting/charging at the second house |
| *"si es en la otra casa donde hay luz de ELFEC, ahí nos vamos para hacer eso"* | confirms second house is grid-connected, not a second SHS |
| *"Aquí no hacemos ninguna actividad; solo lo usamos para prepararnos la cena, comer y luego dormir"* | VA3 dinner-only baseline at the SHS house |
| *"Hacemos cargar la radio nomás... dos celulares, pero no carga"* | appliance inventory — SHS house cannot support modern phone charging |
| *"antes de ayer estaba nublado y se apagó... como por 10 a 20 minutos"* | VA9 weather-linked supply variability |
| *"¿El panel solar lo trasladan a algún lado? — No, solo está aquí"* — "Luis," attribution unclear | flagged tension, not treated as decisive against the daughter's memo-corroborated account |
| **[FIELD MEMO, caseid 6]** multi-source strategy: SHS for basic lighting/radio, ELFEC house for weaving and smartphone charging | directly corroborates the daughter's dual-residence account |

### Celestina Inturias (id 64) — interviewee: Celestina Inturias, 19/11/2024

| Quote | Feeds |
|---|---|
| *"Nosotros estamos aquí como dos semanas... Por eso llevamos el sistema y, cuando volvemos aquí, también lo traemos"* | Rule 9 diagnostic — alternating residence, ~two-week cycle |
| *"con esa luz duermo tranquila y tampoco tengo miedo"* | VA4/Window 4 overnight light, with a stated cause below |
| *"me picó un bicho, creo que era alacrán... Ahora que hay luz, ya no hay bichos que nos piquen"* | stated cause for overnight light — insect safety, not the profile's usual no-stated-cause pattern |
| *"Ustedes me dieron como algo negro; está en mi otra casa"* | corroborates a genuine second residence with its own equipment |
| *"Tengo diez hijos... como aquí no hay buenas condiciones para vivir bien... vienen [de Santa Cruz]"* | household composition — out-migrated children, remittances |
| **[FIELD MEMO, caseid 21]** alternates residency every two weeks due to water scarcity; maintains two separate solar systems, one per residence | directly corroborates the alternating pattern and clarifies the two-systems structure her own phrasing leaves ambiguous |

---

## 8. Open items carried forward

- **Provisional Planting & Harvesting seasonal override set (§5) needs a confirmation pass.** Built from
  a request whose VA numbering didn't account for this profile's two retired slots (VA2, VA6); confirmed
  mapping applied VA1/VA4/VA5/VA9 overrides directly and left VA2/VA6 (retired) and VA7/VA8 (not covered
  by the request) without any override. One specific loose end: the request's dropped VA6 entry ("Outdoor
  evening transit light," occasional_use 0.25) shares its exact name with this file's actual VA7, which
  currently has no override — worth confirming whether that value was meant for VA7 before treating this
  set as final. VA4's override (0.14→0.55) is also a notably large jump on a thin-evidence baseline,
  worth a second look on its own terms.
- **Representativeness of the interviewed subset on dual-residence/relocation prevalence.** 3 of 6
  interviewed households (Guillermo, Rodolfo, Florencio) are confirmed genuinely-empty-during-absence, all
  with a dated field memo; 2 more (Zenón, Celestina) show dual-residence patterns whose occupancy
  consequence is real but less precisely characterized; 0 of 6 show a resident-baseline offset. Whether
  this rate holds across the full N_survey = 12 cannot be checked against any survey field
  (`migration_label` doesn't discriminate), and the memos only cover the six already-interviewed
  households. This is the single biggest unresolved uncertainty in the profile and gates confidence in
  every downstream occupancy number.
- **`children_in_school` data-quality concern**, worth resolving on its own terms: it conflicts with the
  qualitative record for Guillermo (coded `No` despite his own memo and interview describing a
  school-aged child doing homework by the SHS light). This no longer affects VA3 (its `occasional_use` is
  set to 1.0 uniformly, independent of the field), but the field's reliability is worth checking across the
  other profiles that use it (Profile 1's Rule 1, Profile 2's "no young children" criterion).
- **`occupation` is unreliable in different ways for different households, not with one blanket
  correction.** Guillermo is coded *Mining* but is a salaried authority who describes agriculture — a
  genuine mismatch. Rodolfo is also coded *Mining*; his 2024 transcript describes monte logging at the
  time, but he has since taken an actual mining job, so the code is accurate for the current situation
  though not for the reason the transcript alone would suggest. Treat `occupation` per household against
  current field knowledge, not as a profile-wide correction.
- **Occupancy feature is not yet implemented.** This file's household-level structural-absence findings —
  including Florencio's concrete Dec–June window, the most precisely dated of the three — are the direct
  input to that feature's design: a recipient-keyed masking approach, with resident-baseline claims
  requiring explicit co-residence confirmation before they're allowed to damp the mask.
- **Two unresolved tensions from the ids 54/64 override**, worth a follow-up field visit rather than
  further desk analysis: (a) Zenón García's household — the "Luis" respondent's contradiction, unresolved;
  (b) Celestina Inturias's household — `classifications_oficial.csv`'s `portability_shs = Yes` conflicts
  with the alternating-residence, two-system pattern her transcript and memo both independently describe.
- **`thermal_P_var = 0.2` is a declared default, not a measured value** (VA9, USB charging), per Protocol
  §9. Low urgency unless a sensitivity run shows the load curve is sensitive to this figure.
- **Spot-check `func_time` derivations in Profiles 1–3** for the two error types found while building this
  file: formula mismatches between a [WINDOW→margin] tag and its stated value, and citations pointing at an
  interviewer's paraphrase rather than the respondent's own settled answer.