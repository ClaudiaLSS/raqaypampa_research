# Modeling Household Energy Behavior in Raqaypampa, Bolivia

Research compendium for the manuscript:

> **A Socio-Technical Framework for Modeling Household Energy Behavior in Remote Rural
> Electrification: A case in Raqaypampa, Bolivia**
> Claudia Sanchez-Solis, Sergio Balderrama, Jaime Zambrana, Sylvain Quoilin.
> *In press / forthcoming, 2026.*

The study derives four household behavioural profiles for solar-home-system (SHS) users in
Raqaypampa, Bolivia, from a mixed-methods base (semi-structured interviews, surveys and
five-minute datalogger telemetry), encodes each profile as an auditable "truth file", and
simulates them as stochastic load profiles with a forked build of the RAMP demand model.

> **Status: pre-publication.** See [Citation and data use](#citation-and-data-use) before
> using anything here.

---

## The model: a forked RAMP build

**The published results cannot be reproduced with upstream RAMP.** This is not a matter of
convenience or version drift: the study needs two modelling capabilities that upstream RAMP
does not provide, and both were implemented in a fork before the simulations were run.

| | |
|---|---|
| Upstream base | [`RAMP-project/RAMP`](https://github.com/RAMP-project/RAMP) v0.5.2, commit `13e0cee` |
| Fork used | [`ClaudiaLSS/RAMP`](https://github.com/ClaudiaLSS/RAMP), branch `paper-dev`, commit `4a8f445` (2026-08-13) |
| Divergences | three commits, documented in the fork's `FORK_NOTES.md` |

### What the fork changes, and why the paper needs it

**1. Windows of use crossing midnight** — *required.*
Appliance windows may end beyond minute 1440, and the portion of a switch-on event past
midnight carries over to the following morning instead of being truncated. The overnight
virtual appliances in every profile are declared as `[1320, 1680]` (22:00–04:00) and
`[1320, 1740]`; on upstream these windows are silently cut at midnight, losing the entire
overnight load that the "hacer amanecer" practice consists of.

**2. Household-level occupancy mask (`User.prob_home`)** — *required.*
One presence draw per household per day gates every appliance of that household together, so
an absent household produces exactly zero load that day. Upstream has no notion of occupancy;
the only approximation is lowering each appliance's `occasional_use` independently, which
produces incoherent days in which half a routine runs. Profiles 3 and 4 set `prob_home`
(0.96/0.78 and 0.69/0.61/0.61/0.78 respectively) and raise a `TypeError` on an upstream build.
Profiles 1 and 2 set `prob_home: null` and run on either.

**3. `calc_peak_time_range` no longer depends on simulation state** — *correctness only.*
Upstream derives the "theoretical maximum profile" from an attribute that is overwritten with
realised load during a run, and raises `IndexError` when the maximum falls on a single minute.
Fixing it does not change any result in this paper, because every virtual appliance carries
`number = 1`.

Presence and `occasional_use` compose multiplicatively:
`P(appliance runs on a day) = prob_home × occasional_use`. With the mask active,
`occasional_use` is defined as a fraction of *home* days, and the truth files author it on
that basis.

### Installing the model

```bash
git clone https://github.com/ClaudiaLSS/RAMP.git
cd RAMP
git checkout raqaypampa-paper-v1     # the frozen tag, not the moving paper-dev branch
pip install -e .
```

Verify you have the right build before running anything:

```python
import inspect
from ramp import User
assert "prob_home" in inspect.signature(User.__init__).parameters
```

`run_simulation.py` performs this check itself and fails with an explicit message rather than
silently producing upstream results.

> **TODO before submission.** The `raqaypampa-paper-v1` tag exists locally but has not yet
> been pushed, so the model dependency is not yet independently obtainable. Push the branch
> and the tag, archive the tag on Zenodo for a DOI, and add that DOI here and in the
> manuscript's methods section.

### A known upstream defect, documented but not fixed

`UseCase.calc_peak_time_range` treats the set of minutes attaining the aggregate maximum as
one contiguous interval. For any bimodal load shape (morning plus evening lighting suffices)
it is not, and the peak time is drawn from a gaussian centred in the *gap* between the two
blocks. Profiles 1 and 3 run alone are affected; the four-profile community run is not,
because heterogeneous authored powers (2.0/2.5/3.0 W) break the ties.

This does not reach the published results — at `number = 1` the in-peak and off-peak branches
both return exactly 1, so the peak window changes which random numbers are consumed but no
load value. It is left unfixed deliberately and analysed in full in
`scratch/ramp_peak_window_defect.md` (untracked; available on request).

Two cautions carried into any future work: do not report `peak_time_range` for a
single-profile run of Profile 1 or 3, and revisit the issue before introducing any virtual
appliance with `number > 1`.

---

## Repository layout

```
data/
  clean/            interviews, surveys, five-minute datalogger timeseries
    profiles/       the four profile truth files  <- parameter source of record
  metadata/         participant and instrument metadata
manuscript/         LaTeX sources (elsarticle) and figures
notes/              supplementary material
scripts/
  modeling/v2/      current pipeline: extraction -> simulation -> validation
  modeling/v1/      superseded first-approach pipeline, kept for provenance
  plots/            manuscript figure generation
  surveys/          survey processing and classification
  text/             interview metadata and QualCoder qualitative coding
  timeseries/       datalogger preprocessing, cleaning and analysis
```

**Not tracked in git** (see `.gitignore`): `data/raw/`, `results/` and `scratch/`. The
repository ships the cleaned inputs and the code that regenerates the outputs, not the
outputs themselves. Raw data and intermediate scratch notes are available from the
corresponding author on request.

### The truth files are the source of record

`data/clean/profiles/profile_*.md` are not documentation of the model — they *are* the model
input. Each file carries the anthropological reasoning, the anchor quotes that ground it, and
fenced YAML blocks holding the RAMP parameters for every virtual appliance.
`extract_parameters.py` reads those YAML blocks directly. **New or revised parameters are
authored in the markdown and flow outward; they are never hardcoded in the scripts.** The §5
summary table in each file is a convenience mirror of those blocks.

---

## Reproducing the results

Requires the forked RAMP build above, plus `pandas`, `numpy`, `pyarrow` and `matplotlib`.
Run from `scripts/modeling/v2/`.

```bash
# 1. Extract RAMP parameters from the four truth files
python extract_parameters.py --profiles_dir ../../data/clean/profiles --output_dir parameters

# 2. Simulate a full calendar year per profile (profile_0 = homogeneous baseline, "Model A")
python run_simulation.py --profile_json parameters/profile_1_params.json \
    --output_dir simulation_results --year 2024 --n_households 1
#   ... repeat for profiles 2, 3, 4 and 0

# 3. Validate each profile against its empirical baseline (May)
python validate_simulation.py --baseline 1 --profile 1 --months 5
#   ... repeat for profiles 2, 3, 4

# 4. Community run: 28/11/14/12 households by profile, plus 65 homogeneous
python run_community.py --params_dir parameters --counts 1=28,2=11,3=14,4=12 \
    --homogeneous_json parameters/profile_0_params.json --homogeneous_pid 0 \
    --homogeneous_n 65 --output_dir sim_community --year 2024 --seed 42
python validate_community.py --community_dir community_results

# 5. Manuscript figures
cd ../../plots && python run_all.py --out ../../manuscript/Figures
```

Simulations are stochastic. `run_community.py` takes an explicit `--seed`; the per-profile
runs do not, so figures regenerated without seeding will differ within Monte-Carlo noise.

> **TODO:** add a pinned `requirements.txt` or `environment.yml`. The defect analysis was
> carried out on Python 3.10.16 with numpy 1.26.4, and no environment specification is
> currently committed.

---

## Citation and data use

**Status: pre-publication / in press.** If you use this data or code for any analysis,
visualisation or publication, you are required to cite:

> Claudia Sanchez-Solis, Sergio Balderrama, Jaime Zambrana, Sylvain Quoilin,
> "A Socio-Technical Framework for Modeling Household Energy Behavior in Remote Rural
> Electrification: A case in Raqaypampa, Bolivia", 2026. (In press / forthcoming.)

Because this research is not yet published, please **contact the lead author before
submitting any work that uses this dataset**, so that overlap with the primary findings of
the ARES-funded project can be checked.

The interview and survey material concerns identifiable individuals in a small community and
is shared for scholarly verification. Do not redistribute it, and do not attempt to
re-identify participants.

## Acknowledgements

Collected and processed as part of *Tailored Energy Systems for Energy Planning in Bolivia*.
We gratefully acknowledge the financial support and partnership of ARES (Académie de
Recherche et d'Enseignement Supérieur).

## Contact

Claudia Sanchez-Solis — <clsanchez@uliege.be>
