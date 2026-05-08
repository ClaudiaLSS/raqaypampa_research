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


def get_hourly_profile(hourly_probs, appliance_name):
    """Convert hourly probabilities to a daily profile for RAMP"""
    # Extract probabilities for the appliance across all hours
    profile = []
    for hour in range(24):
        key = f'hour_{hour:02d}'
        prob = hourly_probs[key][f'{appliance_name}_Prob']
        profile.append(prob)
    return profile


def run_simulation(user_id, days=365, seed=42, appliance_numbers=None):
    """Run RAMP simulation for a specific user
    
    Args:
        user_id: User ID to simulate
        days: Number of days to simulate
        seed: Random seed for reproducibility
        appliance_numbers: Dict with number of each appliance {'LED_1': 5, 'LED_2': 3, 'USB': 2}
    """
    print(f"\nLoading parameters for user {user_id}...")
    params = load_parameters(user_id)
    
    hardware = params['hardware']
    daily_event_probs = params['daily_event_probs']
    peak_hours = params['peak_hours']
    ramp_params = params.get('ramp_params', {})  # Get RAMP-specific parameters
    
    # Default appliance numbers (can be overridden)
    if appliance_numbers is None:
        appliance_numbers = {
            'LED_1': 1,
            'LED_2': 1,
            'USB': 1
        }
    
    np.random.seed(seed)
    
    print("Creating RAMP use case...")
    
    # Create RAMP use case
    use_case = UseCase()
    
    # Create a user/household
    user = User()
    
    # Define appliances with all RAMP parameters
    appliances_config = {
        'LED_1': {
            'power': hardware['led_1_W'],
            'daily_prob': daily_event_probs['LED_1_Prob'],
            'number': appliance_numbers.get('LED_1', 1),
        },
        'LED_2': {
            'power': hardware['led_2_W'],
            'daily_prob': daily_event_probs['LED_2_Prob'],
            'number': appliance_numbers.get('LED_2', 1),
        },
        'USB': {
            'power': hardware['usb_W'],
            'daily_prob': daily_event_probs['USB_Prob'],
            'number': appliance_numbers.get('USB', 1),
        }
    }
    
    # Add RAMP-specific parameters if available
    for appliance_name in appliances_config:
        if appliance_name in ramp_params:
            ramp_p = ramp_params[appliance_name]
            num_windows = ramp_p.get('num_windows', 1)
            windows_list = []
            
            # Extract individual windows from RAMP naming (window_1, window_2, etc.)
            for i in range(1, num_windows + 1):
                window_key = f'window_{i}'
                if window_key in ramp_p:
                    # Convert to integers - RAMP expects integer minutes
                    window = ramp_p[window_key]
                    windows_list.append([int(window[0]), int(window[1])])
            
            appliances_config[appliance_name].update({
                'num_windows': num_windows,
                'windows': windows_list if windows_list else [[0, 1440]],
                'func_time': int(round(ramp_p.get('func_time', 60))),  # Convert to int
                'func_cycle': int(round(ramp_p.get('func_cycle', 5))),  # Convert to int
                'time_fraction_random_variability': float(ramp_p.get('time_fraction_random_variability', 0.2)),
                'random_var_w': float(ramp_p.get('random_var_w', 0.35))
            })
        else:
            # Use defaults if not in extracted parameters
            appliances_config[appliance_name].update({
                'num_windows': 1,
                'windows': [[0, 1440]],
                'func_time': 60,
                'func_cycle': 5,
                'time_fraction_random_variability': 0.2,
                'random_var_w': 0.35
            })
    
    # Create and configure appliances
    for appliance_name, config in appliances_config.items():
        appliance = Appliance(
            name=appliance_name,
            user=user,
            power=config['power'],
            number=config['number']
        )
        
        # RAMP will generate profiles automatically based on Appliance configuration
        # The parameters are stored in the appliance object for reference
        # Note: func_time in RAMP is the duration of a single usage cycle, not total daily time
        # We reduce it to ~5-10 minutes per cycle to fit within windows
        appliance.daily_prob = config['daily_prob']
        
        # Set func_time and func_cycle FIRST
        appliance.func_time = config['func_time']
        appliance.func_cycle = config['func_cycle']
        
        # Set num_windows
        appliance.num_windows = config['num_windows']
        
        # Set individual windows as window_1, window_2, etc. (RAMP format)
        for i, window in enumerate(config['windows'], start=1):
            setattr(appliance, f'window_{i}', window)
        
        # Cap time_fraction_random_variability to prevent RAMP errors
        # Since func_cycle is now based on 5th percentile (very robust),
        # we can allow moderate variability up to 0.30
        time_variability = min(config['time_fraction_random_variability'], 0.30)
        appliance.time_fraction_random_variability = time_variability
        
        appliance.random_var_w = config['random_var_w']
        
        # Explicitly add appliance to user (important!)
        user.add_appliance(appliance)
        
        # Print appliance configuration
        print(f"\n  {appliance_name}:")
        print(f"    Power: {config['power']} W x {config['number']} units")
        print(f"    Daily probability: {config['daily_prob']}")
        print(f"    Functioning time: {appliance.func_time} min/day (total, distributed across windows)")
        print(f"    Functioning cycle: {appliance.func_cycle:.1f} min/cycle (5th percentile from data)")
        print(f"    Windows: {config['num_windows']}")
        for i, w in enumerate(config['windows'][:config['num_windows']]):
            print(f"      Window {i+1}: {w[0]:.0f}-{w[1]:.0f} minutes ({w[0]/60:.1f}-{w[1]/60:.1f} hours)")
        print(f"    Time variability: {appliance.time_fraction_random_variability:.2f} (capped from {config['time_fraction_random_variability']:.2f})")
        print(f"    Window variability: {config['random_var_w']}")
    
    # Add user to use case
    use_case.add_user(user)
    
    print(f"\nRunning RAMP simulation for {days} days...")
    
    # Run RAMP simulation
    try:
        # Initialize the use case with number of days
        use_case.initialize(num_days=days)
        
        # Generate load profiles
        use_case.generate_daily_load_profiles()
        
        # Extract and save RAMP configuration (for tracking)
        config_df = use_case.export_to_dataframe()
        config_csv = OUTPUT_DIR / f"ramp_config_user_{user_id}.csv"
        config_df.to_csv(config_csv, index=False)
        print(f"✓ RAMP configuration saved to: {config_csv.name}")
        
        # Extract load profile from user object
        # The load profile is stored as an array (1D or 2D depending on RAMP version)
        load_profile = user.load
        
        # Create DataFrame with timestamps and power values
        timestamps = []
        power_values = []
        start_date = datetime(2026, 5, 8)
        
        # Handle 1D array (flattened across all days and minutes)
        if len(load_profile.shape) == 1:
            # 1D array: total_minutes = days * 1440
            total_minutes = load_profile.shape[0]
            for minute_idx in range(total_minutes):
                timestamp = start_date + timedelta(minutes=minute_idx)
                timestamps.append(timestamp)
                power_values.append(load_profile[minute_idx])
        else:
            # 2D array: [day, minute]
            for day_idx in range(load_profile.shape[0]):
                for minute_idx in range(load_profile.shape[1]):
                    timestamp = start_date + timedelta(days=day_idx, minutes=minute_idx)
                    timestamps.append(timestamp)
                    power_values.append(load_profile[day_idx, minute_idx])
        
        # Create DataFrame
        load_profile_df = pd.DataFrame({
            'DateTime': timestamps,
            'Total Load [W]': power_values
        })
        
        # Extract and save results
        print(f"\n✓ Simulation complete for user {user_id}")
        
        # Save load profile
        output_csv = OUTPUT_DIR / f"simulated_profile_user_{user_id}.csv"
        load_profile_df.to_csv(output_csv, index=False)
        print(f"✓ Simulated load profile saved to: {output_csv.name}")
        
        # Print summary statistics
        if 'Total Load [W]' in load_profile_df.columns:
            total_load = load_profile_df['Total Load [W]']
            print(f"\nSimulation Summary (User {user_id}):")
            print(f"  Total energy: {total_load.sum() / 60:.2f} kWh")  # Convert Wmin to Wh to kWh
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
    
    run_simulation(args.user, days=args.days, seed=args.seed, appliance_numbers=appliance_numbers)