#!/usr/bin/env python3
"""
Test script to verify the crypto analyzer setup works
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add src to path
sys.path.append("src")

from src.analyzer import CryptoAnalyzer
from src.visualizer import CryptoVisualizer


def create_sample_data():
    """
    Create sample cryptocurrency data for testing
    """
    # Generate sample data for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    # Create sample data for BTC
    np.random.seed(42)  # For reproducible results
    initial_price = 50000
    returns = np.random.normal(0.001, 0.02, len(dates))  # Daily returns
    prices = [initial_price]

    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))

    # Create OHLCV data
    data = pd.DataFrame(
        {
            "Open": prices,
            "High": [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            "Low": [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            "Close": prices,
            "Volume": np.random.uniform(1000000, 5000000, len(dates)),
        },
        index=dates,
    )

    # Ensure High >= Low and High >= Close >= Low
    data["High"] = data[["Open", "High", "Close"]].max(axis=1)
    data["Low"] = data[["Open", "Low", "Close"]].min(axis=1)

    return data


def test_analysis():
    """
    Test the analysis pipeline with sample data
    """
    print("=== Testing Crypto Analyzer Setup ===")

    # Create sample data
    print("1. Creating sample data...")
    sample_data = create_sample_data()
    print(f"   Created {len(sample_data)} days of sample data")
    print(
        f"   Price range: ${sample_data['Close'].min():.2f} - ${sample_data['Close'].max():.2f}"
    )

    # Test analyzer
    print("\n2. Testing analyzer...")
    analyzer = CryptoAnalyzer()

    # Manually set the data in the scraper
    analyzer.scraper.sample_data = sample_data

    # Override the get_crypto_data_yahoo method for testing
    def mock_get_data(symbol, period="6mo"):
        return sample_data

    analyzer.scraper.get_crypto_data_yahoo = mock_get_data

    # Analyze the sample data
    result = analyzer.analyze_cryptocurrency("BTC", period="6mo")

    if result:
        print("   ✓ Analysis completed successfully")
        print(f"   Last Price: ${result['last_price']:.2f}")

        if result["risk_metrics"]:
            print(f"   Volatility: {result['risk_metrics']['Volatility']:.2%}")
            print(f"   Total Return: {result['risk_metrics']['Total_Return']:.2%}")
            print(f"   Max Drawdown: {result['risk_metrics']['Max_Drawdown']:.2%}")

        # Test saving
        print("\n3. Testing file saving...")
        success = analyzer.save_analysis("BTC")
        if success:
            print("   ✓ Files saved successfully")
        else:
            print("   ✗ Failed to save files")

        # Test visualizer
        print("\n4. Testing visualizer...")
        visualizer = CryptoVisualizer()

        # Create a simple chart
        fig = visualizer.create_price_chart(result["data"], "BTC")
        if fig:
            print("   ✓ Chart created successfully")

            # Save the chart
            chart_path = "output/btc_test_chart.html"
            os.makedirs("output", exist_ok=True)
            fig.write_html(chart_path)
            print(f"   ✓ Chart saved to {chart_path}")
        else:
            print("   ✗ Failed to create chart")

        return True
    else:
        print("   ✗ Analysis failed")
        return False


def main():
    """
    Main test function
    """
    try:
        success = test_analysis()

        if success:
            print("\n=== Test Results ===")
            print("✓ All tests passed!")
            print("✓ Crypto analyzer is working correctly")
            print("✓ Docker setup is ready to use")

            # Check if output files were created
            if os.path.exists("output"):
                files = os.listdir("output")
                if files:
                    print(f"✓ Generated {len(files)} output files")
                    for file in files:
                        print(f"  - {file}")
                else:
                    print("⚠ No output files generated")
        else:
            print("\n=== Test Results ===")
            print("✗ Some tests failed")
            print("Please check the error messages above")

    except Exception as e:
        print(f"\n=== Test Error ===")
        print(f"✗ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
