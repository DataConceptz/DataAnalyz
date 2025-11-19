# ALL_NEMATODES_EXTRACTED_Sampled.csv - Detailed Analysis

## Overview
This file represents an **extracted and sampled** subset of the nematode publication dataset, where genus/species mentions have been extracted from publications.

**Date Analyzed:** November 19, 2025
**File Size:** 14 MB
**Format:** CSV

---

## Key Differences from Final_Nema_Data.xlsx

### Size & Structure
| Metric | CSV File | Excel File | Ratio |
|--------|----------|------------|-------|
| Total Records | 3,924 | 19,072 | 20.6% |
| Columns | 17 | 62 | 27.4% |
| Average Citations | 73.2 | 15.6 | 4.7× higher |
| Median Citations | 19 | 7 | 2.7× higher |

### Data Representation
- **Excel File:** One row per publication with comprehensive metadata
- **CSV File:** One row per genus/species mention (publications can appear multiple times)

---

## Dataset Structure

### Columns (17)
1. **publication_date** - Publication date (various formats)
2. **pub_year** - Publication year (integer)
3. **title** - Publication title
4. **abstract** - Abstract text
5. **journal** - Journal name
6. **publisher** - Publisher name
7. **me_sh_terms** - Medical Subject Headings (MeSH terms)
8. **institution** - Research institution(s)
9. **city** - City of institution
10. **state** - State/province (if applicable)
11. **country** - Country of institution
12. **citations** - Number of citations
13. **factorials** - Concatenated metadata string (delimited by " = ")
14. **text** - Full text or extended abstract
15. **Genus** - Nematode genus
16. **Species** - Nematode species
17. **Count** - Number of genus/species mentions extracted (mostly numeric, 1 text record)

---

## Extraction Methodology

### Multiple Mentions Per Publication
- **761 unique publications** appear multiple times
- **3,102 total duplicate records** (79% of dataset)
- Publications mentioning multiple genera/species are represented by multiple rows

### Example
**Publication:** "A First Report of Anguina pacificae in Ireland"
- Appears 2 times with different species mentions:
  - Anguina agropyri (appears twice as separate records)

**Publication:** "(Nota n.º 4) Sôbre os nematódeos que parasitam o pessegueiro"
- Appears 4 times:
  - Xiphinema campinense (3 records)
  - Xiphinema krugi (1 record)

### Count Field Distribution
| Count | Records | Meaning |
|-------|---------|---------|
| 1 | 3,154 | Single genus/species mention |
| 2 | 484 | Two mentions |
| 3 | 154 | Three mentions |
| 4 | 57 | Four mentions |
| 5 | 38 | Five mentions |
| 6 | 24 | Six mentions |
| 7 | 9 | Seven mentions |
| 8-15 | 3 | Multiple mentions (rare) |
| text | 1 | One anomalous text entry |

---

## Genus Distribution

### Top 20 Genera

| Rank | Genus | Records | % of Dataset |
|------|-------|---------|--------------|
| 1 | Meloidogyne | 697 | 17.8% |
| 2 | Xiphinema | 377 | 9.6% |
| 3 | Pratylenchus | 345 | 8.8% |
| 4 | **Steinernema** | **298** | **7.6%** |
| 5 | Heterodera | 244 | 6.2% |
| 6 | Longidorus | 181 | 4.6% |
| 7 | Bursaphelenchus | 155 | 3.9% |
| 8 | Rotylenchus | 152 | 3.9% |
| 9 | **Heterorhabditis** | **136** | **3.5%** |
| 10 | Aphelenchoides | 129 | 3.3% |
| 11 | Globodera | 124 | 3.2% |
| 12 | Helicotylenchus | 97 | 2.5% |
| 13 | Ditylenchus | 90 | 2.3% |
| 14 | Tylenchorhynchus | 77 | 2.0% |
| 15 | Trichodorus | 74 | 1.9% |
| 16 | Radopholus | 69 | 1.8% |
| 17 | **Anguina** | **66** | **1.7%** |
| 18 | Scutellonema | 66 | 1.7% |
| 19 | Rotylenchulus | 61 | 1.6% |
| 20 | Hoplolaimus | 58 | 1.5% |

