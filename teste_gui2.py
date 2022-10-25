# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 19:51:37 2022

@author: nato
"""

# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QFile
#from PyQt6.QtUiTools import QUiLoader
from PyQt6 import uic


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.load_ui()

    def load_ui(self):
        path = Path(__file__).resolve().parent / "form.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        uic.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())