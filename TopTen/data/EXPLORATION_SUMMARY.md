# TopTen/data Directory Exploration Summary

## Overview
Explored the `TopTen/data` directory containing nematode research publication data.

**Date:** November 19, 2025
**Branch:** claude/explore-topten-data-01M21re43YD7jzbTWRjGDRYm

---

## Files Found

1. **Final_Nema_Data.xlsx** (20.1 MB)
   - Primary dataset containing comprehensive nematode publication data

2. **describe.txt** (3 bytes)
   - Contains minimal content: "Hi"

---

## Dataset Structure

### Basic Statistics
- **Total Publications:** 19,072
- **Columns:** 62 (including 15 unnamed columns)
- **Data Range:** Publications from 1985 to 2023
- **Peak Publication Year:** 2022 (1,346 publications)

### Sheet Information
- **Single Sheet:** "Final_Nema_Data"

---

## Key Columns

### Publication Metadata
- Rank, Publication ID, DOI, PMID, PMCID, ISBN
- Title, Abstract, Acknowledgements, Funding
- Source title, Publisher, ISSN
- Publication dates (standard and online)
- Volume, Issue, Pagination
- Open Access status, Publication Type

### Author & Affiliation Data
- Authors, Authors (Raw Affiliation)
- Corresponding Authors, Authors Affiliations
- Research Organizations (standardized)
- GRID IDs
- Geographic data: City, State, Country

### Funding Information
- Funder, Funder Group, Funder Country
- UIDs of supporting grants
- Supporting Grants

### Citation Metrics
- Times cited
- Recent citations
- RCR (Relative Citation Ratio)
- FCR (Field Citation Ratio)
- Altmetric scores

### Biological Classification
- **Genus:** Primary taxonomic classification
- **Species:** Species-level identification
- **Count:** Occurrence count
- **Country:** Geographic data
- **MeSH terms:** Medical Subject Headings

### Additional Columns
- Unnamed: 47-61 (15 columns)
  - Contain additional country data for multi-country collaborations
  - Only 2-5 non-null values each
  - Represent publications with extensive international collaboration

---

## Top Genera (by publication count)

| Rank | Genus | Publications |
|------|-------|--------------|
| 1 | Meloidogyne | 7,277 |
| 2 | Heterodera | 3,100 |
| 3 | Pratylenchus | 1,622 |
| 4 | Bursaphelenchus | 1,533 |
| 5 | Globodera | 1,490 |
| 6 | Ditylenchus | 535 |
| 7 | Aphelenchoides | 534 |
| 8 | Helicotylenchus | 524 |
| 9 | Xiphinema | 376 |
| 10 | Rotylenchulus | 259 |
| 17 | **Anguina** | **95** |

---

## Top Species (by publication count)

| Rank | Species | Publications |
|------|---------|--------------|
| 1 | incognita | 3,836 |
| 2 | spp | 2,061 |
| 3 | javanica | 1,641 |
| 4 | glycines | 1,528 |
| 5 | xylophilus | 1,390 |
| 6 | pallida | 843 |
| 7 | schachtii | 737 |
| 8 | penetrans | 475 |
| 9 | rostochiensis | 464 |
| 10 | dipsaci | 312 |

---

## Geographic Distribution

### Top Research Countries
1. **United States:** 1,458 publications
2. **United Kingdom:** 771 publications
3. **China:** 721 publications
4. **Brazil:** 567 publications
5. **India:** 530 publications
6. **Japan:** 305 publications
7. **Egypt:** 276 publications
8. **Germany:** 163 publications
9. **Netherlands:** 160 publications
10. **Australia:** 157 publications

---

## Publication Characteristics

### Publication Types
- **Article:** 18,821 (98.7%)
- **Preprint:** 215 (1.1%)
- **Proceeding:** 35 (0.2%)
- **Monograph:** 1 (<0.1%)

### Open Access Distribution
- **Closed Access:** 11,229 (58.9%)
- **Gold OA:** 4,321 (22.7%)
- **Bronze OA:** 1,652 (8.7%)
- **Hybrid OA:** 1,068 (5.6%)
- **Green OA:** 802 (4.2%)

---

## Citation Metrics

### Times Cited Statistics
- **Mean:** 15.6 citations
- **Median:** 7 citations
- **Max:** 1,224 citations
- **75th percentile:** 18 citations

### Most Cited Publications

1. **1,224 citations** - "Top 10 plant parasitic nematodes" (2013)
   - Genus: Aphelenchoides, Species: besseyi

2. **1,146 citations** - "Sequencing of Aspergillus nidulans and comparative analysis" (2005)
   - Genus: Aphelenchoides, Species: oryzae

