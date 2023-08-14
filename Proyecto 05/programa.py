from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLCDNumber, QPushButton)
from functools import partial
from helpers import *

class Calculadora(QLCDNumber):
    def __init__(self):
        super().__init__(digitCount=12, segmentStyle=QLCDNumber.Flat)
        self.texto = "0"
        self.reiniciar = False

    def escribir(self, caracter):
        if self.reiniciar:
            self.limpiar()

        if caracter == '.' and self.texto.count('.') ==1:
            return
        
        if len(self.texto) <= 12:
            self.texto += caracter
            self.display(self.texto.lstrip('0'))

    def preparar(self, operacion):
        self.operacion = operacion
        self.memoria = float(self.texto)
        self.limpiar()
        print(self.operacion, self.memoria)

    def calcular(self):

        resultado = 0.0

        if self.operacion == "+":
            resultado = self.memoria + float(self.texto)
        elif self.operacion == "-":
            resultado = self.memoria - float(self.texto)
        elif self.operacion == "×":
            resultado = self.memoria * float(self.texto)
        elif self.operacion == "÷":
            resultado = self.memoria / float(self.texto)

        self.texto = str(round(resultado, 2))
        if len(self.texto) > 12:
            self.texto = 'Error'
        self.display(self.texto)
        self.reiniciar = True

    def limpiar(self):
        self.texto = '0'
        self.display(self.texto)
        self.reiniciar = False

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(480)
        self.setFixedHeight(360)
        self.setWindowTitle("Calculadora")
        with open(absPath("Scalcula.qss")) as styles:
            self.setStyleSheet(styles.read())

        self.setLayout(QGridLayout())
        self.calculadora = Calculadora()
        self.layout().addWidget(self.calculadora, 0, 0, 1, 0)

        simbolos = [['7', '8', '9', '÷'], ['4', '5', '6', '×'],
                    ['1', '2', '3', '-'], ['.', '0', '=', '+']]

        for i, fila in enumerate(simbolos):
            for j, simbolo in enumerate(fila):
                boton = QPushButton(simbolo)
                boton.setStyleSheet("height:50px;font-size:25px;")
                boton.clicked.connect(partial(self.boton_clicado, simbolo))
                self.layout().addWidget(boton, i+1, j)

    def boton_clicado(self, simbolo):
        if simbolo.isdigit() or simbolo == '.':
            self.calculadora.escribir(simbolo)
        elif simbolo == '=':
            self.calculadora.calcular()
        else:
            self.calculadora.preparar(simbolo)



if __name__ == '__main__':
    app = QApplication()
    window = Window()
    window.show()
    app.exec_()
