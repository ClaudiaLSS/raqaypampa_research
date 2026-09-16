## Section S3: Parameter derivation protocol

This section is the source describing how each RAMP parameter in the Socio-technical model parametrization is derived. Profile truth files reference this section rather than reproducing it, so revisions propagate consistently.

Every parameter falls into one of six derivation sources. Five of the six derive a **per-appliance** parameter; two of those five are **crosswalks** (classification steps that sort respondent language into bins). The sixth derives the one **household-level** parameter, which is not a property of any appliance:

- **[SPEC]** — technical hardware specification (not behavioral; no qualitative translation)
- **[WINDOW]** — derived from the Anthropological Window (interview × survey triangulation)
- **[FREQ-XW]** — frequency crosswalk (Table 1, Section S3.3): respondent frequency language → `occasional_use`
- **[RIG-XW]** — rigidity crosswalk (Table 2, Section S3.3): the qualitative account → a rigidity bin (Strict / Flexible / Chaos), which *is* the variability classification
- **[DECLARED DEFAULT]** — a stated, literature informed, reasoned value used when neither qualitative nor quantitative data directly speaks to a parameter; flagged as pending real data, never presented as derived.
- **[OCC]** — occupancy derivation: stated absence durations → `prob_home`, the probability a household of the profile is present on a given day. Household-level, not per-appliance: one value per profile (optionally per season), gating *every* VA of that household at once.

