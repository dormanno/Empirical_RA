"""Tests for the Empirical Risk Assessment system."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from src.sample_data import SampleDataGenerator
from src.risk_calculator import PortfolioRiskCalculator


def test_sample_data_generation():
    """Test that sample data is generated correctly."""
    generator = SampleDataGenerator(seed=42)
    data = generator.generate_portfolio_data()
    
    # Check all assets are present
    assert 'PFE' in data
    assert 'JPY' in data
    assert 'GOLD' in data
    
    # Check data has reasonable length (around 252 trading days per year)
    for asset, prices in data.items():
        assert len(prices) > 200, f"{asset} should have at least 200 data points"
        assert len(prices) < 300, f"{asset} should have less than 300 data points for 1 year"
    
    print("✓ Sample data generation test passed")


def test_risk_calculations():
    """Test that risk metrics are calculated correctly."""
    generator = SampleDataGenerator(seed=42)
    data = generator.generate_portfolio_data()
    
    weights = {
        'PFE': 0.50,
        'JPY': 0.25,
        'GOLD': 0.25
    }
    
    calculator = PortfolioRiskCalculator(data, weights)
    metrics = calculator.calculate_all_metrics()
    
    # Check all metrics are present
    assert 'Annual Volatility (%)' in metrics
    assert 'Value at Risk 95% (%)' in metrics
    assert 'Conditional VaR 95% (%)' in metrics
    assert 'Sharpe Ratio' in metrics
    assert 'Maximum Drawdown (%)' in metrics
    
    # Check metrics are reasonable (positive and not NaN)
    assert metrics['Annual Volatility (%)'] > 0
    assert not np.isnan(metrics['Annual Volatility (%)'])
    assert metrics['Value at Risk 95% (%)'] > 0
    assert not np.isnan(metrics['Value at Risk 95% (%)'])
    
    print("✓ Risk calculations test passed")


def test_portfolio_weights():
    """Test that portfolio weights sum to 1."""
    weights = {
        'PFE': 0.50,
        'JPY': 0.25,
        'GOLD': 0.25
    }
    
    total_weight = sum(weights.values())
    assert abs(total_weight - 1.0) < 1e-10, "Weights should sum to 1.0"
    
    print("✓ Portfolio weights test passed")


def test_edge_cases():
    """Test edge cases in risk calculations."""
    # Create constant prices (zero volatility)
    dates = pd.bdate_range(start='2025-01-01', end='2025-12-31')
    constant_data = {
        'ASSET1': pd.Series([100.0] * len(dates), index=dates),
        'ASSET2': pd.Series([50.0] * len(dates), index=dates),
        'ASSET3': pd.Series([200.0] * len(dates), index=dates)
    }
    
    weights = {'ASSET1': 0.5, 'ASSET2': 0.25, 'ASSET3': 0.25}
    
    calculator = PortfolioRiskCalculator(constant_data, weights)
    
    # Should handle zero volatility without crashing
    try:
        metrics = calculator.calculate_all_metrics()
        print("✓ Edge case (zero volatility) handled correctly")
    except Exception as e:
        print(f"✗ Edge case test failed: {e}")
        raise


if __name__ == "__main__":
    print("Running Empirical Risk Assessment Tests...")
    print("=" * 70)
    
    test_sample_data_generation()
    test_risk_calculations()
    test_portfolio_weights()
    test_edge_cases()
    
    print("=" * 70)
    print("All tests passed! ✓")
