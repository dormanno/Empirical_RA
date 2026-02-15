# =============================================================================
# Portfolio Risk Analysis - Complete Workflow (R Implementation)
# =============================================================================
# This script replicates the Python integration test in R
# Portfolio: 50% Pfizer (PFE), 25% JPY/PLN, 25% Gold (GC=F)
# Initial Value: 100,000 PLN
# Time Period: 10 years, daily data
# Risk-Free Rate: 2% annual (Polish Treasury Bills)
# =============================================================================

# Load required libraries
suppressPackageStartupMessages({
  library(quantmod)
  library(PerformanceAnalytics)
  library(xts)
  library(zoo)
  library(TTR)
  library(ggplot2)
  library(corrplot)
  library(reshape2)
  library(gridExtra)
  library(MASS)
})

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

# Function to fetch and prepare asset data with currency conversion
fetch_asset_data <- function(ticker, name, fx_ticker = NULL, start_date, end_date, max_abs_return = NULL) {
  cat(sprintf("  Loading data for %s (%s)...\n", name, ticker))
  
  tryCatch({
    # Fetch main asset data
    getSymbols(ticker, src = "yahoo", from = start_date, to = end_date, auto.assign = FALSE, warnings = FALSE) -> asset_data
    
    if (is.null(asset_data) || nrow(asset_data) == 0) {
      stop("No data retrieved")
    }
    
    # Extract adjusted close price
    prices <- Ad(asset_data)
    colnames(prices) <- name
    
    # If currency conversion is needed
    if (!is.null(fx_ticker)) {
      cat(sprintf("    Fetching FX data: %s...\n", fx_ticker))
      fx_data <- getSymbols(fx_ticker, src = "yahoo", from = start_date, to = end_date, auto.assign = FALSE, warnings = FALSE)
      fx_prices <- Ad(fx_data)
      
      # Merge and convert
      merged <- merge(prices, fx_prices, join = "inner")
      prices <- merged[, 1] * merged[, 2]
      colnames(prices) <- name
    }
    
    # Flag outlier price moves based on return threshold
    if (!is.null(max_abs_return)) {
      returns <- ROC(prices, type = "discrete")
      outlier_idx <- which(abs(returns) > max_abs_return)
      if (length(outlier_idx) > 0) {
        prices[outlier_idx] <- NA
      }
    }

    # Forward-fill gaps (match Python ffill behavior), then drop leading NAs
    prices <- na.locf(prices, na.rm = FALSE)
    prices <- na.omit(prices)
    
    cat(sprintf("    [OK] %s: %d data points\n", name, nrow(prices)))
    return(prices)
    
  }, error = function(e) {
    cat(sprintf("    [FAIL] %s: %s\n", name, e$message))
    return(NULL)
  })
}

# Function to calculate Value at Risk using multiple methods
calculate_var <- function(returns, confidence_level = 0.95, num_simulations = 10000) {
  # Historical VaR
  hist_var <- VaR(returns, p = confidence_level, method = "historical")
  
  # Parametric VaR (Gaussian)
  param_var <- VaR(returns, p = confidence_level, method = "gaussian")
  
  # Monte Carlo VaR
  mu <- mean(returns, na.rm = TRUE)
  sigma <- sd(returns, na.rm = TRUE)
  simulated_returns <- rnorm(num_simulations, mean = mu, sd = sigma)
  mc_var <- quantile(simulated_returns, probs = (1 - confidence_level))
  
  return(list(
    historical = abs(as.numeric(hist_var)),
    parametric = abs(as.numeric(param_var)),
    monte_carlo = abs(as.numeric(mc_var))
  ))
}

# Function to calculate Conditional VaR (Expected Shortfall)
calculate_cvar <- function(returns, confidence_level = 0.95, num_simulations = 10000) {
  # Historical CVaR
  hist_cvar <- ES(returns, p = confidence_level, method = "historical")
  
  # Parametric CVaR
  param_cvar <- ES(returns, p = confidence_level, method = "gaussian")
  
  # Monte Carlo CVaR
  mu <- mean(returns, na.rm = TRUE)
  sigma <- sd(returns, na.rm = TRUE)
  simulated_returns <- rnorm(num_simulations, mean = mu, sd = sigma)
  var_threshold <- quantile(simulated_returns, probs = (1 - confidence_level))
  mc_cvar <- mean(simulated_returns[simulated_returns <= var_threshold])
  
  return(list(
    historical = abs(as.numeric(hist_cvar)),
    parametric = abs(as.numeric(param_cvar)),
    monte_carlo = abs(as.numeric(mc_cvar))
  ))
}

