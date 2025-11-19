"""
PART 1: Species & Taxonomic Analysis
=====================================

Analyses:
1. Species discovery rate and taxonomic completeness
2. Host-parasite relationship network
3. Geographic distribution patterns
4. Research bias analysis (species and plant hosts)

Author: Claude
Date: November 19, 2025
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import Counter
import networkx as nx
from analysis_utils import *
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Tables'

print("="*70)
print("PART 1: SPECIES & TAXONOMIC ANALYSIS")
print("="*70)

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================

print("\n[1] Loading and preparing data...")
df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

print(f"   Raw records: {len(df_raw):,}")
print(f"   After filtering: {len(df):,}")

# ============================================================================
# ANALYSIS 1: SPECIES DISCOVERY RATE & TAXONOMIC COMPLETENESS
# ============================================================================

print("\n[2] Analyzing species discovery rate...")

# Group by year and count cumulative species
yearly_species = df.groupby('pub_year').agg({
    'Species': lambda x: x.nunique(),
    'Genus': lambda x: x.nunique()
}).reset_index()

yearly_species.columns = ['Year', 'New_Species', 'Genera']

# Calculate cumulative discovery
yearly_species = yearly_species.sort_values('Year')
yearly_species['Cumulative_Species'] = yearly_species['New_Species'].cumsum()
yearly_species['Cumulative_Genera'] = yearly_species['Genera'].cumsum()

# Calculate discovery rate (species per year)
yearly_species['Discovery_Rate_5yr'] = yearly_species['New_Species'].rolling(window=5, center=True).mean()

# Save table
yearly_species.to_csv(f'{TABLES_PATH}/species_discovery_by_year.csv', index=False)
print(f"   ✓ Saved: species_discovery_by_year.csv")

# FIGURE 1: Species Discovery Rate Over Time
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1a: Annual species discovery
ax = axes[0, 0]
ax.bar(yearly_species['Year'], yearly_species['New_Species'],
       color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.plot(yearly_species['Year'], yearly_species['Discovery_Rate_5yr'],
        color=NEMATODE_COLORS['accent2'], linewidth=2, label='5-year moving average')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Species Mentioned')
ax.set_title('A. Annual Species Discovery Rate', fontweight='bold', loc='left')
ax.legend()
ax.grid(True, alpha=0.3)

# 1b: Cumulative species discovery
ax = axes[0, 1]
ax.plot(yearly_species['Year'], yearly_species['Cumulative_Species'],
        color=NEMATODE_COLORS['primary'], linewidth=2.5, marker='o', markersize=3)
ax.fill_between(yearly_species['Year'], 0, yearly_species['Cumulative_Species'],
                alpha=0.3, color=NEMATODE_COLORS['primary'])
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Species Count')
ax.set_title('B. Cumulative Species Discovery', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

# 1c: Genus vs Species diversity over time
ax = axes[1, 0]
ax.plot(yearly_species['Year'], yearly_species['Cumulative_Genera'],
        color=NEMATODE_COLORS['accent1'], linewidth=2.5, label='Genera', marker='s', markersize=3)
ax.plot(yearly_species['Year'], yearly_species['Cumulative_Species'],
        color=NEMATODE_COLORS['primary'], linewidth=2.5, label='Species', marker='o', markersize=3)
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Count')
ax.set_title('C. Taxonomic Diversity Accumulation', fontweight='bold', loc='left')
ax.legend()
ax.grid(True, alpha=0.3)

# 1d: Species per genus ratio
ax = axes[1, 1]
genus_species_ratio = df.groupby('Genus')['Species'].nunique().reset_index()
genus_species_ratio.columns = ['Genus', 'Species_Count']
genus_species_ratio = genus_species_ratio.sort_values('Species_Count', ascending=False).head(15)

ax.barh(genus_species_ratio['Genus'], genus_species_ratio['Species_Count'],
        color=[GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in genus_species_ratio['Genus']])
ax.set_xlabel('Number of Species')
ax.set_ylabel('Genus')
ax.set_title('D. Species Richness by Genus (Top 15)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig1_Species_Discovery_Analysis.png')
plt.close()

# ============================================================================
# ANALYSIS 2: TAXONOMIC COMPLETENESS
# ============================================================================

print("\n[3] Assessing taxonomic completeness...")

# Calculate completeness metrics
genera_data = df.groupby('Genus').agg({
    'Species': 'nunique',
    'pub_year': 'count',
    'count_numeric': 'sum',
    'citations': ['mean', 'sum']
}).reset_index()

genera_data.columns = ['Genus', 'N_Species', 'N_Publications', 'Total_Mentions',
                       'Mean_Citations', 'Total_Citations']

# Calculate completeness score (publications per species)
genera_data['Pubs_per_Species'] = genera_data['N_Publications'] / genera_data['N_Species']
genera_data = genera_data.sort_values('N_Publications', ascending=False)

# Save table
genera_data.to_csv(f'{TABLES_PATH}/genus_taxonomic_completeness.csv', index=False)
print(f"   ✓ Saved: genus_taxonomic_completeness.csv")

# FIGURE 2: Taxonomic Completeness Analysis
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 2a: Publications vs Species scatter
ax = axes[0, 0]
top_genera = genera_data.head(15)
colors_list = [GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in top_genera['Genus']]

scatter = ax.scatter(top_genera['N_Species'], top_genera['N_Publications'],
                    s=top_genera['Total_Mentions']*2, c=colors_list, alpha=0.6, edgecolors='black', linewidth=1)

# Add genus labels
for idx, row in top_genera.iterrows():
    ax.annotate(row['Genus'], (row['N_Species'], row['N_Publications']),
               fontsize=8, ha='center', va='bottom')

ax.set_xlabel('Number of Species')
ax.set_ylabel('Number of Publications')
ax.set_title('A. Research Effort vs Species Diversity', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

# 2b: Completeness score by genus
ax = axes[0, 1]
top15 = genera_data.head(15)
ax.barh(range(len(top15)), top15['Pubs_per_Species'],
        color=[GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in top15['Genus']])
ax.set_yticks(range(len(top15)))
ax.set_yticklabels(top15['Genus'])
ax.set_xlabel('Publications per Species')
ax.set_title('B. Research Completeness (Top 15 Genera)', fontweight='bold', loc='left')
ax.axvline(top15['Pubs_per_Species'].median(), color='red', linestyle='--',
          label=f'Median: {top15["Pubs_per_Species"].median():.1f}')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

# 2c: Distribution of species per genus
ax = axes[1, 0]
species_counts = genera_data['N_Species'].value_counts().sort_index()
ax.bar(species_counts.index, species_counts.values, color=NEMATODE_COLORS['accent1'],
      alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xlabel('Number of Species per Genus')
ax.set_ylabel('Number of Genera')
ax.set_title('C. Distribution of Species Richness', fontweight='bold', loc='left')
ax.set_xlim(0, max(species_counts.index) + 5)
ax.grid(True, alpha=0.3)

# 2d: Top species by research intensity
ax = axes[1, 1]
species_data = df.groupby(['Genus', 'Species']).agg({
    'pub_year': 'count',
    'citations': 'sum'
}).reset_index()
species_data.columns = ['Genus', 'Species', 'N_Publications', 'Total_Citations']
species_data = species_data.sort_values('N_Publications', ascending=False).head(15)
species_data['Label'] = species_data['Genus'] + ' ' + species_data['Species']

ax.barh(range(len(species_data)), species_data['N_Publications'],
        color=[GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in species_data['Genus']])
ax.set_yticks(range(len(species_data)))
ax.set_yticklabels(species_data['Label'], fontsize=8)
ax.set_xlabel('Number of Publications')
ax.set_title('D. Most Studied Species', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig2_Taxonomic_Completeness.png')
plt.close()

print("\n[Analysis 1 & 2 Complete]")
print("="*70)
