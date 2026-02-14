#!/usr/bin/env python3
"""
Main script to run the investment risk assessment.

This script estimates the risk of an investment portfolio consisting of:
- Pfizer stock: 50%
- JPY currency: 25%
- Gold commodity: 25%

Base currency: Polish Złoty (PLN)
"""
import sys
from src.data_fetcher import DataFetcher
from src.sample_data import SampleDataGenerator
from src.risk_calculator import PortfolioRiskCalculator


def main(use_live_data=False):
    """Main function to run the risk assessment."""
    print("=" * 70)
    print("Investment Risk Assessment - Empirical Methods")
    print("=" * 70)
    print()
    print("Portfolio Composition:")
    print("  - Pfizer (PFE): 50%")
    print("  - Japanese Yen (JPY): 25%")
    print("  - Gold: 25%")
    print("  - Base Currency: Polish Złoty (PLN)")
    print()
    print("=" * 70)
    print()
    
    # Define portfolio weights
    weights = {
        'PFE': 0.50,   # Pfizer stock
        'JPY': 0.25,   # Japanese Yen
        'GOLD': 0.25   # Gold
    }
    
    # Fetch or generate data
    if use_live_data:
        print("Fetching live historical data (1 year) from Yahoo Finance...")
        print()
        try:
            fetcher = DataFetcher()
            portfolio_data = fetcher.fetch_all_portfolio_data()
            print()
            print("Live data fetched successfully!")
        except Exception as e:
            print(f"Error fetching live data: {e}")
            print("Falling back to sample data...")
            print()
            use_live_data = False
    
    if not use_live_data:
        print("Generating sample data (1 year) for demonstration...")
        print()
        generator = SampleDataGenerator()
        portfolio_data = generator.generate_portfolio_data()
        print("Sample data generated successfully!")
        print("(Note: Using synthetic data for demonstration purposes)")
    
    print()
    
    # Display data summary
    print("Data Summary:")
    for asset, data in portfolio_data.items():
        if len(data) == 0:
            print(f"  {asset}: No data available")
        else:
            print(f"  {asset}: {len(data)} data points from {data.index[0].date()} to {data.index[-1].date()}")
    print()
    print("=" * 70)
    print()
    
    # Calculate risk metrics
    print("Calculating risk metrics...")
    calculator = PortfolioRiskCalculator(portfolio_data, weights)
    metrics = calculator.calculate_all_metrics()
    
    print()
    print("=" * 70)
    print("RISK ASSESSMENT RESULTS")
    print("=" * 70)
    print()
    
    # Display results
    for metric_name, metric_value in metrics.items():
        if 'Ratio' in metric_name:
            print(f"{metric_name:.<50} {metric_value:.4f}")
        else:
            print(f"{metric_name:.<50} {metric_value:.2f}")
    
    print()
    print("=" * 70)
    print()
    
    # Interpretation
    print("INTERPRETATION:")
    print()
    volatility = metrics['Annual Volatility (%)']
    var = metrics['Value at Risk 95% (%)']
    sharpe = metrics['Sharpe Ratio']
    
    print(f"1. Volatility: The portfolio has an annual volatility of {volatility:.2f}%.")
    if volatility < 15:
        print("   This indicates LOW risk.")
    elif volatility < 25:
        print("   This indicates MODERATE risk.")
    else:
        print("   This indicates HIGH risk.")
    
    print()
    print(f"2. Value at Risk (95%): With 95% confidence, the maximum expected")
    print(f"   daily loss is {var:.2f}% of the portfolio value.")
    
    print()
    print(f"3. Sharpe Ratio: {sharpe:.4f}")
    if sharpe < 0:
        print("   POOR: Returns are below the risk-free rate.")
    elif sharpe < 1:
        print("   SUBOPTIMAL: Risk-adjusted returns are below average.")
    elif sharpe < 2:
        print("   GOOD: Risk-adjusted returns are above average.")
    else:
        print("   EXCELLENT: Risk-adjusted returns are very good.")
    
    print()
    print("=" * 70)
    print()
    print("Assessment completed successfully!")
    print()


if __name__ == "__main__":
    # Check command line arguments for live data flag
    use_live = "--live" in sys.argv
    main(use_live_data=use_live)
