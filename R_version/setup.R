# =============================================================================
# R Package Installation Script for Portfolio Analysis
# =============================================================================
# This script installs all required packages for the portfolio analysis

cat("Installing required R packages for Portfolio Analysis...\n")
cat(strrep("=", 80), "\n")

# List of required packages
required_packages <- c(
  "quantmod",              # Yahoo Finance data & financial functions
  "PerformanceAnalytics",  # Financial performance & risk metrics
  "xts",                   # Time series objects
  "zoo",                   # Time series support
  "TTR",                   # Technical trading rules
  "ggplot2",               # Advanced plotting
  "corrplot",              # Correlation visualization
  "reshape2",              # Data reshaping
  "gridExtra",             # Multiple plot arrangement
  "MASS"                   # Statistical functions (mvrnorm for Monte Carlo)
)

# Function to install packages if not already installed
install_if_missing <- function(package) {
  if (!require(package, character.only = TRUE, quietly = TRUE)) {
    cat("Installing:", package, "\n")
    install.packages(package, dependencies = TRUE, repos = "https://cran.r-project.org")
    library(package, character.only = TRUE)
    cat("  [OK]", package, "installed successfully\n")
  } else {
    cat("  [OK]", package, "already installed\n")
  }
}

# Install all packages
for (pkg in required_packages) {
  install_if_missing(pkg)
}

cat("\n")
cat(strrep("=", 80), "\n")
cat("All packages installed successfully!\n")
cat("You can now run the portfolio analysis script.\n")
cat(strrep("=", 80), "\n")
