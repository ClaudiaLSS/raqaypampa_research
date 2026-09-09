## Section S3: Parameter derivation protocol

This section is the source describing how each RAMP parameter in the Model B (socio-technical) parametrization is derived. Profile truth files reference this section rather than reproducing it, so revisions propagate consistently.

Every parameter falls into one of six derivation sources, stated explicitly so that no value is left without a declared basis. Five of the six derive a **per-appliance** parameter; two of those five are **crosswalks** — classification steps that sort respondent language into bins. The sixth derives the one **household-level** parameter, which is not a property of any appliance:

- **[SPEC]** — technical hardware specification (not behavioral; no qualitative translation)
- **[WINDOW]** — derived from the Anthropological Window (interview × survey triangulation)
- **[FREQ-XW]** — frequency crosswalk (Table 1, Section S2.2): respondent frequency language → `occasional_use`
- **[RIG-XW]** — rigidity crosswalk (Table 2, Section S2.2): the qualitative account → a rigidity bin (Strict / Flexible / Chaos), which *is* the variability classification
- **[DECLARED DEFAULT]** — a stated, reasoned value used when neither qualitative nor quantitative data directly speaks to a parameter; flagged as pending real data, never presented as derived.
- **[OCC]** — occupancy derivation: stated absence durations → `prob_home`, the probability a household of the profile is present on a given day. Household-level, not per-appliance: one value per profile (optionally per season), gating *every* VA of that household at once.

