from PySide2.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QPushButton, QLineEdit, QProgressBar, \
    QCheckBox, QMessageBox, QFileDialog
from PySide2.QtGui import QIntValidator, QIcon
from make_identifier.generate_identifier import generate_identifier
from threading import Thread
from make_identifier.helpers import resource_path


def make_default_input(layout, col, row, placeholder, value=None):
    line_edit = QLineEdit(value)

    line_edit.setPlaceholderText(placeholder)

    line_edit.setValidator(QIntValidator(0, 99))

    layout.addWidget(line_edit, col, row)

    return line_edit


def generate_layout(layout, win, app):

    layout.addWidget(QLabel("R"), 1, 1)

    r_init_le = make_default_input(layout, 2, 1, "R Inicial*")
    r_end_le = make_default_input(layout, 2, 2, "R Final*")

    layout.addWidget(QLabel("CT"), 3, 1)

    ct_init_le = make_default_input(layout, 4, 1, "CT Inicial*")
    ct_end_le = make_default_input(layout, 4, 2, "CT Final*")

    layout.addWidget(QLabel("PAC"), 5, 1)

    pac_init_le = make_default_input(layout, 6, 1, "PAC Inicial")
    pac_end_le = make_default_input(layout, 6, 2, "PAC Final")

    zip_cb = QCheckBox("Gerar arquivo zipado?")

    layout.addWidget(zip_cb, 7, 1)

    progress_pb = QProgressBar()
    progress_pb.setValue(0)
    progress_pb.setMaximum(100)

    layout.addWidget(progress_pb, 8, 1)

    export_btn = QPushButton("Gerar Adesivos")

    layout.addWidget(export_btn, 8, 2)

    def clear_fields():
        r_init_le.setText("")
        r_end_le.setText("")

        ct_init_le.setText("")
        ct_end_le.setText("")

        pac_init_le.setText("")
        pac_end_le.setText("")

        progress_pb.setValue(0)

    def show_msg_box(text, icon):
        msg_box = QMessageBox()

        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def directory_dialog():
        dialog = QFileDialog(win)
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_() == QFileDialog.Accepted:
            return dialog.selectedFiles()[0]

        return None

    def run_progress(percent):
        progress_pb.setValue(percent)

    def export_click():
        r_init_text = r_init_le.text()
        r_end_text = r_end_le.text()

        ct_init_text = ct_init_le.text()
        ct_end_text = ct_end_le.text()

        pac_init_text = pac_init_le.text()
        pac_end_text = pac_end_le.text()

        if not r_init_text or not r_end_text or not ct_init_text or not ct_end_text:
            return show_msg_box("Campos Inválidos", QMessageBox.Warning)

        path = directory_dialog()

        if not path:
            return

        is_pac = pac_init_text and pac_end_text

        export_btn.setDisabled(True)

        def run_generate_identifier():
            generate_identifier(
                out_path=path,
                make_zip=zip_cb.isChecked(),
                r_init=int(r_init_text),
                r_end=int(r_end_text),
                ct_init=int(ct_init_text),
                ct_end=int(ct_end_text),
                pac_init=int(pac_init_text) if is_pac else None,
                pac_end=int(pac_end_text) if is_pac else None,
                progress=run_progress
            )

        gen_thread = Thread(target=run_generate_identifier)

        app.processEvents()

        gen_thread.start()

        gen_thread.join()

        export_btn.setDisabled(False)

        clear_fields()

        show_msg_box("Arquivos Gerados!", QMessageBox.Information)

    export_btn.clicked.connect(export_click)


def main():
    app = QApplication([])
    app.setStyle('Fusion')

    win = QWidget()
    win.setMinimumSize(400, 200)
    win.setMaximumSize(400, 200)
    win.setWindowTitle("Box Identifier")

    icon_path = resource_path("data/icon.png")
    icon = QIcon(icon_path)

    win.setWindowIcon(icon)

    layout = QGridLayout()

    generate_layout(layout, win, app)

    win.setLayout(layout)

    win.show()

    app.exec_()
