"""Setup configuration for empirical_ra package."""

from setuptools import setup, find_packages

setup(
    name="empirical_ra",
    version="0.1.0",
    description="Empirical Risk Assessment for Portfolio Analysis",
    author="Risk Assessment Team",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "yfinance>=0.1.70",
        "pyyaml>=5.4.0",
        "reportlab>=4.0.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov>=2.12.0"],
    },
)
