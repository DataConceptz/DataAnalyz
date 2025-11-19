"""
PART 1: Species & Taxonomic Analysis - IMPROVED 6X
Nature-Quality Publication Standards

Comprehensive analysis including:
1. Species discovery rate with statistical trends
2. Taxonomic completeness assessment
3. Host-parasite networks (FIXED - only real plants)
4. Geographic distribution patterns
5. Research bias analysis
6. Host plant research intensity

Each figure is professionally designed for Nature publication
"""

import sys
sys.path.append('/home/user/DataAnalyz/TopTen/data/Real_Analyses')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import networkx as nx
from analysis_utils_improved import *

# Configuration
DATA_FILE = '/home/user/DataAnalyz/TopTen/data/Real_Analyses/ALL_NEMATODES_EXTRACTED.csv'
OUTPUT_DIR = '/home/user/DataAnalyz/TopTen/data/Real_Analyses/PART_1_ANALYSIS'

print("\n" + "="*70)
print("PART 1: SPECIES & TAXONOMIC ANALYSIS - REAL DATA")
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
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)

# Apply filters
df_clean = apply_analysis_filters(df)

print(f"\nDataset after filtering:")
print(f"  Total records: {len(df_clean):,}")
print(f"  Unique genera: {df_clean['Genus'].nunique()}")
print(f"  Unique species: {df_clean['Species'].nunique()}")
print(f"  Year range: {df_clean['pub_year'].min()}-{df_clean['pub_year'].max()}")

# ============================================================================
# FIGURE 1: Species Discovery Rate Analysis (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 1: Species Discovery Rate Analysis")
print("="*70)

# Prepare species discovery data
species_by_year = df_clean.groupby(['pub_year', 'Species']).size().reset_index()
species_by_year = species_by_year.groupby('pub_year')['Species'].nunique().reset_index()
species_by_year.columns = ['Year', 'New_Species']

# Calculate cumulative discovery
species_by_year = species_by_year.sort_values('Year')
species_by_year['Cumulative_Species'] = species_by_year['New_Species'].cumsum()

# Calculate 5-year moving average
window = 5
species_by_year['MA_5yr'] = species_by_year['New_Species'].rolling(window=window, center=True).mean()

# Fit discovery curve
years_numeric = species_by_year['Year'].values
cum_species = species_by_year['Cumulative_Species'].values

# Exponential fit
from scipy.optimize import curve_fit

def exponential_func(x, a, b, c):
    return a * np.exp(b * (x - x.min())) + c

try:
    popt, _ = curve_fit(exponential_func, years_numeric, cum_species, maxfev=5000)
    years_fit = np.linspace(years_numeric.min(), years_numeric.max(), 100)
    species_fit = exponential_func(years_fit, *popt)
    fit_successful = True
except:
    fit_successful = False

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# Left: Annual discovery rate with moving average
ax1.bar(species_by_year['Year'], species_by_year['New_Species'],
        color='#1f77b4', alpha=0.6, label='Annual discoveries', width=0.8)
ax1.plot(species_by_year['Year'], species_by_year['MA_5yr'],
         color='#d62728', linewidth=2, label=f'{window}-year moving average')

ax1.set_xlabel('Year', fontweight='bold')
ax1.set_ylabel('Number of Species', fontweight='bold')
ax1.set_title('A. Annual Species Discovery Rate', fontweight='bold', loc='left')
ax1.legend(frameon=True, fancybox=False, edgecolor='black')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', alpha=0.3)

# Right: Cumulative discovery with fit
ax2.scatter(species_by_year['Year'], species_by_year['Cumulative_Species'],
           s=30, color='#1f77b4', alpha=0.6, label='Observed', zorder=3)

if fit_successful:
    ax2.plot(years_fit, species_fit, 'r-', linewidth=2, label='Exponential fit', zorder=2)

ax2.set_xlabel('Year', fontweight='bold')
ax2.set_ylabel('Cumulative Species Count', fontweight='bold')
ax2.set_title('B. Cumulative Species Discovery', fontweight='bold', loc='left')
ax2.legend(frameon=True, fancybox=False, edgecolor='black')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig1_Species_Discovery_Rate.png')
plt.close()

