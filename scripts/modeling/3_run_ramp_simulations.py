import numpy as np
import pandas as pd
import json
import argparse
from pathlib import Path
import sys
from datetime import datetime, timedelta

# RAMP imports
try:
    from ramp import UseCase, User, Appliance
except ImportError:
    print("Error: RAMP library not found. Install it with: pip install rampdemand")
    sys.exit(1)

# Define input and output directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
OUTPUT_DIR = SCRIPT_DIR / "output"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_parameters(user_id):
    """Load extracted parameters for a specific user"""
    param_file = OUTPUT_DIR / f"empirical_parameters_user_{user_id}.json"
    
    if not param_file.exists():
        print(f"Error: Parameter file not found: {param_file}")
        print(f"Please run script 1 first: python3 1_extract_parameters.py --user {user_id}")
        sys.exit(1)
    
    with open(param_file, 'r') as f:
        params = json.load(f)
    
    return params


def run_simulation(user_id, days=365, seed=42, appliance_numbers=None):
    """Run RAMP simulation for a specific user using empirical RAMP parameters
    
    Args:
        user_id: User ID to simulate
        days: Number of days to simulate
        seed: Random seed for reproducibility
        appliance_numbers: Dict with number of each appliance {'LED_1': 5, 'LED_2': 3, 'USB': 2}
    """
    print(f"\nLoading parameters for user {user_id}...")
    params = load_parameters(user_id)
    
    hardware = params['hardware'] # Power ratings (W)
    daily_event_probs = params['daily_event_probs']
    ramp_params = params.get('ramp_params', {})
    thermal_p_var = params.get('thermal_p_var', {})  # Power variability (for post-processing)
    
    print(f"Using RAMP parameters extracted from empirical data")
    print(f"  Thermal power variability (CV) by device (for post-processing):")
    print(f"    LED_1: {thermal_p_var.get('LED_1', 0.0):.2f}")
    print(f"    LED_2: {thermal_p_var.get('LED_2', 0.0):.2f}")
    print(f"    USB: {thermal_p_var.get('USB', 0.0):.2f}")
    
    # Default appliance numbers
    if appliance_numbers is None:
        appliance_numbers = {
            'LED_1': 1,
            'LED_2': 1,
            'USB': 1
        }
    
    appliances_config = {}
    
    # Create appliance configuration using RAMP parameters
    for appliance_name in ['LED_1', 'LED_2', 'USB']:
        power_key = f'{appliance_name.lower()}_W'
        power = hardware[power_key]
        
        appliances_config[appliance_name] = {
            'power': power,
            'daily_prob': daily_event_probs[f'{appliance_name}_Prob'],
            'number': appliance_numbers.get(appliance_name, 1),
            'thermal_p_var': thermal_p_var.get(appliance_name, 0.0),
        }
        
        # Add RAMP-specific parameters if available
        if appliance_name in ramp_params:
            ramp_p = ramp_params[appliance_name]
            num_windows = ramp_p.get('num_windows', 1)
            windows_list = []
            
            # Extract individual windows from RAMP naming
            for i in range(1, num_windows + 1):
                window_key = f'window_{i}'
                if window_key in ramp_p:
                    window = ramp_p[window_key]
                    windows_list.append([int(window[0]), int(window[1])])
            
            appliances_config[appliance_name].update({
                'num_windows': num_windows,
                'windows': windows_list if windows_list else [[0, 1440]],
                'func_time': int(round(ramp_p.get('func_time', 60))),
                'func_cycle': int(round(ramp_p.get('func_cycle', 5))),
                'time_fraction_random_variability': float(ramp_p.get('time_fraction_random_variability', 0.2)),
                'random_var_w': float(ramp_p.get('random_var_w', 0.35))
            })
        else:
            # Use defaults
            appliances_config[appliance_name].update({
                'num_windows': 1,
                'windows': [[0, 1440]],
                'func_time': 60,
                'func_cycle': 5,
                'time_fraction_random_variability': 0.2,
                'random_var_w': 0.35
            })
    
    np.random.seed(seed)
    
    print("\nCreating RAMP use case...")
    
    # Create RAMP use case
    use_case = UseCase()
    
    # Create a user/household
    user = User()
    
    # Create and configure appliances
    for appliance_name, config in appliances_config.items():
        appliance = Appliance(
            name=appliance_name,
            user=user,
            power=config['power'],
            number=config['number']
        )
        
        # Set RAMP parameters from empirical data
        appliance.occasional_use = config['daily_prob']
        appliance.func_time = config.get('func_time', 60)
        appliance.func_cycle = config.get('func_cycle', 5)
        appliance.num_windows = config.get('num_windows', 1)
        
        # Set individual windows
        for i, window in enumerate(config.get('windows', [[0, 1440]]), start=1):
            setattr(appliance, f'window_{i}', window)
        
        appliance.time_fraction_random_variability = config.get('time_fraction_random_variability', 0.2)
        appliance.random_var_w = config.get('random_var_w', 0.35)
        
        # Add appliance to user
        user.add_appliance(appliance)
        
        # Print appliance configuration
        print(f"\n  {appliance_name}:")
        print(f"    Power: {config['power']} W x {config['number']} units")
        print(f"    Occasional_use: {appliance.occasional_use:.2f}  [from time_period_probs]")
        print(f"    Functioning time: {appliance.func_time} min/day")
        print(f"    Functioning cycle: {appliance.func_cycle:.1f} min/cycle")
        print(f"    Windows: {config['num_windows']}")
        for i, w in enumerate(config['windows'][:config['num_windows']]):
            print(f"      Window {i+1}: {w[0]:.0f}-{w[1]:.0f} minutes ({w[0]/60:.1f}-{w[1]/60:.1f} hours)")
        print(f"    Time variability: {appliance.time_fraction_random_variability:.2f}")
        print(f"    Window timing variability: {config['random_var_w']:.2f}")
        print(f"    Power variability (CV): {config.get('thermal_p_var', 0.0):.2f}  [for post-processing]")
    
    # Add user to use case
    use_case.add_user(user)
    
    # Save appliance configuration to CSV
    config_df = pd.DataFrame([
        {
            'Appliance': name,
            'Power_W': config['power'],
            'Number': config['number'],
            'Occasional_Use': config['daily_prob'],
            'Func_Time_min': config.get('func_time', 60),
            'Func_Cycle_min': config.get('func_cycle', 5),
            'Num_Windows': config.get('num_windows', 1),
            'Windows': str(config.get('windows', [[0, 1440]])),
            'Time_Variability': config.get('time_fraction_random_variability', 0.2),
            'Window_Variability': config.get('random_var_w', 0.35),
            'Thermal_P_Var_PostProcess': config.get('thermal_p_var', 0.0)
        }
        for name, config in appliances_config.items()
    ])
    
    config_csv = OUTPUT_DIR / f"ramp_config_user_{user_id}.csv"
    config_df.to_csv(config_csv, index=False)
    print(f"✓ RAMP configuration saved to: {config_csv.name}")
    
    print(f"\nRunning RAMP simulation for {days} days...")
    
    # Run RAMP simulation
    try:
        use_case.initialize(num_days=days)
        load_profile = use_case.generate_daily_load_profiles(flat=True)
        
        # Create timestamped dataframe (RAMP generates 1-minute resolution)
        timestamps = []
        power_values = []
        start_date = datetime(2026, 5, 8)
        
        total_minutes = load_profile.shape[0]
        for minute_idx in range(total_minutes):
            timestamp = start_date + timedelta(minutes=minute_idx)
            timestamps.append(timestamp)
            power_values.append(load_profile[minute_idx])
        
        load_profile_df = pd.DataFrame({
            'DateTime': timestamps,
            'Total Load [W]': power_values
        })
        
        # Resample from 1-minute to 5-minute intervals (to match real data)
        load_profile_df.set_index('DateTime', inplace=True)
        load_profile_df = load_profile_df.resample('5T').mean()
        load_profile_df.reset_index(inplace=True)
        print(f"  Resampled from 1-minute to 5-minute intervals: {len(load_profile_df)} rows")
        
        # Save load profile
        output_csv = OUTPUT_DIR / f"simulated_profile_user_{user_id}.csv"
        load_profile_df.to_csv(output_csv, index=False)
        print(f"✓ Simulated load profile saved to: {output_csv.name}")
        
        # Print summary statistics
        if 'Total Load [W]' in load_profile_df.columns:
            total_load = load_profile_df['Total Load [W]']
            print(f"\nSimulation Summary (User {user_id}):")
            print(f"  Total energy: {total_load.sum() / 60 / 1000:.2f} kWh")
            print(f"  Peak power: {total_load.max():.2f} W")
            print(f"  Average power: {total_load.mean():.2f} W")
            print(f"  Number of data points: {len(load_profile_df)}")
        
        return output_csv
    
    except Exception as e:
        print(f"Error running RAMP simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run RAMP simulations using extracted parameters"
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
        "--led1",
        type=int,
        default=1,
        help="Number of LED_1 appliances (default: 1)"
    )
    parser.add_argument(
        "--led2",
        type=int,
        default=1,
        help="Number of LED_2 appliances (default: 1)"
    )
    parser.add_argument(
        "--usb",
        type=int,
        default=1,
        help="Number of USB appliances (default: 1)"
    )
    
    args = parser.parse_args()
    
    # Create appliance numbers dictionary
    appliance_numbers = {
        'LED_1': args.led1,
        'LED_2': args.led2,
        'USB': args.usb
    }
    
    run_simulation(args.user, days=args.days, seed=args.seed, 
                   appliance_numbers=appliance_numbers)