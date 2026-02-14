"""Portfolio composition and aggregation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import pandas as pd

from empirical_ra.core.asset import Asset


@dataclass
class Portfolio:
    """Manage portfolio assets and weights."""

    assets: Dict[str, Asset] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)
    initial_value: float = 0.0
    base_currency: str = "PLN"
    prices_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    returns_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    rebalance_dates: List[pd.Timestamp] = field(default_factory=list)

    def add_asset(self, asset: Asset, weight: float) -> None:
        """Add an asset and its weight."""
        self.assets[asset.name] = asset
        self.weights[asset.name] = weight

    def set_weights(self, weights: Dict[str, float]) -> None:
        """Update portfolio weights with validation."""
        if not weights:
            raise ValueError("Weights cannot be empty")
        total = sum(weights.values())
        if abs(total - 1.0) > 1e-6:
            raise ValueError("Weights must sum to 1.0")
        self.weights = dict(weights)

    def get_portfolio_prices(self) -> pd.Series:
        """Return the weighted portfolio price series."""
        if self.prices_df.empty:
            # Build prices_df from assets if not already set
            if not self.assets:
                raise ValueError("No assets in portfolio")
            prices = {name: asset.prices for name, asset in self.assets.items()}
            self.prices_df = pd.DataFrame(prices).dropna()
        
        if self.prices_df.empty:
            raise ValueError("No price data available")
        
        if not self.weights:
            raise ValueError("Weights are not set")
        
        aligned_weights = pd.Series(self.weights)
        # Select only columns that match the weights
        available_cols = [col for col in self.prices_df.columns if col in aligned_weights.index]
        if not available_cols:
            raise ValueError("No matching assets between prices and weights")
        
        prices_aligned = self.prices_df[available_cols]
        weights_aligned = aligned_weights[available_cols]
        
        # Normalize weights to sum to 1
        weights_aligned = weights_aligned / weights_aligned.sum()
        
        weighted = prices_aligned.mul(weights_aligned, axis=1).sum(axis=1)
        weighted.name = "portfolio"
        return weighted

    def get_portfolio_returns(self, frequency: str = "daily") -> pd.Series:
        """Return portfolio returns at the requested frequency."""
        portfolio_prices = self.get_portfolio_prices()
        if frequency == "daily":
            returns = portfolio_prices.pct_change()
        elif frequency == "monthly":
            returns = portfolio_prices.resample("ME").last().pct_change()
        elif frequency == "yearly":
            returns = portfolio_prices.resample("YE").last().pct_change()
        else:
            raise ValueError("Unsupported frequency")
        return returns.dropna().rename("portfolio")

    def get_weights(self) -> Dict[str, float]:
        """Return current weights."""
        return dict(self.weights)

    def validate_composition(self) -> bool:
        """Ensure weights sum to 1 and assets are present."""
        if not self.assets or not self.weights:
            return False
        return abs(sum(self.weights.values()) - 1.0) <= 1e-6
