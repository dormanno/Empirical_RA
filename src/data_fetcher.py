"""
Module for fetching historical financial data for portfolio assets.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class DataFetcher:
    """Fetches historical price data for various asset types."""
    
    def __init__(self, start_date=None, end_date=None):
        """
        Initialize DataFetcher.
        
        Args:
            start_date: Start date for historical data (default: 1 year ago)
            end_date: End date for historical data (default: today)
        """
        self.end_date = end_date or datetime.now()
        self.start_date = start_date or (self.end_date - timedelta(days=365))
    
    def fetch_stock_data(self, ticker):
        """
        Fetch stock price data.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PFE' for Pfizer)
            
        Returns:
            DataFrame with adjusted close prices
        """
        stock = yf.Ticker(ticker)
        data = stock.history(start=self.start_date, end=self.end_date)
        return data['Close']
    
    def fetch_currency_data(self, from_currency, to_currency):
        """
        Fetch currency exchange rate data.
        
        Args:
            from_currency: Source currency code (e.g., 'JPY')
            to_currency: Target currency code (e.g., 'PLN')
            
        Returns:
            DataFrame with exchange rates
        """
        # Yahoo Finance uses format: JPYPLN=X
        ticker = f"{from_currency}{to_currency}=X"
        currency = yf.Ticker(ticker)
        data = currency.history(start=self.start_date, end=self.end_date)
        return data['Close']
    
    def fetch_commodity_data(self, commodity_ticker):
        """
        Fetch commodity price data.
        
        Args:
            commodity_ticker: Commodity ticker (e.g., 'GC=F' for Gold)
            
        Returns:
            DataFrame with commodity prices
        """
        commodity = yf.Ticker(commodity_ticker)
        data = commodity.history(start=self.start_date, end=self.end_date)
        return data['Close']
    
    def fetch_all_portfolio_data(self):
        """
        Fetch data for the specific portfolio:
        - Pfizer stock (PFE)
        - JPY currency (JPY to PLN)
        - Gold commodity (GC=F)
        
        Returns:
            Dictionary with DataFrames for each asset
        """
        data = {}
        
        # Fetch Pfizer stock data
        print("Fetching Pfizer (PFE) stock data...")
        data['PFE'] = self.fetch_stock_data('PFE')
        
        # Fetch JPY to PLN exchange rate
        print("Fetching JPY/PLN exchange rate...")
        data['JPY'] = self.fetch_currency_data('JPY', 'PLN')
        
        # Fetch Gold futures data
        print("Fetching Gold (GC=F) data...")
        data['GOLD'] = self.fetch_commodity_data('GC=F')
        
        return data
