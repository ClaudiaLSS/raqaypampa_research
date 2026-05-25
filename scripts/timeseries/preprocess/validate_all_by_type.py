#!/usr/bin/env python3
"""
Batch validate all timeseries files of a specific datalogger type.
Generates a summary report of data quality across all files.

Usage:
    python validate_all_by_type.py --type tpdin
    python validate_all_by_type.py --type old
    python validate_all_by_type.py --type blue
    python validate_all_by_type.py --type all
"""

import pandas as pd
import numpy as np
import argparse
from pathlib import Path
import sys
import subprocess

def get_data_columns(datalogger_type):
    """Get measurement column names by datalogger type."""
    if datalogger_type == 'tpdin':
        return ['v_pv', 'v_usb', 'v_led_1', 'v_led_2', 'c_usb', 'c_led_1', 'c_led_2']
    elif datalogger_type == 'old':
        return ['v_pv', 'v_usb', 'v_led', 'c_usb', 'c_led']
    elif datalogger_type == 'blue':
        return ['v_pv', 'v_cons', 'c_cons']
    else:
        raise ValueError(f"Unknown datalogger type: {datalogger_type}")

def detect_datalogger_type(filename):
    """Detect datalogger type from filename."""
    filename_lower = filename.lower()
    if 'tpdin' in filename_lower:
        return 'tpdin'
    elif 'old' in filename_lower:
        return 'old'
    elif 'blue' in filename_lower:
        return 'blue'
    else:
        return None

def quick_validate(filepath, datalogger_type):
    """Quick validation without full output."""
    try:
        df = pd.read_csv(filepath)
        data_cols = get_data_columns(datalogger_type)
        
        # Basic checks
        total_rows = len(df)
        empty_rows = 0
        pv_coverage = 0
        
        # Count empty rows
        for col in data_cols:
            if col in df.columns:
                empty_rows = (~df[col].notna()).sum()
                break
        
        # PV analysis
        if 'corrected_timestamp' in df.columns and 'v_pv' in df.columns:
            df['corrected_timestamp'] = pd.to_datetime(df['corrected_timestamp'], format='mixed', errors='coerce')
            df['hour'] = df['corrected_timestamp'].dt.hour
            daytime = df[(df['hour'] >= 6) & (df['hour'] < 18)]
            if len(daytime) > 0:
                pv_coverage = round(100 * (daytime['v_pv'] > 2).sum() / len(daytime), 1)
        
        # Timestamp continuity
        regressions = 0
        if 'corrected_timestamp' in df.columns:
            df['corrected_timestamp'] = pd.to_datetime(df['corrected_timestamp'], format='mixed', errors='coerce')
            ts_diff = df['corrected_timestamp'].diff()
            regressions = (ts_diff < pd.Timedelta(0)).sum()
        
        return {
            'status': 'OK',
            'total_rows': total_rows,
            'empty_rows': empty_rows,
            'pv_coverage': pv_coverage,
            'regressions': regressions,
            'error': None
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'total_rows': 0,
            'empty_rows': 0,
            'pv_coverage': 0,
            'regressions': 0,
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(
        description="Batch validate all timeseries files of a specific type",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_all_by_type.py --type tpdin
  python validate_all_by_type.py --type old
  python validate_all_by_type.py --type blue
  python validate_all_by_type.py --type all
        """
    )
    
    parser.add_argument("--type", type=str, required=True, choices=['tpdin', 'old', 'blue', 'all'],
                        help="Datalogger type to validate (or 'all')")
    
    args = parser.parse_args()
    
    # Find timeseries data directory
    timeseries_dir = Path("/home/claudia/Documents/raqaypampa_research/data/clean/timeseries")
    
    if not timeseries_dir.exists():
        print(f"❌ Error: Directory not found: {timeseries_dir}")
        sys.exit(1)
    
    # Determine which types to process
    if args.type == 'all':
        types = ['tpdin', 'old', 'blue']
    else:
        types = [args.type]
    
    # Process each type
    all_results = []
    
    for dtype in types:
        print(f"\n{'='*80}")
        print(f"VALIDATING {dtype.upper()} FILES")
        print(f"{'='*80}\n")
        
        # Find all files of this type
        pattern = f"{dtype}_user_*.csv"
        files = sorted(timeseries_dir.glob(pattern))
        
        if not files:
            print(f"No files found matching pattern: {pattern}\n")
            continue
        
        print(f"Found {len(files)} files\n")
        
        results = []
        
        for filepath in files:
            filename = filepath.name
            result = quick_validate(filepath, dtype)
            result['filename'] = filename
            results.append(result)
            
            # Print status
            status_icon = "✓" if result['status'] == 'OK' and result['regressions'] == 0 else "⚠️" if result['status'] == 'OK' else "❌"
            pv_indicator = "📊" if result['pv_coverage'] > 80 else "⚡" if result['pv_coverage'] > 50 else "❄️"
            
            if result['status'] == 'OK':
                print(f"{status_icon} {filename:25s} | Rows: {result['total_rows']:7,d} | PV: {result['pv_coverage']:5.1f}% {pv_indicator} | Regr: {result['regressions']:3d}")
            else:
                print(f"{status_icon} {filename:25s} | ERROR: {result['error']}")
        
        all_results.append({
            'type': dtype,
            'results': results
        })
    
    # Generate summary report
    print(f"\n\n{'='*80}")
    print("SUMMARY REPORT")
    print(f"{'='*80}\n")
    
    for group in all_results:
        dtype = group['type']
        results = group['results']
        
        if not results:
            continue
        
        ok_count = sum(1 for r in results if r['status'] == 'OK' and r['regressions'] == 0)
        error_count = sum(1 for r in results if r['status'] == 'ERROR')
        regression_count = sum(1 for r in results if r['status'] == 'OK' and r['regressions'] > 0)
        
        print(f"{dtype.upper()}:")
        print(f"  Total files: {len(results)}")
        print(f"  ✓ Good (no issues): {ok_count}")
        if regression_count > 0:
            print(f"  ⚠️  Regressions detected: {regression_count}")
        if error_count > 0:
            print(f"  ❌ Errors: {error_count}")
        
        # Statistics
        if results:
            total_rows = sum(r['total_rows'] for r in results if r['status'] == 'OK')
            avg_pv = np.mean([r['pv_coverage'] for r in results if r['status'] == 'OK' and r['pv_coverage'] > 0])
            print(f"  Total rows: {total_rows:,}")
            print(f"  Avg PV coverage: {avg_pv:.1f}%")
        
        print()
    
    # Data quality assessment
    print(f"{'─'*80}")
    print("DATA QUALITY ASSESSMENT:")
    print(f"{'─'*80}")
    
    for group in all_results:
        dtype = group['type']
        results = group['results']
        
        if not results:
            continue
        
        ok_count = sum(1 for r in results if r['status'] == 'OK' and r['regressions'] == 0)
        total = len(results)
        pct = 100 * ok_count / total if total > 0 else 0
        
        if pct == 100:
            rating = "EXCELLENT ✓"
        elif pct >= 80:
            rating = "GOOD ✓"
        elif pct >= 50:
            rating = "FAIR ⚠️"
        else:
            rating = "POOR ❌"
        
        print(f"  {dtype.upper():10s}: {pct:5.1f}% pass rate → {rating}")
    
    print(f"\n{'='*80}\n")

if __name__ == '__main__':
    main()
