import os
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# -------- Environment Variables --------
ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV").upper()
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
MONGO_URI = os.getenv("MONGO_URI")

# -------- Environment → Database Mapping --------
DB_MAP = {
    "DEV": "email_automation_dev",
    "STAG": "email_automation_stag",
    "PROD": "email_automation_prod"
}

DB_NAME = DB_MAP.get(ENVIRONMENT, "email_automation_dev")

# -------- MongoDB Connection --------
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = mongo_client[DB_NAME]
    mongo_client.admin.command("ping")
    MONGO_STATUS = "connected"
except Exception as e:
    print("MongoDB connection error:", e)
    MONGO_STATUS = "connection_failed"

# -------- Routes --------
@app.route("/")
def home():
    return jsonify({
        "message": "Hello from DevOps Python App 🚀",
        "environment": ENVIRONMENT,
        "log_level": LOG_LEVEL,
        "database": DB_NAME,
        "mongo_status": MONGO_STATUS
    })

@app.route("/health")
def health():
    try:
        mongo_client.admin.command("ping")
        db_status = "UP"
    except Exception:
        db_status = "DOWN"

    return jsonify({
        "status": "UP",
        "environment": ENVIRONMENT,
        "database": DB_NAME,
        "db_status": db_status
    })

# -------- App Runner --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
