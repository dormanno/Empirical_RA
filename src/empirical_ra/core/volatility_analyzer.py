"""Volatility analysis for assets and portfolio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd

from empirical_ra.core.analyzer import Analyzer


@dataclass
class VolatilityAnalyzer(Analyzer):
    """Calculate volatility measures."""

    portfolio_returns: Optional[pd.Series] = None

    def calculate(self) -> Dict:
        """Execute volatility analysis."""
        std_dev = self.calculate_std_dev(self.frequency)
        variance = self.calculate_variance(self.frequency)
        return {"std_dev": std_dev, "variance": variance}

    def calculate_std_dev(self, frequency: str = "daily") -> Dict[str, float]:
        """Calculate standard deviation by asset and portfolio."""
        self._validate_frequency(frequency)
        returns = self._prepare_returns_data()
        stds = returns.std().to_dict()
        if self.portfolio_returns is not None:
            stds["portfolio"] = self.portfolio_returns.std()
        return stds

    def calculate_variance(self, frequency: str = "daily") -> Dict[str, float]:
        """Calculate variance by asset and portfolio."""
        self._validate_frequency(frequency)
        returns = self._prepare_returns_data()
        vars_ = returns.var().to_dict()
        if self.portfolio_returns is not None:
            vars_["portfolio"] = self.portfolio_returns.var()
        return vars_

    def calculate_rolling_volatility(self, window: int) -> Dict[str, pd.Series]:
        """Calculate rolling volatility per asset and portfolio."""
        returns = self._prepare_returns_data()
        rolling = {col: returns[col].rolling(window).std() for col in returns.columns}
        if self.portfolio_returns is not None:
            rolling["portfolio"] = self.portfolio_returns.rolling(window).std()
        return rolling

    def calculate_downside_deviation(self, min_return: float = 0.0) -> Dict[str, float]:
        """Calculate downside deviation below target."""
        returns = self._prepare_returns_data()
        downside = {}
        for col in returns.columns:
            diff = np.minimum(returns[col] - min_return, 0.0)
            downside[col] = np.sqrt((diff ** 2).mean())
        return downside
