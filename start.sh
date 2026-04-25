#!/bin/bash

# Stadium Flow Cloud Run Startup Script

# 1. Initialize the SQLite database
echo "Initializing Stadium Database..."
python backend/setup_db.py

# 2. Start the Simulation Engine in the background
echo "Starting Simulation Engine..."
python backend/sim_engine.py &

# 3. Start the FastAPI Backend on port 8000 in the background
echo "Starting FastAPI Backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# 4. Start the Streamlit Frontend on the port specified by Cloud Run (default 8080)
echo "Starting Streamlit Frontend on port $PORT..."
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