# Function to calculate performance metrics
calculate_performance <- function(portfolio_returns, benchmark_returns, risk_free_rate) {
  # Sharpe Ratio
  sharpe <- SharpeRatio(portfolio_returns, Rf = risk_free_rate, FUN = "StdDev")
  
  # Beta (using CAPM)
  if (!is.null(benchmark_returns) && length(benchmark_returns) > 0) {
    # Align dates
    merged <- merge(portfolio_returns, benchmark_returns, join = "inner")
    if (nrow(merged) > 10) {
      port_ret <- merged[, 1]
      bench_ret <- merged[, 2]
      
      # Calculate beta using regression
      model <- lm(port_ret ~ bench_ret)
      beta <- coef(model)[2]
      
      # Calculate alpha
      alpha <- coef(model)[1]
    } else {
      beta <- 1.0
      alpha <- 0.0
    }
  } else {
    beta <- 1.0
    alpha <- 0.0
  }
  
  return(list(
    sharpe_ratio = as.numeric(sharpe),
    beta = as.numeric(beta),
    alpha = as.numeric(alpha)
  ))
}

# Visualization function: Price timeseries rebased to 100
plot_price_timeseries <- function(prices_rebased) {
  df <- fortify.zoo(prices_rebased)
  df_melted <- melt(df, id.vars = "Index")
  df_melted <- df_melted[!is.na(df_melted$value), ]
  
  p <- ggplot(df_melted, aes(x = Index, y = value, color = variable, linetype = variable)) +
    geom_line(linewidth = 1, alpha = 0.9) +
    scale_color_brewer(palette = "Dark2") +
    labs(title = "Asset Prices Rebased to 100",
         x = "Date",
         y = "Rebased Price",
         color = "Asset",
         linetype = "Asset") +
    theme_minimal() +
    theme(legend.position = "bottom")
  
  print(p)
}

# Visualization function: Return distributions
plot_return_distributions <- function(returns_df) {
  df <- fortify.zoo(returns_df)
  df_melted <- melt(df, id.vars = "Index")
  
  p <- ggplot(df_melted, aes(x = value, fill = variable)) +
    geom_histogram(bins = 50, alpha = 0.7, position = "identity") +
    facet_wrap(~variable, scales = "free") +
    labs(title = "Return Distributions by Asset",
         x = "Daily Returns",
         y = "Frequency") +
    theme_minimal() +
    theme(legend.position = "none")
  
  print(p)
}

# Visualization function: Correlation heatmap
plot_correlation_heatmap <- function(corr_matrix) {
  corrplot(corr_matrix, method = "color", type = "upper",
           addCoef.col = "black", number.cex = 0.7,
           tl.col = "black", tl.srt = 45,
           title = "Asset Correlation Matrix",
           mar = c(0, 0, 2, 0))
}

# Visualization function: Rolling volatility
plot_rolling_volatility <- function(returns_df, window = 20) {
  rolling_sd <- rollapply(returns_df, width = window, FUN = sd, by.column = TRUE, fill = NA, align = "right")
  rolling_sd_annualized <- rolling_sd * sqrt(252)
  
  df <- fortify.zoo(rolling_sd_annualized)
  df_melted <- melt(df, id.vars = "Index")
  
  p <- ggplot(df_melted, aes(x = Index, y = value, color = variable)) +
    geom_line(linewidth = 0.8) +
    labs(title = sprintf("Rolling %d-Day Volatility (Annualized)", window),
         x = "Date",
         y = "Annualized Volatility",
         color = "Asset") +
    theme_minimal() +
    theme(legend.position = "bottom")
  
  print(p)
}