A note on the two crosswalks, since they are the same kind of object: both **[FREQ-XW]** and **[RIG-XW]** are classification steps that read respondent language and assign a bin. The rigidity crosswalk (Table 2, Section S2.2) directly yields `time_fraction_random_variability` and `random_var_w` (they are the bin's assigned values). One parameter, `func_cycle`, is a **second-order derivation**: it takes the rigidity bin and applies a further rule (fraction of `func_time`), so it is marked [RIG-XW → func_time] to show it is one step removed rather than a direct crosswalk output.

**A further distinction governs citation, not derivation, and sits underneath [WINDOW]/[FREQ-XW]/[RIG-XW] rather than beside them.** §S3.1 below defines a three-tier auditability hierarchy for the *qualitative material itself* — interview transcript, field memo, conversational recall. This hierarchy does not add a new kind of RAMP-parameter derivation; it governs how solidly a given [WINDOW]/[FREQ-XW]/[RIG-XW] value is sourced, and is recorded in the `— source:` trailer, not in the derivation tag.

One phenomenon is handled *outside* the per-appliance parameters: **household-level structural absence** (migration/dual-residence), which since 2026-08-18 is an applied model parameter rather than a documented-but-deferred one — it is derived via **[OCC]** into `prob_home` and simulated as RAMP's household-level occupancy mask. 

---

**Population and generalization (who the qualitative parameters actually describe)**

The `ebp_profile` classification is itself survey-derived (family_type, occupation, children_in_school, migration, portability_shs). This means **every classified household has survey data**, but only a subset was also interviewed. Each profile therefore has two population sizes, not one:

- **N_survey** — everyone classified into the profile (defines who counts as that EBP)
- **N_interview** — the subset also interviewed (the only source of qualitative material)

| Truth-file output | Population it draws from | Why |
|---|---|---|
| Windows (`window1`, `window2`) | **N_interview + N_survey** (triangulated) | Anthropological Windows are derived by triangulating interview accounts of practice timing with survey time-use data and hard physical anchors (sunrise/sunset) — survey and physical data alone can't supply the cultural framing, and interview accounts alone can't supply population-scale timing or fixed astronomical anchors |
| Rigidity classification (incl. Extreme/Structural), narrative, frequency-language `occasional_use` | **N_interview only** | Requires actual quotes — a household with no transcript can't supply timing statements, hedging language, or evidence of a dual-household strategy |
| `prob_home` — [OCC], household-level occupancy (§10) | **N_interview only** as the numerator *and* the denominator | Requires a stated absence duration, which only a transcript supplies. The denominator is the full interviewed base, so the value describes the profile rather than its mobile subset — and `migration_label` cannot substitute for the missing survey households |
| Ownership/appliance-count parameters | **N_survey (full)**, where the survey captured them | Structural, not behavioral |

### S3.1 Evidence tiers within Stream A (QUAL): transcript, field memo, conversational recall

Not all qualitative material carries the same auditability. Three tiers, ranked by how independently checkable the claim is:

1. **Interview transcript** (`all_transcripts.txt`) — verbatim, dated, attributable to a named respondent. The primary source underlying N_interview and the sole source for Table A/B crosswalk anchors, since those require the respondent's *own phrasing* (hedging language, frequency markers, timing statements), not a paraphrase.
2. **[FIELD MEMO: caseid, date]** — a written, dated field note (`memos.csv`, authored by the field researcher, Claudia). Close to interview transcript in auditability — it is a specific, attributable, dated document, not recall — but it is a *summary*, not a verbatim quote, so it does not carry a respondent's own frequency/timing language. Field memos are the right evidence for **structural and demographic facts**: household composition, migration/dual-residence pattern, hardware inventory and ownership history, occupation. They should **corroborate or independently establish structural claims**, not substitute for a transcript anchor in Table A/B.
3. **[FIELD OBS: conversational]** — an undocumented exchange recalled by a researcher, with no dated written record. The weakest tier. Never used as the sole basis for a parameter; flag explicitly wherever it appears, and prefer corroboration from tier 1 or 2 before treating it as evidence at all.

**Practical rule:** a `— source:` trailer citing a field memo takes the form `[FIELD MEMO: caseid NN, DD/MM/YYYY]`; a trailer citing undocumented recall takes the form `[FIELD OBS: conversational]`. Do not fold the two into one tag — the split exists precisely so a reader can see which claims rest on a citable document and which rest on memory.

**Coverage check (this dataset).** Cross-referencing `memos.csv` (household `name` field = `user_<id>`) against `all_transcripts.txt` (`user_ID`) shows that in every profile, **every household with a field memo also has an interview transcript** — there is no household in this dataset whose only qualitative evidence is a memo. (The single near-exception is id 67, Dionisio Vargas Castro, Profile 3: interviewed, no memo on file — the reverse direction, not a memo-only case.) This means field memos do not, in this dataset, expand N_interview beyond what transcripts already establish; a hypothetical **N_memo** population (memo but no transcript) is currently empty and the population table below does not need a third column for it.

**Extreme/Structural is not a survey-derived exception.** The diagnostic signal is a **dual-household strategy** — a household genuinely alternating between two residences with two different energy setups (the clearest case being Guillermo Romero: off-grid panel at one residence, paying ELFEC at a second) — and that can only be identified from what a respondent describes in an interview, not from a survey checkbox. So Extreme/Structural assignment requires N_interview evidence, the same as every other rigidity-derived parameter, with **no exception**.

**Concrete example:** if household #50 in Profile 2 was never interviewed, you cannot know whether it practices dual-residence — there is no survey field that reliably tells you this. Its Extreme/Structural status, like its Windows and Rigidity, must be inherited from the profile's interviewed pattern (the generalization described below) rather than individually assigned.

**The honest consequence:** Windows and Rigidity — the qualitative heart of the model — describe a pattern inferred from N_interview, then applied as parametrization for the *entire* N_survey population at simulation time. This is standard qualitative practice (representative-case inference), but it must be stated explicitly rather than left implicit, so a reviewer sees how many actual voices stand behind each profile's model rather than assuming every simulated household was individually evidenced.

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

**A related, more fundamental limitation: single-period survey questions structurally capture typical behavior, not occasional behavior.** A categorical period-code question (e.g., "when do you use light_1 at night?") can only record one representative window per respondent — it has no way to express "usually X, but sometimes Y under specific circumstances." This is not a data-quality problem or a respondent error; it is a structural limit of the question format itself. When a respondent's interview account describes something that appears to exceed or diverge from their own survey answer (e.g., an occasional, trigger-driven practice layered on top of an ordinary routine), the two sources are often not actually in conflict — they are answering different questions the survey was never built to distinguish. This is precisely the kind of layer interview material is positioned to add, and it should be read as *enrichment revealing an additional layer*, not as a Say-Do contradiction requiring the tier-4 "survey wins" tiebreak (§3). The tier-4 rule still applies to genuine disagreements about a practice's *typical* pattern; it should not be invoked reflexively whenever an interview describes something a survey's single-code answer could never have captured in the first place.

**Practical consequence:** a practice that is normally dormant and activates only around an identifiable trigger (a recent fear-inducing incident, a specific social event, an environmental condition) should not be forced into a flat `occasional_use` value that pretends the trigger doesn't exist. But — see the retirement note below — this does **not** mean building a separate conditional-trigger mechanism. Unless the trigger is itself a systematically measured study variable, the honest treatment is **Chaos**: the practice's variability is real and may even have a nameable real-world cause, but the study has no quantified basis for modeling that cause, so it is treated as unpredictable from the data's perspective.







