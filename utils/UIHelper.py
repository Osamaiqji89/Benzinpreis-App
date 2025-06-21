from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QIcon, QFont, QMovie, QFontDatabase
from PyQt6.QtCore import Qt, QByteArray

from services.FuelPriceDB import FuelPriceDB
from utils.path_utils import resource_path

class UIHelper:
    @staticmethod
    def apply_stylesheet(window, path):
        with open(path, "r") as file:
            stylesheet = file.read()
            window.setStyleSheet(stylesheet)

    @staticmethod
    def populate_station_table(table, stations):
        table.clear()
        table.setRowCount(0)
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 80)
        table.setColumnWidth(2, 25)
        
        row_idx = 0
        for station in stations:
            table.insertRow(row_idx)
            table.setItem(row_idx, 0, QTableWidgetItem(f"{station.get('brand', 'Unbekannt')} Tankstelle"))
            table.setItem(row_idx, 1, QTableWidgetItem(f"{station.get('price', 'N/A')} €"))
            icon_item = QTableWidgetItem()
            icon_item.setIcon(QIcon(resource_path("resources/icons/arrow.png")))
            table.setItem(row_idx, 2, icon_item)
            table.setRowHeight(row_idx, 50)
            row_idx += 1

    @staticmethod
    def load_fonts(path):
        QFontDatabase.addApplicationFont(path)
        app_font = QFont(resource_path('resources/fonts/SitkaVF.ttf'))
        QApplication.setFont(app_font)

    @staticmethod
    def create_image_player(filename, parent=None):
        player = QWidget(parent)
        movie = QMovie(filename, QByteArray(), player)
        
        # Create the label that holds the gif
        movie_screen = QLabel()
        movie_screen.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        movie_screen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(movie_screen)
        player.setLayout(main_layout)

        # Add the QMovie object to the label
        movie.setCacheMode(QMovie.CacheMode.CacheAll)
        movie.setSpeed(100)
        movie_screen.setMovie(movie)
        
        # Set size and style
        player.setFixedSize(600, 300)
        player.setStyleSheet("""
            QWidget {
                background-color: rgba(243, 244, 235, 150);
                border: none;
                border-radius: 5px;
            }
            QLabel {
                background-color: rgba(243, 244, 235, 0);
            }
        """)
        player.hide()

        # Add methods to the widget
        def start():
            player.show()
            movie.start()
        
        def stop():
            movie.stop()
            player.hide()
        
        player.start = start
        player.stop = stop
        
        return player
