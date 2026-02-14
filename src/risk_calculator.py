"""
Module for calculating portfolio risk metrics.
"""
import numpy as np
import pandas as pd
from scipy import stats


class PortfolioRiskCalculator:
    """Calculates various risk metrics for a portfolio."""
    
    def __init__(self, prices_data, weights, risk_free_rate=0.03):
        """
        Initialize the risk calculator.
        
        Args:
            prices_data: Dictionary of price series for each asset
            weights: Dictionary of portfolio weights for each asset
            risk_free_rate: Annual risk-free rate (default: 3%)
        """
        self.prices_data = prices_data
        self.weights = weights
        self.risk_free_rate = risk_free_rate
        self.returns = None
        self.portfolio_returns = None
    
    def calculate_returns(self):
        """Calculate daily returns for all assets."""
        self.returns = {}
        for asset, prices in self.prices_data.items():
            self.returns[asset] = prices.pct_change().dropna()
        
        # Align all return series to common dates
        returns_df = pd.DataFrame(self.returns)
        returns_df = returns_df.dropna()
        self.returns = {col: returns_df[col] for col in returns_df.columns}
        
        return self.returns
    
    def calculate_portfolio_returns(self):
        """Calculate portfolio returns based on asset weights."""
        if self.returns is None:
            self.calculate_returns()
        
        # Create DataFrame with aligned returns
        returns_df = pd.DataFrame(self.returns)
        
        # Calculate weighted portfolio returns
        weights_array = np.array([self.weights[asset] for asset in returns_df.columns])
        self.portfolio_returns = (returns_df * weights_array).sum(axis=1)
        
        return self.portfolio_returns
    
    def calculate_volatility(self, annualize=True):
        """
        Calculate portfolio volatility (standard deviation).
        
        Args:
            annualize: If True, annualize the volatility (default: True)
            
        Returns:
            Portfolio volatility as a percentage
        """
        if self.portfolio_returns is None:
            self.calculate_portfolio_returns()
        
        volatility = self.portfolio_returns.std()
        
        if annualize:
            # Annualize assuming 252 trading days
            volatility = volatility * np.sqrt(252)
        
        return volatility * 100  # Return as percentage
    
    def calculate_var(self, confidence_level=0.95, method='historical'):
        """
        Calculate Value at Risk (VaR).
        
        Args:
            confidence_level: Confidence level for VaR (default: 95%)
            method: 'historical' or 'parametric' (default: 'historical')
            
        Returns:
            VaR as a percentage
        """
        if self.portfolio_returns is None:
            self.calculate_portfolio_returns()
        
        if method == 'historical':
            # Historical VaR
            var = np.percentile(self.portfolio_returns, (1 - confidence_level) * 100)
        elif method == 'parametric':
            # Parametric VaR (assuming normal distribution)
            mean = self.portfolio_returns.mean()
            std = self.portfolio_returns.std()
            var = stats.norm.ppf(1 - confidence_level, mean, std)
        else:
            raise ValueError("Method must be 'historical' or 'parametric'")
        
        return abs(var) * 100  # Return as percentage (positive value)
    
    def calculate_cvar(self, confidence_level=0.95):
        """
        Calculate Conditional Value at Risk (CVaR) / Expected Shortfall.
        
        Args:
            confidence_level: Confidence level (default: 95%)
            
        Returns:
            CVaR as a percentage
        """
        if self.portfolio_returns is None:
            self.calculate_portfolio_returns()
        
        # Calculate VaR threshold
        var_threshold = np.percentile(self.portfolio_returns, (1 - confidence_level) * 100)
        
        # CVaR is the average of returns below VaR threshold
        cvar = self.portfolio_returns[self.portfolio_returns <= var_threshold].mean()
        
        return abs(cvar) * 100  # Return as percentage (positive value)
    
    def calculate_sharpe_ratio(self, annualize=True):
        """
        Calculate Sharpe Ratio.
        
        Args:
            annualize: If True, annualize the ratio (default: True)
            
        Returns:
            Sharpe Ratio
        """
        if self.portfolio_returns is None:
            self.calculate_portfolio_returns()
        
        mean_return = self.portfolio_returns.mean()
        std_return = self.portfolio_returns.std()
        
        if annualize:
            # Annualize assuming 252 trading days
            mean_return = mean_return * 252
            std_return = std_return * np.sqrt(252)
        
        sharpe = (mean_return - self.risk_free_rate) / std_return
        
        return sharpe
    
    def calculate_max_drawdown(self):
        """
        Calculate maximum drawdown.
        
        Returns:
            Maximum drawdown as a percentage
        """
        if self.portfolio_returns is None:
            self.calculate_portfolio_returns()
        
        # Calculate cumulative returns
        cum_returns = (1 + self.portfolio_returns).cumprod()
        
        # Calculate running maximum
        running_max = cum_returns.expanding().max()
        
        # Calculate drawdown
        drawdown = (cum_returns - running_max) / running_max
        
        max_drawdown = drawdown.min()
        
        return abs(max_drawdown) * 100  # Return as percentage (positive value)
    
    def calculate_all_metrics(self):
        """
        Calculate all risk metrics.
        
        Returns:
            Dictionary with all risk metrics
        """
        metrics = {
            'Annual Volatility (%)': self.calculate_volatility(annualize=True),
            'Value at Risk 95% (%)': self.calculate_var(confidence_level=0.95, method='historical'),
            'Conditional VaR 95% (%)': self.calculate_cvar(confidence_level=0.95),
            'Sharpe Ratio': self.calculate_sharpe_ratio(annualize=True),
            'Maximum Drawdown (%)': self.calculate_max_drawdown(),
            'Mean Daily Return (%)': self.portfolio_returns.mean() * 100,
            'Annual Return (%)': self.portfolio_returns.mean() * 252 * 100,
        }
        
        return metrics
