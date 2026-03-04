# Bug Fix Log

## Issue #1: Timezone Comparison Error (Fixed 2026-03-03)

### Symptom
When clicking "Calculate Total Return", the app showed an error about timezone comparison:
```
TypeError: Cannot compare tz-naive and tz-aware datetime-like objects
```

### Root Cause
The yfinance library returns dividend data with a timezone-aware index (e.g., `America/New_York`), but the Streamlit date inputs and Python `datetime` objects are timezone-naive. When filtering dividends by date range, pandas cannot compare these directly.

### Fix Applied
Updated `app.py` to detect if the dividend index is timezone-aware and convert comparison timestamps accordingly:

```python
# Get all dividends and filter by date (handle timezone issues)
all_divs = stock.dividends
if not all_divs.empty and len(all_divs) > 0:
    # Make timezone-aware timestamps if the index is timezone-aware
    if all_divs.index.tz is not None:
        # Localize to UTC then convert to the index timezone
        start_ts = pd.Timestamp(start_date).tz_localize('UTC').tz_convert(all_divs.index.tz)
        end_ts = pd.Timestamp(end_date).tz_localize('UTC').tz_convert(all_divs.index.tz)
    else:
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
    divs = all_divs[(all_divs.index >= start_ts) & (all_divs.index <= end_ts)]
else:
    divs = pd.Series([], dtype=float)
```

### Verification
Tested with AAPL (1-year period):
- ✅ 251 price rows fetched
- ✅ 4 dividends filtered correctly (0.26 per quarter)
- ✅ No timezone errors

### Commit
```
git commit 9fa3b49: "Fix timezone comparison issue with dividend date filtering"
```

---

## Testing Checklist

When testing the app, verify:

- [ ] Multiple tickers can be entered (comma-separated)
- [ ] Date range selection works (start < end)
- [ ] Initial investment amount accepted
- [ ] Each ticker can have different DRIP mode
- [ ] NAV discount slider appears when "DRIP at NAV" selected
- [ ] "Calculate Total Return" button triggers calculation
- [ ] No timezone errors appear
- [ ] Chart renders with all tickers
- [ ] Metrics dashboard shows correct values
- [ ] Breakdown table displays all data

---

## Known Limitations

1. **API Rate Limits:** yfinance uses Yahoo Finance which has rate limits. Too many rapid requests may fail temporarily.

2. **Data Quality:** Some stocks may have incomplete dividend history or missing price data for certain date ranges.

3. **Holidays/Weekends:** Date filtering is inclusive. If you select a weekend/holiday end date, the last trading day is used.

4. **Performance:** Fetching data for 10+ tickers over long periods (>10 years) may take 15-30 seconds.

---

## Debugging Commands

### Check if app is running:
```bash
tmux ls | grep dividend-pro
curl -s http://localhost:8501 | head -20
```

### View live logs:
```bash
tmux attach -t dividend-pro
# Press Ctrl+B then D to detach
```

### Restart app:
```bash
tmux kill-session -t dividend-pro
tmux new-session -d -s dividend-pro "cd /tmp/dividend-pro-app && source /tmp/dividend_venv/bin/activate && streamlit run app.py --server.port 8501"
```

### Test data fetch manually:
```bash
cd /tmp/dividend-pro-app
source /tmp/dividend_venv/bin/activate
python3 -c "import yfinance as yf; print(yf.Ticker('AAPL').history(period='1y'))"
```
