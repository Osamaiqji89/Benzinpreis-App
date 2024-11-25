import sys
from PyQt6.QtWidgets import QApplication, QWidget  
from mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())