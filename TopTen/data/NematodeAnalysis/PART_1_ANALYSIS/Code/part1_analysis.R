# ============================================================================
# PART 1: SPECIES & TAXONOMIC ANALYSIS (R Implementation)
# ============================================================================
# Replicates Python analysis in R
# Author: Claude
# Date: November 19, 2025
# ============================================================================

# Load required libraries
library(tidyverse)
library(ggplot2)
library(viridis)
library(igraph)
library(reshape2)

# Set paths
data_path <- "/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv"
charts_path <- "/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Charts"
tables_path <- "/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_1_ANALYSIS/Tables"

# Define consistent color scheme (matching Python)
nematode_colors <- list(
  primary = "#2E86AB",
  secondary = "#A23B72",
  accent1 = "#F18F01",
  accent2 = "#C73E1D",
  accent3 = "#6A994E",
  neutral1 = "#5C6B73",
  neutral2 = "#9DB4C0",
  highlight = "#FFD23F"
)

genus_colors <- c(
  "Meloidogyne" = "#C73E1D",
  "Heterodera" = "#2E86AB",
  "Pratylenchus" = "#6A994E",
  "Bursaphelenchus" = "#F18F01",
  "Globodera" = "#A23B72",
  "Xiphinema" = "#5C6B73",
  "Ditylenchus" = "#FFD23F",
  "Radopholus" = "#06AED5",
  "Longidorus" = "#DD1C1A",
  "Aphelenchoides" = "#8B5A3C"
)

cat("================================================================================\n")
cat("PART 1: SPECIES & TAXONOMIC ANALYSIS (R)\n")
cat("================================================================================\n\n")

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================

cat("[1] Loading and preparing data...\n")

# Read CSV
df_raw <- read.csv(data_path, stringsAsFactors = FALSE)

# Filter out excluded genera and species
exclude_genera <- c("Steinernema", "Heterorhabditis")
exclude_species <- c("sp", "sp.", "spp", "spp.", "species")

df <- df_raw %>%
  filter(!tolower(Genus) %in% tolower(exclude_genera)) %>%
  filter(!tolower(Species) %in% tolower(exclude_species))

cat(sprintf("   Raw records: %d\n", nrow(df_raw)))
cat(sprintf("   After filtering: %d\n", nrow(df)))

# ============================================================================
# 2. SPECIES DISCOVERY RATE ANALYSIS
# ============================================================================

cat("\n[2] Analyzing species discovery rate...\n")

# Yearly species discovery
yearly_species <- df %>%
  group_by(pub_year) %>%
  summarise(
    New_Species = n_distinct(Species),
    Genera = n_distinct(Genus),
    .groups = 'drop'
  ) %>%
  arrange(pub_year) %>%
  mutate(
    Cumulative_Species = cumsum(New_Species),
    Cumulative_Genera = cumsum(Genera),
    Discovery_Rate_5yr = zoo::rollmean(New_Species, k = 5, fill = NA, align = "center")
  )

# Save table
write.csv(yearly_species,
          file.path(tables_path, "species_discovery_by_year_R.csv"),
          row.names = FALSE)
cat("   ✓ Saved: species_discovery_by_year_R.csv\n")

# ============================================================================
# 3. TAXONOMIC COMPLETENESS
# ============================================================================

cat("\n[3] Assessing taxonomic completeness...\n")

# Genus-level completeness
genera_data <- df %>%
  group_by(Genus) %>%
  summarise(
    N_Species = n_distinct(Species),
    N_Publications = n(),
    Total_Mentions = n(),
    Mean_Citations = mean(citations, na.rm = TRUE),
    Total_Citations = sum(citations, na.rm = TRUE),
    .groups = 'drop'
  ) %>%
  mutate(Pubs_per_Species = N_Publications / N_Species) %>%
  arrange(desc(N_Publications))

write.csv(genera_data,
          file.path(tables_path, "genus_taxonomic_completeness_R.csv"),
          row.names = FALSE)
cat("   ✓ Saved: genus_taxonomic_completeness_R.csv\n")

# ============================================================================
# 4. GEOGRAPHIC DISTRIBUTION
# ============================================================================

cat("\n[4] Analyzing geographic distribution...\n")

# Country summary
country_summary <- df %>%
  filter(!is.na(country) & country != "") %>%
  group_by(country) %>%
  summarise(
    N_Genera = n_distinct(Genus),
    N_Species = n_distinct(Species),
    N_Publications = n(),
    Total_Citations = sum(citations, na.rm = TRUE),
    Mean_Citations = mean(citations, na.rm = TRUE),
    .groups = 'drop'
  ) %>%
  arrange(desc(N_Publications))

write.csv(country_summary,
          file.path(tables_path, "country_research_summary_R.csv"),
          row.names = FALSE)
cat("   ✓ Saved: country_research_summary_R.csv\n")

# ============================================================================
# 5. RESEARCH BIAS ANALYSIS
# ============================================================================

cat("\n[5] Analyzing research bias...\n")

# Genus bias
genus_bias <- df %>%
  group_by(Genus) %>%
  summarise(
    n_publications = n(),
    mean_citations = mean(citations, na.rm = TRUE),
    total_citations = sum(citations, na.rm = TRUE),
    .groups = 'drop'
  ) %>%
  mutate(
    expected_pubs = mean(n_publications),
    bias_ratio = n_publications / expected_pubs,
    bias_category = case_when(
      bias_ratio < 0.25 ~ "Severely Understudied",
      bias_ratio < 0.75 ~ "Understudied",
      bias_ratio < 1.5 ~ "Adequately Studied",
      TRUE ~ "Overstudied"
    )
  ) %>%
  arrange(desc(n_publications))

