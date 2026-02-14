"""Monte Carlo VaR."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import numpy as np
import pandas as pd

from empirical_ra.risk.var_base import VaRCalculator


@dataclass
class MonteCarloVaRCalculator(VaRCalculator):
    """Monte Carlo VaR calculator."""

    num_simulations: int = 10000
    mean: float = 0.0
    covariance_matrix: pd.DataFrame = field(default_factory=pd.DataFrame)

    def calculate_var(self, confidence: float = 0.95) -> Dict[str, float]:
        """Calculate VaR from simulated returns."""
        if self.asset_returns_df is None:
            mean = self.portfolio_returns.mean() if self.mean == 0.0 else self.mean
            std = self.portfolio_returns.std()
            sims = np.random.normal(mean, std, self.num_simulations)
            var_value = -np.quantile(sims, 1 - confidence)
            return {"portfolio": var_value}

        returns = self.asset_returns_df.dropna()
        mean_vec = returns.mean().values
        cov = self.covariance_matrix
        if cov.empty:
            cov = returns.cov()
        sims = self._generate_simulated_returns(self.num_simulations, mean_vec, cov.values)
        portfolio_sim = sims.mean(axis=1)
        var_value = -np.quantile(portfolio_sim, 1 - confidence)
        return {"portfolio": var_value}

    def _generate_simulated_returns(
        self, num_paths: int, mean_vec: np.ndarray, cov_matrix: np.ndarray
    ) -> np.ndarray:
        """Generate multivariate normal returns."""
        return np.random.multivariate_normal(mean_vec, cov_matrix, size=num_paths)
