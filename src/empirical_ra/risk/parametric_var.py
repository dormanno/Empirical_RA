"""Parametric (variance-covariance) VaR."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import NormalDist
from typing import Dict

import pandas as pd

from empirical_ra.risk.var_base import VaRCalculator


@dataclass
class ParametricVaRCalculator(VaRCalculator):
    """Parametric VaR assuming normality."""

    mean: float = 0.0
    std: float = 0.0

    def calculate_var(self, confidence: float = 0.95) -> Dict[str, float]:
        """Calculate VaR using normal quantiles."""
        z = self._get_normal_quantile(confidence)
        mean = self.portfolio_returns.mean() if self.mean == 0.0 else self.mean
        std = self.portfolio_returns.std() if self.std == 0.0 else self.std
        var = {"portfolio": -(mean + z * std)}
        if self.asset_returns_df is not None:
            for col in self.asset_returns_df.columns:
                a_mean = self.asset_returns_df[col].mean()
                a_std = self.asset_returns_df[col].std()
                var[col] = -(a_mean + z * a_std)
        return var

    def _get_normal_quantile(self, confidence: float) -> float:
        """Return standard normal quantile."""
        return NormalDist().inv_cdf(1 - confidence)
