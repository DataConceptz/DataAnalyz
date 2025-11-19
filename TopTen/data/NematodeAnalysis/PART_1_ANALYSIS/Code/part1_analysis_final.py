"""
PART 1: Species & Taxonomic Analysis (Final)
=============================================

Analysis 5: Research Bias Analysis
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from analysis_utils import *
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Tables'

# Load data
print("\n" + "="*70)
print("FINAL PART 1 ANALYSIS - RESEARCH BIAS")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# ============================================================================
# ANALYSIS 5: RESEARCH BIAS - NEMATODE SPECIES
# ============================================================================

print("\n[6] Analyzing research bias in nematode species...")

# Calculate bias metrics for species
species_bias = calculate_research_bias(df, 'Species')
species_bias.to_csv(f'{TABLES_PATH}/species_research_bias.csv', index=False)
print(f"   ✓ Saved: species_research_bias.csv")

# Calculate bias for genera
genus_bias = calculate_research_bias(df, 'Genus')
genus_bias.to_csv(f'{TABLES_PATH}/genus_research_bias.csv', index=False)
print(f"   ✓ Saved: genus_research_bias.csv")

# FIGURE 5: Research Bias Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 5a: Genus bias visualization
ax = axes[0, 0]
top_genera_bias = genus_bias.head(20)

colors_bias = []
for cat in top_genera_bias['bias_category']:
    if cat == 'Overstudied':
        colors_bias.append(NEMATODE_COLORS['accent2'])
    elif cat == 'Adequately Studied':
        colors_bias.append(NEMATODE_COLORS['accent3'])
    elif cat == 'Understudied':
        colors_bias.append(NEMATODE_COLORS['accent1'])
    else:
        colors_bias.append(NEMATODE_COLORS['neutral1'])

bars = ax.barh(range(len(top_genera_bias)), top_genera_bias['n_publications'],
              color=colors_bias, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_genera_bias)))
ax.set_yticklabels(top_genera_bias['Genus'], fontsize=9)
ax.set_xlabel('Number of Publications')
ax.set_title('A. Research Effort by Genus (Top 20)', fontweight='bold', loc='left')
ax.axvline(genus_bias['n_publications'].mean(), color='black', linestyle='--',
          linewidth=1.5, label=f'Mean: {genus_bias["n_publications"].mean():.0f}')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

# 5b: Bias ratio distribution
ax = axes[0, 1]
bias_categories = genus_bias['bias_category'].value_counts()
colors = [NEMATODE_COLORS['accent2'], NEMATODE_COLORS['accent3'],
         NEMATODE_COLORS['accent1'], NEMATODE_COLORS['neutral1']]
explode = (0.05, 0, 0, 0.1)

wedges, texts, autotexts = ax.pie(bias_categories.values,
                                   labels=bias_categories.index,
                                   autopct='%1.1f%%',
                                   colors=colors,
                                   explode=explode,
                                   startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)
ax.set_title('B. Distribution of Research Bias (Genera)', fontweight='bold', loc='left')

# 5c: Top species research intensity
ax = axes[1, 0]
top_species_bias = species_bias.head(25)

# Create combined species labels
top_species_bias['Species_Label'] = top_species_bias['Species']

bars = ax.barh(range(len(top_species_bias)), top_species_bias['n_publications'],
              color=NEMATODE_COLORS['secondary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_species_bias)))
ax.set_yticklabels(top_species_bias['Species_Label'], fontsize=8)
ax.set_xlabel('Number of Publications')
ax.set_title('C. Most Studied Species (Top 25)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 5d: Correlation between publications and citations
ax = axes[1, 1]
scatter_data = genus_bias.head(30)

scatter = ax.scatter(scatter_data['n_publications'],
                    scatter_data['mean_citations'],
                    s=scatter_data['total_count']*10,
                    c=scatter_data['bias_ratio'],
                    cmap='RdYlGn_r', alpha=0.6,
                    edgecolors='black', linewidth=1)

# Add top genus labels
for idx, row in scatter_data.head(10).iterrows():
    ax.annotate(row['Genus'], (row['n_publications'], row['mean_citations']),
               fontsize=7, ha='right', va='bottom')

ax.set_xlabel('Number of Publications')
ax.set_ylabel('Mean Citations')
ax.set_title('D. Research Volume vs Impact (Top 30 Genera)', fontweight='bold', loc='left')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Bias Ratio', rotation=270, labelpad=15)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig5_Research_Bias_Analysis.png')
plt.close()

# ============================================================================
# ANALYSIS 6: RESEARCH BIAS - PLANT HOSTS
# ============================================================================

print("\n[7] Analyzing research bias in plant hosts...")

# Extract host plants
df['host_plants'] = df['abstract'].apply(extract_host_plants)

# Create host dataframe
all_hosts = []
for idx, row in df.iterrows():
    if row['host_plants']:
        for host in row['host_plants']:
            all_hosts.append({
                'Host': host.lower(),
                'Genus': row['Genus'],
                'Year': row['pub_year'],
                'Citations': row['citations']
            })

if len(all_hosts) > 0:
    host_df = pd.DataFrame(all_hosts)

    # Calculate host bias metrics
    host_summary = host_df.groupby('Host').agg({
        'Genus': 'count',
        'Citations': ['sum', 'mean']
    }).reset_index()
    host_summary.columns = ['Host', 'N_Mentions', 'Total_Citations', 'Mean_Citations']
    host_summary = host_summary.sort_values('N_Mentions', ascending=False)

    # Calculate bias
    host_summary['expected_mentions'] = host_summary['N_Mentions'].mean()
    host_summary['bias_ratio'] = host_summary['N_Mentions'] / host_summary['expected_mentions']
    host_summary['bias_category'] = pd.cut(
        host_summary['bias_ratio'],
        bins=[0, 0.25, 0.75, 1.5, float('inf')],
        labels=['Severely Understudied', 'Understudied', 'Adequately Studied', 'Overstudied']
    )

    host_summary.to_csv(f'{TABLES_PATH}/host_plant_research_bias.csv', index=False)
    print(f"   ✓ Saved: host_plant_research_bias.csv")

    # FIGURE 6: Plant Host Research Bias
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # 6a: Top studied hosts
    ax = axes[0]
    top_hosts = host_summary.head(25)

    colors_host_bias = []
    for cat in top_hosts['bias_category']:
        if cat == 'Overstudied':
            colors_host_bias.append(NEMATODE_COLORS['accent2'])
        elif cat == 'Adequately Studied':
            colors_host_bias.append(NEMATODE_COLORS['accent3'])
        elif cat == 'Understudied':
            colors_host_bias.append(NEMATODE_COLORS['accent1'])
        else:
            colors_host_bias.append(NEMATODE_COLORS['neutral1'])

    ax.barh(range(len(top_hosts)), top_hosts['N_Mentions'],
           color=colors_host_bias, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.set_yticks(range(len(top_hosts)))
    ax.set_yticklabels([h.capitalize() for h in top_hosts['Host']], fontsize=9)
    ax.set_xlabel('Number of Mentions')
    ax.set_title('A. Research Effort by Host Plant (Top 25)', fontweight='bold', loc='left')
    ax.axvline(host_summary['N_Mentions'].mean(), color='black', linestyle='--',
              linewidth=1.5, label=f'Mean: {host_summary["N_Mentions"].mean():.0f}')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='x')

    # 6b: Host plant bias categories
    ax = axes[1]
    bias_cat_hosts = host_summary['bias_category'].value_counts()
    colors = [NEMATODE_COLORS['accent2'], NEMATODE_COLORS['accent3'],
             NEMATODE_COLORS['accent1'], NEMATODE_COLORS['neutral1']]
    explode = (0.05, 0, 0, 0.1)

    wedges, texts, autotexts = ax.pie(bias_cat_hosts.values,
                                       labels=bias_cat_hosts.index,
                                       autopct='%1.1f%%',
                                       colors=colors,
                                       explode=explode,
                                       startangle=90)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    ax.set_title('B. Distribution of Research Bias (Host Plants)', fontweight='bold', loc='left')

    plt.tight_layout()
    save_figure(fig, f'{CHARTS_PATH}/Fig6_Host_Plant_Research_Bias.png')
    plt.close()

else:
    print("   ⚠ No host plant data available")

print("\n[Analysis 5 & 6 Complete]")
print("\n" + "="*70)
print("PART 1 ANALYSIS COMPLETE!")
print("="*70)
print(f"\n✓ Charts saved to: {CHARTS_PATH}/")
print(f"✓ Tables saved to: {TABLES_PATH}/")
print("\nGenerated Figures:")
print("  - Fig1_Species_Discovery_Analysis.png")
print("  - Fig2_Taxonomic_Completeness.png")
print("  - Fig3_Host_Parasite_Network.png")
print("  - Fig4_Geographic_Distribution.png")
print("  - Fig5_Research_Bias_Analysis.png")
print("  - Fig6_Host_Plant_Research_Bias.png")
