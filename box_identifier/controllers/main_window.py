import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
import os.path as path
from box_identifier.scripts import constants


def run():
    app = QApplication(sys.argv)

    file = QFile(path.join(constants.VIEWS_FOLDER, "mainwindow.ui"))
    file.open(QFile.ReadOnly)

    loader = QUiLoader()

    window = loader.load(file)
    window.show()

    sys.exit(app.exec_())

