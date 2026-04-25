# 🏟️ Stadium Flow: Predictive Queue Rerouting MVP

Welcome to the **Stadium Flow MVP**, a predictive crowd management system designed for cricket stadiums. This system uses real-time simulation and AI-powered recommendations to guide fans to less crowded zones, ensuring a seamless stadium experience.

## 🚀 Overview

The system consists of three main components:
1.  **Backend Agent (FastAPI):** Manages a SQLite database of stadium zones and hosts a background simulation engine.
2.  **Logic Agent (Gemini AI):** Analyzes occupancy data and generates natural language routing recommendations using Gemini 1.5 Flash.
3.  **Frontend Agent (Streamlit):** A dual-view dashboard for Admins (real-time monitoring) and Fans (personalized routing).

---

## 🛠️ Setup Instructions

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

## 🏃 How to Run

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

## 📊 Features

### Admin View
*   **Real-time Monitoring:** A "Premier League" themed bar chart showing occupancy percentages across all stadium zones.
*   **Data Table:** Detailed breakdown of current occupancy vs. total capacity.

### Fan View
*   **Location Selection:** Fans select their current stand or washroom location.
*   **Smart Rerouting:** If the current zone is >80% full, the "Find Shortest Path" engine finds the nearest zone with <50% occupancy.
*   **AI Recommendations:** Generates human-friendly guidance (e.g., *"East Stand is crowded. Head 150m North to the Central Pavilion for zero wait time."*)

---

## 🏗️ System Architecture

*   **Database:** `stadium_flow.db` (SQLite)
*   **Simulation Engine:** `sim_engine.py` (Randomly updates occupancy every 10 seconds).
*   **AI Engine:** `google-genai` (Gemini 1.5 Flash).
*   **Theme:** Professional "Premier League" Red/White aesthetic.

---

*Developed as a Predictive Stadium Queue Rerouting MVP.*
