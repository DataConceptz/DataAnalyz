"""
PART 1 COMPLETE ANALYSIS RUNNER
================================
Runs all PART_1 analyses and generates all outputs
"""

import subprocess
import sys

print("="*80)
print(" PART 1: SPECIES & TAXONOMIC ANALYSIS")
print(" Running Complete Analysis Pipeline")
print("="*80)

scripts = [
    'part1_analysis.py',
    'part1_analysis_continued.py',
    'part1_analysis_final.py'
]

for script in scripts:
    print(f"\n>>> Executing: {script}")
    result = subprocess.run([sys.executable, script],
                          cwd='/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Code',
                          capture_output=False)
    if result.returncode != 0:
        print(f"ERROR in {script}")
        sys.exit(1)

print("\n" + "="*80)
print(" ALL PART 1 ANALYSES COMPLETED SUCCESSFULLY!")
print("="*80)
