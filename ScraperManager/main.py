import sys
import webbrowser

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QSplitter,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QMessageBox,
    QTextEdit,
    QTextBrowser,
    QDialog,
    
)

from PyQt5.QtCore import Qt
from database import Database
from config import *

from ui.theme import DARK_THEME

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


class DetailsHtmlDialog(QDialog):
    """
    مشابه DetailsDialog است، با این تفاوت که مقادیر ستون‌ها به‌عنوان HTML
    رندر می‌شوند (یعنی اگر مقدار سلولی حاوی تگ‌های HTML باشد، به‌جای نمایش
    متن خام تگ‌ها، محتوا به‌صورت صفحه‌ی HTML واقعی نشان داده می‌شود).
    """

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

        html = "<div style='font-family: Tahoma, sans-serif;'>"

        for k, v in row.items():
            html += (
                f"<h3 style='color:#4FC3F7; margin-bottom:2px;'>{k}</h3>"
                f"<div style='margin-bottom:14px;'>{v}</div>"
            )

        html += "</div>"

        browser.setHtml(html)

        layout.addWidget(browser)


class BaseTab(QWidget):

    def __init__(self, db, columns):
        super().__init__()

        self.db = db
        self.columns = columns
        self.df = None          # کل داده اصلی (بدون فیلتر سرچ)
        self.view = None        # دیتافریمی که دقیقا معادل چیزی است که در جدول نمایش داده میشود
        self.current_file = None
        self._loading = False   # جلوگیری از trigger شدن itemChanged هنگام پرکردن برنامه‌ای جدول

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
        self.details2_btn = QPushButton("Details 2 (HTML)")
        self.open_btn = QPushButton("Open Link")

        top.addWidget(self.search)
        top.addWidget(self.refresh_btn)
        top.addWidget(self.details_btn)
        top.addWidget(self.details2_btn)
        top.addWidget(self.open_btn)
        top.addWidget(self.delete_btn)
        top.addWidget(self.save_btn)

        layout.addLayout(top)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        layout.addWidget(self.table)

        self.search.textChanged.connect(self.search_data)
        self.refresh_btn.clicked.connect(self.reload)
        self.delete_btn.clicked.connect(self.delete_row)
        self.details_btn.clicked.connect(self.show_details)
        self.details2_btn.clicked.connect(self.show_details_html)
        self.open_btn.clicked.connect(self.open_link)
        self.save_btn.clicked.connect(self.save_file)

        # مهم: با هر تغییر دستی سلول، مقدار را بلافاصله در view/df همگام می‌کنیم
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

        self.table.setHorizontalHeaderLabels(
            [str(c) for c in self.view.columns]
        )

        for r in range(len(self.view)):
            for c, col in enumerate(self.view.columns):
                self.table.setItem(
                    r, c,
                    QTableWidgetItem(str(self.view.iloc[r, c]))
                )

        self.table.resizeColumnsToContents()

        self._loading = False

    # -----------------------------

    def on_item_changed(self, item):
        """وقتی کاربر یک سلول را در جدول ویرایش می‌کند، مقدار را در view و df به‌روز می‌کنیم."""

        if self._loading or self.view is None:
            return

        row = item.row()
        col = item.column()

        if row < 0 or row >= len(self.view) or col < 0 or col >= len(self.view.columns):
            return

        col_name = self.view.columns[col]
        new_value = item.text()

        # به‌روزرسانی نمای فعلی (که ممکن است فیلترشده باشد)
        self.view.iloc[row, col] = new_value

        # همگام‌سازی با دیتافریم اصلی از طریق ایندکس واقعی
        real_index = self.view.index[row]
        if self.df is not None and real_index in self.df.index:
            self.df.loc[real_index, col_name] = new_value

    # -----------------------------

    def current_row(self):

        row = self.table.currentRow()
        if row < 0 or self.view is None:
            return None

        return self.view.iloc[row]

    # -----------------------------

    def search_data(self, text):

        if self.df is None or self.df.empty:
            return

        self.load_dataframe(
            self.db.search(self.df, text)
        )

    # -----------------------------

    def delete_row(self):

        rows = sorted(
            set(i.row() for i in self.table.selectedIndexes()),
            reverse=True
        )

        if not rows or self.view is None:
            return

        # ایندکس‌های واقعی مربوط به ردیف‌های نمایشی انتخاب‌شده را پیدا می‌کنیم
        real_indexes = [self.view.index[r] for r in rows if r < len(self.view)]

        # حذف از دیتافریم اصلی با ایندکس واقعی
        self.df = self.df.drop(index=real_indexes, errors="ignore")

        # حذف از نمای فعلی هم (برای رفرش صحیح جدول در حالت سرچ)
        self.view = self.view.drop(index=real_indexes, errors="ignore")

        self.load_dataframe(self.view)

    # -----------------------------

    def show_details(self):

        row = self.current_row()
        if row is None:
            return

        DetailsDialog(row).exec()

    # -----------------------------

    def show_details_html(self):

        row = self.current_row()
        if row is None:
            return

        DetailsHtmlDialog(row).exec()

    # -----------------------------

    def save_file(self):

        if self.current_file is None or self.df is None:
            return

        self.db.save(self.df, self.current_file)

        QMessageBox.information(
            self,
            APP_NAME,
            "Saved."
        )

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


class NewsTab(BaseTab):
    def __init__(self, db):
        super().__init__(db, ["عنوان", "منبع", "تاریخ", "لینک"])


class DrugsTab(BaseTab):
    def __init__(self, db):
        super().__init__(db, ["نام", "گروه", "شرکت", "شکل", "کد", "توضیحات"])


class GroupsTab(BaseTab):
    def __init__(self, db):
        super().__init__(db, ["کد گروه", "نام گروه"])


class OtherTab(QWidget):
    def __init__(self, db):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("سایر اطلاعات"))

        text = QTextEdit()
        text.setReadOnly(True)

        text.setPlainText("""

• راهنما
• درباره برنامه
• اطلاعات نسخه
• یادداشت‌ها
• تغییرات نسخه‌ها
        """)

        layout.addWidget(text)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.db = Database()

        self.setWindowTitle(APP_NAME)
        self.resize(1500, 850)

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

        layout.addWidget(splitter, stretch=1)

        self.author_label = QLabel("Author: Telegram: @Alireza_koh1")
        self.author_label.setStyleSheet("""
            color: #666;
            font-size: 10px;
            padding: 6px;
        """)
        self.author_label.setAlignment(Qt.AlignRight)  # 👈 مهم

        layout.addWidget(self.author_label, stretch=0)

        self.setCentralWidget(container)
    # -----------------------------

    def load_files(self):

        self.file_list.clear()
        self.mapping = {}

        for category in self.db.files:

            for f in self.db.files[category]:

                item = QListWidgetItem(
                    f"[{category.upper()}] {f.name}"
                )

                self.file_list.addItem(item)
                self.mapping[item.text()] = (category, f)

    # -----------------------------

    def open_selected_file(self, item):

        category, path = self.mapping[item.text()]

        if category == "news":
            self.tabs.setCurrentWidget(self.news)
            self.news.load_file(path)

        elif category == "drugs":
            self.tabs.setCurrentWidget(self.drugs)
            self.drugs.load_file(path)

        elif category == "groups":
            self.tabs.setCurrentWidget(self.groups)
            self.groups.load_file(path)

        else:
            self.tabs.setCurrentWidget(self.other)


# -----------------------------
# Run App
# -----------------------------

app = QApplication(sys.argv)
app.setStyleSheet(DARK_THEME)

window = MainWindow()
window.show()

sys.exit(app.exec())