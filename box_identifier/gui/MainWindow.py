from PySide2.QtCore import QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QRectF, Qt
from PySide2.QtWidgets import QPushButton, QLineEdit, QComboBox, QCheckBox, QProgressBar, QGraphicsView,\
    QMessageBox, QGraphicsScene, QFileDialog
from PySide2.QtGui import QIntValidator, QIcon, QPixmap
from box_identifier.services import DropBox
from box_identifier.generate_identifier import IdentifierImage, IdentifierFiles
from box_identifier import constants
from dropbox.exceptions import DropboxException
from PIL.ImageQt import ImageQt
from threading import Thread



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

    icon = None

    files_list = []

    dbx_path_selected = ""

    tmp_path = ""

    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)

        ui_path = constants.LOAD_VIEW("mainwindow.ui")
        icon_path = constants.APP_ICON

        self.icon = QIcon(icon_path)
        ui_file = QFile(ui_path)

        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()

        self.window = loader.load(ui_file)
        self.window.setFixedSize(600, 450)
        self.window.setWindowIcon(self.icon)

        ui_file.close()

        try:
            drop_box = DropBox()

            self.files_list = drop_box.all_file_names()

            self.__first_definition(self.window.findChild)
            self.__first_config()

            self.window.show()

        except DropboxException:
            self.__show_ok_msg_box("Não foi possível carregar a lista de arquivos do dropbox!", QMessageBox.warning)
            app.close_all_windows()

    def __first_definition(self, find_child):
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

    def __first_config(self):
        self.__config_line_edit([
            self.input_r_init,
            self.input_r_end,
            self.input_ct_init,
            self.input_ct_end,
            self.input_pac_init,
            self.input_pac_end,
        ])

        select_items = []

        for file in self.files_list:
            select_items.append(file["filename"])

        self.select_background.addItems(select_items)

        self.btn_generate.clicked.connect(self.__generate_handler)
        self.select_background.currentIndexChanged.connect(self.__select_handler)

    def __show_ok_msg_box(self, text, icon):
        msg_box = QMessageBox()

        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(text)
        msg_box.setWindowIcon(self.icon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def __generate_handler(self):

        if not self.dbx_path_selected:
            return self.__show_ok_msg_box("Selecione um Background", QMessageBox.Information)

        text_r_init = self.input_r_init.text()
        text_r_end = self.input_r_end.text()
        text_ct_init = self.input_r_init.text()
        text_ct_end = self.input_r_end.text()
        text_pac_init = self.input_r_init.text()
        text_pac_end = self.input_r_end.text()

        if not text_r_init or not text_r_end or not text_ct_init or not text_ct_end:
            return self.__show_ok_msg_box("Campos Inválidos", QMessageBox.Warning)

        path = self.__directory_dialog()

        if not path:
            return

        is_small = not self.check_large.isChecked()

        make_zip = self.check_zip.isChecked()

        is_pac = text_pac_init and text_pac_end

        temp_path = self.tmp_path

        self.btn_generate.setDisabled(True)

        def run_generate_identifier():
            identifier_files = IdentifierFiles(
                background_path=temp_path,
                font_path=constants.DEFAULT_FONT,
                r_init=int(text_r_init),
                r_end=int(text_r_end),
                ct_init=int(text_ct_init),
                ct_end=int(text_ct_end),
                pac_init=int(text_pac_init) if is_pac else None,
                pac_end=int(text_pac_end) if is_pac else None,
            )

            identifier_files.make_zip = make_zip

            identifier_files.is_small = is_small

            identifier_files.save(path)

        gen_thread = Thread(target=run_generate_identifier)

        gen_thread.start()

        gen_thread.join()

        self.btn_generate.setDisabled(False)

        self.__show_ok_msg_box("Arquivos Gerados!", QMessageBox.Information)

    def __directory_dialog(self):
        dialog = QFileDialog(self.window)
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_() == QFileDialog.Accepted:
            return dialog.selectedFiles()[0]

        return None

    def __select_handler(self, idx):
        list_idx = idx - 1

        if list_idx == -1:
            self.dbx_path_selected = ""
            return

        self.dbx_path_selected = self.files_list[list_idx]["path"]

        self.__change_view_identifier(self.dbx_path_selected)

    def __change_view_identifier(self, dbx_path):

        self.tmp_path = DropBox().get_temp_file_path(dbx_path)

        identifier_image = IdentifierImage(
            "R01-CT01", self.tmp_path,
            constants.DEFAULT_FONT
        )

        identifier_image.is_small = not self.check_large.isChecked()

        identifier_image.is_pac = False

        image = identifier_image.image()

        img_qt = ImageQt(image)

        q_pixmap = QPixmap.fromImage(img_qt)

        graphics_scene = QGraphicsScene()

        graphics_scene.addPixmap(q_pixmap)

        self.graphics_view.setScene(graphics_scene)

        self.graphics_view.fitInView(QRectF(0, 0, image.size[0], image.size[1]), Qt.KeepAspectRatio)

        graphics_scene.update()
