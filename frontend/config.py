import os
from dotenv import load_dotenv

load_dotenv()

# API
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Security
ADMIN_USERNAME = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASS", "admin")

# App Settings
APP_TITLE = "Stadium Flow"
CACHE_TTL = 5  # seconds
CROWD_ALERT_THRESHOLD = 90  # percentage