# Visualization function: VaR timeseries
plot_var_timeseries <- function(portfolio_returns, var_value, method_name) {
  df <- data.frame(Date = index(portfolio_returns), Returns = as.numeric(portfolio_returns))
  df$VaR <- -var_value
  df$Breach <- df$Returns < df$VaR
  
  p <- ggplot(df, aes(x = Date)) +
    geom_line(aes(y = Returns), color = "blue", alpha = 0.6) +
    geom_hline(yintercept = -var_value, color = "red", linetype = "dashed", linewidth = 1) +
    geom_point(data = df[df$Breach, ], aes(x = Date, y = Returns), color = "red", size = 2) +
    labs(title = sprintf("Portfolio Returns vs VaR (%s Method)", method_name),
         x = "Date",
         y = "Daily Returns",
         subtitle = sprintf("VaR (95%%): %.4f | Breaches: %d", var_value, sum(df$Breach))) +
    theme_minimal()
  
  print(p)
}

# Visualization function: CVaR timeseries
plot_cvar_timeseries <- function(portfolio_returns, cvar_value) {
  df <- data.frame(Date = index(portfolio_returns), Returns = as.numeric(portfolio_returns))
  df$CVaR <- -cvar_value
  df$Breach <- df$Returns < df$CVaR
  
  p <- ggplot(df, aes(x = Date)) +
    geom_line(aes(y = Returns), color = "blue", alpha = 0.6) +
    geom_hline(yintercept = -cvar_value, color = "darkred", linetype = "dashed", linewidth = 1) +
    geom_point(data = df[df$Breach, ], aes(x = Date, y = Returns), color = "darkred", size = 2) +
    labs(title = "Portfolio Returns vs Expected Shortfall (CVaR)",
         x = "Date",
         y = "Daily Returns",
         subtitle = sprintf("CVaR (95%%): %.4f | Breaches: %d", cvar_value, sum(df$Breach))) +
    theme_minimal()
  
  print(p)
}

# Visualization function: Beta scatter plot with regression
plot_beta_regression <- function(portfolio_returns, benchmark_returns) {
  merged <- merge(portfolio_returns, benchmark_returns, join = "inner")
  df <- data.frame(
    Portfolio = as.numeric(merged[, 1]),
    Benchmark = as.numeric(merged[, 2])
  )
  
  model <- lm(Portfolio ~ Benchmark, data = df)
  beta <- coef(model)[2]
  alpha <- coef(model)[1]
  r_squared <- summary(model)$r.squared
  
  p <- ggplot(df, aes(x = Benchmark, y = Portfolio)) +
    geom_point(alpha = 0.5, color = "blue") +
    geom_smooth(method = "lm", color = "red", se = TRUE) +
    labs(title = "Portfolio Beta vs MSCI World",
         x = "Benchmark Returns (MSCI World)",
         y = "Portfolio Returns",
         subtitle = sprintf("Beta: %.4f | Alpha: %.6f | R²: %.4f", beta, alpha, r_squared)) +
    theme_minimal()
  
  print(p)
}

# =============================================================================
# MAIN ANALYSIS WORKFLOW
# =============================================================================

cat("\n")
cat(rep("=", 80), "\n", sep = "")
cat("STARTING FULL PORTFOLIO ANALYSIS - R IMPLEMENTATION\n")
cat(rep("=", 80), "\n", sep = "")

# Define parameters
INITIAL_VALUE <- 100000  # PLN
WEIGHTS <- c(0.50, 0.25, 0.25)  # Pfizer, JPY/PLN, Gold
CONFIDENCE_LEVEL <- 0.95
RISK_FREE_RATE_ANNUAL <- 0.02
RISK_FREE_RATE_DAILY <- RISK_FREE_RATE_ANNUAL / 252
NUM_SIMULATIONS <- 10000

# Define date range (10 years)
end_date <- Sys.Date()
start_date <- end_date - (10 * 365)

# =============================================================================
# STEP 1: LOAD DATA FROM YAHOO FINANCE
# =============================================================================
cat("\n[STEP 1] Loading data from Yahoo Finance...\n")

# Fetch Pfizer (with USD/PLN conversion)
pfizer_prices <- fetch_asset_data("PFE", "Pfizer", "USDPLN=X", start_date, end_date)

# Fetch JPY/PLN
jpy_pln_prices <- fetch_asset_data("JPYPLN=X", "JPY/PLN", NULL, start_date, end_date, max_abs_return = 0.05)

