import urllib.request
import json
import ssl
from utils.StatusLogger import StatusLogger
from services.FuelPriceDB import FuelPriceDB

class StationDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://creativecommons.tankerkoenig.de/json/"
        self.func = "list.php?"

    def fetch_stations(self, lat, lon, fuel_type, radius, isFavorites):
        """ Fetch stations from Tankerkönig API """
        try:
            StatusLogger.log(f"Fetching stations: lat={lat}, lon={lon}, fuel={fuel_type}, radius={radius}")
            
            loca = f"lat={lat}&lng={lon}&rad={radius}"
            opti = "&sort=price&type="+fuel_type+"&apikey="
            url = (self.base_url + self.func + loca + opti + self.api_key)
            
            response = urllib.request.urlopen(url, context=ssl.create_default_context())
            data = json.loads(response.read())
            
            stations = data.get("stations", [])
            StatusLogger.success(f"Found {len(stations)} stations")
            if isFavorites:
                favorite_stations = []
                for station in stations:
                    if FuelPriceDB().is_favorite(station['id']):
                        favorite_stations.append(station)
                return favorite_stations
            else:
                return stations
        except Exception as e:
            StatusLogger.error(f"Fehler beim Abrufen der Daten: {e}")
            return []