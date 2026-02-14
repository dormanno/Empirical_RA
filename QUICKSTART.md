# Quick Start Guide

## Installation

1. Navigate to the project directory:
```bash
cd c:\Users\dorma\OneDrive\Repos\Empirical_RA
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run tests to verify:
```bash
pytest tests/ -v
```

## Basic Usage

### 1. Create and Fetch Asset Data

```python
from empirical_ra.core.asset import Asset

# Create an asset
pfizer = Asset(
    name="PFE",
    ticker="PFE",
    asset_type="stock",
    base_currency="USD",
    target_currency="PLN",
    description="Pfizer Inc. stock"
)

# Fetch 10 years of historical data
pfizer.fetch_data("2015-01-01", "2025-01-01")

# Calculate returns
daily_returns = pfizer.calculate_returns("daily")
monthly_returns = pfizer.calculate_returns("monthly")

print(f"Mean daily return: {daily_returns.mean():.4f}")
print(f"Daily volatility: {daily_returns.std():.4f}")
```

### 2. Build a Portfolio

```python
from empirical_ra.core.portfolio import Portfolio

# Create portfolio
portfolio = Portfolio(initial_value=100000.0, base_currency="PLN")

# Add assets with weights (50% Pfizer, 25% JPY, 25% Gold)
portfolio.add_asset(pfizer, 0.5)
portfolio.add_asset(jpy_asset, 0.25)
portfolio.add_asset(gold_asset, 0.25)

# Validate composition
assert portfolio.validate_composition()

# Get portfolio returns
portfolio_returns = portfolio.get_portfolio_returns("daily")
```

### 3. Analyze Returns and Volatility

```python
from empirical_ra.core.return_analyzer import ReturnAnalyzer
from empirical_ra.core.volatility_analyzer import VolatilityAnalyzer

# Get all returns in a DataFrame
returns_df = portfolio.returns_df

# Return analysis
return_analyzer = ReturnAnalyzer(returns_df=returns_df)
return_stats = return_analyzer.calculate()
print(f"Mean returns: {return_stats['mean_returns']}")

# Volatility analysis
vol_analyzer = VolatilityAnalyzer(returns_df=returns_df)
vol_stats = vol_analyzer.calculate()
print(f"Standard deviations: {vol_stats['std_dev']}")
```

### 4. Correlation & Covariance Analysis

```python
from empirical_ra.core.correlation_analyzer import CorrelationAnalyzer

corr_analyzer = CorrelationAnalyzer(returns_df=returns_df)
correlation_matrix = corr_analyzer.calculate_correlation_matrix()
covariance_matrix = corr_analyzer.calculate_covariance_matrix()

print(f"Correlation between PFE and Gold: {corr_analyzer.get_asset_correlation('PFE', 'Gold'):.4f}")
```

### 5. Calculate Value at Risk (3 Methods)

```python
from empirical_ra.risk.historical_var import HistoricalVaRCalculator
from empirical_ra.risk.parametric_var import ParametricVaRCalculator
from empirical_ra.risk.monte_carlo_var import MonteCarloVaRCalculator

# Historical VaR
hist_var = HistoricalVaRCalculator(portfolio_returns=portfolio_returns)
var_hist = hist_var.calculate_var(confidence=0.95)
print(f"Historical VaR (95%): {var_hist['portfolio']:.4f}")

# Parametric VaR (assumes normality)
param_var = ParametricVaRCalculator(portfolio_returns=portfolio_returns)
var_param = param_var.calculate_var(confidence=0.95)
print(f"Parametric VaR (95%): {var_param['portfolio']:.4f}")

# Monte Carlo VaR
mc_var = MonteCarloVaRCalculator(
    portfolio_returns=portfolio_returns,
    asset_returns_df=returns_df,
    num_simulations=10000
)
var_mc = mc_var.calculate_var(confidence=0.95)
print(f"Monte Carlo VaR (95%): {var_mc['portfolio']:.4f}")

