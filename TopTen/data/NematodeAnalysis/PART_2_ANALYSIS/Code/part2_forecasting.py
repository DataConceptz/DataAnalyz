"""
PART 2: Temporal & Trend Analysis - Forecasting
================================================

20-year forecasting for top 10 genera and selected species
Uses multiple models and selects best performer

Author: Claude
Date: November 19, 2025
"""

import sys
sys.path.insert(0, '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.optimize import curve_fit
from analysis_utils import *
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_PATH = '/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv'
CHARTS_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Charts'
TABLES_PATH = '/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Tables'

print("\n" + "="*70)
print("PART 2: FORECASTING ANALYSIS (20 YEARS)")
print("="*70)

# ============================================================================
# LOAD DATA AND PREPARE
# ============================================================================

print("\n[4] Loading data for forecasting...")
df_raw = load_and_prepare_data(DATA_PATH)
df = apply_analysis_filters(df_raw)

# Get top 10 genera
top10_genera = df.groupby('Genus')['count_numeric'].sum().nlargest(10).index.tolist()

# Load species selection
species_selection = pd.read_csv(f'{TABLES_PATH}/selected_species_for_forecasting.csv')

# ============================================================================
# FORECASTING FUNCTIONS
# ============================================================================

def exponential_growth(x, a, b, c):
    """Exponential growth model"""
    return a * np.exp(b * x) + c

def logistic_growth(x, L, k, x0):
    """Logistic growth model"""
    return L / (1 + np.exp(-k * (x - x0)))

def linear_forecast(years, values, forecast_years=20):
    """Simple linear regression forecast"""
    X = np.array(years).reshape(-1, 1)
    y = np.array(values)

    model = LinearRegression()
    model.fit(X, y)

    future_years = np.arange(years.max() + 1, years.max() + forecast_years + 1).reshape(-1, 1)
    predictions = model.predict(future_years)

    # Calculate error metrics
    train_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, train_pred))
    mae = mean_absolute_error(y, train_pred)

    return future_years.flatten(), predictions, rmse, mae, 'Linear'

def polynomial_forecast(years, values, degree=2, forecast_years=20):
    """Polynomial regression forecast"""
    X = np.array(years).reshape(-1, 1)
    y = np.array(values)

    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    future_years = np.arange(years.max() + 1, years.max() + forecast_years + 1).reshape(-1, 1)
    future_poly = poly.transform(future_years)
    predictions = model.predict(future_poly)

    # Ensure non-negative predictions
    predictions = np.maximum(predictions, 0)

    train_pred = model.predict(X_poly)
    rmse = np.sqrt(mean_squared_error(y, train_pred))
    mae = mean_absolute_error(y, train_pred)

    return future_years.flatten(), predictions, rmse, mae, f'Polynomial (degree={degree})'

def exponential_forecast(years, values, forecast_years=20):
    """Exponential growth forecast"""
    try:
        X = np.array(years) - years.min()
        y = np.array(values)

        # Fit exponential model
        popt, _ = curve_fit(exponential_growth, X, y, p0=[1, 0.1, 0], maxfev=5000)

        future_X = np.arange(X.max() + 1, X.max() + forecast_years + 1)
        future_years_out = years.max() + np.arange(1, forecast_years + 1)
        predictions = exponential_growth(future_X, *popt)

        # Ensure reasonable predictions
        predictions = np.clip(predictions, 0, values.max() * 5)

        train_pred = exponential_growth(X, *popt)
        rmse = np.sqrt(mean_squared_error(y, train_pred))
        mae = mean_absolute_error(y, train_pred)

        return future_years_out, predictions, rmse, mae, 'Exponential'
    except:
        return None, None, np.inf, np.inf, 'Exponential'

def moving_average_forecast(years, values, window=5, forecast_years=20):
    """Moving average with trend forecast"""
    # Calculate trend from recent years
    recent_values = values[-window:]
    trend = np.mean(np.diff(recent_values)) if len(recent_values) > 1 else 0

    last_value = values[-1]
    predictions = [last_value + trend * i for i in range(1, forecast_years + 1)]
    predictions = np.maximum(predictions, 0)

    future_years = np.arange(years.max() + 1, years.max() + forecast_years + 1)

    # Simple RMSE using last known value
    rmse = np.std(values[-window:])
    mae = np.mean(np.abs(np.diff(values[-window:])))

    return future_years, np.array(predictions), rmse, mae, 'Moving Average'

def best_forecast_model(years, values, forecast_years=20):
    """Select best forecasting model based on RMSE"""
    models = []

    # Try all models
    for model_func in [linear_forecast, polynomial_forecast, exponential_forecast, moving_average_forecast]:
        try:
            result = model_func(years, values, forecast_years=forecast_years)
            if result[0] is not None:
                models.append({
                    'years': result[0],
                    'predictions': result[1],
                    'rmse': result[2],
                    'mae': result[3],
                    'name': result[4]
                })
        except:
            continue

    # Select best model (lowest RMSE)
    if models:
        best_model = min(models, key=lambda x: x['rmse'])
        return best_model
    else:
        # Fallback to linear if all fail
        return linear_forecast(years, values, forecast_years)

# ============================================================================
# GENUS-LEVEL FORECASTING
# ============================================================================

print("\n[5] Forecasting research trends for top 10 genera (20 years)...")

genus_forecasts = []

for genus in top10_genera:
    genus_data = df[df['Genus'] == genus].groupby('pub_year').agg({
        'count_numeric': 'sum'
    }).reset_index()
    genus_data.columns = ['Year', 'Count']

    if len(genus_data) >= 5:  # Need minimum data points
        years = genus_data['Year'].values
        counts = genus_data['Count'].values

        # Get best forecast
        forecast = best_forecast_model(years, counts, forecast_years=20)

        genus_forecasts.append({
            'Genus': genus,
            'Model': forecast['name'],
            'RMSE': forecast['rmse'],
            'Forecast_Years': forecast['years'],
            'Forecast_Values': forecast['predictions']
        })

        print(f"   {genus}: Best model = {forecast['name']}, RMSE = {forecast['rmse']:.2f}")

