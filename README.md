# 📈 DividendTotalReturn-Pro

A sophisticated web application for calculating total return with three dividend reinvestment plan (DRIP) modes:

1. **No DRIP** – Dividends paid as cash, not reinvested
2. **Traditional DRIP** – Dividends reinvested at market price on ex-date
3. **DRIP at NAV** – Dividends reinvested at a discount to market price (user-defined %, default 5%)

## 🚀 Features

- **Multi-ticker comparison**: Analyze multiple stocks side-by-side
- **Three DRIP modes per ticker**: Flexible configuration for each position
- **Interactive visualizations**: Plotly-powered multi-line charts
- **Real-time data**: Fetches historical prices and dividends via yfinance
- **NAV discount modeling**: Demonstrates the compounding power of discounted reinvestment

## 🧮 NAV Math (Mode C)

```
Dividend Amount = Shares Held × Dividend Per Share
NAV Price = Market Price × (1 - Discount)
New Shares = Dividend Amount / NAV Price
```

**Example:** With a 5% NAV discount, your dividends buy ~5.26% more shares than traditional DRIP. Over decades, this compounding advantage can significantly boost total returns.

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Dividend-Pro-App.git
cd Dividend-Pro-App
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install yfinance streamlit plotly pandas numpy
```

## 🎯 Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Configure your portfolio:
   - Enter stock tickers (comma-separated)
   - Set date range and initial investment
   - Choose DRIP mode for each ticker
   - Adjust NAV discount percentage if using DRIP at NAV

4. Click "Calculate Total Return" to see results

## 📊 Example Use Cases

- **Dividend Aristocrats**: Compare KO, JNJ, PG across DRIP modes
- **High-Yield REITs**: Model NAV discount scenarios
- **Retirement Planning**: Long-term dividend growth portfolios

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Data Source**: yfinance (Yahoo Finance API)
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy

## 📄 License

MIT License - feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. Past performance does not guarantee future results. Always consult a financial advisor before making investment decisions.
