# proxy_model.py

from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtCore import QSortFilterProxyModel


class FilterProxyModel(QSortFilterProxyModel):

    def __init__(self):
        super().__init__()

        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)

        # جستجو در تمام ستون‌ها
        self.setFilterKeyColumn(-1)

    # ------------------------------

    def set_search(self, text):

        regex = QRegularExpression(
            text,
            QRegularExpression.CaseInsensitiveOption
        )

        self.setFilterRegularExpression(regex)

    # ------------------------------

    def clear_search(self):

        self.setFilterRegularExpression("")

    # ------------------------------

    def filterAcceptsRow(
        self,
        source_row,
        source_parent
    ):

        regex = self.filterRegularExpression()

        if not regex.pattern():
            return True

        model = self.sourceModel()

        cols = model.columnCount()

        for col in range(cols):

            index = model.index(
                source_row,
                col,
                source_parent
            )

            value = str(
                model.data(index)
            )

            if regex.match(value).hasMatch():
                return True

        return False

    # ------------------------------

    def row_count(self):

        return self.rowCount()

    # ------------------------------

    def column_count(self):

        return self.columnCount()

    # ------------------------------

    def source_dataframe(self):

        return self.sourceModel().dataframe()

    # ------------------------------

    def source_row(self, proxy_index):

        return self.mapToSource(proxy_index).row()

    # ------------------------------

    def selected_rows(self, indexes):

        rows = []

        for index in indexes:

            r = self.mapToSource(index).row()

            if r not in rows:
                rows.append(r)

        rows.sort(reverse=True)

        return rows

    # ------------------------------

    def value(self, proxy_index):

        source = self.mapToSource(proxy_index)

        return self.sourceModel().data(
            source
        )

    # ------------------------------

    def row_data(self, proxy_index):

        row = self.mapToSource(proxy_index).row()

        return self.sourceModel().row(row)