# Fetch Gold (with USD/PLN conversion)
gold_prices <- fetch_asset_data("GC=F", "Gold", "USDPLN=X", start_date, end_date)

# Combine all prices into one xts object
assets_list <- list(pfizer_prices, jpy_pln_prices, gold_prices)
assets_list <- assets_list[!sapply(assets_list, is.null)]

if (length(assets_list) == 0) {
  stop("ERROR: No asset data could be retrieved. Exiting.")
}

prices_df <- do.call(merge, assets_list)
prices_df <- na.omit(prices_df)

asset_names <- colnames(prices_df)
num_assets <- length(asset_names)

# Adjust weights if some assets are missing
if (num_assets < 3) {
  cat(sprintf("WARNING: Only %d assets loaded (expected 3). Adjusting weights...\n", num_assets))
  WEIGHTS <- WEIGHTS[1:num_assets]
  WEIGHTS <- WEIGHTS / sum(WEIGHTS)
}

cat(sprintf("[OK] Portfolio created with %d assets\n", num_assets))
cat(sprintf("[OK] Data loaded: %d dates, %d assets\n", nrow(prices_df), ncol(prices_df)))

# =============================================================================
# STEP 2: CALCULATE RETURNS
# =============================================================================
cat("\n[STEP 2] Calculating returns...\n")

returns_df <- Return.calculate(prices_df, method = "discrete")
returns_df <- na.omit(returns_df)

# Calculate weighted portfolio returns (preserve xts index)
portfolio_matrix <- as.matrix(returns_df) %*% matrix(WEIGHTS, ncol = 1)
portfolio_returns <- xts(portfolio_matrix, order.by = index(returns_df))
colnames(portfolio_returns) <- "Portfolio"

cat(sprintf("[OK] Returns calculated: %d observations\n", nrow(returns_df)))
cat(sprintf("[OK] Portfolio returns calculated: %d observations\n", nrow(portfolio_returns)))

# =============================================================================
# STEP 3: RETURN ANALYSIS
# =============================================================================
cat("\n[STEP 3] Analyzing returns...\n")

# Calculate mean returns at different frequencies
mean_daily <- colMeans(returns_df, na.rm = TRUE)
mean_monthly <- mean_daily * 21  # Approximate 21 trading days per month
mean_yearly <- mean_daily * 252  # 252 trading days per year

portfolio_mean_daily <- mean(portfolio_returns, na.rm = TRUE)
portfolio_mean_monthly <- portfolio_mean_daily * 21
portfolio_mean_yearly <- portfolio_mean_daily * 252

cat(sprintf("[OK] Mean daily returns: %.6f\n", portfolio_mean_daily))
cat(sprintf("[OK] Mean yearly returns: %.4f\n", portfolio_mean_yearly))

# =============================================================================
# STEP 4: VOLATILITY ANALYSIS
# =============================================================================
cat("\n[STEP 4] Analyzing volatility...\n")

# Calculate standard deviation at different frequencies
std_dev_daily <- apply(returns_df, 2, sd, na.rm = TRUE)
std_dev_monthly <- std_dev_daily * sqrt(21)
std_dev_yearly <- std_dev_daily * sqrt(252)

portfolio_std_daily <- sd(portfolio_returns, na.rm = TRUE)
portfolio_std_monthly <- portfolio_std_daily * sqrt(21)
portfolio_std_yearly <- portfolio_std_daily * sqrt(252)

cat(sprintf("[OK] Std dev daily: %.6f\n", portfolio_std_daily))
cat(sprintf("[OK] Std dev yearly: %.4f\n", portfolio_std_yearly))

# =============================================================================
# STEP 5: CORRELATION ANALYSIS
# =============================================================================
cat("\n[STEP 5] Analyzing correlations...\n")

correlation_matrix <- cor(returns_df, use = "complete.obs")
covariance_matrix <- cov(returns_df, use = "complete.obs")

cat(sprintf("[OK] Correlation matrix: %d x %d\n", nrow(correlation_matrix), ncol(correlation_matrix)))
cat(sprintf("[OK] Covariance matrix: %d x %d\n", nrow(covariance_matrix), ncol(covariance_matrix)))

