"""Tests for data management and configuration."""

import unittest
import tempfile
from pathlib import Path

import pandas as pd

from empirical_ra.data.data_manager import DataManager
from empirical_ra.config.analysis_config import AnalysisConfig
from empirical_ra.core.asset import Asset


class TestDataManager(unittest.TestCase):
    """Test DataManager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_manager = DataManager(data_dir=self.temp_dir.name)

    def tearDown(self):
        """Clean up temp directory."""
        self.temp_dir.cleanup()

    def test_data_manager_creation(self):
        """Test DataManager initialization."""
        self.assertEqual(self.data_manager.data_dir, self.temp_dir.name)
        self.assertEqual(len(self.data_manager.assets), 0)

    def test_validate_data_integrity_empty(self):
        """Test integrity check with no assets."""
        self.assertFalse(self.data_manager.validate_data_integrity())

    def test_handle_missing_data_fail_strategy(self):
        """Test fail strategy with missing data."""
        asset = Asset("TEST", "TEST_TICK", "stock", "USD", "USD")
        asset.prices = pd.Series([100, 200, None])
        self.data_manager.assets["TEST"] = asset
        with self.assertRaises(ValueError):
            self.data_manager.handle_missing_data(strategy="fail")


class TestAnalysisConfig(unittest.TestCase):
    """Test AnalysisConfig functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = AnalysisConfig(
            start_date="2020-01-01",
            end_date="2025-01-01",
            portfolio_assets={"PFE": 0.5, "JPY": 0.25, "GOLD": 0.25},
        )

    def test_config_creation(self):
        """Test config initialization."""
        self.assertEqual(self.config.start_date, "2020-01-01")
        self.assertEqual(self.config.initial_value, 100000.0)

    def test_validate_config_valid(self):
        """Test config validation passes."""
        self.assertTrue(self.config.validate_config())

    def test_validate_config_invalid_weights(self):
        """Test validation fails with invalid weights."""
        self.config.portfolio_assets = {"PFE": 0.5, "JPY": 0.25}
        with self.assertRaises(ValueError):
            self.config.validate_config()

    def test_to_dict(self):
        """Test conversion to dictionary."""
        cfg_dict = self.config.to_dict()
        self.assertIn("start_date", cfg_dict)
        self.assertIn("portfolio_assets", cfg_dict)

    def test_save_and_load_json(self):
        """Test saving and loading from JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "config.json"
            self.config.save_to_file(str(filepath))
            self.assertTrue(filepath.exists())
            new_config = AnalysisConfig(
                start_date="", end_date="", portfolio_assets={}
            )
            new_config.load_from_file(str(filepath))
            self.assertEqual(new_config.start_date, "2020-01-01")


if __name__ == "__main__":
    unittest.main()
