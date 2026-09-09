"""
RAMP Profile Compiler - Empirical Edition

Ingests empirical outputs and compiles them into the strict RAMP engine JSON hierarchy.
Features Semantic Hardware Routing to pair anthropological Virtual Appliances 
with their physical hardware telemetry (LED_1, LED_2, USB).
"""
import json
import argparse
from pathlib import Path
import sys
import re

# Define directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
OUTPUT_DIR = SCRIPT_DIR / "output"
PROFILES_DIR = PROJECT_ROOT / "data" / "clean" / "profiles"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_markdown_profile(markdown_path):
    """
    Extract Virtual Appliances, Anthropological Windows, and Hardware Inventory.
    """
    if not Path(markdown_path).exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
    
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Parse Hardware Inventory Mapping (Which LED is Indoor vs Outdoor)
    inventory_mapping = {'indoor': 'LED_1', 'outdoor': 'LED_2'} # Defaults
    inventory_section = re.search(r'\*\*Appliance inventory:\*\*(.*?)(?=###|\Z)', content, re.DOTALL | re.IGNORECASE)
    
    if inventory_section:
        inv_text = inventory_section.group(1).lower()
        # Find which LED is assigned to outdoor
        if 'led_1' in inv_text and 'outdoor' in inv_text.split('led_1')[1].split('\n')[0]:
            inventory_mapping['outdoor'] = 'LED_1'
            inventory_mapping['indoor'] = 'LED_2'
        elif 'led_2' in inv_text and 'outdoor' in inv_text.split('led_2')[1].split('\n')[0]:
            inventory_mapping['outdoor'] = 'LED_2'
            inventory_mapping['indoor'] = 'LED_1'
            
    # 2. Parse Virtual Appliances
    virtual_appliances = {}
    appliance_pattern = r'### \*\*Virtual Appliance[^:]*: ([^\n]+)\*\*'
    window_pattern = r'- \*\*Anthropological window:\*\* \[(\d+),\s*(\d+)\]'
    
    appliances = re.finditer(appliance_pattern, content)
    
    for appliance_match in appliances:
        app_name = appliance_match.group(1).strip()
        app_start = appliance_match.start()
        
        next_appliance = re.search(appliance_pattern, content[app_start + 10:])
        app_end = app_start + 10 + next_appliance.start() if next_appliance else len(content)
        
        app_section = content[app_start:app_end]
        window_match = re.search(window_pattern, app_section)
        
        if window_match:
            start_minute = int(window_match.group(1))
            end_minute = int(window_match.group(2))
            virtual_appliances[app_name] = (start_minute, end_minute)
    
    return virtual_appliances, inventory_mapping


def determine_target_hardware(va_name, datalogger_type, inventory_mapping):
    """Semantic router: Maps a sociological appliance name to physical hardware."""
    va_lower = va_name.lower()
    
    # 1. Is it a charging/USB device?
    if any(keyword in va_lower for keyword in ['charg', 'portable', 'usb', 'radio', 'phone']):
        return 'USB'
        
    # 2. If it's an OLD logger, there is only one lighting channel
    if datalogger_type == 'old':
        return 'LED'
        
    # 3. If it's TPDIN, route based on Indoor vs Outdoor intent
    if 'outdoor' in va_lower or 'transit' in va_lower:
        return inventory_mapping['outdoor']
    else:
        # Default all task, safety, and morning lights to the indoor channel
        return inventory_mapping['indoor']


def find_matching_period_data(hw_data, va_name, va_bounds):
    """Finds the correct extracted data for the virtual appliance."""
    # 1. Try exact name match (if Script 1 extracted perfectly by VA name)
    if va_name in hw_data:
        return hw_data[va_name]
        
    # 2. Fallback: Match by anthropological window overlap
    start_min, end_min = va_bounds
    best_match = None
    highest_prob = -1
    
    for period_name, params in hw_data.items():
        # Check if the extracted window overlaps with our anthropological window
        w_start, w_end = params.get('window_1', [0, 0])
        
        # If the start time is near the anthropological start time
        if abs(w_start - start_min) <= 120 or abs(w_end - end_min) <= 120:
            if params.get('occasional_use_probability', 0) > highest_prob:
                highest_prob = params.get('occasional_use_probability', 0)
                best_match = params
                
    # 3. Ultimate Fallback: Just return the period with the highest usage
    if not best_match:
        for period_name, params in hw_data.items():
            if params.get('occasional_use_probability', 0) > highest_prob:
                highest_prob = params.get('occasional_use_probability', 0)
                best_match = params
                
    return best_match


