"""
PART 4: Research Content Analysis - IMPROVED 6X
Nature-Quality Publication Standards

Focused analysis including:
1. Keyword frequency analysis
2. Research theme evolution over time
3. Emerging topics identification

Each figure is professionally designed for Nature publication
"""

import sys
sys.path.append('/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from wordcloud import WordCloud
from analysis_utils_improved import *
import re

# Configuration
DATA_FILE = '/home/user/DataAnalyz/TopTen/data/Final_Nema_Data.xlsx'
OUTPUT_DIR = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_4_ANALYSIS'

print("\n" + "="*70)
print("PART 4: RESEARCH CONTENT ANALYSIS - IMPROVED VERSION")
print("="*70 + "\n")

# Load data
print("Loading data...")
df = pd.read_excel(DATA_FILE, engine='openpyxl')
print(f"✓ Loaded {len(df):,} records")

# Standardize column names
df = df.rename(columns={
    'PubYear': 'pub_year',
    'Times cited': 'citations',
    'Abstract': 'abstract',
    'Title': 'title',
})

# Basic cleaning
df['pub_year'] = pd.to_numeric(df['pub_year'], errors='coerce')
df = df.dropna(subset=['pub_year'])
df['pub_year'] = df['pub_year'].astype(int)

# Apply filters
df_clean = apply_analysis_filters(df)

# Filter papers with abstracts
df_with_abstract = df_clean[df_clean['abstract'].notna()].copy()
print(f"\nPapers with abstracts: {len(df_with_abstract):,}")

# Clean abstracts
def clean_abstract(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    # Remove special characters
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

df_with_abstract['abstract_clean'] = df_with_abstract['abstract'].apply(clean_abstract)

# ============================================================================
# FIGURE 1: Top Keywords Analysis (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 1: Top Research Keywords")
print("="*70)

# Extract keywords using TF-IDF
tfidf = TfidfVectorizer(max_features=50, stop_words='english',
                        ngram_range=(1, 2), min_df=10, max_df=0.7)

tfidf_matrix = tfidf.fit_transform(df_with_abstract['abstract_clean'])
feature_names = tfidf.get_feature_names_out()
tfidf_scores = tfidf_matrix.sum(axis=0).A1

# Create keyword dataframe
keyword_df = pd.DataFrame({
    'Keyword': feature_names,
    'TF_IDF_Score': tfidf_scores
}).sort_values('TF_IDF_Score', ascending=False).head(30)

# Create figure with 2 panels
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# LEFT: Bar chart of top 20 keywords
top20_keywords = keyword_df.head(20)
y_pos = np.arange(len(top20_keywords))
colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, len(top20_keywords)))

ax1.barh(y_pos, top20_keywords['TF_IDF_Score'],
        color=colors_gradient, edgecolor='black', linewidth=0.5)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(top20_keywords['Keyword'], fontsize=9)
