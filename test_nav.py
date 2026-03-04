#!/usr/bin/env python3
"""
Quick test to verify NAV fetching works
"""
import sys
sys.path.insert(0, '/tmp/dividend-pro-app')

from nav_fetcher import fetch_nav_history, get_nav_on_date
from datetime import datetime, timedelta

def test_nav_fetch():
    print("=" * 60)
    print("Testing NAV Fetcher Module")
    print("=" * 60)
    
    tickers = ['CLM', 'CRF', 'AAPL']
    start = datetime.now() - timedelta(days=365)
    end = datetime.now()
    
    for ticker in tickers:
        print(f"\n📊 Testing {ticker}...")
        try:
            nav_df = fetch_nav_history(ticker, start, end)
            if nav_df is not None and not nav_df.empty:
                print(f"   ✅ NAV data: {len(nav_df)} rows")
                print(f"   Range: ${nav_df['NAV'].min():.2f} - ${nav_df['NAV'].max():.2f}")
                
                # Test getting NAV on a specific date
                mid_date = nav_df['Date'].iloc[len(nav_df)//2]
                nav_value = get_nav_on_date(nav_df, mid_date)
                print(f"   Sample NAV ({mid_date.date()}): ${nav_value:.2f}")
            else:
                print(f"   ℹ️  No NAV data (expected for non-CEF)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All tests complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_nav_fetch()
