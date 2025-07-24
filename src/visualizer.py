"""
Cryptocurrency Data Visualizer
Creates charts and visualizations for cryptocurrency analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for matplotlib
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class CryptoVisualizer:
    def __init__(self):
        self.colors = {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "danger": "#d62728",
            "warning": "#ff7f0e",
            "info": "#17a2b8",
        }

    def create_price_chart(self, data, symbol, save_path=None):
        """
        Create a comprehensive price chart with technical indicators
        """
        if data is None or data.empty:
            logger.error("No data provided for visualization")
            return None

        # Create subplots
        fig = make_subplots(
            rows=4,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f"{symbol} Price Chart", "Volume", "RSI", "MACD"),
            row_heights=[0.5, 0.15, 0.15, 0.2],
        )

        # Price and moving averages
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                name="Price",
                line=dict(color=self.colors["primary"]),
            ),
            row=1,
            col=1,
        )

        if "SMA_20" in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["SMA_20"],
                    name="SMA 20",
                    line=dict(color=self.colors["secondary"]),
                ),
                row=1,
                col=1,
            )

        if "SMA_50" in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["SMA_50"],
                    name="SMA 50",
                    line=dict(color=self.colors["warning"]),
                ),
                row=1,
                col=1,
            )

        # Bollinger Bands
        if all(col in data.columns for col in ["BB_Upper", "BB_Middle", "BB_Lower"]):
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["BB_Upper"],
                    name="BB Upper",
                    line=dict(color="rgba(255,0,0,0.3)"),
                    showlegend=False,
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["BB_Lower"],
                    name="BB Lower",
                    line=dict(color="rgba(255,0,0,0.3)"),
                    fill="tonexty",
                ),
                row=1,
                col=1,
            )

        # Volume
        colors = [
            "red" if close < open else "green"
            for close, open in zip(data["Close"], data["Open"])
        ]

        fig.add_trace(
            go.Bar(x=data.index, y=data["Volume"], name="Volume", marker_color=colors),
            row=2,
            col=1,
        )

        # RSI
        if "RSI" in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["RSI"],
                    name="RSI",
                    line=dict(color=self.colors["info"]),
                ),
                row=3,
                col=1,
            )
            # Add overbought/oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

        # MACD
        if "MACD" in data.columns and "MACD_Signal" in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["MACD"],
                    name="MACD",
                    line=dict(color=self.colors["primary"]),
                ),
                row=4,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["MACD_Signal"],
                    name="MACD Signal",
                    line=dict(color=self.colors["secondary"]),
                ),
                row=4,
                col=1,
            )

            # MACD Histogram
            colors = ["green" if val >= 0 else "red" for val in data["MACD_Histogram"]]
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data["MACD_Histogram"],
                    name="MACD Histogram",
                    marker_color=colors,
                ),
                row=4,
                col=1,
            )

        # Update layout
        fig.update_layout(
            title=f"{symbol} Technical Analysis",
            height=800,
            showlegend=True,
            xaxis_rangeslider_visible=False,
        )

        if save_path:
            fig.write_html(save_path)
            logger.info(f"Chart saved to {save_path}")

        return fig

    def create_correlation_heatmap(self, data_dict, save_path=None):
        """
        Create correlation heatmap for multiple cryptocurrencies
        """
        # Prepare data for correlation analysis
        returns_data = {}
        for symbol, data in data_dict.items():
            if data is not None and not data.empty:
                returns_data[symbol] = data["Close"].pct_change().dropna()

        if len(returns_data) < 2:
            logger.warning("Need at least 2 cryptocurrencies for correlation analysis")
            return None

        # Create correlation matrix
        returns_df = pd.DataFrame(returns_data)
        correlation_matrix = returns_df.corr()

        # Create heatmap
        fig = go.Figure(
            data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                colorscale="RdBu",
                zmid=0,
                text=np.round(correlation_matrix.values, 2),
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False,
            )
        )

        fig.update_layout(
            title="Cryptocurrency Returns Correlation Matrix",
            xaxis_title="Cryptocurrencies",
            yaxis_title="Cryptocurrencies",
            height=600,
        )

        if save_path:
            fig.write_html(save_path)
            logger.info(f"Correlation heatmap saved to {save_path}")

        return fig

    def create_risk_return_scatter(self, risk_metrics_dict, save_path=None):
        """
        Create risk-return scatter plot
        """
        if not risk_metrics_dict:
            logger.error("No risk metrics provided")
            return None

        # Prepare data
        symbols = []
        returns = []
        volatilities = []

        for symbol, metrics in risk_metrics_dict.items():
            if metrics and "Total_Return" in metrics and "Volatility" in metrics:
                symbols.append(symbol)
                returns.append(metrics["Total_Return"])
                volatilities.append(metrics["Volatility"])

        if len(symbols) < 2:
            logger.warning("Need at least 2 cryptocurrencies for risk-return analysis")
            return None

        # Create scatter plot
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=volatilities,
                y=returns,
                mode="markers+text",
                text=symbols,
                textposition="top center",
                marker=dict(
                    size=15,
                    color=returns,
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Return"),
                ),
                hovertemplate="<b>%{text}</b><br>"
                + "Volatility: %{x:.2%}<br>"
                + "Return: %{y:.2%}<br>"
                + "<extra></extra>",
            )
        )

        fig.update_layout(
            title="Risk-Return Analysis",
            xaxis_title="Volatility (Risk)",
            yaxis_title="Total Return",
            height=600,
        )

        # Add zero return line
        fig.add_hline(y=0, line_dash="dash", line_color="gray")

        if save_path:
            fig.write_html(save_path)
            logger.info(f"Risk-return scatter plot saved to {save_path}")

        return fig

    def create_performance_comparison(self, data_dict, save_path=None):
        """
        Create performance comparison chart
        """
        if not data_dict:
            logger.error("No data provided for performance comparison")
            return None

        # Calculate cumulative returns
        performance_data = {}
        for symbol, data in data_dict.items():
            if data is not None and not data.empty:
                returns = data["Close"].pct_change().dropna()
                cumulative_returns = (1 + returns).cumprod()
                performance_data[symbol] = cumulative_returns

        if len(performance_data) < 2:
            logger.warning(
                "Need at least 2 cryptocurrencies for performance comparison"
            )
            return None

        # Create comparison chart
        fig = go.Figure()

        colors = px.colors.qualitative.Set3
        for i, (symbol, performance) in enumerate(performance_data.items()):
            fig.add_trace(
                go.Scatter(
                    x=performance.index,
                    y=performance.values,
                    name=symbol,
                    line=dict(color=colors[i % len(colors)]),
                )
            )

        fig.update_layout(
            title="Cryptocurrency Performance Comparison",
            xaxis_title="Date",
            yaxis_title="Cumulative Return",
            height=600,
            hovermode="x unified",
        )

        # Add baseline at 1.0
        fig.add_hline(y=1.0, line_dash="dash", line_color="gray")

        if save_path:
            fig.write_html(save_path)
            logger.info(f"Performance comparison saved to {save_path}")

        return fig

    def create_summary_dashboard(self, analysis_results, output_dir="../output"):
        """
        Create a comprehensive dashboard with all visualizations
        """
        if not analysis_results:
            logger.error("No analysis results provided")
            return None

        # Prepare data
        data_dict = {}
        risk_metrics_dict = {}

        for symbol, result in analysis_results.items():
            if result and "data" in result:
                data_dict[symbol] = result["data"]
            if result and "risk_metrics" in result:
                risk_metrics_dict[symbol] = result["risk_metrics"]

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate all charts
        charts_created = []

        # 1. Individual price charts
        for symbol, data in data_dict.items():
            if data is not None:
                chart_path = os.path.join(output_dir, f"{symbol.lower()}_chart.html")
                self.create_price_chart(data, symbol, chart_path)
                charts_created.append(chart_path)

        # 2. Correlation heatmap
        if len(data_dict) >= 2:
            corr_path = os.path.join(output_dir, "correlation_heatmap.html")
            self.create_correlation_heatmap(data_dict, corr_path)
            charts_created.append(corr_path)

        # 3. Risk-return scatter
        if risk_metrics_dict:
            risk_path = os.path.join(output_dir, "risk_return_analysis.html")
            self.create_risk_return_scatter(risk_metrics_dict, risk_path)
            charts_created.append(risk_path)

        # 4. Performance comparison
        if len(data_dict) >= 2:
            perf_path = os.path.join(output_dir, "performance_comparison.html")
            self.create_performance_comparison(data_dict, perf_path)
            charts_created.append(perf_path)

        # Create dashboard index
        dashboard_path = os.path.join(output_dir, "dashboard_index.html")
        self.create_dashboard_index(charts_created, dashboard_path)

        logger.info(f"Dashboard created with {len(charts_created)} charts")
        return dashboard_path

    def create_dashboard_index(self, chart_paths, output_path):
        """
        Create an HTML index page for the dashboard
        """
        html_content = (
            """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cryptocurrency Analysis Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .chart-section { margin-bottom: 40px; }
                .chart-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
                iframe { width: 100%; height: 600px; border: none; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Cryptocurrency Analysis Dashboard</h1>
                <p>Generated on: """
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + """</p>
            </div>
        """
        )

        for chart_path in chart_paths:
            chart_name = (
                os.path.basename(chart_path)
                .replace(".html", "")
                .replace("_", " ")
                .title()
            )
            html_content += f"""
            <div class="chart-section">
                <div class="chart-title">{chart_name}</div>
                <iframe src="{os.path.basename(chart_path)}"></iframe>
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        with open(output_path, "w") as f:
            f.write(html_content)

        logger.info(f"Dashboard index created at {output_path}")


def main():
    """
    Main function to demonstrate visualizer usage
    """
    # This would typically be used with data from the analyzer
    visualizer = CryptoVisualizer()
    logger.info("CryptoVisualizer initialized")


if __name__ == "__main__":
    main()