# VaR for different time horizons
var_horizons = hist_var.calculate_var_for_horizons([1, 21, 252])
```

### 6. Calculate Conditional VaR (Expected Shortfall)

```python
from empirical_ra.risk.cvar_calc import ConditionalVaRCalculator

cvar_calc = ConditionalVaRCalculator(portfolio_returns=portfolio_returns)
cvar = cvar_calc.calculate_cvar(confidence=0.95)
print(f"CVaR (95%): {cvar['portfolio']:.4f}")

# CVaR is always >= VaR (captures tail risk)
assert cvar['portfolio'] >= var_hist['portfolio']
```

### 7. Performance Metrics

```python
from empirical_ra.core.performance_analyzer import PerformanceAnalyzer
from empirical_ra.core.benchmark_analyzer import BenchmarkAnalyzer

# Fetch benchmark (MSCI World)
bench_analyzer = BenchmarkAnalyzer(
    returns_df=returns_df,
    benchmark_ticker="URTH"
)
bench_analyzer.fetch_benchmark_data("2015-01-01", "2025-01-01")
benchmark_returns = bench_analyzer.benchmark_returns

# Performance analysis
perf = PerformanceAnalyzer(
    returns_df=returns_df,
    portfolio_returns=portfolio_returns,
    asset_returns_df=returns_df,
    benchmark_returns=benchmark_returns,
    risk_free_rate=0.01
)

results = perf.calculate()
print(f"Sharpe Ratio: {results['sharpe']['portfolio']:.4f}")
print(f"Sortino Ratio: {results['sortino']['portfolio']:.4f}")
print(f"Beta vs Benchmark: {results['beta']['portfolio']:.4f}")
print(f"Alpha: {results['alpha']['portfolio']:.4f}")
print(f"Max Drawdown: {results['max_drawdown']['portfolio']:.4f}")
```

### 8. Visualization

```python
from empirical_ra.viz.portfolio_visualizer import PortfolioVisualizer
from empirical_ra.viz.regression_visualizer import RegressionVisualizer

# Portfolio visualizations
viz = PortfolioVisualizer()
viz.plot_price_timeseries(portfolio.prices_df, "output/prices.png")
viz.plot_returns_distributions(returns_df, "output/returns_dist.png")
viz.plot_correlation_heatmap(
    corr_analyzer.calculate_correlation_matrix(),
    "output/correlation.png"
)
viz.plot_rolling_volatility(
    vol_analyzer.calculate_rolling_volatility(window=252),
    "output/rolling_vol.png"
)
viz.plot_cumulative_returns(portfolio_returns, "output/cumulative.png")
viz.plot_drawdown(portfolio_returns, "output/drawdown.png")

# Beta regression plots
reg_viz = RegressionVisualizer()
reg_viz.plot_all_betas(returns_df, benchmark_returns, "output/betas.png")
```

### 9. Reporting and Export

```python
from empirical_ra.report.report_generator import ReportGenerator
from empirical_ra.report.essay_report_generator import EssayReportGenerator

# Compile results
report_gen = ReportGenerator(output_dir="output")
report_gen.compile_results({
    "returns": return_stats,
    "volatility": vol_stats,
    "var": var_hist.calculate_var(),
    "cvar": cvar,
    "performance": results
})

# Export to CSV and JSON
summary = report_gen.generate_summary_table()
report_gen.export_to_csv(summary, "summary_stats.csv")
report_gen.save_json_results("results.json")

# Generate essay report
essay = EssayReportGenerator(
    output_dir="output",
    title="Empirical Risk Assessment: Portfolio Analysis",
    author="Risk Analysis Team"
)
essay.compile_results(report_gen.analysis_results)
essay.generate_pdf("output/report.pdf")
```

### 10. Configuration Management

```python
from empirical_ra.config.analysis_config import AnalysisConfig

