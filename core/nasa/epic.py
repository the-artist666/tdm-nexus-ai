import requests

def fetch_epic_image(api_key):
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": api_key}
    try:
        r = requests.get(url, params=params, timeout=5)
        images = r.json()
        if images:
            img_id = images[0]["identifier"]
            date = img_id.split("T")[0].replace("-", "/")
            return f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/epic_RGB_2048.png?api_key={api_key}"
    except:
        pass
    return "https://api.nasa.gov/images/logo.png"
