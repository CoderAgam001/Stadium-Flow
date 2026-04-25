import sqlite3
from backend.config import DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_zones():
    conn = get_db_connection()
    zones = conn.execute("SELECT * FROM zones").fetchall()
    conn.close()
    return [dict(z) for z in zones]

def fetch_analytics_logs(limit=50):
    conn = get_db_connection()
    logs = conn.execute(
        """
        SELECT z.zone_name, l.occupancy, l.timestamp 
        FROM occupancy_logs l 
        JOIN zones z ON l.zone_id = z.zone_id 
        ORDER BY l.timestamp DESC 
        LIMIT ?
        """, (limit,)
    ).fetchall()
    conn.close()
    return [dict(l) for l in logs]

def fetch_zone_trends(zone_ids, limit=5):
    conn = get_db_connection()
    trends = {}
    for z_id in zone_ids:
        logs = conn.execute(
            "SELECT occupancy FROM occupancy_logs WHERE zone_id = ? ORDER BY timestamp DESC LIMIT ?",
            (z_id, limit)
        ).fetchall()
        
        if len(logs) >= 2:
            diff = logs[0][0] - logs[-1][0]
            trends[z_id] = "increasing" if diff > 0 else "decreasing" if diff < 0 else "stable"
        else:
            trends[z_id] = "stable"
    conn.close()
    return trends
