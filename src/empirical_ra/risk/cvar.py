"""Conditional VaR / Expected Shortfall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd

from empirical_ra.risk.var_base import VaRCalculator
from empirical_ra.risk.historical_var import HistoricalVaRCalculator


@dataclass
class ConditionalVaRCalculator(VaRCalculator):
    """Conditional VaR calculator."""

    var_calculator: Optional[VaRCalculator] = None

    def calculate_cvar(self, confidence: float = 0.95) -> Dict[str, float]:
        """Calculate CVaR for assets and portfolio."""
        var_thresholds = self._get_var_thresholds(confidence)
        cvar = {"portfolio": -self._calculate_mean_below_threshold(self.portfolio_returns, var_thresholds["portfolio"])}
        if self.asset_returns_df is not None:
            for col in self.asset_returns_df.columns:
                cvar[col] = -self._calculate_mean_below_threshold(self.asset_returns_df[col], var_thresholds[col])
        return cvar

    def calculate_var(self, confidence: float = 0.95) -> Dict[str, float]:
        """Alias to calculate CVaR for interface consistency."""
        return self.calculate_cvar(confidence)

    def calculate_cvar_for_horizons(self, horizons) -> Dict:
        """Calculate CVaR across horizons using sqrt-time scaling."""
        base = self.calculate_cvar(self.confidence_level)
        return {h: {k: abs(v) * (h ** 0.5) for k, v in base.items()} for h in horizons}

    def _get_var_thresholds(self, confidence: float) -> Dict[str, float]:
        """Return VaR thresholds using provided or historical calculator."""
        calculator = self.var_calculator or HistoricalVaRCalculator(
            portfolio_returns=self.portfolio_returns,
            asset_returns_df=self.asset_returns_df,
            confidence_level=confidence,
        )
        return calculator.calculate_var(confidence)

    def _calculate_mean_below_threshold(self, returns: pd.Series, threshold: float) -> float:
        """Calculate mean of returns below threshold."""
        below = returns[returns <= -abs(threshold)]
        if below.empty:
            return 0.0
        return below.mean()
