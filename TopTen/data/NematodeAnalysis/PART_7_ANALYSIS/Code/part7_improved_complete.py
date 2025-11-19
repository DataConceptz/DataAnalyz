"""
PART 7: Advanced Statistical Analysis - IMPROVED 6X
Nature-Quality Publication Standards

Focused analysis including:
1. PCA analysis of genus characteristics
2. Clustering analysis
3. Research pattern analysis

Each figure is professionally designed for Nature publication
"""

import sys
sys.path.append('/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from analysis_utils_improved import *

# Configuration
DATA_FILE = '/home/user/DataAnalyz/TopTen/data/Final_Nema_Data.xlsx'
OUTPUT_DIR = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_7_ANALYSIS'

print("\n" + "="*70)
print("PART 7: ADVANCED STATISTICAL ANALYSIS - IMPROVED VERSION")
print("="*70 + "\n")

# Load data
print("Loading data...")
df = pd.read_excel(DATA_FILE, engine='openpyxl')
print(f"✓ Loaded {len(df):,} records")

# Standardize column names
df = df.rename(columns={
    'PubYear': 'pub_year',
    'Times cited': 'citations',
})

# Basic cleaning
df['pub_year'] = pd.to_numeric(df['pub_year'], errors='coerce')
df = df.dropna(subset=['pub_year'])
df['pub_year'] = df['pub_year'].astype(int)
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)

# Apply filters
df_clean = apply_analysis_filters(df)

print(f"\nDataset: {len(df_clean):,} records")

# ============================================================================
# Prepare genus-level features
# ============================================================================

print("\nPreparing genus-level features...")

genus_features = df_clean.groupby('Genus').agg({
    'Species': 'nunique',
    'pub_year': ['count', 'min', 'max'],
    'citations': ['mean', 'median', 'sum']
}).reset_index()

genus_features.columns = ['Genus', 'N_Species', 'N_Papers', 'First_Year',
                         'Last_Year', 'Mean_Cit', 'Median_Cit', 'Total_Cit']

# Calculate additional features
genus_features['Years_Span'] = genus_features['Last_Year'] - genus_features['First_Year'] + 1
genus_features['Papers_Per_Year'] = genus_features['N_Papers'] / genus_features['Years_Span']
genus_features['Citations_Per_Paper'] = genus_features['Total_Cit'] / genus_features['N_Papers']

print(f"✓ Created feature matrix for {len(genus_features)} genera")

# ============================================================================
# FIGURE 1: PCA Analysis (IMPROVED - CLEANER)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 1: Principal Component Analysis")
print("="*70)

# Select features for PCA
features_for_pca = ['N_Species', 'N_Papers', 'Mean_Cit', 'Years_Span', 'Papers_Per_Year']
X = genus_features[features_for_pca].fillna(0)

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA(n_components=min(5, len(features_for_pca)))
X_pca = pca.fit_transform(X_scaled)

# Add PCA results to dataframe
genus_features['PC1'] = X_pca[:, 0]
genus_features['PC2'] = X_pca[:, 1]

print(f"✓ PCA variance explained: PC1={pca.explained_variance_ratio_[0]*100:.1f}%, PC2={pca.explained_variance_ratio_[1]*100:.1f}%")

# K-means clustering
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
genus_features['Cluster'] = kmeans.fit_predict(X_scaled)

# Create figure with 2 panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# LEFT: PCA biplot
colors = [get_genus_color(g) for g in genus_features['Genus']]
scatter = ax1.scatter(genus_features['PC1'], genus_features['PC2'],
                     s=genus_features['N_Papers']*2,
                     c=colors, alpha=0.7,
                     edgecolors='black', linewidths=1)

# Label top 10 genera by publications
top10 = genus_features.nlargest(10, 'N_Papers')
for _, row in top10.iterrows():
    ax1.annotate(row['Genus'],
                (row['PC1'], row['PC2']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=8, style='italic', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                         edgecolor='gray', alpha=0.7))

ax1.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax1.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)',
              fontweight='bold')
ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)',
              fontweight='bold')
ax1.set_title('A. PCA Biplot of Genera\n(bubble size = publications)',
             fontweight='bold', loc='left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(True, alpha=0.3)

# RIGHT: Scree plot
variance_explained = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(variance_explained)

ax2_twin = ax2.twinx()

# Bars for individual variance
bars = ax2.bar(range(1, len(variance_explained)+1), variance_explained*100,
              color='#1f77b4', alpha=0.7, edgecolor='black', linewidth=0.5,
              label='Individual')

# Line for cumulative variance
line = ax2_twin.plot(range(1, len(cumulative_variance)+1), cumulative_variance*100,
                    color='#d62728', marker='o', linewidth=2.5,
                    markersize=8, label='Cumulative')

ax2.set_xlabel('Principal Component', fontweight='bold')
ax2.set_ylabel('Variance Explained (%)', fontweight='bold', color='#1f77b4')
ax2_twin.set_ylabel('Cumulative Variance (%)', fontweight='bold', color='#d62728')
ax2.set_title('B. Scree Plot', fontweight='bold', loc='left')
ax2.set_xticks(range(1, len(variance_explained)+1))
ax2.tick_params(axis='y', labelcolor='#1f77b4')
ax2_twin.tick_params(axis='y', labelcolor='#d62728')
ax2.spines['top'].set_visible(False)
ax2_twin.spines['top'].set_visible(False)
ax2.grid(axis='y', alpha=0.3)

# Combined legend
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right',
          frameon=True, fancybox=False, edgecolor='black')

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig1_PCA_Analysis.png')
plt.close()

