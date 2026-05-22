# Manual Parameters RAMP Simulation (Script 4)

This script allows you to **manually set RAMP parameters** and generate load profile simulations with **period-based device modeling** (morning, daytime, evening, night).

## Quick Start

### 1. **Run with Default Parameters**
```bash
python 4_manual_parameters_simulation.py --user 74 --days 5
```

This will:
- Load default parameters extracted from user 74's data
- Create 12 appliance models (3 devices × 4 time periods)
- Simulate 5 days of load profiles
- Compare against real measured data
- Generate 3 comparison plots

### 2. **Create & Edit Custom Config**
```bash
python 4_manual_parameters_simulation.py --create-example
```

This creates: `manual_parameters/manual_params_example.json`

Edit the JSON file to adjust parameters, then run:
```bash
python 4_manual_parameters_simulation.py --user 74 --days 5 --config manual_parameters/manual_params_example.json
```

## Quick Parameter Reference

| Parameter | What it Does |
|-----------|--------------|
| `occasional_use` | Probability device is used (0-1, e.g., 0.99 = 99% of days) |
| `avg_minutes` | Average daily usage duration in minutes (e.g., 105.6 min) |
| `std_minutes` | How much daily duration varies (e.g., ±61.7 minutes) |
| `rand_var` | **VARIATION 1:** Randomness in duration (0-0.30) |
| `windows` | Time window when device can run in minutes from midnight |
| `window_var` | **VARIATION 2:** Randomness in when device starts (0-1.0) |

## Parameter Structure

Each device has 4 time periods with these parameters:

```json
{
  "LED_1": {
    "power_W": 2.56,
    "periods": {
      "morning_prep": {
        "occasional_use": 0.39,     # Probability (0-1) device used in this period
        "avg_minutes": 35.4,        # Average daily usage (minutes) in this period
        "std_minutes": 63.2,        # Standard deviation (variability in usage duration)
        "rand_var": 0.30,           # Coefficient of variation for TIME OF USE (max 0.30)
        "windows": [[240, 600]],    # Time window in minutes [start, end] (OPTIONAL)
        "window_var": 0.35          # Variability for WHEN device turns on (OPTIONAL)
      },
      ...
    }
  }
}
```

### Windows Field (Optional)

The `"windows"` field defines **when** the device can be used:
- **Format:** `[[start_minutes, end_minutes]]` or multiple windows `[[start1, end1], [start2, end2]]`
- **Units:** Minutes from midnight (0-1440)
- **Optional:** If not specified, defaults are used (see table below)

**Example: Morning window (4:00 AM to 10:00 AM)**
```json
"windows": [[240, 600]]
// 240 min = 4:00 AM
// 600 min = 10:00 AM
```

**Example: Two separate windows (split usage)**
```json
"windows": [[240, 600], [1020, 1080]]
// Morning: 4:00-10:00
// Evening: 17:00-18:00
```

### Default Windows (Used if not specified)

| Period | Hours | Window (minutes) |
|--------|-------|------------------|
| `morning_prep` | 4-10h | `[[240, 600]]` |
| `daytime` | 10-17h | `[[600, 1020]]` |
| `evening_school_cooking` | 17-24h | `[[1020, 1440]]` |
| `night_security` | 0-4h | `[[0, 240]]` |

### How to Modify Windows

**Edit in your JSON config file:**

```json
{
  "USB": {
    "periods": {
      "daytime": {
        "occasional_use": 0.78,
        "avg_minutes": 166.8,
        "std_minutes": 121.7,
        "rand_var": 0.30,
        "windows": [[600, 1020]]   // ← Change this to set when device can be used
      }
    }
  }
}
```

**Minute Conversion (for reference):**

| Time | Minutes | Time | Minutes |
|------|---------|------|---------|
| 0:00 (midnight) | 0 | 12:00 (noon) | 720 |
| 4:00 AM | 240 | 16:00 (4 PM) | 960 |
| 6:00 AM | 360 | 18:00 (6 PM) | 1080 |
| 8:00 AM | 480 | 20:00 (8 PM) | 1200 |
| 10:00 AM | 600 | 22:00 (10 PM) | 1320 |

**Example: Change morning window from 4-10 AM to 6-9 AM**

```json
// Before
"windows": [[240, 600]]

// After
"windows": [[360, 540]]
```

**Example: Device available all day**

```json
"windows": [[0, 1440]]
```

**Example: Two separate windows (morning and evening)**

```json
"windows": [[240, 600], [1020, 1320]]   // 4-10 AM and 5-10 PM
```

## Time Periods

| Period | Hours | Description |
|--------|-------|-------------|
| `morning_prep` | 4-10h | Early morning (preparation/cooking) |
| `daytime` | 10-17h | Daytime (school/work) |
| `evening_school_cooking` | 17-24h | Evening (school return, cooking, social) |
| `night_security` | 0-4h | Night (security lights, midnight-4am) |

