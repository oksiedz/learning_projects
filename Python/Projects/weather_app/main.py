import ssl
import certifi
from urllib.request import urlopen, Request
import json

# Constants
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
PARAMS = {
    "lat": "52.2297",      # Latitude for Warsaw
    "lon": "21.0122",      # Longitude for Warsaw
    "appid": "5d16b03859e9a435449b4671a30af940",
}

# Build the API request URL
urlp = f"{BASE_URL}?{'&'.join(f'{k}={v}' for k, v in PARAMS.items())}"

print("URL:", urlp)
print("Params:", PARAMS)

# Fetch weather data from the API
try:
    req = Request(urlp, headers={"User-Agent": "Python"})
    ctx = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(req, context=ctx)
    if response.status != 200:
        raise Exception(f"Request failed with status code: {response.status}")
    data = json.loads(response.read().decode())

    # Save the data to a file
    with open("weather.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nData saved to weather.json")
    print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print("Error:", e)
