"""
RAMP Simulation Execution Engine

Ingests the compiled *_ramp_input_user_{user_id}.json files from Script 2 
and executes the stochastic RAMP demand model.
"""
import numpy as np
import pandas as pd
import json
import argparse
from pathlib import Path
import sys
from datetime import datetime, timedelta

# RAMP imports
try:
    import ramp
    from ramp import UseCase, User, Appliance
    print(f"\n[INFO] Running RAMP from: {ramp.__file__}")
except ImportError:
    print("Error: RAMP library not found. Install it with: pip install rampdemand")
    sys.exit(1)

# Define input and output directories
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_profile_json(user_id):
    """Find the compiled RAMP JSON file for a specific user."""
    # Search for files matching the output format of Script 2
    pattern = f"*_ramp_input_user_{user_id}.json"
    files = list(OUTPUT_DIR.glob(pattern))
    
    if not files:
        print(f"[-] Error: Compiled RAMP configuration not found for User {user_id}")
        print(f"    Looked for: {OUTPUT_DIR}/{pattern}")
        print(f"    Please run '2_profile_compiler.py --user {user_id}' first.")
        sys.exit(1)
    
    # If multiple exist (e.g., re-runs with different profiles), grab the most recently modified
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files[0]


def run_simulation(user_id, days=365, seed=42, num_households=1):
    """Run RAMP simulation using dynamically compiled empirical parameters."""
    
    # 1. Locate and load the JSON
    profile_file = find_profile_json(user_id)
    print(f"\n[*] Loading configuration from: {profile_file.name}")
    
    with open(profile_file, 'r') as f:
        scenario_data = json.load(f)
        
    profile_type = scenario_data.get('socio_technical_profile', 'Unknown_Profile')
    datalogger_type = scenario_data.get('datalogger_type', 'unknown')
    appliances_config = scenario_data.get('appliances', [])
    
    print(f"[+] Loaded socio-technical profile: {profile_type.upper()}")
    print(f"[+] Datalogger Type: {datalogger_type.upper()}")
    print(f"[+] Simulating {len(appliances_config)} Virtual Appliances.")
    
    np.random.seed(seed)
    
    print("\n[*] Creating RAMP use case...")
    use_case = UseCase()
    
    # Create the user/household representation
    # Name the user object after their assigned sociological profile
    user = User(
        user_name=f"U{user_id}_{profile_type}",
        num_users=num_households  
    )
    
    # Map the JSON Virtual Appliances directly to RAMP Appliance objects
    for config in appliances_config:
        
        # 1. Prepare CORE parameters ONLY for the __init__ constructor
        app_kwargs = {
            'user': user,
            'name': config.get('name', 'Unnamed_Appliance'),
            'power': float(config.get('power', 0.0)),
            'number': 1,
            'func_time': int(round(config.get('func_time', 60))),
            'func_cycle': int(round(config.get('func_cycle', 60)))
        }
        
        if 'flat' in config:
            app_kwargs['flat'] = config['flat']
            
        # 2. Create the Appliance
        appliance = Appliance(**app_kwargs)
        
        # 3. Attach standard RAMP attributes AFTER creation
        appliance.num_windows = int(config.get('num_windows', 1))
        appliance.occasional_use = float(config.get('occasional_use', 1.0))
        appliance.time_fraction_random_variability = float(config.get('time_fraction_random_variability', 0.0))
        appliance.random_var_w = float(config.get('random_var_w', 0.0))
        
        # 4. Inject custom time windows dynamically (ensuring they are integers)
        for i in range(1, appliance.num_windows + 1):
            window_key = f'window_{i}'
            if window_key in config:
                # Converts the JSON array [1080.0, 1380.0] into integers [1080, 1380]
                window_list = [int(val) for val in config[window_key]]
                setattr(appliance, window_key, window_list)
                
        # 5. Add the fully configured appliance to the user
        user.add_appliance(appliance)
        
        # Print summary for the console
        flat_status = f", flat={app_kwargs['flat']}" if 'flat' in app_kwargs else ""
        print(f"  -> Added: {app_kwargs['name']} ({app_kwargs['power']}W, {appliance.func_time} mins/day, prob={appliance.occasional_use:.2f}{flat_status})")
        
    use_case.add_user(user)
    
    print(f"\n[*] Running RAMP stochastic simulation for {days} days...")
    
    try:
        use_case.initialize(num_days=days)
        load_profile = use_case.generate_daily_load_profiles(flat=True)
        
        # Create timestamped dataframe (RAMP generates 1-minute resolution)
        timestamps = []
        power_values = []
        start_date = datetime(2026, 1, 1)  # Starting point for the simulation data
        
        total_minutes = load_profile.shape[0]
        for minute_idx in range(total_minutes):
            timestamp = start_date + timedelta(minutes=minute_idx)
            timestamps.append(timestamp)
            power_values.append(load_profile[minute_idx])
        
        load_profile_df = pd.DataFrame({
            'DateTime': timestamps,
            'Total Load [W]': power_values
        })
        
        # Resample from 1-minute to 5-minute intervals
        load_profile_df.set_index('DateTime', inplace=True)
        load_profile_df = load_profile_df.resample('5T').mean()
        load_profile_df.reset_index(inplace=True)
        
        print(f"[+] Resampled from 1-minute to 5-minute intervals: {len(load_profile_df)} rows")
        
        # Save load profile cleanly indicating the user and the profile
        output_csv = OUTPUT_DIR / f"simulated_profile_user_{user_id}_{profile_type}.csv"
        load_profile_df.to_csv(output_csv, index=False)
        print(f"[+] Simulated load profile saved to: {output_csv.name}")
        
        # Print summary statistics
        if 'Total Load [W]' in load_profile_df.columns:
            total_load = load_profile_df['Total Load [W]']
            print(f"\n{'='*50}")
            print(f"--- Simulation Summary (User {user_id} | {profile_type}) ---")
            print(f"{'='*50}")
            print(f"  Total energy demand: {total_load.sum() / (60/5) / 1000:.2f} kWh") # adjusted for 5-min intervals
            print(f"  Absolute Peak power: {total_load.max():.2f} W")
            print(f"  Average base power:  {total_load.mean():.2f} W")
            print(f"{'='*50}\n")
        
        return output_csv
    
    except Exception as e:
        print(f"[-] Error running RAMP simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run RAMP simulations using empirically compiled JSON profiles"
    )
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="User ID to simulate (e.g., '74')"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="Number of days to simulate (default: 365)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--households",
        type=int,
        default=1,
        help="Number of identical households to aggregate in this simulation (default: 1)"
    )
    
    args = parser.parse_args()
    
    run_simulation(
        user_id=args.user, 
        days=args.days, 
        seed=args.seed,
        num_households=args.households
    )