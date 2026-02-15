"""Analysis configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import json
import yaml


@dataclass
class AnalysisConfig:
    """Configuration for risk assessment analysis."""

    start_date: str
    end_date: str
    portfolio_assets: Dict[str, float]
    initial_value: float = 100000.0
    base_currency: str = "PLN"
    risk_free_rate: float = 0.01
    confidence_level: float = 0.95
    time_horizons: List[int] = field(default_factory=lambda: [1, 21, 252])
    monte_carlo_simulations: int = 10000
    rolling_window: int = 252
    benchmark_ticker: str = "URTH"

    def load_from_file(self, config_file: str) -> None:
        """Load configuration from JSON or YAML."""
        path = Path(config_file)
        if path.suffix == ".json":
            with path.open() as f:
                cfg = json.load(f)
        elif path.suffix in [".yaml", ".yml"]:
            with path.open() as f:
                cfg = yaml.safe_load(f)
        else:
            raise ValueError("Unsupported config format")
        for key, val in cfg.items():
            if hasattr(self, key):
                setattr(self, key, val)

    def save_to_file(self, config_file: str) -> None:
        """Save configuration to JSON or YAML."""
        path = Path(config_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        cfg = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "portfolio_assets": self.portfolio_assets,
            "initial_value": self.initial_value,
            "base_currency": self.base_currency,
            "risk_free_rate": self.risk_free_rate,
            "confidence_level": self.confidence_level,
            "time_horizons": self.time_horizons,
            "monte_carlo_simulations": self.monte_carlo_simulations,
            "rolling_window": self.rolling_window,
            "benchmark_ticker": self.benchmark_ticker,
        }
        if path.suffix == ".json":
            with path.open("w") as f:
                json.dump(cfg, f, indent=2)
        elif path.suffix in [".yaml", ".yml"]:
            with path.open("w") as f:
                yaml.dump(cfg, f)
        else:
            raise ValueError("Unsupported config format")

    def validate_config(self) -> bool:
        """Validate configuration parameters."""
        if not self.start_date or not self.end_date:
            raise ValueError("start_date and end_date required")
        if not self.portfolio_assets:
            raise ValueError("portfolio_assets required")
        if abs(sum(self.portfolio_assets.values()) - 1.0) > 1e-6:
            raise ValueError("portfolio_assets must sum to 1.0")
        if self.initial_value <= 0:
            raise ValueError("initial_value must be positive")
        if not (0 < self.confidence_level < 1):
            raise ValueError("confidence_level must be between 0 and 1")
        return True

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "portfolio_assets": self.portfolio_assets,
            "initial_value": self.initial_value,
            "base_currency": self.base_currency,
            "risk_free_rate": self.risk_free_rate,
            "confidence_level": self.confidence_level,
            "time_horizons": self.time_horizons,
            "monte_carlo_simulations": self.monte_carlo_simulations,
            "rolling_window": self.rolling_window,
            "benchmark_ticker": self.benchmark_ticker,
        }
