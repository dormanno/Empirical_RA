"""Risk-adjusted performance metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd

from empirical_ra.core.analyzer import Analyzer


@dataclass
class PerformanceAnalyzer(Analyzer):
    """Calculate risk-adjusted metrics."""

    portfolio_returns: Optional[pd.Series] = None
    asset_returns_df: Optional[pd.DataFrame] = None
    risk_free_rate: float = 0.0
    benchmark_returns: Optional[pd.Series] = None

    def calculate(self) -> Dict:
        """Execute performance analysis."""
        if self.asset_returns_df is None or self.portfolio_returns is None:
            return {}
        return {
            "sharpe": self.calculate_sharpe_ratio(),
            "sortino": self.calculate_sortino_ratio(),
            "beta": self.calculate_beta(),
            "alpha": self.calculate_alpha(),
            "treynor": self.calculate_treynor_ratio(),
            "information_ratio": self.calculate_information_ratio(),
            "max_drawdown": self.calculate_max_drawdown(),
        }

    def calculate_sharpe_ratio(self) -> Dict[str, float]:
        """Compute Sharpe ratio for assets and portfolio."""
        if self.asset_returns_df is None or self.portfolio_returns is None:
            return {}
        excess = self.asset_returns_df - self.risk_free_rate
        ratios = (excess.mean() / excess.std()).to_dict()
        portfolio_excess = self.portfolio_returns - self.risk_free_rate
        ratios["portfolio"] = portfolio_excess.mean() / portfolio_excess.std()
        return ratios

    def calculate_sortino_ratio(self, min_return: float = 0.0) -> Dict[str, float]:
        """Compute Sortino ratio for assets and portfolio."""
        if self.asset_returns_df is None or self.portfolio_returns is None:
            return {}
        ratios = {}
        for col in self.asset_returns_df.columns:
            diff = np.minimum(self.asset_returns_df[col] - min_return, 0.0)
            downside = np.sqrt((diff ** 2).mean())
            ratios[col] = (self.asset_returns_df[col].mean() - self.risk_free_rate) / downside
        portfolio_diff = np.minimum(self.portfolio_returns - min_return, 0.0)
        portfolio_downside = np.sqrt((portfolio_diff ** 2).mean())
        ratios["portfolio"] = (self.portfolio_returns.mean() - self.risk_free_rate) / portfolio_downside
        return ratios

    def calculate_beta(self) -> Dict[str, float]:
        """Compute beta relative to benchmark."""
        if self.benchmark_returns is None or self.asset_returns_df is None or self.portfolio_returns is None:
            return {"error": "benchmark_returns, asset_returns_df, or portfolio_returns not provided"}
        benchmark = self.benchmark_returns.dropna()
        betas = {}
        for col in self.asset_returns_df.columns:
            aligned = pd.concat([self.asset_returns_df[col], benchmark], axis=1, join="inner")
            cov = aligned.iloc[:, 0].cov(aligned.iloc[:, 1])
            betas[col] = cov / aligned.iloc[:, 1].var()
        aligned_port = pd.concat([self.portfolio_returns, benchmark], axis=1, join="inner")
        cov_port = aligned_port.iloc[:, 0].cov(aligned_port.iloc[:, 1])
        betas["portfolio"] = cov_port / aligned_port.iloc[:, 1].var()
        return betas

    def calculate_alpha(self) -> Dict[str, float]:
        """Compute CAPM alpha relative to benchmark."""
        if self.benchmark_returns is None or self.asset_returns_df is None or self.portfolio_returns is None:
            return {"error": "benchmark_returns, asset_returns_df, or portfolio_returns not provided"}
        betas = self.calculate_beta()
        if "error" in betas:
            return betas
        benchmark_mean = self.benchmark_returns.mean()
        alphas = {}
        for col in self.asset_returns_df.columns:
            alphas[col] = self.asset_returns_df[col].mean() - (
                self.risk_free_rate + betas[col] * (benchmark_mean - self.risk_free_rate)
            )
        alphas["portfolio"] = self.portfolio_returns.mean() - (
            self.risk_free_rate + betas["portfolio"] * (benchmark_mean - self.risk_free_rate)
        )
        return alphas

    def calculate_treynor_ratio(self) -> Dict[str, float]:
        """Compute Treynor ratio relative to benchmark."""
        betas = self.calculate_beta()
        if "error" in betas:
            return betas
        if self.asset_returns_df is None or self.portfolio_returns is None:
            return {}
        ratios = {}
        for col in self.asset_returns_df.columns:
            ratios[col] = (self.asset_returns_df[col].mean() - self.risk_free_rate) / betas[col]
        ratios["portfolio"] = (self.portfolio_returns.mean() - self.risk_free_rate) / betas["portfolio"]
        return ratios

    def calculate_information_ratio(self) -> Dict[str, float]:
        """Compute information ratio relative to benchmark."""
        if self.benchmark_returns is None or self.asset_returns_df is None or self.portfolio_returns is None:
            return {"error": "benchmark_returns, asset_returns_df, or portfolio_returns not provided"}
        benchmark = self.benchmark_returns
        ratios = {}
        for col in self.asset_returns_df.columns:
            active = self.asset_returns_df[col].sub(benchmark, fill_value=0.0)
            ratios[col] = active.mean() / active.std()
        portfolio_active = self.portfolio_returns.sub(benchmark, fill_value=0.0)
        ratios["portfolio"] = portfolio_active.mean() / portfolio_active.std()
        return ratios

    def calculate_max_drawdown(self) -> Dict[str, float]:
        """Compute maximum drawdown for assets and portfolio."""
        if self.asset_returns_df is None or self.portfolio_returns is None:
            return {}
        drawdowns = {}
        for col in self.asset_returns_df.columns:
            series = (1 + self.asset_returns_df[col].fillna(0.0)).cumprod()
            peak = series.cummax()
            drawdowns[col] = ((series - peak) / peak).min()
        port_series = (1 + self.portfolio_returns.fillna(0.0)).cumprod()
        port_peak = port_series.cummax()
        drawdowns["portfolio"] = ((port_series - port_peak) / port_peak).min()
        return drawdowns
