"""Base class for Value at Risk calculations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd


@dataclass
class VaRCalculator(ABC):
    """Abstract base class for VaR calculations."""

    portfolio_returns: pd.Series
    asset_returns_df: Optional[pd.DataFrame] = None
    confidence_level: float = 0.95

    @abstractmethod
    def calculate_var(self, confidence: float = 0.95) -> Dict[str, float]:
        """Calculate VaR values."""

    def calculate_var_for_horizons(self, horizons: List[int]) -> Dict[int, Dict[str, float]]:
        """Calculate VaR for multiple horizons using sqrt-time scaling."""
        base = self.calculate_var(self.confidence_level)
        scaled = {}
        for horizon in horizons:
            scaled[horizon] = {k: self._scale_var_to_horizon(v, horizon) for k, v in base.items()}
        return scaled

    def calculate_var_breaches(self, var_value: float) -> List[pd.Timestamp]:
        """Identify dates where returns breach VaR."""
        threshold = -abs(var_value)
        breaches = self.portfolio_returns[self.portfolio_returns <= threshold]
        return list(breaches.index)

    def _scale_var_to_horizon(self, single_period_var: float, periods: int) -> float:
        """Scale VaR to the horizon."""
        return abs(single_period_var) * np.sqrt(periods)
