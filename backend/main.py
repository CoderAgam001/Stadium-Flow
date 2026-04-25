import os
import math
import subprocess
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.config import DB_PATH
from backend.db_service import fetch_all_zones, fetch_analytics_logs, fetch_zone_trends
from backend.ai_service import ai_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup db if not exists
    if not os.path.exists(DB_PATH):
        subprocess.run(["python", "backend/setup_db.py"])
    
    # Start sim_engine as background process
    sim_process = subprocess.Popen(["python", "backend/sim_engine.py"])
    
    try:
        yield
    finally:
        # Suggestion 6: Ensure process is killed reliably
        sim_process.terminate()
        try:
            sim_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            sim_process.kill()

app = FastAPI(title="Stadium Flow MVP", lifespan=lifespan)

class Zone(BaseModel):
    zone_id: int
    zone_name: str
    current_occupancy: int
    capacity: int
    x_coordinate: float
    y_coordinate: float

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

@app.get("/zones", response_model=List[Zone])
def get_zones():
    return fetch_all_zones()

@app.get("/analytics")
def get_analytics():
    return fetch_analytics_logs()

@app.get("/get_recommendation/{user_zone_id}/{dest_zone_id}")
def get_recommendation(user_zone_id: int, dest_zone_id: int):
    zones = fetch_all_zones()
    
    user_zone = next((z for z in zones if z['zone_id'] == user_zone_id), None)
    dest_zone = next((z for z in zones if z['zone_id'] == dest_zone_id), None)

    if not user_zone or not dest_zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    dist_to_dest = int(calculate_distance(user_zone['x_coordinate'], user_zone['y_coordinate'], dest_zone['x_coordinate'], dest_zone['y_coordinate']))
    
    # Get trends for AI context
    zone_ids = [z['zone_id'] for z in zones]
    trends = fetch_zone_trends(zone_ids)
    
    stadium_context = []
    for z in zones:
        stadium_context.append({
            "name": z["zone_name"],
            "occupancy": f"{z['current_occupancy']}/{z['capacity']}",
            "trend": trends.get(z['zone_id'], "stable")
        })

    # Suggestion 8: Use AI service with structured output
    ai_result = ai_service.get_structured_recommendation(
        user_zone, dest_zone, stadium_context, trends, dist_to_dest
    )
    
    return {
        "recommendation": ai_result.recommendation,
        "key_note": ai_result.key_note,
        "distance": ai_result.distance,
        "current_zone": user_zone['zone_name'],
        "dest_zone": dest_zone['zone_name']
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
