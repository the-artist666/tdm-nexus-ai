import requests
import json
import os
from datetime import datetime

CACHE = "data/cache/apod.json"

def fetch_apod(api_key):
    if os.path.exists(CACHE):
        with open(CACHE, 'r') as f:
            data = json.load(f)
            if (datetime.now() - datetime.fromisoformat(data["timestamp"])) < datetime.timedelta(hours=24):
                return data["data"]

    try:
        url = "https://api.nasa.gov/planetary/apod"
        params = {"api_key": api_key, "thumbs": True}
        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        os.makedirs("data/cache", exist_ok=True)
        with open(CACHE, 'w') as f:
            json.dump({"timestamp": datetime.now().isoformat(), "data": data}, f)
        return data
    except:
        return {
            "title": "TDM Nexus AI",
            "url": "https://api.nasa.gov/images/logo.png",
            "explanation": "Time-Field Dark Matter v4.0"
        }
