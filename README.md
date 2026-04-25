# Stadium Flow: Smart AI Rerouting MVP

Welcome to the **Stadium Flow App**, a premium, AI-powered crowd management system designed to optimize fan flow and reduce wait times at major sporting events using real-time predictive analytics and Google Gemini.

This app is an MVP (Minimum Viable Product) that demonstrates the core functionality of the system. 

## Overview

The system consists of three main components:
1.  **Backend Agent (FastAPI):** Manages a SQLite database of stadium zones and hosts a background simulation engine.
2.  **Logic Agent (Gemini AI):** Analyzes occupancy data and generates natural language routing recommendations using Gemini 1.5 Flash.
3.  **Frontend Agent (Streamlit):** A role-based dashboard separating Admin analytics from Guest/Fan navigation.

---

## Setup Instructions

### 1. Environment Configuration
Ensure you have Python 3.9+ installed. It is recommended to use a virtual environment.

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Gemini API Key
This project requires a Google Gemini API Key.
1.  Create a `.env` file in the root directory (if not already present).
2.  Add your API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

### 3. Database Initialization
The database will automatically initialize when you start the backend, but you can run it manually:
```powershell
python backend/setup_db.py
```

---

## How to Run

You can run the entire system using the provided PowerShell script or manually.

### Option A: Using the Startup Script (Recommended)
```powershell
.\run.ps1
```

### Option B: Manual Startup
**1. Start the FastAPI Backend:**
The simulation engine will automatically start in the background as part of the backend lifespan.
```powershell
python backend/main.py
```

**2. Start the Streamlit Dashboard:**
```powershell
streamlit run frontend/app.py
```

---

## ✨ Features & User Roles

To ensure a streamlined, progressive experience, the app separates technical analytics from consumer usage.

### 🏃 Fan View (Guest)
*   **No Login Required:** Fans land directly on a simplified, frictionless navigation screen.
*   **Location Selection:** Fans select their current stand or washroom location.
*   **AI Smart Rerouting:** The engine analyzes crowd patterns and instantly outputs the optimal path visually, without confusing jargon.

### 📊 Admin Dashboard (Secured)
*   **Login Access:** Click "Login as Admin" in the top right corner. 
    *   **Username:** `admin`
    *   **Password:** `admin`
*   **Predictive Logging:** A dedicated sidebar tracks historical occupancy trends for the AI to analyze.
*   **Critical Alerts:** The system flags any zone exceeding 90% capacity.
*   **Raw Data Access:** Admins can expand the raw dataframe to see exact occupancy vs capacity metrics.

---

## 🏗️ System Architecture

*   **Database:** `stadium_flow.db` (SQLite) with an `occupancy_logs` table for trend tracking.
*   **Simulation Engine:** `sim_engine.py` (Randomly updates occupancy and logs data every 10 seconds).
*   **AI Engine:** `google-genai` (Gemini 1.5 Flash).
*   **Theme:** Premium, custom-styled Black aesthetic with dynamic CSS.

---

[*Built with Google Gemini & Antigravity as part of the "Build With AI" series*](https://developers.google.com/community/build-with-ai)

## References
* [Streamlit](https://streamlit.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Gemini AI](https://ai.google.dev/gemini-api)
