from PyQt6.QtWidgets import QApplication, QTableWidgetItem

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
        for idx, station in enumerate(stations):
            table.insertRow(idx)
            table.setItem(idx, 0, QTableWidgetItem(f"{station.get('brand', 'Unbekannt')} Tankstelle"))
            table.setItem(idx, 1, QTableWidgetItem(f"{station.get('price', 'N/A')} €"))
            table.setRowHeight(idx, 50);
