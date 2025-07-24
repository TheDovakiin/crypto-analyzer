"""
Cryptocurrency Data Scraper
Fetches cryptocurrency data from various sources
"""

import requests
import pandas as pd
import yfinance as yf
import ccxt
from datetime import datetime, timedelta
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CryptoScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def get_crypto_data_yahoo(self, symbol, period="1y"):
        """
        Fetch cryptocurrency data from Yahoo Finance
        """
        try:
            ticker = yf.Ticker(f"{symbol}-USD")
            data = ticker.history(period=period)
            
            if data.empty:
                logger.warning(f"No data found for {symbol}-USD")
                return None
                
            logger.info(f"Successfully fetched data for {symbol}")
            return data
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None

    def get_crypto_data_ccxt(
        self, symbol, exchange="binance", timeframe="1d", limit=100
    ):
        """
        Fetch cryptocurrency data using CCXT library
        """
        try:
            exchange_instance = getattr(ccxt, exchange)()
            ohlcv = exchange_instance.fetch_ohlcv(symbol, timeframe, limit=limit)

            df = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)

            logger.info(f"Successfully fetched {symbol} data from {exchange}")
            return df
        except Exception as e:
            logger.error(f"Error fetching data from {exchange} for {symbol}: {e}")
            return None

    def get_top_cryptocurrencies(self, limit=10):
        """
        Get list of top cryptocurrencies by market cap
        """
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": limit,
                "page": 1,
                "sparkline": False,
            }

            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            return [coin["symbol"].upper() for coin in data]
        except Exception as e:
            logger.error(f"Error fetching top cryptocurrencies: {e}")
            return ["BTC", "ETH", "BNB", "ADA", "SOL"]  # Fallback list

    def save_data(self, data, filename, output_dir="../output"):
        """
        Save data to CSV file
        """
        try:
            import os

            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            data.to_csv(filepath)
            logger.info(f"Data saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            return None


def main():
    """
    Main function to demonstrate scraper usage
    """
    scraper = CryptoScraper()

    # Get top cryptocurrencies
    top_cryptos = scraper.get_top_cryptocurrencies(5)
    logger.info(f"Top cryptocurrencies: {top_cryptos}")

    # Fetch data for each cryptocurrency
    for crypto in top_cryptos:
        data = scraper.get_crypto_data_yahoo(crypto, period="6mo")
        if data is not None:
            filename = f"{crypto.lower()}_data.csv"
            scraper.save_data(data, filename)
        time.sleep(1)  # Rate limiting


if __name__ == "__main__":
    main()
