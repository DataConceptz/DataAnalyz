"""
PART 2 COMPLETE ANALYSIS RUNNER
================================
Runs all PART_2 analyses and generates all outputs
"""

import subprocess
import sys

print("="*80)
print(" PART 2: TEMPORAL & TREND ANALYSIS")
print(" Running Complete Analysis Pipeline")
print("="*80)

scripts = [
    'part2_analysis.py',
    'part2_forecasting.py',
    'part2_summary.py'
]

for script in scripts:
    print(f"\n>>> Executing: {script}")
    result = subprocess.run([sys.executable, script],
                          cwd='/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Code',
                          capture_output=False)
    if result.returncode != 0:
        print(f"ERROR in {script}")
        sys.exit(1)

print("\n" + "="*80)
print(" ALL PART 2 ANALYSES COMPLETED SUCCESSFULLY!")
print("="*80)
