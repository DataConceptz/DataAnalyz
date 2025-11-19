# PART 2: Temporal & Trend Analysis

**Long-term research trends and 20-year forecasting for nematode research**

---

## Analyses Performed

1. **Long-term Research Trends by Genus** - Temporal patterns 1960-2023
2. **Species-Level Trends** - Top 3-5 species per genus trends
3. **20-Year Forecasting** - Projections for top 10 genera (2024-2043)
4. **Species Forecasting** - 21 selected species forecasted
5. **Model Comparison** - Multiple forecasting models tested
6. **Growth Rate Analysis** - Historical vs projected growth

---

## Outputs

### Figures (6 total, 600 DPI, 11 MB)
1. **Fig1_Genus_Temporal_Trends.png** (2.5 MB) - Stacked area, individual trends, growth rates, heatmap
2. **Fig2_Species_Temporal_Trends.png** (1.8 MB) - Species trends for top 4 genera
3. **Fig3_Genus_Forecasts_20years.png** (2.2 MB) - 20-year forecasts for top 6 genera
4. **Fig4_Species_Forecasts_Examples.png** (1.7 MB) - Species forecasting examples
5. **Fig5_Comprehensive_Temporal_Overview.png** (1.3 MB) - Overall trends, decades, acceleration
6. **Fig6_Forecast_Comparison.png** (1.7 MB) - Forecast trajectories, growth projections

**Plus 4+ R-generated figures**

### Tables (6 CSV files, 109 KB)
- genus_trends_by_year.csv - Annual genus trends
- species_trends_by_year.csv - Species temporal data
- selected_species_for_forecasting.csv - 21 species selected
- genus_forecasts_20years.csv - Genus-level forecasts (200 rows)
- species_forecasts_20years.csv - Species-level forecasts (400 rows)
- temporal_analysis_summary.csv - Summary statistics

---

## Key Findings

### Forecasting Models Used
- **Polynomial (degree=2)**: 6 genera (best for curved trends)
- **Moving Average**: 3 genera (stable recent trends)
- **Exponential**: 1 genus (rapid growth)

### Top 10 Genera Analyzed
1. Meloidogyne - Polynomial forecast, RMSE: 25.73
2. Pratylenchus - Moving Average, RMSE: 10.14
3. Xiphinema - Moving Average, RMSE: 8.36
4. Heterodera - Polynomial, RMSE: 7.43
5. Bursaphelenchus - Polynomial, RMSE: 8.94
6. Longidorus - Moving Average, RMSE: 3.44
7. Rotylenchus - Polynomial, RMSE: 7.76
8. Globodera - Polynomial, RMSE: 6.53
9. Aphelenchoides - Exponential, RMSE: 3.72
10. Ditylenchus - Polynomial, RMSE: 3.70

### 20-Year Projections (2024-2043)
- **Overall growth expected** for most genera
- **Meloidogyne** projected to remain dominant
- **Emerging interest** in Aphelenchoides (exponential model)
- **Stable research** patterns for minor genera

### Temporal Patterns
- **Peak historical year**: Varies by genus
- **Recent acceleration**: 2010-2023 shows increased activity
- **Decade trends**: 2020s showing strong research output

---

## Code Files

- **part2_analysis.py** - Trend analysis
- **part2_forecasting.py** - 20-year forecasting models
- **part2_summary.py** - Summary visualizations
- **part2_analysis.R** - R implementation with ARIMA forecasting
- **run_part2_complete.py** - Master runner

---

**Analysis Date**: November 19, 2025
**Data**: 3,022 filtered records (1960-2023)
**Forecast Horizon**: 20 years (2024-2043)
