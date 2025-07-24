"""
Configuration template for Crypto Analyzer
Copy this file to config.py and customize with your settings
"""

# API Configuration
API_CONFIG = {
    # Yahoo Finance - no API key required
    "yahoo_finance": {
        "enabled": True,
        "rate_limit": 100,  # requests per minute
    },
    # CoinGecko API - no API key required for basic usage
    "coingecko": {
        "enabled": True,
        "base_url": "https://api.coingecko.com/api/v3",
        "rate_limit": 50,  # requests per minute
    },
    # CCXT Exchange Configuration
    "exchanges": {
        "binance": {
            "enabled": True,
            "api_key": "",  # Add your API key here
            "secret": "",  # Add your secret here
            "sandbox": True,  # Use sandbox for testing
        },
        "coinbase": {
            "enabled": True,
            "api_key": "",
            "secret": "",
            "sandbox": True,
        },
        "kraken": {
            "enabled": True,
            "api_key": "",
            "secret": "",
            "sandbox": True,
        },
    },
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    # Default time periods
    "default_period": "6mo",
    "available_periods": [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ],
    # Technical indicators
    "indicators": {
        "sma_periods": [20, 50],
        "ema_periods": [12, 26],
        "rsi_period": 14,
        "macd_fast": 12,
        "macd_slow": 26,
        "macd_signal": 9,
        "bollinger_period": 20,
        "bollinger_std": 2,
    },
    # Risk metrics
    "risk": {
        "var_confidence": 0.95,
        "annualization_factor": 252,  # Trading days per year
    },
}

# Output Configuration
OUTPUT_CONFIG = {
    "output_dir": "../output",
    "chart_format": "html",  # html, png, jpg
    "chart_theme": "plotly_white",
    "save_data": True,
    "save_charts": True,
    "save_metrics": True,
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "crypto_analyzer.log",
    "console": True,
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "max_workers": 4,  # Number of parallel workers
    "cache_enabled": True,
    "cache_duration": 3600,  # Cache duration in seconds
    "request_timeout": 30,  # Request timeout in seconds
}

# Security Configuration
SECURITY_CONFIG = {
    "verify_ssl": True,
    "user_agent": "CryptoAnalyzer/1.0",
    "max_retries": 3,
    "retry_delay": 1,  # seconds
}
