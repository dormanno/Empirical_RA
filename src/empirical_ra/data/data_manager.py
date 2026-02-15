"""Data management and caching."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from empirical_ra.core.asset import Asset


@dataclass
class DataManager:
    """Centralized data handling."""

    data_dir: str = "./data"
    assets: Dict[str, Asset] = field(default_factory=dict)
    cache: Dict = field(default_factory=dict)

    def fetch_and_store_data(self, assets: Dict[str, Asset], start_date: str, end_date: str) -> None:
        """Fetch and cache asset data."""
        Path(self.data_dir).mkdir(exist_ok=True)
        for name, asset in assets.items():
            asset.fetch_data(start_date, end_date)
            self.assets[name] = asset
            csv_path = Path(self.data_dir) / f"{name}.csv"
            asset.prices.to_csv(csv_path)

    def load_data(self, asset: str) -> pd.DataFrame:
        """Load data from cache or disk."""
        if asset in self.cache:
            return self.cache[asset]
        csv_path = Path(self.data_dir) / f"{asset}.csv"
        if csv_path.exists():
            data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            self.cache[asset] = data
            return data
        raise FileNotFoundError(f"No data for {asset}")

    def export_data(self, asset: str, filepath: str) -> None:
        """Export data to CSV."""
        if asset in self.assets:
            self.assets[asset].prices.to_csv(filepath)
        else:
            raise KeyError(f"Asset {asset} not found")

    def validate_data_integrity(self) -> bool:
        """Check for consistency."""
        if not self.assets:
            return False
        lengths = {name: len(asset.prices) for name, asset in self.assets.items()}
        return len(set(lengths.values())) == 1

    def handle_missing_data(self, strategy: str = "fail") -> None:
        """Handle missing data per strategy."""
        if strategy == "fail":
            for name, asset in self.assets.items():
                if not asset.validate_data():
                    raise ValueError(f"Missing data in {name}")
        elif strategy == "drop":
            for asset in self.assets.values():
                asset.prices = asset.prices.dropna()
        elif strategy == "forward_fill":
            for asset in self.assets.values():
                asset.prices = asset.prices.fillna(method="ffill")
