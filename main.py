import sys
import traceback
from PyQt6.QtWidgets import QApplication, QWidget
from mainWindow import MainWindow
from PyQt6.QtGui import QIcon


def run_app():
    app = QApplication(sys.argv)
    app.setApplicationName("Benzinpreis App")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Fachhochschule Südwestfalen")
    app.setWindowIcon(QIcon("resources/icons/station.ico"))
    mainWindow = MainWindow()
    mainWindow.show()
    return app.exec()


if __name__ == "__main__":
    try:
        exit_code = run_app()
        sys.exit(exit_code)
    except Exception as e:
        tb = traceback.format_exc()
        print("Unhandled exception:\n", tb, file=sys.stderr)
        try:
            with open("error_traceback.log", "w") as f:
                f.write(tb)
        except Exception:
            pass
        # Try to show an error dialog if Qt is available
        try:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Application Error", "An unhandled exception occurred. See error_traceback.log for details.\n\n" + str(e))
        except Exception:
            pass
        sys.exit(1)