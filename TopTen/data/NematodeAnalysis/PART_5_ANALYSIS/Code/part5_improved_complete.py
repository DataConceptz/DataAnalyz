"""
PART 5: Geographic & Collaboration Analysis - IMPROVED 6X
Nature-Quality Publication Standards

Focused analysis including:
1. Global research distribution
2. International collaboration networks
3. Country productivity metrics

Each figure is professionally designed for Nature publication
"""

import sys
sys.path.append('/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from analysis_utils_improved import *
import re

# Configuration
DATA_FILE = '/home/user/DataAnalyz/TopTen/data/Final_Nema_Data.xlsx'
OUTPUT_DIR = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_5_ANALYSIS'

print("\n" + "="*70)
print("PART 5: GEOGRAPHIC & COLLABORATION ANALYSIS - IMPROVED VERSION")
print("="*70 + "\n")

# Load data
print("Loading data...")
df = pd.read_excel(DATA_FILE, engine='openpyxl')
print(f"✓ Loaded {len(df):,} records")

# Standardize column names
df = df.rename(columns={
    'PubYear': 'pub_year',
    'Times cited': 'citations',
    'Country': 'country',
    'Country of standardized research organization': 'org_country',
})

# Basic cleaning
df['pub_year'] = pd.to_numeric(df['pub_year'], errors='coerce')
df = df.dropna(subset=['pub_year'])
df['pub_year'] = df['pub_year'].astype(int)
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)

# Apply filters
df_clean = apply_analysis_filters(df)

print(f"\nDataset after filtering: {len(df_clean):,} records")

# ============================================================================
# FIGURE 1: Global Research Distribution (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 1: Global Research Distribution")
print("="*70)

# Use org_country if available, otherwise country
country_col = 'org_country' if 'org_country' in df_clean.columns else 'country'
df_countries = df_clean[df_clean[country_col].notna()].copy()

