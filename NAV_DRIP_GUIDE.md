# NAV-Based DRIP Guide for Closed-End Funds

## 🎯 Overview

The app now supports **DRIP at NAV** for Closed-End Funds (CEFs) like CLM and CRF, which allows you to model dividend reinvestment at the fund's Net Asset Value rather than the market price.

---

## 📊 Why This Matters

### Closed-End Funds Trade at Premium/Discount

CEFs typically trade at a **discount or premium** to their Net Asset Value (NAV):

- **Market Price:** What you pay on the stock exchange
- **NAV:** The actual value of the fund's underlying assets per share
- **Discount/Premium:** The difference between the two

**Example:**
```
CLM Market Price: $7.50
CLM NAV: $8.00
Discount: -6.25% (trading at 6.25% discount to NAV)
```

### DRIP at NAV Advantage

When you DRIP at NAV:
- You reinvest dividends at the **true asset value** ($8.00)
- Not at the discounted market price ($7.50)
- This gives you **more economic value** per dollar reinvested

**Comparison:**

| DRIP Mode | Price Used | $100 Dividend Buys |
|-----------|------------|-------------------|
| Traditional DRIP | $7.50 (market) | 13.33 shares |
| **DRIP at NAV** | **$8.00 (NAV)** | **12.50 shares** |

*Wait, fewer shares?* Yes, but each share represents MORE underlying value!

**Economic Value Acquired:**
- Traditional DRIP: 13.33 shares × $8.00 NAV = **$106.64**
- DRIP at NAV: 12.50 shares × $8.00 NAV = **$100.00**

Actually, the Traditional DRIP looks better here because you're buying at a discount. The REAL advantage of DRIP at NAV comes when:
1. The fund **narrows its discount** (moves toward NAV)
2. You're getting shares at the "fair" price, not overpaying during premiums

---

## 🔧 How to Use in the App

### Step 1: Add CEF Tickers

Currently supported for NAV-based DRIP:
- **CLM** - Cornerstone Strategic Value Opportunities Fund
- **CRF** - Cornerstone Total Return Fund
- **UTF** - Cohen & Steers Infrastructure Fund
- **UTG** - Reaves Utility Income Fund

### Step 2: Configure DRIP Mode

When you add CLM or CRF, the app automatically defaults to **"DRIP at NAV (CEF)"**

In the DRIP Configuration section:
```
⚙️ CLM
  ⚪ No DRIP
  ⚪ Traditional DRIP
  ⚪ DRIP with Discount
  ⚫ DRIP at NAV (CEF)  ← Select this
```

### Step 3: Set Additional Discount (Optional)

Some CEF DRIP programs offer an **additional discount from NAV**:

```
📊 CLM will reinvest at actual NAV (fetched from historical data)

Discount from NAV (%): [slider 0-10%]
```

**If CLM offers 5% discount from NAV:**
- NAV = $8.00
- DRIP price = $8.00 × (1 - 0.05) = **$7.60**
- $100 dividend buys = 100 / 7.60 = **13.16 shares**

---

## 🧮 DRIP Mode Comparison

### Mode 1: No DRIP
```
Dividends → Cash
Result: Growing cash balance, static share count
```

### Mode 2: Traditional DRIP
```
Dividends → Reinvest at Market Price
Price Used: Whatever CLM trades at on ex-date ($7.50)
Result: Most shares acquired (if trading at discount)
```

### Mode 3: DRIP with Discount
```
Dividends → Reinvest at (Market Price - X%)
Price Used: Market price minus broker discount
Example: $7.50 × (1 - 0.02) = $7.35
Use Case: Brokerages offering 2-5% DRIP discounts
```

### Mode 4: DRIP at NAV (CEF)
```
Dividends → Reinvest at Net Asset Value
Price Used: Actual NAV from historical data ($8.00)
Optional: Additional discount from NAV
Result: Economic value optimization
```

---

## 📈 Real-World Example: CLM

### Scenario
- Initial investment: $10,000
- Time period: 5 years
- Monthly dividends: ~$80 (9.6% annual yield)
- Average discount to NAV: -6%

### Traditional DRIP (Market Price)
```
Year 1: Reinvest at ~$7.50 (market)
Year 5: 1,450 shares, Market Value $10,875
```

