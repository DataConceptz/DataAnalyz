"""
PART 3: Citation & Impact Analysis - REAL DATA (Simplified)
Note: CSV lacks author/journal columns, so focusing on citation metrics only
"""

import sys
sys.path.append('/home/user/DataAnalyz/TopTen/data/Real_Analyses')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from analysis_utils_improved import *

DATA_FILE = '/home/user/DataAnalyz/TopTen/data/Real_Analyses/ALL_NEMATODES_EXTRACTED.csv'
OUTPUT_DIR = '/home/user/DataAnalyz/TopTen/data/Real_Analyses/PART_3_ANALYSIS'

print("\n" + "="*70)
print("PART 3: CITATION & IMPACT ANALYSIS - REAL DATA")
print("="*70 + "\n")

# Load CSV data
print("Loading data...")
df = pd.read_csv(DATA_FILE)
print(f"✓ Loaded {len(df):,} records")

# CSV already has correct column names
df['pub_year'] = pd.to_numeric(df['pub_year'], errors='coerce')
df = df.dropna(subset=['pub_year'])
df['pub_year'] = df['pub_year'].astype(int)
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)

# Apply filters
df_clean = apply_analysis_filters(df)

print(f"\nDataset after filtering:")
print(f"  Total records: {len(df_clean):,}")
print(f"  Total citations: {df_clean['citations'].sum():,.0f}")
print(f"  Mean citations: {df_clean['citations'].mean():.1f}")
print(f"  Median citations: {df_clean['citations'].median():.1f}")

# ============================================================================
# FIGURE 1: Citation Distribution and Impact Categories
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 1: Citation Distribution and Impact")
print("="*70)

citation_percentiles = df_clean['citations'].quantile([0.5, 0.75, 0.90, 0.95, 0.99])

def categorize_impact(citations):
    if citations >= citation_percentiles[0.95]:
        return 'Exceptional (>95th)'
    elif citations >= citation_percentiles[0.90]:
        return 'Very High (90-95th)'
    elif citations >= citation_percentiles[0.75]:
        return 'High (75-90th)'
    elif citations >= citation_percentiles[0.5]:
        return 'Medium (50-75th)'
    else:
        return 'Low (<50th)'

df_clean['Impact_Category'] = df_clean['citations'].apply(categorize_impact)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: Citation distribution
citations_nonzero = df_clean[df_clean['citations'] > 0]['citations']
ax1.hist(np.log10(citations_nonzero + 1), bins=50, color='#1f77b4',
        alpha=0.7, edgecolor='black', linewidth=0.5)
ax1.set_xlabel('Citations (log₁₀ scale)', fontweight='bold')
ax1.set_ylabel('Number of Publications', fontweight='bold')
ax1.set_title('A. Citation Distribution (Log Scale)', fontweight='bold', loc='left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', alpha=0.3)

# RIGHT: Impact categories
impact_counts = df_clean['Impact_Category'].value_counts()
category_order = ['Low (<50th)', 'Medium (50-75th)', 'High (75-90th)',
                 'Very High (90-95th)', 'Exceptional (>95th)']
impact_counts = impact_counts.reindex(category_order)

colors_impact = ['#e0e0e0', '#a0c4ff', '#ffcc80', '#ff8a65', '#d62728']
wedges, texts, autotexts = ax2.pie(impact_counts.values,
                                    labels=impact_counts.index,
                                    colors=colors_impact,
                                    autopct='%1.1f%%',
                                    startangle=90,
                                    explode=(0, 0, 0.05, 0.1, 0.15))

for text in texts:
    text.set_fontsize(8)
    text.set_fontweight('bold')
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(7)

ax2.set_title('B. Distribution of Impact Categories', fontweight='bold', pad=10)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig1_Citation_Distribution_Impact.png')
plt.close()

# Save high-impact papers
high_impact = df_clean[df_clean['citations'] >= citation_percentiles[0.95]].copy()
high_impact_summary = high_impact[['title', 'pub_year', 'journal', 'citations', 'Genus', 'Species']].sort_values('citations', ascending=False)
high_impact_summary.to_csv(f'{OUTPUT_DIR}/Tables/Table1_High_Impact_Papers.csv', index=False)
print(f"✓ Identified {len(high_impact):,} high-impact papers (>95th percentile)")

