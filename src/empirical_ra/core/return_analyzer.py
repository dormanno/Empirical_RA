"""Return analysis for assets and portfolio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd

from empirical_ra.core.analyzer import Analyzer


@dataclass
class ReturnAnalyzer(Analyzer):
    """Calculate return statistics."""

    portfolio_returns: Optional[pd.Series] = None
    risk_free_rate: float = 0.0

    def calculate(self) -> Dict:
        """Execute return analysis."""
        mean_returns = self.calculate_mean_returns(self.frequency)
        distribution_stats = self.get_return_distribution_stats()
        return {"mean_returns": mean_returns, "distribution_stats": distribution_stats}

    def calculate_mean_returns(self, frequency: str = "daily") -> Dict[str, float]:
        """Return mean returns for assets and portfolio."""
        self._validate_frequency(frequency)
        returns = self._prepare_returns_data()
        means = returns.mean().to_dict()
        if self.portfolio_returns is not None:
            means["portfolio"] = self.portfolio_returns.mean()
        return means

    def calculate_log_returns(self, prices_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate log returns from prices."""
        return np.log(prices_df / prices_df.shift(1)).dropna()

    def get_return_distribution_stats(self) -> Dict:
        """Return distribution stats (skew, kurtosis, percentiles)."""
        returns = self._prepare_returns_data()
        stats = {}
        for col in returns.columns:
            series = returns[col].dropna()
            stats[col] = {
                "skew": series.skew(),
                "kurtosis": series.kurtosis(),
                "p05": series.quantile(0.05),
                "p50": series.quantile(0.50),
                "p95": series.quantile(0.95),
            }
        return stats
