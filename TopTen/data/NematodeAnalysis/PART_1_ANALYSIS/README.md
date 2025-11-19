# PART 1: Species & Taxonomic Analysis

**Comprehensive analysis of nematode species diversity, discovery patterns, geographic distribution, and research biases**

---

## Analysis Components

### 1. Species Discovery Rate & Taxonomic Completeness
- Annual and cumulative species discovery trends (1960-2023)
- 5-year moving average discovery rates
- Genus vs species diversity accumulation
- Species richness by genus

### 2. Taxonomic Completeness Assessment
- Publications per species ratio
- Research effort vs species diversity correlation
- Distribution of species richness across genera
- Most intensively studied species identification

### 3. Host-Parasite Relationship Network
- Extraction of 246,491 host-parasite associations from abstracts
- Host plant frequency analysis
- Network visualization of top genera-host relationships
- Top 20 most mentioned host plants

### 4. Geographic Distribution Patterns
- Research output by country (Top 20)
- Taxonomic diversity by geographic region
- Country × Genus distribution heatmap
- Citation impact vs geographic location

### 5. Research Bias Analysis - Nematode Species
- Identification of over/understudied genera and species
- Bias ratio calculations (observed vs expected)
- Classification into 4 bias categories
- Publication volume vs citation impact correlation

### 6. Research Bias Analysis - Plant Hosts
- Host plant research intensity analysis
- Over/understudied crop identification
- Bias distribution across plant species

---

## Generated Outputs

### Charts (600 DPI, PNG format)

1. **Fig1_Species_Discovery_Analysis.png** (1.2 MB)
   - 4-panel figure: Annual discovery, cumulative trends, diversity accumulation, species richness

2. **Fig2_Taxonomic_Completeness.png** (1.4 MB)
   - 4-panel figure: Research effort scatter, completeness scores, richness distribution, top species

3. **Fig3_Host_Parasite_Network.png** (3.2 MB)
   - 2-panel figure: Top host plants bar chart, network visualization

4. **Fig4_Geographic_Distribution.png** (1.8 MB)
   - 4-panel figure: Country output, diversity by country, genus×country heatmap, citation impact

5. **Fig5_Research_Bias_Analysis.png** (1.9 MB)
   - 4-panel figure: Genus bias, bias distribution pie, top species, volume vs impact

6. **Fig6_Host_Plant_Research_Bias.png** (858 KB)
   - 2-panel figure: Host plant research effort, bias category distribution

**R-generated figures:**
- FigR1_Species_Discovery_R.png
- FigR2_Top_Genera_R.png
- FigR3_Geographic_Distribution_R.png
- FigR4_Research_Bias_R.png

### CSV Tables

1. **species_discovery_by_year.csv** - Annual species discovery metrics
2. **genus_taxonomic_completeness.csv** - Completeness metrics by genus
3. **host_parasite_relationships.csv** (2.6 MB) - 246,491 host-parasite pairs
4. **geographic_distribution_by_genus.csv** - Country × Genus publication matrix
5. **country_research_summary.csv** - Country-level research metrics
6. **species_research_bias.csv** - Species-level bias analysis
7. **genus_research_bias.csv** - Genus-level bias analysis
8. **host_plant_research_bias.csv** (3.6 MB) - Plant host bias metrics

**R-generated tables:**
- species_discovery_by_year_R.csv
- genus_taxonomic_completeness_R.csv
- country_research_summary_R.csv
- genus_research_bias_R.csv
- species_research_bias_R.csv

---

## Code Files

### Python Scripts
- **part1_analysis.py** - Species discovery & taxonomic completeness
- **part1_analysis_continued.py** - Host-parasite networks & geographic distribution
- **part1_analysis_final.py** - Research bias analyses
- **run_part1_complete.py** - Master script to run all analyses

### R Scripts
- **part1_analysis.R** - Complete R implementation replicating Python analyses

### Utility Module
- **/NematodeAnalysis/analysis_utils.py** - Shared functions and styling

---

## Key Findings

### Species Discovery
- **672 unique species** analyzed (after filtering)
- **32 genera** included in analysis
- Discovery rate shows peaks in 2013 and 2020
- Cumulative discovery continues to rise, indicating ongoing taxonomic work

### Taxonomic Completeness
- **Meloidogyne**: Highest research intensity (697 records, 210 species mentions)
- **Xiphinema**: High species richness (377 records)
- **Pratylenchus**: Well-studied genus (345 records)
- Mean publications per species: varies widely by genus

### Host-Parasite Relationships
- **246,491 host-parasite associations** extracted from abstracts
- **Top hosts**: Tomato, wheat, potato, rice dominate research
- Strong associations between specific nematode genera and crop species
- Economic crops receive disproportionate research attention

### Geographic Patterns
- **USA leads**: 657 publications (21.7% of filtered dataset)
- **UK second**: 343 publications (11.4%)
- **European concentration**: Spain, Belgium, Netherlands well-represented
- Citation impact varies independently of publication volume

### Research Bias
- **Overstudied**: Meloidogyne, Heterodera (economic importance)
- **Adequately Studied**: Pratylenchus, Xiphinema
- **Understudied**: Many minor genera with limited species coverage
- **Plant host bias**: Major crops overstudied, minor crops neglected

---

## Methodology

### Data Filtering
- Excluded genera: Steinernema, Heterorhabditis (entomopathogenic)
- Excluded species names: sp, sp., spp, spp., species (non-specific)
- Final dataset: 3,022 records (77% of raw data)

### Host Extraction
- Pattern matching in abstracts for:
  - Binomial plant names (e.g., Solanum lycopersicum)
  - Common crop names (tomato, wheat, rice, etc.)
- Manual validation recommended for specific use cases

### Bias Calculation
- Expected publications = mean across all genera/species
- Bias ratio = observed / expected
- Categories: Severely Understudied (<0.25), Understudied (0.25-0.75), Adequately Studied (0.75-1.5), Overstudied (>1.5)

### Color Scheme
Consistent across all figures:
- Primary: #2E86AB (Deep Blue)
- Secondary: #A23B72 (Purple-Magenta)
- Accent1: #F18F01 (Orange)
- Accent2: #C73E1D (Red-Orange)
- Accent3: #6A994E (Green)

Genus-specific colors maintained throughout all visualizations.

---

## Usage

### Running Python Analysis
```bash
cd Code/
python3 run_part1_complete.py
```

### Running R Analysis
```r
source("Code/part1_analysis.R")
```

### Requirements
**Python**: pandas, numpy, matplotlib, seaborn, scipy, networkx
**R**: tidyverse, ggplot2, viridis, igraph, reshape2, zoo

---

## Scalability Notes

All code is designed to work with larger datasets:
- Efficient groupby operations
- Vectorized calculations
- Memory-conscious processing
- Parameterized file paths

To run on the complete dataset, simply update `DATA_PATH` in the scripts.

---

## Next Steps

For comprehensive reporting:
1. **Jupyter Notebook**: Create .ipynb with embedded analysis and visualizations
2. **Word Report**: Generate .docx with findings, figures, and interpretations
3. **PDF Report**: Convert to publication-ready PDF format

---

**Analysis Date**: November 19, 2025
**Data Source**: ALL_NEMATODES_EXTRACTED_Sampled.csv (3,924 records)
**Filtered Dataset**: 3,022 records (32 genera, 672 species)
