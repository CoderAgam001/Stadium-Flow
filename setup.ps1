# Stadium Flow: One-Click Installation Script (Windows)

Write-Host "--- 🏟️ Stadium Flow Setup ---" -ForegroundColor Cyan

# 1. Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python is not installed or not in PATH." -ForegroundColor Red
    exit
}

# 2. Create Virtual Environment
if (!(Test-Path ".venv")) {
    Write-Host "📦 Creating Virtual Environment..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "✅ Virtual Environment already exists." -ForegroundColor Green
}

# 3. Install Dependencies
Write-Host "📥 Installing dependencies from requirements.txt..." -ForegroundColor Yellow
& .venv/Scripts/python.exe -m pip install --upgrade pip
& .venv/Scripts/python.exe -m pip install -r requirements.txt

# 4. Check for .env file
if (!(Test-Path ".env")) {
    Write-Host "⚠️ Warning: .env file not found." -ForegroundColor Magenta
    Write-Host "Creating a template .env file. Please add your GEMINI_API_KEY to it." -ForegroundColor White
    "GEMINI_API_KEY=your_key_here`nAPI_URL=http://localhost:8000" | Out-File -FilePath .env -Encoding utf8
} else {
    Write-Host "✅ .env file found." -ForegroundColor Green
}

# 5. Initialize Database
Write-Host "🗄️ Initializing Stadium Database..." -ForegroundColor Yellow
& .venv/Scripts/python.exe backend/setup_db.py

Write-Host "`n✨ Setup Complete! ✨" -ForegroundColor Green
Write-Host "To start the application, simply run: ./run.ps1" -ForegroundColor Cyan
