from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QRectF, Qt, QObject, QThreadPool
from PySide2.QtWidgets import QPushButton, QLineEdit, QComboBox, QCheckBox, QProgressBar, QGraphicsView,\
    QMessageBox, QGraphicsScene, QFileDialog, QLabel
from PySide2.QtGui import QIntValidator, QIcon, QPixmap
from box_identifier.services import DropBox
from box_identifier.generate_identifier import IdentifierImage, IdentifierFiles
from box_identifier import constants
from PIL.ImageQt import ImageQt
from .worker import Worker


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
    btn_clear = QPushButton

    label_un = QLabel
    label_cm = QLabel

    icon = None

    files_list = []

    dbx_path_selected = ""

    tmp_path = ""

    thread_pool = QThreadPool()

    def __init__(self, parent=None):
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

        self.__first_definition(self.window.findChild)
        self.__first_config()

        self.window.show()

        self.__files_list_worker()

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
        self.btn_clear = find_child(QPushButton, 'btn_clear')

        self.label_un = find_child(QLabel, 'label_un')
        self.label_cm = find_child(QLabel, 'label_cm')

    def __first_config(self):
        self.__config_line_edit([
            self.input_r_init,
            self.input_r_end,
            self.input_ct_init,
            self.input_ct_end,
            self.input_pac_init,
            self.input_pac_end,
        ])

        self.btn_generate.clicked.connect(self.__generate_handler)
        self.btn_clear.clicked.connect(self.__clear_handler)
        self.select_background.currentIndexChanged.connect(self.__select_handler)
        self.check_large.stateChanged.connect(self.__check_large_handler)

    def __generate_handler(self):

        if not self.tmp_path:
            return self.__show_ok_msg_box("Selecione um Background", QMessageBox.Information)

        text_r_init = self.input_r_init.text()
        text_r_end = self.input_r_end.text()
        text_ct_init = self.input_ct_init.text()
        text_ct_end = self.input_ct_end.text()
        text_pac_init = self.input_pac_init.text()
        text_pac_end = self.input_pac_end.text()

        if not text_r_init or not text_r_end or not text_ct_init or not text_ct_end:
            return self.__show_ok_msg_box("Campos Inválidos", QMessageBox.Warning)

        path = self.__directory_dialog()

        if not path:
            return

        is_small = not self.check_large.isChecked()

        make_zip = self.check_zip.isChecked()

        is_pac = text_pac_init and text_pac_end

        generate_identifier_dict = dict(
            background_path=self.tmp_path,
            font_path=constants.DEFAULT_FONT,
            r_init=int(text_r_init),
            r_end=int(text_r_end),
            ct_init=int(text_ct_init),
            ct_end=int(text_ct_end),
            pac_init=int(text_pac_init) if is_pac else None,
            pac_end=int(text_pac_end) if is_pac else None,
            make_zip=make_zip,
            is_small=is_small,
            out_path=path
        )

        self.__generate_identifier_worker(generate_identifier_dict)

        self.window.activateWindow()

    def __clear_handler(self):
        inputs = [
            self.input_r_init,
            self.input_r_end,
            self.input_ct_init,
            self.input_ct_end,
            self.input_pac_init,
            self.input_pac_end,
        ]

        for input_field in inputs:
            input_field.setText("")

        self.select_background.setCurrentIndex(0)
        self.check_large.setChecked(False)
        self.check_zip.setChecked(False)
        self.label_un.setText("0 un")
        self.label_cm.setText("0 cm")

        self.graphics_view.setScene(QGraphicsScene())

        self.tmp_path = ""


    def __select_handler(self, idx):
        list_idx = idx - 1

        if list_idx == -1:
            self.dbx_path_selected = ""
            return

        self.dbx_path_selected = self.files_list[list_idx]["path"]

        self.__file_show_worker(self.dbx_path_selected)

    def __check_large_handler(self):

        dbx_path = self.dbx_path_selected

        if not dbx_path:
            return

        self.__file_show_worker(dbx_path)

    def __show_ok_msg_box(self, text, icon):
        msg_box = QMessageBox()

        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(text)
        msg_box.setWindowIcon(self.icon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def __directory_dialog(self):
        dialog = QFileDialog(self.window)
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_() == QFileDialog.Accepted:
            return dialog.selectedFiles()[0]

        return None

    def __disable_all_widgets(self, disabled):
        widgets = [
            self.input_r_init,
            self.input_r_end,
            self.input_ct_init,
            self.input_ct_end,
            self.input_pac_init,
            self.input_pac_end,
            self.select_background,
            self.check_large,
            self.check_zip,
            self.btn_generate,
            self.btn_clear
        ]

        for widget in widgets:
            widget.setDisabled(disabled)

    @staticmethod
    def __config_line_edit(lines_edit):
        for line_edit in lines_edit:
            line_edit.setValidator(QIntValidator(0, 99))

    """ Worker Functions """

    """ File List """

    def __files_list_worker(self):

        self.btn_generate.setDisabled(True)
        self.btn_clear.setDisabled(True)
        self.select_background.setDisabled(True)
        self.check_large.setDisabled(True)

        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)

        worker = Worker(self.__files_list_process)

        worker.signals.result.connect(self.__files_list_result)
        worker.signals.error.connect(self.__files_list_error)

        self.thread_pool.start(worker)

    @staticmethod
    def __files_list_process(progress_callback):
        drop_box = DropBox()

        return drop_box.all_file_names()

    def __files_list_result(self, result):

        self.files_list = result

        select_items = []

        for file in self.files_list:
            select_items.append(file["filename"])

        self.select_background.addItems(select_items)

        self.select_background.setDisabled(False)
        self.check_large.setDisabled(False)
        self.btn_generate.setDisabled(False)
        self.btn_clear.setDisabled(False)

        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    def __files_list_error(self):
        self.__show_ok_msg_box("Não foi possível carregar a lista de arquivos do dropbox!", QMessageBox.Warning)
        self.select_background.setDisabled(True)
        self.check_large.setDisabled(True)
        self.btn_generate.setDisabled(True)
        self.btn_clear.setDisabled(False)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    """ File List """

    """ Show Image """

    def __file_show_worker(self, dbx_path):

        self.btn_generate.setDisabled(True)
        self.btn_clear.setDisabled(True)
        self.select_background.setDisabled(True)
        self.check_large.setDisabled(False)

        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)

        is_small = not self.check_large.isChecked()

        kwargs = {"dbx_path": dbx_path, "is_small": is_small}

        worker = Worker(self.__file_show_process, **kwargs)

        worker.signals.result.connect(self.__file_show_result)
        worker.signals.error.connect(self.__file_show_error)

        self.thread_pool.start(worker)

    @staticmethod
    def __file_show_process(progress_callback, dbx_path, is_small):
        drop_box = DropBox()

        tmp_path = drop_box.get_temp_file_path(dbx_path)

        identifier_image = IdentifierImage(
            "R01-CT01", tmp_path,
            constants.DEFAULT_FONT
        )

        identifier_image.is_small = is_small

        identifier_image.is_pac = False

        image = identifier_image.image()

        return tmp_path, image

    def __file_show_result(self, result):

        tmp_path, image = result

        self.tmp_path = tmp_path

        img_qt = ImageQt(image)

        q_pixmap = QPixmap.fromImage(img_qt)

        graphics_scene = QGraphicsScene()

        graphics_scene.addPixmap(q_pixmap)

        self.graphics_view.setScene(graphics_scene)

        self.graphics_view.fitInView(QRectF(0, 0, image.size[0], image.size[1]), Qt.KeepAspectRatio)

        graphics_scene.update()

        self.check_large.setDisabled(False)
        self.select_background.setDisabled(False)
        self.btn_generate.setDisabled(False)
        self.btn_clear.setDisabled(False)

        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    def __file_show_error(self):
        self.__show_ok_msg_box("Não foi possível localizar este arquivo!", QMessageBox.Warning)
        self.tmp_path = ""
        self.select_background.setDisabled(False)
        self.check_large.setDisabled(False)
        self.btn_generate.setDisabled(True)
        self.btn_clear.setDisabled(False)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    """ Show Image """

    """ Generate Identifier """

    def __generate_identifier_worker(self, generate_identifier_dict):

        self.__disable_all_widgets(True)

        kwargs = {"generate_identifier_dict": generate_identifier_dict}

        worker = Worker(self.__generate_identifier_process, **kwargs)

        worker.signals.result.connect(self.__generate_identifier_result)
        worker.signals.error.connect(self.__generate_identifier_error)
        worker.signals.progress.connect(self.__generate_identifier_progress)

        self.thread_pool.start(worker)

    @staticmethod
    def __generate_identifier_process(progress_callback, generate_identifier_dict):

        gid = generate_identifier_dict

        identifier_files = IdentifierFiles(
            background_path=gid["background_path"],
            font_path=gid["font_path"],
            r_init=gid["r_init"],
            r_end=gid["r_end"],
            ct_init=gid["ct_init"],
            ct_end=gid["ct_end"],
            pac_init=gid["pac_init"],
            pac_end=gid["pac_end"]
        )

        identifier_files.make_zip = gid["make_zip"]

        identifier_files.is_small = gid["is_small"]

        identifier_files.save(gid["out_path"], progress_callback)

        return None

    def __generate_identifier_result(self, result):

        self.__disable_all_widgets(False)

        self.__show_ok_msg_box("Arquivos Gerados!", QMessageBox.Information)

        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    def __generate_identifier_error(self):
        self.__disable_all_widgets(False)

        self.__show_ok_msg_box("Não foi possível gerar os arquivos!", QMessageBox.Warning)

        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    def __generate_identifier_progress(self, percent):
        self.progress_bar.setValue(percent)

    """ Generate Identifier """
