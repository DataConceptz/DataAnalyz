"""
Utility Functions for Nematode Research Analysis Project
Provides consistent styling, plotting, and data processing functions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONSISTENT COLOR SCHEME
# ============================================================================

# Primary color palette for all visualizations
NEMATODE_COLORS = {
    'primary': '#2E86AB',      # Deep blue
    'secondary': '#A23B72',    # Purple-magenta
    'accent1': '#F18F01',      # Orange
    'accent2': '#C73E1D',      # Red-orange
    'accent3': '#6A994E',      # Green
    'neutral1': '#5C6B73',     # Gray-blue
    'neutral2': '#9DB4C0',     # Light blue-gray
    'highlight': '#FFD23F',    # Yellow
}

# Extended palette for multiple categories
EXTENDED_PALETTE = [
    '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E',
    '#5C6B73', '#9DB4C0', '#FFD23F', '#06AED5', '#DD1C1A',
    '#8B5A3C', '#4A5859', '#86BBD8', '#F26419', '#33658A'
]

# Genus-specific colors (for consistency across analyses)
GENUS_COLORS = {
    'Meloidogyne': '#C73E1D',      # Red (root-knot)
    'Heterodera': '#2E86AB',       # Blue (cyst)
    'Pratylenchus': '#6A994E',     # Green (lesion)
    'Bursaphelenchus': '#F18F01',  # Orange (pine wilt)
    'Globodera': '#A23B72',        # Purple (potato cyst)
    'Xiphinema': '#5C6B73',        # Gray
    'Ditylenchus': '#FFD23F',      # Yellow
    'Radopholus': '#06AED5',       # Cyan
    'Longidorus': '#DD1C1A',       # Dark red
    'Aphelenchoides': '#8B5A3C',   # Brown
}

# ============================================================================
# PLOTTING CONFIGURATION
# ============================================================================

def set_publication_style():
    """Set matplotlib parameters for publication-quality figures"""
    rcParams['figure.dpi'] = 600
    rcParams['savefig.dpi'] = 600
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
    rcParams['font.size'] = 10
    rcParams['axes.labelsize'] = 11
    rcParams['axes.titlesize'] = 12
    rcParams['xtick.labelsize'] = 9
    rcParams['ytick.labelsize'] = 9
    rcParams['legend.fontsize'] = 9
    rcParams['figure.titlesize'] = 13
    rcParams['axes.linewidth'] = 1.0
    rcParams['grid.linewidth'] = 0.5
    rcParams['lines.linewidth'] = 1.5

    # Set seaborn style
    sns.set_style("whitegrid", {
        'grid.linestyle': '--',
        'grid.alpha': 0.3,
        'axes.edgecolor': '0.2',
    })
    sns.set_palette(EXTENDED_PALETTE)

def save_figure(fig, filepath, dpi=600, bbox_inches='tight'):
    """Save figure in publication quality"""
    fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches, facecolor='white', edgecolor='none')
    print(f"✓ Saved: {filepath}")

# ============================================================================
# DATA CLEANING FUNCTIONS
# ============================================================================

def clean_species_names(df, species_col='Species'):
    """
    Remove generic species names (sp, sp., spp, spp., species)
    Returns cleaned dataframe
    """
    exclude_species = ['sp', 'sp.', 'spp', 'spp.', 'species']
    df_clean = df[~df[species_col].str.lower().isin(exclude_species)].copy()
    return df_clean

def filter_excluded_genera(df, genus_col='Genus', exclude_list=None):
    """
    Remove excluded genera (Steinernema, Heterorhabditis by default)
    """
    if exclude_list is None:
        exclude_list = ['Steinernema', 'Heterorhabditis']
    df_clean = df[~df[genus_col].str.capitalize().isin([g.capitalize() for g in exclude_list])].copy()
    return df_clean

def apply_analysis_filters(df):
    """Apply all standard filters for analysis"""
    df = filter_excluded_genera(df)
    df = clean_species_names(df)
    return df

def extract_country_from_factorials(row):
    """
    Extract country information from factorials column if country column is empty
    """
    if pd.notna(row.get('country')) and row.get('country') != '':
        return row['country']

    if pd.notna(row.get('factorials')):
        parts = str(row['factorials']).split('=')
        if len(parts) >= 10:
            country_part = parts[9].strip()
            if country_part and country_part != 'NA':
                # Take first country if multiple
                return country_part.split(';')[0].strip()

    return None

def standardize_countries(df):
    """
    Standardize country names and extract from all available columns
    """
    df_copy = df.copy()

    # Extract country from factorials if missing
    df_copy['country_clean'] = df_copy.apply(extract_country_from_factorials, axis=1)

    # Standardize common variations
    country_mapping = {
        'United States': 'USA',
        'United Kingdom': 'UK',
        'The Netherlands': 'Netherlands',
    }

    df_copy['country_clean'] = df_copy['country_clean'].replace(country_mapping)

    return df_copy

# ============================================================================
# COUNT FIELD PROCESSING
# ============================================================================

def process_count_field(df, count_col='Count'):
    """
    Process Count field - convert to numeric where possible
    """
    df_copy = df.copy()

    # Try to convert to numeric, set non-numeric to NaN
    df_copy['count_numeric'] = pd.to_numeric(df_copy[count_col], errors='coerce')

    # Fill NaN with 1 (assuming single mention if not specified)
    df_copy['count_numeric'] = df_copy['count_numeric'].fillna(1).astype(int)

    return df_copy

# ============================================================================
# DATE PROCESSING
# ============================================================================

def standardize_publication_dates(df):
    """
    Standardize publication_date column to datetime
    """
    df_copy = df.copy()

    # Convert publication_date to datetime
    df_copy['publication_date'] = pd.to_datetime(df_copy['publication_date'], errors='coerce')

    # If publication_date is missing, use pub_year to create date
    mask = df_copy['publication_date'].isna()
    if mask.sum() > 0:
        df_copy.loc[mask, 'publication_date'] = pd.to_datetime(
            df_copy.loc[mask, 'pub_year'].astype(str) + '-01-01',
            errors='coerce'
        )

    return df_copy

# ============================================================================
# TEXT PROCESSING
# ============================================================================

def clean_text(text):
    """Clean and normalize text for analysis"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    # Remove special characters but keep spaces and hyphens
    import re
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def extract_host_plants(abstract):
    """
    Extract potential host plant names from abstract text
    Uses pattern matching for common plant name patterns
    """
    if pd.isna(abstract):
        return []

    import re

    # Common plant name patterns
    patterns = [
        r'\b([A-Z][a-z]+\s+[a-z]+)\b',  # Binomial names (e.g., Solanum lycopersicum)
        r'\b(tomato|potato|wheat|rice|corn|maize|barley|soybean|cotton|tobacco|pepper|eggplant|carrot|banana|coffee|sugar\s*cane|peanut|groundnut|bean|pea|chickpea|lentil|clover|alfalfa)\b',
    ]

    hosts = []
    for pattern in patterns:
        matches = re.findall(pattern, str(abstract), re.IGNORECASE)
        hosts.extend(matches)

    # Remove duplicates and return
    return list(set([h.strip() for h in hosts if h]))

