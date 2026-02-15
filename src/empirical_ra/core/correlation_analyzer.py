"""Correlation and covariance analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd

from empirical_ra.core.analyzer import Analyzer


@dataclass
class CorrelationAnalyzer(Analyzer):
    """Analyze correlations between assets."""

    def calculate(self) -> Dict:
        """Execute correlation analysis."""
        corr = self.calculate_correlation_matrix()
        cov = self.calculate_covariance_matrix()
        return {"correlation": corr, "covariance": cov}

    def calculate_correlation_matrix(self) -> pd.DataFrame:
        """Return correlation matrix."""
        returns = self._prepare_returns_data()
        return returns.corr()

    def calculate_covariance_matrix(self) -> pd.DataFrame:
        """Return covariance matrix."""
        returns = self._prepare_returns_data()
        return returns.cov()

    def get_asset_correlation(self, asset1: str, asset2: str) -> float:
        """Return pairwise correlation."""
        corr = self.calculate_correlation_matrix()
        return float(corr.loc[asset1, asset2])

    def calculate_portmanteau_test(self) -> Dict:
        """Run Ljung-Box test if statsmodels is available."""
        returns = self._prepare_returns_data()
        try:
            from statsmodels.stats.diagnostic import acorr_ljungbox
        except ImportError:
            return {"error": "statsmodels is required for Ljung-Box test"}
        results = {}
        for col in returns.columns:
            lb = acorr_ljungbox(returns[col].dropna(), lags=[10], return_df=True)
            results[col] = lb.iloc[0].to_dict()
        return results