# Save data
species_by_year.to_csv(f'{OUTPUT_DIR}/Tables/Table1_Species_Discovery_Rates.csv', index=False)
print(f"✓ Saved species discovery data ({len(species_by_year)} years)")

# ============================================================================
# FIGURE 2: Taxonomic Completeness by Genus (IMPROVED - SINGLE PANEL)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 2: Taxonomic Completeness Analysis")
print("="*70)

# Calculate genus-level metrics
genus_stats = df_clean.groupby('Genus').agg({
    'Species': 'nunique',
    'pub_year': ['count', 'min', 'max'],
    'citations': 'mean'
}).reset_index()

genus_stats.columns = ['Genus', 'N_Species', 'N_Publications', 'First_Year', 'Last_Year', 'Mean_Citations']
genus_stats['Years_Studied'] = genus_stats['Last_Year'] - genus_stats['First_Year']
genus_stats['Publications_Per_Species'] = genus_stats['N_Publications'] / genus_stats['N_Species']

# Sort by number of species
genus_stats = genus_stats.sort_values('N_Species', ascending=False).head(20)

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Create color map using consistent genus colors
colors = [get_genus_color(genus) for genus in genus_stats['Genus']]

# Horizontal bar chart
y_pos = np.arange(len(genus_stats))
bars = ax.barh(y_pos, genus_stats['N_Species'], color=colors, edgecolor='black', linewidth=0.5)

# Add value labels
for i, (idx, row) in enumerate(genus_stats.iterrows()):
    ax.text(row['N_Species'] + 1, i, f"{int(row['N_Species'])}",
           va='center', ha='left', fontsize=8)

ax.set_yticks(y_pos)
ax.set_yticklabels(genus_stats['Genus'], style='italic')
ax.set_xlabel('Number of Species', fontweight='bold')
ax.set_title('Species Richness by Genus (Top 20)', fontweight='bold', pad=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig2_Taxonomic_Completeness.png')
plt.close()

# Save data
genus_stats.to_csv(f'{OUTPUT_DIR}/Tables/Table2_Genus_Taxonomic_Stats.csv', index=False)
print(f"✓ Saved taxonomic completeness data ({len(genus_stats)} genera)")

# ============================================================================
# FIGURE 3: Research Effort vs Species Diversity (NEW)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 3: Research Effort vs Species Diversity")
print("="*70)

# Use all genera for this analysis
genus_full_stats = df_clean.groupby('Genus').agg({
    'Species': 'nunique',
    'pub_year': 'count',
    'citations': 'mean'
}).reset_index()
genus_full_stats.columns = ['Genus', 'N_Species', 'N_Publications', 'Mean_Citations']

# Create figure
fig, ax = plt.subplots(figsize=(10, 7))

# Get colors for top genera
top_genera = genus_full_stats.nlargest(15, 'N_Publications')['Genus'].tolist()
colors = [get_genus_color(g) if g in top_genera else '#cccccc' for g in genus_full_stats['Genus']]
alphas = [0.7 if g in top_genera else 0.3 for g in genus_full_stats['Genus']]
sizes = [80 if g in top_genera else 30 for g in genus_full_stats['Genus']]

# Scatter plot
for i, row in genus_full_stats.iterrows():
    ax.scatter(row['N_Publications'], row['N_Species'],
              s=sizes[i], c=[colors[i]], alpha=alphas[i],
              edgecolors='black', linewidth=0.5, zorder=3 if row['Genus'] in top_genera else 1)

# Label top 10 genera
for _, row in genus_full_stats.nlargest(10, 'N_Publications').iterrows():
    ax.annotate(row['Genus'],
               (row['N_Publications'], row['N_Species']),
               xytext=(5, 5), textcoords='offset points',
               fontsize=8, style='italic', fontweight='bold')

# Add trend line
z = np.polyfit(genus_full_stats['N_Publications'], genus_full_stats['N_Species'], 1)
p = np.poly1d(z)
x_trend = np.linspace(genus_full_stats['N_Publications'].min(),
                     genus_full_stats['N_Publications'].max(), 100)
ax.plot(x_trend, p(x_trend), "r--", alpha=0.5, linewidth=2, label='Linear trend', zorder=2)

# Calculate correlation
r, p_val = stats.pearsonr(genus_full_stats['N_Publications'], genus_full_stats['N_Species'])
ax.text(0.05, 0.95, f'r = {r:.3f}\np < 0.001' if p_val < 0.001 else f'r = {r:.3f}\np = {p_val:.3f}',
       transform=ax.transAxes, va='top', ha='left',
       bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8))

