import pandas as pd
import json
from pathlib import Path
import sys

# Define structural paths
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Path for your direct input file
SCENARIOS_FILE = SCRIPT_DIR / "scenarios.csv"

def get_virtual_appliances(profile_type):
    """
    Maps the explicitly requested Energy Behavior Profile to its predefined 
    Virtual Appliances (from virtual_appliances.md).
    """
    compiled_appliances = []

    # =========================================================================
    # EBP 1: THE EDUCATIONAL / AGRICULTURAL CORE
    # =========================================================================
    if profile_type == "EBP_1_Agricultural_Core":
        compiled_appliances.extend([
            {
                "name": "Indoor_Task_Light_LED2",
                "power": 3.0,
                "occasional_use": 1.0,
                "num_windows": 1,
                "window_1": [1080, 1290],
                "func_time": 100.0,
                "func_cycle": 60.0,
                "time_fraction_random_variability": 0.2,
                "random_var_w": 0.3
            },
            {
                "name": "Outdoor_Night_Transit_Light",
                "power": 2.0,
                "occasional_use": 1.0,
                "num_windows": 1,
                "window_1": [1080, 1260],
                "func_time": 80.0,
                "func_cycle": 50.0,
                "time_fraction_random_variability": 0.3,
                "random_var_w": 0.35
            },
            {
                "name": "Indoor_Safety_Light_night",
                "power": 3.0,
                "occasional_use": 0.25,
                "num_windows": 2,
                "window_1": [1260, 1440], 
                "window_2": [0, 420], 
                "func_time": 480.0,               
                "func_cycle": 140.0,              
                "time_fraction_random_variability": 0.1,
                "random_var_w": 0.1
        
            },
            {
                "name": "Indoor_Morning_Light",
                "power": 3.0,
                "occasional_use": 0.30,
                "num_windows": 1,
                "window_1": [400, 480],
                "func_time": 50.0,
                "func_cycle": 30.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Indoor_occasional_daytime_Light",
                "power": 3.0,
                "occasional_use": 0.15,
                "num_windows": 1,
                "window_1": [420, 1080],
                "func_time": 20.0,
                "func_cycle": 5.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Outdoor_Morning_Light",
                "power": 2.0,
                "occasional_use": 0.30,
                "num_windows": 1,
                "window_1": [300, 420],
                "func_time": 50.0,
                "func_cycle": 30.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Cellphone_Charging_USB",
                "power": 2.0,
                "occasional_use": 1.0,
                "num_windows": 1,
                "window_1": [0, 1440],
                "func_time": 470.0,
                "func_cycle": 180.0,
                "time_fraction_random_variability": 0.35,
                "random_var_w": 0.0
            }
        ])

    # =========================================================================
    # EBP 2: THE ISOLATED ELDERLY
    # =========================================================================
    elif profile_type == "EBP_2_Isolated_Elderly":
        compiled_appliances.extend([
            {
                "name": "Indoor_Task_Light_LED2",
                "power": 3.0,
                "occasional_use": 0.26,
                "num_windows": 2,
                "window_1": [1140, 1440],
                "window_2": [0, 60],
                "func_time": 100.0,
                "func_cycle": 60.0,
                "time_fraction_random_variability": 0.35,
                "random_var_w": 0.20
            },
            {
                "name": "Indoor_Safety_Light_LED1",
                "power": 3.0,
                "occasional_use": 0.70,
                "num_windows": 1,
                "window_1": [0, 300],
                "func_time": 300.0,
                "func_cycle": 240.0,
                "time_fraction_random_variability": 0.35,
                "random_var_w": 0.20
            },
            {
                "name": "Outdoor_Night_Transit_Light",
                "power": 2.0,
                "occasional_use": 0.10,
                "num_windows": 1,
                "window_1": [1200, 1320],
                "func_time": 50.0,
                "func_cycle": 10.0,
                "time_fraction_random_variability": 0.35,
                "random_var_w": 0.20
            },
            {
                "name": "Cellphone_Radio_Charging_USB",
                "power": 3.0,
                "occasional_use": 1.0,
                "num_windows": 1,
                "window_1": [0, 1440],
                "func_time": 550.0,
                "func_cycle": 85.0,
                "time_fraction_random_variability": 0.40,
                "random_var_w": 0.0
            }
        ])

    # =========================================================================
    # EBP 3: THE EXTENDED / MULTI-TASKING HUB
    # =========================================================================
    elif profile_type == "EBP_3_Extended_Hub":
        compiled_appliances.extend([
            {
                "name": "Indoor_Task_Communal_Light",
                "power": 3.0,
                "occasional_use": 1.0,
                "num_windows": 1,
                "window_1": [1020, 1440],
                "func_time": 240.0,
                "func_cycle": 180.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Indoor_Safety_Light",
                "power": 3.0,
                "occasional_use": 0.85,
                "num_windows": 1,
                "window_1": [0, 420],
                "func_time": 420.0,
                "func_cycle": 300.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Outdoor_Social_Transit_Light",
                "power": 2.0,
                "occasional_use": 0.60,
                "num_windows": 1,
                "window_1": [1080, 1260],
                "func_time": 45.0,
                "func_cycle": 20.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Stacked_Phone_Charging_USB",
                "power": 5.0,
                "occasional_use": 1.0,
                "num_windows": 1,
                "window_1": [0, 1440],
                "func_time": 900.0,
                "func_cycle": 300.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.0
            }
        ])

    # =========================================================================
    # EBP 4: THE SYSTEM BREAKERS
    # =========================================================================
    elif profile_type == "EBP_4_System_Breakers":
        compiled_appliances.extend([
            {
                "name": "Erratic_Indoor_Evening_Task_Light_LED2",
                "power": 3.0,
                "occasional_use": 0.90,
                "num_windows": 1,
                "window_1": [1080, 1380],
                "func_time": 100.0,
                "func_cycle": 70.0,
                "time_fraction_random_variability": 0.35,
                "random_var_w": 0.30
            },
            {
                "name": "Indoor_Morning_Light",
                "power": 3.0,
                "occasional_use": 0.30,
                "num_windows": 1,
                "window_1": [300, 420],
                "func_time": 60.0,
                "func_cycle": 40.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Indoor_Safety_Light_LED1",
                "power": 2.0,
                "occasional_use": 0.35,
                "num_windows": 2,
                "window_1": [0, 419],
                "window_2": [1381, 1440],
                "func_time": 350.0,
                "func_cycle": 240.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Outdoor_Transit_Light",
                "power": 2.0,
                "occasional_use": 0.10,
                "num_windows": 1,
                "window_1": [1080, 1320],
                "func_time": 60.0,
                "func_cycle": 75.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            },
            {
                "name": "Burst_Phone_Radio_Charging_USB",
                "power": 3.0,
                "occasional_use": 0.44,
                "num_windows": 1,
                "window_1": [0, 1440],
                "func_time": 300.0,
                "func_cycle": 180.0,
                "time_fraction_random_variability": 0.20,
                "random_var_w": 0.35
            }
        ])
    else:
        print(f"[-] Unknown profile: {profile_type}")

    return compiled_appliances