def compile_ramp_appliances(ramp_params_by_period_file, virtual_appliances, inventory_mapping, hardware_dict, datalogger_type):
    """Compile paired parameters into final RAMP JSON architecture."""
    with open(ramp_params_by_period_file, 'r') as f:
        ramp_data = json.load(f)
    
    compiled_appliances = []
    
    for va_name, va_bounds in virtual_appliances.items():
        # 1. Determine which hardware port this virtual appliance uses
        target_hw = determine_target_hardware(va_name, datalogger_type, inventory_mapping)
        
        # Ensure we have data for this hardware
        if target_hw not in ramp_data:
            continue
            
        hw_data = ramp_data[target_hw]
        
        # 2. Find the correct time period data
        best_params = find_matching_period_data(hw_data, va_name, va_bounds)
        
        # 3. Apply the Pruning Rule (Occasional Use >= 0.15)
        if best_params and best_params.get('occasional_use_probability', 0) >= 0.15:
            
            appliance_def = {
                'name': va_name,
                'number': 1,
                'power': hardware_dict.get(f'{target_hw}_W', 3.0),
                'num_windows': best_params.get('num_windows', 1),
                'func_time': best_params.get('func_time', 0.0),
                'func_cycle': best_params.get('func_cycle', 0.0),
                'time_fraction_random_variability': best_params.get('time_fraction_random_variability', 0.0),
                'random_var_w': best_params.get('random_var_w', 0.0),
                'occasional_use': best_params.get('occasional_use_probability', 0.0)
            }
            
            # Map the precise extracted windows
            window_count = best_params.get('num_windows', 1)
            for i in range(1, window_count + 1):
                window_key = f'window_{i}'
                if window_key in best_params:
                    appliance_def[window_key] = best_params[window_key]
                elif i == 1:
                    appliance_def['window_1'] = list(va_bounds)
            
            compiled_appliances.append(appliance_def)
            
    return compiled_appliances


def compile_profile(user_id):
    """Compile empirical data into a RAMP profile JSON."""
    empirical_file = OUTPUT_DIR / f"empirical_parameters_user_{user_id}.json"
    ramp_period_file = OUTPUT_DIR / f"ramp_parameters_by_period_user_{user_id}.json"
    
    if not empirical_file.exists() or not ramp_period_file.exists():
        print(f"[!] Missing input JSON files for user {user_id}")
        return False
    
    with open(empirical_file, 'r') as f:
        baseline_data = json.load(f)
    
    hardware_dict = baseline_data.get('hardware', {})
    datalogger_type = baseline_data.get('datalogger_type', 'unknown')
    
    # Dynamically fetch the EXACT profile assigned to this user by Script 1
    assigned_profile = baseline_data.get('assigned_profile', 'profile_1_agricultural_core.md')
    profile_md_file = PROFILES_DIR / assigned_profile
    
    try:
        virtual_appliances, inventory_mapping = parse_markdown_profile(profile_md_file)
        inferred_profile_name = profile_md_file.stem.replace('profile_', '')
    except Exception as e:
        print(f"[!] Error parsing profile {assigned_profile}: {e}")
        return False
    
    # Compile the mapped appliances
    try:
        compiled_appliances = compile_ramp_appliances(
            ramp_period_file, virtual_appliances, inventory_mapping, hardware_dict, datalogger_type
        )
    except Exception as e:
        print(f"[!] Error compiling appliances for user {user_id}: {e}")
        return False
    
    # Build final RAMP payload
    ramp_config = {
        'user_id': user_id,
        'datalogger_type': datalogger_type,
        'socio_technical_profile': inferred_profile_name,
        'appliances': compiled_appliances
    }
    
    output_json_path = OUTPUT_DIR / f"{inferred_profile_name}_ramp_input_user_{user_id}.json"
    with open(output_json_path, 'w') as f:
        json.dump(ramp_config, f, indent=4)
    
    print(f"[+] User {user_id} ({datalogger_type.upper()}) -> {inferred_profile_name.upper()}")
    print(f"    ✓ Read hardware mapping: Indoor={inventory_mapping['indoor']}, Outdoor={inventory_mapping['outdoor']}")
    print(f"    ✓ Compiled {len(compiled_appliances)} active appliances (pruned {len(virtual_appliances) - len(compiled_appliances)} unused)")
    print(f"    ✓ Saved: {output_json_path.name}")
    
    return True


def batch_compile():
    empirical_files = list(OUTPUT_DIR.glob('empirical_parameters_user_*.json'))
    
    if not empirical_files:
        print(f"No empirical parameter files found in {OUTPUT_DIR}")
        return
    
    print(f"\n{'='*70}")
    print(f"RAMP PROFILE COMPILER - BATCH MODE")
    print(f"{'='*70}")
    print(f"Found {len(empirical_files)} user(s) to compile\n")
    
    success_count = 0
    for empirical_file in sorted(empirical_files):
        user_id = empirical_file.stem.split('_')[-1]
        if compile_profile(user_id):
            success_count += 1
    
    print(f"\n{'='*70}")
    print(f"✓ Compilation complete: {success_count}/{len(empirical_files)} users successful")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile empirical RAMP parameters into RAMP JSON")
    parser.add_argument("--user", type=str, help="Process specific user (e.g., '74')")
    args = parser.parse_args()
    
    if args.user:
        print(f"\n{'='*70}")
        print(f"RAMP PROFILE COMPILER - USER MODE")
        print(f"{'='*70}\n")
        compile_profile(args.user)
    else:
        batch_compile()