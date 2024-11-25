import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QGridLayout, QPushButton, QTextEdit, QListWidget
from PyQt6 import uic
from PyQt6.uic import loadUi
import urllib.request
import json
import ssl
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("resources/env/tankerkoenig.env")

# Retrieve credentials
apikey = os.getenv('API_KEY')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Abfragen der Tankerkoenig API.
# https://creativecommons.tankerkoenig.de/

home = "https://creativecommons.tankerkoenig.de/json/"
func = "list.php?"
lat = 51.3765096 
lon = 7.6960842
#rad = 40


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("Benzinpreis App")
        self.setGeometry(200, 200, 400, 600)
        #self.initUI()
        loadUi("resources/ui/mainWindow.ui", self) 
        self.apply_stylesheet()
        
        self.radius_input.setPlaceholderText("Suchradius in km (z. B. 5)")

        # Button
        self.search_button.clicked.connect(self.search_stations)

        # Ausgabe
        #self.result_output.setReadOnly(True)
    def apply_stylesheet(self):
        with open("resources/stylesheets/lightStyle.qss", "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def search_stations(self):
        # Nur den Radius aus dem Eingabefeld holen
        rad = self.radius_input.text()
        loca = f"lat={lat}&lng={lon}&rad={rad}"
        opti = "&sort=price&type=diesel&apikey="

        url = home + func + loca + opti + apikey
        html = urllib.request.urlopen(url, context=ctx).read()
        data = json.loads(html)
        if not rad:
            self.station_list.addItem("Bitte den Radius eingeben.")
            return
        
        try:
            # Tankstellen-Daten abrufen
            loca = f"lat={lat}&lng={lon}&rad={rad}"
            opti = f"&sort=price&type=diesel&apikey={apikey}"
            url = home + func + loca + opti
            html = urllib.request.urlopen(url, context=ctx).read()
            data = json.loads(html)

            # Ergebnisse in der ListBox anzeigen
            self.station_list.clear()
            if 'stations' not in data:
                self.station_list.addItem("Keine Tankstellen gefunden.")
                return

            for ts in data['stations']:
                station_info = f"{ts['place']}, {ts['street']} {ts['houseNumber']}: {ts['name']}"
                self.station_list.addItem(station_info)

        except Exception as e:
            self.station_list.clear()
            self.station_list.addItem(f"Fehler beim Abrufen der Daten: {e}")
            print(f"Error: {e}")  # Print the error for debugging