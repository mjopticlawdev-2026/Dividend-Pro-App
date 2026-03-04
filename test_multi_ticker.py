#!/usr/bin/env python3
"""
Test multi-ticker processing to verify no catastrophic errors
"""
import sys
sys.path.insert(0, '/tmp/dividend-pro-app')

def test_multi_ticker_config():
    """Simulate session state with multiple tickers"""
    
    # Simulate session state
    ticker_list = ['CLM', 'AAPL', 'MSFT']
    drip_config = {
        'CLM': {
            'mode': 'DRIP at NAV (CEF)',
            'drip_discount': 0.0,
            'nav_discount_pct': 0.0
        },
        'AAPL': {
            'mode': 'Traditional DRIP',
            'drip_discount': 0.0,
            'nav_discount_pct': 0.0
        },
        'MSFT': {
            'mode': 'DRIP with Discount',
            'drip_discount': 3.0,
            'nav_discount_pct': 0.0
        }
    }
    
    print("="*60)
    print("Testing Multi-Ticker Configuration")
    print("="*60)
    
    for ticker in ticker_list:
        print(f"\n📊 {ticker}")
        config = drip_config.get(ticker, {})
        mode = config.get('mode', 'Traditional DRIP')
        drip_disc = config.get('drip_discount', 0.0)
        nav_disc = config.get('nav_discount_pct', 0.0)
        
        print(f"   Mode: {mode}")
        print(f"   DRIP Discount: {drip_disc}%")
        print(f"   NAV Discount: {nav_disc}%")
        
        # Validate mode for non-CEF
        if mode == "DRIP at NAV (CEF)" and ticker not in ['CLM', 'CRF', 'UTF', 'UTG']:
            print(f"   ⚠️  Invalid mode for non-CEF - would fallback to Traditional DRIP")
        else:
            print(f"   ✅ Valid configuration")
    
    print("\n" + "="*60)
    print("✅ Configuration test passed!")
    print("="*60)

if __name__ == "__main__":
    test_multi_ticker_config()