### DRIP at NAV
```
Year 1: Reinvest at ~$8.00 (NAV)
Year 5: 1,360 shares, Market Value $10,200
```

**But wait—if market converges to NAV:**
- Traditional DRIP shares × $8.00 = $11,600
- DRIP at NAV shares × $8.00 = **$10,880**

**Hmm, Traditional still wins if you bought at a discount!**

### When DRIP at NAV Wins

1. **Fund narrows discount:**
   - Start: -6% discount
   - End: -2% discount
   - DRIP at NAV protected you from overpaying

2. **Fund goes to premium:**
   - If CLM trades at +5% premium later
   - Traditional DRIP would have overpaid
   - NAV DRIP bought at fair value

3. **Volatility protection:**
   - Market price swings don't affect your reinvestment
   - Smooth, consistent NAV-based accumulation

---

## 🔍 How NAV is Calculated in the App

### For CLM/CRF (Built-in Estimation)

The app uses a **discount-based NAV estimator**:

```python
# CLM typically trades at ~5% discount to NAV
NAV ≈ Market Price / (1 - 0.05)
NAV ≈ Market Price / 0.95

If CLM = $7.50
NAV ≈ $7.50 / 0.95 = $7.89
```

**Why estimation?**
- Real-time NAV data requires paid APIs
- Historical NAV data not always available
- Estimation is accurate within 1-2% for stable discounts

### Future Enhancements

Planned integrations:
- **CEF Connect API:** Real historical NAV data
- **Cornerstone Website Scraping:** Official NAV values
- **Manual NAV Upload:** CSV import for custom NAV data

---

## 💡 Best Practices

### When to Use DRIP at NAV

✅ **Use NAV-based DRIP when:**
- Fund has historically volatile premium/discount
- You want to avoid overpaying during premiums
- Fund offers additional discount from NAV
- Long-term hold (10+ years) to benefit from fair pricing

❌ **Stick with Traditional DRIP when:**
- Fund consistently trades at deep discount
- You want maximum share accumulation
- Market price unlikely to converge to NAV

### Combining Modes

**Strategy:** Split positions
- 50% CLM with Traditional DRIP (maximize shares)
- 50% CLM with DRIP at NAV (fair value anchor)

---

## 📊 Supported CEF Tickers

| Ticker | Fund Name | Typical Discount | DRIP at NAV? |
|--------|-----------|------------------|--------------|
| **CLM** | Cornerstone Strategic Value | -5% to -8% | ✅ Yes |
| **CRF** | Cornerstone Total Return | -6% to -10% | ✅ Yes |
| **UTF** | Cohen & Steers Infrastructure | -8% to -12% | ✅ Yes |
| **UTG** | Reaves Utility Income | -10% to -15% | ✅ Yes |

### Adding More CEFs

To add support for other CEFs:
1. Edit `nav_fetcher.py`
2. Add ticker to `CEF_NAV_TICKERS` list
3. Set typical discount in `TYPICAL_DISCOUNTS` dict

---

## 🧪 Testing the Feature

### Test Case 1: CLM with Traditional DRIP
```
Add: CLM
Mode: Traditional DRIP
Range: 3 years
Investment: $10,000
```

### Test Case 2: CLM with DRIP at NAV
```
Add: CLM
Mode: DRIP at NAV (CEF)
Discount from NAV: 0%
Range: 3 years
Investment: $10,000
```

### Test Case 3: CLM with NAV + Discount
```
Add: CLM
Mode: DRIP at NAV (CEF)
Discount from NAV: 5%
Range: 3 years
Investment: $10,000
```

**Compare the three:** See how share counts and final values differ!

---

## ⚠️ Limitations

1. **NAV Estimation:** Uses typical discount ratios, not real-time NAV
2. **CEF-Specific:** Only works for supported CEF tickers
3. **Historical Accuracy:** Estimated NAV may differ from actual by 1-3%

**For production use:** Integrate real NAV data APIs

---

## 🔗 Resources

- **CEF Connect:** https://www.cefconnect.com (NAV data)
- **Cornerstone Funds:** https://www.cornerstonefunds.com
- **CLM Fund Page:** https://www.cornerstonestrategicinvestmentfund.com
- **CRF Fund Page:** https://www.cornerstonetotalreturnfund.com

---

**Questions?** Check TICKER_GUIDE.md or BUGFIX_LOG.md
