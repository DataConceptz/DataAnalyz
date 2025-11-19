"""
PART 4: Research Content Analysis
==================================
Text mining, keyword analysis, methodology evolution, emerging topics
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from wordcloud import WordCloud
from analysis_utils import *

DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_4_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_4_ANALYSIS/Tables'

print("="*70)
print("PART 4: RESEARCH CONTENT ANALYSIS")
print("="*70)

df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# Clean abstracts
df['abstract_clean'] = df['abstract'].apply(clean_text)
df_with_abstract = df[df['abstract_clean'].str.len() > 50].copy()

print(f"   Records with abstracts: {len(df_with_abstract):,}")

# ============================================================================
# ANALYSIS 1: KEYWORD EXTRACTION & FREQUENCY
# ============================================================================

print("\n[1] Extracting keywords and themes...")

# TF-IDF for keyword extraction
tfidf = TfidfVectorizer(max_features=100, stop_words='english', ngram_range=(1, 2))
tfidf_matrix = tfidf.fit_transform(df_with_abstract['abstract_clean'])
feature_names = tfidf.get_feature_names_out()

# Get top keywords
tfidf_scores = tfidf_matrix.sum(axis=0).A1
keyword_scores = dict(zip(feature_names, tfidf_scores))
top_keywords = pd.DataFrame(sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)[:50],
                           columns=['Keyword', 'TF-IDF_Score'])
top_keywords.to_csv(f'{TABLES_PATH}/top_50_keywords.csv', index=False)

print(f"   ✓ Top keyword: {top_keywords.iloc[0]['Keyword']}")

# Method keywords
method_keywords = {
    'molecular': ['pcr', 'dna', 'rna', 'sequencing', 'molecular', 'genome', 'genetic', 'gene'],
    'microscopy': ['microscopy', 'microscope', 'imaging', 'morphology', 'morphological'],
    'bioassay': ['bioassay', 'assay', 'test', 'screening'],
    'field': ['field', 'survey', 'sampling', 'occurrence'],
    'greenhouse': ['greenhouse', 'pot', 'experimental']
}

method_counts = {}
for method, keywords in method_keywords.items():
    pattern = '|'.join(keywords)
    method_counts[method] = df_with_abstract['abstract_clean'].str.contains(pattern, regex=True).sum()

method_df = pd.DataFrame(list(method_counts.items()), columns=['Method', 'Count'])
method_df.to_csv(f'{TABLES_PATH}/methodology_keywords.csv', index=False)

# FIGURE 1: Keyword Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1a: Top keywords bar chart
ax = axes[0, 0]
top_30 = top_keywords.head(30)
ax.barh(range(len(top_30)), top_30['TF-IDF_Score'],
       color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(top_30)))
ax.set_yticklabels(top_30['Keyword'], fontsize=8)
ax.set_xlabel('TF-IDF Score')
ax.set_title('A. Top 30 Keywords (TF-IDF)', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='x')

# 1b: Word cloud
ax = axes[0, 1]
wordcloud = WordCloud(width=800, height=400, background_color='white',
                     colormap='viridis', max_words=100).generate_from_frequencies(keyword_scores)
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_title('B. Keyword Word Cloud', fontweight='bold', loc='left')
ax.axis('off')

# 1c: Methodology distribution
ax = axes[1, 0]
ax.bar(range(len(method_df)), method_df['Count'],
      color=[NEMATODE_COLORS['accent1'], NEMATODE_COLORS['accent2'],
             NEMATODE_COLORS['accent3'], NEMATODE_COLORS['secondary'],
             NEMATODE_COLORS['primary']], alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_xticks(range(len(method_df)))
ax.set_xticklabels(method_df['Method'], rotation=45, ha='right')
ax.set_ylabel('Number of Papers')
ax.set_title('C. Research Methodology Distribution', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3, axis='y')

# 1d: Keyword co-occurrence
ax = axes[1, 1]
top_10_kw = top_keywords.head(10)['Keyword'].tolist()
cooccur_matrix = pd.DataFrame(0, index=top_10_kw, columns=top_10_kw)

for _, row in df_with_abstract.iterrows():
    abstract = row['abstract_clean']
    present_kw = [kw for kw in top_10_kw if kw in abstract]
    for kw1 in present_kw:
        for kw2 in present_kw:
            if kw1 != kw2:
                cooccur_matrix.loc[kw1, kw2] += 1

sns.heatmap(cooccur_matrix, annot=True, fmt='g', cmap='Blues', ax=ax,
           cbar_kws={'label': 'Co-occurrences'}, linewidths=0.5)
ax.set_title('D. Keyword Co-occurrence Matrix (Top 10)', fontweight='bold', loc='left')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig1_Keyword_Analysis.png')
plt.close()

# ============================================================================
# ANALYSIS 2: TEMPORAL KEYWORD TRENDS
# ============================================================================

print("\n[2] Analyzing keyword evolution over time...")

# Track key themes over time
key_themes = {
    'Control': ['control', 'management', 'resistant', 'resistance'],
    'Genomics': ['genome', 'genomic', 'sequencing', 'transcriptome'],
    'Ecology': ['ecology', 'diversity', 'community', 'population'],
    'Pathology': ['pathogen', 'disease', 'infection', 'pathogenicity'],
    'Molecular': ['molecular', 'pcr', 'dna', 'gene']
}

theme_trends = []
for year in range(1990, 2024):
    year_data = df_with_abstract[df_with_abstract['pub_year'] == year]
    if len(year_data) > 0:
        for theme, keywords in key_themes.items():
            pattern = '|'.join(keywords)
            count = year_data['abstract_clean'].str.contains(pattern, regex=True).sum()
            theme_trends.append({'Year': year, 'Theme': theme, 'Count': count})

theme_df = pd.DataFrame(theme_trends)
theme_df.to_csv(f'{TABLES_PATH}/theme_evolution_over_time.csv', index=False)

# FIGURE 2: Temporal Trends
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2a: Theme evolution
ax = axes[0, 0]
for theme in key_themes.keys():
    theme_data = theme_df[theme_df['Theme'] == theme]
    ax.plot(theme_data['Year'], theme_data['Count'], 'o-',
           label=theme, linewidth=2, markersize=3)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('A. Research Theme Evolution', fontweight='bold', loc='left')
ax.legend()
ax.grid(True, alpha=0.3)

# 2b: Molecular vs traditional
ax = axes[0, 1]
molecular_years = []
traditional_years = []
for year in range(1990, 2024):
    year_data = df_with_abstract[df_with_abstract['pub_year'] == year]
    if len(year_data) > 0:
        mol = year_data['abstract_clean'].str.contains('pcr|dna|molecular|gene', regex=True).sum()
        trad = year_data['abstract_clean'].str.contains('microscopy|morphology', regex=True).sum()
        molecular_years.append({'Year': year, 'Count': mol, 'Type': 'Molecular'})
        traditional_years.append({'Year': year, 'Count': trad, 'Type': 'Traditional'})

mol_trad_df = pd.DataFrame(molecular_years + traditional_years)
mol_pivot = mol_trad_df.pivot(index='Year', columns='Type', values='Count')
mol_pivot.plot(kind='area', stacked=False, ax=ax, color=[NEMATODE_COLORS['accent1'], NEMATODE_COLORS['neutral1']], alpha=0.7)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('B. Molecular vs Traditional Approaches', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

# 2c: Emerging topics (recent 5 years)
ax = axes[1, 0]
recent = df_with_abstract[df_with_abstract['pub_year'] >= 2019]
old = df_with_abstract[df_with_abstract['pub_year'] < 2015]

emerging_keywords = {}
for keyword in top_keywords.head(20)['Keyword']:
    recent_freq = recent['abstract_clean'].str.contains(keyword, regex=False).sum() / len(recent)
    old_freq = old['abstract_clean'].str.contains(keyword, regex=False).sum() / len(old) if len(old) > 0 else 0
    growth = (recent_freq - old_freq) / old_freq * 100 if old_freq > 0 else 0
    emerging_keywords[keyword] = growth

emerging_df = pd.DataFrame(sorted(emerging_keywords.items(), key=lambda x: x[1], reverse=True)[:15],
                          columns=['Keyword', 'Growth_%'])
colors_growth = [NEMATODE_COLORS['accent3'] if x >= 0 else NEMATODE_COLORS['accent2']
                for x in emerging_df['Growth_%']]
ax.barh(range(len(emerging_df)), emerging_df['Growth_%'],
       color=colors_growth, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(emerging_df)))
ax.set_yticklabels(emerging_df['Keyword'], fontsize=8)
ax.set_xlabel('Growth Rate (%)')
ax.set_title('C. Emerging Topics (2019-2023 vs 2010-2014)', fontweight='bold', loc='left')
ax.axvline(0, color='black', linestyle='-', linewidth=1)
ax.grid(True, alpha=0.3, axis='x')

# 2d: Topic diversity over time
ax = axes[1, 1]
diversity_over_time = []
for year in range(1990, 2024, 3):
    year_data = df_with_abstract[(df_with_abstract['pub_year'] >= year) &
                                (df_with_abstract['pub_year'] < year+3)]
    if len(year_data) > 10:
        all_text = ' '.join(year_data['abstract_clean'].values)
        words = all_text.split()
        unique_words = len(set(words))
        diversity_over_time.append({'Year': year, 'Unique_Words': unique_words})

div_df = pd.DataFrame(diversity_over_time)
ax.plot(div_df['Year'], div_df['Unique_Words'], 'o-',
       color=NEMATODE_COLORS['secondary'], linewidth=2, markersize=4)
ax.set_xlabel('Year')
ax.set_ylabel('Unique Words in Abstracts')
ax.set_title('D. Research Vocabulary Diversity', fontweight='bold', loc='left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig2_Temporal_Content_Trends.png')
plt.close()

print("\n[Part 4 Complete]")
print("="*70)
print(f"✓ Charts: {CHARTS_PATH}/")
print(f"✓ Tables: {TABLES_PATH}/")
