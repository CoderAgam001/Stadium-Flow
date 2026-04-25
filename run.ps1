# Predictive Queue Rerouting MVP Startup Script

$VENV_PYTHON = ".venv/Scripts/python.exe"
$VENV_UVICORN = ".venv/Scripts/uvicorn.exe"
$VENV_STREAMLIT = ".venv/Scripts/streamlit.exe"

Write-Host "Initializing Database..."
& $VENV_PYTHON backend/setup_db.py

Write-Host "Starting Simulation Engine in Background..."
Start-Process -NoNewWindow -FilePath $VENV_PYTHON -ArgumentList "backend/sim_engine.py"

Write-Host "Starting FastAPI Backend..."
Start-Process -NoNewWindow -FilePath $VENV_UVICORN -ArgumentList "backend.main:app", "--reload"

Write-Host "Starting Streamlit Frontend..."
& $VENV_STREAMLIT run frontend/app.py
