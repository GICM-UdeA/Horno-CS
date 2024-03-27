from PyQt5.QtCore import QAbstractTableModel, Qt

class PandasModel(QAbstractTableModel):

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self)
        self._data = data
        self.rows = data.shape[0]
        self.columns = data.shape[1]

    def rowCount(self, parent=None):
        return self.rows

    def columnCount(self, parnet=None):
        return self.columns

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None