"""
PART 2: Temporal & Trend Analysis
==================================

Analyses:
1. Long-term research trend analysis by genus and species
2. Advanced forecasting models (20-year projections)
3. Top 10 genera with 3-5 species each
4. Publication date formatting and time series preparation

Author: Claude
Date: November 19, 2025
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from analysis_utils import *
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Tables'

print("="*70)
print("PART 2: TEMPORAL & TREND ANALYSIS")
print("="*70)

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================

print("\n[1] Loading and preparing data...")
df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# Ensure publication_date is datetime
df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')

# Fill missing dates using pub_year
mask = df['publication_date'].isna()
if mask.sum() > 0:
    df.loc[mask, 'publication_date'] = pd.to_datetime(
        df.loc[mask, 'pub_year'].astype(str) + '-07-01',  # Mid-year
        errors='coerce'
    )

print(f"   Data prepared: {len(df):,} records")
print(f"   Date range: {df['publication_date'].min()} to {df['publication_date'].max()}")

# ============================================================================
# ANALYSIS 1: LONG-TERM RESEARCH TRENDS BY GENUS
# ============================================================================

print("\n[2] Analyzing long-term research trends by genus...")

# Aggregate by year and genus
genus_trends = df.groupby(['pub_year', 'Genus']).agg({
    'count_numeric': 'sum',
    'Species': 'count'
}).reset_index()
genus_trends.columns = ['Year', 'Genus', 'Total_Count', 'N_Records']

# Save detailed trends
genus_trends.to_csv(f'{TABLES_PATH}/genus_trends_by_year.csv', index=False)
print(f"   ✓ Saved: genus_trends_by_year.csv")

# Get top 10 genera by total records
top10_genera = df.groupby('Genus')['count_numeric'].sum().nlargest(10).index.tolist()
print(f"   ✓ Top 10 genera identified: {', '.join(top10_genera[:5])}...")

# FIGURE 1: Research Trends Over Time (Top 10 Genera)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1a: Stacked area chart - top 10 genera
ax = axes[0, 0]
genus_pivot = genus_trends[genus_trends['Genus'].isin(top10_genera)].pivot_table(
    index='Year',
    columns='Genus',
    values='N_Records',
    fill_value=0
)

colors_genera = [GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in genus_pivot.columns]
ax.stackplot(genus_pivot.index, *[genus_pivot[col] for col in genus_pivot.columns],
            labels=genus_pivot.columns, colors=colors_genera, alpha=0.8)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Records')
ax.set_title('A. Research Trends - Top 10 Genera (Stacked)', fontweight='bold', loc='left')
ax.legend(loc='upper left', fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)

# 1b: Individual trends - top 5 genera
ax = axes[0, 1]
for genus in top10_genera[:5]:
    genus_data = genus_trends[genus_trends['Genus'] == genus]
    color = GENUS_COLORS.get(genus, NEMATODE_COLORS['primary'])
    ax.plot(genus_data['Year'], genus_data['N_Records'],
           label=genus, linewidth=2, marker='o', markersize=3, color=color)

ax.set_xlabel('Year')
ax.set_ylabel('Number of Records')
ax.set_title('B. Individual Trends - Top 5 Genera', fontweight='bold', loc='left')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# 1c: Growth rate analysis
ax = axes[1, 0]
# Calculate 5-year moving average growth
growth_data = []
for genus in top10_genera:
    genus_yearly = genus_trends[genus_trends['Genus'] == genus].sort_values('Year')
    if len(genus_yearly) > 5:
        genus_yearly['MA_5yr'] = genus_yearly['N_Records'].rolling(window=5, min_periods=1).mean()
        recent_avg = genus_yearly['MA_5yr'].iloc[-5:].mean()
        early_avg = genus_yearly['MA_5yr'].iloc[:5].mean()
        growth_rate = ((recent_avg - early_avg) / early_avg * 100) if early_avg > 0 else 0
        growth_data.append({'Genus': genus, 'Growth_Rate': growth_rate, 'Recent_Avg': recent_avg})

growth_df = pd.DataFrame(growth_data).sort_values('Growth_Rate', ascending=False)
colors_growth = [GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in growth_df['Genus']]

ax.barh(range(len(growth_df)), growth_df['Growth_Rate'],
       color=colors_growth, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(growth_df)))
ax.set_yticklabels(growth_df['Genus'])
ax.set_xlabel('Growth Rate (%)')
ax.set_title('C. Research Growth Rate (Early vs Recent)', fontweight='bold', loc='left')
ax.axvline(0, color='black', linestyle='-', linewidth=1)
ax.grid(True, alpha=0.3, axis='x')

# 1d: Publication density heatmap
ax = axes[1, 1]
heatmap_data = genus_trends[genus_trends['Genus'].isin(top10_genera[:10])].pivot_table(
    index='Genus',
    columns='Year',
    values='N_Records',
    fill_value=0
)

# Select recent 20 years for clarity
recent_years = sorted(heatmap_data.columns)[-20:]
heatmap_recent = heatmap_data[recent_years]

sns.heatmap(heatmap_recent, cmap='YlOrRd', linewidths=0.5, ax=ax,
           cbar_kws={'label': 'Records'}, fmt='g')
ax.set_title('D. Publication Density (Last 20 Years)', fontweight='bold', loc='left')
ax.set_xlabel('Year')
ax.set_ylabel('Genus')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig1_Genus_Temporal_Trends.png')
plt.close()

# ============================================================================
# ANALYSIS 2: SPECIES-LEVEL TRENDS
# ============================================================================

print("\n[3] Analyzing species-level trends...")

# Get top 3-5 species for each top 10 genus
top_species_by_genus = {}
for genus in top10_genera:
    genus_df = df[df['Genus'] == genus]
    top_species = genus_df.groupby('Species')['count_numeric'].sum().nlargest(5).index.tolist()
    # Limit to 3-5 species with substantial records
    species_counts = genus_df.groupby('Species').size()
    significant_species = species_counts[species_counts >= 10].index.tolist()
    top_species = [s for s in top_species if s in significant_species][:5]
    top_species_by_genus[genus] = top_species

# Save species selection
species_selection = []
for genus, species_list in top_species_by_genus.items():
    for species in species_list:
        species_selection.append({'Genus': genus, 'Species': species})
species_selection_df = pd.DataFrame(species_selection)
species_selection_df.to_csv(f'{TABLES_PATH}/selected_species_for_forecasting.csv', index=False)
print(f"   ✓ Selected species for forecasting: {len(species_selection_df)}")

# Species trends over time
species_trends = df.groupby(['pub_year', 'Genus', 'Species']).agg({
    'count_numeric': 'sum',
}).reset_index()
species_trends.columns = ['Year', 'Genus', 'Species', 'Total_Count']
species_trends.to_csv(f'{TABLES_PATH}/species_trends_by_year.csv', index=False)

# FIGURE 2: Species-Level Trends (Selected genera)
n_genera_plot = min(4, len(top10_genera))
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

for idx, genus in enumerate(top10_genera[:4]):
    ax = axes[idx]
    species_list = top_species_by_genus.get(genus, [])[:5]

    for species in species_list:
        data = species_trends[(species_trends['Genus'] == genus) &
                            (species_trends['Species'] == species)]
        if len(data) > 0:
            ax.plot(data['Year'], data['Total_Count'],
                   label=species, linewidth=2, marker='o', markersize=3)

    ax.set_xlabel('Year')
    ax.set_ylabel('Occurrence Count')
    ax.set_title(f'{chr(65+idx)}. {genus} - Species Trends', fontweight='bold', loc='left')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig2_Species_Temporal_Trends.png')
plt.close()

print("\n[Analysis 1 & 2 Complete]")
print("="*70)
