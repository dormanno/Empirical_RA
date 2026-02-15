"""Portfolio visualization."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class PortfolioVisualizer:
    """Portfolio visualization utilities."""

    @staticmethod
    def plot_price_timeseries(
        prices_df: pd.DataFrame, save_path: Optional[str] = None
    ) -> None:
        """Plot rebased price time series."""
        rebased = prices_df.div(prices_df.iloc[0]) * 100
        plt.figure(figsize=(12, 6))
        for col in rebased.columns:
            plt.plot(rebased.index, rebased[col], label=col)
        plt.xlabel("Date")
        plt.ylabel("Price (rebased to 100)")
        plt.title("Asset Price Time Series")
        plt.legend()
        plt.grid()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_returns_distributions(
        returns_df: pd.DataFrame, save_path: Optional[str] = None
    ) -> None:
        """Plot return distribution histograms."""
        fig, axes = plt.subplots(1, len(returns_df.columns), figsize=(15, 5))
        if len(returns_df.columns) == 1:
            axes = [axes]
        for ax, col in zip(axes, returns_df.columns):
            ax.hist(returns_df[col].dropna(), bins=50, edgecolor="black")
            ax.set_title(col)
            ax.set_xlabel("Return")
            ax.set_ylabel("Frequency")
        plt.tight_layout()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_correlation_heatmap(corr_matrix: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """Plot correlation heatmap."""
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, vmin=-1, vmax=1)
        plt.title("Correlation Matrix")
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_rolling_volatility(
        rolling_vol: Dict[str, pd.Series], save_path: Optional[str] = None
    ) -> None:
        """Plot rolling volatility."""
        plt.figure(figsize=(12, 6))
        for asset, vol_series in rolling_vol.items():
            plt.plot(vol_series.index, vol_series, label=asset)
        plt.xlabel("Date")
        plt.ylabel("Rolling Volatility")
        plt.title("Rolling Standard Deviation")
        plt.legend()
        plt.grid()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_cumulative_returns(
        portfolio_returns: pd.Series, save_path: Optional[str] = None
    ) -> None:
        """Plot cumulative returns."""
        cumsum = (1 + portfolio_returns.fillna(0.0)).cumprod()
        plt.figure(figsize=(12, 6))
        plt.plot(cumsum.index, cumsum.values)
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.title("Portfolio Cumulative Returns")
        plt.grid()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_drawdown(portfolio_returns: pd.Series, save_path: Optional[str] = None) -> None:
        """Plot drawdown."""
        cumsum = (1 + portfolio_returns.fillna(0.0)).cumprod()
        peak = cumsum.cummax()
        drawdown = (cumsum - peak) / peak
        plt.figure(figsize=(12, 6))
        plt.fill_between(drawdown.index, drawdown.values, alpha=0.3)
        plt.plot(drawdown.index, drawdown.values)
        plt.xlabel("Date")
        plt.ylabel("Drawdown")
        plt.title("Portfolio Drawdown")
        plt.grid()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_var_timeseries(
        returns: pd.Series, var_value: float, save_path: Optional[str] = None
    ) -> None:
        """Plot returns time series with VaR breaches highlighted."""
        threshold = -abs(var_value)
        clean_returns = returns.dropna()
        breaches = clean_returns[clean_returns <= threshold]
        breach_ratio = (clean_returns < threshold).mean()
        plt.figure(figsize=(12, 6))
        plt.plot(returns.index, returns.values, label="Returns")
        plt.axhline(threshold, color="red", linestyle="--", label=f"VaR ({threshold:.4f})")
        plt.scatter(breaches.index, breaches.values, color="red", marker="x", s=100, label="Breaches")
        plt.text(
            0.01,
            0.98,
            f"Breach ratio: {breach_ratio:.2%}",
            transform=plt.gca().transAxes,
            va="top",
            ha="left",
        )
        plt.xlabel("Date")
        plt.ylabel("Return")
        plt.title("Portfolio Returns with VaR")
        plt.legend()
        plt.grid()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_cvar_timeseries(
        returns: pd.Series, cvar_value: float, save_path: Optional[str] = None
    ) -> None:
        """Plot returns time series with Expected Shortfall threshold highlighted."""
        threshold = -abs(cvar_value)
        clean_returns = returns.dropna()
        tail = clean_returns[clean_returns <= threshold]
        tail_ratio = (clean_returns < threshold).mean()
        plt.figure(figsize=(12, 6))
        plt.plot(returns.index, returns.values, label="Returns")
        plt.axhline(threshold, color="orange", linestyle="--", label=f"ES ({threshold:.4f})")
        plt.scatter(tail.index, tail.values, color="orange", marker="x", s=100, label="Tail Events")
        plt.text(
            0.01,
            0.98,
            f"Tail ratio: {tail_ratio:.2%}",
            transform=plt.gca().transAxes,
            va="top",
            ha="left",
        )
        plt.xlabel("Date")
        plt.ylabel("Return")
        plt.title("Portfolio Returns with Expected Shortfall")
        plt.legend()
        plt.grid()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()
