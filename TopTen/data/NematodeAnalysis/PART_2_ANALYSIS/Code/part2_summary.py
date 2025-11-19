"""
PART 2: Temporal & Trend Analysis - Summary Visualizations
===========================================================

Additional trend analyses and comparative visualizations

Author: Claude
Date: November 19, 2025
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from analysis_utils import *
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Tables'

print("\n" + "="*70)
print("PART 2: SUMMARY ANALYSIS & VISUALIZATIONS")
print("="*70)

# Load data
df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# Load forecast results
genus_forecasts = pd.read_csv(f'{TABLES_PATH}/genus_forecasts_20years.csv')
species_forecasts = pd.read_csv(f'{TABLES_PATH}/species_forecasts_20years.csv')

top10_genera = df.groupby('Genus')['count_numeric'].sum().nlargest(10).index.tolist()

# ============================================================================
# FIGURE 5: COMPREHENSIVE TEMPORAL OVERVIEW
# ============================================================================

print("\n[7] Creating comprehensive temporal overview...")

fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 5a: Overall publication trend
ax1 = fig.add_subplot(gs[0, :2])
overall_trend = df.groupby('pub_year').size().reset_index()
overall_trend.columns = ['Year', 'Count']

ax1.bar(overall_trend['Year'], overall_trend['Count'],
       color=NEMATODE_COLORS['primary'], alpha=0.7, edgecolor='black', linewidth=0.5)

# Add trend line
z = np.polyfit(overall_trend['Year'], overall_trend['Count'], 2)
p = np.poly1d(z)
ax1.plot(overall_trend['Year'], p(overall_trend['Year']),
        "r--", linewidth=2, label='Polynomial Trend')

ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Records')
ax1.set_title('A. Overall Research Output Trend', fontweight='bold', loc='left')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 5b: Decade comparison
ax2 = fig.add_subplot(gs[0, 2])
df['Decade'] = (df['pub_year'] // 10) * 10
decade_counts = df.groupby('Decade').size().reset_index()
decade_counts.columns = ['Decade', 'Count']
decade_labels = [f"{int(d)}s" for d in decade_counts['Decade']]

ax2.bar(range(len(decade_counts)), decade_counts['Count'],
       color=NEMATODE_COLORS['accent1'], alpha=0.7, edgecolor='black', linewidth=0.5)
ax2.set_xticks(range(len(decade_counts)))
ax2.set_xticklabels(decade_labels, rotation=45, ha='right')
ax2.set_ylabel('Total Records')
ax2.set_title('B. Research by Decade', fontweight='bold', loc='left')
ax2.grid(True, alpha=0.3, axis='y')

# 5c: Research acceleration (year-over-year change)
ax3 = fig.add_subplot(gs[1, :2])
overall_trend['YoY_Change'] = overall_trend['Count'].diff()
overall_trend['YoY_Pct'] = overall_trend['Count'].pct_change() * 100

colors_yoy = [NEMATODE_COLORS['accent3'] if x >= 0 else NEMATODE_COLORS['accent2']
             for x in overall_trend['YoY_Change'].fillna(0)]

ax3.bar(overall_trend['Year'], overall_trend['YoY_Change'],
       color=colors_yoy, alpha=0.7, edgecolor='black', linewidth=0.5)
ax3.axhline(0, color='black', linestyle='-', linewidth=1)
ax3.set_xlabel('Year')
ax3.set_ylabel('Year-over-Year Change')
ax3.set_title('C. Research Acceleration (Annual Change)', fontweight='bold', loc='left')
ax3.grid(True, alpha=0.3)

# 5d: Forecast summary (total projected research 2024-2043)
ax4 = fig.add_subplot(gs[1, 2])
forecast_summary = genus_forecasts.groupby('Year')['Forecasted_Count'].sum().reset_index()

ax4.plot(forecast_summary['Year'], forecast_summary['Forecasted_Count'],
        'o-', color=NEMATODE_COLORS['secondary'], linewidth=2, markersize=4)
ax4.fill_between(forecast_summary['Year'], 0, forecast_summary['Forecasted_Count'],
                color=NEMATODE_COLORS['secondary'], alpha=0.3)
ax4.set_xlabel('Year')
ax4.set_ylabel('Projected Count')
ax4.set_title('D. Total Projected Research\n(Top 10 Genera)', fontweight='bold', loc='left', fontsize=10)
ax4.grid(True, alpha=0.3)

# 5e: Model performance comparison
ax5 = fig.add_subplot(gs[2, :])
model_performance = genus_forecasts.groupby(['Genus', 'Model'])['RMSE'].first().reset_index()

genera_sorted = model_performance.groupby('Genus')['RMSE'].mean().sort_values().index
model_pivot = model_performance.pivot_table(index='Genus', columns='Model', values='RMSE', fill_value=0)
model_pivot = model_pivot.reindex(genera_sorted)

x = np.arange(len(model_pivot))
width = 0.2
models = model_pivot.columns

for idx, model in enumerate(models):
    offset = (idx - len(models)/2) * width
    ax5.bar(x + offset, model_pivot[model], width, label=model, alpha=0.7, edgecolor='black', linewidth=0.5)

ax5.set_xticks(x)
ax5.set_xticklabels(model_pivot.index, rotation=45, ha='right')
ax5.set_ylabel('RMSE')
ax5.set_xlabel('Genus')
ax5.set_title('E. Forecasting Model Performance (RMSE by Genus)', fontweight='bold', loc='left')
ax5.legend(fontsize=8, ncol=len(models))
ax5.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig5_Comprehensive_Temporal_Overview.png')
plt.close()

# ============================================================================
# FIGURE 6: FORECAST COMPARISON & UNCERTAINTY
# ============================================================================

print("\n[8] Creating forecast comparison visualization...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 6a: Forecast trajectories (all top 10 genera)
ax = axes[0, 0]
for genus in top10_genera:
    forecast_data = genus_forecasts[genus_forecasts['Genus'] == genus]
    color = GENUS_COLORS.get(genus, NEMATODE_COLORS['neutral1'])
    ax.plot(forecast_data['Year'], forecast_data['Forecasted_Count'],
           linewidth=2, label=genus, color=color, alpha=0.7)

ax.set_xlabel('Year')
ax.set_ylabel('Forecasted Count')
ax.set_title('A. Forecast Trajectories (2024-2043)', fontweight='bold', loc='left')
ax.legend(fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)

# 6b: Projected growth rates
ax = axes[0, 1]
growth_projections = []
for genus in top10_genera:
    forecast_data = genus_forecasts[genus_forecasts['Genus'] == genus].sort_values('Year')
    if len(forecast_data) >= 2:
        first_year = forecast_data.iloc[0]['Forecasted_Count']
        last_year = forecast_data.iloc[-1]['Forecasted_Count']
        total_growth = ((last_year - first_year) / first_year * 100) if first_year > 0 else 0
        growth_projections.append({'Genus': genus, 'Growth': total_growth})

growth_df = pd.DataFrame(growth_projections).sort_values('Growth', ascending=False)
colors_growth = [GENUS_COLORS.get(g, NEMATODE_COLORS['neutral1']) for g in growth_df['Genus']]

ax.barh(range(len(growth_df)), growth_df['Growth'],
       color=colors_growth, alpha=0.7, edgecolor='black', linewidth=0.5)
ax.set_yticks(range(len(growth_df)))
ax.set_yticklabels(growth_df['Genus'])
ax.set_xlabel('Projected Growth (%)')
ax.set_title('B. 20-Year Growth Projections', fontweight='bold', loc='left')
ax.axvline(0, color='black', linestyle='-', linewidth=1)
ax.grid(True, alpha=0.3, axis='x')

# 6c: Forecast vs Historical (Selected genera)
ax = axes[1, 0]
for genus in top10_genera[:3]:
    # Historical
    hist_data = df[df['Genus'] == genus].groupby('pub_year')['count_numeric'].sum().reset_index()
    # Forecast
    forecast_data = genus_forecasts[genus_forecasts['Genus'] == genus]

    color = GENUS_COLORS.get(genus, NEMATODE_COLORS['primary'])
    ax.plot(hist_data['pub_year'], hist_data['count_numeric'],
           'o-', color=color, linewidth=2, label=f'{genus} (hist)', markersize=3)
    ax.plot(forecast_data['Year'], forecast_data['Forecasted_Count'],
           '--', color=color, linewidth=2, alpha=0.7)

ax.axvline(df['pub_year'].max(), color='red', linestyle=':', linewidth=1.5, label='Present')
ax.set_xlabel('Year')
ax.set_ylabel('Count')
ax.set_title('C. Historical vs Forecast (Top 3 Genera)', fontweight='bold', loc='left')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# 6d: Model selection frequency
ax = axes[1, 1]
model_counts = genus_forecasts.groupby('Model')['Genus'].nunique().reset_index()
model_counts.columns = ['Model', 'Count']

colors_model = [NEMATODE_COLORS['accent1'], NEMATODE_COLORS['accent2'],
               NEMATODE_COLORS['accent3'], NEMATODE_COLORS['primary']][:len(model_counts)]

ax.pie(model_counts['Count'], labels=model_counts['Model'], autopct='%1.1f%%',
      colors=colors_model, startangle=90)
ax.set_title('D. Best Model Selection\n(by Genus)', fontweight='bold', loc='left', fontsize=10)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig6_Forecast_Comparison.png')
plt.close()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n[9] Generating summary statistics...")

# Overall statistics
summary_stats = {
    'Total_Records_Analyzed': len(df),
    'Time_Span_Years': df['pub_year'].max() - df['pub_year'].min(),
    'Average_Annual_Records': len(df) / (df['pub_year'].max() - df['pub_year'].min()),
    'Peak_Year': df.groupby('pub_year').size().idxmax(),
    'Peak_Year_Count': df.groupby('pub_year').size().max(),
    'Genera_Forecasted': len(top10_genera),
    'Species_Forecasted': len(species_forecasts),
    'Forecast_Horizon_Years': 20
}

summary_df = pd.DataFrame([summary_stats]).T
summary_df.columns = ['Value']
summary_df.to_csv(f'{TABLES_PATH}/temporal_analysis_summary.csv')
print(f"   ✓ Saved: temporal_analysis_summary.csv")

print("\n" + "="*70)
print("PART 2 ANALYSIS COMPLETE!")
print("="*70)
print(f"\n✓ Charts saved to: {CHARTS_PATH}/")
print(f"✓ Tables saved to: {TABLES_PATH}/")
print("\nGenerated Figures:")
print("  - Fig1_Genus_Temporal_Trends.png")
print("  - Fig2_Species_Temporal_Trends.png")
print("  - Fig3_Genus_Forecasts_20years.png")
print("  - Fig4_Species_Forecasts_Examples.png")
print("  - Fig5_Comprehensive_Temporal_Overview.png")
print("  - Fig6_Forecast_Comparison.png")
