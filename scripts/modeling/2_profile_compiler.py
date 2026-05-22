import pandas as pd
import json
from pathlib import Path
import sys

# Define structural paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
OUTPUT_DIR = SCRIPT_DIR / "output"

def calculate_user_profile_deterministic(metrics_row):
    """
    Step 1: Deterministic Classification 
    Sorts households using strict mathematical thresholds derived from qualitative triangulation.
    """
    base_load = metrics_row['Real_Base_Load_Watts']
    mrsd = metrics_row['Real_MRSD_Chaos']
    peak_hour = metrics_row['Real_Modal_Peak_Hour']
    
    # Triangulated Threshold: Continuous overnight lighting indicates Profile 2
    if base_load >= 1.0:
        return "EBP_2_Isolated_Elderly"
    
    # Triangulated Threshold: High structural chaos indicates Profile 4
    elif mrsd >= 0.70:
        return "EBP_4_System_Breakers"
        
    # Triangulated Threshold: Early morning synchronization indicates Profile 1
    elif 4 <= peak_hour <= 6:
        return "EBP_1_Agricultural_Core"
        
    # Default fallback based on high-density family structures
    else:
        return "EBP_3_Extended_Hub"

def transform_parameters_to_ramp(user_id, profile_type, empirical_data):
    """
    Step 2: Algorithmic Appliance Splitting & Parameter Transformation
    Maps fuzzy social rules to crisp RAMP parameters using empirical data as the baseline magnitude.
    """
    hardware = empirical_data['hardware']
    thermal_var = empirical_data['thermal_p_var']
    period_usage = empirical_data['appliance_period_usage']
    
    compiled_appliances = []
    
    # =========================================================================
    # EBP 1: THE AGRICULTURAL CORE
    # =========================================================================
    if profile_type == "EBP_1_Agricultural_Core":
        
        # Virtual Appliance 1: Morning Livelihood Routine
        morning_time = period_usage['LED_1']['morning_block']['avg_minutes']
        if morning_time > 0:
            compiled_appliances.append({
                "name": "LED_1_Morning_AgriPrep",
                "power": hardware['led_1_W'],
                "power_fraction_variability": thermal_var['LED_1'],
                "num_windows": 1,
                "window_1": [240, 360],  # Rigid constraint: 04:00 - 06:00
                "func_time": morning_time,  # Objective magnitude from data
                "func_cycle": 15,
                "random_var_w": 0.05,    # High socio-temporal rigidity
                "time_fraction_random_variability": 0.15
            })
            
        # Virtual Appliance 2: Evening Domestic Routine
        evening_time = period_usage['LED_1']['evening_block']['avg_minutes']
        if evening_time > 0:
            compiled_appliances.append({
                "name": "LED_1_Evening_Domestic",
                "power": hardware['led_1_W'],
                "power_fraction_variability": thermal_var['LED_1'],
                "num_windows": 1,
                "window_1": [1080, 1320], # Cultural boundary: 18:00 - 22:00
                "func_time": evening_time,
                "func_cycle": 30,
                "random_var_w": 0.10,
                "time_fraction_random_variability": 0.20
            })

    # =========================================================================
    # EBP 2: THE ISOLATED ELDERLY
    # =========================================================================
    elif profile_type == "EBP_2_Isolated_Elderly":
        # Force a rigid, continuous overnight lighting draw
        compiled_appliances.append({
            "name": "LED_2_Night_Safety_Baseline",
            "power": max(hardware['led_2_W'], 1.5), 
            "power_fraction_variability": 0.02,     
            "num_windows": 1,
            "window_1": [0, 240],    # Bounded exclusively to the overnight block
            "func_time": 240.0,      # Continuous baseline
            "func_cycle": 240,       
            "random_var_w": 0.0,     # Absolute socio-temporal rigidity
            "time_fraction_random_variability": 0.0
        })
        
        # Daytime Companionship (Fuzzy Rule -> Handled by Data)
        day_time = period_usage['USB']['daytime_block']['avg_minutes']
        if day_time > 0:
            compiled_appliances.append({
                "name": "USB_Daytime_Companionship_Radio",
                "power": hardware['usb_W'],
                "power_fraction_variability": thermal_var['USB'],
                "num_windows": 1,
                "window_1": [540, 1020], # Broad daytime window: 09:00 - 17:00
                "func_time": day_time,
                "func_cycle": 60,        
                "random_var_w": 0.30,    # High elasticity (highly shiftable)
                "time_fraction_random_variability": 0.25
            })

    # =========================================================================
    # EBP 3: THE EXTENDED HUB
    # =========================================================================
    elif profile_type == "EBP_3_Extended_Hub":
        # Chaotic phone charging throughout the entire waking day
        day_time = period_usage['USB']['daytime_block']['avg_minutes'] + period_usage['USB']['evening_block']['avg_minutes']
        compiled_appliances.append({
            "name": "USB_Chaotic_Communal_Charging",
            "power": hardware['usb_W'],
            "power_fraction_variability": thermal_var['USB'],
            "num_windows": 1,
            "window_1": [360, 1320], # Maximize window: 06:00 - 22:00
            "func_time": min(day_time, 480.0), 
            "func_cycle": 15,
            "random_var_w": 0.40,    # Maximum window elasticity
            "time_fraction_random_variability": 0.45 
        })
        
        # Extended cooking window
        evening_time = period_usage['LED_1']['evening_block']['avg_minutes']
        compiled_appliances.append({
            "name": "LED_1_Extended_Evening_Cooking",
            "power": hardware['led_1_W'],
            "power_fraction_variability": thermal_var['LED_1'],
            "num_windows": 1,
            "window_1": [1020, 1380], # Broadened cooking window: 17:00 - 23:00
            "func_time": max(evening_time, 180.0), 
            "func_cycle": 45,
            "random_var_w": 0.15,
            "time_fraction_random_variability": 0.20
        })

    # =========================================================================
    # EBP 4: THE SYSTEM BREAKERS
    # =========================================================================
    elif profile_type == "EBP_4_System_Breakers":
        # Wildly unpredictable spikes across the entire cycle
        total_time = period_usage['LED_1']['evening_block']['avg_minutes'] + period_usage['USB']['daytime_block']['avg_minutes']
        compiled_appliances.append({
            "name": "System_Breaker_Unpredictable_Load",
            "power": hardware['led_1_W'] * 1.5, # Simulates parallel battery hacks
            "power_fraction_variability": 0.35,
            "num_windows": 1,
            "window_1": [0, 1440],   # Permitted at any minute of the day
            "func_time": max(total_time, 60.0),
            "func_cycle": 10,
            "random_var_w": 0.50,    # Pure stochastic freedom
            "time_fraction_random_variability": 0.80 
        })

    return compiled_appliances