# Save PCA results
genus_features[['Genus', 'PC1', 'PC2', 'Cluster']].to_csv(
    f'{OUTPUT_DIR}/Tables/Table1_PCA_Results.csv', index=False)
print("✓ Saved PCA results")

# ============================================================================
# FIGURE 2: Clustering Analysis (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 2: Hierarchical Clustering Analysis")
print("="*70)

# Perform hierarchical clustering
linkage_matrix = linkage(X_scaled, method='ward')

# Create figure with 2 panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))

# LEFT: Dendrogram (for top 20 genera)
top20_idx = genus_features.nlargest(20, 'N_Papers').index
X_scaled_top20 = X_scaled[top20_idx]
genus_labels_top20 = genus_features.loc[top20_idx, 'Genus'].values

linkage_top20 = linkage(X_scaled_top20, method='ward')

dendrogram(linkage_top20, labels=genus_labels_top20,
          ax=ax1, orientation='right', color_threshold=0,
          above_threshold_color='#1f77b4')

ax1.set_xlabel('Ward Distance', fontweight='bold')
ax1.set_title('A. Hierarchical Clustering (Top 20 Genera)',
             fontweight='bold', loc='left', pad=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# Make genus labels italic
for label in ax1.get_yticklabels():
    label.set_fontstyle('italic')
    label.set_fontsize(8)

# RIGHT: Cluster characteristics heatmap
cluster_chars = genus_features.groupby('Cluster')[features_for_pca].mean()
cluster_chars_norm = (cluster_chars - cluster_chars.min()) / (cluster_chars.max() - cluster_chars.min())

sns.heatmap(cluster_chars_norm.T, annot=True, fmt='.2f',
           cmap='RdYlGn', cbar_kws={'label': 'Normalized Value'},
           linewidths=1, linecolor='gray', ax=ax2)

ax2.set_xlabel('Cluster', fontweight='bold')
ax2.set_ylabel('Feature', fontweight='bold')
ax2.set_title('B. Cluster Characteristics Heatmap',
             fontweight='bold', loc='left', pad=10)
ax2.set_xticklabels([f'Cluster {i}' for i in range(len(cluster_chars))])

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig2_Clustering_Analysis.png')
plt.close()

# Save cluster assignments
genus_features[['Genus', 'Cluster', 'N_Papers', 'N_Species', 'Mean_Cit']].to_csv(
    f'{OUTPUT_DIR}/Tables/Table2_Cluster_Assignments.csv', index=False)
print(f"✓ Identified {kmeans.n_clusters} research clusters")

# ============================================================================
# FIGURE 3: Feature Correlations (NEW)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 3: Feature Correlation Matrix")
print("="*70)

# Calculate correlation matrix
correlation_features = ['N_Species', 'N_Papers', 'Mean_Cit', 'Years_Span',
                       'Papers_Per_Year', 'Citations_Per_Paper']
corr_matrix = genus_features[correlation_features].corr()

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Create mask for upper triangle
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# Plot heatmap
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
           cmap='coolwarm', center=0, vmin=-1, vmax=1,
           square=True, linewidths=1, linecolor='gray',
           cbar_kws={'label': 'Correlation Coefficient',
                    'shrink': 0.8}, ax=ax)

ax.set_title('Feature Correlation Matrix', fontweight='bold', pad=15, fontsize=14)

# Improve labels
feature_labels = ['Species\nCount', 'Paper\nCount', 'Mean\nCitations',
                 'Years\nActive', 'Papers/\nYear', 'Citations/\nPaper']
ax.set_xticklabels(feature_labels, rotation=0, ha='center')
ax.set_yticklabels(feature_labels, rotation=0)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig3_Correlation_Matrix.png')
plt.close()

# Save correlation matrix
corr_matrix.to_csv(f'{OUTPUT_DIR}/Tables/Table3_Correlation_Matrix.csv')
print("✓ Computed and saved correlation matrix")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("PART 7 ANALYSIS COMPLETE - IMPROVED VERSION")
print("="*70)
print("\nGenerated Figures:")
print("  ✓ Fig1: PCA Analysis (2-panel: biplot + scree plot)")
print("  ✓ Fig2: Hierarchical Clustering (2-panel: dendrogram + heatmap)")
print("  ✓ Fig3: Feature Correlation Matrix (heatmap)")
print("\nKey Results:")
print(f"  • PCA: {pca.explained_variance_ratio_[0]*100:.1f}% + {pca.explained_variance_ratio_[1]*100:.1f}% = {(pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1])*100:.1f}% variance explained")
print(f"  • K-means: {kmeans.n_clusters} distinct research clusters identified")
print("\nAll figures saved in Nature-quality format (600 DPI)")
print("="*70 + "\n")
