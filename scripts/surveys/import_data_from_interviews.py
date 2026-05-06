import pandas as pd
import numpy as np
import os

def create_data_1_2():
    # Set up paths relative to this script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "../../data/clean/surveys")
    INTERVIEWS_DIR = os.path.join(BASE_DIR, "../../data/raw/interviews")
    OUTPUT_DIR = os.path.join(BASE_DIR, "../../data/clean/surveys")
    try:
        # Load the target schema (data_1) and socioeconomic data (data_0)
        df_1 = pd.read_csv(os.path.join(DATA_DIR, "data_1.csv"))
        df_0 = pd.read_csv(os.path.join(DATA_DIR, "data_0.csv"))
        
        existing_ids = df_1['id'].astype(str).str.strip().tolist()
        
        # Read the transcripts file
        with open(os.path.join(INTERVIEWS_DIR, "all_transcripts.txt"), "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split by user ID
        blocks = content.split("user_ID:")
        new_users = []
        
        for block in blocks[1:]:
            lines = block.strip().split('\n')
            uid = lines[0].strip()
            
            # Exclude if already in data_1 or if it's an Authority profile (starts with A)
            if uid in existing_ids or uid.startswith('A'):
                continue
                
            user_data = {'id': uid}
            text_lower = block.lower()
            
            # --- 1. NLP Extraction Rules (Energy Use Data) ---
            # Appliances
            user_data['radios'] = 1 if 'radio' in text_lower else 0
            user_data['phones'] = 2 if 'dos celular' in text_lower or '2 celular' in text_lower else (1 if 'celular' in text_lower else 0)
            user_data['light_bulbs'] = 2 if 'dos foco' in text_lower else (1 if 'foco' in text_lower or 'luz' in text_lower else 0)
            
            # Technical Issues
            user_data['tech_problems_radio'] = 1 if any(phrase in text_lower for phrase in ['radio no funciona', 'se arruinó', 'no da', 'no carga la radio', 'se ha roto', 'se malogró']) else 0
            user_data['tech_problems_battery'] = 1 if any(phrase in text_lower for phrase in ['batería se agota', 'no carga bien', 'se apaga la luz', 'se apaga']) else 0
            
            # Behavior
            user_data['portability_shs'] = 1 if 'llevamos' in text_lower and any(loc in text_lower for loc in ['monte', 'chapare', 'trabajar', 'otra casa']) else 0
            
            # Cooking
            user_data['cooking_fuel_biomass'] = 1 if 'fogón' in text_lower or 'leña' in text_lower else 0
            user_data['cooking_fuel_gas'] = 1 if 'gas' in text_lower else 0
            
            # Latent Demand / Aspirations
            user_data['desired_app_TV'] = 1 if 'televisión' in text_lower or 'tele' in text_lower or 'tv' in text_lower else 0
            user_data['desired_app_fridge'] = 1 if 'refrigerador' in text_lower or 'heladera' in text_lower else 0
            user_data['desired_app_radio'] = 1 if 'comprarme otra' in text_lower and 'radio' in text_lower else 0
            
            # SHS Usage
            user_data['illum_solarpv'] = 1 
            
            new_users.append(user_data)
            
        df_new = pd.DataFrame(new_users)
        
        if df_new.empty:
            print("No new users found to extract from the transcripts.")
            return
            
        # --- 2. Merge with Socioeconomic Data (data_0.csv) ---
        df_0['id'] = df_0['id'].astype(str)
        df_new = df_new.merge(df_0, on='id', how='left')
        
        # --- 3. Align Columns to data_1.csv ---
        final_cols = df_1.columns.tolist()
        for col in final_cols:
            if col not in df_new.columns:
                df_new[col] = -1 # Add -1 for unavailable data
                
        # Reorder and fill missing merges with -1
        df_new = df_new[final_cols].fillna(-1)
        
        # Safely attempt to format numericals
        for col in df_new.columns:
            try:
                # Convert to numeric, keeping -1 formatting clean
                if df_new[col].dtype == 'float64':
                    df_new[col] = df_new[col].round(2)
            except:
                pass
        
        # --- 4. Save Outputs ---
        df_new.to_csv(os.path.join(OUTPUT_DIR, "data_1_2.csv"), index=False)
        print(f"✅ Successfully generated 'data_1_2.csv' with {len(df_new)} new households.")
        
        # Duplicate codebook for consistency
        codebook_1 = pd.read_csv(os.path.join(DATA_DIR, "codebook_1.csv"))
        codebook_1.to_csv(os.path.join(OUTPUT_DIR, "codebook_1_2.csv"), index=False)
        print(f"✅ Successfully cloned 'codebook_1.csv' to 'codebook_1_2.csv'.")
        
    except Exception as e:
        print(f"Error executing script: {e}")

create_data_1_2()