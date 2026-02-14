"""Tests for Asset class."""

import unittest
from datetime import datetime, timedelta

import pandas as pd

from empirical_ra.core.asset import Asset


class TestAsset(unittest.TestCase):
    """Test Asset functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.asset = Asset(
            name="TEST",
            ticker="AAPL",
            asset_type="stock",
            base_currency="USD",
            target_currency="USD",
            description="Test asset",
        )
        # Create mock price series
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        self.asset.prices = pd.Series(range(100, 200), index=dates, name="TEST")

    def test_asset_creation(self):
        """Test asset initialization."""
        self.assertEqual(self.asset.name, "TEST")
        self.assertEqual(self.asset.ticker, "AAPL")
        self.assertEqual(self.asset.asset_type, "stock")

    def test_asset_prices_loaded(self):
        """Test that prices are loaded."""
        self.assertFalse(self.asset.prices.empty)
        self.assertEqual(len(self.asset.prices), 100)

    def test_calculate_returns(self):
        """Test daily returns calculation."""
        returns = self.asset.calculate_returns("daily")
        self.assertFalse(returns.empty)
        self.assertEqual(len(returns), 99)  # One less due to pct_change

    def test_calculate_returns_monthly(self):
        """Test monthly returns calculation."""
        returns = self.asset.calculate_returns("monthly")
        self.assertGreater(len(returns), 0)

    def test_validate_data_with_valid_data(self):
        """Test data validation with good data."""
        self.assertTrue(self.asset.validate_data())

    def test_validate_data_empty_prices(self):
        """Test validation fails with empty prices."""
        self.asset.prices = pd.Series()
        self.assertFalse(self.asset.validate_data())

    def test_adjust_for_dividends_no_dividends(self):
        """Test dividend adjustment when no dividends exist."""
        adjusted = self.asset.adjust_for_dividends()
        pd.testing.assert_series_equal(adjusted, self.asset.prices, check_names=False)


if __name__ == "__main__":
    unittest.main()
