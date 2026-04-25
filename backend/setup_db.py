import sqlite3
import os

DB_PATH = 'stadium_flow.db'

def setup_database():
    # Remove existing db for clean setup during MVP iteration
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create zones table
    cursor.execute('''
        CREATE TABLE zones (
            zone_id INTEGER PRIMARY KEY,
            zone_name TEXT NOT NULL,
            current_occupancy INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            x_coordinate FLOAT NOT NULL,
            y_coordinate FLOAT NOT NULL
        )
    ''')

    # Initial data for 5 zones
    zones_data = [
        (1, 'North Stand Washroom', 0, 100, 0.0, 100.0),
        (2, 'South Stand Washroom', 0, 120, 0.0, -100.0),
        (3, 'East Stand Concessions', 0, 200, 100.0, 0.0),
        (4, 'West Stand Concessions', 0, 150, -100.0, 0.0),
        (5, 'Central Pavilion', 0, 300, 0.0, 0.0)
    ]

    cursor.executemany('''
        INSERT INTO zones (zone_id, zone_name, current_occupancy, capacity, x_coordinate, y_coordinate)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', zones_data)

    conn.commit()
    conn.close()
    print(f"Database {DB_PATH} initialized successfully with 5 zones.")

if __name__ == "__main__":
    setup_database()