# ============================================================================
# STATISTICAL HELPERS
# ============================================================================

def calculate_research_bias(df, group_col, count_col='count_numeric'):
    """
    Calculate research bias metrics (over/understudied species/genera)
    Returns dataframe with bias metrics
    """
    grouped = df.groupby(group_col).agg({
        count_col: 'sum',
        'pub_year': 'count',
        'citations': ['mean', 'sum']
    }).reset_index()

    grouped.columns = [group_col, 'total_count', 'n_publications', 'mean_citations', 'total_citations']

    # Calculate expected vs observed
    grouped['expected_pubs'] = grouped['n_publications'].mean()
    grouped['bias_ratio'] = grouped['n_publications'] / grouped['expected_pubs']
    grouped['bias_category'] = pd.cut(
        grouped['bias_ratio'],
        bins=[0, 0.25, 0.75, 1.5, float('inf')],
        labels=['Severely Understudied', 'Understudied', 'Adequately Studied', 'Overstudied']
    )

    return grouped.sort_values('n_publications', ascending=False)

# ============================================================================
# LOADING AND INITIALIZATION
# ============================================================================

def load_and_prepare_data(filepath):
    """
    Load CSV and apply initial preparation
    """
    df = pd.read_csv(filepath, low_memory=False)

    # Apply standard processing
    df = standardize_publication_dates(df)
    df = standardize_countries(df)
    df = process_count_field(df)

    print(f"✓ Loaded {len(df):,} records")
    print(f"✓ Date range: {df['pub_year'].min()} - {df['pub_year'].max()}")
    print(f"✓ Unique genera: {df['Genus'].nunique()}")
    print(f"✓ Unique species: {df['Species'].nunique()}")

    return df

# ============================================================================
# REPORT GENERATION HELPERS
# ============================================================================

def create_summary_table(df, title="Summary Statistics"):
    """Create a formatted summary statistics table"""
    summary = {
        'Total Records': len(df),
        'Unique Genera': df['Genus'].nunique() if 'Genus' in df.columns else 'N/A',
        'Unique Species': df['Species'].nunique() if 'Species' in df.columns else 'N/A',
        'Date Range': f"{df['pub_year'].min()}-{df['pub_year'].max()}" if 'pub_year' in df.columns else 'N/A',
        'Total Citations': df['citations'].sum() if 'citations' in df.columns else 'N/A',
        'Mean Citations': f"{df['citations'].mean():.1f}" if 'citations' in df.columns else 'N/A',
    }
    return pd.DataFrame([summary]).T.rename(columns={0: 'Value'})

# Initialize publication style when module is imported
set_publication_style()

print("✓ Nematode Analysis Utilities Loaded")
print("✓ Publication style configured (600 DPI)")
print("✓ Consistent color scheme initialized")