# Save forecast results
forecast_results = []
for fc in genus_forecasts:
    for year, value in zip(fc['Forecast_Years'], fc['Forecast_Values']):
        forecast_results.append({
            'Genus': fc['Genus'],
            'Year': int(year),
            'Forecasted_Count': value,
            'Model': fc['Model'],
            'RMSE': fc['RMSE']
        })

forecast_df = pd.DataFrame(forecast_results)
forecast_df.to_csv(f'{TABLES_PATH}/genus_forecasts_20years.csv', index=False)
print(f"   ✓ Saved: genus_forecasts_20years.csv")

# FIGURE 3: Genus Forecasting (Top 6 genera)
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for idx, genus in enumerate(top10_genera[:6]):
    ax = axes[idx]

    # Historical data
    hist_data = df[df['Genus'] == genus].groupby('pub_year').agg({
        'count_numeric': 'sum'
    }).reset_index()

    # Forecast data
    forecast_data = forecast_df[forecast_df['Genus'] == genus]

    # Plot historical
    color = GENUS_COLORS.get(genus, NEMATODE_COLORS['primary'])
    ax.plot(hist_data['pub_year'], hist_data['count_numeric'],
           'o-', color=color, linewidth=2, label='Historical', markersize=4)

    # Plot forecast
    ax.plot(forecast_data['Year'], forecast_data['Forecasted_Count'],
           '--', color=color, linewidth=2, alpha=0.7, label='Forecast')

    # Fill forecast area
    ax.fill_between(forecast_data['Year'], 0, forecast_data['Forecasted_Count'],
                    color=color, alpha=0.2)

    # Add vertical line at present
    current_year = hist_data['pub_year'].max()
    ax.axvline(current_year, color='red', linestyle=':', linewidth=1, alpha=0.5)

    ax.set_xlabel('Year')
    ax.set_ylabel('Occurrence Count')
    model_name = forecast_data['Model'].iloc[0] if len(forecast_data) > 0 else 'N/A'
    ax.set_title(f'{chr(65+idx)}. {genus}\n({model_name})', fontweight='bold', loc='left', fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig3_Genus_Forecasts_20years.png')
plt.close()

# ============================================================================
# SPECIES-LEVEL FORECASTING
# ============================================================================

print("\n[6] Forecasting for selected species...")

species_forecasts = []

for idx, row in species_selection.iterrows():
    genus = row['Genus']
    species = row['Species']

    species_data = df[(df['Genus'] == genus) & (df['Species'] == species)].groupby('pub_year').agg({
        'count_numeric': 'sum'
    }).reset_index()
    species_data.columns = ['Year', 'Count']

    if len(species_data) >= 5:
        years = species_data['Year'].values
        counts = species_data['Count'].values

        forecast = best_forecast_model(years, counts, forecast_years=20)

        species_forecasts.append({
            'Genus': genus,
            'Species': species,
            'Model': forecast['name'],
            'RMSE': forecast['rmse'],
            'Forecast_Years': forecast['years'],
            'Forecast_Values': forecast['predictions']
        })

print(f"   ✓ Forecasted {len(species_forecasts)} species")

# Save species forecasts
species_forecast_results = []
for fc in species_forecasts:
    for year, value in zip(fc['Forecast_Years'], fc['Forecast_Values']):
        species_forecast_results.append({
            'Genus': fc['Genus'],
            'Species': fc['Species'],
            'Year': int(year),
            'Forecasted_Count': value,
            'Model': fc['Model'],
            'RMSE': fc['RMSE']
        })

species_forecast_df = pd.DataFrame(species_forecast_results)
species_forecast_df.to_csv(f'{TABLES_PATH}/species_forecasts_20years.csv', index=False)
print(f"   ✓ Saved: species_forecasts_20years.csv")

# FIGURE 4: Species Forecasting Examples (Top 4 genera, 2 species each)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

for idx, genus in enumerate(top10_genera[:4]):
    ax = axes[idx]

    # Get top 2 species for this genus
    genus_species = species_selection[species_selection['Genus'] == genus]['Species'].values[:2]

    for species in genus_species:
        # Historical data
        hist_data = df[(df['Genus'] == genus) & (df['Species'] == species)].groupby('pub_year').agg({
            'count_numeric': 'sum'
        }).reset_index()

        if len(hist_data) > 0:
            # Forecast data
            forecast_data = species_forecast_df[
                (species_forecast_df['Genus'] == genus) &
                (species_forecast_df['Species'] == species)
            ]

            # Plot
            ax.plot(hist_data['pub_year'], hist_data['count_numeric'],
                   'o-', linewidth=2, label=f'{species} (hist)', markersize=3)

            if len(forecast_data) > 0:
                ax.plot(forecast_data['Year'], forecast_data['Forecasted_Count'],
                       '--', linewidth=2, alpha=0.7, label=f'{species} (forecast)')

    # Add vertical line at present
    ax.axvline(df['pub_year'].max(), color='red', linestyle=':', linewidth=1, alpha=0.5)

    ax.set_xlabel('Year')
    ax.set_ylabel('Occurrence Count')
    ax.set_title(f'{chr(65+idx)}. {genus} - Species Forecasts', fontweight='bold', loc='left')
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, f'{CHARTS_PATH}/Fig4_Species_Forecasts_Examples.png')
plt.close()

print("\n[Forecasting Complete]")
print("="*70)
