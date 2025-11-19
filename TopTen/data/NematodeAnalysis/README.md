# Comprehensive Nematode Research Analysis Project

**Dataset:** ALL_NEMATODES_EXTRACTED_Sampled.csv
**Date Started:** November 19, 2025
**Branch:** claude/explore-topten-data-01M21re43YD7jzbTWRjGDRYm

---

## Project Overview

This is a comprehensive, publication-grade analysis of nematode research literature covering 7 major analytical dimensions:

1. **PART_1**: Species & Taxonomic Analysis
2. **PART_2**: Temporal & Trend Analysis
3. **PART_3**: Citation & Impact Analysis
4. **PART_4**: Research Content Analysis
5. **PART_5**: Geographic & Collaboration Analysis
6. **PART_6**: Economic & Agricultural Impact
7. **PART_7**: Advanced Statistical Analysis

---

## Data Specifications

### Source Data
- **File**: ALL_NEMATODES_EXTRACTED_Sampled.csv
- **Records**: 3,924 genus/species mentions
- **Columns**: 17 (publication metadata, citations, geographic data, text content)
- **Time Range**: 1975-2023

### Data Cleaning Rules
- **Exclude from species-level analysis**: sp, sp., spp, spp., species
- **Exclude genera**: Steinernema, Heterorhabditis
- **Country extraction**: Check country, factorials, and all relevant columns

---

## Folder Structure

Each PART_X_ANALYSIS folder contains:
```
PART_X_ANALYSIS/
├── Charts/          # Publication-quality figures (600 DPI)
├── Tables/          # CSV output tables
├── Code/            # Python, R, and Jupyter notebook files
├── Reports/         # Analysis reports (Word + PDF)
└── README.md        # Part-specific documentation
```

---

## Analysis Specifications

### PART_1: Species & Taxonomic Analysis
- Species discovery rate and taxonomic completeness
- Host-parasite relationship network (extracted from abstracts)
- Geographic distribution patterns
- Research bias analysis (over/understudied species and plant hosts)

### PART_2: Temporal & Trend Analysis
- Long-term research trends by genus and species
- 20-year forecasting for top 10 genera (3-5 species each)
- Publication date formatting and time series analysis

### PART_3: Citation & Impact Analysis
- High-impact paper identification
- Citation network and influential author identification
- Cross-genus citation patterns
- Journal impact factor correlation

### PART_4: Research Content Analysis
- Abstract text mining for research themes
- Keyword co-occurrence network analysis
- Research methodology evolution
- Molecular vs traditional approaches
- Emerging vs declining topics

### PART_5: Geographic & Collaboration Analysis
- Global research distribution mapping
- International collaboration networks
- Country-wise productivity and impact metrics
- Research migration patterns over time

### PART_6: Economic & Agricultural Impact
- Economic impact correlation with research investment
- Crop-specific nematode research patterns
- Outbreak correlation with research spikes
- Climate change impact on research priorities

### PART_7: Advanced Statistical Analysis
- Machine learning models for trend prediction
- Principal component analysis
- Time series clustering
- Anomaly detection in publication patterns

---

## Output Standards

### Figures
- **Resolution**: 600 DPI minimum
- **Format**: PNG and/or PDF
- **Color Scheme**: Consistent across all charts
- **Labeling**: Clear, publication-ready labels

### Code
- **Python**: Complete .py and .ipynb files
- **R**: Complete .R scripts replicating Python analysis
- **Documentation**: Comprehensive comments and explanations
- **Scalability**: Designed to work on larger datasets

### Reports
- **Word Format**: .docx with embedded figures
- **PDF Format**: .pdf for publication submission
- **Content**: Methods, results, figures, tables, interpretations

---

## Technical Requirements

### Python Packages
- pandas, numpy, matplotlib, seaborn
- scipy, scikit-learn, statsmodels
- networkx, nltk, spacy
- prophet, pmdarima (forecasting)
- geopandas, folium (mapping)
- python-docx, reportlab (reporting)

### R Packages
- tidyverse, ggplot2, dplyr
- forecast, prophet
- igraph, network
- tm, wordcloud, quanteda
- caret, randomForest
- knitr, rmarkdown

---

## Color Scheme

**Primary Palette** (to be defined and used consistently):
- Will be established in PART_1 and maintained across all analyses

---

## Progress Tracking

- [ ] PART_1: Species & Taxonomic Analysis
- [ ] PART_2: Temporal & Trend Analysis
- [ ] PART_3: Citation & Impact Analysis
- [ ] PART_4: Research Content Analysis
- [ ] PART_5: Geographic & Collaboration Analysis
- [ ] PART_6: Economic & Agricultural Impact
- [ ] PART_7: Advanced Statistical Analysis

---

## Notes

- All code is designed to scale to the complete dataset
- Consistent methodology across all analysis parts
- Publication-quality standards maintained throughout
- Cross-references between analysis parts where relevant

---

**Last Updated:** November 19, 2025
