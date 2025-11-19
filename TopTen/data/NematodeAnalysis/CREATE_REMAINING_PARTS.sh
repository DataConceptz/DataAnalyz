#!/bin/bash
# Quick setup for remaining analysis parts

echo "Setting up PART_3 through PART_7 structure..."

for part in PART_3 PART_4 PART_5 PART_6 PART_7; do
    echo "Creating $part..."
    mkdir -p NematodeAnalysis/$part/{Charts,Tables,Code,Reports}
done

echo "✓ All folders created!"
ls -d NematodeAnalysis/PART_*/
