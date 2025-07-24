# 🚀 Cryptocurrency Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

A comprehensive cryptocurrency analysis tool that scrapes data, performs technical analysis, and creates interactive visualizations. Perfect for crypto traders, analysts, and researchers who want to make data-driven investment decisions.

## ✨ Features

- **📊 Data Scraping**: Fetches real-time cryptocurrency data from multiple sources (Yahoo Finance, CCXT exchanges)
- **📈 Technical Analysis**: Calculates 15+ technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands, etc.)
- **⚠️ Risk Analysis**: Computes comprehensive risk metrics (volatility, Sharpe ratio, max drawdown, VaR)
- **🎨 Interactive Visualization**: Creates beautiful, interactive charts and dashboards using Plotly
- **🐳 Docker Support**: Containerized application for easy deployment and consistency
- **📱 Web-Ready**: Generate HTML reports perfect for sharing and embedding

## 🏗️ Project Structure

```
crypto-analyzer/
├── 📁 src/
│   ├── scraper.py         # Data scraping module
│   ├── analyzer.py        # Technical analysis module
│   └── visualizer.py      # Visualization module
├── 📁 data/               # Input data directory
├── 📁 output/             # Generated charts and analysis
├── 🐳 Dockerfile          # Docker container configuration
├── 🐳 docker-compose.yml  # Docker Compose configuration
├── 📋 requirements.txt    # Python dependencies
├── 📖 README.md          # Project documentation
└── ⚖️ LICENSE            # MIT License
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kgabeci/crypto-analyzer.git
   cd crypto-analyzer
   ```

2. **Build and run with Docker Compose:**

   ```bash
   docker compose up --build
   ```

3. **Or build and run manually:**

   ```bash
   # Build the Docker image
   docker build -t crypto-analyzer .

   # Run the container
   docker run -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output crypto-analyzer
   ```

### Local Development

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the analyzer:**
   ```bash
   python src/analyzer.py
   ```

## 📊 Usage Examples

### Data Scraping

```python
from src.scraper import CryptoScraper

scraper = CryptoScraper()

# Get Bitcoin data from Yahoo Finance
btc_data = scraper.get_crypto_data_yahoo("BTC", period="1y")

# Get Ethereum data from Binance
eth_data = scraper.get_crypto_data_ccxt("ETH/USDT", exchange='binance')

# Get top 10 cryptocurrencies by market cap
top_cryptos = scraper.get_top_cryptocurrencies(10)
```

### Technical Analysis

```python
from src.analyzer import CryptoAnalyzer

analyzer = CryptoAnalyzer()

# Complete analysis of Bitcoin
result = analyzer.analyze_cryptocurrency("BTC", period="6mo")

# Access results
print(f"Last Price: ${result['last_price']:.2f}")
print(f"Volatility: {result['risk_metrics']['Volatility']:.2%}")
print(f"Sharpe Ratio: {result['risk_metrics']['Sharpe_Ratio']:.2f}")
```

### Interactive Visualization

```python
from src.visualizer import CryptoVisualizer

visualizer = CryptoVisualizer()

# Create comprehensive price chart with indicators
fig = visualizer.create_price_chart(data, "BTC", "btc_chart.html")

# Create correlation heatmap for multiple cryptocurrencies
fig = visualizer.create_correlation_heatmap(data_dict, "correlation.html")

# Generate complete dashboard
dashboard_path = visualizer.create_summary_dashboard(analysis_results)
```

## 📈 Technical Indicators

The analyzer calculates comprehensive technical indicators:

| Indicator           | Description                           | Period      |
| ------------------- | ------------------------------------- | ----------- |
| **SMA**             | Simple Moving Average                 | 20, 50 days |
| **EMA**             | Exponential Moving Average            | 12, 26 days |
| **MACD**            | Moving Average Convergence Divergence | 12, 26, 9   |
| **RSI**             | Relative Strength Index               | 14 days     |
| **Bollinger Bands** | Volatility bands                      | 20 days, 2σ |
| **Volume SMA**      | Volume moving average                 | 20 days     |
| **Volume Ratio**    | Current volume vs average             | -           |

## ⚠️ Risk Metrics

Comprehensive risk analysis including:

- **Volatility**: Annualized standard deviation of returns
- **Sharpe Ratio**: Risk-adjusted return measure
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Value at Risk (VaR)**: 95% confidence level
- **Conditional VaR (CVaR)**: Expected loss beyond VaR
- **Total Return**: Cumulative return over the period

## 📁 Output Files

The analysis generates professional reports:

- `{symbol}_analysis.csv` - Price data with all technical indicators
- `{symbol}_signals.csv` - Trading signals and recommendations
- `{symbol}_metrics.txt` - Risk metrics summary
- `{symbol}_chart.html` - Interactive price chart with indicators
- `correlation_heatmap.html` - Correlation matrix visualization
- `risk_return_analysis.html` - Risk-return scatter plot
- `performance_comparison.html` - Performance comparison chart
- `dashboard_index.html` - Comprehensive dashboard

## 🔧 Configuration

### Environment Variables

- `PYTHONPATH`: Set to `/app` in Docker container
- `PYTHONUNBUFFERED`: Set to `1` for immediate output

### Docker Configuration

The Dockerfile includes:

- Python 3.9 slim base image
- System dependencies (curl, wget)
- Non-root user for security
- Volume mounts for data and output directories

## 🌐 API Sources

- **Yahoo Finance**: Historical price data
- **CoinGecko API**: Market cap rankings and metadata
- **CCXT Library**: Exchange data (Binance, Coinbase, Kraken, etc.)

## 📦 Dependencies

### Core Libraries

- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `requests` - HTTP requests
- `yfinance` - Yahoo Finance data
- `ccxt` - Cryptocurrency exchange data

### Visualization

- `matplotlib` - Static plotting
- `seaborn` - Statistical visualization
- `plotly` - Interactive charts

### Web Scraping

- `beautifulsoup4` - HTML parsing
- `selenium` - Web automation

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This tool is for educational and research purposes only.** Cryptocurrency trading involves significant risk and can result in substantial financial losses. Always:

- Do your own research
- Never invest more than you can afford to lose
- Consider consulting with financial advisors
- Understand that past performance doesn't guarantee future results

## 🆘 Support

Need help? Here's how to get support:

1. 📖 Check the documentation above
2. 🔍 Search existing [issues](../../issues)
3. 🐛 Create a new issue with detailed information
4. 💬 Join our community discussions

## 🗺️ Roadmap

- [ ] Add machine learning models for price prediction
- [ ] Implement real-time data streaming
- [ ] Create web dashboard with Flask/FastAPI
- [ ] Add portfolio optimization features
- [ ] Support for more exchanges and data sources
- [ ] Mobile app companion
- [ ] Advanced backtesting capabilities

---

**Made with ❤️ for the crypto community**

_If you find this project helpful, please give it a ⭐ on GitHub!_
