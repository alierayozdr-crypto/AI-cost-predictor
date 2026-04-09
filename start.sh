#!/bin/bash

# Unset problematic env var that Railway sets
unset STREAMLIT_SERVER_PORT

# Run streamlit with explicit port
streamlit run app.py \
  --server.port=${PORT:-8501} \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
