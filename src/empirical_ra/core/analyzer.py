"""Common analyzer base class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict

import pandas as pd


@dataclass
class Analyzer(ABC):
    """Abstract base class for analyzers."""

    returns_df: pd.DataFrame
    frequency: str = "daily"
    results_cache: Dict = field(default_factory=dict)
    periods_per_year: Dict[str, int] = field(
        default_factory=lambda: {"daily": 252, "monthly": 12, "yearly": 1}
    )

    @abstractmethod
    def calculate(self) -> Dict:
        """Run analyzer calculations."""

    def get_results(self) -> Dict:
        """Return cached results or compute if missing."""
        if not self.results_cache:
            self.results_cache = self.calculate()
        return self.results_cache

    def clear_cache(self) -> None:
        """Clear cached results."""
        self.results_cache = {}

    def _annualize_metric(self, periodic_value: float, frequency: str) -> float:
        """Annualize a periodic metric using linear scaling."""
        periods = self._get_periods_per_year(frequency)
        return periodic_value * periods

    def _get_periods_per_year(self, frequency: str) -> int:
        """Return number of periods per year."""
        self._validate_frequency(frequency)
        return self.periods_per_year[frequency]

    def _validate_frequency(self, frequency: str) -> bool:
        """Validate frequency input."""
        if frequency not in self.periods_per_year:
            raise ValueError("Unsupported frequency")
        return True

    def _prepare_returns_data(self, drop_na: bool = True) -> pd.DataFrame:
        """Prepare returns data for analysis."""
        data = self.returns_df.copy()
        if drop_na:
            data = data.dropna()
        return data
