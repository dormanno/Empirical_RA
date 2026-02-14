# Class Design for Empirical Risk Assessment Project

## Overview
This document outlines the class structure needed to implement the empirical risk assessment project for a 3-asset portfolio (Pfizer, JPY, Gold) with risk metrics calculated in Python and R.

---

## Core Data Classes

### 1. `Asset`
**Purpose**: Represent individual asset with its price data and metadata

**Properties**:
- `name: str` - Asset identifier (e.g., 'PFE', 'JPY/PLN', 'XAU/USD')
- `ticker: str` - Yahoo Finance ticker symbol
- `asset_type: str` - Type ('stock', 'commodity', 'currency')
- `base_currency: str` - Original currency of asset
- `target_currency: str` - Currency to convert to (PLN)
- `prices: pd.Series` - Time series of daily prices
- `dividends: pd.Series` - Dividend data (if applicable)
- `description: str` - Asset description

**Methods**:
- `fetch_data(start_date: str, end_date: str) -> None` - Fetch historical data from Yahoo Finance
- `adjust_for_dividends() -> pd.Series` - Adjust prices for stock splits/dividends
- `calculate_returns(frequency: str) -> pd.Series` - Calculate returns at specified frequency (daily, monthly, yearly)
- `validate_data() -> bool` - Check for missing values and data quality

---

### 2. `Portfolio`
**Purpose**: Manage portfolio composition and overall metrics

**Properties**:
- `assets: Dict[str, Asset]` - Dictionary of assets in portfolio
- `weights: Dict[str, float]` - Portfolio weights (sum to 1.0)
- `initial_value: float` - Initial portfolio value in PLN
- `base_currency: str` - Portfolio base currency (PLN)
- `prices_df: pd.DataFrame` - Combined price data for all assets
- `returns_df: pd.DataFrame` - Combined returns data for all assets
- `rebalance_dates: List[date]` - Rebalancing dates (if applicable)

**Methods**:
- `add_asset(asset: Asset, weight: float) -> None` - Add asset to portfolio
- `set_weights(weights: Dict[str, float]) -> None` - Update portfolio weights with validation
- `get_portfolio_prices() -> pd.Series` - Calculate portfolio price time series
- `get_portfolio_returns(frequency: str) -> pd.Series` - Calculate portfolio returns
- `get_weights() -> Dict[str, float]` - Return current weights
- `validate_composition() -> bool` - Ensure weights sum to 1.0, all initialized

---

## Risk Metrics Classes

### 3. `Analyzer` (Base Class)
**Purpose**: Abstract base class for all risk/return analyzers providing common functionality

**Properties**:
- `returns_df: pd.DataFrame` - Returns data for all assets
- `frequency: str` - Frequency of returns ('daily', 'monthly', 'yearly')
- `results_cache: Dict` - Cache for computed results to avoid recalculation
- `periods_per_year: Dict[str, int]` - Mapping of frequency to periods (daily: 252, monthly: 12, yearly: 1)

**Methods** (Abstract/Common):
- `calculate() -> Dict` - Abstract method for main analysis calculation by subclass
- `get_results() -> Dict` - Get cached results or compute if not cached
- `clear_cache() -> None` - Clear cached results
- `_annualize_metric(periodic_value: float, frequency: str) -> float` - Annualize any periodic metric
- `_get_periods_per_year(frequency: str) -> int` - Get number of periods in a year
- `_validate_frequency(frequency: str) -> bool` - Validate frequency parameter
- `_prepare_returns_data(drop_na: bool = True) -> pd.DataFrame` - Common data preparation

---

### 3a. `ReturnAnalyzer(Analyzer)`
**Purpose**: Calculate return statistics and distributions

**Properties** (in addition to parent):
- `portfolio_returns: pd.Series` - Portfolio returns
- `risk_free_rate: float` - Risk-free rate (Polish T-bills)

**Methods**:
- `calculate() -> Dict` - Execute all return analysis
- `calculate_mean_returns(frequency: str) -> Dict[str, float]` - Mean returns by asset and portfolio
- `calculate_log_returns(prices_df: pd.DataFrame) -> pd.DataFrame` - Calculate log returns
- `get_return_distribution_stats() -> Dict` - Skewness, kurtosis, percentiles, etc.

---

### 3b. `VolatilityAnalyzer(Analyzer)`
**Purpose**: Calculate volatility and dispersion measures