**Notable:** This dataset includes significant coverage of **entomopathogenic nematodes** (Steinernema, Heterorhabditis), which are less prominent in the Excel file.

---

## Species Distribution

### Top 20 Species

| Rank | Species | Records |
|------|---------|---------|
| 1 | incognita | 210 |
| 2 | spp. | 150 |
| 3 | sp | 128 |
| 4 | sp. | 105 |
| 5 | species | 90 |
| 6 | javanica | 79 |
| 7 | **carpocapsae** | **55** |
| 8 | xylophilus | 55 |
| 9 | glycines | 52 |
| 10 | **feltiae** | **43** |
| 11 | rostochiensis | 35 |
| 12 | similis | 35 |
| 13 | **bacteriophora** | **35** |
| 14 | penetrans | 35 |
| 15 | arenaria | 34 |
| 16 | spp | 34 |
| 17 | pallida | 33 |
| 18 | hapla | 33 |
| 19 | schachtii | 28 |
| 20 | reniformis | 28 |

**Note:** Bolded species are entomopathogenic (biocontrol agents).

---

## Entomopathogenic Nematodes Analysis

### Overview
- **Total records:** 434 (11.1% of dataset)
- **Steinernema:** 298 records
- **Heterorhabditis:** 136 records

### Steinernema Species (Top 10)
1. carpocapsae - 55
2. feltiae - 43
3. glaseri - 8
4. sp. - 7
5. spp. - 6
6. riobrave - 6
7. species - 5
8. diaprepesi - 4
9. abbasi - 4
10. kraussei - 4

### Heterorhabditis Species (Top 10)
1. bacteriophora - 35
2. indica - 10
3. sp. - 6
4. megidis - 6
5. spp. - 5
6. zealandica - 5
7. species - 4
8. amazonensis - 4
9. atacamensis - 3
10. heliothidis - 3

**Significance:** This dataset provides better coverage of entomopathogenic nematodes used in biological control, compared to the plant-parasitic focus of the Excel file.

---

## Anguina (Seed Gall Nematodes) Analysis

### Basic Statistics
- **Total records:** 66
- **Unique species:** 21
- **Citation range:** 0-150

### Species Distribution
| Species | Records |
|---------|---------|
| tritici | 5 |
| funesta | 4 |
| agrostis | 4 |
| species | 3 |
| obesa | 3 |
| microlaenae | 3 |
| limberi | 3 |
| pacificae | 3 |
| plantaginis | 3 |
| spp. | 3 |
| radicicola | 3 |
| sp. | 3 |
| woodi | 3 |
| graminis | 3 |
| australis | 3 |
| oryzae | 3 |
| paludicola | 3 |
| parietinus | 3 |
| agropyronifloris | 3 |
| agropyri | 2 |
| Others | 1 each |

### Top Cited Anguina Publications

1. **150 citations** (1995) - **A. agrostis**
   - "Endogenous toxins and mycotoxins in forage grasses and their effects on livestock"

2. **85 citations** (1990) - **A. tritici**
   - "Nematicidal activity of some essential plant oils"

3. **73 citations** (1981) - **A. tritici**
   - "Anhydrobiosis in nematodes—I. The role of glycerol myo-inositol and trehalose during dehydration"

4. **52 citations** (1992) - **A. spp.**
   - "Clavibacter toxicus sp. nov., the Bacterium Responsible for Annual Ryegrass Toxicity"

5. **41 citations** (1975) - **A. sp**
   - "WIMMERA RYE GRASS TOXICITY IN WESTERN AUSTRALIA"

### Publication Timeline
- **Earliest:** 1975 (3 records)
- **Most productive year:** 2016 (9 records)
- **Recent years:** Active through 2023
- **Historical clusters:** 2001, 2002, 2005, 2015, 2016 (7-9 records each)

---

## Geographic Distribution

### Top 20 Countries

