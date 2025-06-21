import folium
from PyQt6.QtWebEngineWidgets import QWebEngineView
from utils.StatusLogger import StatusLogger
from services.FuelPriceDB import FuelPriceDB
from utils.path_utils import resource_path
class MapManager:
    def __init__(self, map_view: QWebEngineView):
        self.map_view: QWebEngineView = map_view

    def create_map(self, stations, lat, lon, rad):
        try:
            StatusLogger.log(f"Loading map for coordinates: {lat}, {lon}")
            map_center = [lat, lon]
            my_map = folium.Map(location=map_center, zoom_start=13)
            # Dynamisch die Kartenbegrenzungen basierend auf dem Radius festlegen
            lat_offset = rad / 111.0  # 1° Breitengrad entspricht ca. 111 km
            lon_offset = rad / (111.0 * abs(lat))  # Berücksichtigt Breitenabhängigkeit
            bounds = [
                [lat - lat_offset, lon - lon_offset],  # Südwest-Ecke
                [lat + lat_offset, lon + lon_offset],  # Nordost-Ecke
            ]
            my_map.fit_bounds(bounds)
            my_map.options["maxBounds"] = bounds
            for station in stations:
                popup_html = f"""
                    <div style="font-size:14px; font-weight:bold; color:darkblue;">
                        <p>{station['name']}</p>
                        <p>Preis: <span style="color:green;">{station['price']} €</span></p>
                    </div>
                """
                # Style für Tooltip
                tooltip_html = f"""
                    <div style="font-size:12px; color:darkblue;">
                        {station['name']}
                    </div>
                """
                folium.Marker(
                    location=[station["lat"], station["lng"]],
                    popup=folium.Popup(popup_html, max_width=250),  # Popup mit HTML-Inhalt
                    tooltip=tooltip_html,  # Tooltip mit HTML-Inhalt
                ).add_to(my_map)
            my_map.save(resource_path("resources/map/map.html"))
            self.map_view.setHtml(my_map.get_root().render())
            StatusLogger.success(f"Map loaded with {len(stations)} stations")
        except Exception as e:
            StatusLogger.error(f"Map loading error: {e}")
