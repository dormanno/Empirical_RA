"""Essay report generation with APA formatting."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

from empirical_ra.report.report_generator import ReportGenerator


class EssayReportGenerator(ReportGenerator):
    """Generate PDF essay reports with analysis results."""

    def __init__(self, output_dir: str = "./output", title: str = "", author: str = ""):
        """Initialize essay report generator."""
        super().__init__(output_dir)
        self.title = title
        self.author = author
        self.analysis_data: Dict = {}
        self.viz_files: Dict = {}

    def generate_data_section(self) -> str:
        """Generate data sources section."""
        if self.analysis_data:
            assets = ", ".join(self.analysis_data.get("assets", []))
            time_period = self.analysis_data.get("time_period", "[Period not specified]")
            portfolio_value = self.analysis_data.get("portfolio_value", "N/A")
            return f"""## Data Section

This analysis uses 10 years of daily historical data from Yahoo Finance:
- Assets analyzed: {assets}

Data currency: USD, converted to PLN base currency.
Portfolio base value: {portfolio_value:,.0f} PLN
Analysis period: {time_period}
Total data points: {self.analysis_data.get("data_points", "N/A")}
"""
        return f"""## Data Section

This analysis uses 10 years of daily historical data from Yahoo Finance:
- Pfizer (PFE) stock prices in USD
- JPY/PLN exchange rates
- Gold spot prices (XAU/USD) in USD

Data currency: USD, converted to PLN base currency.
Portfolio base value: 100,000 PLN
Analysis period: [Start date] to [End date]
"""

    def generate_methodology_section(self) -> str:
        """Generate methodology section."""
        return """## Methodology

This empirical risk assessment employs:
1. **Return Analysis**: Mean, variance, skewness, and kurtosis
2. **Volatility Analysis**: Standard deviation and rolling volatility
3. **Correlation Analysis**: Pearson correlation and covariance matrices
4. **Value at Risk (95% confidence)**:
   - Historical simulation
   - Parametric (variance-covariance)
   - Monte Carlo simulation
5. **Conditional VaR**: Expected shortfall
6. **Performance Metrics**: Sharpe ratio, Sortino ratio, beta, alpha
7. **Benchmark Comparison**: MSCI World index
"""

    def generate_results_section(self) -> str:
        """Generate results section with key findings."""
        section = "## Results\n\nKey performance metrics:\n"
        
        if self.analysis_data:
            # Add return metrics
            if "returns" in self.analysis_data:
                section += "\n### Return Analysis\n"
                returns = self.analysis_data["returns"]
                section += f"- Mean Daily Returns: {returns.get('mean_daily', 'N/A')}\n"
                section += f"- Mean Yearly Returns: {returns.get('mean_yearly', 'N/A')}\n"
            
            # Add volatility metrics
            if "volatility" in self.analysis_data:
                section += "\n### Volatility Analysis\n"
                volatility = self.analysis_data["volatility"]
                section += f"- Daily Volatility: {volatility.get('std_dev_daily', 'N/A')}\n"
                section += f"- Yearly Volatility: {volatility.get('std_dev_yearly', 'N/A')}\n"
            
            # Add performance metrics
            if "performance" in self.analysis_data:
                section += "\n### Performance Metrics\n"
                perf = self.analysis_data["performance"]
                section += f"- Sharpe Ratio: {perf.get('sharpe_ratio', 'N/A')}\n"
                section += f"- Beta: {perf.get('beta', 'N/A')}\n"
                section += f"- Alpha: {perf.get('alpha', 'N/A')}\n"
            
            # Add VaR metrics
            if "var" in self.analysis_data:
                section += "\n### Value at Risk (95% Confidence)\n"
                var = self.analysis_data["var"]
                section += f"- Historical VaR: {var.get('historical_var', 'N/A')}\n"
                section += f"- Parametric VaR: {var.get('parametric_var', 'N/A')}\n"
                section += f"- Monte Carlo VaR: {var.get('monte_carlo_var', 'N/A')}\n"
            
            # Add CVaR metrics
            if "cvar" in self.analysis_data:
                section += "\n### Conditional Value at Risk (95% Confidence)\n"
                cvar = self.analysis_data["cvar"]
                section += f"- Historical CVaR: {cvar.get('historical_cvar', 'N/A')}\n"
                section += f"- Parametric CVaR: {cvar.get('parametric_cvar', 'N/A')}\n"
                section += f"- Monte Carlo CVaR: {cvar.get('monte_carlo_cvar', 'N/A')}\n"
        elif self.analysis_results:
            for key, val in self.analysis_results.items():
                section += f"\n### {key}\n"
                if isinstance(val, dict):
                    for k, v in val.items():
                        section += f"- {k}: {v}\n"
        
        return section

    def generate_discussion_section(self) -> str:
        """Generate interpretation and discussion."""
        return """## Discussion

### Interpretation
This portfolio demonstrates diversification benefits across equity, currency, and commodity exposures.

### Limitations
1. Historical data may not predict future performance
2. Portfolio weights are static (no rebalancing)
3. No hedging applied (unhedged position)
4. Normality assumption may not hold for all assets

