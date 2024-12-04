import sys
from PyQt6.QtWidgets import QApplication, QWidget  
from mainWindow import MainWindow
from PyQt6.QtGui import QIcon

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Benzinpreis App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Fachhochschule Südwestfalen") 
    app.setWindowIcon(QIcon("resources/icons/station.ico"))
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())