**Properties** (in addition to parent):
- `portfolio_returns: pd.Series` - Portfolio returns

**Methods**:
- `calculate() -> Dict` - Execute all volatility analysis
- `calculate_std_dev(frequency: str) -> Dict[str, float]` - Standard deviation by asset and portfolio
- `calculate_variance(frequency: str) -> Dict[str, float]` - Variance
- `calculate_rolling_volatility(window: int) -> Dict[str, pd.Series]` - Rolling volatility
- `calculate_downside_deviation(min_return: float = 0) -> Dict[str, float]` - Downside deviation below target

---

### 3c. `CorrelationAnalyzer(Analyzer)`
**Purpose**: Analyze correlations and covariances between assets

**Methods**:
- `calculate() -> Dict` - Execute all correlation analysis
- `calculate_correlation_matrix() -> pd.DataFrame` - Pearson correlation matrix
- `calculate_covariance_matrix() -> pd.DataFrame` - Covariance matrix
- `get_asset_correlation(asset1: str, asset2: str) -> float` - Pairwise correlation
- `calculate_portmanteau_test() -> Dict` - Test for autocorrelation in returns

---

### 4. `VaRCalculator` (Base Class)
**Purpose**: Abstract base class for Value at Risk calculations

**Properties**:
- `portfolio_returns: pd.Series` - Portfolio returns
- `asset_returns_df: pd.DataFrame` - Individual asset returns
- `confidence_level: float` - Default 0.95 (95%)

**Methods**:
- `calculate_var(confidence: float = 0.95) -> Dict[str, float]` - Abstract method to be implemented by subclasses
- `calculate_var_for_horizons(horizons: List[int]) -> Dict` - VaR for multiple time horizons
- `calculate_var_breaches(var_value: float) -> List[date]` - Identify VaR breaches in history
- `_scale_var_to_horizon(single_period_var: float, periods: int) -> float` - Helper to scale VaR across time horizons

---

### 4a. `HistoricalVaRCalculator(VaRCalculator)`
**Purpose**: Calculate VaR using historical simulation methodology

**Methods**:
- `calculate_var(confidence: float = 0.95) -> Dict[str, float]` - Historical simulation VaR using empirical quantiles
- `_calculate_empirical_quantile(returns: pd.Series, confidence: float) -> float` - Compute empirical quantile

---

### 4b. `ParametricVaRCalculator(VaRCalculator)`
**Purpose**: Calculate VaR using variance-covariance (parametric) methodology

**Properties** (in addition to parent):
- `mean: float` - Mean of portfolio returns
- `std: float` - Standard deviation of portfolio returns

**Methods**:
- `calculate_var(confidence: float = 0.95) -> Dict[str, float]` - Variance-covariance VaR assuming normality
- `_get_normal_quantile(confidence: float) -> float` - Get critical value from standard normal distribution

---

### 4c. `MonteCarloVaRCalculator(VaRCalculator)`
**Purpose**: Calculate VaR using Monte Carlo simulation methodology

**Properties** (in addition to parent):
- `num_simulations: int` - Number of Monte Carlo simulations (default 10000)
- `mean: float` - Mean returns for sim initialization
- `covariance_matrix: pd.DataFrame` - Covariance matrix for multivariate normal sampling

**Methods**:
- `calculate_var(confidence: float = 0.95) -> Dict[str, float]` - Monte Carlo VaR from simulated paths
- `_generate_simulated_returns(num_paths: int, num_periods: int) -> np.ndarray` - Generate multivariate normal paths
- `_calculate_quantile_from_simulations(simulated_returns: np.ndarray, confidence: float) -> float` - Extract VaR from sim results

---

### 5. `ConditionalVaRCalculator(VaRCalculator)`
**Purpose**: Calculate Conditional VaR / Expected Shortfall (inherits from VaRCalculator)

**Properties** (in addition to parent):
- `var_calculator: VaRCalculator` - Instance of a VaR calculator to identify threshold (optional - can use any method)

**Methods**:
- `calculate_cvar(confidence: float = 0.95) -> Dict[str, float]` - CVaR for assets and portfolio (mean of returns below VaR)
- `calculate_cvar_for_horizons(horizons: List[int]) -> Dict` - CVaR for multiple time horizons
- `_get_var_threshold(returns: pd.Series, confidence: float) -> float` - Get VaR threshold (uses historical method)
- `_calculate_mean_below_threshold(returns: pd.Series, threshold: float) -> float` - Calculate mean of returns below VaR

