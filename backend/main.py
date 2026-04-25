import os
import sqlite3
import math
import subprocess
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup db if not exists
    if not os.path.exists(DB_PATH):
        subprocess.run(["python", "backend/setup_db.py"])
    
    # Start sim_engine as background process
    sim_process = subprocess.Popen(["python", "backend/sim_engine.py"])
    yield
    sim_process.terminate()
    
app = FastAPI(title="Stadium Flow MVP", lifespan=lifespan)
DB_PATH = 'stadium_flow.db'

# Initialize Gemini Client
# It will automatically look for GEMINI_API_KEY in the environment
try:
    gemini_client = genai.Client()
except Exception as e:
    print(f"Warning: Failed to initialize Gemini Client. Make sure GEMINI_API_KEY is set. Error: {e}")
    gemini_client = None

class Zone(BaseModel):
    zone_id: int
    zone_name: str
    current_occupancy: int
    capacity: int
    x_coordinate: float
    y_coordinate: float

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_direction(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return "nearby"
    if abs(dx) > abs(dy):
        return "East" if dx > 0 else "West"
    else:
        return "North" if dy > 0 else "South"

@app.get("/zones", response_model=List[Zone])
def get_zones():
    conn = get_db_connection()
    zones = conn.execute("SELECT * FROM zones").fetchall()
    conn.close()
    return [dict(z) for z in zones]

@app.get("/analytics")
def get_analytics():
    conn = get_db_connection()
    # Get last 10 logs for each zone to show trends
    logs = conn.execute("""
        SELECT z.zone_name, l.occupancy, l.timestamp 
        FROM occupancy_logs l 
        JOIN zones z ON l.zone_id = z.zone_id 
        ORDER BY l.timestamp DESC 
        LIMIT 50
    """).fetchall()
    conn.close()
    return [dict(l) for l in logs]

@app.get("/get_recommendation/{user_zone_id}")
def get_recommendation(user_zone_id: int):
    conn = get_db_connection()
    zones_rows = conn.execute("SELECT * FROM zones").fetchall()
    
    # Calculate trends (simple linear trend from last 5 logs)
    trends = {}
    for zone in zones_rows:
        z_id = zone['zone_id']
        logs = conn.execute(
            "SELECT occupancy FROM occupancy_logs WHERE zone_id = ? ORDER BY timestamp DESC LIMIT 5",
            (z_id,)
        ).fetchall()
        if len(logs) >= 2:
            diff = logs[0][0] - logs[-1][0]
            trends[z_id] = "increasing" if diff > 0 else "decreasing" if diff < 0 else "stable"
        else:
            trends[z_id] = "stable"
    
    conn.close()

    zones = [dict(z) for z in zones_rows]
    user_zone = next((z for z in zones if z['zone_id'] == user_zone_id), None)

    if not user_zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    occupancy_pct = user_zone['current_occupancy'] / user_zone['capacity']
    
    # Context for Gemini
    stadium_context = []
    for z in zones:
        stadium_context.append({
            "name": z["zone_name"],
            "occupancy": f"{z['current_occupancy']}/{z['capacity']}",
            "trend": trends.get(z['zone_id'], "stable"),
            "distance_from_user": int(calculate_distance(user_zone['x_coordinate'], user_zone['y_coordinate'], z['x_coordinate'], z['y_coordinate']))
        })

    prompt = f"""
    You are an AI Crowd Controller for a Cricket Stadium.
    User Location: {user_zone['zone_name']} (Current: {user_zone['current_occupancy']}/{user_zone['capacity']}, Trend: {trends.get(user_zone_id, 'stable')})
    
    Stadium State:
    {stadium_context}
    
    TASK:
    1. Analyze if the user's current zone is getting too crowded (>80% or high increasing trend).
    2. If yes, pick the BEST alternative zone. Consider distance, current occupancy, AND trend (avoid zones with fast increasing trends).
    3. Write a friendly, 2-sentence recommendation. Mention the "predicted" state if a trend is high.
    
    Format:
    Recommendation: [Your text]
    Target Zone: [Name of recommended zone or 'None']
    Distance: [Distance in meters or 0]
    """

    recommendation_text = "Standard routing logic applies. Stay put or check nearby zones."
    target_zone = "None"
    dist = 0

    if gemini_client:
        try:
            response = gemini_client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            # Simple parsing for the MVP
            text = response.text
            recommendation_text = text.split("Recommendation:")[1].split("Target Zone:")[0].strip() if "Recommendation:" in text else text
            if "Target Zone:" in text:
                target_zone = text.split("Target Zone:")[1].split("Distance:")[0].strip()
            if "Distance:" in text:
                try:
                    dist = int(text.split("Distance:")[1].strip().split(" ")[0])
                except:
                    dist = 0
        except Exception as e:
            recommendation_text = f"AI Routing Error: {e}. Fallback: Head to Pavilion."
    
    return {
        "recommendation": recommendation_text,
        "current_zone": user_zone['zone_name'],
        "recommended_zone": target_zone,
        "distance": dist
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
