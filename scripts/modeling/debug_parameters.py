import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"

# Load parameters for user 74
param_file = OUTPUT_DIR / "empirical_parameters_user_74.json"

if param_file.exists():
    with open(param_file, 'r') as f:
        params = json.load(f)
    
    print("\n" + "="*70)
    print("EXTRACTED RAMP PARAMETERS - USER 74")
    print("="*70)
    
    print("\n📱 HARDWARE:")
    for key, val in params['hardware'].items():
        print(f"  {key}: {val} W")
    
    print("\n📊 DAILY EVENT PROBABILITIES:")
    for key, val in params['daily_event_probs'].items():
        print(f"  {key}: {val*100:.1f}%")
    
    print("\n🔄 RAMP PARAMETERS (Used by RAMP simulation):")
    for appliance, ramp_data in params['ramp_params'].items():
        print(f"\n  {appliance}:")
        print(f"    - num_windows: {ramp_data.get('num_windows', 'N/A')}")
        print(f"    - func_time (avg minutes/day): {ramp_data.get('func_time', 'N/A')}")
        print(f"    - func_cycle (min per cycle): {ramp_data.get('func_cycle', 'N/A')}")
        print(f"    - time_fraction_random_variability: {ramp_data.get('time_fraction_random_variability', 'N/A')}")
        print(f"    - random_var_w (window variability): {ramp_data.get('random_var_w', 'N/A')}")
        
        # Print windows
        for i in range(1, ramp_data.get('num_windows', 1) + 1):
            window_key = f'window_{i}'
            if window_key in ramp_data:
                window = ramp_data[window_key]
                start_h = window[0] / 60
                end_h = window[1] / 60
                print(f"    - window_{i}: {start_h:.1f}-{end_h:.1f} hours ({window[0]}-{window[1]} minutes)")
    
    print("\n" + "="*70)
    print("DIAGNOSIS:")
    print("="*70)
    
    # Check for issues
    issues = []
    
    for appliance, daily_prob in params['daily_event_probs'].items():
        if daily_prob < 0.3:
            issues.append(f"⚠️  {appliance} daily probability is {daily_prob*100:.1f}% (very low - appliance rarely turns on)")
    
    for appliance, ramp_data in params['ramp_params'].items():
        func_time = ramp_data.get('func_time', 0)
        if func_time < 20:
            issues.append(f"⚠️  {appliance} func_time is {func_time} min (very short usage periods)")
        
        num_windows = ramp_data.get('num_windows', 1)
        if num_windows > 3:
            issues.append(f"⚠️  {appliance} has {num_windows} windows (fragmented usage)")
    
    if issues:
        print("\nPotential issues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✓ Parameters look reasonable")
    
    print("\n" + "="*70 + "\n")
else:
    print(f"Error: Parameter file not found: {param_file}")
    print("Run script 1 first: python3 1_extract_parameters.py --user 74")
