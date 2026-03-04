import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

# Dark theme configuration
st.set_page_config(
    page_title="DividendTotalReturn-Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark, technical theme
st.markdown("""
<style>
    /* Main background - force override */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d35 100%) !important;
    }
    
    /* Main content area */
    .main .block-container {
        background: transparent !important;
    }
    
    /* Sidebar styling - force override */
    section[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%) !important;
        border-right: 1px solid #2d3748 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e0e0e0 !important;
    }
    
    /* Headers - force all header elements */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #00d4ff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
    }
    
    /* All text elements */
    p, span, div, label {
        color: #e0e0e0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ff88;
        font-family: 'Courier New', monospace;
        font-size: 28px;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Courier New', monospace;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background-color: #1a1f2e !important;
        color: #e0e0e0 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%);
        color: #000;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        background: linear-gradient(90deg, #00ffcc 0%, #00d4ff 100%);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #1a1f2e;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        background-color: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
        color: #e0e0e0;
    }
    
    /* Warning boxes */
    .stWarning {
        background-color: rgba(255, 165, 0, 0.1);
        border-left: 4px solid #ffa500;
        color: #e0e0e0;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #e0e0e0 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Slider */
    .stSlider {
        color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# Title with tech styling
st.markdown("<h1>⚡ DIVIDEND TOTAL RETURN PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888; font-family: Courier New; font-size: 14px;'>Advanced Multi-DRIP Portfolio Analysis Engine</p>", unsafe_allow_html=True)

# Initialize session state for ticker management
if 'ticker_list' not in st.session_state:
    st.session_state.ticker_list = []
if 'drip_config' not in st.session_state:
    st.session_state.drip_config = {}

# Sidebar configuration
with st.sidebar:
    st.markdown("<h2>⚙️ CONFIGURATION</h2>", unsafe_allow_html=True)
    
    # Ticker management
    st.markdown("<h3>📊 Ticker Management</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        new_ticker = st.text_input(
            "Add Ticker",
            placeholder="Enter symbol (e.g., AAPL)",
            key="ticker_input",
            label_visibility="collapsed"
        ).strip().upper()
    with col2:
        if st.button("➕ ADD", key="add_ticker"):
            if new_ticker and new_ticker not in st.session_state.ticker_list:
                if len(st.session_state.ticker_list) < 10:
                    st.session_state.ticker_list.append(new_ticker)
                    st.session_state.drip_config[new_ticker] = {
                        'mode': 'Traditional DRIP',
                        'nav_discount': 5.0
                    }
                    st.rerun()
                else:
                    st.warning("⚠️ Maximum 10 tickers")
    
    # Display current tickers with remove buttons
    if st.session_state.ticker_list:
        st.markdown(f"<p style='color: #888; font-size: 12px;'>Active Tickers: {len(st.session_state.ticker_list)}/10</p>", unsafe_allow_html=True)
        for ticker in st.session_state.ticker_list:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"<span style='color: #00d4ff; font-family: Courier New; font-weight: bold;'>{ticker}</span>", unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"remove_{ticker}"):
                    st.session_state.ticker_list.remove(ticker)
                    del st.session_state.drip_config[ticker]
                    st.rerun()
    else:
        st.info("👆 Add tickers to begin")
    
    st.markdown("---")
    
    # Date range
    st.markdown("<h3>📅 Date Range</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start",
            value=datetime.now() - timedelta(days=365*3),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "End",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # Initial investment
    st.markdown("<h3>💰 Initial Investment</h3>", unsafe_allow_html=True)
    initial_investment = st.number_input(
        "Amount ($)",
        min_value=100.0,
        value=10000.0,
        step=100.0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # DRIP Configuration per ticker
    if st.session_state.ticker_list:
        st.markdown("<h3>🔧 DRIP Configuration</h3>", unsafe_allow_html=True)
        
        for ticker in st.session_state.ticker_list:
            with st.expander(f"⚙️ {ticker}", expanded=False):
                mode = st.radio(
                    "DRIP Mode",
                    options=["No DRIP", "Traditional DRIP", "DRIP at NAV"],
                    key=f"mode_{ticker}",
                    index=["No DRIP", "Traditional DRIP", "DRIP at NAV"].index(
                        st.session_state.drip_config[ticker]['mode']
                    )
                )
                st.session_state.drip_config[ticker]['mode'] = mode
                
                if mode == "DRIP at NAV":
                    discount = st.slider(
                        "NAV Discount (%)",
                        min_value=0.0,
                        max_value=20.0,
                        value=st.session_state.drip_config[ticker]['nav_discount'],
                        step=0.5,
                        key=f"discount_{ticker}"
                    )
                    st.session_state.drip_config[ticker]['nav_discount'] = discount

# Main content area
if st.session_state.ticker_list:
    # Calculate button
    if st.button("🚀 EXECUTE ANALYSIS", type="primary", use_container_width=True):
        if start_date >= end_date:
            st.error("⚠️ Start date must be before end date")
        else:
            with st.spinner("⚡ Fetching market data and computing returns..."):
                results = {}
                errors = []
                
                # Progress bar
                progress_bar = st.progress(0)
                total_tickers = len(st.session_state.ticker_list)
                
                for idx, ticker in enumerate(st.session_state.ticker_list):
                    try:
                        # Update progress
                        progress_bar.progress((idx + 1) / total_tickers)
                        
                        # Fetch data
                        stock = yf.Ticker(ticker)
                        hist = stock.history(start=start_date, end=end_date)
                        
                        # Handle dividends with timezone fix
                        all_divs = stock.dividends
                        if not all_divs.empty and len(all_divs) > 0:
                            if all_divs.index.tz is not None:
                                start_ts = pd.Timestamp(start_date).tz_localize('UTC').tz_convert(all_divs.index.tz)
                                end_ts = pd.Timestamp(end_date).tz_localize('UTC').tz_convert(all_divs.index.tz)
                            else:
                                start_ts = pd.Timestamp(start_date)
                                end_ts = pd.Timestamp(end_date)
                            divs = all_divs[(all_divs.index >= start_ts) & (all_divs.index <= end_ts)]
                        else:
                            divs = pd.Series([], dtype=float)
                        
                        if hist.empty:
                            errors.append(f"{ticker}: No price data")
                            continue
                        
                        # Calculate returns
                        drip_mode = st.session_state.drip_config[ticker]['mode']
                        nav_discount = st.session_state.drip_config[ticker]['nav_discount'] / 100.0
                        
                        initial_price = hist['Close'].iloc[0]
                        shares = initial_investment / initial_price
                        cash = 0.0
                        
                        position_values = []
                        dates = []
                        
                        for date in hist.index:
                            current_price = hist.loc[date, 'Close']
                            
                            # Check for dividend
                            dividend_per_share = 0.0
                            if date in divs.index:
                                dividend_per_share = divs.loc[date]
                            
                            if dividend_per_share > 0:
                                dividend_amount = shares * dividend_per_share
                                
                                if drip_mode == "No DRIP":
                                    cash += dividend_amount
                                elif drip_mode == "Traditional DRIP":
                                    new_shares = dividend_amount / current_price
                                    shares += new_shares
                                elif drip_mode == "DRIP at NAV":
                                    nav_price = current_price * (1 - nav_discount)
                                    new_shares = dividend_amount / nav_price
                                    shares += new_shares
                            
                            position_value = (shares * current_price) + cash
                            position_values.append(position_value)
                            dates.append(date)
                        
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
                            "nav_discount": nav_discount * 100
                        }
                        
                    except Exception as e:
                        errors.append(f"{ticker}: {str(e)}")
                
                progress_bar.empty()
                
                # Display errors
                if errors:
                    st.warning("⚠️ Some tickers encountered errors:")
                    for error in errors:
                        st.write(f"• {error}")
                
                # Display results
                if results:
                    st.success(f"✅ Analysis complete for {len(results)} ticker(s)")
                    
                    # Metrics dashboard
                    st.markdown("<h2>📊 PERFORMANCE METRICS</h2>", unsafe_allow_html=True)
                    
                    # Create metric columns (2 rows of 5)
                    num_results = len(results)
                    cols_per_row = min(5, num_results)
                    
                    for row_start in range(0, num_results, 5):
                        row_results = list(results.items())[row_start:row_start + 5]
                        cols = st.columns(len(row_results))
                        
                        for idx, (ticker, data) in enumerate(row_results):
                            with cols[idx]:
                                delta_color = "normal" if data['total_return'] >= 0 else "inverse"
                                st.metric(
                                    label=f"🎯 {ticker}",
                                    value=f"${data['final_value']:,.0f}",
                                    delta=f"{data['total_return']:.2f}%"
                                )
                                st.caption(f"{data['drip_mode']}")
                    
                    st.markdown("---")
                    
                    # Total Value Over Time Chart
                    st.markdown("<h2>📈 TOTAL VALUE TRAJECTORY</h2>", unsafe_allow_html=True)
                    
                    fig = go.Figure()
                    
                    # Color palette for dark theme
                    colors = ['#00d4ff', '#00ff88', '#ff00ff', '#ffaa00', '#ff3366', 
                             '#00ffcc', '#cc00ff', '#ffcc00', '#3366ff', '#ff6633']
                    
                    for idx, (ticker, data) in enumerate(results.items()):
                        fig.add_trace(go.Scatter(
                            x=data['dates'],
                            y=data['values'],
                            mode='lines',
                            name=f"{ticker} ({data['drip_mode']})",
                            line=dict(color=colors[idx % len(colors)], width=2),
                            hovertemplate=f"<b>{ticker}</b><br>" +
                                          "Date: %{x|%Y-%m-%d}<br>" +
                                          "Value: $%{y:,.2f}<br>" +
                                          "<extra></extra>"
                        ))
                    
                    # Initial investment line
                    fig.add_hline(
                        y=initial_investment,
                        line_dash="dash",
                        line_color="rgba(255, 255, 255, 0.3)",
                        annotation_text=f"Initial: ${initial_investment:,.0f}",
                        annotation_position="right",
                        annotation_font_color="white"
                    )
                    
                    fig.update_layout(
                        title="Portfolio Value Evolution",
                        xaxis_title="Date",
                        yaxis_title="Total Value ($)",
                        hovermode="x unified",
                        height=600,
                        template="plotly_dark",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Courier New", color="#e0e0e0"),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Performance comparison bar chart
                    st.markdown("<h2>🏆 PERFORMANCE COMPARISON</h2>", unsafe_allow_html=True)
                    
                    perf_fig = go.Figure()
                    
                    tickers_sorted = sorted(results.items(), key=lambda x: x[1]['total_return'], reverse=True)
                    ticker_names = [t[0] for t in tickers_sorted]
                    returns = [t[1]['total_return'] for t in tickers_sorted]
                    bar_colors = ['#00ff88' if r >= 0 else '#ff3366' for r in returns]
                    
                    perf_fig.add_trace(go.Bar(
                        x=ticker_names,
                        y=returns,
                        marker_color=bar_colors,
                        text=[f"{r:.2f}%" for r in returns],
                        textposition='outside',
                        hovertemplate="<b>%{x}</b><br>Return: %{y:.2f}%<extra></extra>"
                    ))
                    
                    perf_fig.update_layout(
                        title="Total Return Ranking",
                        xaxis_title="Ticker",
                        yaxis_title="Total Return (%)",
                        height=400,
                        template="plotly_dark",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Courier New", color="#e0e0e0"),
                        showlegend=False
                    )
                    
                    st.plotly_chart(perf_fig, use_container_width=True)
                    
                    # Detailed breakdown table
                    st.markdown("<h2>📋 DETAILED BREAKDOWN</h2>", unsafe_allow_html=True)
                    
                    breakdown_data = []
                    for ticker, data in results.items():
                        breakdown_data.append({
                            "Ticker": ticker,
                            "DRIP Mode": data['drip_mode'],
                            "NAV Discount": f"{data['nav_discount']:.1f}%" if data['drip_mode'] == "DRIP at NAV" else "N/A",
                            "Final Shares": f"{data['final_shares']:.4f}",
                            "Cash Balance": f"${data['final_cash']:.2f}",
                            "Final Value": f"${data['final_value']:,.2f}",
                            "Total Return": f"{data['total_return']:.2f}%"
                        })
                    
                    df = pd.DataFrame(breakdown_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    # Landing state
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; background: rgba(0, 212, 255, 0.05); border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.2);'>
        <h2 style='color: #00d4ff; font-family: Courier New;'>🎯 GETTING STARTED</h2>
        <p style='color: #888; font-size: 16px; line-height: 1.8;'>
            <b>1.</b> Add up to 10 ticker symbols using the sidebar<br>
            <b>2.</b> Configure DRIP mode for each ticker<br>
            <b>3.</b> Set date range and initial investment<br>
            <b>4.</b> Execute analysis to compare performance
        </p>
        <p style='color: #00d4ff; font-size: 14px; margin-top: 20px;'>
            <b>DRIP MODES:</b> No DRIP | Traditional DRIP | DRIP at NAV (5-20% discount)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <h3 style='color: #00d4ff;'>💡 DRIP MODE INSIGHTS</h3>
    <div style='background: rgba(0, 212, 255, 0.05); padding: 20px; border-radius: 8px; border-left: 4px solid #00d4ff;'>
        <p style='color: #e0e0e0; line-height: 1.8;'>
        <b style='color: #00ff88;'>No DRIP:</b> Dividends accumulate as cash. Share count remains constant.<br><br>
        <b style='color: #00ff88;'>Traditional DRIP:</b> Dividends reinvested at market price on ex-date.<br>
        <code style='background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 4px;'>New Shares = Dividend Amount / Market Price</code><br><br>
        <b style='color: #00ff88;'>DRIP at NAV:</b> Dividends reinvested at discounted price (compounding advantage).<br>
        <code style='background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 4px;'>New Shares = Dividend Amount / (Market Price × (1 - Discount))</code>
        </p>
        <p style='color: #ffa500; margin-top: 15px;'>
        ⚡ <b>KEY INSIGHT:</b> A 5% NAV discount buys ~5.26% more shares per reinvestment, creating exponential compounding over decades.
        </p>
    </div>
    """, unsafe_allow_html=True)