# ============================================================================
# FIGURE 2: Citation Metrics by Genus
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 2: Citation Metrics by Genus")
print("="*70)

genus_citations = df_clean.groupby('Genus').agg({
    'citations': ['sum', 'mean', 'median', 'count'],
    'pub_year': ['min', 'max']
}).reset_index()
genus_citations.columns = ['Genus', 'Total_Citations', 'Mean_Citations',
                          'Median_Citations', 'N_Papers', 'First_Year', 'Last_Year']

top15_cit = genus_citations.nlargest(15, 'Total_Citations')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: Mean citations per paper
colors = [get_genus_color(g) for g in top15_cit['Genus']]
y_pos = np.arange(len(top15_cit))

ax1.barh(y_pos, top15_cit['Mean_Citations'], color=colors,
        edgecolor='black', linewidth=0.5, alpha=0.8)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(top15_cit['Genus'], style='italic', fontsize=9)
ax1.set_xlabel('Mean Citations per Paper', fontweight='bold')
ax1.set_title('A. Average Citation Impact by Genus (Top 15)',
             fontweight='bold', loc='left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# RIGHT: Total citations vs papers
ax2.scatter(top15_cit['N_Papers'], top15_cit['Total_Citations'],
           s=top15_cit['Mean_Citations']*5, c=colors, alpha=0.6,
           edgecolors='black', linewidths=1)

for _, row in top15_cit.head(8).iterrows():
    ax2.annotate(row['Genus'],
                (row['N_Papers'], row['Total_Citations']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=8, style='italic', fontweight='bold')

ax2.set_xlabel('Number of Papers', fontweight='bold')
ax2.set_ylabel('Total Citations', fontweight='bold')
ax2.set_title('B. Research Volume vs Impact\n(bubble size = mean citations)',
             fontweight='bold', loc='left')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig2_Citation_Metrics_by_Genus.png')
plt.close()

# Save data
genus_citations.to_csv(f'{OUTPUT_DIR}/Tables/Table2_Genus_Citation_Metrics.csv', index=False)
print(f"✓ Saved citation metrics for {len(genus_citations)} genera")

# ============================================================================
# FIGURE 3: Temporal Citation Patterns
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 3: Temporal Citation Patterns")
print("="*70)

top8_genera = genus_citations.nlargest(8, 'Total_Citations')['Genus'].tolist()

fig, ax = plt.subplots(figsize=(12, 7))

for genus in top8_genera:
    genus_data = df_clean[df_clean['Genus'] == genus].groupby('pub_year').agg({
        'citations': 'mean'
    }).reset_index()

    genus_data['MA_3yr'] = genus_data['citations'].rolling(window=3, center=True).mean()

    color = get_genus_color(genus)
    ax.plot(genus_data['pub_year'], genus_data['MA_3yr'],
           linewidth=2.5, label=genus, color=color, alpha=0.8, marker='o',
           markersize=3, markevery=5)

ax.set_xlabel('Publication Year', fontweight='bold')
ax.set_ylabel('Mean Citations per Paper (3-year MA)', fontweight='bold')
ax.set_title('Temporal Evolution of Citation Impact for Top 8 Genera',
            fontweight='bold', pad=15)
ax.legend(loc='best', ncol=2, frameon=True, fancybox=False, edgecolor='black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig3_Temporal_Citation_Patterns.png')
plt.close()

print("✓ Saved temporal citation patterns")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("PART 3 ANALYSIS COMPLETE - REAL DATA (SIMPLIFIED)")
print("="*70)
print("\nGenerated Figures:")
print("  ✓ Fig1: Citation Distribution and Impact Categories (2-panel)")
print("  ✓ Fig2: Citation Metrics by Genus (2-panel)")
print("  ✓ Fig3: Temporal Citation Patterns (line plot)")
print("\nNote: Author and journal analyses skipped (columns not in CSV)")
print("\nAll figures saved in Nature-quality format (600 DPI)")
print("Consistent genus colors used throughout")
print("="*70 + "\n")
