# details_dialog.py

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QApplication,
    QHBoxLayout,
)

from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

from pathlib import Path


class DetailsDialog(QDialog):

    def __init__(self, title="", content="", file_path=None, parent=None):
        super().__init__(parent)

        self.file_path = file_path

        self.setWindowTitle(title)
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        self.info = QLabel(title)
        layout.addWidget(self.info)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setPlainText(content)
        layout.addWidget(self.text)

        buttons = QHBoxLayout()

        self.copy_btn = QPushButton("کپی متن")
        self.copy_btn.clicked.connect(self.copy_text)
        buttons.addWidget(self.copy_btn)

        self.save_btn = QPushButton("ذخیره")
        self.save_btn.clicked.connect(self.save_text)
        buttons.addWidget(self.save_btn)

        self.open_btn = QPushButton("باز کردن فایل")
        self.open_btn.clicked.connect(self.open_file)
        buttons.addWidget(self.open_btn)

        self.close_btn = QPushButton("بستن")
        self.close_btn.clicked.connect(self.close)
        buttons.addWidget(self.close_btn)

        layout.addLayout(buttons)

    def copy_text(self):
        QApplication.clipboard().setText(self.text.toPlainText())

    def save_text(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره",
            "",
            "Text (*.txt)"
        )

        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.text.toPlainText())

            QMessageBox.information(
                self,
                "ذخیره شد",
                "فایل ذخیره شد."
            )

    def open_file(self):

        if self.file_path is None:
            return

        path = Path(self.file_path)

        if path.exists():
            QDesktopServices.openUrl(
                QUrl.fromLocalFile(str(path))
            )