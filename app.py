import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="DividendTotalReturn-Pro", layout="wide")

st.title("📈 DividendTotalReturn-Pro")
st.markdown("**Calculate Total Return with Three DRIP Modes: No DRIP, Traditional DRIP, and DRIP at NAV**")

# Sidebar inputs
st.sidebar.header("Portfolio Configuration")

# Tickers input
tickers_input = st.sidebar.text_area(
    "Stock Tickers (comma-separated)",
    value="AAPL, MSFT, KO",
    help="Enter stock tickers separated by commas"
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# Date range
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=365*3),
        max_value=datetime.now()
    )
with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now(),
        max_value=datetime.now()
    )

# Initial investment
initial_investment = st.sidebar.number_input(
    "Initial Investment ($)",
    min_value=100.0,
    value=10000.0,
    step=100.0
)

st.sidebar.markdown("---")
st.sidebar.header("DRIP Configuration")

# DRIP settings per ticker
drip_settings = {}
for ticker in tickers:
    st.sidebar.subheader(f"🔹 {ticker}")
    
    drip_mode = st.sidebar.radio(
        f"{ticker} DRIP Mode",
        options=["No DRIP", "Traditional DRIP", "DRIP at NAV"],
        key=f"drip_{ticker}",
        help=f"Select dividend reinvestment mode for {ticker}"
    )
    
    nav_discount = 0.0
    if drip_mode == "DRIP at NAV":
        nav_discount = st.sidebar.slider(
            f"{ticker} NAV Discount (%)",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.5,
            key=f"discount_{ticker}",
            help="Discount percentage below market price for NAV reinvestment"
        ) / 100.0
    
    drip_settings[ticker] = {
        "mode": drip_mode,
        "nav_discount": nav_discount
    }