## What Each Parameter Does

### `occasional_use` (0 to 1)
- **0.0** = Never used in this period
- **0.5** = 50% chance of being used on any given day
- **1.0** = Always used in this period

**Example:** LED_1 evening has 0.99 → lights turn on 99% of evenings

### `avg_minutes` 
- Average duration the device is **active** per day in this period
- Only applies on days when `occasional_use` probability triggers

**Example:** LED_1 morning = 35.4 min → when used, lights stay on ~35 minutes

### `std_minutes`
- Variability in usage duration
- High value = inconsistent usage pattern
- Low value = consistent usage pattern

**Example:** USB night = 109.5 min std → highly variable night charging

### `rand_var` (0 to 0.30)
- **What it controls:** Variation in **HOW LONG** the device runs
- Coefficient of variation (std / mean)
- Controls randomness in simulated usage duration
- Capped at 0.30 to keep results realistic

**Example:** LED_1 evening with avg_minutes=105 and std_minutes=61.7:
- Some days: 60 minutes, other days: 150 minutes (realistic variation)

### `window_var` (0 to 1.0) - OPTIONAL
- **What it controls:** Variation in **WHEN** the device turns on within its time window
- Higher value = more random start times
- Lower value = more consistent start times
- **Default:** 0.35 (if not specified in JSON)

**Example:**
- `window_var = 0.1`: Device starts almost same time every day
- `window_var = 0.5`: Device can start anytime within the window

**Together they create realistic patterns:**
- `rand_var = 0.30` → "Duration varies by 30%"
- `window_var = 0.35` → "Start time varies by 35%"

## Usage Examples

### Where to Find Each Parameter in JSON

```json
{
  "LED_1": {
    "power_W": 2.56,
    "periods": {
      "morning_prep": {
        "occasional_use": 0.39,         ← When is device used?
        "avg_minutes": 35.4,            ← How long does it run?
        "std_minutes": 63.2,            ← How much does duration vary?
        "rand_var": 0.30,               ← VARIATION 1: Duration randomness
        "windows": [[240, 600]],        ← What hours can device be used?
        "window_var": 0.35              ← VARIATION 2: Start time randomness
      }
    }
  }
}
```

### Example 1: Adjust Time-of-Use Variation

Increase `rand_var` to make device usage more unpredictable:

```json
"daytime": {
  "occasional_use": 0.78,
  "avg_minutes": 166.8,
  "std_minutes": 121.7,
  "rand_var": 0.50,          ← INCREASE: More variable daily usage
  "windows": [[600, 1020]],
  "window_var": 0.35
}
```

### Example 2: Adjust Window Variability

Decrease `window_var` to make device turn on at consistent times:

```json
"morning_prep": {
  "occasional_use": 0.39,
  "avg_minutes": 35.4,
  "std_minutes": 63.2,
  "rand_var": 0.30,
  "windows": [[240, 600]],
  "window_var": 0.10        ← DECREASE: Consistent start times
}
```

### Example 3: Change When Device Can Be Used

```json
// LED only available during cooking hours (6-8 PM instead of 5-12 AM)
"evening_school_cooking": {
  "occasional_use": 1.0,
  "avg_minutes": 150.0,
  "std_minutes": 40.0,
  "rand_var": 0.25,
  "windows": [[360, 480]]      // 6 PM to 8 PM only (360-480 min from 0:00)
}
```

### Example 4: Increase Evening Usage
```json
// Edit manual_params_example.json
"evening_school_cooking": {
  "occasional_use": 1.0,      # Always on (was 0.99)
  "avg_minutes": 150.0,       # Longer duration (was 105.6)
  "std_minutes": 40.0,        # Less variable (was 61.7)
  "rand_var": 0.25,
  "windows": [[1020, 1440]]   # Keep same time window (5-12 AM)
}
```

Then run:
```bash
python 4_manual_parameters_simulation.py --user 74 --days 5 --config my_config.json
```

### Example 5: Test Lower USB Usage
```python
"USB": {
  "periods": {
    "daytime": {
      "occasional_use": 0.5,       # Only 50% of days (was 0.78)
      "avg_minutes": 100.0,        # Less charging (was 166.8)
      "std_minutes": 50.0,         # More stable (was 121.7)
      "rand_var": 0.30,
      "windows": [[600, 1020]]     # Same daytime window (10 AM - 5 PM)
    }
  }
}
```

## Output Files

### Simulation Results
- **File:** `output/simulated_profile_user_XX_manual.csv`
- **Format:** DateTime, Total Load [W]
- **Resolution:** 1-minute intervals

