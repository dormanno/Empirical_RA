"""Main orchestration engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

import pandas as pd

from empirical_ra.core.asset import Asset
from empirical_ra.core.portfolio import Portfolio
from empirical_ra.core.return_analyzer import ReturnAnalyzer
from empirical_ra.core.volatility_analyzer import VolatilityAnalyzer
from empirical_ra.core.correlation_analyzer import CorrelationAnalyzer
from empirical_ra.core.performance_analyzer import PerformanceAnalyzer
from empirical_ra.core.benchmark_analyzer import BenchmarkAnalyzer
from empirical_ra.risk.historical_var import HistoricalVaRCalculator
from empirical_ra.risk.parametric_var import ParametricVaRCalculator
from empirical_ra.risk.monte_carlo_var import MonteCarloVaRCalculator
from empirical_ra.risk.cvar_calc import ConditionalVaRCalculator
from empirical_ra.data.data_manager import DataManager
from empirical_ra.viz.portfolio_visualizer import PortfolioVisualizer
from empirical_ra.viz.regression_visualizer import RegressionVisualizer
from empirical_ra.report.report_generator import ReportGenerator
from empirical_ra.report.essay_report_generator import EssayReportGenerator
from empirical_ra.config.analysis_config import AnalysisConfig


@dataclass
class RiskAssessmentEngine:
    """Main orchestrator for risk assessment."""

    portfolio: Portfolio = field(default_factory=Portfolio)
    data_manager: DataManager = field(default_factory=DataManager)
    return_analyzer: ReturnAnalyzer = field(default_factory=lambda: None)
    volatility_analyzer: VolatilityAnalyzer = field(default_factory=lambda: None)
    correlation_analyzer: CorrelationAnalyzer = field(default_factory=lambda: None)
    historical_var: HistoricalVaRCalculator = field(default_factory=lambda: None)
    parametric_var: ParametricVaRCalculator = field(default_factory=lambda: None)
    monte_carlo_var: MonteCarloVaRCalculator = field(default_factory=lambda: None)
    cvar_calculator: ConditionalVaRCalculator = field(default_factory=lambda: None)
    performance_analyzer: PerformanceAnalyzer = field(default_factory=lambda: None)
    benchmark_analyzer: BenchmarkAnalyzer = field(default_factory=lambda: None)
    visualizer: PortfolioVisualizer = field(default_factory=PortfolioVisualizer)
    regression_visualizer: RegressionVisualizer = field(default_factory=RegressionVisualizer)
    report_generator: ReportGenerator = field(default_factory=ReportGenerator)
    essay_generator: EssayReportGenerator = field(default_factory=EssayReportGenerator)
    config: AnalysisConfig = field(default_factory=lambda: None)
    results: Dict = field(default_factory=dict)

    def initialize(self, config_path: str) -> None:
        """Initialize engine from configuration."""
        self.config = AnalysisConfig(
            start_date="2015-01-01", end_date="2025-01-01", portfolio_assets={}
        )
        self.config.load_from_file(config_path)
        self.config.validate_config()

    def run_full_analysis(self) -> Dict:
        """Execute complete pipeline."""
        self.run_returns_analysis()
        self.run_volatility_analysis()
        self.run_risk_metrics_analysis()
        self.run_benchmark_comparison()
        return self.results

    def run_returns_analysis(self) -> Dict:
        """Return-specific analysis."""
        if self.return_analyzer:
            return_results = self.return_analyzer.calculate()
            self.results["returns"] = return_results
        return self.results.get("returns", {})

    def run_volatility_analysis(self) -> Dict:
        """Volatility-specific analysis."""
        if self.volatility_analyzer:
            vol_results = self.volatility_analyzer.calculate()
            self.results["volatility"] = vol_results
        return self.results.get("volatility", {})

    def run_risk_metrics_analysis(self) -> Dict:
        """VaR and CVaR analysis."""
        risk_results = {}
        if self.historical_var:
            risk_results["historical_var"] = self.historical_var.calculate_var()
        if self.parametric_var:
            risk_results["parametric_var"] = self.parametric_var.calculate_var()
        if self.monte_carlo_var:
            risk_results["monte_carlo_var"] = self.monte_carlo_var.calculate_var()
        if self.cvar_calculator:
            risk_results["cvar"] = self.cvar_calculator.calculate_cvar()
        self.results["risk"] = risk_results
        return risk_results

    def run_benchmark_comparison(self) -> Dict:
        """Benchmark analysis."""
        if self.benchmark_analyzer:
            bench_results = self.benchmark_analyzer.calculate()
            self.results["benchmark"] = bench_results
        if self.performance_analyzer:
            perf_results = self.performance_analyzer.calculate()
            self.results["performance"] = perf_results
        return {**self.results.get("benchmark", {}), **self.results.get("performance", {})}

    def generate_all_visualizations(self) -> None:
        """Create all charts."""
        if not self.portfolio.prices_df.empty:
            self.visualizer.plot_price_timeseries(
                self.portfolio.prices_df, "./output/prices_timeseries.png"
            )
        if not self.portfolio.returns_df.empty:
            self.visualizer.plot_returns_distributions(
                self.portfolio.returns_df, "./output/returns_distribution.png"
            )
            self.visualizer.plot_cumulative_returns(
                self.portfolio.portfolio_returns, "./output/cumulative_returns.png"
            )

    def export_all_results(self, output_dir: str = "./output") -> None:
        """Export results to files."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self.report_generator.output_dir = output_dir
        self.report_generator.compile_results(self.results)
        self.report_generator.save_json_results("results.json")

    def generate_essay_report(self, output_path: str) -> None:
        """Generate PDF essay."""
        self.essay_generator.generate_pdf(output_path)

    def get_summary_statistics(self) -> Dict:
        """Return all summary metrics."""
        return self.results
