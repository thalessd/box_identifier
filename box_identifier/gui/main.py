import sys
from PySide2.QtCore import QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QPushButton
from box_identifier import constants


class Main(QObject):

    def __init__(self, ui_file, parent=None):
        super(Main, self).__init__(parent)

        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()

        self.window = loader.load(ui_file)
        self.window.setFixedSize(600, 450)

        ui_file.close()

        btn_generate = self.window.findChild(QPushButton, 'btn_generate')

        btn_generate.clicked.connect(self.generate_handler)

        self.window.show()

    def generate_handler(self):
        print("Teste")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    _main = Main(constants.LOAD_VIEW("main.ui"))

    sys.exit(app.exec_())