| Rank | Country | Records |
|------|---------|---------|
| 1 | United States | 657 |
| 2 | United Kingdom | 343 |
| 3 | Spain | 220 |
| 4 | Belgium | 193 |
| 5 | Iran | 162 |
| 6 | China | 158 |
| 7 | Brazil | 113 |
| 8 | Australia | 109 |
| 9 | France | 106 |
| 10 | South Africa | 102 |
| 11 | Germany | 82 |
| 12 | Japan | 80 |
| 13 | India | 78 |
| 14 | Netherlands | 62 |
| 15 | Egypt | 48 |
| 16 | Italy | 45 |
| 17 | Poland | 36 |
| 18 | Russia | 32 |
| 19 | Kenya | 32 |
| 20 | New Zealand | 29 |

**Notable differences from Excel file:**
- Belgium ranks 4th (vs. not in top 20 in Excel)
- Iran ranks 5th (vs. 6th in Excel)
- Spain ranks 3rd (vs. 17th in Excel)

---

## Publication Sources

### Top 15 Journals

| Rank | Journal | Records |
|------|---------|---------|
| 1 | Nematology | 692 |
| 2 | Journal of Nematology | 618 |
| 3 | European Journal of Plant Pathology | 139 |
| 4 | Molecular Plant Pathology | 105 |
| 5 | Systematic Parasitology | 80 |
| 6 | Frontiers in Plant Science | 74 |
| 7 | PLOS ONE | 73 |
| 8 | Biological Control | 67 |
| 9 | Annals of Applied Biology | 58 |
| 10 | Australasian Plant Pathology | 56 |
| 11 | Plant Disease | 53 |
| 12 | Journal of Invertebrate Pathology | 53 |
| 13 | Annual Review of Phytopathology | 45 |
| 14 | CABI Compendium | 45 |
| 15 | Zoologica Scripta | 43 |

**Concentration:** Top 2 journals account for 33.4% of all records.

### Top 10 Publishers

| Rank | Publisher | Records |
|------|---------|---------|
| 1 | Brill Academic Publishers | 695 |
| 2 | Springer Nature | 513 |
| 3 | Wiley | 458 |
| 4 | Elsevier | 418 |
| 5 | De Gruyter | 171 |
| 6 | Taylor & Francis | 103 |
| 7 | Public Library of Science (PLoS) | 98 |
| 8 | Frontiers | 89 |
| 9 | Scientific Societies | 86 |
| 10 | MDPI | 68 |

---

## Publication Timeline

### Year Distribution (Recent)
| Year | Records | Notes |
|------|---------|-------|
| 2023 | 44 | Most recent |
| 2022 | 129 | |
| 2021 | 203 | |
| **2020** | **408** | **Peak year** |
| 2019 | 116 | |
| 2018 | 125 | |
| 2017 | 132 | |
| 2016 | 128 | |
| 2015 | 110 | |
| 2014 | 131 | |
| 2013 | 229 | High activity |
| 2012 | 167 | |
| 2011 | 217 | |
| 2010 | 181 | |

**Peak Year:** 2020 with 408 records (10.4% of dataset)
**Historical Range:** 1975-2023 (48 years)

---

## Citation Analysis

### Statistics
- **Mean:** 73.2 citations
- **Median:** 19 citations
- **Maximum:** 1,224 citations
- **25th percentile:** 6 citations
- **75th percentile:** 53 citations

### Highly Cited Publications

**Top cited (1,224 citations each):**
All are from the same 2013 paper "Top 10 plant‐parasitic nematodes" which mentions multiple genera:
- Aphelenchoides besseyi (2 records)
- Ditylenchus dipsaci
- Bursaphelenchus xylophilus (2 records)
- Pratylenchus spp.
- Radopholus similis
- Rotylenchulus reniformis
- Nacobbus aberrans

This explains the multiple 1,224 citation records - one review paper extracted for 10 different genera.

---

## Special Fields

### Factorials Field
Contains concatenated metadata in format:
`date = title = = journal = publisher = MeSH = institution = city = state = country = citations`

**Example:**
```
2019-01-01 = Integrative taxonomy of Xiphinema histriae and Xiphinema lapidosum from Spain = = Journal of Nematology = De Gruyter = NA = Institute for Sustainable Agriculture; Zhejiang University = Cordova; Hangzhou = ; Zhejiang = Spain; China = 2
```

