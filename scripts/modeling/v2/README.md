# Empirical Baseline Extraction Pipeline

## Overview

This refactored pipeline extracts comprehensive empirical metrics from both **OLD** and **TPDIN** datalogger types. The architecture is modular, maintainable, and scales easily to new datalogger formats.

## File Structure

```
scripts/modeling/
├── base_extractor.py              # Common metrics (structural, reliability)
├── tpdin_extractor.py             # Handler for TPDIN (3 appliances)
├── old_extractor.py               # Handler for OLD (2 appliances)
├── extract_empirical_baseline.py  # Main pipeline (auto-detects type)
└── README.md                       # This file
```

## Architecture

### 1. **BaseExtractor** (`base_extractor.py`)
Abstract base class containing all **type-agnostic metrics**:
- **Structural Profiling**: Modal Peak Hour, Base Load, MRSD Chaos Index, Relative Mean Power
- **Reliability Metrics**: Blackout frequency, climatic vs behavioral rates, reliability index

### 2. **TPDINExtractor** (`tpdin_extractor.py`)
Handles TPDIN (newest) dataloggers:
- 3 separate appliances: LED_1, LED_2, USB
- Columns: `v_led_1`, `v_led_2`, `v_usb`, `c_led_1`, `c_led_2`, `c_usb`
- Additional fields: temperature, `c_extra`, etc.

Extracts:
- Hardware (median wattage per appliance)
- Hourly probabilities (per-appliance, per-hour)
- RAMP parameters (per appliance)
- Power variation statistics

### 3. **OldExtractor** (`old_extractor.py`)
Handles OLD (legacy) dataloggers:
- 2 combined appliances: LED (combined), USB
- Columns: `v_led_1`, `v_usb`, `c_led`, `c_usb`
- Solar parameters: `voc`, `isc`

Extracts identical metrics but aggregates LEDs into single appliance.

### 4. **Main Pipeline** (`extract_empirical_baseline.py`)
Orchestrates the extraction:
- Auto-detects datalogger type (filename or column inspection)
- Routes to correct extractor
- Batch processes all files
- Outputs: JSON (per-user), CSV (summary), Hourly matrix

## Usage

### Basic Usage
```bash
# Process all files in data/clean/timeseries
python extract_empirical_baseline.py

# Process only TPDIN dataloggers
python extract_empirical_baseline.py --type tpdin

# Process only OLD dataloggers
python extract_empirical_baseline.py --type old

# Process specific user
python extract_empirical_baseline.py --user 74

# Custom pattern
python extract_empirical_baseline.py --pattern "*_user_7*.csv"
```

## Extracted Metrics

### Hardware Metrics
- Median wattage for each appliance when active

### Temporal Metrics
- Hourly usage probability (per appliance, per hour)
- Peak hours (most common usage time)
- Daily event probability (% days with use)

### RAMP Parameters
- `num_windows`: Number of active periods per day
- `func_time`: Average daily usage time (minutes)
- `func_cycle`: Median continuous usage duration
- `time_fraction_random_variability`: Daily variability (std/mean)
- `random_var_w`: Window variability (std/mean of window sizes)
- `window_1`, `window_2`, etc.: Time-of-day windows (minute ranges)

### Power Variation
- Mean, Std, Coefficient of Variation
- Min/Max/Range/Median
- Quartile ranges (Q25, Q75)

### Tier 2: Structural Profiling
- **Modal Peak Hour**: Time of day with highest median power
- **Base Load**: 10th percentile of active power (system idle)
- **MRSD Chaos Index**: Day-to-day variability
- **Relative Mean Power**: Usage intensity by time-of-day (morning/daytime/evening/night)

### Reliability Metrics
- **Blackout Frequency**: Number of events
- **Mean Outage Duration**: Average blackout length (minutes)
- **Reliability Index**: % of time operational
- **Climatic Blackouts**: Events due to low sun (VPV < 15V)
- **Behavioral Blackouts**: Events despite sufficient sun
- **CBR/BBR**: Rates per 100 days

## Output Files

### Per-User
- `empirical_parameters_user_{ID}.json` — Full metrics in JSON
- `hourly_probabilities_user_{ID}.csv` — Hourly matrix (Hour | Appliance1 | Appliance2 | ...)

### Summary
- `empirical_parameters_summary.csv` — One row per user, all key metrics

## Adding New Datalogger Types

1. **Create new extractor class**:
   ```python
   from base_extractor import BaseExtractor
   
   class NewExtractor(BaseExtractor):
       def preprocess(self, filename):
           # Load and transform
       
       def extract_hardware(self, df):
           # Appliance wattages
       
       # ... implement other abstract methods
   ```

2. **Update detection logic** in `extract_empirical_baseline.py`:
   ```python
   def detect_datalogger_type(filename):
       # Add condition for new type
       if 'mynewlogger' in str(filename).lower():
           return 'mynewlogger'
   ```

3. **Update main function** to route to new extractor

## Data Assumptions

- **Timestamps**: Stored in `corrected_timestamp` column
- **Power**: Calculated as V × I
- **Interval**: 5 minutes (configurable in BaseExtractor)
- **Blackout threshold**: 7 minutes
- **Power threshold**: 0.5W (appliance "on")
- **Solar classification**: VPV < 15V during peak hours (10:00-15:00) = climatic failure

## Notes

- All extractors handle missing data gracefully
- Dataloggers of different sizes (months vs years) are supported
- Summary CSV automatically adapts to appliance count (OLD: 2 appliances, TPDIN: 3)
