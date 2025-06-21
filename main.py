import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
from mainWindow import MainWindow
from utils.path_utils import resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Benzinpreis App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Fachhochschule Südwestfalen") 
    app.setWindowIcon(QIcon(resource_path("resources/icons/station.ico")))
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