A note on the two crosswalks, since they are the same kind of object: both **[FREQ-XW]** and **[RIG-XW]** are classification steps that read respondent language and assign a bin. The rigidity crosswalk (Table 2, Section S3.3) directly yields `time_fraction_random_variability` and `random_var_w` (they are the bin's assigned values). One parameter, `func_cycle`, is a **second-order derivation**: it takes the rigidity bin and applies a further rule (fraction of `func_time`), so it is marked [RIG-XW → func_time] to show it is one step removed rather than a direct crosswalk output.

One phenomenon is handled *outside* the per-appliance parameters: **household-level structural absence** (migration/dual-residence), which since 2026-08-18 is an applied model parameter rather than a documented-but-deferred one — it is derived via **[OCC]** into `prob_home` and simulated as RAMP's household-level occupancy mask. 

---

**Population and generalization (who the qualitative parameters actually describe)**

The `ebp_profile` classification is itself survey-derived (family_type, occupation, children_in_school, migration, portability_shs). This means **every classified household has survey data**, but only a subset was also interviewed, in this specific case. Each profile therefore has two population sizes, not one:

- **N_survey** — everyone classified into the profile (defines who counts as that EBP)
- **N_interview** — the subset also interviewed (the only source of qualitative material)

| Truth-file output | Population it draws from | Why |
|---|---|---|
| Windows (`window1`, `window2`) | **N_interview + N_survey** (triangulated) | Anthropological Windows are derived by triangulating interview accounts of practice timing with survey time-use data and hard physical anchors (sunrise/sunset) — survey and physical data alone can't supply the cultural framing, and interview accounts alone can't supply population-scale timing or fixed astronomical anchors |
| Rigidity classification (incl. Extreme/Structural), narrative, frequency-language `occasional_use` | **N_interview only** | Requires actual quotes — a household with no transcript can't supply timing statements, hedging language, or evidence of a dual-household strategy |
| `prob_home` — [OCC], household-level occupancy (§10) | **N_interview only** as the numerator *and* the denominator | Requires a stated absence duration, which only a transcript supplies. The denominator is the full interviewed base, so the value describes the profile rather than its mobile subset — and `migration_label` cannot substitute for the missing survey households |
| Ownership/appliance-count parameters | **N_survey (full)**, where the survey captured them | Structural, not behavioral |

### S3.1 Evidence tiers within Stream A (QUAL): transcript, field memo

Not all qualitative material carries the same auditability. Three tiers, ranked by how independently checkable the claim is:

1. **Interview transcript** (`all_transcripts.txt`) — verbatim, dated, attributable to a named respondent. The primary source underlying N_interview and the sole source for Table A/B crosswalk anchors, since those require the respondent's *own phrasing* (hedging language, frequency markers, timing statements), not a paraphrase.
2. **[FIELD MEMO: caseid, date]** — a written, dated field note (`memos.csv`, authored by the field researcher). Close to interview transcript in auditability — it is a specific, attributable, dated document, not recall — but it is a *summary*, not a verbatim quote, so it does not carry a respondent's own frequency/timing language. Field memos are the right evidence for **structural and demographic facts**: household composition, migration/dual-residence pattern, hardware inventory and ownership history, occupation. They should **corroborate or independently establish structural claims**, not substitute for a transcript anchor in Table 1 and 2.
3. **[FIELD OBS: conversational]** — an undocumented exchange recalled by a researcher, with no dated written record. The weakest tier. Never used as the sole basis for a parameter; flag explicitly wherever it appears, and prefer corroboration from tier 1 or 2 before treating it as evidence at all.

**Practical rule:** a `— source:` trailer citing a field memo takes the form `[FIELD MEMO: caseid NN, DD/MM/YYYY]`; a trailer citing undocumented recall takes the form `[FIELD OBS: conversational]`. Do not fold the two into one tag — the split exists precisely so a reader can see which claims rest on a citable document and which rest on memory.

In practical terms, each Energy Behavior profile owns a truth file, which contains a detailed picture in terms of demographics, energy culture and specific RAMP parameters obtained from this derivation protocol.

Each truth file requieres a header block formt shown bellow:

```
Population: N_survey = [X] (classified via family_type/occupation/migration/portability_shs)
            N_interview = [Y] (subset with transcript; source of all qualitative parameters,
            including Windows, Rigidity/variability bin — including Extreme/Structural —
            and occasional_use)
Generalization: all qualitative parameters below (Windows, Rigidity, occasional_use,
Extreme/Structural bin assignment, and the household-level prob_home) are inferred from
N_interview and applied uniformly to all N_survey households in this profile at simulation
time. There is no survey-only shortcut for any of these — dual-household/structural-absence
status requires interview evidence, the same as ordinary timing and frequency parameters.
```

Note what "applied uniformly" means for `prob_home` specifically: it is one probability per profile, so every one of the N_survey households carries the same *chance* of being absent, and each then draws independently day by day. A category of 30 households at `prob_home = 0.7` therefore has roughly nine absent households on a given day — not a 30% chance of all thirty emptying at once. The parameter generalizes a rate, not a schedule, which is the correct treatment given that the interviews establish how much absence occurs in the profile but not which of the un-interviewed households it belongs to.

Where a household's transcript is corroborated by a written field memo, cite both: `— source: [respondent, date; FIELD MEMO caseid NN]`.

### S3.2 Data-completeness tiers (what to do when a source is missing or vague, per practice)

Not every interview mentions explicit time boundaries for every practice, and not every respondent gives comparable detail. This determines *which row* of the interview×survey crossing table is usable for a given practice:

| Data situation | What to do | Confidence / `random_var_w` |
|---|---|---|
| Both interview and survey give explicit clock times | Apply the 3-tier crossing rule as defined in §3 | As specified there |
| Only one source gives explicit times | Use that source's bounds directly | Moderate–high — one notch less confident than an agreeing pair, since there's nothing to corroborate against |
| Neither source gives clock times, only time-of-day language ("por la mañana") | Anchor to the Window's own pre-defined outer bounds (already grounded in physical anchors) rather than inventing precision from vague language | High (widest bin) |
| No timing information at all for this respondent, this practice | Do not derive an individual window from nothing. Pool across other N_interview respondents in the same profile who did report timing for that practice; use the pooled range | High, and explicitly flagged **pooled evidence** — a different epistemic status (profile-level generalization) than the other three (household-level triangulation) |

The pooled-evidence flag matters because it's a second, independent axis of "how much do we actually know" — distinct from the N_survey/N_interview generalization above. A VA can rest on solid individual evidence from a well-covered profile, or on pooled evidence from a thinly-covered one; both should be visible in the file.

**A related, more fundamental limitation: single-period survey questions structurally capture typical behavior, not occasional behavior.** A categorical period-code question (e.g., "when do you use light_1 at night?") can only record one representative window per respondent — it has no way to express "usually X, but sometimes Y under specific circumstances." This is not a data-quality problem or a respondent error; it is a structural limit of the question format itself. When a respondent's interview account describes something that appears to exceed or diverge from their own survey answer (e.g., an occasional, trigger-driven practice layered on top of an ordinary routine), the two sources are often not actually in conflict — they are answering different questions the survey was never built to distinguish. This is precisely the kind of layer interview material is positioned to add, and it should be read as *enrichment revealing an additional layer*, not as a Say-Do contradiction. The tier-4 rule still applies to genuine disagreements about a practice's *typical* pattern; it should not be invoked reflexively whenever an interview describes something a survey's single-code answer could never have captured in the first place.



### S3.3 Crosswalk Tables
To understand the parameter derivation protocol, the crosswalks designed to translate qualitative evidence into quantitative simulation parameters are provided below. These are used to derive two main characteristics of appliance use: the probability of being used (occasiona_use) and the rigidity of each activity (main source for the randomization parameters).

This crosswalk was built inductively from the interview corpus and refined against it, in the following steps:

1. **Parameter-driven extraction.** Starting from what RAMP actually requires (`occasional_use`, `time_fraction_random_variability`, `random_var_w`), the interview transcripts for each of the four EBP profiles were searched for the language respondents use to express *frequency* (how often a practice occurs) and *temporal variability* (how stable its timing is). This yielded a corpus of naturally-occurring frequency and timing expressions in the respondents' own words (Spanish/Quechua-Spanish), each tied to a specific respondent, profile, and interview date.
   
2. **Inductive binning.** Recurring expressions were grouped into a small number of bins. Language was mostly qualitative ("a veces," "de vez en cuando," "siempre"), so it was grouped into ordinal bins and assigned a representative probability/variability value.

3. **Cross-profile validation.** Each bin was checked against anchor quotes drawn from *multiple* profiles, not a single one, to confirm that a given expression carries approximately the same meaning regardless of who says it (e.g., that "a veces" implies a similar frequency whether spoken by an elderly single resident or a school-age household).

4. **Iterative refinement where bins broke.** The scheme was revised wherever transcript evidence contradicted an initial definition. Two substantive revisions are recorded rather than hidden, because they demonstrate the crosswalk was tested against the data:
   - The **"Chaos" bin was redefined** from an outcome-based criterion (timing varies day to day) to an *epistemic* one (the respondent's own account signals they cannot specify a stable pattern — hedging language, self-contradiction, explicitly unanchored windows).
   - **Household-level structural absence** (dual residence, extended absence) was distinguished from practice-level variability and made a separate axis, triggered by **explicit dual-household or extended-absence language in the interview narrative** — not by the survey's `migration_label`, which is too common across the sample to discriminate (most households show some migration), and not by EBP profile membership either — because multi-month absence was found in a Profile 3 household, not only in Profile 4.
  
5. **Priority-override layer.** Practices anchored to a profile's non-negotiable social rules (education, subsistence cooking) are assigned Daily/Fixed frequency and Strict variability by default, overriding isolated hedging language, since such hedging typically concerns incidental detail rather than whether the practice occurs (see override note in Table 1).


**Methodological note**

Bins are a classification instrument, not a statistical estimator. Respondents' frequency and timing accounts are ordinal semantic expressions in their own words ("a veces," "siempre"), not measurements of a continuous variable. Statistical binning — clustering, distribution-fitting, quantile cutoffs — presupposes such a variable and a sampling distribution over it; applied here it would impose a metric structure the data does not carry and manufacture false precision. The bins were therefore derived inductively: recurring expressions were grouped and validated against anchor quotes from multiple profiles. Their validity rests on transparency and traceability — every value maps to at least one dated interview anchor — and on the recorded revision history, which documents where transcript evidence contradicted a bin and the scheme was revised. Those revisions are reported, not hidden, because they are the evidence that the classification was tested against the data rather than imposed on it.

The extraction rule enforces fidelity to actually-occurring categories. Where a parameter is grounded in the survey's categorical period codes, the value is the single most common reported code (the mode), bounds and all — not a summary statistic across window widths. A median or mean of widths can silently yield a window no respondent reported, whereas the modal code is by construction a real answer someone gave. This constraint surfaced and corrected three constructed-artifact windows during Profile 1's finalization. The frequency crosswalk follows the same logic, reading the dominant recurring expression rather than an averaged frequency. Where no mode exists (bimodal codes), the absence is carried forward as elevated random_var_w rather than resolved by interpolating a value no respondent chose.

The bin values are declared, not measured. The representative numbers assigned to each bin are declared values within an ordinal scheme, calibrated to anchor quotes and always propagated with an explicit variability parameter — not point estimates asserting precision. Throughout, the qualitative step refines within the systematically-collected survey envelope rather than overriding it, with the survey taking precedence in genuine conflict.

---

**Table 1 — Frequency Language → `occasional_use`**

**Priority override (apply before any other rule below):** if a practice is anchored to an established non-negotiable social rule for the profile (e.g., education, subsistence cooking, or any other rule the profile's truth file defines as non-negotiable), default to **Daily/Fixed** frequency (`occasional_use` ≈ 1) and, on the variability table, **Strict** (0.1) — regardless of hedging language ("a veces," "depende") appearing in isolated quotes about that practice. Such hedging is almost always about an incidental detail (which exact task, whether the light stays on the full duration), not about whether the practice occurs that day. Override this default only with specific, explicit evidence of exception (a stated skip pattern — e.g., "solo cuando no hay tarea" — not just soft phrasing).

Example: Zenón García's *"la necesitamos cada día por las noches; los chicos van haciendo sus tareas"* (P1, 26/02/2026) already reflects this correctly — homework light is `occasional_use: 1`, Strict variability — because it is anchored to the Educational rule, not because every quote about it used "siempre."

**Fallback bins:**

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


## Derivation map

| RAMP parameter | Source | One-line basis |
|---|---|---|
| `power` (w) | [SPEC] | SHS appliance nameplate rating |
| `number` / counts | [SPEC] | Survey appliance inventory |
| `w_1` / `w_2` (window bounds) | [WINDOW] | Outer bounds of the Anthropological Window |
| `func_time` (total daily on-time) | [WINDOW→margin] | Window width × (1 − random_var_w); window from survey duration/period fields where available |
| `func_cycle` (min. continuous run) | [RIG-XW → func_time] | Rigidity bin → fraction of `func_time` (second-order) |
| `time_fraction_random_variability` | [RIG-XW] | Rigidity bin's assigned total-on-time variation |
| `random_var_w` | [RIG-XW] | Rigidity bin's assigned window-width variation |
| `occasional_use` | [FREQ-XW] | Frequency crosswalk: language → probability |
| `P_var` (charging/supply appliances only) | [DECLARED DEFAULT] | Stated, reasoned value pending real measurement; physical mechanism stated explicitly since RAMP's parameter name references thermal variability specifically |
| `prob_home` (**household-level**, one per profile ± per season) | [OCC] | Stated absence durations ÷ interviewed household-months → P(household present on a given day); gates every VA of the household together (§10) |

---
Here the provenance of each parameter is explained in detail:

## 1. `power` — [SPEC]
Device wattage is a technical property of the hardware, not a behavioral variable. Taken directly from the appliance nameplate / SHS deployment inventory (LED and radio ratings). Carries none of the qualitative-translation burden and is the most directly verifiable parameter in the model.

## 2. `number` / appliance counts — [SPEC]
Ownership and quantity per household from the survey appliance inventory. Countable, survey-sourced.

## 3. `w_1` / `w_2` (time-window bounds) — [WINDOW]
The window bounds are the outer edges of the **Anthropological Window** for the practice. The Anthropological Window is itself a triangulated construct: the practice's timing as described in interviews, **crossed with** the survey time-use data, plus hard physical anchors (sunrise/sunset). The window is therefore not a single self-report but a convergence of two independent sources — which is what makes it auditable rather than interpretive.

*Crossing convention when interview and survey diverge on timing.* Survey and interview timing data sit at different resolutions — the survey gives a coarse, systematically-collected envelope; the interview gives finer situated detail — so they typically *refine* rather than *contradict* each other. The rule is a refinement hierarchy with a defined fallback, and it simultaneously sets `random_var_w`:

1. **Survey sets the coarse envelope; interview refines within it.** The survey time-use response establishes the outer window; interview detail tightens the bounds where it gives a more specific range.
2. **Interview range nests inside the survey envelope** → use the interview bounds; set `random_var_w` **low** (sources agree, one sharpens the other — high evidential confidence).
3. **Ranges overlap but do not nest** → take the **union** as the window; set `random_var_w` **higher** (sources bound the practice only loosely — moderate confidence).
4. **Genuine conflict (non-overlapping ranges)** → default to the **survey** (the instrument applied identically across all households; an outlying interview statement may be idiosyncratic or a recall/transcription artifact); flag in the provenance note; set `random_var_w` **high**. Should be rare — frequent conflict for a given practice is itself a finding to note.

The survey-wins tiebreak in tier 4 is deliberate: it keeps the qualitative contribution as *enrichment* (adding resolution and meaning, the common case) rather than *override* (vetoing structured data, the contested case), which avoids the "cherry-picked qualitative data". This convention also makes `random_var_w` a rule-governed readout of source agreement rather than a separate judgment.

**Use the modal code, not a median-of-widths statistic, when grounding a window in survey period-code data.** Survey period-of-use questions are categorical (e.g., "18:00–22:00," "19:00–21:00," not raw clock times). It is tempting to compute a summary statistic across respondents' reported *widths* (e.g., median duration) and center that on an assumed typical start time — but this can silently produce a window that **no respondent actually reported**, since a median width paired with an assumed start time is a constructed artifact, not a real answer. The correct method: take the single most common reported code (the mode) directly, bounds and all. This surfaced as a real error in Profile 1 — VA3's window was originally set from a width-only median (17:00–20:00, nobody's actual answer) and was corrected to the true modal code (18:00–22:00, the single most common reported window, independently corroborated by three interview quotes) once checked directly. The same check caught and corrected two further instances (VA5, VA7) before they were finalized. Treat this as a required verification step for every survey-grounded window, not an occasional spot-check.

## 4. `func_time` (total daily functioning time) — [WINDOW→margin rule]

The survey codebook contains direct duration data (`light_bulb_N_time`, `phone_N_time`, `radio_time` — average daily hours) and direct period-of-use codes (`light_N_morning`/`light_N_night` — categorical windows). Checking these against each other empirically (Profile 1, N=26): reported total daily on-time closely matches the *sum* of reported morning+night window widths (ratio ≈ 1.0) — i.e., respondents report their stated windows as continuously occupied, not sparsely used within a wider span. This is a real empirical finding and should not be diluted by an invented "intensity" fraction.

However, RAMP requires `func_time` to sit strictly below the window width so stochastic placement has room to operate without truncating at the boundary. This is an **engine constraint**, that aims to represent uncertainty of human behavior and must be handled as a separate, explicitly-labeled step rather than folded into the empirical value:

> `func_time = window_width × (1 − random_var_w)`

This draws the margin from `random_var_w` (already set by the rigidity crosswalk, Table 2) rather than an arbitrary constant. It also functions as an implicit bias correction: `random_var_w` is lowest for well-anchored (Strict) practices, which are also the reports least likely to suffer recall/rounding bias, so those reports are trusted closest to their full value; poorly-anchored (Chaos) reports — more likely to be rough estimates — are discounted more. One formula, two justifications (engine constraint + bias correction), both stated rather than left implicit.

Where the direct survey duration/period fields aren't available for a given appliance (e.g., no equivalent field exists), fall back to duration statements in the interview ("dos horas," "hasta las 10") as the window-width source, then apply the same margin formula.

## 5. `func_cycle` (minimum continuous run-time) — [RIG-XW → func_time]
This is a **second-order derivation**: the rigidity crosswalk (Table 2) classifies the practice, then a further rule expresses `func_cycle` as a fraction of `func_time`:

> The more rigid (continuous, non-negotiable) the practice, the closer `func_cycle` is to `func_time` (the activity runs in one unbroken block). The more trigger-driven (intermittent, unpredictable) the practice, the smaller `func_cycle` is relative to `func_time` (the activity fires in short bursts within its window).

Worked reasoning: 
- **Rigid / continuous** (evening homework+dinner light, safety light): people do not get up mid-activity to toggle the light, and cooking/homework does not take less than its multi-hour block — so `func_cycle` ≈ `func_time`. *Anchor: VA3, func_cycle 150 / func_time 180 ≈ 0.83.*
- **Flexible / bounded-but-shifting** (a practice the respondent can describe, but without a single fixed anchor): sits between the two extremes — the practice isn't as fragmented as a Chaos trigger, but isn't as continuous as a Strict routine either. `func_cycle` ≈ 0.6 of `func_time`, the stated midpoint between Strict's ~0.83 and Chaos's ~0.5. *Anchor: VA1/VA5 (Profile 1), func_cycle ≈50 / func_time 84 ≈ 0.6.*
- **Trigger-driven / intermittent** (daytime "search for something in the room" light): use is provoked by unpredictable specific needs, so it fires in short fragments — `func_cycle` ≪ `func_time`. *Anchor: VA2, func_cycle 30 / func_time 60 = 0.5.*

Rigidity here is the *same* assessment used for the two variability parameters below, so `func_cycle` is not an independent judgment but a third output of one rigidity construct.

## 6. `time_fraction_random_variability` — [RIG-XW]
Per RAMP documentation, this randomizes the **total functioning time** (`func_time` ± this fraction) — i.e., how much the *quantity of daily use* varies. It is a direct output of the rigidity crosswalk (Table 2): Strict ≈ 0.1, Flexible ≈ 0.2, Chaos ≈ 0.3.

## 7. `random_var_w` — [RIG-XW]
Per RAMP documentation, this randomizes the **size of the functioning window** (the w_1/w_2 bounds) — i.e., how much the *permissible time-envelope* stretches or contracts. A direct output of the rigidity crosswalk (Table 2), distinct from §6: one varies *how long the appliance runs*, the other varies *how wide the window is*.

Justification (from rigidity, with an evidential interpretation): a Strict practice is externally anchored (school, sunset), so its window barely moves → low `random_var_w`; a Chaos practice has no firm anchor, so its window floats → high `random_var_w`. Conceptually, `random_var_w` encodes **how confidently the source data bounds the window**, and this is the actual value-setting rule (not a second independent one): it is set directly by the interview×survey crossing tiers — nested sources → **~0.1–0.2**; overlapping → **~0.2–0.3**; conflicting → **~0.3–0.4**. Rigidity and source-agreement align in practice (rigid practices tend to have well-agreed windows), so Table 2's Strict/Flexible/Chaos values (0.2/0.3/0.35) are typical *outcomes* of this rule, not a separate rule — use them as a sanity check: if a VA's rigidity bin and its evidence-confidence tier disagree noticeably, that's worth a second look, since it may mean the rigidity call rode on narrative tone rather than on how well-anchored the timing evidence actually is.

*Why two parameters, not one:* rigidity is the common cause, but the two act on different objects, so a practice can be rigid in one respect and loose in the other. The decisive case is **VA9 (Portable devices charging):** its window is [0, 1440] — the entire day, because charging can occur at any daylight hour — so `random_var_w = 0`, not because timing is certain but because a window already spanning 24h has no width left to randomize (window-flex is undefined for a full-day window). Yet `time_fraction_random_variability = 0.2`, because *how much* charging happens still varies day to day (battery state of charge, number of devices, visitors, supply fluctuation under cloud cover). The two parameters are here **decoupled by construction**: window-flex is driven to zero by a structural fact (the full-day window) that has no bearing on total-time variability. This pair cannot be explained as two labels on one rigidity value — one parameter reports an unbounded/maximal window, the other reports that the quantity of use still varies — which proves the two are not redundant. Supporting transcript evidence for the fixed-window/variable-quantity reading: *"a veces lo cargamos en el día o en la noche"* (timing unconstrained); *"Para dos celulares no abastece; solo abastece para uno"* (Edelfrida Jiménez Salazar, P1 — quantity contested by demand); *"cuando hay bastante sol, hay bastante energía"* (Miguel Meneses, P1 — amount tied to fluctuating supply).

## 8. `occasional_use` — [FREQ-XW]
Probability that the practice occurs on a given day, from respondent frequency language via the frequency crosswalk (Table 1), subject to the priority override for non-negotiable practices.

**"On a given day" means a *home* day wherever the occupancy mask is active.** The two probabilities are independent draws and compose multiplicatively, `P(VA runs on a day) = prob_home × occasional_use`, so once a profile carries a `prob_home` the crosswalk's denominator is home-days rather than calendar-days. This is the correct reading of the source evidence rather than a reinterpretation of it: a respondent describing how often they light the evening meal is describing the evenings they are there, and Table A's markers ("siempre," "a veces") are heard against the household's own presence, not against the calendar. Declare the reading explicitly per profile (`occasional_use_basis`), and never encode absence a second time by lowering `occasional_use`.

## 9. `P_var` — [DECLARED DEFAULT] (used for supply/charging-type appliances)
Percentage random variability applied to an appliance's power draw, per RAMP's own parameter (confirmed: always a scalar fraction, e.g. 0.2 = 20%, applied as variability around a baseline power — in RAMP's own documented example, a time-varying power series thermal_p_var; the mechanism also functions when applied to a plain constant `power`, without requiring a full external time series). RAMP's parameter name references thermal variability specifically, but nothing prevents applying the same mechanism to a different physical source of power variability — e.g., device-charging electronics (CC-CV current taper as a battery approaches full charge) rather than temperature. When repurposed this way, state the actual physical mechanism explicitly rather than letting the parameter's name imply a justification it doesn't have.

Where a specific value isn't grounded in real measurement (lab data, manufacturer specs, or a directly-cited study), it should be recorded as a **declared default**: a stated, reasoned starting value, explicitly flagged as pending real data rather than presented as measured. State the reasoning (e.g., known charging-curve physics, device-type diversity) so the value is defensible even before real data replaces it, and flag any downstream result that turns out to be sensitive to the exact figure chosen.

*§9 is the last per-appliance parameter. The one household-level parameter, `prob_home` — [OCC], is specified in **§10**, which sits further down under "Handled outside per-appliance parameters" because that is what it is: a property of the household, applied to all of its VAs at once.*


## 10. `prob_home` — [OCC] (household-level occupancy)

The probability that a household of the profile is **present** on a given day. This is the quantification of a structural-absence, and the only parameter in this protocol that is not a property of an appliance. One presence draw is made per household per day and gates every VA of that household together, so an absent household produces exactly zero load that day — which is the whole point of deriving it separately. Encoding the same absence in each appliance's `occasional_use` would give every appliance its own independent absence die and produce incoherent days: some VAs of one routine running while others that belong to it do not.

**Eligibility (who enters the arithmetic).** Only households meeting the diagnostic bar stated above **and** carrying a *stated duration* — a specific number of weeks or months, or an explicitly dated window. Three exclusions follow, and each must be named in the profile rather than silently applied:

- **Mobility without a duration is excluded.** A household described as leaving for the *monte* or the mine, with no stated length, contributes nothing to the numerator. It is real absence that the arithmetic cannot see.
- **Absence without an empty house is excluded.** Where resident kin sustain a load during the household's absence, or where the pattern may be a narrower commute-for-tasks rather than a departure, the occupancy consequence is not established. Check for a resident-baseline offset explicitly; do not assume absence implies zero load.
- **`migration_label` is never a substitute** for either, per the paragraph above.

Because the first two exclusions only ever remove absence, **a derived `prob_home` is an upper bound on presence, never a point estimate.** State this in the profile. It aligns with the independent directional finding that self-reports overstate presence, which makes the bound the conservative direction rather than an arbitrary one.

**Derivation rule.**

1. Convert each eligible household's stated absence to **household-months**.
2. **Annual value:** `prob_home = 1 − (Σ absent household-months ÷ (N_interview × 12))`. The denominator is the *full* interviewed base, not the eligible subset — the parameter describes the profile, in which non-absent households are a real and load-bearing majority.
3. **Seasonal values,** only where the evidence itself places the absence in particular months (a dated window, or a named migration season): distribute each household's months into seasons, capped by each season's own length, and compute `prob_home(season) = 1 − (absent household-months in season ÷ (N_interview × months in season))`. Where a stated duration exceeds the window it is associated with, the excess spills to adjacent months rather than being discarded or double-counted.
4. Round to two decimals. Check that the month-weighted mean of the seasonal values reproduces the annual value — if it doesn't, the distribution in step 3 has lost or duplicated household-months.

Report the arithmetic in the truth file, not just the result: the household table with each stated duration and its source, the sums, and the division. The step that carries the most interpretive weight is step 3's distribution, and it is the step a reader is most likely to want to redo differently.

**Confidence must be reported separately for level and shape.** These are two different claims resting on different evidence, and one is routinely much weaker than the other. The *level* (annual absent fraction) is carried by every eligible household. The *seasonal shape* is carried only by those whose absence has a dated window — so a profile with one dated household and two aseasonal ones has a well-supported level and a shape resting on a single case. Where that is so, say it, and name the flat-annual alternative as the conservative sensitivity variant.

**Declare `prob_home: null`, never a token value, where no eligible household exists.** This mirrors the retired-VA/placeholder distinction in the structural-requirements section above: continuous occupancy attested by respondents is a substantive finding and should be recorded as one. It is also the numerically safer choice — `null` skips the presence draw entirely rather than drawing against a probability of 1, so a profile declared sedentary keeps a random stream identical to a run predating this parameter, and its already-computed results stay reproducible.


**Applied values (as of 2026-08-18).**

| Profile | `prob_home` | Basis in brief |
|---|---|---|
| 1 — Agricultural Core | `null` | Single thin dual-residence account (≈1 month/yr) computes to ≈0.995, below the resolution of a daily draw; the season's partial absence is already in the per-VA floors, so a mask would double-count |
| 2 — Isolated Elderly | `null` | Continuous 365-day occupancy, attested by respondents and corroborated by a field memo for all nine interviews. The study's presence baseline |
| 3 — Extended Hub | 0.96; 0.78 in free grazing | Two eligible households (6 and 3 months); the migration window concentrates two-thirds of those months in Jul–Sep. Four further mobile households are ineligible for want of a stated duration |
| 4 — System Breakers | 0.69 / 0.61 / 0.61 / 0.78 by season, 0.68 annual | Three eligible households (a dated Dec–June window, a fortnightly alternation, a relocation). Inverts the community's seasonal shape: presence is lowest in growing and harvesting. Level well-supported, shape resting on the one dated window |

**Authoring and implementation.** `prob_home` is authored in each truth file's Seasonality section as a single fenced ```` ```yaml occupancy ```` block (`prob_home`, optional `seasonal_prob_home`, and `occasional_use_basis` declaring the §8 reading), parsed by `extract_parameters.py` into the profile JSON, resolved per season by `season_resolve.py`, and passed to RAMP's `User.prob_home`. Three limitations of the engine-side mechanism affect how a profile may be written:

- The mask gates **every** appliance of the household, including ones declared `flat`. A load that genuinely continues during absence must be assigned to a separate always-present user — the pipeline does this automatically for `flat` VAs, but the modeling decision is the analyst's.
- It is **not supported with RAMP's parallel processing**, which loses the grouping of appliances into individual households.
- It is **not part of RAMP's .xlsx model format**, so it exists only in the Python-side parameters — a model round-tripped through .xlsx silently loses it.


## How this protocol was derived (methods note)

The crosswalks were built inductively, not imposed: transcripts were searched for the language respondents use to express frequency and timing-stability; recurring expressions were binned; each bin was validated against anchor quotes from *multiple* profiles (licensing a single universal crosswalk, and supporting the transferability claim of §5.4); and the scheme was revised where transcript evidence contradicted an initial definition. Recorded revisions: (1) "Chaos" redefined from an outcome criterion to an epistemic one; (2) a proposed conditional-VA mechanism for weather- and psychological-triggered practices was retired, since no trigger was ever collected as a systematically measured study variable — such practices are Chaos instead, an extension of the epistemic definition to cover data-availability as well as respondent uncertainty; (3) structural absence separated as a household-level axis keyed to migration status rather than profile; (4) window-grounding corrected from a median-of-widths statistic to the true modal survey code, after the former was found to produce windows no respondent had actually reported (caught and fixed in three separate cases during Profile 1's finalization); (5) two VA-set-level structural requirements — window continuity for shared-hardware VAs, and a conservation-logic plausibility check before modeling any VA — were added after being applied ad hoc to Profile 1 without first being stated as general rules; (6) the population table's classification source was updated to `classifications_oficial.csv`, adopted for every household except ids 58 and 83, where a documented qualitative override is retained; ids 7 and 67 move to Profile 3, id 88 to Profile 1, and ids 58 and 83 stay with Profile 1 under the override — all four truth files reflect this membership; (7) field memos (`memos.csv`) were formalized as a distinct, dated evidence tier — `[FIELD MEMO: caseid, date]`, ranked between interview transcript and undocumented conversational recall — after their coverage was checked household-by-household against `all_transcripts.txt` and found to corroborate, not replace, existing transcript-based evidence throughout the sample; (8) 2026-08-18 — the structural-absence axis moved from *documented but deferred* to *applied*, gaining a sixth derivation source **[OCC]** and a quantified parameter, `prob_home` (§10). This was a translation of evidence already collected and already reasoned about, not new fieldwork: the diagnostic bar, the `migration_label` exclusion, and the anchors were all fixed by revision (3), and what §10 adds is the arithmetic that turns stated absence durations into a probability, the eligibility rule that keeps unquantified mobility out of the numerator (making every derived value an upper bound on presence), and the double-counting rule governing when the mask may and may not coexist with per-VA seasonal reductions. Two of the four profiles resolve to `prob_home: null` on their own evidence, which is a recorded finding of continuous occupancy rather than a default. Every applied value traces to ≥1 anchor quote (respondent ID, profile, date); a full quote-by-quote mapping lives in the supplementary provenance file.