**Note on Inheritance**: CVaR inherits from VaRCalculator because:
1. Both are tail-risk metrics dealing with extreme losses
2. CVaR fundamentally depends on the VaR threshold (mathematically: CVaR = E[returns | returns ≤ VaR])
3. Both share common properties (confidence_level, portfolio_returns) and helper methods
4. Inheritance allows flexible implementation where CVaR can use any VaR methodology to find the threshold
5. Conceptually, CVaR "is-a" more refined VaR calculation (it's VaR + expected losses beyond VaR)

---

### 6. `PerformanceAnalyzer(Analyzer)`
**Purpose**: Calculate risk-adjusted performance metrics

**Properties** (in addition to parent):
- `portfolio_returns: pd.Series` - Portfolio returns
- `asset_returns_df: pd.DataFrame` - Individual asset returns
- `risk_free_rate: float` - Risk-free rate (Polish T-bills)
- `benchmark_returns: pd.Series` - Benchmark (MSCI World) returns
- `portfolio_volatility: float` - Portfolio standard deviation

**Methods**:
- `calculate() -> Dict` - Execute all performance analysis
- `calculate_sharpe_ratio() -> Dict[str, float]` - Sharpe ratio for assets and portfolio
- `calculate_sortino_ratio(min_return: float = 0) -> Dict[str, float]` - Sortino ratio
- `calculate_beta() -> Dict[str, float]` - Beta relative to benchmark
- `calculate_alpha() -> Dict[str, float]` - Alpha relative to benchmark
- `calculate_treynor_ratio() -> Dict[str, float]` - Treynor ratio
- `calculate_information_ratio() -> Dict[str, float]` - Information ratio vs benchmark
- `calculate_max_drawdown() -> Dict[str, float]` - Maximum drawdown

---

### 7. `BenchmarkAnalyzer(Analyzer)`
**Purpose**: Fetch and analyze benchmark data (MSCI World)

**Properties** (in addition to parent):
- `benchmark_ticker: str` - MSCI World ticker
- `benchmark_prices: pd.Series` - Benchmark price data
- `benchmark_returns: pd.Series` - Benchmark returns (overrides parent for benchmark-specific use)
- `start_date: str` - Analysis start date
- `end_date: str` - Analysis end date

**Methods**:
- `calculate() -> Dict` - Execute all benchmark analysis
- `fetch_benchmark_data(start_date: str, end_date: str) -> None` - Fetch MSCI World data and calculate returns
- `calculate_benchmark_returns() -> pd.Series` - Calculate returns for benchmark
- `get_benchmark_stats() -> Dict` - Mean return, volatility, Sharpe ratio, etc.

---

## Data Management Classes

### 8. `DataManager`
**Purpose**: Centralized data handling and storage

**Properties**:
- `data_dir: str` - Directory for storing downloaded data
- `assets: Dict[str, Asset]` - Cache of loaded assets
- `cache: Dict` - In-memory cache of data

**Methods**:
- `fetch_and_store_data(assets: List[str], start_date: str, end_date: str) -> None` - Fetch and save data
- `load_data(asset: str) -> pd.DataFrame` - Load data from cache or disk
- `export_data(asset: str, filepath: str) -> None` - Export to CSV
- `validate_data_integrity() -> bool` - Check consistency across assets
- `handle_missing_data(strategy: str = 'fail') -> None` - Handle missing values

---

## Visualization Classes

### 9. `PortfolioVisualizer`
**Purpose**: Create visualizations for portfolio analysis

**Methods**:
- `plot_price_timeseries(prices_df: pd.DataFrame, save_path: str = None) -> None` - Time series rebased to 100
- `plot_returns_distributions(returns_df: pd.DataFrame, save_path: str = None) -> None` - Return distribution histograms
- `plot_correlation_heatmap(corr_matrix: pd.DataFrame, save_path: str = None) -> None` - Correlation heatmap
- `plot_rolling_volatility(rolling_vol: Dict, save_path: str = None) -> None` - Rolling volatility chart
- `plot_cumulative_returns(portfolio_returns: pd.Series, save_path: str = None) -> None` - Cumulative returns
- `plot_drawdown(portfolio_returns: pd.Series, save_path: str = None) -> None` - Drawdown analysis
- `plot_var_timeseries(returns: pd.Series, var_breaches: List, save_path: str = None) -> None` - VaR with breaches highlighted

---

### 10. `RegressionVisualizer`
**Purpose**: Visualize asset sensitivity to benchmark

**Methods**:
- `plot_beta_regression(asset_returns: pd.Series, benchmark_returns: pd.Series, asset_name: str, save_path: str = None) -> None` - Scatter plot with regression line
- `plot_all_betas(returns_df: pd.DataFrame, benchmark_returns: pd.Series, save_path: str = None) -> None` - Multiple beta plots

---

## Reporting Classes

### 11. `ReportGenerator`
**Purpose**: Generate analysis reports and export results

**Properties**:
- `output_dir: str` - Directory for report output
- `analysis_results: Dict` - Aggregated analysis results
- `visualizations: Dict[str, str]` - Filepaths of generated visualizations

**Methods**:
- `compile_results(analyses: Dict) -> None` - Aggregate all analysis results
- `export_to_csv(data: pd.DataFrame, filename: str) -> None` - Export tables to CSV
- `save_figures(figures: Dict[str, plt.Figure]) -> None` - Save all visualizations as PNG
- `generate_summary_table() -> pd.DataFrame` - Create summary statistics table
- `save_json_results(filename: str) -> None` - Save results as JSON for R/Python transfer

---

### 12. `EssayReportGenerator`
**Purpose**: Generate PDF essay report with analysis

**Properties**:
- `title: str` - Report title
- `author: str` - Author name
- `analysis_results: Dict` - Results to report
- `visualizations: Dict` - Generated charts/tables

**Methods**:
- `generate_data_section() -> str` - Markdown for data sources/collection
- `generate_methodology_section() -> str` - Markdown for methods used
- `generate_results_section() -> str` - Markdown with tables, figures, analysis
- `generate_discussion_section() -> str` - Markdown for interpretation/limitations/recommendations
- `generate_pdf(output_path: str) -> None` - Convert to PDF with APA formatting
- `generate_references() -> str` - Generate APA formatted references

---

## Orchestration Class

### 13. `RiskAssessmentEngine`
**Purpose**: Main orchestrator coordinating all analyses

**Properties**:
- `portfolio: Portfolio` - Portfolio object
- `data_manager: DataManager` - Data handling
- `return_analyzer: ReturnAnalyzer` - Return calculations
- `volatility_analyzer: VolatilityAnalyzer` - Volatility calculations
- `correlation_analyzer: CorrelationAnalyzer` - Correlation analysis
- `historical_var_calculator: HistoricalVaRCalculator` - Historical simulation VaR
- `parametric_var_calculator: ParametricVaRCalculator` - Variance-covariance VaR
- `monte_carlo_var_calculator: MonteCarloVaRCalculator` - Monte Carlo VaR
- `cvar_calculator: ConditionalVaRCalculator` - CVaR calculations
- `performance_analyzer: PerformanceAnalyzer` - Performance metrics
- `benchmark_analyzer: BenchmarkAnalyzer` - Benchmark analysis
- `visualizer: PortfolioVisualizer` - Visualizations
- `regression_visualizer: RegressionVisualizer` - Beta/regression plots
- `report_generator: ReportGenerator` - Results export
- `essay_generator: EssayReportGenerator` - PDF essay generation
- `config: Dict` - Configuration settings
- `results: Dict` - Aggregated results

**Methods**:
- `initialize(config_path: str) -> None` - Initialize from config file
- `run_full_analysis() -> Dict` - Execute complete pipeline
- `run_returns_analysis() -> Dict` - Return-specific analysis
- `run_volatility_analysis() -> Dict` - Volatility-specific analysis
- `run_risk_metrics_analysis() -> Dict` - VaR (all 3 methods), CVaR, Sharpe, Beta
- `run_benchmark_comparison() -> Dict` - Compare with MSCI World
- `generate_all_visualizations() -> None` - Create all charts
- `export_all_results(output_dir: str) -> None` - Export CSV and PNG files
- `generate_essay_report(output_path: str) -> None` - Generate PDF report
- `get_summary_statistics() -> Dict` - Return all summary metrics

---

## Configuration Class

### 14. `AnalysisConfig`
**Purpose**: Manage analysis configuration and parameters

**Properties**:
- `start_date: str` - Analysis start date
- `end_date: str` - Analysis end date
- `portfolio_assets: Dict[str, float]` - Asset tickers and weights
- `initial_value: float` - Initial portfolio value in PLN
- `risk_free_rate: float` - Risk-free rate for Sharpe ratio
- `confidence_level: float` - VaR/CVaR confidence (default 0.95)
- `time_horizons: List[int]` - Horizons in days (e.g., [1, 21, 252])
- `monte_carlo_simulations: int` - Number of MC simulations (default 10000)
- `rolling_window: int` - Window for rolling volatility
- `benchmark_ticker: str` - MSCI World ticker

**Methods**:
- `load_from_file(config_file: str) -> None` - Load configuration from JSON/YAML
- `save_to_file(config_file: str) -> None` - Save configuration
- `validate_config() -> bool` - Validate all parameters
- `to_dict() -> Dict` - Convert to dictionary

---

## Summary of Dependencies and Inheritance Hierarchy

### Inheritance Hierarchies
```
Analyzer (base class)
├── ReturnAnalyzer
├── VolatilityAnalyzer
├── CorrelationAnalyzer
├── PerformanceAnalyzer
└── BenchmarkAnalyzer

VaRCalculator (base class)
├── HistoricalVaRCalculator
├── ParametricVaRCalculator
├── MonteCarloVaRCalculator
└── ConditionalVaRCalculator
```

### Data Flow
**Asset** → Foundation data class  
**Portfolio** → Contains Assets, feeds into analyzers  
**DataManager** → Manages Asset data  
**Analyzer** (base class) → Provides common properties, caching, and annualization methods  
**ReturnAnalyzer(Analyzer), VolatilityAnalyzer(Analyzer), CorrelationAnalyzer(Analyzer)** → Analyze Portfolio returns  
**PerformanceAnalyzer(Analyzer)** → Analyze risk-adjusted performance and benchmark sensitivity  
**BenchmarkAnalyzer(Analyzer)** → Fetch and analyze benchmark (MSCI World) data  
**VaRCalculator** (hierarchy) → Calculate Value at Risk using three methodologies  
**ConditionalVaRCalculator(VaRCalculator)** → Calculate CVaR/Expected Shortfall  
**PortfolioVisualizer, RegressionVisualizer** → Use outputs from analyzers  
**ReportGenerator, EssayReportGenerator** → Aggregate and export results  
**RiskAssessmentEngine** → Orchestrates all classes  
**AnalysisConfig** → Configures all components  

---

## Notes for Implementation

1. **Python**: Use `pandas.DataFrame`, `numpy`, `scipy.stats`, `matplotlib`, `seaborn`, `python-dateutil`
2. **R**: Use `quantmod`, `PerformanceAnalytics`, `ggplot2`, `tidyverse`, `TTR`
3. Currency conversion should be handled in Asset class when prices are fetched
4. All calculations should support multiple time horizons: daily, monthly, yearly (except VARs)
5. Risk-free rate can be stored as singleton or in AnalysisConfig
6. **Analyzer Base Class (Pattern for all analyzers)**:
   - Common properties: `returns_df`, `frequency`, `results_cache`, `periods_per_year`
   - All analyzers inherit `_annualize_metric()`, `_get_periods_per_year()`, and `_validate_frequency()` 
   - Implement caching to avoid recalculating metrics
   - All subclasses implement `calculate()` method that returns Dict with results
   - Frequency parameter consistently used: 'daily' (252), 'monthly' (12), 'yearly' (1)
   - Use `get_results()` to access cached or newly computed results
7. VaR Calculator Hierarchy:
   - Base `VaRCalculator` class provides common functionality and abstract interface
   - Three concrete implementations: Historical (empirical quantiles), Parametric (assumes normality), Monte Carlo (simulations)
   - Each calculator uses `portfolio_returns` and optionally `asset_returns_df` for individual asset VaR
   - Supports scaling VaR across time horizons using the square-root-of-time rule
8. ConditionalVaR (CVaR/Expected Shortfall):
   - Inherits from VaRCalculator because it is mathematically defined as E[returns | returns ≤ VaR threshold]
   - Can use any VaR methodology to identify the threshold, then calculate mean of returns below threshold
   - More robust than VaR as it accounts for tail severity, not just tail probability
   - This inheritance structure allows flexible implementation and code reuse
9. Portfolio composition: 50% Pfizer, 25% JPY, 25% Gold with fixed weights (no rebalancing)

