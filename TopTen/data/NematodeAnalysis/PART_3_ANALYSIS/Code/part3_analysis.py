"""
PART 3: Citation & Impact Analysis
===================================
High-impact papers, citation networks, author identification, journal analysis
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
import re

DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_3_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_3_ANALYSIS/Tables'

print("="*70)
print("PART 3: CITATION & IMPACT ANALYSIS")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# ============================================================================
# ANALYSIS 1: HIGH-IMPACT PAPERS
# ============================================================================

print("\n[1] Identifying high-impact papers...")

# Define impact thresholds
citation_percentiles = df['citations'].quantile([0.5, 0.75, 0.90, 0.95, 0.99])
df['impact_category'] = pd.cut(df['citations'],
    bins=[-np.inf, citation_percentiles[0.5], citation_percentiles[0.75],
          citation_percentiles[0.90], citation_percentiles[0.95], np.inf],
    labels=['Low', 'Medium', 'High', 'Very High', 'Exceptional']
)

# High-impact papers (top 10%)
high_impact = df[df['citations'] >= citation_percentiles[0.90]].copy()
high_impact_summary = high_impact.groupby(['Genus', 'Species']).agg({
    'citations': ['count', 'mean', 'sum', 'max'],
    'pub_year': ['min', 'max']
}).reset_index()
high_impact_summary.columns = ['_'.join(col).strip('_') for col in high_impact_summary.columns]
high_impact_summary.to_csv(f'{TABLES_PATH}/high_impact_papers_summary.csv', index=False)

# Top 50 most cited papers
top_cited = df.nlargest(50, 'citations')[['title', 'Genus', 'Species', 'pub_year',
                                           'citations', 'journal', 'country_clean']]
top_cited.to_csv(f'{TABLES_PATH}/top_50_cited_papers.csv', index=False)

print(f"   ✓ High-impact papers: {len(high_impact):,}")
print(f"   ✓ Citation range (top 10%): {citation_percentiles[0.90]:.0f} - {df['citations'].max():.0f}")

# FIGURE 1: Citation Distribution and Impact
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1a: Citation distribution
ax = axes[0, 0]
bins = np.logspace(0, np.log10(df['citations'].max()+1), 50)
ax.hist(df['citations'], bins=bins, color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xscale('log')
ax.set_xlabel('Citations (log scale)')
ax.set_ylabel('Number of Papers')
ax.set_title('A. Citation Distribution', fontweight='bold', loc='left')
ax.axvline(citation_percentiles[0.90], color='red', linestyle='--', label='90th percentile')
ax.legend()
ax.grid(True, alpha=0.3)

# 1b: Impact categories
ax = axes[0, 1]
impact_counts = df['impact_category'].value_counts()
colors = [NEMATODE_COLORS['neutral1'], NEMATODE_COLORS['accent1'],
          NEMATODE_COLORS['accent3'], NEMATODE_COLORS['secondary'], NEMATODE_COLORS['accent2']]
ax.pie(impact_counts.values, labels=impact_counts.index, autopct='%1.1f%%',
      colors=colors, startangle=90)
ax.set_title('B. Impact Category Distribution', fontweight='bold', loc='left')

# 1c: Citations by genus (top 10)
ax = axes[1, 0]
genus_citations = df.groupby('Genus')['citations'].agg(['mean', 'sum', 'count']).reset_index()
genus_citations = genus_citations.sort_values('sum', ascending=False).head(10)
colors_gen = [GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in genus_citations['Genus']]
ax.barh(range(len(genus_citations)), genus_citations['sum'], color=colors_gen, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(genus_citations)))
ax.set_yticklabels(genus_citations['Genus'])
ax.set_xlabel('Total Citations')
ax.set_title('C. Total Citations by Genus (Top 10)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 1d: Mean citations vs publications
ax = axes[1, 1]
top_genera = df.groupby('Genus').agg({'citations': 'mean', 'pub_year': 'count'}).reset_index()
top_genera = top_genera[top_genera['pub_year'] >= 20].nlargest(15, 'pub_year')
scatter = ax.scatter(top_genera['pub_year'], top_genera['citations'],
                    s=top_genera['pub_year']*3, alpha=0.6,
                    c=range(len(top_genera)), cmap='viridis', edgecolors='black', linewidth=1)
for idx, row in top_genera.iterrows():
    ax.annotate(row['Genus'], (row['pub_year'], row['citations']), fontsize=7, ha='center')
ax.set_xlabel('Number of Publications')
ax.set_ylabel('Mean Citations')
ax.set_title('D. Publication Volume vs Impact', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig1_Citation_Impact_Analysis.png')
plt.close()

# ============================================================================
# ANALYSIS 2: AUTHOR ANALYSIS
# ============================================================================

print("\n[2] Analyzing influential authors...")

# Extract authors (simplified - first author from factorials)
def extract_first_author(factorials):
    if pd.isna(factorials):
        return None
    parts = str(factorials).split('=')
    if len(parts) < 2:
        return None
    authors_part = parts[1].strip() if len(parts) > 1 else None
    if authors_part and authors_part != 'NA':
        # Get first author
        authors = authors_part.split(';')[0].split(',')[0].strip()
        return authors if len(authors) > 2 else None
    return None

df['first_author'] = df['factorials'].apply(extract_first_author)
df_with_authors = df[df['first_author'].notna()].copy()

# Author productivity and impact
author_stats = df_with_authors.groupby('first_author').agg({
    'citations': ['count', 'sum', 'mean'],
    'Genus': lambda x: x.nunique(),
    'pub_year': ['min', 'max']
}).reset_index()
author_stats.columns = ['_'.join(col).strip('_') for col in author_stats.columns]
author_stats.columns = ['Author', 'N_Papers', 'Total_Citations', 'Mean_Citations',
                        'N_Genera', 'First_Year', 'Last_Year']
author_stats['Years_Active'] = author_stats['Last_Year'] - author_stats['First_Year']
author_stats = author_stats.sort_values('Total_Citations', ascending=False)
author_stats.head(100).to_csv(f'{TABLES_PATH}/top_100_authors.csv', index=False)

print(f"   ✓ Unique authors identified: {len(author_stats):,}")
print(f"   ✓ Top author: {author_stats.iloc[0]['Author']} ({author_stats.iloc[0]['N_Papers']:.0f} papers)")

# FIGURE 2: Author Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2a: Top 20 authors by publications
ax = axes[0, 0]
top_authors = author_stats.nlargest(20, 'N_Papers')
ax.barh(range(len(top_authors)), top_authors['N_Papers'],
       color=NEMATODE_COLORS['secondary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_authors)))
ax.set_yticklabels(top_authors['Author'], fontsize=8)
ax.set_xlabel('Number of Papers')
ax.set_title('A. Most Prolific Authors (Top 20)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 2b: Author productivity vs impact
ax = axes[0, 1]
top_50_auth = author_stats[author_stats['N_Papers'] >= 3].nlargest(50, 'Total_Citations')
scatter = ax.scatter(top_50_auth['N_Papers'], top_50_auth['Mean_Citations'],
                    s=top_50_auth['Total_Citations']/5, alpha=0.6,
                    c=top_50_auth['N_Genera'], cmap='plasma', edgecolors='black', linewidth=1)
ax.set_xlabel('Number of Papers')
ax.set_ylabel('Mean Citations per Paper')
ax.set_title('B. Author Productivity vs Impact (Top 50)', fontweight='bold', loc='left')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Genera Studied')
ax.grid(True, alpha=0.3)

# 2c: Author career span
ax = axes[1, 0]
career_bins = [0, 5, 10, 15, 20, 50]
author_stats['Career_Bin'] = pd.cut(author_stats['Years_Active'], bins=career_bins,
                                     labels=['0-5yr', '6-10yr', '11-15yr', '16-20yr', '20+yr'])
career_dist = author_stats['Career_Bin'].value_counts().sort_index()
ax.bar(range(len(career_dist)), career_dist.values,
      color=NEMATODE_COLORS['accent3'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(career_dist)))
ax.set_xticklabels(career_dist.index)
ax.set_ylabel('Number of Authors')
ax.set_title('C. Author Career Span Distribution', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='y')

# 2d: Genera diversity by top authors
ax = axes[1, 1]
top_diverse = author_stats.nlargest(15, 'N_Genera')
ax.barh(range(len(top_diverse)), top_diverse['N_Genera'],
       color=NEMATODE_COLORS['accent1'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_diverse)))
ax.set_yticklabels(top_diverse['Author'], fontsize=8)
ax.set_xlabel('Number of Genera Studied')
ax.set_title('D. Most Taxonomically Diverse Authors', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig2_Author_Analysis.png')
plt.close()

print("\n[Part 3 Analysis 1-2 Complete]")
print("="*70)