ax.set_xlabel('Number of Publications', fontweight='bold')
ax.set_ylabel('Number of Species', fontweight='bold')
ax.set_title('Research Effort vs Species Diversity', fontweight='bold', pad=10)
ax.legend(frameon=True, fancybox=False, edgecolor='black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig3_Research_Effort_vs_Diversity.png')
plt.close()

print(f"✓ Correlation: r={r:.3f}, p={p_val:.3e}")

# ============================================================================
# FIGURE 4: Host-Parasite Networks (FIXED - REAL PLANTS ONLY)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 4: Host-Parasite Network Analysis")
print("="*70)

# Extract host plants from abstracts (IMPROVED METHOD)
print("Extracting host-parasite relationships...")
df_with_abstract = df_clean[df_clean['abstract'].notna()].copy()

# Use improved extraction function
host_plant_records = []
for idx, row in df_with_abstract.iterrows():
    hosts = extract_host_plants_improved(row['abstract'])
    for host in hosts:
        host_plant_records.append({
            'Genus': row['Genus'],
            'Species': row['Species'],
            'Host': host,
            'Year': row['pub_year']
        })

df_hosts = pd.DataFrame(host_plant_records)

if len(df_hosts) > 0:
    print(f"✓ Extracted {len(df_hosts):,} host-parasite relationships")
    print(f"✓ Unique nematode genera: {df_hosts['Genus'].nunique()}")
    print(f"✓ Unique host plants: {df_hosts['Host'].nunique()}")

    # Create network for top genera and hosts
    genus_host_counts = df_hosts.groupby(['Genus', 'Host']).size().reset_index(name='Count')

    # Filter top interactions
    top_genera = genus_host_counts.groupby('Genus')['Count'].sum().nlargest(8).index
    genus_host_filtered = genus_host_counts[genus_host_counts['Genus'].isin(top_genera)]

    top_hosts = genus_host_filtered.groupby('Host')['Count'].sum().nlargest(15).index
    genus_host_filtered = genus_host_filtered[genus_host_filtered['Host'].isin(top_hosts)]

    # Create figure with 2 subplots
    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.2], wspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # LEFT: Bar chart of most common hosts
    host_counts = df_hosts['Host'].value_counts().head(20)
    y_pos = np.arange(len(host_counts))
    ax1.barh(y_pos, host_counts.values, color='#2ca02c', alpha=0.7, edgecolor='black', linewidth=0.5)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(host_counts.index, fontsize=8)
    ax1.set_xlabel('Number of Nematode Associations', fontweight='bold')
    ax1.set_title('A. Most Frequently Reported Host Plants', fontweight='bold', loc='left')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, v in enumerate(host_counts.values):
        ax1.text(v + max(host_counts.values)*0.01, i, str(int(v)),
                va='center', ha='left', fontsize=7)

    # RIGHT: Network visualization
    G = nx.Graph()

    # Add nodes
    for genus in top_genera:
        G.add_node(genus, node_type='nematode')
    for host in top_hosts:
        G.add_node(host, node_type='host')

    # Add edges with weights
    for _, row in genus_host_filtered.iterrows():
        G.add_edge(row['Genus'], row['Host'], weight=row['Count'])

    # Layout
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

    # Draw network
    # Nematode nodes
    nematode_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'nematode']
    nematode_colors = [get_genus_color(n) for n in nematode_nodes]
    nx.draw_networkx_nodes(G, pos, nodelist=nematode_nodes,
                          node_color=nematode_colors,
                          node_size=600, alpha=0.9, ax=ax2,
                          edgecolors='black', linewidths=1.5)

    # Host nodes
    host_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'host']
    nx.draw_networkx_nodes(G, pos, nodelist=host_nodes,
                          node_color='#2ca02c', node_shape='s',
                          node_size=400, alpha=0.7, ax=ax2,
                          edgecolors='black', linewidths=1)

    # Draw edges with varying thickness
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights)
    widths = [1 + 3 * (w / max_weight) for w in weights]

    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.2, ax=ax2)

    # Labels
    labels = {n: n for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=7,
                           font_weight='bold', ax=ax2)

    ax2.set_title('B. Host-Parasite Network (Top 8 Genera, 15 Hosts)',
                 fontweight='bold', loc='left')
    ax2.axis('off')

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='gray', edgecolor='black', label='Nematode (circle)'),
        Patch(facecolor='#2ca02c', edgecolor='black', label='Host plant (square)')
    ]
    ax2.legend(handles=legend_elements, loc='upper right', frameon=True,
              fancybox=False, edgecolor='black')

    plt.tight_layout()
    save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig4_Host_Parasite_Network.png')
    plt.close()

    # Save host-parasite data
    df_hosts.to_csv(f'{OUTPUT_DIR}/Tables/Table3_Host_Parasite_Relationships.csv', index=False)
    genus_host_counts.to_csv(f'{OUTPUT_DIR}/Tables/Table4_Genus_Host_Counts.csv', index=False)
    print(f"✓ Saved host-parasite network data")
