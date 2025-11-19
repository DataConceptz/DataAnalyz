"""
PART 7: Advanced Statistical Analysis
======================================
ML models, PCA, clustering, anomaly detection
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from analysis_utils import *

DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_7_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_7_ANALYSIS/Tables'

print("="*70)
print("PART 7: ADVANCED STATISTICAL ANALYSIS")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# Prepare feature matrix
genus_features = df.groupby('Genus').agg({
    'citations': ['mean', 'sum', 'std'],
    'pub_year': ['min', 'max', 'count'],
    'Species': 'nunique',
    'count_numeric': 'sum'
}).reset_index()
genus_features.columns = ['_'.join(col).strip('_') for col in genus_features.columns]
genus_features.columns = ['Genus', 'Cit_Mean', 'Cit_Sum', 'Cit_Std', 'First_Year',
                         'Last_Year', 'N_Papers', 'N_Species', 'Total_Count']
genus_features['Years_Span'] = genus_features['Last_Year'] - genus_features['First_Year']
genus_features['Papers_Per_Year'] = genus_features['N_Papers'] / (genus_features['Years_Span'] + 1)
genus_features.to_csv(f'{TABLES_PATH}/genus_feature_matrix.csv', index=False)

# PCA Analysis
features_for_pca = ['Cit_Mean', 'N_Papers', 'N_Species', 'Years_Span', 'Papers_Per_Year']
X = genus_features[features_for_pca].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=min(5, len(features_for_pca)))
X_pca = pca.fit_transform(X_scaled)

pca_results = pd.DataFrame({
    'Genus': genus_features['Genus'],
    'PC1': X_pca[:, 0],
    'PC2': X_pca[:, 1] if X_pca.shape[1] > 1 else 0
})
pca_results.to_csv(f'{TABLES_PATH}/pca_results.csv', index=False)

print(f"   ✓ PCA variance explained: {pca.explained_variance_ratio_[:2].sum():.2%}")

# Clustering
n_clusters = min(5, len(genus_features) // 3)
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
genus_features['Cluster'] = clusters
genus_features.to_csv(f'{TABLES_PATH}/genus_clusters.csv', index=False)

# Anomaly detection
iso_forest = IsolationForest(contamination=0.1, random_state=42)
anomalies = iso_forest.fit_predict(X_scaled)
genus_features['Is_Anomaly'] = anomalies == -1
anomaly_genera = genus_features[genus_features['Is_Anomaly']]['Genus'].tolist()

print(f"   ✓ Clusters identified: {n_clusters}")
print(f"   ✓ Anomalies detected: {sum(anomalies == -1)}")

# FIGURE 1: PCA and Clustering
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1a: PCA biplot
ax = axes[0, 0]
scatter = ax.scatter(pca_results['PC1'], pca_results['PC2'],
                    c=genus_features['Cluster'], cmap='viridis',
                    s=genus_features['N_Papers']*5, alpha=0.6, edgecolors='black', linewidth=1)

# Label top genera
top_genera_pca = genus_features.nlargest(10, 'N_Papers')
for _, row in top_genera_pca.iterrows():
    idx = genus_features[genus_features['Genus'] == row['Genus']].index[0]
    ax.annotate(row['Genus'], (pca_results.iloc[idx]['PC1'], pca_results.iloc[idx]['PC2']), fontsize=7)

ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)' if len(pca.explained_variance_ratio_) > 1 else 'PC2')
ax.set_title('A. PCA Biplot with Clusters', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)
plt.colorbar(scatter, ax=ax, label='Cluster')

# 1b: Scree plot
ax = axes[0, 1]
ax.plot(range(1, len(pca.explained_variance_ratio_)+1), pca.explained_variance_ratio_,
       'o-', color=NEMATODE_COLORS['primary'], linewidth=2, markersize=6)
ax.set_xlabel('Principal Component')
ax.set_ylabel('Variance Explained')
ax.set_title('B. PCA Scree Plot', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

# 1c: Feature loadings
ax = axes[1, 0]
loadings = pca.components_[:2].T
loading_df = pd.DataFrame(loadings, columns=['PC1', 'PC2'], index=features_for_pca)
sns.heatmap(loading_df, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax,
           cbar_kws={'label': 'Loading'}, linewidths=0.5)
ax.set_title('C. Feature Loadings (PC1 & PC2)', fontweight='bold', loc='left')

# 1d: Cluster characteristics
ax = axes[1, 1]
cluster_means = genus_features.groupby('Cluster')[['Cit_Mean', 'N_Papers']].mean()
x = np.arange(len(cluster_means))
width = 0.35
ax.bar(x - width/2, cluster_means['Cit_Mean'], width, label='Mean Citations', alpha=0.7)
ax.bar(x + width/2, cluster_means['N_Papers']/10, width, label='Papers/10', alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels([f'C{i}' for i in cluster_means.index])
ax.set_xlabel('Cluster')
ax.set_ylabel('Value')
ax.set_title('D. Cluster Characteristics', fontweight='bold', loc='left')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig1_PCA_Clustering.png')
plt.close()

# FIGURE 2: Anomaly Detection and Patterns
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2a: Anomaly scores
ax = axes[0, 0]
anomaly_scores = iso_forest.score_samples(X_scaled)
colors_anom = ['red' if a == -1 else 'blue' for a in anomalies]
ax.scatter(range(len(anomaly_scores)), sorted(anomaly_scores), c=colors_anom, alpha=0.6)
ax.axhline(y=np.percentile(anomaly_scores, 10), color='red', linestyle='--', label='Anomaly threshold')
ax.set_xlabel('Genus (ranked)')
ax.set_ylabel('Anomaly Score')
ax.set_title('A. Anomaly Detection Scores', fontweight='bold', loc='left')
ax.legend()
ax.grid(True, alpha=0.3)

# 2b: Anomalous genera characteristics
ax = axes[0, 1]
if len(anomaly_genera) > 0:
    anom_df = genus_features[genus_features['Genus'].isin(anomaly_genera)].head(10)
    ax.barh(range(len(anom_df)), anom_df['Cit_Mean'],
           color=NEMATODE_COLORS['accent2'], alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.set_yticks(range(len(anom_df)))
    ax.set_yticklabels(anom_df['Genus'], fontsize=8)
    ax.set_xlabel('Mean Citations')
    ax.set_title('B. Anomalous Genera (High Impact)', fontweight='bold', loc='left')
    ax.grid(True, alpha=0.3, axis='x')

# 2c: Time series clustering
ax = axes[1, 0]
top_genera_ts = df.groupby('Genus')['pub_year'].count().nlargest(6).index
for genus in top_genera_ts:
    genus_yearly = df[df['Genus'] == genus].groupby('pub_year').size()
    color = GENUS_COLORS.get(genus, NEMATODE_COLORS['neutral1'])
    ax.plot(genus_yearly.index, genus_yearly.values, 'o-',
           label=genus, color=color, linewidth=2, markersize=3)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('C. Publication Time Series (Top 6 Genera)', fontweight='bold', loc='left')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# 2d: Correlation matrix
ax = axes[1, 1]
corr_features = ['Cit_Mean', 'N_Papers', 'N_Species', 'Years_Span']
corr_matrix = genus_features[corr_features].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax,
           cbar_kws={'label': 'Correlation'}, linewidths=0.5)
ax.set_title('D. Feature Correlation Matrix', fontweight='bold', loc='left')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig2_Anomaly_Detection.png')
plt.close()

print("\n[Part 7 Complete]")
print("="*70)
