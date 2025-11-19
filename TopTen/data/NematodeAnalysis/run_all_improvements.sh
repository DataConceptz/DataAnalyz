#!/bin/bash
# Master script to run all improved analyses

echo "======================================================================="
echo "Running All Improved Nematode Analyses"
echo "======================================================================="
echo ""

# PART_1
echo "Running PART_1 (Species & Taxonomic Analysis)..."
cd /home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS
python Code/part1_improved_complete.py > /tmp/part1_improved.log 2>&1
if [ $? -eq 0 ]; then
    echo "✓ PART_1 Complete"
else
    echo "✗ PART_1 Failed - check /tmp/part1_improved.log"
fi
echo ""

# PART_2
echo "Running PART_2 (Temporal & Trend Analysis)..."
cd /home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS
python Code/part2_improved_complete.py > /tmp/part2_improved.log 2>&1
if [ $? -eq 0 ]; then
    echo "✓ PART_2 Complete"
else
    echo "✗ PART_2 Failed - check /tmp/part2_improved.log"
fi
echo ""

# PART_3-7 will be created with simpler focused improvements
echo "======================================================================="
echo "All analyses complete!"
echo "Check /tmp/*_improved.log for detailed output"
echo "======================================================================="
