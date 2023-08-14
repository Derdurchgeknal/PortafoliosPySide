from PySide6 import QtCore, QtGui, QtWidgets
import PySide6.QtGui
from helpers import absPath
import random
import sys


class Carta(QtWidgets.QLabel):
    def __init__(self, imagenPath, numero, nombre, palo, parent=None):
        super().__init__(parent)

        self.imagenPath = imagenPath
        self.numero = numero
        self.nombre = nombre
        self.palo = palo
        self.visible = False

        self.imagen = QtGui.QPixmap(absPath("images/Reverso.png"))
        self.setPixmap(self.imagen)
        self.setScaledContents(True)

        self.anchoBase = self.sizeHint().width()
        self.altoBase = self.sizeHint().height()

        self.animaciones = QtCore.QParallelAnimationGroup()

    def mostrar(self):
        self.imagen = QtGui.QPixmap(absPath(f"images/{self.imagenPath}.png"))
        self.setPixmap(self.imagen)
        self.visible = True

    def esconder(self):
        self.imagen = QtGui.QPixmap(absPath("images/Reverso.png"))
        self.setPixmap(self.imagen)
        self.visible = False

    def posicionar(self, x, y, sobreponer=True):
        if sobreponer:  
            self.raise_()
        self.move(x, y)

    def mover(self, x, y, sobreponer=True, duracion=1000, escalado=1):
        self.animaciones = QtCore.QParallelAnimationGroup()
        if sobreponer:  
            self.raise_()
        pos = QtCore.QPropertyAnimation(self, b"pos")
        pos.setEndValue(QtCore.QPoint(x, y))
        pos.setDuration(duracion)
        self.animaciones.addAnimation(pos)

        size = QtCore.QPropertyAnimation(self, b"size")
        size.setStartValue(QtCore.QSize(self.anchoBase, self.altoBase))
        size.setEndValue(QtCore.QSize(self.anchoBase*escalado, self.altoBase*escalado))
        size.setDuration(duracion)
        self.animaciones.addAnimation(size)
        self.animaciones.start()

    def reestablecer(self):
        self.animaciones.stop()
        self.animaciones = QtCore.QParallelAnimationGroup()
        self.resize(self.anchoBase, self.altoBase)

    def mousePressEvent(self, event):
        if self.visible:
            print(f"{self.nombre} de {self.palo}")
        
class Baraja(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        nombres = ["As", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Siete", "Ocho", "Nueve", "Diez", "Jota", "Reina", "Rey"]
        palos = ["Tréboles", "Diamantes", "Corazones", "Picas"]
        self.cartas = []
        self.jugadas = []
        for palo in palos:
            for i, nombre in enumerate(nombres):
                carta = Carta(f"{i+1}{palo[0]}", i+1, nombre, palo, self)
                self.cartas.append(carta)
        self.mezclar()

    def extraer(self):
        if len(self.cartas) > 0:
            carta = self.cartas.pop()
            self.jugadas.append(carta)
            return carta

    def mezclar(self):
        random.shuffle(self.cartas)

    def reiniciar(self):
        for carta in self.jugadas:
            carta.esconder()
            carta.reestablecer() # propiedades visuales y animaciones
            self.cartas.append(carta)
        self.jugadas = []
        self.mezclar()
    

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 320)
        self.setStyleSheet("QMainWindow {background-color: #144b12}")

        self.baraja = Baraja(self)
        self.setCentralWidget(self.baraja)
        self.preparar()

        

        tomarBtn = QtWidgets.QPushButton("Tomar carta", self)
        tomarBtn.move(365, 15)
        tomarBtn.clicked.connect(self.tomar)

        reiniciarBtn = QtWidgets.QPushButton("Reiniciar juego", self)
        reiniciarBtn.move(250, 15)
        reiniciarBtn.clicked.connect(self.reiniciar)

    def preparar(self):
        offset = 0
        for carta in self.baraja.cartas:
            carta.posicionar(40+offset, 60+offset)
            offset += 0.25

    def tomar(self):
        carta = self.baraja.extraer()
        if carta:
            carta.mover(300, 110, duracion=750, escalado=0.75)
            carta.mostrar()

    def reiniciar(self):
        self.baraja.reiniciar()
        self.preparar()
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    # exec_() si PySide6 < 6.1.0 (pip install --upgrade pyside6)
