import folium

class MapManager:
    def __init__(self, map_view):
        self.map_view = map_view

    def create_map(self, stations, lat, lon, rad):
        map_center = [lat, lon]
        my_map = folium.Map(location=map_center, zoom_start=13 - (rad / 8))
        for station in stations:
            folium.Marker(
                location=[station["lat"], station["lng"]],
                popup=f"{station['name']}<br>Preis: {station['price']} €",
                tooltip=station["name"],
            ).add_to(my_map)
        my_map.save("resources/map/map.html")
        self.map_view.setHtml(my_map.get_root().render())