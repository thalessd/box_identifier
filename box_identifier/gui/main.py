import sys
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from box_identifier import constants


def main():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    main_ui_path = constants.LOAD_VIEW("main.ui")

    file = QFile(main_ui_path)

    file.open(QFile.ReadOnly)

    loader = QUiLoader()

    window = loader.load(file)

    window.setFixedSize(600, 450)

    window.show()

    sys.exit(app.exec_())