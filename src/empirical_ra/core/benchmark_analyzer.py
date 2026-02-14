"""Benchmark data and analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import pandas as pd

from empirical_ra.core.analyzer import Analyzer


@dataclass
class BenchmarkAnalyzer(Analyzer):
    """Fetch and analyze benchmark data."""

    benchmark_ticker: str = ""
    benchmark_prices: pd.Series = field(default_factory=pd.Series)
    benchmark_returns: pd.Series = field(default_factory=pd.Series)
    start_date: str = ""
    end_date: str = ""

    def calculate(self) -> Dict:
        """Execute benchmark analysis."""
        stats = self.get_benchmark_stats()
        return {"benchmark_stats": stats}

    def fetch_benchmark_data(self, start_date: str, end_date: str) -> None:
        """Fetch benchmark prices from Yahoo Finance."""
        try:
            import yfinance as yf
        except ImportError as exc:
            raise ImportError("yfinance is required to fetch data") from exc

        data = yf.download(self.benchmark_ticker, start=start_date, end=end_date, auto_adjust=True)
        if data.empty:
            raise ValueError(f"No data returned for {self.benchmark_ticker}")
        self.benchmark_prices = data["Close"].rename("benchmark")
        self.benchmark_returns = self.calculate_benchmark_returns()
        self.start_date = start_date
        self.end_date = end_date

    def calculate_benchmark_returns(self) -> pd.Series:
        """Calculate benchmark returns."""
        if self.benchmark_prices.empty:
            raise ValueError("Benchmark prices are not loaded")
        return self.benchmark_prices.pct_change().dropna().rename("benchmark")

    def get_benchmark_stats(self) -> Dict:
        """Return basic stats for benchmark."""
        if self.benchmark_returns.empty:
            raise ValueError("Benchmark returns are not loaded")
        return {
            "mean": self.benchmark_returns.mean(),
            "volatility": self.benchmark_returns.std(),
        }
