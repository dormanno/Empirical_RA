"""Results reporting and export."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


class ReportGenerator:
    """Generate and export analysis results."""

    def __init__(self, output_dir: str = "./output"):
        """Initialize report generator."""
        self.output_dir = output_dir
        self.analysis_results: Dict = {}
        self.visualizations: Dict[str, str] = {}
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def compile_results(self, analyses: Dict) -> None:
        """Aggregate analysis results."""
        self.analysis_results = dict(analyses)

    def export_to_csv(self, data: pd.DataFrame, filename: str) -> None:
        """Export table to CSV."""
        filepath = Path(self.output_dir) / filename
        data.to_csv(filepath)

    def save_figures(self, figures: Dict[str, str]) -> None:
        """Save figure filepaths."""
        self.visualizations = dict(figures)

    def generate_summary_table(self) -> pd.DataFrame:
        """Create summary statistics table."""
        if not self.analysis_results:
            raise ValueError("No results compiled")
        summary_data = []
        for key, val in self.analysis_results.items():
            if isinstance(val, dict):
                summary_data.append({**val, "category": key})
        return pd.DataFrame(summary_data) if summary_data else pd.DataFrame()

    def save_json_results(self, filename: str) -> None:
        """Save results as JSON."""
        import json

        filepath = Path(self.output_dir) / filename
        with filepath.open("w") as f:
            json.dump(self.analysis_results, f, default=str, indent=2)
