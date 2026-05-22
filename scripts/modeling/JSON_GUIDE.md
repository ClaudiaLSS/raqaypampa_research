# Simplified JSON Guide for Manual Parameters

## The JSON You Need to Modify

Use this minimal JSON structure. It has only the essential fields:

```json
{
  "LED_1": {
    "power_W": 2.56,              ← Device power in watts (rarely change)
    "periods": {
      "morning_prep": {
        "occasional_use": 0.39,   ← Probability: 0.39 = 39% of days (MODIFY THIS)
        "avg_minutes": 35.4,      ← Average daily usage in minutes (MODIFY THIS)
        "std_minutes": 63.2,      ← Standard deviation, variability (MODIFY THIS)
        "rand_var": 0.30          ← Duration variation: 0-0.30 (MODIFY THIS)
      },
      ...more periods...
    }
  },
  "LED_2": { ... },
  "USB": { ... }
}
```

## What Each Field Does

### Fields You Will Modify:

| Field | Range | What to Change | Example |
|-------|-------|----------------|---------|
| `occasional_use` | 0 to 1 | Probability device is used that day | 0.99 = used 99% of days |
| `avg_minutes` | 0-1440 | Average daily usage in minutes | 105.6 = ~1.75 hours/day |
| `std_minutes` | 0+ | How much duration varies | 61.7 = ±62 min variation |
| `rand_var` | 0-0.30 | Randomness in daily duration | 0.30 = ±30% variation |

### Fields You Can Ignore:

| Field | Why Keep It | When Change |
|-------|------------|-------------|
| `power_W` | Device's actual power draw in watts | Only if device specs change |

## Common Modifications

### 1. Make Device Used More Often
```json
"evening_school_cooking": {
  "occasional_use": 1.0,    ← Change from 0.99 to 1.0 (always used)
  "avg_minutes": 105.6,
  "std_minutes": 61.7,
  "rand_var": 0.30
}
```

### 2. Increase Average Usage Time
```json
"daytime": {
  "occasional_use": 0.10,
  "avg_minutes": 100.0,     ← Change from 5.8 to 100.0
  "std_minutes": 25.8,
  "rand_var": 0.30
}
```

### 3. Reduce Variability (More Consistent)
```json
"morning_prep": {
  "occasional_use": 0.39,
  "avg_minutes": 35.4,
  "std_minutes": 20.0,      ← Change from 63.2 to 20.0 (more consistent)
  "rand_var": 0.15          ← Change from 0.30 to 0.15 (less random)
}
```

### 4. Increase Variability (More Realistic)
```json
"night_security": {
  "occasional_use": 0.13,
  "avg_minutes": 3.0,
  "std_minutes": 50.0,      ← Change from 19.1 to 50.0 (more variable)
  "rand_var": 0.30
}
```

## Optional Advanced Fields

If you want to customize **when** the device can be used:

```json
"evening_school_cooking": {
  "occasional_use": 0.99,
  "avg_minutes": 105.6,
  "std_minutes": 61.7,
  "rand_var": 0.30,
  "windows": [[1020, 1440]],     ← OPTIONAL: Time window (5 PM - midnight)
  "window_var": 0.35             ← OPTIONAL: Start time variability
}
```

**Don't add these unless you want to customize time windows!**

## 3 Time Periods (Hardcoded Defaults)

If you DON'T specify `windows`, these defaults are used:

| Period | Default Window | Hours |
|--------|---|-------|
| `morning_prep` | [[240, 600]] | 4:00 AM - 10:00 AM |
| `daytime` | [[600, 1020]] | 10:00 AM - 5:00 PM |
| `evening_school_cooking` | [[1020, 1440]] | 5:00 PM - 12:00 AM |
| `night_security` | [[0, 240]] | 12:00 AM - 4:00 AM |

## Files You Can Use

### Minimal JSON (Recommended for Most Users)
```bash
minimal_params.json
# Only 5 fields per period, easy to understand
```

### Full JSON (Advanced Users)
```bash
manual_params_example.json
# Includes optional windows and window_var fields
```

### How to Use

1. **Copy minimal_params.json:**
```bash
cp scripts/modeling/manual_parameters/minimal_params.json my_custom_params.json
```

2. **Edit my_custom_params.json** with your values

3. **Run simulation:**
```bash
python 4_manual_parameters_simulation.py --user 74 --days 5 --config my_custom_params.json
```

## Quick Cheat Sheet

**Change how often device is used:**
```json
"occasional_use": 0.99    // More often
"occasional_use": 0.50    // Less often
```

**Change how long it runs:**
```json
"avg_minutes": 200        // Longer
"avg_minutes": 50         // Shorter
```

**Change consistency:**
```json
"std_minutes": 10         // Very consistent
"std_minutes": 100        // Very variable
"rand_var": 0.10          // Consistent duration
"rand_var": 0.30          // Variable duration
```

---

**Start with minimal_params.json and modify only these 4 fields per period!**
