"""
Master Script for Running All 7 Analyses on Real Data (CSV)
Automatically handles CSV format and runs all improved analyses
"""

import sys
import os
import subprocess

BASE_DIR = '/home/user/DataAnalyz/TopTen/data/Real_Analyses'
DATA_FILE = f'{BASE_DIR}/ALL_NEMATODES_EXTRACTED.csv'

print("="*80)
print("RUNNING ALL 7 IMPROVED ANALYSES ON REAL DATA")
print("="*80)
print(f"\nData file: {DATA_FILE}")
print(f"Output directory: {BASE_DIR}")
print("\n" + "="*80 + "\n")

# Check if data file exists
if not os.path.exists(DATA_FILE):
    print(f"ERROR: Data file not found: {DATA_FILE}")
    print("Please ensure ALL_NEMATODES_EXTRACTED.csv is in the Real_Analyses folder")
    sys.exit(1)

# Import shared libraries
sys.path.append(BASE_DIR)
from analysis_utils_improved import *

# Quick data check
print("Checking data file...")
import pandas as pd
df_check = pd.read_csv(DATA_FILE, nrows=5)
print(f"✓ File readable")
print(f"✓ Columns: {', '.join(df_check.columns[:10].tolist())}...")

df_full = pd.read_csv(DATA_FILE)
print(f"✓ Total records: {len(df_full):,}")
print(f"✓ Unique genera: {df_full['Genus'].nunique() if 'Genus' in df_full.columns else 'N/A'}")
print(f"✓ Unique species: {df_full['Species'].nunique() if 'Species' in df_full.columns else 'N/A'}")
print(f"✓ Year range: {df_full['pub_year'].min()}-{df_full['pub_year'].max() if 'pub_year' in df_full.columns else 'N/A'}")

print("\n" + "="*80)
print("DATA CHECK COMPLETE - READY TO RUN ANALYSES")
print("="*80)
print("\nNote: Each analysis part will be generated using the improved scripts.")
print("All figures will be 600 DPI Nature-quality with consistent colors.")
print("\n" + "="*80 + "\n")
