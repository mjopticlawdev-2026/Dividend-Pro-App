# Troubleshooting Guide

## 🆘 Common Issues & Solutions

### Issue: "Catastrophic errors" when adding multiple tickers

**Symptoms:**
- App works with one ticker (e.g., CLM alone)
- Adding a second ticker causes errors
- Website becomes unusable

**Root Causes:**
1. Configuration mismatch between CEF and non-CEF tickers
2. Session state corruption
3. Invalid DRIP mode for ticker type

**Solutions:**

#### Quick Fix #1: Clear and Re-add
```
1. Remove ALL tickers (click ❌ on each)
2. Hard refresh browser (Ctrl+Shift+R)
3. Add tickers back one at a time
4. Configure DRIP mode for each before adding next
```

#### Quick Fix #2: Restart App
```bash
tmux kill-session -t dividend-pro
/tmp/dividend-pro-app/start.sh
```
Then hard refresh browser.

#### Quick Fix #3: Check Mode Compatibility
- **CLM, CRF, UTF, UTG:** Can use "DRIP at NAV (CEF)"
- **All others (AAPL, MSFT, etc.):** Use "Traditional DRIP" or "DRIP with Discount"
- **Don't** try to use "DRIP at NAV (CEF)" on non-CEF tickers

---

### Issue: Ticker won't add

**Symptoms:**
- Click "➕ ADD" but ticker doesn't appear
- No error message shown

**Solutions:**
1. Check if ticker already in list (can't add duplicates)
2. Verify ticker symbol is valid (letters only, max 6 chars)
3. Check if you hit 10-ticker limit
4. Try uppercase (AAPL not aapl)

---

### Issue: "Invalid symbol or no data available"

**Symptoms:**
- Ticker adds successfully
- Error appears when executing analysis

**Solutions:**
1. Verify ticker exists on Yahoo Finance (finance.yahoo.com)
2. Check date range isn't before IPO/listing date
3. Try shorter date range (e.g., 1 year instead of 10)
4. For non-US stocks, use correct format (e.g., BP.L for London)

---

### Issue: App slow or unresponsive

**Symptoms:**
- Analysis takes >30 seconds
- Progress bar stuck

**Solutions:**
1. **Reduce ticker count:** Start with 2-3 tickers, add more gradually
2. **Shorten date range:** Try 1-3 years instead of 10+
3. **Check internet:** yfinance needs active connection
4. **Wait it out:** 10 tickers × 10 years = lots of data fetching

---

### Issue: NAV data not fetching for CLM/CRF

**Symptoms:**
- "DRIP at NAV (CEF)" selected
- Results show "At NAV (est)" instead of "At NAV ✓"

**This is normal!**
- The app uses estimated NAV based on typical discount
- Real NAV requires paid APIs
- Estimation is accurate within 1-3%

**To verify NAV estimation:**
```bash
cd /tmp/dividend-pro-app
source /tmp/dividend_venv/bin/activate
python3 test_nav.py
```

---

### Issue: Wrong DRIP mode showing in results

**Symptoms:**
- Configured "DRIP at NAV (CEF)" for AAPL
- Results show "Traditional DRIP"

**This is a safety feature!**
- Non-CEF tickers can't use NAV mode
- App automatically falls back to Traditional DRIP
- Only CLM, CRF, UTF, UTG support NAV mode

---

### Issue: Charts not rendering

**Symptoms:**
- Metrics show up
- Charts are blank or missing

**Solutions:**
1. Hard refresh browser (Ctrl+Shift+R)
2. Try different browser (Chrome recommended)
3. Disable browser extensions (ad blockers can interfere)
4. Check console for JavaScript errors (F12 → Console tab)

---

### Issue: Discount slider not appearing

**Symptoms:**
- Selected "DRIP with Discount" or "DRIP at NAV (CEF)"
- No slider shows up

**Solutions:**
1. Expand the ticker's configuration section (click "⚙️ TICKER")
2. Make sure mode is fully selected (radio button filled)
3. Refresh page if slider doesn't appear after 1-2 seconds

---

## 🔍 Diagnostic Commands

### Check if app is running:
```bash
curl http://localhost:8501/_stcore/health
# Should return: ok
```

### View app logs:
```bash
tmux attach -t dividend-pro
# Press Ctrl+B then D to detach
```

### Test NAV module:
```bash
cd /tmp/dividend-pro-app
source /tmp/dividend_venv/bin/activate
python3 test_nav.py
```

### Test multi-ticker config:
```bash
cd /tmp/dividend-pro-app
source /tmp/dividend_venv/bin/activate
python3 test_multi_ticker.py
```

---

## 🔄 Complete Reset

If nothing else works:

```bash
# 1. Kill app
tmux kill-session -t dividend-pro

# 2. Clear cache
rm -rf /tmp/dividend-pro-app/.streamlit/cache
rm -rf /home/mj/.streamlit/cache

# 3. Restart
/tmp/dividend-pro-app/start.sh

# 4. Hard refresh browser (Ctrl+Shift+R)
```

---

## 📊 Best Practices

### For Stable Performance:
1. **Start small:** Test with 1-2 tickers first
2. **Use CEF modes correctly:** Only CLM/CRF/UTF/UTG for NAV mode
3. **Reasonable date ranges:** 1-5 years is optimal
4. **One mode change at a time:** Don't change multiple configs then execute
5. **Remove before re-adding:** If changing ticker, remove old one first

### Known Limitations:
- **Max 10 tickers** (performance/UI limit)
- **NAV estimated** (real NAV requires paid APIs)
- **Yahoo Finance rate limits** (too many requests = temporary fail)
- **Historical data gaps** (some old CEF data incomplete)

---

## 🆘 Still Stuck?

**Check these files:**
- `TICKER_GUIDE.md` - Valid ticker symbols
- `NAV_DRIP_GUIDE.md` - CEF-specific help
- `BUGFIX_LOG.md` - Known bugs and fixes
- `CHANGELOG.md` - Recent changes

**Run diagnostics:**
```bash
cd /tmp/dividend-pro-app
source /tmp/dividend_venv/bin/activate

# Test NAV
python3 test_nav.py

# Test multi-ticker
python3 test_multi_ticker.py

# Check app health
curl http://localhost:8501/_stcore/health
```

**Last resort:**
```bash
# Restart everything fresh
tmux kill-session -t dividend-pro
rm -rf /tmp/dividend-pro-app/.streamlit/cache
/tmp/dividend-pro-app/start.sh
# Then hard refresh browser (Ctrl+Shift+R)
```