3. **964 citations** - "First Report of the Cereal Cyst Nematode Heterodera latipons" (2012)
   - Genus: Heterodera, Species: avenae

4. **906 citations** - "Genome sequence of the metazoan plant-parasitic nematode Meloidogyne incognita" (2008)
   - Genus: Meloidogyne, Species: incognita

5. **533 citations** - "First report of Bursaphelenchus xylophilus in Portugal and in Europe" (1999)
   - Genus: Bursaphelenchus, Species: xylophilus

### Relative Citation Ratio (RCR)
- **Publications with RCR:** 6,496 (34.1%)
- **Mean RCR:** 0.80
- **Median RCR:** 0.52
- **Max RCR:** 25.55

### Altmetric Scores
- **Publications with Altmetric scores:** 5,083 (26.6%)
- **Mean Altmetric:** 5.0
- **Median Altmetric:** 3.0
- **Max Altmetric:** 692

---

## Funding Analysis

### Funding Coverage
- **Publications with funding info:** 7,220 (37.9%)

### Top 10 Funders

1. **National Institute of Food and Agriculture (NIFA):** 1,629 grants
2. **National Natural Science Foundation of China (NSFC):** 958 grants
3. **Agricultural Research Service (ARS):** 838 grants
4. **European Commission:** 549 grants
5. **National Council for Scientific and Technological Development (CNPq, Brazil):** 519 grants
6. **Ministry of Science and Technology (China):** 488 grants
7. **USDA:** 473 grants
8. **CAPES (Brazil):** 357 grants
9. **Japan Society for the Promotion of Science (JSPS):** 230 grants
10. **Biotechnology and Biological Sciences Research Council (BBSRC, UK):** 176 grants

---

## Publication Timeline

### Recent Years (2018-2023)
- 2023: 732 publications
- 2022: 1,346 publications (peak)
- 2021: 1,139 publications
- 2020: 1,104 publications
- 2019: 928 publications
- 2018: 721 publications

### Historical Coverage
- Dataset spans from **1985 to 2023** (38 years)
- Oldest publication: 1985
- Most recent: 2023

---

## Data Quality Notes

### Missing Data
- Various columns have missing values, particularly:
  - ISBN, PMCID (mostly N/A for journal articles)
  - Anthology title, Book editors (N/A for non-book publications)
  - RCR, FCR, Altmetric (not available for all publications)
  - Funding information (62% of publications lack funding data)

### Unnamed Columns (47-61)
- These columns appear to store overflow country data
- Used for publications with extensive international collaboration
- Most publications have only 1-2 countries; these columns handle edge cases with 10+ collaborating countries

---

## Key Insights

1. **Research Focus:** Meloidogyne (root-knot nematodes) dominates the dataset with 38% of all publications
   - M. incognita alone accounts for 20% of all publications

2. **Geographic Concentration:**
   - United States leads in publication output
   - Strong representation from UK, China, Brazil, and India
   - Reflects global agricultural concerns with plant-parasitic nematodes

3. **Open Access Trend:**
   - 41% of publications are open access
   - Gold OA is the most common open access route

4. **Citation Impact:**
   - Highly skewed distribution (mean: 15.6, median: 7)
   - Top papers are highly influential (>1000 citations)
   - Review papers and genome sequencing studies tend to have highest impact

5. **Funding:**
   - US and Chinese funding agencies dominate
   - Agricultural research organizations are primary funders
   - Only 38% of publications report funding information

6. **Publication Growth:**
   - Peak in 2022 suggests active research area
   - Steady growth from 2010-2022
   - Slight decline in 2023 (may be due to data collection timing)

---

## Recommendations for Analysis

1. **Temporal Analysis:**
   - Track research trends by genus/species over time
   - Analyze citation patterns by publication year

2. **Geographic Analysis:**
   - Map collaboration networks between countries
   - Identify regional research priorities

3. **Impact Analysis:**
   - Correlate funding with citation metrics
   - Analyze OA vs. closed access citation patterns

4. **Taxonomic Analysis:**
   - Deep dive into top genera (Meloidogyne, Heterodera, etc.)
   - Identify emerging species of research interest

5. **Data Cleaning:**
   - Consolidate duplicate country entries (e.g., "United States; United States")
   - Clean up unnamed columns or parse into proper structure
   - Investigate character encoding issues in some titles/abstracts

---

## Technical Details

- **File Format:** Excel (.xlsx)
- **File Size:** 20,079,554 bytes (~20.1 MB)
- **Readable with:** pandas, openpyxl
- **Location:** `/home/user/DataAnalyz/TopTen/data/Final_Nema_Data.xlsx`
