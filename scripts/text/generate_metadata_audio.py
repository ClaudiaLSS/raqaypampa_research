#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:37:23 2026

@author: claudia
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import mutagen  # Importación base necesaria

# --- SET YOUR PATHS ---
AUDIO_DIR = Path("/home/claudia/Documents/raqaypampa_research/data/raw/interviews/recordings_feb2026")
OUTPUT_CSV = Path("/home/claudia/Documents/raqaypampa_research/data/raw/interviews/recordings_feb2026/audio_inventory.csv")

def generate_audio_metadata():
    audio_records = []
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    if not AUDIO_DIR.exists():
        print(f"❌ Carpeta no encontrada: {AUDIO_DIR}")
        return

    print(f"🔍 Analizando archivos en {AUDIO_DIR}...")

    for file_path in AUDIO_DIR.iterdir():
        if file_path.suffix.lower() == ".mp3":
            try:
                # Usamos mutagen.File para evitar el error de 'MP3 undefined'
                audio = mutagen.File(file_path)
                
                # Obtener duración
                if audio is not None and hasattr(audio, 'info'):
                    duration_sec = audio.info.length
                    mins, secs = divmod(int(duration_sec), 60)
                    duration_str = f"{mins:02d}:{secs:02d}"
                else:
                    duration_str = "00:00"

                stats = file_path.stat()
                file_date = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d')
                
                # Extraer User ID (ej: user_48 -> 48)
                user_id = file_path.stem.split('_')[-1]

                audio_records.append({
                    "file_name": file_path.name,
                    "case_id": file_path.stem,
                    "user_id": user_id,
                    "duration": duration_str,
                    "size_mb": round(stats.st_size / (1024 * 1024), 2),
                    "fecha_archivo": file_date,
                    "tipo": "Autoridad" if "A" in user_id or "auth" in file_path.name.lower() else "Usuario"
                })
                print(f" ✅ Procesado: {file_path.name}")

            except Exception as e:
                print(f" ❌ Error en {file_path.name}: {e}")

    if audio_records:
        df = pd.DataFrame(audio_records)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\n🚀 ¡Inventario listo! {len(df)} archivos registrados.")
        print(f"📍 Archivo guardado en: {OUTPUT_CSV}")
    else:
        print(f" ⚠️ No se procesaron archivos. Verifica que mutagen esté instalado: 'pip install mutagen'")

if __name__ == "__main__":
    generate_audio_metadata()