write.csv(genus_bias,
          file.path(tables_path, "genus_research_bias_R.csv"),
          row.names = FALSE)
cat("   ✓ Saved: genus_research_bias_R.csv\n")

# Species bias
species_bias <- df %>%
  group_by(Species) %>%
  summarise(
    n_publications = n(),
    mean_citations = mean(citations, na.rm = TRUE),
    total_citations = sum(citations, na.rm = TRUE),
    .groups = 'drop'
  ) %>%
  mutate(
    expected_pubs = mean(n_publications),
    bias_ratio = n_publications / expected_pubs
  ) %>%
  arrange(desc(n_publications))

write.csv(species_bias,
          file.path(tables_path, "species_research_bias_R.csv"),
          row.names = FALSE)
cat("   ✓ Saved: species_research_bias_R.csv\n")

# ============================================================================
# 6. GENERATE PUBLICATION-QUALITY FIGURES
# ============================================================================

cat("\n[6] Generating publication-quality figures...\n")

# Set theme for all plots
theme_publication <- theme_bw() +
  theme(
    text = element_text(size = 10, family = "sans"),
    axis.text = element_text(size = 9),
    axis.title = element_text(size = 11),
    plot.title = element_text(size = 12, face = "bold"),
    legend.text = element_text(size = 9),
    legend.title = element_text(size = 10),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(linetype = "dashed", alpha = 0.3)
  )

# Figure R1: Species Discovery Rate
p1 <- ggplot(yearly_species, aes(x = pub_year, y = New_Species)) +
  geom_bar(stat = "identity", fill = nematode_colors$primary, alpha = 0.7) +
  geom_line(aes(y = Discovery_Rate_5yr), color = nematode_colors$accent2, size = 1.2) +
  labs(
    title = "Annual Species Discovery Rate",
    x = "Year",
    y = "Number of Species Mentioned"
  ) +
  theme_publication

ggsave(
  filename = file.path(charts_path, "FigR1_Species_Discovery_R.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 600
)
cat("   ✓ Saved: FigR1_Species_Discovery_R.png\n")

# Figure R2: Top Genera by Publications
top_genera <- genera_data %>% head(15)
top_genera$Genus <- factor(top_genera$Genus, levels = rev(top_genera$Genus))

p2 <- ggplot(top_genera, aes(x = Genus, y = N_Publications)) +
  geom_bar(stat = "identity", fill = nematode_colors$primary, alpha = 0.7) +
  coord_flip() +
  labs(
    title = "Top 15 Genera by Research Output",
    x = "Genus",
    y = "Number of Publications"
  ) +
  theme_publication

ggsave(
  filename = file.path(charts_path, "FigR2_Top_Genera_R.png"),
  plot = p2,
  width = 10,
  height = 6,
  dpi = 600
)
cat("   ✓ Saved: FigR2_Top_Genera_R.png\n")

# Figure R3: Geographic Distribution
top_countries <- country_summary %>% head(20)
top_countries$country <- factor(top_countries$country, levels = rev(top_countries$country))

p3 <- ggplot(top_countries, aes(x = country, y = N_Publications)) +
  geom_bar(stat = "identity", fill = nematode_colors$accent1, alpha = 0.7) +
  coord_flip() +
  labs(
    title = "Research Output by Country (Top 20)",
    x = "Country",
    y = "Number of Publications"
  ) +
  theme_publication

ggsave(
  filename = file.path(charts_path, "FigR3_Geographic_Distribution_R.png"),
  plot = p3,
  width = 10,
  height = 8,
  dpi = 600
)
cat("   ✓ Saved: FigR3_Geographic_Distribution_R.png\n")

# Figure R4: Research Bias Distribution
bias_summary <- genus_bias %>%
  count(bias_category) %>%
  mutate(
    percentage = n / sum(n) * 100,
    label = sprintf("%s\n%.1f%%", bias_category, percentage)
  )

p4 <- ggplot(bias_summary, aes(x = "", y = n, fill = bias_category)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  scale_fill_manual(values = c(
    "Overstudied" = nematode_colors$accent2,
    "Adequately Studied" = nematode_colors$accent3,
    "Understudied" = nematode_colors$accent1,
    "Severely Understudied" = nematode_colors$neutral1
  )) +
  labs(title = "Distribution of Research Bias (Genera)") +
  theme_void() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 12),
    legend.title = element_blank()
  )

ggsave(
  filename = file.path(charts_path, "FigR4_Research_Bias_R.png"),
  plot = p4,
  width = 8,
  height = 6,
  dpi = 600
)
cat("   ✓ Saved: FigR4_Research_Bias_R.png\n")

cat("\n================================================================================\n")
cat("PART 1 ANALYSIS COMPLETE (R)!\n")
cat("================================================================================\n")
cat(sprintf("\n✓ Charts saved to: %s/\n", charts_path))
cat(sprintf("✓ Tables saved to: %s/\n", tables_path))
cat("\nGenerated R Figures:\n")
cat("  - FigR1_Species_Discovery_R.png\n")
cat("  - FigR2_Top_Genera_R.png\n")
cat("  - FigR3_Geographic_Distribution_R.png\n")
cat("  - FigR4_Research_Bias_R.png\n")