# =============================================================================
# STEP 6: VALUE AT RISK (VaR) - ALL 3 METHODS
# =============================================================================
cat("\n[STEP 6] Calculating Value at Risk (VaR)...\n")

var_results <- calculate_var(portfolio_returns, CONFIDENCE_LEVEL, NUM_SIMULATIONS)

cat(sprintf("[OK] Historical VaR: %.4f\n", var_results$historical))
cat(sprintf("[OK] Parametric VaR: %.4f\n", var_results$parametric))
cat(sprintf("[OK] Monte Carlo VaR: %.4f\n", var_results$monte_carlo))

# =============================================================================
# STEP 7: CONDITIONAL VaR (CVaR / EXPECTED SHORTFALL)
# =============================================================================
cat("\n[STEP 7] Calculating Conditional VaR (Expected Shortfall)...\n")

cvar_results <- calculate_cvar(portfolio_returns, CONFIDENCE_LEVEL, NUM_SIMULATIONS)

cat(sprintf("[OK] Historical CVaR: %.4f\n", cvar_results$historical))
cat(sprintf("[OK] Parametric CVaR: %.4f\n", cvar_results$parametric))
cat(sprintf("[OK] Monte Carlo CVaR: %.4f\n", cvar_results$monte_carlo))

# =============================================================================
# STEP 8: PERFORMANCE ANALYSIS (SHARPE RATIO, BETA, ALPHA)
# =============================================================================
cat("\n[STEP 8] Analyzing performance metrics...\n")

# Fetch benchmark (MSCI World - URTH)
cat("  Loading benchmark data (MSCI World - URTH)...\n")
benchmark_returns <- NULL

tryCatch({
  benchmark_data <- fetch_asset_data("URTH", "MSCI_World", "USDPLN=X", 
                                     start_date = format(start(prices_df), "%Y-%m-%d"),
                                     end_date = format(end(prices_df), "%Y-%m-%d"))
  
  if (!is.null(benchmark_data)) {
    benchmark_returns <- Return.calculate(benchmark_data, method = "discrete")
    benchmark_returns <- na.omit(benchmark_returns)
    cat(sprintf("  [OK] Benchmark data loaded: %d observations\n", nrow(benchmark_returns)))
  }
}, error = function(e) {
  cat(sprintf("  [WARN] Could not load benchmark: %s\n", e$message))
})

# Calculate performance metrics
performance_results <- calculate_performance(portfolio_returns, benchmark_returns, RISK_FREE_RATE_DAILY)

cat(sprintf("[OK] Sharpe Ratio: %.4f\n", performance_results$sharpe_ratio))
cat(sprintf("[OK] Beta (vs MSCI World): %.4f\n", performance_results$beta))
cat(sprintf("[OK] Alpha: %.6f\n", performance_results$alpha))

# =============================================================================
# STEP 9: GENERATE VISUALIZATIONS (DISPLAY ONLY - NO EXPORT)
# =============================================================================
cat("\n[STEP 9] Generating visualizations...\n")

# Set up plotting parameters
par(mfrow = c(1, 1))

# 1. Price timeseries rebased to 100
cat("[PLOT 1] Price timeseries rebased to 100...\n")
prices_rebased <- sweep(prices_df, 2, as.numeric(prices_df[1, ]), "/") * 100
plot_price_timeseries(prices_rebased)
readline(prompt = "Press [Enter] to continue to next plot...")

# 2. Return distribution histograms
cat("[PLOT 2] Return distributions...\n")
plot_return_distributions(returns_df)
readline(prompt = "Press [Enter] to continue to next plot...")

# 3. Correlation heatmap
cat("[PLOT 3] Correlation heatmap...\n")
plot_correlation_heatmap(correlation_matrix)
readline(prompt = "Press [Enter] to continue to next plot...")

# 4. Rolling volatility
cat("[PLOT 4] Rolling volatility...\n")
plot_rolling_volatility(returns_df, window = 20)
readline(prompt = "Press [Enter] to continue to next plot...")

# 5. VaR timeseries (Historical)
cat("[PLOT 5] VaR timeseries (Historical method)...\n")
plot_var_timeseries(portfolio_returns, var_results$historical, "Historical")
readline(prompt = "Press [Enter] to continue to next plot...")