if len(df_countries) > 0:
    country_stats = df_countries.groupby(country_col).agg({
        'Genus': 'nunique',
        'Species': 'nunique',
        'pub_year': 'count',
        'citations': ['mean', 'sum']
    }).reset_index()
    country_stats.columns = ['Country', 'N_Genera', 'N_Species', 'N_Publications',
                            'Mean_Citations', 'Total_Citations']

    # Calculate research efficiency
    country_stats['Citations_Per_Paper'] = country_stats['Total_Citations'] / country_stats['N_Publications']

    # Focus on top 30 countries
    top30_countries = country_stats.nlargest(30, 'N_Publications')

    # Create figure with 2 panels
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # LEFT: Top countries by publications
    y_pos = np.arange(len(top30_countries))
    colors_gradient = plt.cm.viridis(np.linspace(0.2, 0.9, len(top30_countries)))

    ax1.barh(y_pos, top30_countries['N_Publications'],
            color=colors_gradient, edgecolor='black', linewidth=0.5)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(top30_countries['Country'], fontsize=8)
    ax1.set_xlabel('Number of Publications', fontweight='bold')
    ax1.set_title('A. Top 30 Countries by Publication Output',
                 fontweight='bold', loc='left')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='x', alpha=0.3)

    # RIGHT: Research efficiency (top 20 by citations per paper)
    top20_efficient = country_stats[country_stats['N_Publications'] >= 10].nlargest(20, 'Citations_Per_Paper')
    y_pos = np.arange(len(top20_efficient))
    colors_heat = plt.cm.plasma(np.linspace(0.2, 0.9, len(top20_efficient)))

    ax2.barh(y_pos, top20_efficient['Citations_Per_Paper'],
            color=colors_heat, edgecolor='black', linewidth=0.5)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(top20_efficient['Country'], fontsize=8)
    ax2.set_xlabel('Mean Citations per Paper', fontweight='bold')
    ax2.set_title('B. Research Impact Efficiency (≥10 papers)',
                 fontweight='bold', loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig1_Global_Research_Distribution.png')
    plt.close()

    # Save data
    country_stats.to_csv(f'{OUTPUT_DIR}/Tables/Table1_Country_Statistics.csv', index=False)
    print(f"✓ Analyzed {len(country_stats)} countries")

# ============================================================================
# FIGURE 2: Country Collaboration Network (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 2: International Collaboration Network")
print("="*70)

# Extract multi-country papers
# Parse country field to find collaborations
collaboration_pairs = []

for _, row in df_countries.iterrows():
    countries_str = str(row[country_col])
    # Split by common separators
    countries = re.split(r'[;,|]', countries_str)
    countries = [c.strip() for c in countries if c.strip() and c.strip() != 'nan']

    # Create pairs for multi-country papers
    if len(countries) > 1:
        countries = list(set(countries))[:5]  # Max 5 countries per paper
        for i in range(len(countries)):
            for j in range(i+1, len(countries)):
                collaboration_pairs.append({
                    'Country1': countries[i],
                    'Country2': countries[j],
                    'Year': row['pub_year']
                })

if len(collaboration_pairs) > 0:
    df_collab = pd.DataFrame(collaboration_pairs)

    # Count collaboration frequency
    collab_counts = df_collab.groupby(['Country1', 'Country2']).size().reset_index(name='Count')
    collab_counts = collab_counts[collab_counts['Count'] >= 3]  # At least 3 collaborations

    # Get top collaborating countries
    top_countries_collab = set()
    for _, row in collab_counts.nlargest(50, 'Count').iterrows():
        top_countries_collab.add(row['Country1'])
        top_countries_collab.add(row['Country2'])

    # Filter to top countries
    collab_counts_filtered = collab_counts[
        collab_counts['Country1'].isin(top_countries_collab) &
        collab_counts['Country2'].isin(top_countries_collab)
    ]

    # Create network
    G = nx.Graph()

    for _, row in collab_counts_filtered.iterrows():
        G.add_edge(row['Country1'], row['Country2'], weight=row['Count'])

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # LEFT: Network visualization
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Node sizes based on degree
    node_sizes = [300 * G.degree(n) for n in G.nodes()]

    # Draw network
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                          node_color='#1f77b4', alpha=0.7,
                          edgecolors='black', linewidths=1.5, ax=ax1)

    # Edge widths based on collaboration count
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    widths = [1 + 4 * (w / max_weight) for w in weights]

    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.3, ax=ax1)

    # Labels
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold', ax=ax1)

    ax1.set_title('A. International Collaboration Network',
                 fontweight='bold', pad=10)
    ax1.axis('off')

    # RIGHT: Top collaboration pairs
    top20_pairs = collab_counts.nlargest(20, 'Count')
    top20_pairs['Pair'] = top20_pairs['Country1'] + ' - ' + top20_pairs['Country2']

    y_pos = np.arange(len(top20_pairs))
    colors_collab = plt.cm.coolwarm(np.linspace(0.3, 0.9, len(top20_pairs)))

    ax2.barh(y_pos, top20_pairs['Count'], color=colors_collab,
            edgecolor='black', linewidth=0.5)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(top20_pairs['Pair'], fontsize=8)
    ax2.set_xlabel('Number of Collaborative Publications', fontweight='bold')
    ax2.set_title('B. Top 20 Collaboration Pairs',
                 fontweight='bold', loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig2_Collaboration_Network.png')
    plt.close()

    # Save data
    collab_counts.to_csv(f'{OUTPUT_DIR}/Tables/Table2_Collaboration_Pairs.csv', index=False)
    print(f"✓ Identified {len(collab_counts):,} collaboration pairs")
else:
    print("⚠ No collaboration data found")

# ============================================================================
# FIGURE 3: Temporal Evolution of Research by Region (NEW)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 3: Regional Research Trends")
print("="*70)

# Define regions
regions = {
    'North America': ['USA', 'United States', 'Canada', 'Mexico'],
    'Europe': ['UK', 'United Kingdom', 'Germany', 'France', 'Italy', 'Spain',
              'Netherlands', 'Belgium', 'Poland', 'Sweden', 'Denmark'],
    'Asia': ['China', 'Japan', 'India', 'Korea', 'South Korea', 'Thailand',
            'Vietnam', 'Taiwan', 'Pakistan', 'Iran'],
    'South America': ['Brazil', 'Argentina', 'Chile', 'Colombia'],
    'Africa': ['Egypt', 'South Africa', 'Kenya', 'Nigeria'],
    'Oceania': ['Australia', 'New Zealand']
}

# Assign regions
def assign_region(country):
    if pd.isna(country):
        return 'Unknown'
    country_str = str(country)
    for region, countries in regions.items():
        if any(c.lower() in country_str.lower() for c in countries):
            return region
    return 'Other'

df_countries['Region'] = df_countries[country_col].apply(assign_region)

# Calculate publications by region and year
region_trends = df_countries.groupby(['pub_year', 'Region']).size().reset_index(name='Count')

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

region_colors = {
    'North America': '#1f77b4',
    'Europe': '#2ca02c',
    'Asia': '#d62728',
    'South America': '#ff7f0e',
    'Africa': '#9467bd',
    'Oceania': '#8c564b'
}

for region in ['North America', 'Europe', 'Asia', 'South America', 'Oceania', 'Africa']:
    region_data = region_trends[region_trends['Region'] == region]
    if len(region_data) > 0:
        region_data = region_data.sort_values('pub_year')
        # Apply smoothing
        region_data['MA_3yr'] = region_data['Count'].rolling(window=3, center=True).mean()

        ax.plot(region_data['pub_year'], region_data['MA_3yr'],
               linewidth=2.5, label=region, color=region_colors.get(region, 'gray'),
               alpha=0.8, marker='o', markersize=3, markevery=5)

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Number of Publications (3-year MA)', fontweight='bold')
ax.set_title('Temporal Evolution of Research by Geographic Region (1960-2023)',
            fontweight='bold', pad=15)
ax.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig3_Regional_Trends.png')
plt.close()

print("✓ Analyzed regional research trends")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("PART 5 ANALYSIS COMPLETE - IMPROVED VERSION")
print("="*70)
print("\nGenerated Figures:")
print("  ✓ Fig1: Global Research Distribution (2-panel)")
print("  ✓ Fig2: International Collaboration Network (2-panel)")
print("  ✓ Fig3: Regional Research Trends (line plot)")
print("\nAll figures saved in Nature-quality format (600 DPI)")
print("="*70 + "\n")
