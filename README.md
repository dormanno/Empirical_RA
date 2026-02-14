# Empirical_RA
Project on Empirical methods of Risk Assessment at UEK

## Overview

This project implements empirical methods for investment risk assessment. It calculates various risk metrics for a multi-asset portfolio consisting of stocks, currencies, and commodities.

## Investment Portfolio

The current implementation assesses the risk of the following investment portfolio:
- **Pfizer (PFE) Stock**: 50% allocation
- **Japanese Yen (JPY)**: 25% allocation
- **Gold**: 25% allocation
- **Base Currency**: Polish Złoty (PLN)

## Risk Metrics Calculated

The system calculates the following risk metrics:
1. **Annual Volatility**: Standard deviation of returns (annualized)
2. **Value at Risk (VaR) at 95%**: Maximum expected loss with 95% confidence
3. **Conditional VaR (CVaR)**: Expected loss beyond the VaR threshold
4. **Sharpe Ratio**: Risk-adjusted return measure
5. **Maximum Drawdown**: Largest peak-to-trough decline
6. **Mean Daily Return**: Average daily portfolio return
7. **Annual Return**: Annualized portfolio return

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/dormanno/Empirical_RA.git
cd Empirical_RA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Using Sample Data (Default)

Run the risk assessment with synthetic sample data:
```bash
python main.py
```

This mode generates realistic sample data for demonstration purposes, which is useful for:
- Testing the implementation
- Understanding the output format
- Running without internet access

### Using Live Data

To fetch real historical data from Yahoo Finance:
```bash
python main.py --live
```

**Note**: This requires internet access and will fetch the last year of historical data for all portfolio assets.

## Project Structure

```
Empirical_RA/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── data_fetcher.py      # Module for fetching live financial data
│   ├── sample_data.py       # Module for generating sample data
│   └── risk_calculator.py   # Module for calculating risk metrics
├── main.py                  # Main script to run the analysis
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **yfinance**: Yahoo Finance data fetching
- **scipy**: Statistical functions
- **matplotlib**: Plotting (for future visualization features)

## Example Output

```
======================================================================
Investment Risk Assessment - Empirical Methods
======================================================================

Portfolio Composition:
  - Pfizer (PFE): 50%
  - Japanese Yen (JPY): 25%
  - Gold: 25%
  - Base Currency: Polish Złoty (PLN)

======================================================================

RISK ASSESSMENT RESULTS
======================================================================

Annual Volatility (%)................................ 12.67
Value at Risk 95% (%)................................ 1.38
Conditional VaR 95% (%).............................. 1.62
Sharpe Ratio......................................... 0.1534
Maximum Drawdown (%).................................. 11.00
Mean Daily Return (%)................................. 0.02
Annual Return (%)..................................... 4.94

======================================================================

INTERPRETATION:

1. Volatility: The portfolio has an annual volatility of 12.67%.
   This indicates LOW risk.

2. Value at Risk (95%): With 95% confidence, the maximum expected
   daily loss is 1.38% of the portfolio value.

3. Sharpe Ratio: 0.1534
   SUBOPTIMAL: Risk-adjusted returns are below average.
```

## Methodology

### Data Collection
- Stock data: Retrieved from Yahoo Finance using yfinance library
- Currency data: Exchange rates from Yahoo Finance (JPY/PLN pair)
- Commodity data: Gold futures prices from Yahoo Finance

### Risk Calculation
- **Returns**: Calculated as percentage changes in asset prices
- **Portfolio Returns**: Weighted sum of individual asset returns
- **Volatility**: Standard deviation of returns, annualized using √252 factor
- **VaR**: Historical simulation method using quantile analysis
- **CVaR**: Average of returns below the VaR threshold
- **Sharpe Ratio**: (Annual Return - Risk-Free Rate) / Annual Volatility

## Customization

To analyze a different portfolio, modify the `weights` dictionary in `main.py`:

```python
weights = {
    'ASSET1': 0.40,  # 40% allocation
    'ASSET2': 0.35,  # 35% allocation
    'ASSET3': 0.25,  # 25% allocation
}
```

You can also modify the data fetcher to include different assets by updating the `fetch_all_portfolio_data()` method in `src/data_fetcher.py`.

## License

This project is for educational purposes as part of the Empirical Risk Assessment course at UEK.