else:
    print("⚠ No host plant data extracted")

# ============================================================================
# FIGURE 5: Geographic Distribution (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 5: Geographic Distribution Analysis")
print("="*70)

# Extract country data
# Use country_clean if available, otherwise use country
country_col = 'country_clean' if 'country_clean' in df_clean.columns else 'country'
df_countries = df_clean[df_clean[country_col].notna()].copy()

if len(df_countries) > 0:
    country_stats = df_countries.groupby(country_col).agg({
        'Genus': 'nunique',
        'Species': 'nunique',
        'pub_year': 'count',
        'citations': 'mean'
    }).reset_index()
    country_stats.columns = ['Country', 'N_Genera', 'N_Species', 'N_Publications', 'Mean_Citations']
    country_stats = country_stats.sort_values('N_Publications', ascending=False).head(25)

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # LEFT: Publications by country
    y_pos = np.arange(len(country_stats))
    colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, len(country_stats)))

    ax1.barh(y_pos, country_stats['N_Publications'],
            color=colors_gradient, edgecolor='black', linewidth=0.5)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(country_stats['Country'], fontsize=8)
    ax1.set_xlabel('Number of Publications', fontweight='bold')
    ax1.set_title('A. Research Output by Country (Top 25)', fontweight='bold', loc='left')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, v in enumerate(country_stats['N_Publications'].values):
        ax1.text(v + max(country_stats['N_Publications'])*0.01, i, str(int(v)),
                va='center', ha='left', fontsize=7)

    # RIGHT: Bubble chart - Efficiency vs Diversity
    top_countries = country_stats.head(20)

    bubble_sizes = top_countries['Mean_Citations'] * 5
    bubble_colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(top_countries)))

    scatter = ax2.scatter(top_countries['N_Publications'],
                         top_countries['N_Genera'],
                         s=bubble_sizes, c=bubble_colors,
                         alpha=0.6, edgecolors='black', linewidths=1)

    # Label top 10
    for i, (_, row) in enumerate(top_countries.head(10).iterrows()):
        ax2.annotate(row['Country'],
                    (row['N_Publications'], row['N_Genera']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=7, fontweight='bold')

    ax2.set_xlabel('Number of Publications', fontweight='bold')
    ax2.set_ylabel('Genus Diversity', fontweight='bold')
    ax2.set_title('B. Research Output vs Diversity\n(bubble size = mean citations)',
                 fontweight='bold', loc='left')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig5_Geographic_Distribution.png')
    plt.close()

    # Save data
    country_stats.to_csv(f'{OUTPUT_DIR}/Tables/Table5_Country_Statistics.csv', index=False)
    print(f"✓ Saved geographic distribution data ({len(country_stats)} countries)")
else:
    print("⚠ No country data available")

# ============================================================================
# FIGURE 6: Research Bias Analysis (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 6: Research Bias Analysis")
print("="*70)

# Calculate research bias
genus_publications = df_clean.groupby('Genus').agg({
    'pub_year': 'count',
    'Species': 'nunique',
    'citations': 'mean'
}).reset_index()
genus_publications.columns = ['Genus', 'N_Publications', 'N_Species', 'Mean_Citations']

# Calculate bias metrics
mean_pubs = genus_publications['N_Publications'].mean()
genus_publications['Bias_Ratio'] = genus_publications['N_Publications'] / mean_pubs
genus_publications['Publications_Per_Species'] = genus_publications['N_Publications'] / genus_publications['N_Species']

# Classify bias
def classify_bias(ratio):
    if ratio < 0.25:
        return 'Severely Understudied'
    elif ratio < 0.75:
        return 'Understudied'
    elif ratio < 1.5:
        return 'Adequately Studied'
    else:
        return 'Overstudied'

genus_publications['Bias_Category'] = genus_publications['Bias_Ratio'].apply(classify_bias)

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: Top 20 genera by publication count
top20 = genus_publications.nlargest(20, 'N_Publications')
colors = [get_genus_color(g) for g in top20['Genus']]

y_pos = np.arange(len(top20))
ax1.barh(y_pos, top20['N_Publications'], color=colors,
        edgecolor='black', linewidth=0.5, alpha=0.8)
ax1.axvline(mean_pubs, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_pubs:.0f}')
ax1.set_yticks(y_pos)
ax1.set_yticklabels(top20['Genus'], style='italic', fontsize=8)
ax1.set_xlabel('Number of Publications', fontweight='bold')
ax1.set_title('A. Research Effort by Genus (Top 20)', fontweight='bold', loc='left')
ax1.legend(frameon=True, fancybox=False, edgecolor='black')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# RIGHT: Bias distribution pie chart
bias_counts = genus_publications['Bias_Category'].value_counts()
colors_pie = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
explode = (0.05, 0.05, 0, 0.05)

wedges, texts, autotexts = ax2.pie(bias_counts.values,
                                    labels=bias_counts.index,
                                    colors=colors_pie,
                                    autopct='%1.1f%%',
                                    explode=explode,
                                    startangle=90)

for text in texts:
    text.set_fontweight('bold')
    text.set_fontsize(9)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(8)

ax2.set_title('B. Distribution of Research Bias Categories',
             fontweight='bold', pad=10)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig6_Research_Bias_Analysis.png')
plt.close()

# Save data
genus_publications.to_csv(f'{OUTPUT_DIR}/Tables/Table6_Research_Bias_Metrics.csv', index=False)
print(f"✓ Saved research bias data ({len(genus_publications)} genera)")

# Bias summary
print("\nResearch Bias Summary:")
for category in ['Overstudied', 'Adequately Studied', 'Understudied', 'Severely Understudied']:
    count = len(genus_publications[genus_publications['Bias_Category'] == category])
    pct = 100 * count / len(genus_publications)
    print(f"  {category}: {count} genera ({pct:.1f}%)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("PART 1 ANALYSIS COMPLETE - IMPROVED VERSION")
print("="*70)
print("\nGenerated Figures:")
print("  ✓ Fig1: Species Discovery Rate Analysis (2-panel)")
print("  ✓ Fig2: Taxonomic Completeness (single panel)")
print("  ✓ Fig3: Research Effort vs Diversity (scatter)")
print("  ✓ Fig4: Host-Parasite Network (FIXED - real plants only)")
print("  ✓ Fig5: Geographic Distribution (2-panel)")
print("  ✓ Fig6: Research Bias Analysis (2-panel)")
print("\nAll figures saved in Nature-quality format (600 DPI)")
print("Consistent genus colors used throughout")
print("="*70 + "\n")
