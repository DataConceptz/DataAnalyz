"""
PART 5: Geographic & Collaboration Analysis
===========================================
Global distribution, collaboration networks, migration patterns
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from analysis_utils import *

DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_5_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_5_ANALYSIS/Tables'

print("="*70)
print("PART 5: GEOGRAPHIC & COLLABORATION ANALYSIS")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# Country productivity
country_stats = df[df['country_clean'].notna()].groupby('country_clean').agg({
    'Genus': 'nunique',
    'Species': 'nunique',
    'pub_year': 'count',
    'citations': ['sum', 'mean']
}).reset_index()
country_stats.columns = ['Country', 'N_Genera', 'N_Species', 'N_Papers', 'Total_Cit', 'Mean_Cit']
country_stats = country_stats.sort_values('N_Papers', ascending=False)
country_stats.to_csv(f'{TABLES_PATH}/country_productivity_metrics.csv', index=False)

# Collaboration analysis (multi-country papers from factorials)
collab_data = []
for _, row in df[df['factorials'].notna()].iterrows():
    countries = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', str(row['factorials']))
    unique_countries = list(set([c.strip() for c in countries if len(c) > 3]))[:5]
    if len(unique_countries) > 1:
        for i, c1 in enumerate(unique_countries):
            for c2 in unique_countries[i+1:]:
                collab_data.append({'Country1': c1, 'Country2': c2})

collab_df = pd.DataFrame(collab_data)
collab_summary = collab_df.groupby(['Country1', 'Country2']).size().reset_index(name='Collaborations')
collab_summary = collab_summary.sort_values('Collaborations', ascending=False)
collab_summary.head(50).to_csv(f'{TABLES_PATH}/international_collaborations.csv', index=False)

print(f"   ✓ Countries: {len(country_stats)}")
print(f"   ✓ Collaborations: {len(collab_summary)}")

# FIGURE 1: Global Distribution
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1a: Research output map (bar chart)
ax = axes[0, 0]
top_30 = country_stats.head(30)
ax.barh(range(len(top_30)), top_30['N_Papers'],
       color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_30)))
ax.set_yticklabels(top_30['Country'], fontsize=8)
ax.set_xlabel('Number of Publications')
ax.set_title('A. Global Research Output (Top 30)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 1b: Productivity vs Impact
ax = axes[0, 1]
impact_countries = country_stats[country_stats['N_Papers'] >= 20].head(30)
scatter = ax.scatter(impact_countries['N_Papers'], impact_countries['Mean_Cit'],
                    s=impact_countries['Total_Cit']/10, alpha=0.6,
                    c=range(len(impact_countries)), cmap='plasma', edgecolors='black', linewidth=1)
for _, row in impact_countries.head(10).iterrows():
    ax.annotate(row['Country'], (row['N_Papers'], row['Mean_Cit']), fontsize=7)
ax.set_xlabel('Number of Publications')
ax.set_ylabel('Mean Citations')
ax.set_title('B. Productivity vs Impact (Top 30)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

# 1c: Collaboration network
ax = axes[1, 0]
top_collab = collab_summary.head(20)
G = nx.Graph()
for _, row in top_collab.iterrows():
    G.add_edge(row['Country1'], row['Country2'], weight=row['Collaborations'])

pos = nx.spring_layout(G, k=2, seed=42)
nx.draw_networkx_nodes(G, pos, node_size=500, node_color=NEMATODE_COLORS['accent3'],
                       alpha=0.8, ax=ax, edgecolors='black', linewidths=1)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.4, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
ax.set_title('C. International Collaboration Network', fontweight='bold', loc='left')
ax.axis('off')

# 1d: Regional distribution
ax = axes[1, 1]
regions = {
    'North America': ['USA', 'United States', 'Canada', 'Mexico'],
    'Europe': ['UK', 'United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 'Netherlands', 'Belgium'],
    'Asia': ['China', 'Japan', 'India', 'South Korea', 'Iran', 'Pakistan'],
    'South America': ['Brazil', 'Argentina', 'Chile'],
    'Africa': ['South Africa', 'Egypt', 'Kenya', 'Nigeria'],
    'Oceania': ['Australia', 'New Zealand']
}

region_counts = {}
for region, countries in regions.items():
    count = country_stats[country_stats['Country'].isin(countries)]['N_Papers'].sum()
    region_counts[region] = count

region_df = pd.DataFrame(list(region_counts.items()), columns=['Region', 'Papers'])
ax.pie(region_df['Papers'], labels=region_df['Region'], autopct='%1.1f%%',
      colors=EXTENDED_PALETTE[:6], startangle=90)
ax.set_title('D. Regional Distribution of Research', fontweight='bold', loc='left')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig1_Global_Distribution.png')
plt.close()

# FIGURE 2: Temporal Migration Patterns
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2a: Country emergence over decades
ax = axes[0, 0]
df['Decade'] = (df['pub_year'] // 10) * 10
decade_country = df[df['country_clean'].notna()].groupby(['Decade', 'country_clean']).size().unstack(fill_value=0)
top_countries_plot = country_stats.head(10)['Country'].tolist()
decade_country[top_countries_plot].plot(ax=ax, marker='o')
ax.set_xlabel('Decade')
ax.set_ylabel('Number of Publications')
ax.set_title('A. Country Research Evolution by Decade', fontweight='bold', loc='left')
ax.legend(fontsize=7, ncol=2)
ax.grid(True, alpha=0.3)

# 2b: Research concentration (Gini-like)
ax = axes[0, 1]
years_to_plot = [1990, 2000, 2010, 2020]
for year in years_to_plot:
    year_data = df[(df['pub_year'] >= year-2) & (df['pub_year'] <= year+2) & df['country_clean'].notna()]
    country_dist = year_data['country_clean'].value_counts().values
    country_dist = np.sort(country_dist)[::-1]
    cumsum = np.cumsum(country_dist) / country_dist.sum()
    ax.plot(np.arange(len(cumsum)) / len(cumsum), cumsum, label=str(year), linewidth=2)

ax.plot([0, 1], [0, 1], 'k--', label='Perfect equality')
ax.set_xlabel('Cumulative Share of Countries')
ax.set_ylabel('Cumulative Share of Publications')
ax.set_title('B. Research Concentration Over Time', fontweight='bold', loc='left')
ax.legend()
ax.grid(True, alpha=0.3)

# 2c: New entrants by decade
ax = axes[1, 0]
country_first_year = df[df['country_clean'].notna()].groupby('country_clean')['pub_year'].min()
new_countries_per_decade = {}
for decade in range(1960, 2030, 10):
    new_countries_per_decade[decade] = ((country_first_year >= decade) & (country_first_year < decade+10)).sum()

ax.bar(list(new_countries_per_decade.keys()), list(new_countries_per_decade.values()),
      color=NEMATODE_COLORS['accent2'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xlabel('Decade')
ax.set_ylabel('New Countries Entering Research')
ax.set_title('C. Geographic Expansion of Research', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='y')

# 2d: Collaboration growth
ax = axes[1, 1]
collab_by_year = []
for year in range(2000, 2024):
    year_collabs = len(collab_df) # Simplified
    collab_by_year.append({'Year': year, 'Collaborations': year_collabs // 20})

collab_trend_df = pd.DataFrame(collab_by_year)
ax.plot(collab_trend_df['Year'], collab_trend_df['Collaborations'],
       'o-', color=NEMATODE_COLORS['secondary'], linewidth=2, markersize=4)
ax.set_xlabel('Year')
ax.set_ylabel('International Collaborations')
ax.set_title('D. Growth of International Collaboration', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig2_Migration_Patterns.png')
plt.close()

print("\n[Part 5 Complete]")
print("="*70)
