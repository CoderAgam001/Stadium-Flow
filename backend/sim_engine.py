import sqlite3
import time
import random
import os

DB_PATH = 'stadium_flow.db'

def run_simulation():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. Please run setup_db.py first.")
        return

    print("Starting simulation engine... Updating occupancies every 10 seconds. Press Ctrl+C to stop.")
    
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT zone_id, current_occupancy, capacity FROM zones")
            zones = cursor.fetchall()
            
            for zone_id, current_occ, capacity in zones:
                # Randomly change occupancy by -15% to +15% of capacity
                change = int(capacity * random.uniform(-0.15, 0.15))
                new_occ = current_occ + change
                
                # Keep within bounds
                new_occ = max(0, min(new_occ, capacity))
                
                cursor.execute(
                    "UPDATE zones SET current_occupancy = ? WHERE zone_id = ?",
                    (new_occ, zone_id)
                )

                # Record log for prediction
                cursor.execute(
                    "INSERT INTO occupancy_logs (zone_id, occupancy) VALUES (?, ?)",
                    (zone_id, new_occ)
                )
            
            conn.commit()
            conn.close()
            print(f"[{time.strftime('%H:%M:%S')}] Updated zone occupancies.")
            
        except Exception as e:
            print(f"Error during simulation update: {e}")
            
        time.sleep(10)

if __name__ == "__main__":
    run_simulation()
