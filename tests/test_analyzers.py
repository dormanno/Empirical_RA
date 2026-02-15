"""Tests for analyzers."""

import unittest

import pandas as pd
import numpy as np

from empirical_ra.core.return_analyzer import ReturnAnalyzer
from empirical_ra.core.volatility_analyzer import VolatilityAnalyzer
from empirical_ra.core.correlation_analyzer import CorrelationAnalyzer


class TestReturnAnalyzer(unittest.TestCase):
    """Test ReturnAnalyzer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        returns = pd.DataFrame(
            {
                "ASSET1": np.random.normal(0.0005, 0.01, 100),
                "ASSET2": np.random.normal(0.0003, 0.015, 100),
            },
            index=dates,
        )
        self.analyzer = ReturnAnalyzer(returns_df=returns)

    def test_calculate_mean_returns(self):
        """Test mean return calculation."""
        means = self.analyzer.calculate_mean_returns("daily")
        self.assertIn("ASSET1", means)
        self.assertIn("ASSET2", means)

    def test_get_return_distribution_stats(self):
        """Test return distribution statistics."""
        stats = self.analyzer.get_return_distribution_stats()
        self.assertIn("ASSET1", stats)
        self.assertIn("skew", stats["ASSET1"])
        self.assertIn("kurtosis", stats["ASSET1"])

    def test_calculate_log_returns(self):
        """Test log returns calculation."""
        prices = pd.DataFrame(
            {"ASSET1": [100, 102, 105], "ASSET2": [50, 51, 52]}, index=pd.date_range("2023-01-01", periods=3, freq="D")
        )
        log_returns = self.analyzer.calculate_log_returns(prices)
        self.assertEqual(len(log_returns), 2)


class TestVolatilityAnalyzer(unittest.TestCase):
    """Test VolatilityAnalyzer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        returns = pd.DataFrame(
            {
                "ASSET1": np.random.normal(0.0005, 0.01, 100),
                "ASSET2": np.random.normal(0.0003, 0.015, 100),
            },
            index=dates,
        )
        self.analyzer = VolatilityAnalyzer(returns_df=returns)

    def test_calculate_std_dev(self):
        """Test standard deviation calculation."""
        stds = self.analyzer.calculate_std_dev("daily")
        self.assertIn("ASSET1", stds)
        self.assertGreater(stds["ASSET1"], 0)

    def test_calculate_variance(self):
        """Test variance calculation."""
        vars_ = self.analyzer.calculate_variance("daily")
        self.assertIn("ASSET1", vars_)
        self.assertGreater(vars_["ASSET1"], 0)

    def test_rolling_volatility(self):
        """Test rolling volatility."""
        rolling = self.analyzer.calculate_rolling_volatility(window=20)
        self.assertIn("ASSET1", rolling)
        self.assertGreater(len(rolling["ASSET1"]), 0)

    def test_downside_deviation(self):
        """Test downside deviation."""
        downside = self.analyzer.calculate_downside_deviation()
        self.assertIn("ASSET1", downside)
        self.assertGreaterEqual(downside["ASSET1"], 0)


class TestCorrelationAnalyzer(unittest.TestCase):
    """Test CorrelationAnalyzer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
        returns = pd.DataFrame(
            {
                "ASSET1": np.random.normal(0.0005, 0.01, 100),
                "ASSET2": np.random.normal(0.0003, 0.015, 100),
            },
            index=dates,
        )
        self.analyzer = CorrelationAnalyzer(returns_df=returns)

    def test_correlation_matrix(self):
        """Test correlation matrix calculation."""
        corr = self.analyzer.calculate_correlation_matrix()
        self.assertEqual(corr.shape, (2, 2))
        self.assertAlmostEqual(corr.loc["ASSET1", "ASSET1"], 1.0)

    def test_covariance_matrix(self):
        """Test covariance matrix calculation."""
        cov = self.analyzer.calculate_covariance_matrix()
        self.assertEqual(cov.shape, (2, 2))

    def test_asset_correlation(self):
        """Test pairwise correlation."""
        corr = self.analyzer.get_asset_correlation("ASSET1", "ASSET2")
        self.assertGreaterEqual(corr, -1.0)
        self.assertLessEqual(corr, 1.0)


if __name__ == "__main__":
    unittest.main()
