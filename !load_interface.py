import numpy as np
from matplotlib import pyplot 
import pint
# from . import lalala.py 
import sys, os
#from pysica_classes import *
#import pysica_classes as psc
#import pysica_plots as psp
import pysica_gui as pg
import datetime
import pandas as pd
import pysica_classes as psc
import pysica as ps

from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)


if __name__ == '__main__':
    ps = ps.PySICA()
    app = QApplication(sys.argv)
    pysica_janela = pg.PySICA_GUI()
    
    #pysica_janela = pg.WidgetGallery()
    pysica_janela.show()
    sys.exit(app.exec())
    
    

