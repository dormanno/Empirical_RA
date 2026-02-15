# =============================================================================
# OPTIONAL: Export Results to Files
# =============================================================================
# This script extends the main portfolio analysis to export results
# Add these lines at the end of portfolio_analysis.R if you want to save outputs
# =============================================================================

# Note: This is NOT included in the main script as per requirements
# (calculations only, no exports)
# Use this if you need to save results for reporting

# =============================================================================
# CREATE OUTPUT DIRECTORY
# =============================================================================
output_dir <- "./R_output"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

cat("\nOptional: Exporting results to files...\n")

# =============================================================================
# EXPORT 1: PRICE DATA
# =============================================================================
write.csv(prices_df, 
          file = file.path(output_dir, "01_portfolio_prices.csv"),
          row.names = TRUE)
cat("[EXPORT] 01_portfolio_prices.csv\n")

# =============================================================================
# EXPORT 2: RETURNS DATA
# =============================================================================
write.csv(returns_df,
          file = file.path(output_dir, "02_portfolio_returns.csv"),
          row.names = TRUE)
cat("[EXPORT] 02_portfolio_returns.csv\n")

# =============================================================================
# EXPORT 3: SUMMARY STATISTICS
# =============================================================================
summary_stats <- data.frame(
  Metric = c("Mean Daily", "Mean Monthly", "Mean Yearly",
             "Std Dev Daily", "Std Dev Monthly", "Std Dev Yearly",
             "Sharpe Ratio", "Beta", "Alpha"),
  Value = c(portfolio_mean_daily, portfolio_mean_monthly, portfolio_mean_yearly,
            portfolio_std_daily, portfolio_std_monthly, portfolio_std_yearly,
            performance_results$sharpe_ratio, 
            performance_results$beta, 
            performance_results$alpha)
)

write.csv(summary_stats,
          file = file.path(output_dir, "03_summary_statistics.csv"),
          row.names = FALSE)
cat("[EXPORT] 03_summary_statistics.csv\n")

# =============================================================================
# EXPORT 4: CORRELATION MATRIX
# =============================================================================
write.csv(correlation_matrix,
          file = file.path(output_dir, "04_correlation_matrix.csv"),
          row.names = TRUE)
cat("[EXPORT] 04_correlation_matrix.csv\n")

# =============================================================================
# EXPORT 5: COVARIANCE MATRIX
# =============================================================================
write.csv(covariance_matrix,
          file = file.path(output_dir, "05_covariance_matrix.csv"),
          row.names = TRUE)
cat("[EXPORT] 05_covariance_matrix.csv\n")

# =============================================================================
# EXPORT 6: VAR RESULTS
# =============================================================================
var_summary <- data.frame(
  Method = c("Historical", "Parametric", "Monte Carlo"),
  VaR_95 = c(var_results$historical, 
             var_results$parametric, 
             var_results$monte_carlo)
)

write.csv(var_summary,
          file = file.path(output_dir, "06_var_results.csv"),
          row.names = FALSE)
cat("[EXPORT] 06_var_results.csv\n")

# =============================================================================
# EXPORT 7: CVAR RESULTS
# =============================================================================
cvar_summary <- data.frame(
  Method = c("Historical", "Parametric", "Monte Carlo"),
  CVaR_95 = c(cvar_results$historical,
              cvar_results$parametric,
              cvar_results$monte_carlo)
)

write.csv(cvar_summary,
          file = file.path(output_dir, "07_cvar_results.csv"),
          row.names = FALSE)
cat("[EXPORT] 07_cvar_results.csv\n")

# =============================================================================
# EXPORT 8: ASSET-LEVEL STATISTICS
# =============================================================================
asset_stats <- data.frame(
  Asset = asset_names,
  Mean_Daily = mean_daily,
  Std_Dev_Daily = std_dev_daily,
  Mean_Yearly = mean_yearly,
  Std_Dev_Yearly = std_dev_yearly,
  Weight = WEIGHTS
)

write.csv(asset_stats,
          file = file.path(output_dir, "08_asset_statistics.csv"),
          row.names = FALSE)
cat("[EXPORT] 08_asset_statistics.csv\n")

# =============================================================================
# EXPORT 9: VISUALIZATIONS (PNG)
# =============================================================================
# Note: These require re-generating plots with ggsave()

# 9.1 Price Timeseries
df <- fortify.zoo(prices_rebased)
df_melted <- melt(df, id.vars = "Index")
p1 <- ggplot(df_melted, aes(x = Index, y = value, color = variable)) +
  geom_line(linewidth = 1) +
  labs(title = "Asset Prices Rebased to 100", x = "Date", y = "Rebased Price") +
  theme_minimal()