### Text Field
Contains extended abstracts or full text extracts for detailed analysis and text mining.

---

## Key Insights

### 1. Extraction Methodology
- This is a **processed dataset** where genus/species mentions have been extracted from publications
- Same publication can appear multiple times (different genus/species)
- Enables analysis at the genus/species level rather than publication level

### 2. Quality Bias
- Higher average citations (73.2 vs 15.6) suggests **quality filtering**
- Likely focuses on more impactful or frequently cited papers
- Median citation (19) indicates robust central tendency

### 3. Taxonomic Coverage
- **Broader taxonomic scope** than Excel file
- Strong representation of entomopathogenic nematodes (11% of dataset)
- Includes beneficial nematodes for biological control

### 4. Geographic Patterns
- **European bias:** Belgium, Spain, UK highly represented
- May reflect specific sampling criteria or research networks
- Different from US/China dominance in Excel file

### 5. Journal Focus
- **Nematology specialists:** Nematology + Journal of Nematology = 1,310 records (33.4%)
- Broader scope in Excel file with more diverse journals

### 6. Temporal Distribution
- **Peak in 2020** (not 2022 like Excel file)
- Suggests different inclusion criteria or sampling methodology
- May be focused on specific research areas or grant cycles

---

## Comparison Summary: CSV vs Excel

| Feature | CSV (Sampled) | Excel (Complete) |
|---------|---------------|------------------|
| **Records** | 3,924 | 19,072 |
| **Structure** | Genus/species mentions | Unique publications |
| **Duplicates** | 79% are duplicates | No duplicates |
| **Avg Citations** | 73.2 | 15.6 |
| **Top Genus** | Meloidogyne (18%) | Meloidogyne (38%) |
| **Entomopathogenic** | 11% | <3% (estimated) |
| **Peak Year** | 2020 | 2022 |
| **Top Country** | USA (657) | USA (1,458) |
| **Top Journal** | Nematology (692) | Journal of Nematology |
| **Data Type** | Extracted mentions | Complete metadata |

---

## Use Cases

### This CSV File Is Better For:
1. **Taxonomic diversity studies** - Multiple mentions per publication
2. **Genus/species-level analysis** - Direct genus/species indexing
3. **Entomopathogenic research** - Better coverage of biocontrol agents
4. **Text mining** - Includes text and factorial fields
5. **High-impact research** - Pre-filtered for citation quality

### The Excel File Is Better For:
1. **Bibliometric analysis** - Complete publication records
2. **Funding analysis** - Detailed funder information
3. **Author network analysis** - Complete author and affiliation data
4. **Open access studies** - OA status included
5. **Comprehensive surveys** - No sampling bias

---

## Data Quality Notes

### Strengths
- Clean genus/species extraction
- Rich citation metadata
- Extended text fields for analysis
- Geographic precision (city/state/country)

### Limitations
- Duplicate publications (by design)
- Single anomalous text entry in Count field
- MeSH terms mostly absent (shown as NaN)
- Factorials field requires parsing
- Missing some metadata (RCR, FCR, Altmetric, funding details)

---

## Recommendations

### For Anguina Research
1. Use CSV for **species-level diversity** analysis (21 species vs broader Excel coverage)
2. Focus on **high-impact studies** (150, 85, 73 citation papers)
3. Investigate **toxicity research** connection (top papers are toxicity-related)
4. Explore **historical perspective** (1975-2023 coverage)

### For Comparative Analysis
1. **Cross-reference** CSV records with Excel file using title matching
2. **Validate extraction** by comparing genus/species mentions
3. **Integrate datasets** for comprehensive taxonomic + bibliometric analysis
4. **Use together** for maximum research value

### For Future Data Collection
1. Document extraction methodology clearly
2. Consider adding extraction confidence scores
3. Include publication DOI for easy cross-referencing
4. Standardize species naming (sp. vs sp vs spp.)
5. Parse factorials field into separate columns for easier analysis