# Create configuration
config = AnalysisConfig(
    start_date="2015-01-01",
    end_date="2025-01-01",
    portfolio_assets={"PFE": 0.5, "JPY": 0.25, "GOLD": 0.25},
    initial_value=100000.0,
    base_currency="PLN",
    risk_free_rate=0.01,
    confidence_level=0.95,
    monte_carlo_simulations=10000,
    rolling_window=252
)

# Validate configuration
config.validate_config()

# Save to file (JSON or YAML)
config.save_to_file("config.json")

# Load from file
loaded_config = AnalysisConfig(
    start_date="", end_date="", portfolio_assets={}
)
loaded_config.load_from_file("config.json")
```

### 11. Using the Main Engine

```python
from empirical_ra.engine.risk_assessment_engine import RiskAssessmentEngine

# Initialize engine
engine = RiskAssessmentEngine()

# Configure (can load from file)
config_path = "config.json"
# engine.initialize(config_path)  # Or set config manually

# Run full analysis pipeline
results = engine.run_full_analysis()

# Or run specific analyses
engine.run_returns_analysis()
engine.run_volatility_analysis()
engine.run_risk_metrics_analysis()
engine.run_benchmark_comparison()

# Generate all visualizations
engine.generate_all_visualizations()

# Export all results
engine.export_all_results(output_dir="output")

# Get summary
summary = engine.get_summary_statistics()
```

## Configuration File Example

### config.json
```json
{
  "start_date": "2015-01-01",
  "end_date": "2025-01-01",
  "portfolio_assets": {
    "PFE": 0.5,
    "JPY": 0.25,
    "GOLD": 0.25
  },
  "initial_value": 100000,
  "base_currency": "PLN",
  "risk_free_rate": 0.01,
  "confidence_level": 0.95,
  "time_horizons": [1, 21, 252],
  "monte_carlo_simulations": 10000,
  "rolling_window": 252,
  "benchmark_ticker": "URTH"
}
```

### config.yaml
```yaml
start_date: "2015-01-01"
end_date: "2025-01-01"
portfolio_assets:
  PFE: 0.5
  JPY: 0.25
  GOLD: 0.25
initial_value: 100000
base_currency: PLN
risk_free_rate: 0.01
confidence_level: 0.95
time_horizons: [1, 21, 252]
monte_carlo_simulations: 10000
rolling_window: 252
benchmark_ticker: URTH
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_asset.py -v

# Run specific test class
pytest tests/test_asset.py::TestAsset -v

# Run with coverage report
pytest tests/ --cov=empirical_ra --cov-report=html

# Run with detailed output
pytest tests/ -vv --tb=long
```

## Project Organization

```
Empirical_RA/
├── src/empirical_ra/          # Main package
├── tests/                      # Test suite (41 tests)
├── output/                     # Results directory
├── setup.py                    # Package configuration
├── config.json                 # Configuration file
├── CLASS_DESIGN.md            # Class design document
├── PROJECT_DETAILS.md         # Project specifications
├── README.md                  # Project overview
└── IMPLEMENTATION_SUMMARY.md  # This file
```

## Troubleshooting

**Missing yfinance data:**
```python
# yfinance may have delayed data, try alternative ticker
try:
    asset.fetch_data("2020-01-01", "2025-01-01")
except ValueError as e:
    print(f"Error: {e}")
    # Try with adjusted dates or different ticker
```

**Division by zero errors:**
```python
# Some metrics require non-zero denominators
# Check returns are properly loaded:
assert len(returns_df) > 0
assert returns_df.std().sum() > 0
```

**Out of memory with Monte Carlo:**
```python
# Reduce number of simulations
mc_var = MonteCarloVaRCalculator(
    portfolio_returns=portfolio_returns,
    num_simulations=5000  # Lower from 10000
)
```

## Next Steps

1. Load your portfolio configuration
2. Run the analysis pipeline
3. Generate visualizations
4. Export results to CSV/JSON
5. Create PDF report with findings