ggsave(filename = file.path(output_dir, "09_price_timeseries.png"),
       plot = p1, width = 10, height = 6, dpi = 300)
cat("[EXPORT] 09_price_timeseries.png\n")

# 9.2 Return Distributions
df <- fortify.zoo(returns_df)
df_melted <- melt(df, id.vars = "Index")
p2 <- ggplot(df_melted, aes(x = value, fill = variable)) +
  geom_histogram(bins = 50, alpha = 0.7, position = "identity") +
  facet_wrap(~variable, scales = "free") +
  labs(title = "Return Distributions", x = "Daily Returns", y = "Frequency") +
  theme_minimal()
ggsave(filename = file.path(output_dir, "10_return_distributions.png"),
       plot = p2, width = 10, height = 6, dpi = 300)
cat("[EXPORT] 10_return_distributions.png\n")

# 9.3 Correlation Heatmap
png(filename = file.path(output_dir, "11_correlation_heatmap.png"),
    width = 800, height = 800, res = 150)
corrplot(correlation_matrix, method = "color", type = "upper",
         addCoef.col = "black", number.cex = 0.7,
         tl.col = "black", tl.srt = 45,
         title = "Correlation Matrix", mar = c(0, 0, 2, 0))
dev.off()
cat("[EXPORT] 11_correlation_heatmap.png\n")

# 9.4 Rolling Volatility
rolling_sd <- rollapply(returns_df, width = 20, FUN = sd, 
                        by.column = TRUE, fill = NA, align = "right")
rolling_sd_annualized <- rolling_sd * sqrt(252)
df <- fortify.zoo(rolling_sd_annualized)
df_melted <- melt(df, id.vars = "Index")
p4 <- ggplot(df_melted, aes(x = Index, y = value, color = variable)) +
  geom_line(linewidth = 0.8) +
  labs(title = "Rolling 20-Day Volatility (Annualized)", 
       x = "Date", y = "Volatility") +
  theme_minimal()
ggsave(filename = file.path(output_dir, "12_rolling_volatility.png"),
       plot = p4, width = 10, height = 6, dpi = 300)
cat("[EXPORT] 12_rolling_volatility.png\n")

# 9.5 VaR Timeseries (Historical)
df <- data.frame(Date = index(portfolio_returns), 
                 Returns = as.numeric(portfolio_returns))
df$VaR <- -var_results$historical
df$Breach <- df$Returns < df$VaR
p5 <- ggplot(df, aes(x = Date)) +
  geom_line(aes(y = Returns), color = "blue", alpha = 0.6) +
  geom_hline(yintercept = -var_results$historical, 
             color = "red", linetype = "dashed") +
  geom_point(data = df[df$Breach, ], 
             aes(x = Date, y = Returns), color = "red", size = 2) +
  labs(title = "VaR Breach Analysis (Historical)", 
       x = "Date", y = "Returns") +
  theme_minimal()
ggsave(filename = file.path(output_dir, "13_var_historical.png"),
       plot = p5, width = 10, height = 6, dpi = 300)
cat("[EXPORT] 13_var_historical.png\n")

# 9.6 CVaR Timeseries
df$CVaR <- -cvar_results$historical
df$CVaR_Breach <- df$Returns < df$CVaR
p6 <- ggplot(df, aes(x = Date)) +
  geom_line(aes(y = Returns), color = "blue", alpha = 0.6) +
  geom_hline(yintercept = -cvar_results$historical,
             color = "darkred", linetype = "dashed") +
  geom_point(data = df[df$CVaR_Breach, ], 
             aes(x = Date, y = Returns), color = "darkred", size = 2) +
  labs(title = "CVaR Breach Analysis", x = "Date", y = "Returns") +
  theme_minimal()
ggsave(filename = file.path(output_dir, "14_cvar_analysis.png"),
       plot = p6, width = 10, height = 6, dpi = 300)
cat("[EXPORT] 14_cvar_analysis.png\n")

# 9.7 Beta Scatter Plot
if (!is.null(benchmark_returns)) {
  merged <- merge(portfolio_returns, benchmark_returns, join = "inner")
  df_beta <- data.frame(
    Portfolio = as.numeric(merged[, 1]),
    Benchmark = as.numeric(merged[, 2])
  )
  
  p7 <- ggplot(df_beta, aes(x = Benchmark, y = Portfolio)) +
    geom_point(alpha = 0.5, color = "blue") +
    geom_smooth(method = "lm", color = "red", se = TRUE) +
    labs(title = "Portfolio Beta vs MSCI World",
         x = "Benchmark Returns", y = "Portfolio Returns") +
    theme_minimal()
  ggsave(filename = file.path(output_dir, "15_beta_scatter.png"),
         plot = p7, width = 10, height = 6, dpi = 300)
  cat("[EXPORT] 15_beta_scatter.png\n")
}