# 6. VaR timeseries (Parametric)
cat("[PLOT 6] VaR timeseries (Parametric method)...\n")
plot_var_timeseries(portfolio_returns, var_results$parametric, "Parametric")
readline(prompt = "Press [Enter] to continue to next plot...")

# 7. VaR timeseries (Monte Carlo)
cat("[PLOT 7] VaR timeseries (Monte Carlo method)...\n")
plot_var_timeseries(portfolio_returns, var_results$monte_carlo, "Monte Carlo")
readline(prompt = "Press [Enter] to continue to next plot...")

# 8. CVaR/Expected Shortfall timeseries
cat("[PLOT 8] Expected Shortfall timeseries...\n")
plot_cvar_timeseries(portfolio_returns, cvar_results$historical)
readline(prompt = "Press [Enter] to continue to next plot...")

# 9. Beta scatter plot with regression
if (!is.null(benchmark_returns)) {
  cat("[PLOT 9] Beta scatter plot with regression line...\n")
  plot_beta_regression(portfolio_returns, benchmark_returns)
  readline(prompt = "Press [Enter] to continue...")
} else {
  cat("[PLOT 9] Skipped (no benchmark data available)\n")
}

# =============================================================================
# STEP 10: SUMMARY AND RESULTS
# =============================================================================
cat("\n")
cat(rep("=", 80), "\n", sep = "")
cat("ANALYSIS COMPLETE - SUMMARY\n")
cat(rep("=", 80), "\n", sep = "")

cat(sprintf("\n Portfolio Value: %s PLN\n", format(INITIAL_VALUE, big.mark = ",")))
cat(sprintf(" Asset Allocation:\n"))
for (i in 1:length(asset_names)) {
  cat(sprintf("   - %s: %.0f%%\n", asset_names[i], WEIGHTS[i] * 100))
}
cat(sprintf(" Time Period: %s to %s\n", format(start(prices_df), "%Y-%m-%d"), format(end(prices_df), "%Y-%m-%d")))
cat(sprintf(" Number of observations: %d\n", nrow(returns_df)))

cat("\n Portfolio Returns:\n")
cat(sprintf("  - Daily Mean: %.6f\n", portfolio_mean_daily))
cat(sprintf("  - Monthly Mean: %.6f\n", portfolio_mean_monthly))
cat(sprintf("  - Yearly Mean: %.4f\n", portfolio_mean_yearly))

cat("\n Risk Metrics:\n")
cat(sprintf("  - Daily Volatility: %.6f\n", portfolio_std_daily))
cat(sprintf("  - Monthly Volatility: %.6f\n", portfolio_std_monthly))
cat(sprintf("  - Yearly Volatility: %.4f\n", portfolio_std_yearly))
cat(sprintf("  - Sharpe Ratio: %.4f\n", performance_results$sharpe_ratio))
cat(sprintf("  - Beta: %.4f\n", performance_results$beta))
cat(sprintf("  - Alpha: %.6f\n", performance_results$alpha))

cat("\n Value at Risk (95%% confidence):\n")
cat(sprintf("  - Historical VaR: %.4f\n", var_results$historical))
cat(sprintf("  - Parametric VaR: %.4f\n", var_results$parametric))
cat(sprintf("  - Monte Carlo VaR: %.4f\n", var_results$monte_carlo))

cat("\n Expected Shortfall / CVaR (95%% confidence):\n")
cat(sprintf("  - Historical CVaR: %.4f\n", cvar_results$historical))
cat(sprintf("  - Parametric CVaR: %.4f\n", cvar_results$parametric))
cat(sprintf("  - Monte Carlo CVaR: %.4f\n", cvar_results$monte_carlo))

cat("\n Asset-Level Statistics:\n")
cat("\n Mean Daily Returns:\n")
print(mean_daily)
cat("\n Daily Standard Deviation:\n")
print(std_dev_daily)
cat("\n Correlation Matrix:\n")
print(round(correlation_matrix, 4))

cat("\n")
cat(rep("=", 80), "\n", sep = "")
cat("Analysis completed successfully!\n")
cat(rep("=", 80), "\n", sep = "")
