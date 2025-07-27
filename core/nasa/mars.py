import requests
import json
import os

CACHE = "data/cache/mars.json"

def fetch_mars_photo(api_key):
    if os.path.exists(CACHE):
        with open(CACHE, 'r') as f:
            return json.load(f).get("img_src", "https://api.nasa.gov/images/logo.png")

    try:
        url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
        params = {"sol": 1000, "camera": "FHAZ", "api_key": api_key}
        r = requests.get(url, params=params, timeout=5)
        photos = r.json().get("photos", [])
        if photos:
            img_url = photos[0]["img_src"]
            with open(CACHE, 'w') as f:
                json.dump({"img_src": img_url}, f)
            return img_url
    except:
        pass
    return "https://api.nasa.gov/images/logo.png"
