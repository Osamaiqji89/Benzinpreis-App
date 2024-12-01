import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QGridLayout, QPushButton, QTextEdit, QListWidget
from PyQt6.QtCore import QUrl
from PyQt6 import uic
import os
from PyQt6.uic import loadUi
from dotenv import load_dotenv
import folium
from PyQt6.QtWebEngineWidgets import QWebEngineView
from geopy.geocoders import Nominatim
from LocationService import LocationService
from StationDataFetcher import StationDataFetcher
from MapManager import MapManager
from UIHelper import UIHelper
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        loadUi("resources/ui/mainWindow.ui", self)
        load_dotenv("resources/env/tankerkoenig.env")
        
        self.setWindowTitle("Benzinpreis App")
        self.setGeometry(200, 200, 1200, 800)
        self.api_key = os.getenv("API_KEY")
        self.radius = 5
        self.fetcher = StationDataFetcher(self.api_key)
        self.location_service = LocationService()
        self.map_view = QWebEngineView()
        self.gridLayout_3.addWidget(self.map_view)
        self.map_manager = MapManager(self.map_view)
        self.setup_connectiions()
        self.setup_ui()

    def setup_ui(self):
        header = self.station_Table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.btnDiesel.setChecked(True)
        UIHelper.apply_stylesheet(self, "resources/stylesheets/lightStyle.qss")
        self.go_to_my_location()

    def setup_connectiions(self):
        self.horiSliderRadius.valueChanged.connect(self.update_radius)
        self.search_button.clicked.connect(self.go_to_my_location)
        self.edtSearch.returnPressed.connect(self.search_stations_by_city_or_zip)
        self.btnDiesel.clicked.connect(self.on_Diesele_clicked)
        self.btnSuperE10.clicked.connect(self.on_SuperE10_clicked)
        self.btnSuperPlus.clicked.connect(self.on_SuperPlus_clicked)

    def update_radius(self):
        self.radius = self.horiSliderRadius.value()
        lat, lon = self.location_service.get_lat_lon()
        self.load_stations_and_map(lat, lon, self.radius)
        self.lblRadius.setText(f"Suchradius: {self.radius} km")

    def go_to_my_location(self):
        lat, lon = self.location_service.get_location_by_ip()
        self.radius = self.horiSliderRadius.value()
        self.load_stations_and_map(lat, lon, self.radius)
        self.lblRadius.setText(f"Suchradius: {self.radius} km")

    def search_stations_by_city_or_zip(self):
        city_or_zip = self.edtSearch.text().strip()
        lat, lon = self.location_service.lon_lat_city(city_or_zip)
        self.load_stations_and_map(lat, lon, self.radius)

    def load_stations_and_map(self, lat, lon, rad):
        fuel_type = self.get_fuel_type()
        stations = self.fetcher.fetch_stations(lat, lon, fuel_type, rad)
        UIHelper.populate_station_table(self.station_Table, stations)
        self.map_manager.create_map(stations, lat, lon, rad)

    def get_fuel_type(self):
        if self.btnDiesel.isChecked():
            return "diesel"
        elif self.btnSuperE10.isChecked():
            return "e10"
        elif self.btnSuperPlus.isChecked():
            return "e5"
        else:
            return None

    def on_Diesele_clicked(self):
        lat, lon = self.location_service.get_lat_lon()
        self.load_stations_and_map(lat, lon, self.radius)
        self.btnDiesel.setChecked(True)
        self.btnSuperE10.setChecked(False)
        self.btnSuperPlus.setChecked(False)

    def on_SuperE10_clicked(self):
        lat, lon = self.location_service.get_lat_lon()
        self.load_stations_and_map(lat, lon, self.radius)
        self.btnDiesel.setChecked(False)
        self.btnSuperE10.setChecked(True)
        self.btnSuperPlus.setChecked(False)

    def on_SuperPlus_clicked(self):
        lat, lon = self.location_service.get_lat_lon()
        self.load_stations_and_map(lat, lon, self.radius)
        self.btnDiesel.setChecked(False)
        self.btnSuperE10.setChecked(False)
        self.btnSuperPlus.setChecked(True)