# models.py

import pandas as pd

from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QVariant
)


class PandasModel(QAbstractTableModel):

    def __init__(self, dataframe=pd.DataFrame()):
        super().__init__()

        self._df = dataframe.copy()

    # ----------------------------

    def set_dataframe(self, df):

        self.beginResetModel()

        self._df = df.copy()

        self.endResetModel()

    # ----------------------------

    def dataframe(self):

        return self._df

    # ----------------------------

    def rowCount(self, parent=QModelIndex()):

        return len(self._df.index)

    # ----------------------------

    def columnCount(self, parent=QModelIndex()):

        return len(self._df.columns)

    # ----------------------------

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return QVariant()

        if role in (Qt.DisplayRole, Qt.EditRole):

            value = self._df.iloc[
                index.row(),
                index.column()
            ]

            return str(value)

        return QVariant()

    # ----------------------------

    def headerData(
            self,
            section,
            orientation,
            role=Qt.DisplayRole
    ):

        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:

            return str(
                self._df.columns[section]
            )

        return str(section + 1)

    # ----------------------------

    def flags(self, index):

        return (
            Qt.ItemIsEnabled
            | Qt.ItemIsSelectable
            | Qt.ItemIsEditable
        )

    # ----------------------------

    def setData(
            self,
            index,
            value,
            role=Qt.EditRole
    ):

        if role == Qt.EditRole:

            self._df.iat[
                index.row(),
                index.column()
            ] = value

            self.dataChanged.emit(
                index,
                index
            )

            return True

        return False

    # ----------------------------

    def sort(
            self,
            column,
            order
    ):

        col = self._df.columns[column]

        self.layoutAboutToBeChanged.emit()

        self._df.sort_values(
            by=col,
            ascending=(
                order == Qt.AscendingOrder
            ),
            inplace=True,
            ignore_index=True
        )

        self.layoutChanged.emit()

    # ----------------------------

    def removeRows(
            self,
            row,
            count,
            parent=QModelIndex()
    ):

        self.beginRemoveRows(
            parent,
            row,
            row + count - 1
        )

        self._df.drop(
            self._df.index[
                row:row+count
            ],
            inplace=True
        )

        self._df.reset_index(
            drop=True,
            inplace=True
        )

        self.endRemoveRows()

        return True

    # ----------------------------

    def insert_dataframe(self, df):

        self.beginResetModel()

        self._df = pd.concat(
            [self._df, df],
            ignore_index=True
        )

        self.endResetModel()

    # ----------------------------

    def row(self, index):

        return self._df.iloc[index]

    # ----------------------------

    def search(self, text):

        if text == "":
            return self._df

        mask = self._df.astype(str).apply(
            lambda c:
            c.str.contains(
                text,
                case=False,
                na=False
            )
        )

        return self._df[
            mask.any(axis=1)
        ]

    # ----------------------------

    def export_csv(self, filename):

        self._df.to_csv(
            filename,
            index=False
        )

    # ----------------------------

    def export_excel(self, filename):

        self._df.to_excel(
            filename,
            index=False
        )

    # ----------------------------

    def clear(self):

        self.beginResetModel()

        self._df = pd.DataFrame()

        self.endResetModel()