def main():
    metrics_file = PROJECT_ROOT / "results" / "timeseries" / "metrics" / "validation_metrics_dual_tier.csv"
    if not metrics_file.exists():
        print("[-] Error: Run Script 3 first to generate the dual-tier validation metrics file.")
        sys.exit(1)
        
    df_metrics = pd.read_csv(metrics_file)
    
    for _, row in df_metrics.iterrows():
        user_id = str(int(row['User_ID']))
        
        # Step 1: Objective Classification
        assigned_profile = calculate_user_profile_deterministic(row)
        
        # Step 2: Load Raw Empirical Parameters from Script 1
        json_input_path = OUTPUT_DIR / f"empirical_parameters_user_{user_id}.json"
        if not json_input_path.exists():
            print(f"[-] Warning: Missing raw JSON for user {user_id}. Skipping.")
            continue
            
        with open(json_input_path, 'r') as f:
            empirical_params = json.load(f)
            
        # Step 3: Algorithmic Transformation (Virtual Appliances)
        ramp_appliances = transform_parameters_to_ramp(user_id, assigned_profile, empirical_params)
        
        # Step 4: Package into standard RAMP Configuration
        ramp_config = {
            "user_id": user_id,
            "socio_technical_profile": assigned_profile,
            "appliances": ramp_appliances
        }
        
        output_json_path = OUTPUT_DIR / f"ramp_input_config_user_{user_id}.json"
        with open(output_json_path, 'w') as f:
            json.dump(ramp_config, f, indent=4)
            
        print(f"[+] User {user_id} classified as {assigned_profile} -> Virtual Appliances Compiled.")

if __name__ == "__main__":
    main()