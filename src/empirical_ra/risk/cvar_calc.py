"""Conditional VaR / Expected Shortfall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from empirical_ra.risk.var_base import VaRCalculator


@dataclass
class ConditionalVaRCalculator(VaRCalculator):
    """Conditional VaR (CVaR) / Expected Shortfall."""

    var_calculator: Optional[VaRCalculator] = None

    def calculate_var(self, confidence: float = 0.95) -> Dict[str, float]:
        """Calculate VaR (inherited method, delegates to CVaR logic)."""
        return self.calculate_cvar(confidence)

    def calculate_cvar(self, confidence: float = 0.95) -> Dict[str, float]:
        """Calculate CVaR as mean of returns below VaR threshold."""
        cvar = {}
        threshold = self._get_var_threshold(self.portfolio_returns, confidence)
        cvar["portfolio"] = -self._calculate_mean_below_threshold(self.portfolio_returns, threshold)
        if self.asset_returns_df is not None:
            for col in self.asset_returns_df.columns:
                threshold = self._get_var_threshold(self.asset_returns_df[col], confidence)
                cvar[col] = -self._calculate_mean_below_threshold(self.asset_returns_df[col], threshold)
        return cvar

    def calculate_cvar_for_horizons(self, horizons: List[int]) -> Dict[int, Dict[str, float]]:
        """Calculate CVaR for multiple time horizons."""
        base = self.calculate_cvar(self.confidence_level)
        scaled = {}
        for horizon in horizons:
            scaled[horizon] = {k: self._scale_var_to_horizon(v, horizon) for k, v in base.items()}
        return scaled

    def _get_var_threshold(self, returns: pd.Series, confidence: float) -> float:
        """Get VaR threshold using historical method."""
        return returns.dropna().quantile(1 - confidence)

    def _calculate_mean_below_threshold(self, returns: pd.Series, threshold: float) -> float:
        """Mean of returns below threshold."""
        return returns[returns <= threshold].mean()
