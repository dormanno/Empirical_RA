"""Regression visualization for beta analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


class RegressionVisualizer:
    """Beta and regression visualization."""

    @staticmethod
    def plot_beta_regression(
        asset_returns: pd.Series,
        benchmark_returns: pd.Series,
        asset_name: str,
        save_path: Optional[str] = None,
    ) -> None:
        """Plot scatter with regression line."""
        aligned = pd.concat([asset_returns, benchmark_returns], axis=1, join="inner")
        aligned = aligned.dropna()
        x = aligned.iloc[:, 1].values
        y = aligned.iloc[:, 0].values
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.5, s=20)
        plt.plot(x, intercept + slope * x, "r-", label=f"Beta: {slope:.4f}")
        plt.xlabel("Benchmark Return")
        plt.ylabel(f"{asset_name} Return")
        plt.title(f"{asset_name} Beta Regression")
        plt.legend()
        plt.grid()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_all_betas(
        returns_df: pd.DataFrame,
        benchmark_returns: pd.Series,
        save_path: Optional[str] = None,
    ) -> None:
        """Plot beta regressions for multiple assets."""
        n = len(returns_df.columns)
        cols = min(3, n)
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
        axes = axes.flatten() if n > 1 else [axes]
        for i, col in enumerate(returns_df.columns):
            aligned = pd.concat([returns_df[col], benchmark_returns], axis=1, join="inner")
            aligned = aligned.dropna()
            x = aligned.iloc[:, 1].values
            y = aligned.iloc[:, 0].values
            slope, intercept, _, _, _ = stats.linregress(x, y)
            axes[i].scatter(x, y, alpha=0.5, s=20)
            axes[i].plot(x, intercept + slope * x, "r-", label=f"Beta: {slope:.4f}")
            axes[i].set_xlabel("Benchmark Return")
            axes[i].set_ylabel(f"{col} Return")
            axes[i].set_title(f"{col}")
            axes[i].legend()
            axes[i].grid()
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        plt.tight_layout()
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path)
        plt.close()
