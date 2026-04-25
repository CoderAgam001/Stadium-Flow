# Stadium Flow: Smart AI Rerouting MVP

Welcome to the **Stadium Flow App**, a premium, AI-powered crowd management system designed to optimize fan flow and reduce wait times at major sporting events using real-time predictive analytics and Google Gemini.

This app is an MVP (Minimum Viable Product) that demonstrates the core functionality of the system. 

## Overview

The system consists of three main components:
1.  **Backend Agent (FastAPI):** Manages a SQLite database of stadium zones and hosts a background simulation engine.

2.  **Logic Agent (Gemini AI):** Analyzes occupancy data and generates natural language routing recommendations using Gemini 1.5 Flash.

3.  **Frontend Agent (Streamlit):** A role-based dashboard separating Admin analytics from Guest/Fan navigation.

---

## 🚀 Quick Start (Windows)

To make it as easy as possible for a third person to review the project, I have included one-click scripts for setup and execution.

### 1. One-Click Setup
Open PowerShell in the project root and run:
```powershell
./setup.ps1
```
*This script will create the virtual environment, install all dependencies, initialize the database, and create a template `.env` file.*

### 2. Configure AI
Open the newly created `.env` file and add your Google Gemini API Key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run the App
Once setup is complete, launch the entire stack with:
```powershell
./run.ps1
```

---

## 🛠️ Manual Installation (Optional)
If you prefer to set up the environment manually:
1. **Create Venv**: `python -m venv .venv`
2. **Install Deps**: `pip install -r requirements.txt`
3. **Init DB**: `python backend/setup_db.py`

---

## Features & User Roles

To ensure a streamlined, progressive experience, the app separates technical analytics from consumer usage.

### Fan View (Guest)
*   **No Login Required:** Fans land directly on a simplified, frictionless navigation screen.

*   **Location Selection:** Fans select their current stand or washroom location.

*   **AI Smart Rerouting:** The engine analyzes crowd patterns and instantly outputs the optimal path visually, without confusing jargon.

### Admin Dashboard (Secured)
*   **Login Access:** Click "Login as Admin" in the top right corner. 
    *   **Username:** `admin`
    *   **Password:** `admin`
    
    *Note: these credentials are for the **MVP only** and future versions will have proper authentication as well as authorization.*

*   **Predictive Logging:** A dedicated sidebar tracks historical occupancy trends for the AI to analyze.

*   **Critical Alerts:** The system flags any zone exceeding 90% capacity.

*   **Raw Data Access:** Admins can expand the raw dataframe to see exact occupancy vs capacity metrics.

---

## ☁️ Cloud Deployment (Google Cloud Run)

This project is Docker-ready for deployment to Google Cloud Run.

### 1. Build the Image
Build and push your container to Google Container Registry (replace `PROJECT_ID` with your actual project id):
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/stadium-flow-ai
```

### 2. Deploy to Cloud Run
Launch the service with your Gemini API key:
```bash
gcloud run deploy stadium-flow-ai \
    --image gcr.io/PROJECT_ID/stadium-flow-ai \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="GEMINI_API_KEY=your_actual_key_here"
```

---

## System Architecture

*   **Database:** `stadium_flow.db` (SQLite) with an `occupancy_logs` table for trend tracking.
*   **Simulation Engine:** `sim_engine.py` (Randomly updates occupancy and logs data every 10 seconds).
*   **AI Engine:** `google-genai` (Gemini 2.5 Flash).
*   **Theme:** Premium, custom-styled Black aesthetic with dynamic CSS components.

---

[*Built with Google Gemini & Antigravity as part of the "Build With AI" series*](https://developers.google.com/community/build-with-ai)

## References
* [Streamlit](https://streamlit.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Gemini AI](https://ai.google.dev/gemini-api)