# =============================================================================
# EXPORT 10: COMPREHENSIVE TEXT REPORT
# =============================================================================
report_file <- file.path(output_dir, "16_comprehensive_report.txt")
sink(report_file)

cat(rep("=", 80), "\n", sep = "")
cat("PORTFOLIO RISK ANALYSIS - COMPREHENSIVE REPORT\n")
cat(rep("=", 80), "\n\n", sep = "")

cat("PORTFOLIO SPECIFICATION\n")
cat(rep("-", 80), "\n", sep = "")
cat(sprintf("Initial Value: %s PLN\n", format(INITIAL_VALUE, big.mark = ",")))
cat(sprintf("Time Period: %s to %s\n", 
            format(start(prices_df), "%Y-%m-%d"), 
            format(end(prices_df), "%Y-%m-%d")))
cat(sprintf("Number of Observations: %d\n", nrow(returns_df)))
cat("\nAsset Allocation:\n")
for (i in 1:length(asset_names)) {
  cat(sprintf("  - %s: %.1f%%\n", asset_names[i], WEIGHTS[i] * 100))
}

cat("\n\nRETURN ANALYSIS\n")
cat(rep("-", 80), "\n", sep = "")
cat(sprintf("Portfolio Mean Daily Return: %.6f\n", portfolio_mean_daily))
cat(sprintf("Portfolio Mean Monthly Return: %.6f\n", portfolio_mean_monthly))
cat(sprintf("Portfolio Mean Yearly Return: %.4f\n", portfolio_mean_yearly))
cat("\nAsset-Level Mean Daily Returns:\n")
print(mean_daily)

cat("\n\nVOLATILITY ANALYSIS\n")
cat(rep("-", 80), "\n", sep = "")
cat(sprintf("Portfolio Daily Volatility: %.6f\n", portfolio_std_daily))
cat(sprintf("Portfolio Monthly Volatility: %.6f\n", portfolio_std_monthly))
cat(sprintf("Portfolio Yearly Volatility: %.4f\n", portfolio_std_yearly))
cat("\nAsset-Level Daily Volatility:\n")
print(std_dev_daily)

cat("\n\nCORRELATION ANALYSIS\n")
cat(rep("-", 80), "\n", sep = "")
cat("Correlation Matrix:\n")
print(round(correlation_matrix, 4))
cat("\nCovariance Matrix:\n")
print(covariance_matrix)

cat("\n\nVALUE AT RISK (95% Confidence)\n")
cat(rep("-", 80), "\n", sep = "")
cat(sprintf("Historical VaR: %.4f\n", var_results$historical))
cat(sprintf("Parametric VaR: %.4f\n", var_results$parametric))
cat(sprintf("Monte Carlo VaR: %.4f\n", var_results$monte_carlo))

cat("\n\nCONDITIONAL VALUE AT RISK (95% Confidence)\n")
cat(rep("-", 80), "\n", sep = "")
cat(sprintf("Historical CVaR: %.4f\n", cvar_results$historical))
cat(sprintf("Parametric CVaR: %.4f\n", cvar_results$parametric))
cat(sprintf("Monte Carlo CVaR: %.4f\n", cvar_results$monte_carlo))

cat("\n\nPERFORMANCE METRICS\n")
cat(rep("-", 80), "\n", sep = "")
cat(sprintf("Sharpe Ratio: %.4f\n", performance_results$sharpe_ratio))
cat(sprintf("Beta (vs MSCI World): %.4f\n", performance_results$beta))
cat(sprintf("Alpha: %.6f\n", performance_results$alpha))

cat("\n\n")
cat(rep("=", 80), "\n", sep = "")
cat("END OF REPORT\n")
cat(rep("=", 80), "\n", sep = "")

sink()
cat("[EXPORT] 16_comprehensive_report.txt\n")

# =============================================================================
# SUMMARY
# =============================================================================
cat("\n")
cat(rep("=", 80), "\n", sep = "")
cat("EXPORT COMPLETE\n")
cat(rep("=", 80), "\n", sep = "")
cat(sprintf("\nAll results exported to: %s\n", normalizePath(output_dir)))
cat("\nFiles created:\n")
cat("  - 8 CSV files (data & statistics)\n")
cat("  - 7 PNG files (visualizations)\n")
cat("  - 1 TXT file (comprehensive report)\n")
cat("\nTotal: 16 files\n")
cat(rep("=", 80), "\n", sep = "")
