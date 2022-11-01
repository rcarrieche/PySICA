# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 05:24:34 2022

@author: nato
"""

import pysica_classes as psc
import pandas as pd
import sys

from PyQt6.QtCore import QDateTime, Qt, QTimer, QAbstractTableModel, QModelIndex, QVariant
from PyQt6.QtGui import QColor, QPalette, QAction
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QTabWidget, QMainWindow, QToolBar, QTableView)



db = psc.Database()

origens = db.get_origins()

#tags = db.get_tags([], ['PI485'])

#tags['total_values']

class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._dataframe.index[section])

        return None

class PandasModel2(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return QVariant(str(
                    self._data.iloc[index.row()][index.column()]))
        return QVariant()



class OrigensWidget(QWidget):
    def __init__(self):
        super(OrigensWidget, self).__init__()
        #db = psc.Database()
        #origens = db.get_origins()
        #self.tabs = 
        
        self.tabela = OrigensTable()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Teste tabela"))
        layout.addWidget(self.tabela)
        self.setLayout(layout)
        #self.view.show()
        

class OrigensTable(QTableView):
    def __init__(self):
        super(OrigensTable, self).__init__()
        db = psc.Database()
        origens = db.get_origins()
        #view = QTableView()
        #view.resize(800, 500)
        #view.setAlternatingRowColors(True)
        model = PandasModel(origens)
        #print()
        self.setModel(model)

if __name__ == '__main__':
    application = QApplication(sys.argv)
    """
    view = QTableView()
    model = PandasModel(origens)
    view.setModel(model)

    view.show()
    """
    janela = OrigensWidget()
    #janela.addWidget
    janela.show()
    sys.exit(application.exec())