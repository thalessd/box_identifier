import sys
from PySide2.QtWidgets import QApplication
from .MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    _main_window = MainWindow(app)

    sys.exit(app.exec_())

