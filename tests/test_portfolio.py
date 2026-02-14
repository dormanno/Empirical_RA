"""Tests for Portfolio class."""

import unittest

import numpy as np
import pandas as pd

from empirical_ra.core.asset import Asset
from empirical_ra.core.portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    """Test Portfolio functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.portfolio = Portfolio(initial_value=100000.0)
        # Create mock assets
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        for i, name in enumerate(["ASSET1", "ASSET2", "ASSET3"]):
            asset = Asset(
                name=name,
                ticker=f"{name}_TICKER",
                asset_type="stock",
                base_currency="USD",
                target_currency="USD",
            )
            asset.prices = pd.Series(100 * (1.001 ** (i + np.arange(100))), index=dates, name=name)
            self.portfolio.add_asset(asset, 1.0 / 3)

    def test_portfolio_creation(self):
        """Test portfolio initialization."""
        self.assertEqual(len(self.portfolio.assets), 3)
        self.assertEqual(self.portfolio.initial_value, 100000.0)

    def test_add_asset(self):
        """Test adding assets."""
        self.assertEqual(len(self.portfolio.assets), 3)
        new_asset = Asset("NEW", "NEW_TICKER", "stock", "USD", "USD")
        self.portfolio.add_asset(new_asset, 0.1)
        self.assertEqual(len(self.portfolio.assets), 4)

    def test_set_weights_valid(self):
        """Test setting valid weights."""
        weights = {"ASSET1": 0.5, "ASSET2": 0.3, "ASSET3": 0.2}
        self.portfolio.set_weights(weights)
        self.assertEqual(self.portfolio.weights, weights)

    def test_set_weights_invalid_sum(self):
        """Test that invalid weights raise error."""
        weights = {"ASSET1": 0.5, "ASSET2": 0.3}
        with self.assertRaises(ValueError):
            self.portfolio.set_weights(weights)

    def test_get_weights(self):
        """Test retrieving weights."""
        weights = self.portfolio.get_weights()
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=5)

    def test_validate_composition_valid(self):
        """Test validation of portfolio composition."""
        self.assertTrue(self.portfolio.validate_composition())

    def test_validate_composition_empty(self):
        """Test validation fails with no assets."""
        empty_portfolio = Portfolio()
        self.assertFalse(empty_portfolio.validate_composition())

    def test_get_portfolio_prices(self):
        """Test portfolio price calculation."""
        prices = self.portfolio.get_portfolio_prices()
        self.assertEqual(len(prices), 100)
        self.assertGreater(prices.iloc[0], 0)

    def test_get_portfolio_returns(self):
        """Test portfolio returns calculation."""
        returns = self.portfolio.get_portfolio_returns("daily")
        self.assertGreater(len(returns), 0)
        self.assertLess(len(returns), 100)


if __name__ == "__main__":
    unittest.main()
