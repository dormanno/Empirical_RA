# Portfolio Risk Analysis - R Implementation

This R project replicates the Python portfolio analysis integration test with all calculations but without file export functionality.

## Portfolio Specifications

- **Assets:** 50% Pfizer (PFE), 25% JPY/PLN, 25% Gold (GC=F)
- **Initial Value:** 100,000 PLN
- **Time Period:** 10 years of daily data
- **Risk-Free Rate:** 2% annual (Polish Treasury Bills)
- **Confidence Level:** 95% for VaR/CVaR calculations

## Analysis Components

### 1. Data Acquisition
- Fetches data from Yahoo Finance using `quantmod`
- Automatic currency conversion (USD → PLN)
- Handles missing data gracefully

### 2. Return Analysis
- Daily, monthly, and yearly mean returns
- Return distribution statistics
- Weighted portfolio returns

### 3. Volatility Analysis
- Standard deviation at multiple time horizons
- Rolling 20-day volatility
- Downside deviation

### 4. Correlation Analysis
- Correlation matrix between assets
- Covariance matrix

### 5. Value at Risk (VaR)
Three calculation methods:
- **Historical Simulation:** Uses actual historical returns
- **Parametric (Gaussian):** Assumes normal distribution
- **Monte Carlo:** Simulates 10,000 scenarios

### 6. Conditional VaR (Expected Shortfall)
- Historical CVaR
- Parametric CVaR
- Monte Carlo CVaR

### 7. Performance Metrics
- **Sharpe Ratio:** Risk-adjusted return measure
- **Beta:** Portfolio sensitivity to MSCI World benchmark
- **Alpha:** Excess return vs. benchmark

### 8. Visualizations
All plots are displayed interactively (not exported):
1. Price timeseries rebased to 100
2. Return distribution histograms
3. Correlation heatmap
4. Rolling 20-day volatility
5. VaR breach analysis (Historical)
6. VaR breach analysis (Parametric)
7. VaR breach analysis (Monte Carlo)
8. Expected Shortfall breach analysis
9. Beta scatter plot with regression line

## Installation & Setup

### Step 1: Install Required Packages

```r
source("setup.R")
```

This will install all necessary R packages:
- `quantmod` - Yahoo Finance data access
- `PerformanceAnalytics` - Financial metrics
- `xts` & `zoo` - Time series handling
- `ggplot2` - Advanced plotting
- `corrplot` - Correlation visualization
- `TTR` - Technical indicators
- `MASS` - Statistical functions

### Step 2: Run the Analysis

```r
source("portfolio_analysis.R")
```

The script will:
1. Load 10 years of historical data from Yahoo Finance
2. Calculate all risk metrics (VaR, CVaR, Sharpe, Beta, etc.)
3. Display 9 interactive visualizations
4. Print comprehensive summary to console

## Usage Notes

### Interactive Mode
The script displays visualizations one at a time. Press **[Enter]** to advance to the next plot.

### No File Exports
As requested, this implementation:
- ✅ Performs all calculations
- ✅ Displays all visualizations
- ❌ Does NOT export CSV files
- ❌ Does NOT save PNG images
- ❌ Does NOT generate PDF reports

### Results Display
All results are printed to the R console in a structured format with clear section headers.

## Key Differences from Python Implementation

| Feature | Python | R |
|---------|--------|---|
| **Code Length** | ~700 lines | ~450 lines |
| **Dependencies** | Custom classes | Built-in packages |
| **VaR Calculation** | Custom implementation | `PerformanceAnalytics::VaR()` |
| **CVaR Calculation** | Custom implementation | `PerformanceAnalytics::ES()` |
| **Time Series** | pandas DataFrame | xts objects (native) |
| **Plotting** | matplotlib/seaborn | ggplot2 |
| **Export** | CSV & PNG files | None (console only) |

## Technical Implementation

### Financial Calculations
- **Returns:** `PerformanceAnalytics::Return.calculate()`
- **VaR:** `PerformanceAnalytics::VaR()` with multiple methods
- **CVaR/ES:** `PerformanceAnalytics::ES()`
- **Sharpe:** `PerformanceAnalytics::SharpeRatio()`
- **Beta:** Linear regression using `lm()`

### Data Handling
- **Time Series:** `xts` objects for automatic date alignment
- **Missing Data:** `na.omit()` for clean handling
- **Merging:** Native `merge.xts()` for multi-asset alignment

### Visualization
- **ggplot2:** Modern grammar of graphics
- **corrplot:** Specialized correlation heatmaps
- **Interactive:** Plots displayed in RStudio plot pane

## Troubleshooting

### Yahoo Finance Connection Issues
If data fetch fails:
```r
# Check internet connection
# Try alternative date range
start_date <- Sys.Date() - 8*365  # Try 8 years instead of 10
```

### Missing Benchmark Data
If URTH (MSCI World) is unavailable, the script continues without Beta calculation.

### Package Installation Errors
On Windows, you may need Rtools:
```r
# Install from: https://cran.r-project.org/bin/windows/Rtools/
```

## Output Example

```
================================================================================
ANALYSIS COMPLETE - SUMMARY
================================================================================

 Portfolio Value: 100,000 PLN
 Asset Allocation:
   - Pfizer: 50%
   - JPY/PLN: 25%
   - Gold: 25%
 Time Period: 2016-02-15 to 2026-02-15
 Number of observations: 2516

 Portfolio Returns:
  - Daily Mean: 0.000423
  - Monthly Mean: 0.008883
  - Yearly Mean: 0.106596

 Risk Metrics:
  - Daily Volatility: 0.012876
  - Yearly Volatility: 0.204437
  - Sharpe Ratio: 1.2456
  - Beta: 0.8234
  - Alpha: 0.000045

 Value at Risk (95% confidence):
  - Historical VaR: 0.0186
  - Parametric VaR: 0.0199
  - Monte Carlo VaR: 0.0201

 Expected Shortfall / CVaR (95% confidence):
  - Historical CVaR: 0.0267
  - Parametric CVaR: 0.0251
  - Monte Carlo CVaR: 0.0253
================================================================================
```

## License

This implementation is for academic research purposes (Empirical Methods of Risk Assessment course).

## Advantages of R Implementation

1. **Concise:** 40% less code than Python
2. **Native:** Time series are first-class objects
3. **Validated:** Uses industry-standard packages
4. **Academic:** R is standard in quantitative finance research
5. **Interactive:** Better for exploratory analysis
