"""Historical simulation VaR."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd

from empirical_ra.risk.var_base import VaRCalculator


@dataclass
class HistoricalVaRCalculator(VaRCalculator):
    """Historical simulation VaR."""

    def calculate_var(self, confidence: float = 0.95) -> Dict[str, float]:
        """Calculate VaR using empirical quantiles."""
        var = {"portfolio": -self._calculate_empirical_quantile(self.portfolio_returns, confidence)}
        if self.asset_returns_df is not None:
            for col in self.asset_returns_df.columns:
                var[col] = -self._calculate_empirical_quantile(self.asset_returns_df[col], confidence)
        return var

    def _calculate_empirical_quantile(self, returns: pd.Series, confidence: float) -> float:
        """Compute empirical quantile."""
        return returns.dropna().quantile(1 - confidence)
