"""
PART 6: Economic & Agricultural Impact Analysis - IMPROVED 6X
Nature-Quality Publication Standards

Focused analysis including:
1. Crop-nematode associations
2. Economic crop impact analysis
3. Climate-related research trends

Each figure is professionally designed for Nature publication
"""

import sys
sys.path.append('/home/user/DataAnalyz/TopTen/data/Real_Analyses')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from analysis_utils_improved import *
import re

# Configuration
DATA_FILE = '/home/user/DataAnalyz/TopTen/data/Real_Analyses/ALL_NEMATODES_EXTRACTED.csv'
OUTPUT_DIR = '/home/user/DataAnalyz/TopTen/data/Real_Analyses/PART_6_ANALYSIS'

print("\n" + "="*70)
print("PART 6: ECONOMIC & AGRICULTURAL IMPACT ANALYSIS - REAL DATA")
print("="*70 + "\n")

# Load data
print("Loading data...")
df = pd.read_csv(DATA_FILE)
print(f"✓ Loaded {len(df):,} records")

# CSV already has correct column names

# Basic cleaning
df['pub_year'] = pd.to_numeric(df['pub_year'], errors='coerce')
df = df.dropna(subset=['pub_year'])
df['pub_year'] = df['pub_year'].astype(int)

# Apply filters
df_clean = apply_analysis_filters(df)

print(f"\nDataset: {len(df_clean):,} records")

# ============================================================================
# FIGURE 1: Crop-Nematode Associations (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 1: Major Crop-Nematode Associations")
print("="*70)

# Extract crop mentions from abstracts
df_with_abstract = df_clean[df_clean['abstract'].notna()].copy()

# Define major economic crops
major_crops = {
    'Tomato': ['tomato'],
    'Potato': ['potato'],
    'Soybean': ['soybean', 'soya'],
    'Wheat': ['wheat'],
    'Rice': ['rice'],
    'Corn/Maize': ['corn', 'maize'],
    'Cotton': ['cotton'],
    'Banana': ['banana'],
    'Tobacco': ['tobacco'],
    'Sugar Beet': ['sugar beet', 'sugarbeet'],
    'Coffee': ['coffee'],
    'Citrus': ['citrus', 'orange', 'lemon']
}

# Extract crop-genus associations
crop_genus_assoc = []

for _, row in df_with_abstract.iterrows():
    abstract = str(row['abstract']).lower()
    genus = row['Genus']

    for crop, keywords in major_crops.items():
        if any(kw in abstract for kw in keywords):
            crop_genus_assoc.append({
                'Crop': crop,
                'Genus': genus,
                'Year': row['pub_year']
            })

df_crop_genus = pd.DataFrame(crop_genus_assoc)

if len(df_crop_genus) > 0:
    # Count associations
    assoc_counts = df_crop_genus.groupby(['Crop', 'Genus']).size().reset_index(name='Count')

    # Get top genera for each crop
    top_assoc = assoc_counts.sort_values('Count', ascending=False).head(30)

    # Create pivot for heatmap
    crop_genus_pivot = assoc_counts.pivot(index='Crop', columns='Genus', values='Count').fillna(0)

    # Select top 10 genera and top 12 crops
    top_genera = assoc_counts.groupby('Genus')['Count'].sum().nlargest(10).index
    top_crops = assoc_counts.groupby('Crop')['Count'].sum().nlargest(12).index

    heatmap_data = crop_genus_pivot.loc[top_crops, top_genera]

    # Create figure with 2 panels
    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1], wspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # LEFT: Heatmap
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd',
               cbar_kws={'label': 'Number of Publications'},
               linewidths=0.5, linecolor='gray', ax=ax1)
    ax1.set_xlabel('Nematode Genus', fontweight='bold', style='italic')
    ax1.set_ylabel('Crop', fontweight='bold')
    ax1.set_title('A. Crop-Nematode Association Matrix',
                 fontweight='bold', loc='left', pad=15)

    # RIGHT: Top 15 associations
    top15 = top_assoc.head(15).copy()
    top15['Association'] = top15['Crop'] + ' × ' + top15['Genus']

    y_pos = np.arange(len(top15))
    colors = [get_genus_color(g) for g in top15['Genus']]

    ax2.barh(y_pos, top15['Count'], color=colors,
            edgecolor='black', linewidth=0.5, alpha=0.8)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(top15['Association'], fontsize=8)
    ax2.set_xlabel('Number of Publications', fontweight='bold')
    ax2.set_title('B. Top 15 Crop-Nematode Pairs',
                 fontweight='bold', loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig1_Crop_Nematode_Associations.png')
    plt.close()

    # Save data
    assoc_counts.to_csv(f'{OUTPUT_DIR}/Tables/Table1_Crop_Genus_Associations.csv', index=False)
    print(f"✓ Identified {len(assoc_counts)} crop-genus associations")

# ============================================================================
# FIGURE 2: Economic Impact Research Trends (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 2: Economic Impact Research Trends")
print("="*70)

# Define economic keywords
economic_keywords = {
    'Yield Loss': ['yield loss', 'yield reduction', 'crop loss'],
    'Economic Damage': ['economic', 'damage', 'loss', 'cost'],
    'Management': ['management', 'control', 'integrated pest'],
    'Resistance': ['resistance', 'resistant cultivar', 'resistant variety']
}

# Count keyword mentions over time
economic_trends = []

for year in range(1980, 2024):
    year_data = df_with_abstract[df_with_abstract['pub_year'] == year]
    if len(year_data) > 0:
        year_abstracts = ' '.join(year_data['abstract'].astype(str).str.lower().values)

        for category, keywords in economic_keywords.items():
            count = sum(year_abstracts.count(kw) for kw in keywords)
            normalized = count / len(year_data)
            economic_trends.append({
                'Year': year,
                'Category': category,
                'Normalized_Count': normalized
            })

df_economic = pd.DataFrame(economic_trends)

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: Temporal trends
category_colors = {
    'Yield Loss': '#d62728',
    'Economic Damage': '#ff7f0e',
    'Management': '#2ca02c',
    'Resistance': '#1f77b4'
}

for category in economic_keywords.keys():
    cat_data = df_economic[df_economic['Category'] == category]
    cat_data = cat_data.sort_values('Year')
    # Apply smoothing
    cat_data['MA_3yr'] = cat_data['Normalized_Count'].rolling(window=3, center=True).mean()

    ax1.plot(cat_data['Year'], cat_data['MA_3yr'],
            linewidth=2.5, label=category, color=category_colors[category],
            alpha=0.8, marker='o', markersize=3, markevery=5)

ax1.set_xlabel('Year', fontweight='bold')
ax1.set_ylabel('Relative Frequency (mentions per paper)', fontweight='bold')
ax1.set_title('A. Economic Impact Research Themes (1980-2023)',
             fontweight='bold', loc='left')
ax1.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='black')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(True, alpha=0.3)

