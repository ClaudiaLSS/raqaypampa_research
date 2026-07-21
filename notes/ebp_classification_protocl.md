# EBP Classification Protocol

A step-by-step guide to the household stratification method used to assign
Energy Behavior Profiles (EBPs), written to be replicable in another
community/dataset and to be adapted directly into a paper's methods section.

---

## 1. What this method is for

The goal is to sort households into a small number of structurally
distinct profiles — using only **fixed, survey-derived fields** — so that:

- the rule can be applied identically and transparently to every surveyed
  household, including the ones who were never interviewed;
- a reviewer can rerun it and get the same answer;
- qualitative data (interviews, field memos) can then be used *downstream*
  to characterize and validate each profile, without that qualitative
  data having been used to decide who belongs to which profile in the
  first place (which would make any later "our interviews confirm the
  profile's behavior" claim circular).

If your qualitative fieldwork later suggests a specific field was
**miscoded** for a specific household, the correct move is to correct that
field at its source (see §5) and rerun the same fixed rule — not to
special-case that household's assignment by hand.

---

## 2. Define the profiles theoretically, then map each one to observable fields

Before writing any code, write down — in plain language — what
distinguishes each profile as a *behavioral/structural type*, then map
each defining trait onto one specific, already-collected survey variable.
In this study:

| Profile | Theoretical definition | Structural proxy used |
|---|---|---|
| 1 — Educational/Agricultural Core | A nuclear or stable extended household organized around children's schooling | `family_type` (nuclear or stable-extended codes) + `children_in_school` |
| 2 — Isolated Elderly | Single-person or childless-couple households, generally elderly | `family_type` (unipersonal / couple codes) |
| 3 — Extended Hub | Numerous or extended households with competing internal demand for energy/devices | `family_type` (numerous/extended codes) as the residual of Profile 1 |
| 4 — System Breakers | Households whose routine is structurally decoupled from the settlement (miners, students, or anyone not captured by the above) | `occupation` (breaker occupations) as an override, plus residual catch-all |

Do this mapping explicitly and write it down — it is the single most
important design decision, and it's the first thing worth re-examining if
the resulting profiles don't look right later (see §6).

---

## 3. Required fields and their codes

| Variable | Meaning | Codes |
|---|---|---|
| `family_type` | Household composition | 1 Unipersonal · 2 Monoparental · 3 Monoparental numeroso · 4 Pareja nuclear · 5 Nuclear completo · 6 Nuclear completo numeroso · 7 Extendido · 8 Extendido sin hijos · 9 Extendido numeroso · 10 Extendido numeroso sin hijos |
| `occupation` | Main occupation of household head | 1 Domestic labour · 2 Agriculture · 3 Student · 4 Mining |
| `children_in_school` | Whether the family has children in school | 0 No · 1 Yes |
| `migration` | Whether a family member migrates temporarily | 0 No · 1 Yes |
| `portability_shs` | Whether the family keeps the solar home system mostly at home | 0 No · 1 Yes |

**Scope note:** confirm which survey wave/instrument actually contains
every field the rule needs *before* fixing your population. In this study,
`portability_shs` only existed in the social-practices survey, not the
socioeconomic survey — so the classified population was implicitly capped
at the intersection of the two survey waves (N=65 of 100 socioeconomic
respondents), not the full socioeconomic sample. That's a legitimate scope
decision, but it must be a *decision*, documented in the methods section
and reflected in your reported N — not something a reader discovers by
noticing your classified list is shorter than your survey list.

---

## 4. Write the rule as an explicit, ordered decision tree

State the rule as a strict hierarchy, evaluated in this order, and stop at
the first match. This is the part that most benefits from being written
in prose *before* being written in code — logic bugs hide easily in
`isin([...])` lists, and are much easier to catch by reading a sentence
than by reading a list of integers.

1. **Determine if the occupation is a "system breaker" occupation**
   (Student or Mining). This is an override that will matter in every
   subsequent step.
2. **Profile 2 (Isolated Elderly):** if `family_type` is Unipersonal or
   Pareja nuclear, AND the occupation is *not* a breaker occupation →
   Profile 2. Stop.
3. **Profile 1 (Educational/Agricultural Core):** if the occupation is
   *not* a breaker occupation, AND either:
   - `family_type` is a nuclear code (Monoparental, Monoparental
     numeroso, Nuclear completo, Nuclear completo numeroso) **and**
     `children_in_school = Yes`; **or**
   - `family_type` is an extended code (Extendido and its numerous/
     childless variants) **and** `children_in_school = Yes` **and** the
     household is "stable" (`migration = No` **and**
     `portability_shs = Yes`)

   → Profile 1. Stop.

   *Design note:* every extended-family code must clear the same
   stability bar. Don't let one extended code slip into the easier
   nuclear path by accident — this was the actual bug found and fixed in
   this study (see §6, Case 1).
4. **Profile 3 (Extended Hub):** if the occupation is *not* a breaker
   occupation, AND `family_type` is a numerous or extended code, AND the
   household didn't qualify for Profile 1 → Profile 3. Stop.
5. **Profile 4 (System Breakers):** everyone left over — including every
   breaker occupation, regardless of family structure.

This ordering matters: a breaker occupation always wins over family
structure, and Profile 1 is always attempted before a household is
allowed to fall into the "extended, unstable" catch-all of Profile 3.

---

## 5. Handle missing data by testing sensitivity, not by silent defaults

Real survey data has missing/not-collected values (commonly coded `-1`).
The naive failure mode is to let a missing value pass silently through a
boolean comparison — e.g. `migration != 1` evaluates `True` when
`migration` is actually missing, silently treating "unknown" as "confirmed
non-migrant." This produces classifications that look complete but are
partly fabricated.

**Protocol:** for every household with one or more missing required
fields:

1. Enumerate every plausible coded value for each missing field (per the
   codebook's valid range).
2. Hold all known fields fixed, and re-run the classification rule for
   every combination of plausible values for the missing field(s).
3. If **every** combination produces the same profile, assign that
   profile — the missing field turns out not to be decisive for this
   household, and there is no need to discard a household whose outcome
   is actually fully determined by what you do know (e.g. a known
   breaker occupation alone determines Profile 4, no matter what family
   structure is unrecorded).
4. If combinations disagree, leave the household **explicitly**
   "Unclassified — Insufficient Data," and log which field(s) drove the
   ambiguity and which profiles were in play. Do not guess, even if one
   outcome seems more "typical."

This is mechanical and requires no judgment calls, which is exactly why
it belongs in the script rather than in a case-by-case manual decision.

---

## 6. Correcting individual data points: when and how

Two different kinds of "problem" surface once you sit with a
classification, and they call for different responses.

**(a) A logic bug in the rule itself** — the rule doesn't do what its own
documentation/comments say it does. Fix the code, document the fix (what
was wrong, why, what changed), and rerun on the whole dataset. This
affects every household the buggy branch touched, not just the one that
happened to prompt the investigation.

**(b) A specific field looks miscoded for a specific household** — this
is where qualitative data (interviews, field memos) legitimately enters
the process, but only as a **field-level correction with a documented
justification**, never as a direct override of the profile label. The
protocol used in this study:

1. A household's assignment looks surprising or is flagged by a
   concordance check (see §7).
2. Read the interview/memo directly and check it against the *specific
   coded field* that's driving the assignment — not against the profile
   label itself. ("Does the transcript support `family_type = Extendido`
   specifically — i.e., non-nuclear kin co-residing?" not "does the
   transcript feel like Profile 3?")
3. If the qualitative record clearly contradicts the coded value (e.g. a
   respondent explicitly describes grown children who moved out, which
   doesn't meet the codebook's definition of "Extendido"), correct the
   field at the source, with a written justification citing what in the
   record supports the correction.
4. Rerun the same, unchanged classification rule on the corrected data.
   Never hand-assign the resulting profile.
5. Log the correction: which household, which field, old value, new
   value, what evidence justified it, and — critically — **whether the
   correction actually changes the classification outcome**. A field can
   be wrong and still not matter (see the "Claudio" case below); a field
   can also be entangled with another missing/contested field such that
   fixing one alone doesn't resolve anything (see the "Vicente" case
   below) — check the entangled field too before concluding a household
   is settled.

**Cases from this study, as worked examples:**

- *Guillermo (id 72):* interview showed the co-resident household was
  nuclear-shaped (parents + resident children only; two adult children
  who'd moved away were being mentioned, not co-residing), not
  "Extendido" in the codebook's co-residence sense. Corrected
  `family_type` from 7 to 5. Outcome changed: Profile 3 → Profile 1.
- *Claudio (id 65):* occupation was known (Student, a breaker occupation)
  but three other fields were missing. Per §5, the missing fields didn't
  matter — a known breaker occupation alone determines Profile 4. No
  qualitative correction was needed or attempted; the sensitivity check
  alone resolved it.
- *Vicente (id 88):* `occupation` was missing (the decisive field) *and*
  `children_in_school = No` was in direct contradiction with his own
  transcript. Checked a second survey wave for a cross-reference (found
  none — the value was missing at the source in both waves, not a
  linkage artifact) before treating it as a genuine gap. Both fields were
  eventually corrected based on the researcher's independent field
  knowledge — not the transcript, which never mentioned his occupation.
  Correcting only one of the two fields would have left the household
  still ambiguous between two different profiles; both had to be fixed
  together before the sensitivity check could resolve to a single profile.

---

## 7. Validate the finished classification against qualitative data — without editing it

Once the survey-based classification is finalized, build a **concordance
check**: for every household with an interview and/or memo, screen the
qualitative text for markers associated with each profile's defining
theme (e.g. explicit dual-residence language for Profile 4, isolation
language for Profile 2). Flag disagreements between the strongest
qualitative theme present and the theme expected for the assigned
profile, for manual review.

This step is validation, not reassignment: it never edits
`ebp_profile` directly. It does two things:
- catches candidates for the field-level correction process in §6;
- produces a reportable validity statistic (e.g. "X% of interviewed
  households showed no thematic conflict with their survey-derived
  profile") that is itself a legitimate mixed-methods finding, rather
  than a silent adjustment.

Expect real false positives from keyword screening (e.g. someone
mentioning a relative's mining job, or a hypothetical "someday" plan,
will trigger a keyword without indicating a genuine mismatch) — the
screen is meant to narrow 65 households down to a manageable review list,
not to render a verdict by itself.

---

## 8. What to report in a methods section

At minimum:
- The full decision tree (§4), stated in prose, with the variable→profile
  mapping table (§2).
- The scope of the classified population and *why* (§3) — e.g. which
  survey wave(s) supplied which required field, and what that implies
  about N.
- The missing-data policy (§5) — how many households needed it, how many
  were resolved without ambiguity vs. left unclassified, and why.
- Any individual field-level corrections made from qualitative evidence
  (§6): how many, on what basis, and their effect on final counts. This
  belongs in the methods section (or an appendix table), not just a lab
  notebook — it's the difference between a fixed algorithmic
  classification and a set of ad hoc individual judgment calls, and
  reviewers will want to see that the latter was kept small, documented,
  and principled.
- The concordance-check result (§7), if performed, as a validity check.

---

## 9. Recipe for adapting this to a new case

1. Write your profile theory in plain language (§2) before touching data.
2. Map each profile trait to one specific already-collected variable.
   Prefer variables that exist in every wave/instrument you plan to draw
   your population from — don't let a rule silently define your scope.
3. Write the decision tree in prose, in strict priority order, and read
   it back against the profile theory: does each branch actually test
   what the theory says it should?
4. Implement the rule as a single-household function (not vectorized
   pandas boolean masks) — it's far easier to unit-test and to brute-force
   for missing-data sensitivity (§5) than a chain of `.isin()` masks.
5. Validate the *code* against its own comments/docstring line by line —
   the bug found in this study was exactly a mismatch between what a
   comment said and what the code did.
6. Run the missing-data sensitivity check (§5) before ever manually
   inspecting or "fixing" an unclassified household — most of them may
   resolve on their own.
7. Only then bring in qualitative data, and only as a field-level,
   documented correction process (§6), never a direct label override.
8. Build the concordance check (§7) last, as an independent validity
   layer over the finished classification.