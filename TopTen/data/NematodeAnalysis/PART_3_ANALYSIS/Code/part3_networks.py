"""
PART 3: Citation Networks and Journal Analysis
===============================================
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from analysis_utils import *

DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_3_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_3_ANALYSIS/Tables'

print("\n" + "="*70)
print("PART 3: CITATION NETWORKS & JOURNAL ANALYSIS")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# ============================================================================
# ANALYSIS 3: CROSS-GENUS CITATION PATTERNS
# ============================================================================

print("\n[3] Analyzing cross-genus citation patterns...")

# Create genus co-occurrence in high-citation papers
high_cite_threshold = df['citations'].quantile(0.75)
high_cite_papers = df[df['citations'] >= high_cite_threshold]

# Group by paper (using title as proxy)
genus_cooccurrence = high_cite_papers.groupby('title')['Genus'].apply(list).reset_index()

# Build co-occurrence matrix
from collections import defaultdict
cooccur_dict = defaultdict(int)

for genera_list in genus_cooccurrence['Genus']:
    unique_genera = list(set(genera_list))
    for i, g1 in enumerate(unique_genera):
        for g2 in unique_genera[i+1:]:
            pair = tuple(sorted([g1, g2]))
            cooccur_dict[pair] += 1

# Create co-occurrence dataframe
cooccur_data = []
for (g1, g2), count in cooccur_dict.items():
    cooccur_data.append({'Genus1': g1, 'Genus2': g2, 'Cooccurrences': count})
cooccur_df = pd.DataFrame(cooccur_data).sort_values('Cooccurrences', ascending=False)
cooccur_df.to_csv(f'{TABLES_PATH}/genus_cooccurrence_patterns.csv', index=False)

print(f"   ✓ Genus pairs identified: {len(cooccur_df):,}")

# Citation transfer analysis (genus to genus)
genus_cite_stats = df.groupby('Genus').agg({
    'citations': ['mean', 'sum', 'count']
}).reset_index()
genus_cite_stats.columns = ['Genus', 'Mean_Cit', 'Total_Cit', 'N_Papers']
genus_cite_stats.to_csv(f'{TABLES_PATH}/genus_citation_statistics.csv', index=False)

# FIGURE 3: Citation Networks
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# 3a: Co-occurrence network
ax = axes[0]
top_pairs = cooccur_df.head(30)
G = nx.Graph()
for _, row in top_pairs.iterrows():
    G.add_edge(row['Genus1'], row['Genus2'], weight=row['Cooccurrences'])

pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
node_sizes = [genus_cite_stats[genus_cite_stats['Genus']==n]['N_Papers'].values[0]*10
             if n in genus_cite_stats['Genus'].values else 100 for n in G.nodes()]
node_colors = [GENUS_COLORS.get(n, NEMATODE_COLORS['neutral1']) for n in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors,
                       alpha=0.8, ax=ax, edgecolors='black', linewidths=1)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.4, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)

ax.set_title('A. Genus Co-occurrence Network (High-Impact Papers)', fontweight='bold', loc='left')
ax.axis('off')

# 3b: Citation flow heatmap
ax = axes[1]
top_genera = genus_cite_stats.nlargest(12, 'Total_Cit')['Genus'].tolist()
cite_matrix = pd.DataFrame(0, index=top_genera, columns=top_genera)

for g1 in top_genera:
    for g2 in top_genera:
        if g1 != g2:
            pair = tuple(sorted([g1, g2]))
            cite_matrix.loc[g1, g2] = cooccur_dict.get(pair, 0)

sns.heatmap(cite_matrix, annot=True, fmt='g', cmap='YlOrRd', ax=ax,
           cbar_kws={'label': 'Co-occurrences'}, linewidths=0.5)
ax.set_title('B. Citation Cross-Reference Matrix (Top 12 Genera)', fontweight='bold', loc='left')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig3_Citation_Networks.png')
plt.close()

# ============================================================================
# ANALYSIS 4: JOURNAL IMPACT ANALYSIS
# ============================================================================

print("\n[4] Analyzing journal impact and patterns...")

journal_stats = df.groupby('journal').agg({
    'citations': ['count', 'sum', 'mean', 'median'],
    'Genus': lambda x: x.nunique(),
    'pub_year': ['min', 'max']
}).reset_index()
journal_stats.columns = ['_'.join(col).strip('_') for col in journal_stats.columns]
journal_stats.columns = ['Journal', 'N_Papers', 'Total_Citations', 'Mean_Citations',
                         'Median_Citations', 'N_Genera', 'First_Year', 'Last_Year']
journal_stats['Years_Publishing'] = journal_stats['Last_Year'] - journal_stats['First_Year']
journal_stats = journal_stats.sort_values('Total_Citations', ascending=False)
journal_stats.head(50).to_csv(f'{TABLES_PATH}/top_50_journals.csv', index=False)

print(f"   ✓ Journals analyzed: {len(journal_stats):,}")
print(f"   ✓ Top journal: {journal_stats.iloc[0]['Journal']}")

# FIGURE 4: Journal Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 4a: Top journals by citations
ax = axes[0, 0]
top_journals = journal_stats.nlargest(15, 'Total_Citations')
ax.barh(range(len(top_journals)), top_journals['Total_Citations'],
       color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_journals)))
ax.set_yticklabels([j[:40] + '...' if len(j) > 40 else j for j in top_journals['Journal']], fontsize=8)
ax.set_xlabel('Total Citations')
ax.set_title('A. Top Journals by Total Citations', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 4b: Journal quality (mean citations vs papers)
ax = axes[0, 1]
qual_journals = journal_stats[journal_stats['N_Papers'] >= 10].nlargest(30, 'Mean_Citations')
scatter = ax.scatter(qual_journals['N_Papers'], qual_journals['Mean_Citations'],
                    s=qual_journals['Total_Citations']/5, alpha=0.6,
                    c=range(len(qual_journals)), cmap='viridis', edgecolors='black', linewidth=1)
ax.set_xlabel('Number of Papers')
ax.set_ylabel('Mean Citations per Paper')
ax.set_title('B. Journal Quality vs Quantity', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

# 4c: Citation distribution by top journals
ax = axes[1, 0]
top_5_journals = journal_stats.nlargest(5, 'N_Papers')['Journal'].tolist()
journal_cite_data = []
for journal in top_5_journals:
    cites = df[df['journal'] == journal]['citations'].values
    journal_cite_data.append(cites)

bp = ax.boxplot(journal_cite_data, labels=[j[:20] + '...' if len(j) > 20 else j for j in top_5_journals],
               patch_artist=True)
for patch, color in zip(bp['boxes'], EXTENDED_PALETTE[:5]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_ylabel('Citations')
ax.set_title('C. Citation Distribution (Top 5 Journals)', fontweight='bold', loc='left')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3, axis='y')

# 4d: Journal longevity
ax = axes[1, 1]
active_journals = journal_stats[journal_stats['Years_Publishing'] >= 1]
longevity_bins = [0, 5, 10, 15, 20, 50]
active_journals['Longevity_Bin'] = pd.cut(active_journals['Years_Publishing'],
                                          bins=longevity_bins,
                                          labels=['1-5yr', '6-10yr', '11-15yr', '16-20yr', '20+yr'])
long_dist = active_journals['Longevity_Bin'].value_counts().sort_index()
ax.bar(range(len(long_dist)), long_dist.values,
      color=NEMATODE_COLORS['accent3'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(long_dist)))
ax.set_xticklabels(long_dist.index)
ax.set_ylabel('Number of Journals')
ax.set_title('D. Journal Longevity Distribution', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig4_Journal_Analysis.png')
plt.close()

# FIGURE 5: Temporal Citation Trends
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 5a: Citations by publication year
ax = axes[0, 0]
year_cites = df.groupby('pub_year').agg({
    'citations': ['mean', 'sum', 'count']
}).reset_index()
year_cites.columns = ['Year', 'Mean_Cit', 'Total_Cit', 'N_Papers']

ax.plot(year_cites['Year'], year_cites['Mean_Cit'],
       'o-', color=NEMATODE_COLORS['primary'], linewidth=2, markersize=4)
ax.set_xlabel('Publication Year')
ax.set_ylabel('Mean Citations')
ax.set_title('A. Mean Citations by Publication Year', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

# 5b: High-impact paper trends
ax = axes[0, 1]
high_impact_year = df[df['citations'] >= df['citations'].quantile(0.90)].groupby('pub_year').size()
ax.bar(high_impact_year.index, high_impact_year.values,
      color=NEMATODE_COLORS['accent2'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xlabel('Publication Year')
ax.set_ylabel('Number of High-Impact Papers')
ax.set_title('B. High-Impact Papers Over Time (Top 10%)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='y')

# 5c: Impact factor vs recency
ax = axes[1, 0]
recent_papers = df[df['pub_year'] >= 2010]
old_papers = df[df['pub_year'] < 2010]
data_to_plot = [old_papers['citations'].values, recent_papers['citations'].values]
bp = ax.boxplot(data_to_plot, labels=['Before 2010', '2010-2023'], patch_artist=True)
bp['boxes'][0].set_facecolor(NEMATODE_COLORS['neutral1'])
bp['boxes'][1].set_facecolor(NEMATODE_COLORS['accent1'])
for box in bp['boxes']:
    box.set_alpha(0.7)
ax.set_ylabel('Citations')
ax.set_title('C. Citation Impact: Historical vs Recent', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='y')

# 5d: Citation accumulation rate
ax = axes[1, 1]
top_genera = df.groupby('Genus')['citations'].sum().nlargest(6).index
for genus in top_genera:
    genus_year = df[df['Genus'] == genus].groupby('pub_year')['citations'].mean()
    color = GENUS_COLORS.get(genus, NEMATODE_COLORS['neutral1'])
    ax.plot(genus_year.index, genus_year.values, 'o-',
           label=genus, color=color, linewidth=2, markersize=3)
ax.set_xlabel('Year')
ax.set_ylabel('Mean Citations')
ax.set_title('D. Citation Trends by Top Genera', fontweight='bold', loc='left')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig5_Temporal_Citation_Trends.png')
plt.close()

print("\n[Part 3 Complete]")
print("="*70)
print(f"✓ Charts: {CHARTS_PATH}/")
print(f"✓ Tables: {TABLES_PATH}/")
print("\nGenerated:")
print("  - Fig1_Citation_Impact_Analysis.png")
print("  - Fig2_Author_Analysis.png")
print("  - Fig3_Citation_Networks.png")
print("  - Fig4_Journal_Analysis.png")
print("  - Fig5_Temporal_Citation_Trends.png")
