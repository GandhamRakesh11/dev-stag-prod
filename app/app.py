import os
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
MONGO_URI = os.getenv("MONGO_URI")
PORT = int(os.getenv("PORT", 5000))

DB_MAP = {
    "DEV": "email_automation_dev",
    "STAG": "email_automation_stag",
    "PROD": "email_automation_prod"
}

DB_NAME = DB_MAP.get(ENVIRONMENT, "email_automation_dev")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from DevOps Python App 🚀",
        "environment": ENVIRONMENT,
        "database": DB_NAME
    })

@app.route("/health")
def health():
    try:
        mongo_client.admin.command("ping")
        db_status = "UP"
    except:
        db_status = "DOWN"

    return jsonify({
        "status": "UP",
        "environment": ENVIRONMENT,
        "db_status": db_status
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
