# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 04:41:50 2022

@author: nato
"""

import pysica_classes as psc
from constantes import *

import pandas as pd


from PyQt6.QtCore import QDateTime, Qt, QTimer, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor, QPalette, QAction
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QTabWidget, QMainWindow, QToolBar, QTableView)

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent) # sempre tem que invocar a superclasse
        
        # muda a palette da aplicação inteira. Pelo visto, QApplication age na aplicação toda
        self.originalPalette = QApplication.palette()
        
        # Criação do combobox de estilo. 
        #TODO: usar combobox indexado por id ao invés de string com nome
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox) # provavelmente liga o label ao combobox
        
        # paleta de estilo
        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        
        

        # metodos para criar as outras partes. Está criando elas como variáveis diretamente na classe principal
        #TODO: ver o porquê da diferença de de se criar as partes como variáveis de classe ou variáveis de instância no __init__
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        # TODO: ver o que faz o textActivated() 
        styleComboBox.textActivated.connect(self.changeStyle) # muda o combobox usando o método changeStyle()
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        
        # desbilitador. 
        # muito mal gosto colocar lógica dentro da view
        self.disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        # TODO: por algum motivo, usar pelo método não desabilita da primeira vez.
        self.disableWidgetsCheckBox.setChecked(True)
        self.disableWidgetsCheckBox.setChecked(False)
        self.disableWidgetsCheckBox.toggled.connect(self.disableWidgets) 
        
        # cria a primeira linha
        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(self.disableWidgetsCheckBox)

        # cria a grade principal
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")
        self.changeStyle('Windows')

    def changeStyle(self, styleName):
        # cria o estilo
        QApplication.setStyle(QStyleFactory.create(styleName))
        
        # chama o changePalette 
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.CheckState.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Orientation.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Orientation.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)
    
    def disableWidgets(self):
        self.disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)



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

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class TagWidget(QWidget):
    def __init__(self):
        super(TagWidget, self).__init__()

class TagsWidget(QWidget):
    def __init__(self):
        super(TagsWidget, self).__init__()
        
class DadosWidget(QWidget):
    def __init__(self):
        super(DadosWidget, self).__init__()    

class FluxogramasWidget(QWidget):
    def __init__(self):
        super(FluxogramasWidget, self).__init__()  
        
class AnalisesWidget(QWidget):
    def __init__(self):
        super(AnalisesWidget, self).__init__()  

class UsuarioWidget(QWidget):
    def __init__(self):
        super(UsuarioWidget, self).__init__() 
        
class DocumentosWidget(QWidget):
    def __init__(self):
        super(DocumentosWidget, self).__init__() 

class OrigensWidget(QWidget):
    def __init__(self):
        super(OrigensWidget, self).__init__()
        #db = psc.Database()
        #origens = db.get_origins()
        #self.tabs = 
        # define tabela
        self.tabela = OrigensTable()
        
        
        
        layout_final = QVBoxLayout()
        
        layout_final.addWidget(self.groupbox_nova_origem())
        layout_final.addWidget(QLabel("Origens (TODAS)"))
        layout_final.addWidget(self.tabela)
        self.setLayout(layout_final)
        #self.view.show()

    def groupbox_nova_origem(self):
        grupo_insert = QGroupBox()
        layout_insert = QHBoxLayout()
        insert_nome_label = QLabel("Nova origem")
        insert_nome = QLineEdit("Nome da origem")
        insert_nome_label.setBuddy(insert_nome)
        insert_descricao_label = QLabel("Descrição")
        insert_descricao = QLineEdit("Descrição")
        insert_descricao_label.setBuddy(insert_descricao)
        botao_inserir = QPushButton("Inserir")
        layout_insert.addWidget(insert_nome_label)
        layout_insert.addWidget(insert_nome)
        layout_insert.addStretch(1)
        layout_insert.addWidget(insert_descricao_label)
        layout_insert.addWidget(insert_descricao)
        layout_insert.addWidget(botao_inserir)
        grupo_insert.setLayout(layout_insert)
        return grupo_insert

class OrigensTable(QTableView):
    def __init__(self):
        super(OrigensTable, self).__init__()
        db = psc.Database()
        origens = db.get_origins()
        origens = origens.drop(['data_origin_id', 'related_docs'], axis=1)
        #origens['tags'] = origens.loc[]
        #view = QTableView()
        #view.resize(800, 500)
        #view.setAlternatingRowColors(True)
        model = PandasModel(origens)
        #print()
        self.setModel(model)
        self.setAlternatingRowColors(True)
        
class DatasetsWidget(QWidget):
    def __init__(self):
        super(DatasetsWidget, self).__init__()
        self.tabela = DatasetsTable()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dataset: conjunto de tags contendo dados para análise"))
        layout.addWidget(self.tabela)
        self.setLayout(layout)
        #self.view.show()
        
class DatasetsTable(QTableView):
    def __init__(self):
        super(DatasetsTable, self).__init__()
        db = psc.Database()
        datasets = db.get_datasets()
        #view = QTableView()
        #view.resize(800, 500)
        #view.setAlternatingRowColors(True)
        model = PandasModel(datasets)
        #print()
        self.setModel(model)
        self.setAlternatingRowColors(True)


class ConexoesWidget(QWidget):
    def __init__(self):
        super(ConexoesWidget, self).__init__() 


class PySICA_GUI(QMainWindow):
    def __init__(self, parent=None):
        super(PySICA_GUI, self).__init__(parent)
        self.setWindowTitle(MAIN_TITLE)

        tabs = QTabWidget()
        #tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)
        
        toolbar = QToolBar("Teste toolbar")
        self.addToolBar(toolbar)
        
        action_arquivo = QAction("Arquivo", self)
        toolbar.addAction(action_arquivo)
        action_editar = QAction("Editar", self)
        toolbar.addAction(action_editar)
        action_busca = QAction("Busca", self)
        toolbar.addAction(action_busca)
        toolbar.addAction(QAction("Sair", self))
        
        
        self.aba_fluxogramas = FluxogramasWidget()
        #tabs.addTab(UsuarioWidget(), "Usuario")
        tabs.addTab(self.aba_fluxogramas, "Fluxogramas")
        self.aba_tags = TagsWidget()
        tabs.addTab(self.aba_tags, "Tags")
        self.aba_dados = DatasetsWidget()
        tabs.addTab(self.aba_dados, "Dados")
        self.aba_analises = AnalisesWidget()
        tabs.addTab(self.aba_analises, "Análises")
        #tabs.addTab(ConexoesWidget(), "Conexões")
        tabs.addTab(DocumentosWidget(), "Documentação")
       
        tabs.addTab(OrigensWidget(), "Fontes/Origens")
        #tabs.addTab(OrigensWidget(), "Origens")
        
        self.setCentralWidget(tabs)

"""
        for n, color in enumerate(["red", "green", "blue", "yellow"]):
        	tabs.addTab(WidgetGallery(), color)
  """      
        

