import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_PATH = 'stadium_flow.db'

# AI Model
GEMINI_MODEL = 'gemini-2.5-flash'

# Thresholds
CROWD_ALERT_THRESHOLD = 0.9  # 90%
CROWD_BUSY_THRESHOLD = 0.8   # 80%
