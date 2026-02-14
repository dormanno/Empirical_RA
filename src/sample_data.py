"""
Module for generating sample data when live data is not available.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class SampleDataGenerator:
    """Generates realistic sample financial data for testing and demonstration."""
    
    def __init__(self, start_date=None, end_date=None, seed=42):
        """
        Initialize sample data generator.
        
        Args:
            start_date: Start date for sample data (default: 1 year ago)
            end_date: End date for sample data (default: today)
            seed: Random seed for reproducibility
        """
        np.random.seed(seed)
        self.end_date = end_date or datetime.now()
        self.start_date = start_date or (self.end_date - timedelta(days=365))
        
        # Generate date range (trading days only)
        self.dates = pd.bdate_range(start=self.start_date, end=self.end_date)
    
    def generate_stock_prices(self, initial_price=30.0, mean_return=0.0003, 
                             volatility=0.015):
        """
        Generate stock price series using geometric Brownian motion.
        
        Args:
            initial_price: Starting price
            mean_return: Mean daily return
            volatility: Daily volatility
            
        Returns:
            Series with stock prices
        """
        n_days = len(self.dates)
        returns = np.random.normal(mean_return, volatility, n_days)
        prices = initial_price * np.exp(np.cumsum(returns))
        
        return pd.Series(prices, index=self.dates)
    
    def generate_currency_rates(self, initial_rate=0.02, mean_return=0.0,
                                volatility=0.008):
        """
        Generate currency exchange rate series.
        
        Args:
            initial_rate: Starting exchange rate
            mean_return: Mean daily change
            volatility: Daily volatility
            
        Returns:
            Series with exchange rates
        """
        n_days = len(self.dates)
        returns = np.random.normal(mean_return, volatility, n_days)
        rates = initial_rate * np.exp(np.cumsum(returns))
        
        return pd.Series(rates, index=self.dates)
    
    def generate_commodity_prices(self, initial_price=2000.0, mean_return=0.0002,
                                  volatility=0.012):
        """
        Generate commodity price series.
        
        Args:
            initial_price: Starting price
            mean_return: Mean daily return
            volatility: Daily volatility
            
        Returns:
            Series with commodity prices
        """
        n_days = len(self.dates)
        returns = np.random.normal(mean_return, volatility, n_days)
        prices = initial_price * np.exp(np.cumsum(returns))
        
        return pd.Series(prices, index=self.dates)
    
    def generate_portfolio_data(self):
        """
        Generate sample data for the portfolio:
        - Pfizer stock (PFE)
        - JPY to PLN exchange rate
        - Gold commodity prices
        
        Returns:
            Dictionary with sample data for each asset
        """
        data = {}
        
        # Generate Pfizer stock prices (pharmaceutical company, moderate volatility)
        data['PFE'] = self.generate_stock_prices(
            initial_price=30.0,
            mean_return=0.0003,  # Slight upward trend
            volatility=0.015      # Moderate volatility
        )
        
        # Generate JPY/PLN exchange rate (currency pair, lower volatility)
        data['JPY'] = self.generate_currency_rates(
            initial_rate=0.027,   # Approximate JPY to PLN rate
            mean_return=0.0,      # No trend (mean-reverting)
            volatility=0.008      # Lower volatility for currency
        )
        
        # Generate Gold prices (safe haven asset, moderate volatility)
        data['GOLD'] = self.generate_commodity_prices(
            initial_price=2000.0,
            mean_return=0.0002,   # Slight upward trend
            volatility=0.012      # Moderate volatility
        )
        
        return data
