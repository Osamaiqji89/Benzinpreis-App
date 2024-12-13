import os
import uuid
from PyQt6.uic import loadUi
from dotenv import load_dotenv
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, 
    QGridLayout, QTableWidget, QToolButton, QSlider, QLineEdit, QLabel, QWidget, QVBoxLayout, QSizePolicy,
    QPushButton, QCheckBox, QSpinBox)
from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtCore import Qt, QByteArray, QTimer
from services.StationDataFetcher import StationDataFetcher
from services.FuelPriceDB import FuelPriceDB
from services.LocationService import LocationService
from utils.MapManager import MapManager
from utils.UIHelper import UIHelper
from utils.History import History
from utils.StatusLogger import StatusLogger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))



class MainWindow(QMainWindow):
    _status_bar = None

    @classmethod
    def update_status_bar(cls, message, duration=5000):
        """
        Update the status bar from any class or method
        
        :param message: Message to display
        :param duration: How long to show the message (milliseconds)
        """
        if cls._status_bar:
            cls._status_bar.showMessage(str(message), duration)

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
        self.btnBackToStations: QToolButton
        self.btnBackToHome: QToolButton
        self.btnHistory: QToolButton
        self.btnCountry: QToolButton
        self.btnCity: QToolButton
        self.btnAddToFavorites: QToolButton
        self.btnFavorites: QToolButton
        self.spBoxRadius: QSpinBox
        loadUi("resources/ui/mainWindow.ui", self)
        load_dotenv("resources/env/tankerkoenig.env")
        self.setWindowTitle("Benzinpreis App")
        self.setWindowIcon(QIcon("resources/icons/station.ico"))
        self.setGeometry(200, 200, 1200, 800)
        self.api_key = os.getenv("API_KEY")
        self.radius = 5
        self.station_id = ""
        self.isFavorite = False
        self.fuelPriceDB = FuelPriceDB()
        self.history = History(self.gridLayoutHistory)
        self.fetcher = StationDataFetcher(self.api_key)
        self.location_service = LocationService()
        self.map_view: QWebEngineView = QWebEngineView()
        self.gridLayout_3.addWidget(self.map_view)
        self.map_manager = MapManager(self.map_view)
        self.setup_connectiions()
        self.setup_ui()
        self.statusBar = super().statusBar()
        StatusLogger.set_status_bar(self.statusBar)
        MainWindow._status_bar = self.statusBar

        self.loading_player = UIHelper.create_image_player("resources/icons/loading.gif", self.centralStackedWidget.widget(1))
        self.gridLayoutHistory.addWidget(self.loading_player, 0, 0, -1, -1, Qt.AlignmentFlag.AlignCenter)

    def setup_ui(self):
        self.btnDiesel.setChecked(True)
        self.stackedWidget.setCurrentIndex(0)
        self.centralStackedWidget.setCurrentIndex(0)
        UIHelper.apply_stylesheet(self, "resources/stylesheets/lightStyle.qss")
        UIHelper.load_fonts('resources/fonts/SitkaVF.ttf')
        self.go_to_my_location()
        self.btnBackToHome.setVisible(False)
        
    def setup_connectiions(self):
        self.horiSliderRadius.valueChanged.connect(self.update_radius)
        self.search_button.clicked.connect(self.go_to_my_location)
        self.edtSearch.returnPressed.connect(self.search_stations_by_city_or_zip)
        self.btnDiesel.clicked.connect(self.on_Diesele_clicked)
        self.btnSuperE10.clicked.connect(self.on_SuperE10_clicked)
        self.btnSuperPlus.clicked.connect(self.on_SuperPlus_clicked)
        self.station_Table.itemClicked.connect(self.on_station_clicked)
        self.btnBackToStations.clicked.connect(self.on_backToStations_clicked)
        self.btnBackToHome.clicked.connect(self.on_BackToHome_clicked)
        self.btnHistory.clicked.connect(self.on_History_clicked)
        self.btnCountry.clicked.connect(self.on_History_clicked)
        self.btnCity.clicked.connect(self.on_HistoryCity_clicked)
        self.spBoxRadius.valueChanged.connect(self.update_Radius_From_SpinBox)
        self.btnAddToFavorites.clicked.connect(self.toggle_favorite)
        self.btnFavorites.clicked.connect(self.show_favorites_only)

    def update_radius(self):
        self.radius = self.horiSliderRadius.value()
        self.on_BackToHome_clicked()
        self.reload_stations()
        self.spBoxRadius.setValue(self.radius)

    def update_Radius_From_SpinBox(self):
        self.horiSliderRadius.setValue(self.spBoxRadius.value())
    
    def go_to_my_location(self):
        self.on_BackToHome_clicked()
        lat, lon = self.location_service.get_location_by_ip()
        self.radius = self.horiSliderRadius.value()
        self.load_stations_and_map(lat, lon, self.radius)
        self.spBoxRadius.setValue(self.radius)

    def search_stations_by_city_or_zip(self):
        self.on_BackToHome_clicked()
        city_or_zip = self.edtSearch.text().strip()
        lat, lon = self.location_service.lon_lat_city(city_or_zip)
        self.load_stations_and_map(lat, lon, self.radius)

    def load_stations_and_map(self, lat, lon, rad):
        fuel_type = self.get_fuel_type()
        stations = self.fetcher.fetch_stations(lat, lon, fuel_type, rad, self.isFavorite)
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
        self.loadHistory()
        self.reload_stations()

    def on_SuperE10_clicked(self):
        self.btnDiesel.setChecked(False)
        self.btnSuperE10.setChecked(True)
        self.btnSuperPlus.setChecked(False)
        self.loadHistory()
        self.reload_stations()

    def on_SuperPlus_clicked(self):
        self.btnDiesel.setChecked(False)
        self.btnSuperE10.setChecked(False)
        self.btnSuperPlus.setChecked(True)
        self.loadHistory()
        self.reload_stations()

    def on_History_clicked(self):
        self.loadHistory()
        self.centralStackedWidget.setCurrentIndex(1)
        self.btnHistory.setVisible(False)
        self.btnBackToHome.setVisible(True)
    def on_HistoryCity_clicked(self):
        self.loading_player.start()
        QTimer.singleShot(100, self.loadCityHistory)
    def on_BackToHome_clicked(self):
        self.centralStackedWidget.setCurrentIndex(0)
        self.btnHistory.setVisible(True)
        self.btnBackToHome.setVisible(False)

    def on_backToStations_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def reload_stations(self):
        lat, lon = self.location_service.get_lat_lon()
        self.load_stations_and_map(lat, lon, self.radius)

    def loadHistory(self):
        fuel_type = self.get_fuel_type()
        self.history.create_price_history_plot(fuel_type)

    def loadCityHistory(self):
        try:
            lat, lon = self.location_service.get_lat_lon()
            selected_fuel_type = self.get_fuel_type()
            plz = self.location_service.get_postal_code(lat, lon)
            plz_prefix = plz[:3]
            if plz_prefix:
                stations_df = self.fuelPriceDB.load_stations_from_db(plz_prefix)
                prices_df = self.fuelPriceDB.load_prices_from_db(stations_df, selected_fuel_type)
                self.history.plot_price_trend(prices_df, selected_fuel_type, plz_prefix)  
        except Exception as e:
            StatusLogger.error(f"Error in loadCityHistory: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Hide loading animation
            self.loading_player.stop()

    def on_station_clicked(self):
        lat, lon = self.location_service.get_lat_lon()
        stations = self.fetcher.fetch_stations(lat, lon, "diesel", self.radius, self.isFavorite)

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
        self.station_id = first_station.get("id", "Unbekannt")
        status_text = f"<span style='color: {'green' if is_open else 'red'};'>{'Geöffnet' if is_open else 'Geschlossen'}</span>"

        self.btnAddToFavorites.setChecked(self.fuelPriceDB.is_favorite(self.station_id))
        self.lblOpen.setText(status_text)
        self.lblStatioName.setText(f"{brand} Tankstelle")
        self.lblAddress.setText(f"{street} {house_number} \n{post_code} {city}")
        self.lblDieselPrice.setText(f"{str(first_station.get('price', 'N/A'))} €")

        for fuel in ["e10", "e5"]:
            stations = self.fetcher.fetch_stations(lat, lon, fuel, self.radius, self.isFavorite)
            if stations:
                first_station = stations[self.station_Table.currentRow()]
                price = first_station.get('price', 'N/A')
                if fuel == "e10":
                    self.lcdE10.setText(f"{str(price)} €")
                elif fuel == "e5":
                    self.lcdSuperPlus.setText(f"{str(price)} €")

            self.stackedWidget.setCurrentIndex(1)

    def toggle_favorite(self):
        if self.station_id:
            if self.fuelPriceDB.is_favorite(self.station_id):
                self.fuelPriceDB.remove_from_favorites(self.station_id)
                self.btnAddToFavorites.setChecked(False)
            else:
                self.fuelPriceDB.add_to_favorites(self.station_id)
                self.btnAddToFavorites.setChecked(True)
            self.reload_stations()
        else:
            StatusLogger.error("Keine Tankstelle ausgewählt")

    def show_favorites_only(self):
        self.isFavorite = not self.isFavorite
        lat, lon = self.location_service.get_lat_lon()
        self.load_stations_and_map(lat, lon, self.radius)