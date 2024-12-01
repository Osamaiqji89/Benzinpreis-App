from geopy.geocoders import Nominatim
import requests


class LocationService:
    def __init__(self):
        self.name = ""
        self.lon = 0.0
        self.lat = 0.0

    def get_location_by_ip(self):
        try:
            response = requests.get("https://ipinfo.io", timeout=5)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            ip_data = response.json()
            self.lat, self.lon = map(float, ip_data["loc"].split(","))
        except requests.exceptions.RequestException as e:
            print(f"Standort konnte nicht abgerufen werden: {e}")
            self.lat, self.lon = 51.3765096, 7.6960842  # Fallback auf Standardkoordinaten
        return self.lat, self.lon

    def lon_lat_city(self, cityName):
        self.name = cityName
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(cityName, country_codes="de")
        if not location:
            raise Exception("Wrong city name", 404)
        self.lat = location.latitude
        self.lon = location.longitude
        return self.get_lat_lon()

    def get_lat_lon(self):
        return self.lat, self.lon