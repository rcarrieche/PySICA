# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:57:58 2022

@author: nato
"""
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout

import sys

global i
i = 1
def kkk():
    global i
    print("kkkkkk {}".format(i))
    i = i+1

global a
class TesteJanelaPrincipal(QMainWindow):
    print("lalala 1")
    
    def __init__(self, *args, **kwargs):
        self.a = 0
        print("lalala 2")
        super(TesteJanelaPrincipal, self).__init__(*args, **kwargs)
        print("lalala 3")
        self.setWindowTitle("Teste janela jkjsdfklklfd")
        label = QLabel("teste LABEL")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
        self.button = QPushButton("teste botão")
        #button.setCheckable(True)
        #button.pressed.connect(self.close)
        self.button.clicked.connect(self.botao_clicado)
        self.button.released.connect(kkk)
        #self.setFixedSize(400, 300)
        self.setFixedSize(QSize(400, 300))
        self.setCentralWidget(self.button)
        vbox = QVBoxLayout()
        vbox.addWidget(TesteJanela2().show())
        vbox.addWidget(self.button)
        self.setLayout(vbox)
   
    def botao_clicado(self, checado):
        self.a = self.a + 1
        print("Checado? ", checado)
        print("clicou {}x".format(self.a))
        self.setWindowTitle("clicou já era... {}x".format(self.a))
        if self.a % 2 == 0:
            self.button.setText("licou {} pares".format(self.a/2))

class TesteJanela2(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(TesteJanela2, self).__init__(*args, **kwargs)
        self.label = QLabel("Clique aqui")
        self.setCentralWidget(self.label)
        self.setFixedSize(QSize(400, 300))
        
    def mousePressEvent(self, e):
        self.label.setText("Tá segurando")
    def mouseReleaseEvent(self, e):
        self.label.setText("Soltou mouse!")
    def mouseDoubleClickEvent(self, e):
        print(e)
        self.label.setText("Clique duplo!!!")
    def mouseMoveEvent(self, e):
        print(e)
        self.label.setText("rato se mexendo!")
        

app = QApplication(sys.argv)
window = TesteJanelaPrincipal()
window.show()
app.exec()

"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Teste título")

        button = QPushButton("teste botão")
        button.pressed.connect(self.close)

        self.setCentralWidget(button)
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()

"""