ax1.set_xlabel('TF-IDF Score', fontweight='bold')
ax1.set_title('A. Top 20 Research Keywords', fontweight='bold', loc='left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# RIGHT: Word cloud
keyword_dict = dict(zip(keyword_df['Keyword'], keyword_df['TF_IDF_Score']))
wordcloud = WordCloud(width=800, height=600, background_color='white',
                     colormap='viridis', relative_scaling=0.5,
                     min_font_size=10).generate_from_frequencies(keyword_dict)

ax2.imshow(wordcloud, interpolation='bilinear')
ax2.set_title('B. Research Keywords Word Cloud', fontweight='bold', pad=10)
ax2.axis('off')

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig1_Top_Keywords.png')
plt.close()

# Save data
keyword_df.to_csv(f'{OUTPUT_DIR}/Tables/Table1_Top_Keywords.csv', index=False)
print(f"✓ Extracted and saved top {len(keyword_df)} keywords")

# ============================================================================
# FIGURE 2: Temporal Research Theme Evolution (IMPROVED)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 2: Research Theme Evolution")
print("="*70)

# Define research themes based on keywords
themes = {
    'Molecular/Genetics': ['gene', 'genetic', 'molecular', 'dna', 'rna', 'genome', 'sequence'],
    'Plant Pathology': ['pathogen', 'disease', 'infection', 'resistance', 'susceptible', 'pathogenicity'],
    'Management/Control': ['control', 'management', 'nematicide', 'resistant', 'biocontrol', 'integrated'],
    'Ecology/Biology': ['population', 'ecology', 'distribution', 'diversity', 'biology', 'life cycle'],
    'Crop Impact': ['yield', 'damage', 'loss', 'crop', 'production', 'economic'],
    'Diagnostics': ['identification', 'detection', 'diagnosis', 'morphology', 'taxonomy', 'species']
}

# Count theme occurrences by year
theme_trends = []

for year in range(1980, 2024):
    year_data = df_with_abstract[df_with_abstract['pub_year'] == year]
    if len(year_data) > 0:
        year_abstracts = ' '.join(year_data['abstract_clean'].values)

        for theme, keywords in themes.items():
            count = sum(year_abstracts.count(kw) for kw in keywords)
            # Normalize by number of papers
            normalized_count = count / len(year_data)
            theme_trends.append({
                'Year': year,
                'Theme': theme,
                'Normalized_Count': normalized_count
            })

df_themes = pd.DataFrame(theme_trends)

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

theme_colors = {
    'Molecular/Genetics': '#d62728',
    'Plant Pathology': '#2ca02c',
    'Management/Control': '#ff7f0e',
    'Ecology/Biology': '#1f77b4',
    'Crop Impact': '#9467bd',
    'Diagnostics': '#8c564b'
}

for theme in themes.keys():
    theme_data = df_themes[df_themes['Theme'] == theme]
    # Apply smoothing
    theme_data = theme_data.sort_values('Year')
    theme_data['MA_3yr'] = theme_data['Normalized_Count'].rolling(window=3, center=True).mean()

    ax.plot(theme_data['Year'], theme_data['MA_3yr'],
           linewidth=2.5, label=theme, color=theme_colors[theme],
           alpha=0.8, marker='o', markersize=3, markevery=5)

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Theme Intensity (mentions per paper)', fontweight='bold')
ax.set_title('Evolution of Research Themes Over Time (1980-2023)',
            fontweight='bold', pad=15)
ax.legend(loc='best', frameon=True, fancybox=False, edgecolor='black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig2_Theme_Evolution.png')
plt.close()

# Save data
df_themes.to_csv(f'{OUTPUT_DIR}/Tables/Table2_Theme_Trends.csv', index=False)
print("✓ Analyzed theme evolution across 44 years")

# ============================================================================
# FIGURE 3: Emerging vs Declining Topics (NEW)
# ============================================================================

print("\n" + "="*70)
print("Generating Figure 3: Emerging vs Declining Topics")
print("="*70)

# Compare recent (2014-2023) vs older (2004-2013) periods
recent_abstracts = df_with_abstract[
    (df_with_abstract['pub_year'] >= 2014) & (df_with_abstract['pub_year'] <= 2023)
]['abstract_clean']

older_abstracts = df_with_abstract[
    (df_with_abstract['pub_year'] >= 2004) & (df_with_abstract['pub_year'] < 2014)
]['abstract_clean']

# Get top terms for each period
vectorizer = CountVectorizer(max_features=100, stop_words='english',
                             ngram_range=(1, 2), min_df=5)

recent_counts = vectorizer.fit_transform(recent_abstracts)
recent_vocab = vectorizer.get_feature_names_out()
recent_freq = recent_counts.sum(axis=0).A1 / len(recent_abstracts)

older_counts = vectorizer.fit_transform(older_abstracts)
older_vocab = vectorizer.get_feature_names_out()
older_freq = older_counts.sum(axis=0).A1 / len(older_abstracts)

# Find common terms and calculate change
common_terms = set(recent_vocab) & set(older_vocab)

term_changes = []
for term in common_terms:
    recent_idx = np.where(recent_vocab == term)[0][0]
    older_idx = np.where(older_vocab == term)[0][0]

    recent_f = recent_freq[recent_idx]
    older_f = older_freq[older_idx]

    if older_f > 0:
        pct_change = ((recent_f - older_f) / older_f) * 100
        term_changes.append({
            'Term': term,
            'Change_Percent': pct_change,
            'Recent_Freq': recent_f,
            'Older_Freq': older_f
        })

df_changes = pd.DataFrame(term_changes)

# Get top emerging and declining
emerging = df_changes.nlargest(15, 'Change_Percent')
declining = df_changes.nsmallest(15, 'Change_Percent')

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# LEFT: Emerging topics
y_pos = np.arange(len(emerging))
ax1.barh(y_pos, emerging['Change_Percent'], color='#2ca02c',
        edgecolor='black', linewidth=0.5, alpha=0.7)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(emerging['Term'], fontsize=9)
ax1.set_xlabel('Growth Rate (%)', fontweight='bold')
ax1.set_title('A. Emerging Topics (2014-2023 vs 2004-2013)',
             fontweight='bold', loc='left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# RIGHT: Declining topics
y_pos = np.arange(len(declining))
ax2.barh(y_pos, abs(declining['Change_Percent']), color='#d62728',
        edgecolor='black', linewidth=0.5, alpha=0.7)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(declining['Term'], fontsize=9)
ax2.set_xlabel('Decline Rate (%)', fontweight='bold')
ax2.set_title('B. Declining Topics (2014-2023 vs 2004-2013)',
             fontweight='bold', loc='left')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='x', alpha=0.3)
ax2.invert_xaxis()  # Declining shown as positive bars

plt.tight_layout()
save_figure(fig, f'{OUTPUT_DIR}/Charts/Fig3_Emerging_Declining_Topics.png')
plt.close()

# Save data
df_changes.to_csv(f'{OUTPUT_DIR}/Tables/Table3_Topic_Changes.csv', index=False)
print(f"✓ Identified emerging and declining topics")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("PART 4 ANALYSIS COMPLETE - IMPROVED VERSION")
print("="*70)
print("\nGenerated Figures:")
print("  ✓ Fig1: Top Research Keywords (bar + word cloud)")
print("  ✓ Fig2: Research Theme Evolution (line plot)")
print("  ✓ Fig3: Emerging vs Declining Topics (2-panel bars)")
print("\nAll figures saved in Nature-quality format (600 DPI)")
print("="*70 + "\n")