### Comparison Figures
All saved to `results/timeseries/figures/`:

1. **comparison_manual_user_XX_avg_profile.png**
   - Average daily load curve
   - Real data (black) vs. Simulation (blue dashed)
   - Shows overall pattern match

2. **comparison_manual_user_XX_variability.png**
   - Standard deviation by hour
   - Real variability vs. simulated variability
   - Shows if simulation captures uncertainty

3. **comparison_manual_user_XX_statistics.png**
   - Table comparing mean, max, std dev
   - Shows percentage differences
   - Validates overall magnitude

## Tips for Parameter Tuning

### 1. Customize Time Windows

Change when devices can be used by modifying the `windows` field:

```json
// LED turns on later in morning (7:00-10:00 instead of 4:00-10:00)
"morning_prep": {
  "occasional_use": 0.39,
  "avg_minutes": 35.4,
  "std_minutes": 63.2,
  "rand_var": 0.30,
  "windows": [[420, 600]]   // 7:00 AM = 420 minutes
}

// Device used in two separate time slots
"daytime": {
  "occasional_use": 0.78,
  "avg_minutes": 166.8,
  "std_minutes": 121.7,
  "rand_var": 0.30,
  "windows": [[600, 720], [1200, 1260]]  // 10-12h and 20-21h
}
```

### Minute-to-Hour Conversion

| Time | Minutes |
|------|---------|
| 0:00 (midnight) | 0 |
| 4:00 AM | 240 |
| 8:00 AM | 480 |
| 12:00 PM (noon) | 720 |
| 16:00 (4 PM) | 960 |
| 20:00 (8 PM) | 1200 |
| 23:59 (almost midnight) | 1439 |
| 24:00 (end of day) | 1440 |

**Formula:** Hours × 60 = Minutes
- 4 hours = 4 × 60 = 240 minutes
- 17 hours = 17 × 60 = 1020 minutes

### 2. Match Average Load
Look at real data average power, adjust `avg_minutes` to match:
```bash
# If real data averages 1.0W and simulation averages 0.5W,
# increase avg_minutes for each device
```

### 2. Match Peak Hour Patterns
Check if peaks occur at right times:
- Evening peaks should align with 17-24h period
- Morning peaks with 4-10h period

### 3. Control Variability
- High `std_minutes` → more variable/realistic simulation
- Low `std_minutes` → smoother/more predictable
- Use real data standard deviations as guide

### 4. Test Extreme Scenarios
```python
# Always on device
"occasional_use": 1.0,
"avg_minutes": 1440,  # Full day (24 hours)

# Never used
"occasional_use": 0.0,
"avg_minutes": 0
```

## Workflow for Parameter Extraction

1. **Run Script 1** to extract empirical parameters from real data
   ```bash
   python 1_extract_parameters.py --user 74
   ```
   → Creates `output/empirical_parameters_user_74.json`

2. **Review extracted parameters** to understand your data

3. **Create custom config** by copying example:
   ```bash
   cp manual_parameters/manual_params_example.json manual_parameters/my_user.json
   ```

4. **Edit parameters** to adjust values for hypothesis testing

5. **Run simulations** with custom config:
   ```bash
   python 4_manual_parameters_simulation.py --user 74 --days 30 --config manual_parameters/my_user.json
   ```

6. **Compare plots** against real data to validate assumptions

## Command Reference

| Command | Purpose |
|---------|---------|
| `--user N` | User ID to compare against (required unless --create-example) |
| `--days N` | Number of days to simulate (default: 5) |
| `--config FILE` | Path to custom JSON config file |
| `--create-example` | Generate example config file and exit |

## Example Workflow

```bash
# 1. Create example config
python 4_manual_parameters_simulation.py --create-example

# 2. Copy and edit it
cp manual_parameters/manual_params_example.json manual_parameters/my_hypothesis.json
# ... edit the JSON file ...

# 3. Test with 5 days
python 4_manual_parameters_simulation.py --user 74 --days 5 --config manual_parameters/my_hypothesis.json

# 4. If results look good, run longer simulation
python 4_manual_parameters_simulation.py --user 74 --days 365 --config manual_parameters/my_hypothesis.json

# 5. Compare the plots in results/timeseries/figures/
```

## All 4 Scripts Together

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| **1_extract_parameters.py** | Extract from real data | Real CSV | Parameters JSON |
| **2_run_simulations.py** | Run with period models | Parameters JSON | Simulated CSV |
| **3_plot_comparison.py** | Compare period vs daily | Real CSV + Simulated CSV | Comparison plots |
| **4_manual_parameters_simulation.py** | Manual testing + visualization | Custom JSON config | Simulated CSV + Plots |

---

**Questions?** Check the parameter structure in the generated JSON files or run with `--days 1` for quick testing.