def create_template_csv():
    """Generates a default scenarios.csv file if it does not exist."""
    print(f"[*] {SCENARIOS_FILE.name} not found. Generating a template...")
    template_data = {
        "Scenario_ID": ["Sim_Standard_Farmer", "Sim_Isolated_Elder", "Sim_Busy_Hub", "Sim_Nomad"],
        "Target_Profile": ["EBP_1_Agricultural_Core", "EBP_2_Isolated_Elderly", "EBP_3_Extended_Hub", "EBP_4_System_Breakers"]
    }
    pd.DataFrame(template_data).to_csv(SCENARIOS_FILE, index=False)
    print(f"[+] Template created at {SCENARIOS_FILE}. You can edit this file to run different scenarios.")


def main():
    # If the scenarios file doesn't exist, create it automatically
    if not SCENARIOS_FILE.exists():
        create_template_csv()
    
    # Read the direct configuration file
    df_scenarios = pd.read_csv(SCENARIOS_FILE)
    
    # Process each explicitly requested scenario
    for _, row in df_scenarios.iterrows():
        scenario_id = str(row['Scenario_ID']).strip()
        target_profile = str(row['Target_Profile']).strip()
        
        # Pull the predefined appliances
        ramp_appliances = get_virtual_appliances(target_profile)
        
        # Package into standard RAMP Configuration
        ramp_config = {
            "scenario_id": scenario_id,
            "socio_technical_profile": target_profile,
            "appliances": ramp_appliances
        }
        
        # Save output
        output_json_path = OUTPUT_DIR / f"ramp_config_{scenario_id}.json"
        with open(output_json_path, 'w') as f:
            json.dump(ramp_config, f, indent=4)
            
        print(f"[+] Scenario '{scenario_id}' -> Configured as {target_profile} -> JSON Generated.")

if __name__ == "__main__":
    main()