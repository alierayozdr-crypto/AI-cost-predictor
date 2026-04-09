#!/bin/bash

# Override Railway's incorrect STREAMLIT_SERVER_PORT with actual PORT value
export STREAMLIT_SERVER_PORT=${PORT:-8501}

# Run streamlit
streamlit run app.py \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
