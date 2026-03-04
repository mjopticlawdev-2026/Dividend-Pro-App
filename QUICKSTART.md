# ⚡ DividendTotalReturn-Pro v2.0 - Quick Start

## 🎯 Access
**URL:** http://localhost:8501

---

## 🚀 5-Minute Workflow

### 1. Add Tickers (Sidebar)
```
📊 Ticker Management
[AAPL      ] [➕ ADD]
```
- Type ticker → Click ADD
- Repeat for up to 10 stocks
- Click ❌ to remove any

### 2. Configure DRIP (Sidebar)
```
🔧 DRIP Configuration
▶ ⚙️ AAPL
  ⚪ No DRIP
  ⚫ Traditional DRIP  ← Select this
  ⚪ DRIP at NAV
```

### 3. Set Parameters (Sidebar)
```
📅 Date Range
Start: 2023-01-01
End:   2026-03-03

💰 Initial Investment
$10,000
```

### 4. Execute
```
[🚀 EXECUTE ANALYSIS]
```

### 5. Review Results
- **Metrics:** Top row shows final values & returns
- **Chart 1:** Line graph of value over time
- **Chart 2:** Bar chart ranking by performance
- **Table:** Detailed breakdown

---

## 🎨 Theme

**Colors:**
- Cyan: #00d4ff (primary)
- Green: #00ff88 (positive)
- Red: #ff3366 (negative)
- Orange: #ffa500 (warning)

**Background:** Dark gradient (#0a0e27 → #1a1d35)

---

## 💡 DRIP Modes Explained

| Mode | Behavior | Best For |
|------|----------|----------|
| **No DRIP** | Cash accumulates | Need liquidity |
| **Traditional DRIP** | Reinvest at market price | Standard compounding |
| **DRIP at NAV** | Reinvest at 5-20% discount | Max compounding |

**NAV Formula:**
```
New Shares = Dividend / (Price × (1 - Discount))
```

**Example:** $100 dividend, $50 price, 5% discount
- Traditional: $100 ÷ $50 = **2.00 shares**
- NAV: $100 ÷ ($50 × 0.95) = **2.11 shares** ✨ (+5.26%)

---

## 🐛 Troubleshooting

**App not responding?**
```bash
tmux kill-session -t dividend-pro
tmux new-session -d -s dividend-pro \
  "cd /tmp/dividend-pro-app && \
   source /tmp/dividend_venv/bin/activate && \
   streamlit run app.py --server.port 8501"
```

**Data fetch errors?**
- Check ticker symbols (use Yahoo Finance format)
- Try shorter date range
- Yahoo Finance rate limits apply

**Timezone errors?**
- Fixed in v1.0.1+ (auto-detects timezone)

---

## 📊 Sample Portfolios

### Dividend Aristocrats
```
KO, JNJ, PG, PEP, MCD
Traditional DRIP
10 years, $50k
```

### High-Yield REITs
```
O, STAG, VNQ
DRIP at NAV (5%)
5 years, $25k
```

### Tech Growth + Dividends
```
AAPL, MSFT, AVGO
Mix of modes
3 years, $10k
```

---

## ⌨️ Keyboard Tips

- **Tab:** Navigate between fields
- **Enter:** Submit after typing ticker
- **Space:** Toggle radio buttons
- **Arrows:** Adjust sliders

---

## 📁 File Locations

**App:** `/tmp/dividend-pro-app/app.py`  
**Docs:** `/home/mj/.openclaw/workspace-mj_finance/`  
**PDF:** `DRIP_Logic_Verification.pdf`  
**Logs:** `tmux attach -t dividend-pro`

---

## 🔄 Version Info

**Current:** v2.0.0  
**Released:** 2026-03-03  
**Changes:** Dark theme, reactive UI, 10 tickers, 2 charts  
**Commits:** 5 total

---

**Need help?** Check CHANGELOG.md or BUGFIX_LOG.md in `/tmp/dividend-pro-app/`
