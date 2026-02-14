# Clarifying Questions for Empirical Risk Assessment Project

Before proceeding with the implementation of this empirical risk assessment project, the following questions should be clarified:

## 1. Data Sources and Time Period

### 1.1 Historical Data
- **What time period should be analyzed?** 10 years of historical data
- **What is the data frequency?** daily
- **What data sources should be used?**
  - For Pfizer stock prices - Yahoo Finance
  - For JPY/PLN exchange rates - Yahoo Finance
  - For gold prices - Gold Spot (XAU/USD) from Yahoo Finance
- **Should we account for any historical events or crises?** no

### 1.2 Data Quality
- **How should missing data be handled?** fail if data is missed - it is not expected
- **Should data be adjusted for dividends/splits?** Yes
- **What currency conventions should be followed?** USD/PLN for Pfizer, USD/PLN for gold

## 2. Risk Metrics and Methodology

### 2.1 Risk Measures
- **Which risk metrics should be calculated?**
  - Mean return
  - Standard deviation
  - Covariance matrix
  - Correlation matrix
  - Portfolio volatility
  - Value at Risk (95% confidence level)  
  - Conditional VaR /Expected Shortfall (95% confidence level)
  - Sharpe ratio
  - Beta: Sensitivity to market (MSCI World) 
- **What time horizon for risk assessment?** 1 day, 1 month, 1 year (except VaRs)

### 2.2 Statistical Methods
- **What methodology should be used for VaR calculation?**
  - All three:
    - Historical simulation
    - Parametric (variance-covariance) method
    - Monte Carlo simulation  
- **Should returns be assumed to be normally distributed?** yes
- **Should correlations between assets be analyzed?** yes
- **Are there any specific statistical tests required?** no

## 3. Portfolio Specifications

### 3.1 Portfolio Composition
- **Are the portfolio weights fixed?** Yes: 50% Pfizer, 25% JPY, 25% gold
- **What is the initial portfolio value in PLN?** 100000PLN
- **Should rebalancing be considered?** no

### 3.2 Currency Hedging
- No hedging. It only for academical research not for real investment

### 3.3 Asset Clarifications
- **JPY - is this referring to** Japanese Yen currency holdings (cash position)  

## 4. Implementation Requirements (Python & R)

### 4.1 Code Structure
- **Should the Python and R implementations be separate or integrated?**
- **What libraries/packages are preferred or required?**
  - Python: pandas, numpy. Others if requried
  - R: quantmod, PerformanceAnalytics, ggplot2. Others if requried
- **Should there be unit tests?** Yes, in Python
- **What code documentation standard should be followed?** no need, just methods and classes to be providede with commetns

### 4.2 Output Requirements
- **What visualizations are expected?**
  - Time series line chart of portfolio constituents rebased to 100
  - Return Distribution histograms separately for the constituents
  - Correlation heatmap
  - Rolling Volatility line chart
  - VaR: Time series of portfolio returns with VaR breaches highlighted    
  - Sensitivity to MSCI World on Scatter Plot with Regression Line
  - rest of the metrics on most suitable charts

- **Should results be exported?** CSV, and PNG for charts

## 5. Essay/Report Requirements

### 5.1 Structure and Format
- **The essay should be 2-3 pages - is this:** 2-3 pages including figures and tables
- **What citation style?** APA
- **What format?** PDF

### 5.2 Content Requirements
- **Data section - what level of detail?**  
  - Data sources and collection methods only
- **Methodology section - should it include:**    
  - list and justification of chosen methods
- **Results section - what should be presented?**
  - Abovementioned visuals with explanations
  - Analysis results  
- **Discussion section - what aspects should be covered?**
  - Interpretation of results for the investor?
  - Limitations of the analysis?
  - Recommendations?

### 5.3 Academic Requirements
- **Is this for a course assignment?** Empirical Methods of Risk Assessment
- **Are there specific grading rubrics or requirements to follow?** no
- **Should any specific literature or textbooks be referenced?** no

## 7. Additional Considerations

### 7.1 Assumptions
- **Should we assume any risk-free rate for calculations?** Polis Treasury bills
- **Should transaction costs be considered?** no
- **What about taxes on investment returns?** ignore as it is academical research rather than pratical application

### 7.2 Scope
- **Should the analysis include recommendations for portfolio adjustment?** yes
- **Should we compare this portfolio with benchmark indices?** yes, MSCI World
- **Are there any regulatory or compliance considerations?** ignore as it is academical research rather than pratical application

