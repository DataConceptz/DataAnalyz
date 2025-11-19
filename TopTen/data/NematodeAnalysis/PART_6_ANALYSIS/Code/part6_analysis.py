"""
PART 6: Economic & Agricultural Impact Analysis
===============================================
Crop patterns, economic impact, climate trends
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from analysis_utils import *

DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_6_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_6_ANALYSIS/Tables'

print("="*70)
print("PART 6: ECONOMIC & AGRICULTURAL IMPACT ANALYSIS")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# Extract crop mentions from abstracts
crop_keywords = {
    'Tomato': ['tomato', 'lycopersicum'],
    'Potato': ['potato', 'solanum tuberosum'],
    'Wheat': ['wheat', 'triticum'],
    'Rice': ['rice', 'oryza'],
    'Soybean': ['soybean', 'glycine max'],
    'Cotton': ['cotton', 'gossypium'],
    'Corn/Maize': ['corn', 'maize', 'zea mays'],
    'Banana': ['banana', 'musa'],
    'Coffee': ['coffee', 'coffea'],
    'Sugar cane': ['sugar cane', 'sugarcane', 'saccharum']
}

crop_nematode_data = []
for crop, keywords in crop_keywords.items():
    pattern = '|'.join(keywords)
    for genus in df['Genus'].unique():
        genus_data = df[df['Genus'] == genus]
        mentions = genus_data['abstract'].str.contains(pattern, case=False, na=False).sum()
        if mentions > 0:
            citations = genus_data[genus_data['abstract'].str.contains(pattern, case=False, na=False)]['citations'].sum()
            crop_nematode_data.append({
                'Crop': crop,
                'Genus': genus,
                'Mentions': mentions,
                'Total_Citations': citations
            })

crop_nem_df = pd.DataFrame(crop_nematode_data)
crop_nem_df = crop_nem_df.sort_values('Mentions', ascending=False)
crop_nem_df.to_csv(f'{TABLES_PATH}/crop_nematode_associations.csv', index=False)

# Economic impact keywords
impact_keywords = {
    'Yield loss': ['yield loss', 'yield reduction', 'crop loss'],
    'Economic damage': ['economic', 'damage', 'loss'],
    'Control cost': ['control', 'management cost', 'treatment'],
    'Resistance': ['resistant', 'resistance']
}

impact_trends = []
for year in range(1990, 2024):
    year_data = df[df['pub_year'] == year]
    for impact_type, keywords in impact_keywords.items():
        pattern = '|'.join(keywords)
        count = year_data['abstract'].str.contains(pattern, case=False, na=False).sum()
        impact_trends.append({'Year': year, 'Impact_Type': impact_type, 'Count': count})

impact_df = pd.DataFrame(impact_trends)
impact_df.to_csv(f'{TABLES_PATH}/economic_impact_trends.csv', index=False)

print(f"   ✓ Crop-nematode associations: {len(crop_nem_df)}")

# FIGURE 1: Crop-Nematode Patterns
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1a: Top crop-nematode pairs
ax = axes[0, 0]
top_pairs = crop_nem_df.nlargest(20, 'Mentions')
ax.barh(range(len(top_pairs)), top_pairs['Mentions'],
       color=NEMATODE_COLORS['accent3'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_pairs)))
ax.set_yticklabels([f"{row['Crop']} - {row['Genus']}" for _, row in top_pairs.iterrows()], fontsize=8)
ax.set_xlabel('Number of Mentions')
ax.set_title('A. Top 20 Crop-Nematode Associations', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 1b: Crop research intensity
ax = axes[0, 1]
crop_totals = crop_nem_df.groupby('Crop')['Mentions'].sum().sort_values(ascending=False)
ax.pie(crop_totals.values, labels=crop_totals.index, autopct='%1.1f%%',
      colors=EXTENDED_PALETTE[:len(crop_totals)], startangle=90)
ax.set_title('B. Research Distribution by Crop', fontweight='bold', loc='left')

# 1c: Nematode specificity
ax = axes[1, 0]
genus_crops = crop_nem_df.groupby('Genus')['Crop'].nunique().sort_values(ascending=False).head(15)
colors = [GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in genus_crops.index]
ax.barh(range(len(genus_crops)), genus_crops.values, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(genus_crops)))
ax.set_yticklabels(genus_crops.index)
ax.set_xlabel('Number of Crops Affected')
ax.set_title('C. Nematode Host Range (Top 15)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 1d: Heatmap of top interactions
ax = axes[1, 1]
top_crops = crop_nem_df.groupby('Crop')['Mentions'].sum().nlargest(8).index
top_genera = crop_nem_df.groupby('Genus')['Mentions'].sum().nlargest(8).index
heatmap_data = crop_nem_df[(crop_nem_df['Crop'].isin(top_crops)) &
                           (crop_nem_df['Genus'].isin(top_genera))]
heatmap_pivot = heatmap_data.pivot_table(index='Genus', columns='Crop', values='Mentions', fill_value=0)
sns.heatmap(heatmap_pivot, annot=True, fmt='g', cmap='YlOrRd', ax=ax,
           cbar_kws={'label': 'Mentions'}, linewidths=0.5)
ax.set_title('D. Crop-Nematode Interaction Matrix', fontweight='bold', loc='left')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig1_Crop_Nematode_Patterns.png')
plt.close()

# FIGURE 2: Economic Impact Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2a: Economic impact trends
ax = axes[0, 0]
for impact_type in impact_keywords.keys():
    data = impact_df[impact_df['Impact_Type'] == impact_type]
    ax.plot(data['Year'], data['Count'], 'o-', label=impact_type, linewidth=2, markersize=3)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('A. Economic Impact Research Trends', fontweight='bold', loc='left')
ax.legend()
ax.grid(True, alpha=0.3)

# 2b: Climate-related keywords
ax = axes[0, 1]
climate_keywords = ['climate', 'temperature', 'warming', 'drought', 'rain']
climate_trends = []
for year in range(2000, 2024):
    year_data = df[df['pub_year'] == year]
    for keyword in climate_keywords:
        count = year_data['abstract'].str.contains(keyword, case=False, na=False).sum()
        climate_trends.append({'Year': year, 'Keyword': keyword, 'Count': count})

climate_df = pd.DataFrame(climate_trends)
for keyword in climate_keywords:
    data = climate_df[climate_df['Keyword'] == keyword]
    ax.plot(data['Year'], data['Count'], 'o-', label=keyword.capitalize(), linewidth=2, markersize=3)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('B. Climate-Related Research Trends', fontweight='bold', loc='left')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# 2c: Research investment proxy (publications by top countries)
ax = axes[1, 0]
top_countries_econ = df[df['country_clean'].notna()].groupby('country_clean').size().nlargest(10)
ax.bar(range(len(top_countries_econ)), top_countries_econ.values,
      color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(top_countries_econ)))
ax.set_xticklabels(top_countries_econ.index, rotation=45, ha='right')
ax.set_ylabel('Research Investment (Publications)')
ax.set_title('C. Research Investment by Country', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='y')

# 2d: High-value crop focus
ax = axes[1, 1]
high_value_crops = ['Coffee', 'Banana', 'Cotton', 'Sugar cane']
high_value_data = crop_nem_df[crop_nem_df['Crop'].isin(high_value_crops)]
value_by_year = []
for year in range(2000, 2024):
    year_df = df[df['pub_year'] == year]
    pattern = '|'.join([kw for crop in high_value_crops for kw in crop_keywords[crop]])
    count = year_df['abstract'].str.contains(pattern, case=False, na=False).sum()
    value_by_year.append({'Year': year, 'Count': count})

value_trend_df = pd.DataFrame(value_by_year)
ax.plot(value_trend_df['Year'], value_trend_df['Count'],
       'o-', color=NEMATODE_COLORS['accent2'], linewidth=2, markersize=4)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('D. High-Value Crop Research Trends', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig2_Economic_Impact_Analysis.png')
plt.close()

print("\n[Part 6 Complete]")
print("="*70)
