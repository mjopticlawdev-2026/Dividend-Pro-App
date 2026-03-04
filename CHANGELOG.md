# Changelog

## v2.0.0 - Major UI Redesign (2026-03-03 21:53 PST)

### 🎨 New Features

**Modern Dark Theme**
- Cyberpunk-inspired dark gradient background (#0a0e27 → #1a1d35)
- Technical color scheme: cyan (#00d4ff), neon green (#00ff88), magenta (#ff00ff)
- Monospace "Courier New" fonts throughout for technical aesthetic
- Glowing button hover effects with box shadows

**Reactive Ticker Management**
- ✅ Add/remove tickers dynamically without page refresh
- ✅ Real-time ticker list updates (up to 10 tickers)
- ✅ Individual remove buttons per ticker
- ✅ Input clears automatically after adding ticker
- ✅ Session state persistence across interactions

**Enhanced Capacity**
- 10 tickers maximum (up from 3 default)
- Visual counter showing active tickers (e.g., "Active Tickers: 3/10")
- Warning when attempting to exceed limit

**New Visualizations**
- **Total Value Trajectory Chart:** Multi-line time series with distinct colors per ticker
- **Performance Comparison Chart:** Horizontal bar chart ranking tickers by total return
- **Color-coded returns:** Green bars for gains, red for losses
- Both charts use plotly_dark template for consistency

**Improved DRIP Configuration**
- Collapsible expanders per ticker for cleaner interface
- Default to "Traditional DRIP" for new tickers
- NAV discount slider only appears when "DRIP at NAV" selected
- Configuration persists in session state

**Better User Experience**
- Progress bar during data fetching
- Landing page with clear instructions
- Color-coded metrics (delta indicators)
- Responsive grid layout (5 columns per row for metrics)
- Professional typography and spacing

### 🔧 Technical Improvements

**Session State Management**
- `ticker_list`: Array of active tickers
- `drip_config`: Dictionary storing DRIP settings per ticker
- Persistent across button clicks and reruns

**CSS Customization**
- Custom dark theme CSS injected via st.markdown
- Styled components: buttons, inputs, metrics, dataframes
- Gradient backgrounds and borders
- Monospace fonts for technical aesthetic

**Chart Enhancements**
- 10-color palette for line charts
- Unified hover mode on time series
- Transparent backgrounds (plot_bgcolor, paper_bgcolor)
- Horizontal legend positioning
- Custom annotations

### 🐛 Bug Fixes

- Fixed reactive updates when adding/removing tickers
- Input field now clears after adding ticker
- Proper state synchronization between UI and calculations

### 📊 Visual Examples

**Metrics Dashboard:**
```
🎯 AAPL          🎯 MSFT          🎯 KO
$12,450          $11,890          $10,320
↑ 24.50%         ↑ 18.90%         ↑ 3.20%
Traditional DRIP  DRIP at NAV      No DRIP
```

**Performance Bar Chart:**
- Sorted by return (highest to lowest)
- Green/red color coding
- Percentage labels on bars

**Color Palette:**
- Primary: #00d4ff (cyan)
- Success: #00ff88 (neon green)
- Warning: #ffa500 (orange)
- Error: #ff3366 (red)
- Accent: #ff00ff (magenta)

### 📝 Code Stats

- Lines changed: +450, -261
- New CSS: ~100 lines
- New session state logic: ~30 lines
- New performance chart: ~40 lines

---

## v1.0.1 - Timezone Fix (2026-03-03 21:48 PST)

### 🐛 Bug Fixes
- Fixed timezone comparison error when filtering dividends
- Added timezone-aware timestamp conversion
- Graceful handling of both tz-aware and tz-naive data

### 📄 Documentation
- Added BUGFIX_LOG.md with troubleshooting guide
- Documented timezone issue and solution

---

## v1.0.0 - Initial Release (2026-03-03 20:36 PST)

### 🚀 Core Features
- Three DRIP modes: No DRIP, Traditional DRIP, DRIP at NAV
- Multi-ticker comparison (comma-separated input)
- Date range selection
- Interactive Plotly charts
- Detailed breakdown table
- Real-time data via yfinance

### 📊 Calculations
- Exact NAV math: `New Shares = Dividend Amount / (Market Price × (1 - Discount))`
- Per-ticker DRIP configuration
- Cash accumulation tracking
- Total return percentage

### 📄 Documentation
- README.md
- DRIP_Logic_Verification.pdf
- GITHUB_SETUP.md
- DividendPro_DeploymentSummary.md