### Recommendations
1. Monitor portfolio performance quarterly
2. Consider periodic rebalancing
3. Explore currency hedging strategies
4. Analyze tail risk and stress scenarios
"""

    def generate_pdf(self, output_path: str, analysis_data: Dict = None, viz_files: Dict = None) -> None:
        """Generate PDF report with embedded visualizations."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib.enums import TA_CENTER
        except ImportError:
            raise ImportError("reportlab is required for PDF generation")

        # Store analysis and visualization data
        if analysis_data:
            self.analysis_data = analysis_data
        if viz_files:
            self.viz_files = viz_files

        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom style for centered captions
        caption_style = ParagraphStyle(
            'Caption',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            fontSize=10,
            textColor='#666666'
        )
        
        # Title and metadata
        title = analysis_data.get("portfolio_name", "Portfolio Analysis") if analysis_data else self.title
        story.append(Paragraph(title, styles["Heading1"]))
        story.append(Paragraph(f"By {self.author} | {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))
        
        # Data section
        story.append(Paragraph(self.generate_data_section(), styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add first visualization: Price timeseries
        if "price_timeseries" in self.viz_files:
            story.append(Paragraph("## Price Performance", styles["Heading2"]))
            try:
                img = Image(self.viz_files["price_timeseries"], width=6*inch, height=3.5*inch)
                story.append(img)
                story.append(Paragraph("Portfolio price timeseries rebased to 100", caption_style))
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"[Price chart could not be loaded: {e}]", styles["Normal"]))
        
        # Methodology section
        story.append(Paragraph(self.generate_methodology_section(), styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add second visualization: Returns distribution
        if "returns_distribution" in self.viz_files:
            story.append(Paragraph("## Return Distribution Analysis", styles["Heading2"]))
            try:
                img = Image(self.viz_files["returns_distribution"], width=6*inch, height=3.5*inch)
                story.append(img)
                story.append(Paragraph("Historical return distributions for all assets", caption_style))
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"[Returns distribution chart could not be loaded: {e}]", styles["Normal"]))
        
        # Add third visualization: Correlation heatmap
        if "correlation_heatmap" in self.viz_files:
            story.append(Paragraph("## Correlation Analysis", styles["Heading2"]))
            try:
                img = Image(self.viz_files["correlation_heatmap"], width=5*inch, height=4*inch)
                story.append(img)
                story.append(Paragraph("Asset correlation matrix heatmap", caption_style))
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"[Correlation heatmap could not be loaded: {e}]", styles["Normal"]))
        
        # Page break before risk analysis
        story.append(PageBreak())
        
        # Results section
        story.append(Paragraph(self.generate_results_section(), styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add rolling volatility chart
        if "rolling_volatility" in self.viz_files:
            story.append(Paragraph("## Rolling Volatility", styles["Heading3"]))
            try:
                img = Image(self.viz_files["rolling_volatility"], width=6*inch, height=3.5*inch)
                story.append(img)
                story.append(Paragraph("20-day rolling volatility over time", caption_style))
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"[Rolling volatility chart could not be loaded: {e}]", styles["Normal"]))
        
        # Add VaR visualizations
        if any(f in self.viz_files for f in ["var_timeseries_historical", "var_timeseries_parametric"]):
            story.append(Paragraph("## Value at Risk Analysis", styles["Heading3"]))
            
            # Historical VaR
            if "var_timeseries_historical" in self.viz_files:
                try:
                    story.append(Paragraph("Historical VaR", styles["Heading4"]))
                    img = Image(self.viz_files["var_timeseries_historical"], width=6*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.15 * inch))
                except Exception as e:
                    story.append(Paragraph(f"[Historical VaR chart: {e}]", styles["Normal"]))
            
            # Parametric VaR
            if "var_timeseries_parametric" in self.viz_files:
                try:
                    story.append(Paragraph("Parametric VaR", styles["Heading4"]))
                    img = Image(self.viz_files["var_timeseries_parametric"], width=6*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.15 * inch))
                except Exception as e:
                    story.append(Paragraph(f"[Parametric VaR chart: {e}]", styles["Normal"]))
        
        # Page break before discussion
        story.append(PageBreak())
        
        # Add discussion section
        story.append(Paragraph(self.generate_discussion_section(), styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add CVaR visualization
        if "expected_shortfall_timeseries" in self.viz_files:
            story.append(Paragraph("## Conditional Value at Risk (Expected Shortfall)", styles["Heading3"]))
            try:
                img = Image(self.viz_files["expected_shortfall_timeseries"], width=6*inch, height=3.5*inch)
                story.append(img)
                story.append(Paragraph("Expected Shortfall timeseries", caption_style))
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"[CVaR chart: {e}]", styles["Normal"]))
        
        # Add Beta scatter plot
        if "beta_scatter" in self.viz_files:
            story.append(Paragraph("## Beta Analysis", styles["Heading3"]))
            try:
                img = Image(self.viz_files["beta_scatter"], width=5.5*inch, height=4*inch)
                story.append(img)
                story.append(Paragraph("Portfolio beta vs MSCI World benchmark", caption_style))
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                story.append(Paragraph(f"[Beta scatter plot: {e}]", styles["Normal"]))
        
        # References
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(self.generate_references(), styles["Normal"]))
        
        doc.build(story)

    def generate_references(self) -> str:
        """Generate APA formatted references."""
        return """## References

Jorion, P. (2007). Value at Risk: The New Benchmark for Managing Financial Risk (3rd ed.). McGraw-Hill.

Markowitz, H. (1952). Portfolio Selection. The Journal of Finance, 7(1), 77-91.

Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. 
The Journal of Finance, 19(3), 425-442.
"""
