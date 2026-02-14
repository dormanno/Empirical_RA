"""Check if all required libraries are installed."""

import sys

# Test all core imports
tests = [
    ("pandas", "import pandas"),
    ("numpy", "import numpy"),
    ("scipy", "import scipy"),
    ("matplotlib", "import matplotlib"),
    ("seaborn", "import seaborn"),
    ("yfinance", "import yfinance"),
    ("pyyaml", "import yaml"),
    ("reportlab", "import reportlab"),  # Optional for PDF generation
]

print("=== Library Status ===\n")
missing = []
for name, cmd in tests:
    try:
        exec(cmd)
        print(f"[OK] {name:15} installed")
    except ImportError as e:
        print(f"[MISSING] {name:15} - {e}")
        missing.append(name)

print("\n" + "="*40)
if missing:
    print(f"\nMissing libraries: {', '.join(missing)}")
    print("\nTo install missing libraries, run:")
    print(f"  pip install {' '.join(missing)}")
else:
    print("\n[OK] All required libraries are installed!")

# Test package imports
print("\n=== Package Import Test ===\n")
try:
    from empirical_ra import (
        Asset, Portfolio, ReturnAnalyzer, VolatilityAnalyzer,
        CorrelationAnalyzer, PerformanceAnalyzer, BenchmarkAnalyzer,
        HistoricalVaRCalculator, ParametricVaRCalculator, MonteCarloVaRCalculator,
        ConditionalVaRCalculator, DataManager, PortfolioVisualizer,
        RegressionVisualizer, ReportGenerator, EssayReportGenerator,
        RiskAssessmentEngine, AnalysisConfig
    )
    print("[OK] All 20 core classes imported successfully")
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    sys.exit(1)

print("\n[OK] All checks passed!")
