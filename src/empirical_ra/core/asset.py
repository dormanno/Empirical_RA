"""Asset data model and helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import pandas as pd


@dataclass
class Asset:
    """Represent a single asset and its price history."""

    name: str
    ticker: str
    asset_type: str
    base_currency: str
    target_currency: str
    description: str = ""
    fx_ticker: Optional[str] = None
    prices: pd.Series = field(default_factory=pd.Series)
    dividends: pd.Series = field(default_factory=pd.Series)

    def fetch_data(self, start_date: str, end_date: str) -> None:
        """Fetch adjusted prices and dividends from Yahoo Finance."""
        try:
            import yfinance as yf
        except ImportError as exc:
            raise ImportError("yfinance is required to fetch data") from exc

        data = yf.download(self.ticker, start=start_date, end=end_date, auto_adjust=True)
        if data.empty:
            raise ValueError(f"No data returned for {self.ticker}")

        # Get Close prices and set the name directly
        self.prices = data["Close"]
        self.prices.name = self.name
        
        if "Dividends" in data.columns:
            self.dividends = data["Dividends"]
            self.dividends.name = self.name

        # Convert currency when a FX ticker is provided.
        if self.fx_ticker:
            fx_data = yf.download(self.fx_ticker, start=start_date, end=end_date, auto_adjust=True)
            if fx_data.empty:
                raise ValueError(f"No FX data returned for {self.fx_ticker}")
            fx_rates = fx_data["Close"]
            fx_rates.name = "fx"
            aligned = pd.concat([self.prices, fx_rates], axis=1, join="inner")
            self.prices = (aligned[self.name] * aligned["fx"])
            self.prices.name = self.name

    def adjust_for_dividends(self) -> pd.Series:
        """Return prices adjusted for dividends if available."""
        if self.prices.empty:
            raise ValueError("Prices are not loaded")
        if self.dividends.empty:
            return self.prices
        adjusted = self.prices + self.dividends.reindex(self.prices.index).fillna(0)
        return adjusted.rename(self.name)

    def calculate_returns(self, frequency: str = "daily") -> pd.Series:
        """Calculate simple returns at the requested frequency."""
        if self.prices.empty:
            raise ValueError("Prices are not loaded")
        series = self.prices
        if frequency == "daily":
            returns = series.pct_change()
        elif frequency == "monthly":
            returns = series.resample("ME").last().pct_change()
        elif frequency == "yearly":
            returns = series.resample("YE").last().pct_change()
        else:
            raise ValueError("Unsupported frequency")
        returns = returns.dropna()
        returns.name = self.name
        return returns

    def validate_data(self) -> bool:
        """Check for missing values or empty series."""
        if self.prices.empty:
            return False
        return not self.prices.isna().any()
