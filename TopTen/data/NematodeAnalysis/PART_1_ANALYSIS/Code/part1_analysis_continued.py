"""
PART 1: Species & Taxonomic Analysis (Continued)
=================================================

Analyses 3-5:
- Host-parasite relationship network
- Geographic distribution patterns
- Research bias analysis
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from collections import Counter
from analysis_utils import *
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Tables'

# Load data
print("\n" + "="*70)
print("CONTINUING PART 1 ANALYSIS...")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# ============================================================================
# ANALYSIS 3: HOST-PARASITE RELATIONSHIP NETWORK
# ============================================================================

print("\n[4] Extracting host-parasite relationships from abstracts...")

# Extract host plants from abstracts
df['host_plants'] = df['abstract'].apply(extract_host_plants)

# Create host-parasite pairs
host_parasite_pairs = []
for idx, row in df.iterrows():
    if row['host_plants']:
        for host in row['host_plants']:
            host_parasite_pairs.append({
                'Genus': row['Genus'],
                'Species': row['Species'],
                'Host': host,
                'Citations': row['citations']
            })

hp_df = pd.DataFrame(host_parasite_pairs)

if len(hp_df) > 0:
    # Aggregate relationships
    host_parasite_summary = hp_df.groupby(['Genus', 'Host']).agg({
        'Species': 'count',
        'Citations': 'mean'
    }).reset_index()
    host_parasite_summary.columns = ['Genus', 'Host', 'N_Mentions', 'Avg_Citations']
    host_parasite_summary = host_parasite_summary.sort_values('N_Mentions', ascending=False)

    # Save table
    host_parasite_summary.to_csv(f'{TABLES_PATH}/host_parasite_relationships.csv', index=False)
    print(f"   ✓ Extracted {len(hp_df):,} host-parasite relationships")
    print(f"   ✓ Saved: host_parasite_relationships.csv")

    # FIGURE 3: Host-Parasite Network
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # 3a: Top host plants
    ax = axes[0]
    top_hosts = hp_df['Host'].value_counts().head(20)
    ax.barh(range(len(top_hosts)), top_hosts.values,
           color=NEMATODE_COLORS['accent3'], alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.set_yticks(range(len(top_hosts)))
    ax.set_yticklabels([h.capitalize() for h in top_hosts.index], fontsize=9)
    ax.set_xlabel('Number of Nematode-Host Associations')
    ax.set_title('A. Most Frequently Mentioned Host Plants', fontweight='bold', loc='left')
    ax.grid(True, alpha=0.3, axis='x')

    # 3b: Network visualization (top relationships only)
    ax = axes[1]
    # Filter to top genera and hosts for visualization
    top_genera = hp_df['Genus'].value_counts().head(8).index
    top_hosts_list = hp_df['Host'].value_counts().head(15).index

    hp_filtered = hp_df[hp_df['Genus'].isin(top_genera) & hp_df['Host'].isin(top_hosts_list)]

    # Create network
    G = nx.Graph()
    for idx, row in hp_filtered.iterrows():
        G.add_edge(row['Genus'], row['Host'], weight=1)

    # Position nodes
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Draw network
    genera_nodes = [n for n in G.nodes() if n in top_genera]
    host_nodes = [n for n in G.nodes() if n not in top_genera]

    nx.draw_networkx_nodes(G, pos, nodelist=genera_nodes,
                          node_color=[GENUS_COLORS.get(g, NEMATODE_COLORS['primary']) for g in genera_nodes],
                          node_size=800, alpha=0.9, ax=ax, label='Nematode Genera')
    nx.draw_networkx_nodes(G, pos, nodelist=host_nodes,
                          node_color=NEMATODE_COLORS['accent3'],
                          node_size=500, alpha=0.7, ax=ax, node_shape='s', label='Host Plants')
    nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.3, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)

    ax.set_title('B. Host-Parasite Network (Top 8 Genera, 15 Hosts)', fontweight='bold', loc='left')
    ax.legend(loc='upper right')
    ax.axis('off')

    plt.tight_layout()
    save_figure(fig, f'{CHARTS_PATH}/Fig3_Host_Parasite_Network.png')
    plt.close()

else:
    print("   ⚠ No host-parasite relationships extracted")

# ============================================================================
# ANALYSIS 4: GEOGRAPHIC DISTRIBUTION PATTERNS
# ============================================================================

print("\n[5] Analyzing geographic distribution patterns...")

# Country-Genus analysis
country_genus = df.groupby(['country_clean', 'Genus']).agg({
    'pub_year': 'count',
    'count_numeric': 'sum',
    'citations': 'sum'
}).reset_index()
country_genus.columns = ['Country', 'Genus', 'N_Publications', 'Total_Mentions', 'Total_Citations']
country_genus = country_genus[country_genus['Country'].notna()]

# Save table
country_genus_wide = country_genus.pivot_table(
    index='Country',
    columns='Genus',
    values='N_Publications',
    fill_value=0
)
country_genus_wide.to_csv(f'{TABLES_PATH}/geographic_distribution_by_genus.csv')
print(f"   ✓ Saved: geographic_distribution_by_genus.csv")

# Country summary
country_summary = df[df['country_clean'].notna()].groupby('country_clean').agg({
    'Genus': 'nunique',
    'Species': 'nunique',
    'pub_year': 'count',
    'citations': ['sum', 'mean']
}).reset_index()
country_summary.columns = ['Country', 'N_Genera', 'N_Species', 'N_Publications', 'Total_Citations', 'Mean_Citations']
country_summary = country_summary.sort_values('N_Publications', ascending=False)

country_summary.to_csv(f'{TABLES_PATH}/country_research_summary.csv', index=False)
print(f"   ✓ Saved: country_research_summary.csv")

# FIGURE 4: Geographic Distribution
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 4a: Top research countries
ax = axes[0, 0]
top_countries = country_summary.head(20)
ax.barh(range(len(top_countries)), top_countries['N_Publications'],
       color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_countries)))
ax.set_yticklabels(top_countries['Country'], fontsize=9)
ax.set_xlabel('Number of Publications')
ax.set_title('A. Research Output by Country (Top 20)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 4b: Species diversity by country
ax = axes[0, 1]
top_countries_div = country_summary.head(15)
x = np.arange(len(top_countries_div))
width = 0.35

bars1 = ax.bar(x - width/2, top_countries_div['N_Genera'],
              width, label='Genera', color=NEMATODE_COLORS['accent1'], alpha=0.7, edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x + width/2, top_countries_div['N_Species'],
              width, label='Species', color=NEMATODE_COLORS['secondary'], alpha=0.7, edgecolor='black', linewidth=0.5)

ax.set_xlabel('Country')
ax.set_ylabel('Count')
ax.set_title('B. Taxonomic Diversity by Country (Top 15)', fontweight='bold', loc='left')
ax.set_xticks(x)
ax.set_xticklabels(top_countries_div['Country'], rotation=45, ha='right', fontsize=8)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# 4c: Genus distribution heatmap (top 10 countries, top 10 genera)
ax = axes[1, 0]
top10_countries = country_summary.head(10)['Country'].tolist()
top10_genera = df['Genus'].value_counts().head(10).index.tolist()

heatmap_data = country_genus[
    (country_genus['Country'].isin(top10_countries)) &
    (country_genus['Genus'].isin(top10_genera))
].pivot_table(
    index='Country',
    columns='Genus',
    values='N_Publications',
    fill_value=0
)

# Reorder to match top lists
heatmap_data = heatmap_data.reindex(index=top10_countries, columns=top10_genera, fill_value=0)

sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='YlOrRd',
           cbar_kws={'label': 'Publications'}, ax=ax, linewidths=0.5)
ax.set_title('C. Geographic Distribution Heatmap (Top 10×10)', fontweight='bold', loc='left')
ax.set_xlabel('Genus')
ax.set_ylabel('Country')

# 4d: Citation impact by country
ax = axes[1, 1]
top_cit_countries = country_summary.head(15)
scatter = ax.scatter(top_cit_countries['N_Publications'],
                    top_cit_countries['Mean_Citations'],
                    s=top_cit_countries['Total_Citations']/10,
                    c=range(len(top_cit_countries)),
                    cmap='viridis', alpha=0.6, edgecolors='black', linewidth=1)

# Add country labels
for idx, row in top_cit_countries.iterrows():
    ax.annotate(row['Country'], (row['N_Publications'], row['Mean_Citations']),
               fontsize=7, ha='right', va='bottom')

ax.set_xlabel('Number of Publications')
ax.set_ylabel('Mean Citations per Publication')
ax.set_title('D. Research Output vs Citation Impact', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig4_Geographic_Distribution.png')
plt.close()

print("\n[Analysis 3 & 4 Complete]")
print("="*70)