# Calculate button
if st.sidebar.button("🚀 Calculate Total Return", type="primary"):
    if not tickers:
        st.error("Please enter at least one ticker symbol.")
    elif start_date >= end_date:
        st.error("Start date must be before end date.")
    else:
        with st.spinner("Fetching data and calculating returns..."):
            results = {}
            errors = []
            
            for ticker in tickers:
                try:
                    # Fetch historical data
                    stock = yf.Ticker(ticker)
                    hist = stock.history(start=start_date, end=end_date)
                    
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
                    
                    if hist.empty:
                        errors.append(f"{ticker}: No price data found")
                        continue
                    
                    # Calculate position value over time
                    drip_mode = drip_settings[ticker]["mode"]
                    nav_discount = drip_settings[ticker]["nav_discount"]
                    
                    # Initialize
                    initial_price = hist['Close'].iloc[0]
                    shares = initial_investment / initial_price
                    cash = 0.0
                    
                    position_values = []
                    dates = []
                    
                    for date in hist.index:
                        current_price = hist.loc[date, 'Close']
                        
                        # Check for dividend on this date
                        dividend_per_share = 0.0
                        if date in divs.index:
                            dividend_per_share = divs.loc[date]
                        
                        if dividend_per_share > 0:
                            dividend_amount = shares * dividend_per_share
                            
                            if drip_mode == "No DRIP":
                                # (A) No DRIP - dividends paid as cash
                                cash += dividend_amount
                            
                            elif drip_mode == "Traditional DRIP":
                                # (B) Traditional DRIP - reinvest at market price
                                new_shares = dividend_amount / current_price
                                shares += new_shares
                            
                            elif drip_mode == "DRIP at NAV":
                                # (C) DRIP at NAV - reinvest at discount
                                # NAV math: New Shares = Dividend Amount / (Market Price * (1 - Discount))
                                nav_price = current_price * (1 - nav_discount)
                                new_shares = dividend_amount / nav_price
                                shares += new_shares
                        
                        # Total position value = stock value + cash
                        position_value = (shares * current_price) + cash
                        position_values.append(position_value)
                        dates.append(date)
                    
                    # Calculate final metrics
                    final_value = position_values[-1]
                    total_return = ((final_value - initial_investment) / initial_investment) * 100
                    
                    results[ticker] = {
                        "dates": dates,
                        "values": position_values,
                        "final_value": final_value,
                        "total_return": total_return,
                        "final_shares": shares,
                        "final_cash": cash,
                        "drip_mode": drip_mode,
                        "nav_discount": nav_discount
                    }
                    
                except Exception as e:
                    errors.append(f"{ticker}: {str(e)}")
            
            # Display errors
            if errors:
                st.warning("⚠️ Some tickers encountered errors:")
                for error in errors:
                    st.write(f"• {error}")
            
            # Display results
            if results:
                st.success(f"✅ Successfully calculated returns for {len(results)} ticker(s)")
                
                # Metrics dashboard
                st.header("📊 Summary Metrics")
                cols = st.columns(len(results))
                for idx, (ticker, data) in enumerate(results.items()):
                    with cols[idx]:
                        st.metric(
                            label=f"{ticker}",
                            value=f"${data['final_value']:,.2f}",
                            delta=f"{data['total_return']:.2f}%"
                        )
                        st.caption(f"Mode: {data['drip_mode']}")
                        if data['drip_mode'] == "DRIP at NAV":
                            st.caption(f"NAV Discount: {data['nav_discount']*100:.1f}%")
                
                # Multi-line chart
                st.header("📈 Total Value Over Time")
                fig = go.Figure()
                
                for ticker, data in results.items():
                    fig.add_trace(go.Scatter(
                        x=data['dates'],
                        y=data['values'],
                        mode='lines',
                        name=f"{ticker} ({data['drip_mode']})",
                        hovertemplate=f"<b>{ticker}</b><br>" +
                                      "Date: %{x}<br>" +
                                      "Value: $%{y:,.2f}<br>" +
                                      "<extra></extra>"
                    ))
                
                fig.add_hline(
                    y=initial_investment,
                    line_dash="dash",
                    line_color="gray",
                    annotation_text=f"Initial: ${initial_investment:,.0f}",
                    annotation_position="right"
                )
                
                fig.update_layout(
                    title="Portfolio Total Value Comparison",
                    xaxis_title="Date",
                    yaxis_title="Total Value ($)",
                    hovermode="x unified",
                    height=600,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed breakdown table
                st.header("📋 Detailed Breakdown")
                breakdown_data = []
                for ticker, data in results.items():
                    breakdown_data.append({
                        "Ticker": ticker,
                        "DRIP Mode": data['drip_mode'],
                        "NAV Discount": f"{data['nav_discount']*100:.1f}%" if data['drip_mode'] == "DRIP at NAV" else "N/A",
                        "Final Shares": f"{data['final_shares']:.4f}",
                        "Cash Balance": f"${data['final_cash']:.2f}",
                        "Final Value": f"${data['final_value']:,.2f}",
                        "Total Return": f"{data['total_return']:.2f}%"
                    })
                
                df = pd.DataFrame(breakdown_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # DRIP comparison insight
                st.header("💡 DRIP Mode Insights")
                st.markdown("""
                **Understanding the Three DRIP Modes:**
                
                - **No DRIP (Mode A)**: Dividends are paid as cash and not reinvested. The cash balance grows but share count remains constant.
                
                - **Traditional DRIP (Mode B)**: Dividends are automatically reinvested at the market price on the ex-dividend date. 
                  This is the standard DRIP offered by most brokerages.
                  
                - **DRIP at NAV (Mode C)**: Dividends are reinvested at a discount to the market price. This creates a compounding 
                  advantage as you acquire more shares per dollar of dividend than traditional DRIP.
                  
                **NAV Math (Mode C):**
                ```
                Dividend Amount = Shares Held × Dividend Per Share
                NAV Price = Market Price × (1 - Discount)
                New Shares = Dividend Amount / NAV Price
                ```
                
                **Why NAV Matters:** A 5% NAV discount means your dividends buy ~5.26% more shares than traditional DRIP. 
                Over decades, this compounding difference can significantly boost total returns.
                """)

else:
    st.info("👈 Configure your portfolio in the sidebar and click 'Calculate Total Return' to begin.")
    
    st.markdown("""
    ### How to Use:
    1. Enter stock tickers (comma-separated) in the sidebar
    2. Set your date range and initial investment amount
    3. Configure DRIP mode for each ticker:
       - **No DRIP**: Dividends accumulate as cash
       - **Traditional DRIP**: Dividends reinvested at market price
       - **DRIP at NAV**: Dividends reinvested at discounted price
    4. Click "Calculate Total Return" to see results
    
    ### Example Use Cases:
    - Compare dividend aristocrats (KO, JNJ, PG) across DRIP modes
    - Analyze high-yield REITs with NAV discounts
    - Model long-term retirement portfolios with dividend reinvestment
    """)
