import os
import sqlite3
import math
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types

app = FastAPI(title="Stadium Flow MVP")
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

@app.get("/zones", response_model=List[Zone])
def get_zones():
    conn = get_db_connection()
    zones = conn.execute("SELECT * FROM zones").fetchall()
    conn.close()
    return [dict(z) for z in zones]

@app.get("/get_recommendation/{user_zone_id}")
def get_recommendation(user_zone_id: int):
    conn = get_db_connection()
    zones_rows = conn.execute("SELECT * FROM zones").fetchall()
    conn.close()

    zones = [dict(z) for z in zones_rows]
    user_zone = next((z for z in zones if z['zone_id'] == user_zone_id), None)

    if not user_zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    occupancy_pct = user_zone['current_occupancy'] / user_zone['capacity']

    if occupancy_pct <= 0.8:
        return {"recommendation": f"You are currently at {user_zone['zone_name']}. The area is not too crowded ({(occupancy_pct*100):.1f}% full). No need to relocate!"}

    # If > 80%, find closest zone under 50%
    candidate_zones = [z for z in zones if (z['current_occupancy'] / z['capacity']) < 0.5]

    if not candidate_zones:
        return {"recommendation": f"You are at {user_zone['zone_name']}, which is very crowded. Unfortunately, all other zones are also quite full right now."}

    # Find closest candidate
    closest_zone = None
    min_distance = float('inf')

    for candidate in candidate_zones:
        dist = calculate_distance(
            user_zone['x_coordinate'], user_zone['y_coordinate'],
            candidate['x_coordinate'], candidate['y_coordinate']
        )
        if dist < min_distance:
            min_distance = dist
            closest_zone = candidate

    # Call Gemini to format natural language recommendation
    distance_meters = int(min_distance) # Just treat coordinates as meters for MVP
    
    prompt = f"""
    You are a friendly and helpful predictive queue rerouting assistant for a cricket stadium.
    The user is currently at "{user_zone['zone_name']}" which is very crowded ({user_zone['current_occupancy']} out of {user_zone['capacity']} people).
    The best alternative is "{closest_zone['zone_name']}" which is only {int((closest_zone['current_occupancy']/closest_zone['capacity'])*100)}% full.
    It is approximately {distance_meters} meters away.
    
    Write a brief, friendly 1-2 sentence recommendation telling them their current zone is crowded and they should head to the alternative zone for a shorter wait time.
    """

    recommendation_text = ""
    if gemini_client:
        try:
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            recommendation_text = response.text.strip()
        except Exception as e:
            recommendation_text = f"Error calling Gemini: {e}. Fallback: Head to {closest_zone['zone_name']} ({distance_meters}m away) for shorter waits."
    else:
         recommendation_text = f"GEMINI_API_KEY missing. Fallback: Head to {closest_zone['zone_name']} ({distance_meters}m away) for shorter waits."

    return {
        "recommendation": recommendation_text,
        "current_zone": user_zone['zone_name'],
        "recommended_zone": closest_zone['zone_name'],
        "distance": distance_meters
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
