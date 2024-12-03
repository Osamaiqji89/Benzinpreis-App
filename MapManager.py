import folium

class MapManager:
    def __init__(self, map_view):
        self.map_view = map_view

    def create_map(self, stations, lat, lon, rad):
        map_center = [lat, lon]
        my_map = folium.Map(location=map_center, zoom_start=13 - (rad / 8))
        for station in stations:
            # Style für Popup
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
        my_map.save("resources/map/map.html")
        self.map_view.setHtml(my_map.get_root().render())
