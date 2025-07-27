import requests

def fetch_exoplanet_count():
    url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"
    params = {"table": "exoplanets", "format": "json", "select": "count(*)"}
    try:
        r = requests.get(url, params=params, timeout=5)
        return r.json()[0]["count(*)"]
    except:
        return "N/A"
