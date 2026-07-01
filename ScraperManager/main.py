import sys
import webbrowser
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QSplitter, QListWidget, QListWidgetItem,
    QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QMessageBox, QTextEdit, QTextBrowser, QDialog
)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from database import Database
from config import *
from ui.theme import DARK_THEME


# -----------------------------
# Helper (PyInstaller safe path)
# -----------------------------
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)


# -----------------------------
# Details Dialog
# -----------------------------
class DetailsDialog(QDialog):
    def __init__(self, row):
        super().__init__()
        self.setWindowTitle("Details")
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
            QTextEdit {
                background-color: #181818;
                color: #EAEAEA;
                border: none;
                font-size: 13px;
            }
        """)

        data = ""
        for k, v in row.items():
            data += f"{k}\n{'-'*40}\n{v}\n\n"

        text.setPlainText(data)
        layout.addWidget(text)


# -----------------------------
# HTML Dialog
# -----------------------------
class DetailsHtmlDialog(QDialog):
    def __init__(self, row):
        super().__init__()
        self.setWindowTitle("Details (HTML)")
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet("""
            QTextBrowser {
                background-color: #181818;
                color: #EAEAEA;
                border: none;
                font-size: 13px;
            }
        """)

        html = "<div style='font-family: Tahoma;'>"

        for k, v in row.items():
            html += f"<h3 style='color:#4FC3F7'>{k}</h3><div>{v}</div>"

        html += "</div>"

        browser.setHtml(html)
        layout.addWidget(browser)


# -----------------------------
# Base Tab
# -----------------------------
class BaseTab(QWidget):
    def __init__(self, db, columns):
        super().__init__()

        self.db = db
        self.columns = columns
        self.df = None
        self.view = None
        self.current_file = None
        self._loading = False

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)

        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")

        self.refresh_btn = QPushButton("Refresh")
        self.save_btn = QPushButton("Save")
        self.delete_btn = QPushButton("Delete")
        self.details_btn = QPushButton("Details")
        self.details_html_btn = QPushButton("HTML")
        self.open_btn = QPushButton("Open Link")

        top.addWidget(self.search)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.details_btn)
        top.addWidget(self.details_html_btn)
        top.addWidget(self.open_btn)
        top.addWidget(self.delete_btn)
        top.addWidget(self.save_btn)

        layout.addLayout(top)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        self.search.textChanged.connect(self.search_data)
        self.refresh_btn.clicked.connect(self.reload)
        self.save_btn.clicked.connect(self.save_file)
        self.delete_btn.clicked.connect(self.delete_row)
        self.details_btn.clicked.connect(self.show_details)
        self.details_html_btn.clicked.connect(self.show_details_html)
        self.open_btn.clicked.connect(self.open_link)

        self.table.itemChanged.connect(self.on_item_changed)

    # -----------------------------

    def load_file(self, path):
        self.current_file = path
        self.df = self.db.load(path)
        self.load_dataframe(self.df)

    # -----------------------------

    def load_dataframe(self, df):
        self._loading = True

        self.view = df.reset_index(drop=True)

        self.table.setRowCount(len(self.view))
        self.table.setColumnCount(len(self.view.columns))
        self.table.setHorizontalHeaderLabels([str(c) for c in self.view.columns])

        for r in range(len(self.view)):
            for c, col in enumerate(self.view.columns):
                self.table.setItem(r, c, QTableWidgetItem(str(self.view.iloc[r, c])))

        self.table.resizeColumnsToContents()
        self._loading = False

    # -----------------------------

    def on_item_changed(self, item):
        if self._loading or self.view is None:
            return

        row, col = item.row(), item.column()

        col_name = self.view.columns[col]
        value = item.text()

        self.view.iloc[row, col] = value
        real_index = self.view.index[row]

        if self.df is not None:
            self.df.loc[real_index, col_name] = value

    # -----------------------------

    def current_row(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.view.iloc[row]

    # -----------------------------

    def search_data(self, text):
        if self.df is None:
            return
        self.load_dataframe(self.db.search(self.df, text))

    # -----------------------------

    def delete_row(self):
        rows = sorted(set(i.row() for i in self.table.selectedIndexes()), reverse=True)
        if not rows:
            return

        real_indexes = [self.view.index[r] for r in rows]

        self.df = self.df.drop(index=real_indexes, errors="ignore")
        self.view = self.view.drop(index=real_indexes, errors="ignore")

        self.load_dataframe(self.view)

    # -----------------------------

    def show_details(self):
        row = self.current_row()
        if row is not None:
            DetailsDialog(row).exec()

    def show_details_html(self):
        row = self.current_row()
        if row is not None:
            DetailsHtmlDialog(row).exec()

    # -----------------------------

    def save_file(self):
        if self.current_file:
            self.db.save(self.df, self.current_file)
            QMessageBox.information(self, APP_NAME, "Saved")

    # -----------------------------

    def open_link(self):
        row = self.current_row()
        if row is None:
            return

        for c in self.df.columns:
            if "url" in c.lower() or "link" in c.lower():
                webbrowser.open(str(row[c]))
                return

    # -----------------------------

    def reload(self):
        if self.current_file:
            self.load_file(self.current_file)


# -----------------------------
# Tabs
# -----------------------------
class NewsTab(BaseTab):
    def __init__(self, db):
        super().__init__(db, ["عنوان", "منبع", "تاریخ", "لینک"])


class DrugsTab(BaseTab):
    def __init__(self, db):
        super().__init__(db, ["نام", "گروه", "شرکت", "شکل", "کد", "توضیحات"])


class GroupsTab(BaseTab):
    def __init__(self, db):
        super().__init__(db, ["کد", "نام"])


class OtherTab(QWidget):
    def __init__(self, db):
        super().__init__()
        layout = QVBoxLayout(self)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText("About / Help / Notes")
        layout.addWidget(text)


# -----------------------------
# Main Window
# -----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database()

        self.setWindowTitle(APP_NAME)
        self.resize(1500, 850)

        icon = resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon))

        self.build()

    # -----------------------------

    def build(self):

        splitter = QSplitter()

        self.file_list = QListWidget()
        splitter.addWidget(self.file_list)

        self.tabs = QTabWidget()

        self.news = NewsTab(self.db)
        self.drugs = DrugsTab(self.db)
        self.groups = GroupsTab(self.db)
        self.other = OtherTab(self.db)

        self.tabs.addTab(self.news, "News")
        self.tabs.addTab(self.drugs, "Drugs")
        self.tabs.addTab(self.groups, "Groups")
        self.tabs.addTab(self.other, "Other")

        splitter.addWidget(self.tabs)
        splitter.setStretchFactor(1, 5)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(splitter, 1)

        self.author_label = QLabel("Author: Telegram: @Alireza_koh1")
        self.author_label.setAlignment(Qt.AlignRight)
        self.author_label.setStyleSheet("color:#666;font-size:10px;padding:6px;")

        layout.addWidget(self.author_label)

        self.setCentralWidget(container)

        self.load_files()
        self.file_list.itemDoubleClicked.connect(self.open_selected_file)

    # -----------------------------

    def load_files(self):
        self.file_list.clear()
        self.mapping = {}

        for cat in self.db.files:
            for f in self.db.files[cat]:
                item = QListWidgetItem(f"[{cat}] {f.name}")
                self.file_list.addItem(item)
                self.mapping[item.text()] = (cat, f)

    # -----------------------------

    def open_selected_file(self, item):
        cat, path = self.mapping[item.text()]

        if cat == "news":
            self.tabs.setCurrentWidget(self.news)
            self.news.load_file(path)

        elif cat == "drugs":
            self.tabs.setCurrentWidget(self.drugs)
            self.drugs.load_file(path)

        elif cat == "groups":
            self.tabs.setCurrentWidget(self.groups)
            self.groups.load_file(path)

        else:
            self.tabs.setCurrentWidget(self.other)


# -----------------------------
# Run
# -----------------------------
app = QApplication(sys.argv)

app.setWindowIcon(QIcon(resource_path("icon.ico")))
app.setStyleSheet(DARK_THEME)

window = MainWindow()
window.show()

sys.exit(app.exec())