import requests
from datetime import datetime

def fetch_neo_count(api_key):
    today = datetime.now().strftime("%Y-%m-%d")
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {"start_date": today, "end_date": today, "api_key": api_key}
    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        return sum(len(data["near_earth_objects"][date]) for date in data["near_earth_objects"])
    except:
        return "N/A"
