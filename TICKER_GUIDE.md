# Ticker Symbol Guide

## ✅ Valid Tickers

Use **Yahoo Finance** ticker format:

### US Stocks
- `AAPL` - Apple Inc.
- `MSFT` - Microsoft Corporation  
- `KO` - Coca-Cola Company
- `JNJ` - Johnson & Johnson
- `PG` - Procter & Gamble

### ETFs
- `SPY` - S&P 500 ETF
- `QQQ` - Nasdaq-100 ETF
- `VYM` - Vanguard High Dividend Yield ETF
- `SCHD` - Schwab US Dividend Equity ETF

### REITs
- `O` - Realty Income
- `STAG` - STAG Industrial
- `VNQ` - Vanguard Real Estate ETF

## ❌ Common Errors

### "Invalid symbol or no data available"
**Causes:**
- Ticker doesn't exist on Yahoo Finance
- Company recently delisted
- Using wrong exchange format

**Solutions:**
- Verify ticker on finance.yahoo.com
- Check if company still publicly traded
- For non-US stocks, add exchange suffix (e.g., `AAPL.L` for London)

### "No price data"
**Causes:**
- IPO/listing happened after your start date
- Stock suspended/halted
- Data gap in Yahoo Finance

**Solutions:**
- Adjust start date to after IPO
- Check Yahoo Finance for data availability

### Ticker not adding
**Causes:**
- Already in list
- Maximum 10 tickers reached
- Invalid format (too long, contains numbers/symbols)

**Solutions:**
- Check active ticker list in sidebar
- Remove a ticker before adding new one
- Use standard format (letters only, max 6 chars)

## 🔍 How to Find Tickers

1. **Yahoo Finance:** https://finance.yahoo.com
   - Search company name
   - Ticker shown in upper left

2. **Google Search:**
   ```
   "[Company Name] ticker symbol"
   ```

3. **Common Formats:**
   - US stocks: `TICKER` (e.g., `AAPL`)
   - Canadian: `TICKER.TO` (e.g., `TD.TO`)
   - UK: `TICKER.L` (e.g., `BP.L`)
   - German: `TICKER.DE` (e.g., `BMW.DE`)

## 💡 Best Practices

### For Dividend Analysis
- Choose stocks with consistent dividend history (5+ years)
- Dividend Aristocrats are good candidates
- REITs typically have high yields
- ETFs like VYM, SCHD are diversified options

### Date Ranges
- **Short term (1-3 years):** Good for testing DRIP modes
- **Medium term (3-10 years):** Shows compounding effects
- **Long term (10+ years):** Best for NAV discount comparison

### DRIP Modes by Asset Type
- **Growth stocks (AAPL, MSFT):** Traditional DRIP or No DRIP
- **Dividend aristocrats (KO, JNJ):** Traditional DRIP or NAV
- **High-yield REITs (O):** DRIP at NAV to maximize compounding
- **Low-yield stocks:** No DRIP (dividends too small)

## 🧪 Test Portfolios

### Conservative Dividend Portfolio
```
KO, JNJ, PG, PEP, MCD
Traditional DRIP
10 years, $50k
```

### High-Yield REIT Portfolio
```
O, STAG, VNQ
DRIP at NAV (5%)
5 years, $25k
```

### Tech + Dividends
```
AAPL, MSFT, AVGO, TXN
Mix of modes
3 years, $30k
```

### Dividend Aristocrat Comparison
```
Target, Lowe's, Walmart, Costco, Home Depot
Compare NAV vs Traditional
15 years, $100k
```

## 🆘 Still Having Issues?

1. **Test with known-good ticker:** Try `AAPL` first
2. **Check date range:** Ensure start < end, not too far back
3. **Simplify:** Start with 1-2 tickers
4. **Verify on Yahoo:** Search ticker on finance.yahoo.com
5. **Clear and retry:** Remove all tickers and start fresh
