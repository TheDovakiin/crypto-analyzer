#!/usr/bin/env python3
"""
Basic Crypto Analysis Example

This script demonstrates how to use the Crypto Analyzer
to perform basic analysis on Bitcoin data.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import CryptoScraper
from src.analyzer import CryptoAnalyzer
from src.visualizer import CryptoVisualizer


def main():
    """Run basic crypto analysis example."""
    print("🚀 Crypto Analyzer - Basic Example")
    print("=" * 50)

    # Initialize components
    scraper = CryptoScraper()
    analyzer = CryptoAnalyzer()
    visualizer = CryptoVisualizer()

    # Get Bitcoin data
    print("📊 Fetching Bitcoin data...")
    btc_data = scraper.get_crypto_data_yahoo("BTC", period="6mo")

    if btc_data is None or btc_data.empty:
        print("❌ Failed to fetch Bitcoin data")
        return

    print(f"✅ Fetched {len(btc_data)} days of Bitcoin data")
    print(f"📅 Date range: {btc_data.index[0].date()} to {btc_data.index[-1].date()}")
    print(f"💰 Current price: ${btc_data['Close'].iloc[-1]:.2f}")

    # Perform analysis
    print("\n📈 Performing technical analysis...")
    result = analyzer.analyze_cryptocurrency("BTC", period="6mo")

    if result is None:
        print("❌ Analysis failed")
        return

    # Display results
    print("\n📊 Analysis Results:")
    print("-" * 30)

    risk_metrics = result["risk_metrics"]
    print(f"📈 Total Return: {risk_metrics['Total_Return']:.2%}")
    print(f"📊 Volatility: {risk_metrics['Volatility']:.2%}")
    print(f"⚖️  Sharpe Ratio: {risk_metrics['Sharpe_Ratio']:.2f}")
    print(f"📉 Max Drawdown: {risk_metrics['Max_Drawdown']:.2%}")
    print(f"⚠️  VaR (95%): {risk_metrics['VaR_95']:.2%}")

    # Create visualization
    print("\n🎨 Creating visualization...")
    chart_path = visualizer.create_price_chart(
        result["data"], "BTC", "../output/btc_example_chart.html"
    )

    if chart_path:
        print(f"✅ Chart saved to: {chart_path}")
    else:
        print("❌ Failed to create chart")

    # Save analysis
    print("\n💾 Saving analysis results...")
    if analyzer.save_analysis("BTC"):
        print("✅ Analysis saved successfully")
    else:
        print("❌ Failed to save analysis")

    print("\n🎉 Example completed successfully!")
    print("📁 Check the 'output' directory for results")


if __name__ == "__main__":
    main()
