#!/bin/bash
PORT=${PORT:-8501}
export STREAMLIT_SERVER_PORT=$(python3 -c "print(int('$PORT'))")
streamlit run app.py --server.address=0.0.0.0 --server.headless=true
