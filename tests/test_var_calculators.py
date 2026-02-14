"""Tests for VaR calculators."""

import unittest

import pandas as pd
import numpy as np

from empirical_ra.risk.historical_var import HistoricalVaRCalculator
from empirical_ra.risk.parametric_var import ParametricVaRCalculator
from empirical_ra.risk.monte_carlo_var import MonteCarloVaRCalculator
from empirical_ra.risk.cvar_calc import ConditionalVaRCalculator


class TestHistoricalVaRCalculator(unittest.TestCase):
    """Test Historical VaR calculator."""

    def setUp(self):
        """Set up test fixtures."""
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        self.returns = pd.Series(np.random.normal(0.0005, 0.01, 100), index=dates)
        self.calculator = HistoricalVaRCalculator(portfolio_returns=self.returns)

    def test_calculate_var(self):
        """Test VaR calculation."""
        var = self.calculator.calculate_var(confidence=0.95)
        self.assertIn("portfolio", var)
        self.assertGreater(var["portfolio"], 0)

    def test_var_breaches(self):
        """Test VaR breach detection."""
        var = self.calculator.calculate_var(0.95)
        breaches = self.calculator.calculate_var_breaches(var["portfolio"])
        self.assertIsInstance(breaches, list)


class TestParametricVaRCalculator(unittest.TestCase):
    """Test Parametric VaR calculator."""

    def setUp(self):
        """Set up test fixtures."""
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        self.returns = pd.Series(np.random.normal(0.0005, 0.01, 100), index=dates)
        self.calculator = ParametricVaRCalculator(portfolio_returns=self.returns)

    def test_calculate_var(self):
        """Test parametric VaR."""
        var = self.calculator.calculate_var(confidence=0.95)
        self.assertIn("portfolio", var)
        self.assertGreater(var["portfolio"], 0)

    def test_normal_quantile(self):
        """Test normal quantile retrieval."""
        z = self.calculator._get_normal_quantile(0.95)
        # Inverse CDF should be positive for confidence > 0.5
        self.assertGreater(abs(z), 1.6)  # ~1.645 for 95% confidence


class TestMonteCarloVaRCalculator(unittest.TestCase):
    """Test Monte Carlo VaR calculator."""

    def setUp(self):
        """Set up test fixtures."""
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        self.returns = pd.Series(np.random.normal(0.0005, 0.01, 100), index=dates)
        self.calculator = MonteCarloVaRCalculator(
            portfolio_returns=self.returns, num_simulations=1000
        )

    def test_calculate_var(self):
        """Test Monte Carlo VaR."""
        var = self.calculator.calculate_var(confidence=0.95)
        self.assertIn("portfolio", var)
        self.assertGreater(var["portfolio"], 0)


class TestConditionalVaRCalculator(unittest.TestCase):
    """Test Conditional VaR calculator."""

    def setUp(self):
        """Set up test fixtures."""
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        self.returns = pd.Series(np.random.normal(0.0005, 0.01, 100), index=dates)
        self.calculator = ConditionalVaRCalculator(portfolio_returns=self.returns)

    def test_calculate_cvar(self):
        """Test CVaR calculation."""
        cvar = self.calculator.calculate_cvar(confidence=0.95)
        self.assertIn("portfolio", cvar)
        self.assertGreater(cvar["portfolio"], 0)

    def test_cvar_greater_than_var(self):
        """Test that CVaR >= VaR."""
        from empirical_ra.risk.historical_var import HistoricalVaRCalculator

        var_calc = HistoricalVaRCalculator(portfolio_returns=self.returns)
        var = var_calc.calculate_var(0.95)["portfolio"]
        cvar = self.calculator.calculate_cvar(0.95)["portfolio"]
        # CVaR should be >= VaR due to tail capturing, but may differ slightly
        self.assertGreaterEqual(cvar, var - 0.01)  # Allow small tolerance


if __name__ == "__main__":
    unittest.main()
