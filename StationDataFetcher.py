import urllib.request
import json
import ssl


class StationDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://creativecommons.tankerkoenig.de/json/"
        self.func = "list.php?"

    def fetch_stations(self, lat, lon, fuel_type, radius):
        try:
            loca = f"lat={lat}&lng={lon}&rad={radius}"
            opti = "&sort=price&type="+fuel_type+"&apikey="
            url = (
                f"{self.base_url}{self.func}lat={lat}&lng={lon}&rad={radius}"
                f"&sort=price&type={fuel_type}&apikey={self.api_key}"
            )
            response = urllib.request.urlopen(url, context=ssl.create_default_context())
            data = json.loads(response.read())
            return data.get("stations", [])
        except Exception as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return []
        