# RIGHT: Recent vs Past comparison (2014-2023 vs 2000-2013)
recent_period = df_economic[df_economic['Year'] >= 2014].groupby('Category')['Normalized_Count'].mean()
past_period = df_economic[(df_economic['Year'] >= 2000) & (df_economic['Year'] < 2014)].groupby('Category')['Normalized_Count'].mean()

categories = list(economic_keywords.keys())
x = np.arange(len(categories))
width = 0.35

bars1 = ax2.bar(x - width/2, [past_period.get(c, 0) for c in categories],
               width, label='2000-2013', color='#9467bd', alpha=0.7,
               edgecolor='black', linewidth=0.5)
bars2 = ax2.bar(x + width/2, [recent_period.get(c, 0) for c in categories],
               width, label='2014-2023', color='#2ca02c', alpha=0.7,
               edgecolor='black', linewidth=0.5)

ax2.set_xlabel('Research Theme', fontweight='bold')
ax2.set_ylabel('Relative Frequency', fontweight='bold')
ax2.set_title('B. Period Comparison', fontweight='bold', loc='left')
ax2.set_xticks(x)
ax2.set_xticklabels(categories, rotation=45, ha='right')
ax2.legend(frameon=True, fancybox=False, edgecolor='black')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig2_Economic_Impact_Trends.png')
plt.close()

# Save data
df_economic.to_csv(f'{OUTPUT_DIR}/Tables/Table2_Economic_Theme_Trends.csv', index=False)
print("✓ Analyzed economic impact research trends")

# ============================================================================
# FIGURE 3: Climate & Environmental Keywords (NEW)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 3: Climate & Environmental Research")
print("="*70)

# Define climate/environmental keywords
climate_keywords = ['climate change', 'global warming', 'temperature', 'drought',
                   'rainfall', 'precipitation', 'soil moisture', 'soil temperature']

env_keywords = ['soil health', 'soil quality', 'sustainable', 'biodiversity',
               'ecosystem', 'organic', 'biological control']

# Count mentions over time
climate_counts = []
env_counts = []

for year in range(1990, 2024):
    year_abstracts = df_with_abstract[df_with_abstract['pub_year'] == year]['abstract'].astype(str).str.lower()

    if len(year_abstracts) > 0:
        all_abstracts = ' '.join(year_abstracts.values)
        climate_count = sum(all_abstracts.count(kw) for kw in climate_keywords)
        env_count = sum(all_abstracts.count(kw) for kw in env_keywords)

        climate_counts.append({
            'Year': year,
            'Category': 'Climate-Related',
            'Count': climate_count / len(year_abstracts)
        })
        env_counts.append({
            'Year': year,
            'Category': 'Environmental/Sustainable',
            'Count': env_count / len(year_abstracts)
        })

df_climate = pd.DataFrame(climate_counts + env_counts)

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))

for category, color in [('Climate-Related', '#d62728'), ('Environmental/Sustainable', '#2ca02c')]:
    cat_data = df_climate[df_climate['Category'] == category]
    cat_data = cat_data.sort_values('Year')
    # Smoothing
    cat_data['MA_3yr'] = cat_data['Count'].rolling(window=3, center=True).mean()

    ax.plot(cat_data['Year'], cat_data['MA_3yr'],
           linewidth=3, label=category, color=color,
           alpha=0.8, marker='o', markersize=4, markevery=3)

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Relative Frequency (mentions per paper)', fontweight='bold')
ax.set_title('Emergence of Climate & Environmental Research Themes (1990-2023)',
            fontweight='bold', pad=15)
ax.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig3_Climate_Environmental_Trends.png')
plt.close()

# Save data
df_climate.to_csv(f'{OUTPUT_DIR}/Tables/Table3_Climate_Env_Trends.csv', index=False)
print("✓ Analyzed climate and environmental research trends")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("PART 6 ANALYSIS COMPLETE - IMPROVED VERSION")
print("="*70)
print("\nGenerated Figures:")
print("  ✓ Fig1: Crop-Nematode Associations (heatmap + bars)")
print("  ✓ Fig2: Economic Impact Research Trends (2-panel)")
print("  ✓ Fig3: Climate & Environmental Research (line plot)")
print("\nAll figures saved in Nature-quality format (600 DPI)")
print("="*70 + "\n")
