# Predictive Queue Rerouting MVP Startup Script

Write-Host "Initializing Database..."
python backend/setup_db.py

Write-Host "Starting Simulation Engine in Background..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "backend/sim_engine.py"

Write-Host "Starting FastAPI Backend..."
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "backend.main:app", "--reload"

Write-Host "Starting Streamlit Frontend..."
streamlit run frontend/app.py
