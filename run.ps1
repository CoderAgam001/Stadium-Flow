# Stadium Flow System Startup Script

# Activate the virtual environment
if (Test-Path ".venv/Scripts/Activate.ps1") {
    . .venv/Scripts/Activate.ps1
}

# Set the paths to the executables in the virtual environment
$VENV_PYTHON = ".venv/Scripts/python.exe"
$VENV_UVICORN = ".venv/Scripts/uvicorn.exe"
$VENV_STREAMLIT = ".venv/Scripts/streamlit.exe"

# Initialize Database
Write-Host "Initializing Database..."
& $VENV_PYTHON backend/setup_db.py

# Start Simulation Engine in Background
Write-Host "Starting Simulation Engine in Background..."
Start-Process -NoNewWindow -FilePath $VENV_PYTHON -ArgumentList "backend/sim_engine.py"

# Start FastAPI Backend
Write-Host "Starting FastAPI Backend..."
Start-Process -NoNewWindow -FilePath $VENV_UVICORN -ArgumentList "backend.main:app", "--reload"

# Start Streamlit Frontend
Write-Host "Starting Streamlit Frontend..."
& $VENV_STREAMLIT run frontend/app.py
