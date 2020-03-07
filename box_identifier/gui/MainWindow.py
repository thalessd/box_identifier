from PySide2.QtCore import QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QPushButton, QLineEdit, QComboBox, QCheckBox, QProgressBar, QGraphicsView,\
    QDialog, QVBoxLayout
from PySide2.QtGui import QIntValidator, QIcon
from box_identifier import constants


class MainWindow(QObject):
    input_r_init = QLineEdit
    input_r_end = QLineEdit
    input_ct_init = QLineEdit
    input_ct_end = QLineEdit
    input_pac_init = QLineEdit
    input_pac_end = QLineEdit

    select_background = QComboBox

    check_large = QCheckBox
    check_zip = QCheckBox

    progress_bar = QProgressBar

    graphics_view = QGraphicsView

    btn_generate = QPushButton

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        ui_path = constants.LOAD_VIEW("mainwindow.ui")
        icon_path = constants.APP_ICON

        icon = QIcon(icon_path)
        ui_file = QFile(ui_path)

        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()

        self.window = loader.load(ui_file)
        self.window.setFixedSize(600, 450)
        self.window.setWindowIcon(icon)

        ui_file.close()

        self.first_definition(self.window.findChild)
        self.first_config()

        self.window.show()

    def first_definition(self, find_child):
        self.input_r_init = find_child(QLineEdit, 'input_r_init')
        self.input_r_end = find_child(QLineEdit, 'input_r_end')
        self.input_ct_init = find_child(QLineEdit, 'input_ct_init')
        self.input_ct_end = find_child(QLineEdit, 'input_ct_end')
        self.input_pac_init = find_child(QLineEdit, 'input_pac_init')
        self.input_pac_end = find_child(QLineEdit, 'input_pac_end')

        self.select_background = find_child(QComboBox, 'select_background')

        self.check_large = find_child(QCheckBox, 'check_large')
        self.check_zip = find_child(QCheckBox, 'check_zip')

        self.progress_bar = find_child(QProgressBar, 'progress_bar')

        self.graphics_view = find_child(QGraphicsView, 'graphics_view')

        self.btn_generate = find_child(QPushButton, 'btn_generate')

    @staticmethod
    def __config_line_edit(lines_edit):
        for line_edit in lines_edit:
            line_edit.setValidator(QIntValidator(0, 99))

    def first_config(self):
        self.__config_line_edit([
            self.input_r_init,
            self.input_r_end,
            self.input_ct_init,
            self.input_ct_end,
            self.input_pac_init,
            self.input_pac_end,
        ])

        self.btn_generate.clicked.connect(self.generate_handler)

    def generate_handler(self):
        first_load_dialog = FirstLoadDialog()

        first_load_dialog.show()
