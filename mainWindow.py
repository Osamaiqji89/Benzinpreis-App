import os
from PyQt6.uic import loadUi
from dotenv import load_dotenv
from PyQt6.QtWebEngineWidgets import QWebEngineView
from LocationService import LocationService
from StationDataFetcher import StationDataFetcher
from MapManager import MapManager
from UIHelper import UIHelper
from PyQt6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, 
    QGridLayout, QTableWidget, QToolButton, QSlider, QLineEdit, QLabel)
from PyQt6.QtGui import QIcon
class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        ## UI Elements from QT Designer see --> resources/ui/mainWindow.ui
        self.gridLayout_3: QGridLayout
        self.station_Table: QTableWidget
        self.btnDiesel: QToolButton
        self.horiSliderRadius: QSlider
        self.search_button: QToolButton
        self.edtSearch: QLineEdit
        self.btnSuperE10: QToolButton
        self.btnSuperPlus: QToolButton
        self.lblRadius: QLabel

        loadUi("resources/ui/mainWindow.ui", self)
        load_dotenv("resources/env/tankerkoenig.env")
        
        self.setWindowTitle("Benzinpreis App")
        self.setWindowIcon(QIcon("resources/icons/station.ico"))
        self.setGeometry(200, 200, 1200, 800)
        self.api_key = os.getenv("API_KEY")
        self.radius = 5
        self.fetcher = StationDataFetcher(self.api_key)
        self.location_service = LocationService()
        self.map_view: QWebEngineView = QWebEngineView()
        self.gridLayout_3.addWidget(self.map_view)
        self.map_manager = MapManager(self.map_view)
        self.setup_connectiions()
        self.setup_ui()

    def setup_ui(self):
        header = self.station_Table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.btnDiesel.setChecked(True)
        self.stackedWidget.setCurrentIndex(0)
        UIHelper.apply_stylesheet(self, "resources/stylesheets/lightStyle.qss")
        self.go_to_my_location()

    def setup_connectiions(self):
        self.horiSliderRadius.valueChanged.connect(self.update_radius)
        self.search_button.clicked.connect(self.go_to_my_location)
        self.edtSearch.returnPressed.connect(self.search_stations_by_city_or_zip)
        self.btnDiesel.clicked.connect(self.on_Diesele_clicked)
        self.btnSuperE10.clicked.connect(self.on_SuperE10_clicked)
        self.btnSuperPlus.clicked.connect(self.on_SuperPlus_clicked)
        self.station_Table.itemClicked.connect(self.on_station_clicked)
        self.btnBack.clicked.connect(self.on_back_clicked)

    def update_radius(self):
        self.radius = self.horiSliderRadius.value()
        self.reload_stations()
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
        self.btnDiesel.setChecked(True)
        self.btnSuperE10.setChecked(False)
        self.btnSuperPlus.setChecked(False)
        self.reload_stations()

    def on_SuperE10_clicked(self):
        self.btnDiesel.setChecked(False)
        self.btnSuperE10.setChecked(True)
        self.btnSuperPlus.setChecked(False)
        self.reload_stations()

    def on_SuperPlus_clicked(self):
        self.btnDiesel.setChecked(False)
        self.btnSuperE10.setChecked(False)
        self.btnSuperPlus.setChecked(True)
        self.reload_stations()

    def reload_stations(self):
        lat, lon = self.location_service.get_lat_lon()
        self.load_stations_and_map(lat, lon, self.radius)

    def on_station_clicked(self):
        lat, lon = self.location_service.get_lat_lon()
        stations = self.fetcher.fetch_stations(lat, lon, "diesel", self.radius)

        first_station = stations[self.station_Table.currentRow()]
        name = first_station.get("name", "Unbekannt")
        brand = first_station.get("brand", "Unbekannt")
        street = first_station.get("street", "Unbekannt")
        house_number = first_station.get("houseNumber", "Unbekannt")
        post_code = first_station.get("postCode", "Unbekannt")
        post_code = first_station.get("postCode", "Unbekannt")
        city = first_station.get("place", "Unbekannt")
        price = (first_station.get('price', 'N/A'))
        is_open = first_station.get("isOpen", False)
        status_text = f"<span style='color: {'green' if is_open else 'red'};'>{'Geöffnet' if is_open else 'Geschlossen'}</span>"

        self.lblOpen.setText(status_text)
        self.lblStatioName.setText(f"{brand} Tankstelle")
        self.lblAddress.setText(f"{street} {house_number} \n{post_code} {city}")
        self.lblDieselPrice.setText(f"{str(first_station.get('price', 'N/A'))} €")

        for fuel in ["e10", "e5"]:
            stations = self.fetcher.fetch_stations(lat, lon, fuel, self.radius)
            if stations:
                first_station = stations[self.station_Table.currentRow()]
                price = first_station.get('price', 'N/A')
                if fuel == "e10":
                    self.lcdE10.setText(f"{str(price)} €")
                elif fuel == "e5":
                    self.lcdSuperPlus.setText(f"{str(price)} €")

            self.stackedWidget.setCurrentIndex(1)

    def on_back_clicked(self):
        self.stackedWidget.setCurrentIndex(0)