# Clarifying Questions for Empirical Risk Assessment Project

Before proceeding with the implementation of this empirical risk assessment project, the following questions should be clarified:

## 1. Data Sources and Time Period

### 1.1 Historical Data
- **What time period should be analyzed?** (e.g., 1 year, 5 years, 10 years of historical data?)
- **What is the data frequency?** (daily, weekly, monthly prices?)
- **What data sources should be used?**
  - For Pfizer stock prices? (e.g., Yahoo Finance, Bloomberg, other?)
  - For JPY/PLN exchange rates? (e.g., NBP, ECB, other central banks?)
  - For gold prices? (e.g., London Bullion Market, in USD or PLN?)
- **Should we account for any historical events or crises?** (e.g., COVID-19, financial crisis?)

### 1.2 Data Quality
- **How should missing data be handled?** (interpolation, forward-fill, exclusion?)
- **Should data be adjusted for dividends/splits?** (for Pfizer shares)
- **What currency conventions should be followed?** (USD/PLN for Pfizer, USD/PLN for gold?)

## 2. Risk Metrics and Methodology

### 2.1 Risk Measures
- **Which risk metrics should be calculated?**
  - Value at Risk (VaR)? If yes, at what confidence level? (e.g., 95%, 99%)
  - Conditional VaR (CVaR/Expected Shortfall)?
  - Standard deviation/variance?
  - Maximum drawdown?
  - Sharpe ratio or other risk-adjusted returns?
- **What time horizon for risk assessment?** (1-day, 10-day, 1-month?)

### 2.2 Statistical Methods
- **What methodology should be used for VaR calculation?**
  - Historical simulation?
  - Parametric (variance-covariance) method?
  - Monte Carlo simulation?
  - All of the above for comparison?
- **Should returns be assumed to be normally distributed?**
- **Should correlations between assets be analyzed?**
- **Are there any specific statistical tests required?** (normality tests, stationarity tests?)

## 3. Portfolio Specifications

### 3.1 Portfolio Composition
- **Are the portfolio weights fixed?** (50% Pfizer, 25% JPY, 25% gold)
- **What is the initial portfolio value in PLN?** (for absolute risk calculations)
- **Should rebalancing be considered?** If yes, how often?

### 3.2 Currency Hedging
- **The portfolio is stated as "unhedged" - should we discuss hedging alternatives?**
- **Should we show comparison with hedged scenarios?**
- **How should currency risk be isolated from asset price risk?**

### 3.3 Asset Clarifications
- **JPY - is this referring to:**
  - Japanese Yen currency holdings (cash position)?
  - Japanese Yen bonds?
  - ETF tracking JPY?
  - Clarification needed on the exact financial instrument

## 4. Implementation Requirements (Python & R)

### 4.1 Code Structure
- **Should the Python and R implementations be separate or integrated?**
- **What libraries/packages are preferred or required?**
  - Python: pandas, numpy, scipy, matplotlib? Others?
  - R: quantmod, PerformanceAnalytics, ggplot2? Others?
- **Should there be unit tests?**
- **What code documentation standard should be followed?**

### 4.2 Output Requirements
- **What visualizations are expected?**
  - Time series plots?
  - Distribution plots?
  - Risk metric charts?
  - Correlation matrices?
- **Should results be exported?** (CSV, Excel, PDF?)
- **Should the code be reproducible?** (seed values, version control?)

## 5. Essay/Report Requirements

### 5.1 Structure and Format
- **The essay should be 2-3 pages - is this:**
  - 2-3 pages of text only?
  - 2-3 pages including figures and tables?
- **What citation style?** (APA, Chicago, IEEE?)
- **What format?** (PDF, Word, LaTeX?)

### 5.2 Content Requirements
- **Data section - what level of detail?**
  - Descriptive statistics?
  - Data sources and collection methods?
- **Methodology section - should it include:**
  - Theoretical background?
  - Mathematical formulas?
  - Justification of chosen methods?
- **Results section - what should be presented?**
  - All calculated risk metrics?
  - Comparison between methods?
  - Sensitivity analysis?
- **Discussion section - what aspects should be covered?**
  - Interpretation of results for the investor?
  - Limitations of the analysis?
  - Recommendations?

### 5.3 Academic Requirements
- **Is this for a course assignment?** If yes, which course?
- **Are there specific grading rubrics or requirements to follow?**
- **Should any specific literature or textbooks be referenced?**

## 6. Timeline and Deliverables

- **What is the deadline for this project?**
- **Should code, essay, and data be submitted separately or together?**
- **Are there any intermediate checkpoints or reviews?**
- **What is the expected folder structure for deliverables?**

## 7. Additional Considerations

### 7.1 Assumptions
- **Should we assume any risk-free rate for calculations?** (Polish government bonds?)
- **Should transaction costs be considered?**
- **What about taxes on investment returns?** (relevant for Polish investor)

### 7.2 Scope
- **Should the analysis include recommendations for portfolio adjustment?**
- **Should we compare this portfolio with benchmark indices?** (WIG20, S&P500, etc.)
- **Are there any regulatory or compliance considerations?** (Polish financial regulations)

---

*Please address these questions before starting the implementation to ensure the project meets all requirements and expectations.*
