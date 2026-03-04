#!/bin/bash
# DividendTotalReturn-Pro Startup Script

cd /tmp/dividend-pro-app
source /tmp/dividend_venv/bin/activate
export PYTHONPATH=/tmp/dividend-pro-app:$PYTHONPATH

# Clear cache
rm -rf .streamlit/cache 2>/dev/null

# Start streamlit
streamlit run app.py --server.port 8501 --server.headless true
