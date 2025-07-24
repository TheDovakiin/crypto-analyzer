"""
Cryptocurrency Data Analyzer
Performs technical analysis on cryptocurrency data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
import sys

# Add parent directory to path to import scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.scraper import CryptoScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CryptoAnalyzer:
    def __init__(self):
        self.scraper = CryptoScraper()
        self.analysis_results = {}

    def calculate_technical_indicators(self, data):
        """
        Calculate various technical indicators for the given data
        """
        if data is None or data.empty:
            return None

        df = data.copy()

        # Moving Averages
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["SMA_50"] = df["Close"].rolling(window=50).mean()
        df["EMA_12"] = df["Close"].ewm(span=12).mean()
        df["EMA_26"] = df["Close"].ewm(span=26).mean()

        # MACD
        df["MACD"] = df["EMA_12"] - df["EMA_26"]
        df["MACD_Signal"] = df["MACD"].ewm(span=9).mean()
        df["MACD_Histogram"] = df["MACD"] - df["MACD_Signal"]

        # RSI
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df["BB_Middle"] = df["Close"].rolling(window=20).mean()
        bb_std = df["Close"].rolling(window=20).std()
        df["BB_Upper"] = df["BB_Middle"] + (bb_std * 2)
        df["BB_Lower"] = df["BB_Middle"] - (bb_std * 2)

        # Volume indicators
        df["Volume_SMA"] = df["Volume"].rolling(window=20).mean()
        df["Volume_Ratio"] = df["Volume"] / df["Volume_SMA"]

        # Price changes
        df["Daily_Return"] = df["Close"].pct_change()
        df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod()

        return df

    def generate_signals(self, data):
        """
        Generate trading signals based on technical indicators
        """
        if data is None or data.empty:
            return None

        df = data.copy()
        signals = pd.DataFrame(index=df.index)
        signals["Signal"] = 0  # 0: Hold, 1: Buy, -1: Sell

        # MACD Signal
        signals.loc[df["MACD"] > df["MACD_Signal"], "MACD_Signal"] = 1
        signals.loc[df["MACD"] < df["MACD_Signal"], "MACD_Signal"] = -1

        # RSI Signal
        signals.loc[df["RSI"] < 30, "RSI_Signal"] = 1  # Oversold
        signals.loc[df["RSI"] > 70, "RSI_Signal"] = -1  # Overbought

        # Moving Average Signal
        signals.loc[df["SMA_20"] > df["SMA_50"], "MA_Signal"] = 1
        signals.loc[df["SMA_20"] < df["SMA_50"], "MA_Signal"] = -1

        # Bollinger Bands Signal
        signals.loc[df["Close"] < df["BB_Lower"], "BB_Signal"] = 1  # Oversold
        signals.loc[df["Close"] > df["BB_Upper"], "BB_Signal"] = -1  # Overbought

        # Combined signal (simple average)
        signal_columns = ["MACD_Signal", "RSI_Signal", "MA_Signal", "BB_Signal"]
        available_signals = [col for col in signal_columns if col in signals.columns]

        if available_signals:
            signals["Combined_Signal"] = signals[available_signals].mean(axis=1)
            signals["Final_Signal"] = np.where(
                signals["Combined_Signal"] > 0.5,
                1,
                np.where(signals["Combined_Signal"] < -0.5, -1, 0),
            )

        return signals

    def calculate_risk_metrics(self, data):
        """
        Calculate risk metrics for the cryptocurrency
        """
        if data is None or data.empty:
            return None

        returns = data["Close"].pct_change().dropna()

        metrics = {
            "Volatility": returns.std() * np.sqrt(252),  # Annualized volatility
            "Sharpe_Ratio": (returns.mean() * 252) / (returns.std() * np.sqrt(252)),
            "Max_Drawdown": self.calculate_max_drawdown(data["Close"]),
            "VaR_95": np.percentile(returns, 5),  # 95% Value at Risk
            "CVaR_95": returns[
                returns <= np.percentile(returns, 5)
            ].mean(),  # Conditional VaR
            "Total_Return": (data["Close"].iloc[-1] / data["Close"].iloc[0]) - 1,
        }

        return metrics

    def calculate_max_drawdown(self, prices):
        """
        Calculate maximum drawdown
        """
        peak = prices.expanding(min_periods=1).max()
        drawdown = (prices - peak) / peak
        return drawdown.min()

    def analyze_cryptocurrency(self, symbol, period="6mo"):
        """
        Complete analysis of a cryptocurrency
        """
        logger.info(f"Starting analysis for {symbol}")

        # Fetch data
        data = self.scraper.get_crypto_data_yahoo(symbol, period)
        if data is None or data.empty:
            logger.error(f"Could not fetch data for {symbol}")
            return None

        # Calculate technical indicators
        data_with_indicators = self.calculate_technical_indicators(data)

        # Generate signals
        signals = self.generate_signals(data_with_indicators)

        # Calculate risk metrics
        risk_metrics = self.calculate_risk_metrics(data_with_indicators)

        # Compile results
        analysis_result = {
            "symbol": symbol,
            "data": data_with_indicators,
            "signals": signals,
            "risk_metrics": risk_metrics,
            "last_price": data_with_indicators["Close"].iloc[-1],
            "analysis_date": datetime.now(),
        }

        self.analysis_results[symbol] = analysis_result
        logger.info(f"Analysis completed for {symbol}")

        return analysis_result

    def save_analysis(self, symbol, output_dir="../output"):
        """
        Save analysis results to files
        """
        if symbol not in self.analysis_results:
            logger.error(f"No analysis results found for {symbol}")
            return None

        result = self.analysis_results[symbol]

        try:
            os.makedirs(output_dir, exist_ok=True)

            # Save data with indicators
            data_file = os.path.join(output_dir, f"{symbol.lower()}_analysis.csv")
            result["data"].to_csv(data_file)

            # Save signals
            if result["signals"] is not None:
                signals_file = os.path.join(output_dir, f"{symbol.lower()}_signals.csv")
                result["signals"].to_csv(signals_file)

            # Save risk metrics
            if result["risk_metrics"] is not None:
                metrics_file = os.path.join(output_dir, f"{symbol.lower()}_metrics.txt")
                with open(metrics_file, "w") as f:
                    f.write(f"Analysis for {symbol}\n")
                    f.write(f"Date: {result['analysis_date']}\n")
                    f.write(f"Last Price: ${result['last_price']:.2f}\n\n")
                    f.write("Risk Metrics:\n")
                    for metric, value in result["risk_metrics"].items():
                        f.write(f"{metric}: {value:.4f}\n")

            logger.info(f"Analysis saved for {symbol}")
            return True

        except Exception as e:
            logger.error(f"Error saving analysis for {symbol}: {e}")
            return False


def main():
    """
    Main function to run cryptocurrency analysis
    """
    analyzer = CryptoAnalyzer()

    # Get top cryptocurrencies
    top_cryptos = analyzer.scraper.get_top_cryptocurrencies(5)
    logger.info(f"Analyzing top cryptocurrencies: {top_cryptos}")

    # Analyze each cryptocurrency
    successful_analyses = 0
    for crypto in top_cryptos:
        try:
            result = analyzer.analyze_cryptocurrency(crypto)
            if result:
                analyzer.save_analysis(crypto)
                successful_analyses += 1

                # Print summary
                print(f"\n=== {crypto} Analysis Summary ===")
                print(f"Last Price: ${result['last_price']:.2f}")
                if result["risk_metrics"]:
                    print(f"Volatility: {result['risk_metrics']['Volatility']:.2%}")
                    print(f"Total Return: {result['risk_metrics']['Total_Return']:.2%}")
                    print(f"Max Drawdown: {result['risk_metrics']['Max_Drawdown']:.2%}")
            else:
                print(f"\n=== {crypto} Analysis Failed ===")
                print("No data available for analysis")

        except Exception as e:
            logger.error(f"Error analyzing {crypto}: {e}")
            print(f"\n=== {crypto} Analysis Error ===")
            print(f"Error: {e}")
            continue

    print(f"\n=== Analysis Complete ===")
    print(
        f"Successfully analyzed {successful_analyses} out of {len(top_cryptos)} cryptocurrencies"
    )


if __name__ == "__main__":
    main()
