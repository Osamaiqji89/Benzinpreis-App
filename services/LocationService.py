from geopy.geocoders import Nominatim
import requests
from utils.StatusLogger import StatusLogger


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
            #print(f"Standort konnte nicht abgerufen werden: {e}")
            StatusLogger.error(f"Standort konnte nicht abgerufen werden: {e}")
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
        try:
            StatusLogger.log("Fetching location...")
            return self.lat, self.lon
        except Exception as e:
            StatusLogger.error(f"Location error: {e}")

    def get_postal_code(self, lat, lon):
        """
        Get postal code from coordinates using reverse geocoding
        Args:
            lat: latitude
            lon: longitude
        Returns:
            str: postal code or None if not found
        """
        try:
            geolocator = Nominatim(user_agent="MyApp")
            location = geolocator.reverse((lat, lon), language="de")
            if location and location.raw.get('address'):
                return location.raw['address'].get('postcode')
            return None
        except Exception as e:
            #print(f"Error getting postal code: {e}")
            StatusLogger.error(f"Error getting postal code: {e}")
            return None