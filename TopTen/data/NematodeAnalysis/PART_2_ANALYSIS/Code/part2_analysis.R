# ============================================================================
# PART 2: TEMPORAL & TREND ANALYSIS (R Implementation)
# ============================================================================
# Simplified R implementation of temporal trend analysis and basic forecasting
# Author: Claude
# Date: November 19, 2025
# ============================================================================

library(tidyverse)
library(ggplot2)
library(forecast)
library(zoo)

# Paths
data_path <- "/home/user/DataAnalyz/TopTen/data/ALL_NEMATODES_EXTRACTED_Sampled.csv"
charts_path <- "/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Charts"
tables_path <- "/home/user/DataAnalyz/TopTen/data/NematodeAnalysis/PART_2_ANALYSIS/Tables"

# Color scheme (matching Python)
nematode_colors <- list(
  primary = "#2E86AB",
  secondary = "#A23B72",
  accent1 = "#F18F01",
  accent2 = "#C73E1D",
  accent3 = "#6A994E"
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
  "Longidorus" = "#DD1A",
  "Aphelenchoides" = "#8B5A3C"
)

cat("================================================================================\n")
cat("PART 2: TEMPORAL & TREND ANALYSIS (R)\n")
cat("================================================================================\n\n")

# Load data
cat("[1] Loading and preparing data...\n")
df_raw <- read.csv(data_path, stringsAsFactors = FALSE)

# Filter
exclude_genera <- c("Steinernema", "Heterorhabditis")
exclude_species <- c("sp", "sp.", "spp", "spp.", "species")

df <- df_raw %>%
  filter(!tolower(Genus) %in% tolower(exclude_genera)) %>%
  filter(!tolower(Species) %in% tolower(exclude_species))

cat(sprintf("   Filtered dataset: %d records\n", nrow(df)))

# Get top 10 genera
top10_genera <- df %>%
  group_by(Genus) %>%
  summarise(total = n()) %>%
  arrange(desc(total)) %>%
  head(10) %>%
  pull(Genus)

# ============================================================================
# TEMPORAL TRENDS
# ============================================================================

cat("\n[2] Analyzing temporal trends...\n")

# Genus trends by year
genus_trends <- df %>%
  group_by(pub_year, Genus) %>%
  summarise(n_records = n(), .groups = 'drop')

write.csv(genus_trends,
          file.path(tables_path, "genus_trends_by_year_R.csv"),
          row.names = FALSE)

# Overall trend
overall_trend <- df %>%
  group_by(pub_year) %>%
  summarise(count = n()) %>%
  arrange(pub_year)

# FigureR1: Overall Temporal Trend
p1 <- ggplot(overall_trend, aes(x = pub_year, y = count)) +
  geom_bar(stat = "identity", fill = nematode_colors$primary, alpha = 0.7) +
  geom_smooth(method = "loess", color = nematode_colors$accent2, se = FALSE, size = 1.5) +
  labs(
    title = "Overall Research Output Trend",
    x = "Year",
    y = "Number of Records"
  ) +
  theme_bw() +
  theme(
    text = element_text(size = 11),
    plot.title = element_text(face = "bold")
  )

ggsave(
  filename = file.path(charts_path, "FigR1_Overall_Temporal_Trend_R.png"),
  plot = p1,
  width = 10,
  height = 6,
  dpi = 600
)
cat("   ✓ Saved: FigR1_Overall_Temporal_Trend_R.png\n")

# FigureR2: Top Genera Trends
genus_trends_top10 <- genus_trends %>%
  filter(Genus %in% top10_genera)

p2 <- ggplot(genus_trends_top10, aes(x = pub_year, y = n_records, color = Genus)) +
  geom_line(size = 1.2) +
  labs(
    title = "Research Trends - Top 10 Genera",
    x = "Year",
    y = "Number of Records"
  ) +
  theme_bw() +
  theme(
    text = element_text(size = 11),
    plot.title = element_text(face = "bold"),
    legend.position = "right"
  )

ggsave(
  filename = file.path(charts_path, "FigR2_Genus_Trends_R.png"),
  plot = p2,
  width = 12,
  height = 6,
  dpi = 600
)
cat("   ✓ Saved: FigR2_Genus_Trends_R.png\n")

# ============================================================================
# BASIC FORECASTING
# ============================================================================

cat("\n[3] Performing basic forecasting...\n")

# Forecast for top 3 genera (simplified)
forecast_results <- list()

for (genus in top10_genera[1:3]) {
  genus_data <- df %>%
    filter(Genus == genus) %>%
    group_by(pub_year) %>%
    summarise(count = n(), .groups = 'drop') %>%
    arrange(pub_year)

  if (nrow(genus_data) >= 10) {
    # Create time series
    ts_data <- ts(genus_data$count, start = min(genus_data$pub_year))

    # Fit ARIMA model
    fit <- auto.arima(ts_data, seasonal = FALSE)

    # Forecast 20 years
    forecast_obj <- forecast(fit, h = 20)

    forecast_results[[genus]] <- list(
      years = (max(genus_data$pub_year) + 1):(max(genus_data$pub_year) + 20),
      forecast = as.numeric(forecast_obj$mean),
      lower = as.numeric(forecast_obj$lower[,2]),
      upper = as.numeric(forecast_obj$upper[,2])
    )
  }
}

cat(sprintf("   ✓ Generated forecasts for %d genera\n", length(forecast_results)))

# FigureR3: Forecasts for top genera
for (idx in 1:min(3, length(forecast_results))) {
  genus <- names(forecast_results)[idx]
  result <- forecast_results[[genus]]

  # Historical data
  hist_data <- df %>%
    filter(Genus == genus) %>%
    group_by(pub_year) %>%
    summarise(count = n())

  # Combine historical and forecast
  plot_data <- data.frame(
    year = c(hist_data$pub_year, result$years),
    count = c(hist_data$count, result$forecast),
    type = c(rep("Historical", nrow(hist_data)), rep("Forecast", length(result$years)))
  )

  p <- ggplot(plot_data, aes(x = year, y = count, color = type)) +
    geom_line(size = 1.2) +
    geom_point(size = 2) +
    labs(
      title = paste(genus, "- 20-Year Forecast"),
      x = "Year",
      y = "Count"
    ) +
    scale_color_manual(values = c("Historical" = nematode_colors$primary,
                                  "Forecast" = nematode_colors$accent2)) +
    theme_bw() +
    theme(
      text = element_text(size = 11),
      plot.title = element_text(face = "bold")
    )

  ggsave(
    filename = file.path(charts_path, sprintf("FigR3_%s_Forecast_R.png", genus)),
    plot = p,
    width = 10,
    height = 6,
    dpi = 600
  )
}

cat("   ✓ Saved forecast visualizations\n")

cat("\n================================================================================\n")
cat("PART 2 ANALYSIS COMPLETE (R)!\n")
cat("================================================================================\n")
cat(sprintf("✓ Charts saved to: %s/\n", charts_path))
cat(sprintf("✓ Tables saved to: %s/\n", tables_path))
