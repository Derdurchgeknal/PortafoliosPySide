import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtCore import Qt
from helpers import absPath
from ui_tabla import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # nos conectamos a la base de datos
        conexion = QSqlDatabase.addDatabase("QSQLITE")
        conexion.setDatabaseName(absPath("contactos.db"))
        if not conexion.open():
            print("No se puede conectar a la base de datos")
            sys.exit(True)

        # creamos el modelo
        self.modelo = QSqlTableModel()
        self.modelo.setTable("contactos")
        self.modelo.select()
        self.modelo.setHeaderData(0, Qt.Horizontal, "Id")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(2, Qt.Horizontal, "Empleo")
        self.modelo.setHeaderData(3, Qt.Horizontal, "Email")

        # configuramos la tabla
        self.tabla.setModel(self.modelo)
        self.tabla.resizeColumnsToContents()
        self.tabla.setColumnHidden(0, True)

        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tabla.selectionModel().selectionChanged.connect(self.seleccionar_fila)
        self.boton_modificar.clicked.connect(self.modificar_fila)
        self.boton_nuevo.clicked.connect(self.nueva_fila)
        self.boton_borrar.clicked.connect(self.borrar_fila)

        self.fila = -1

    def seleccionar_fila(self, seleccion):
        if seleccion.indexes():
            self.fila = seleccion.indexes()[0].row()
            nombre = self.modelo.index(self.fila, 1).data()
            empleo = self.modelo.index(self.fila, 2).data()
            email = self.modelo.index(self.fila, 3).data()
            self.line_nombre.setText(nombre)
            self.line_empleo.setText(empleo)
            self.line_email.setText(email)

    def modificar_fila(self):
        nombre = self.line_nombre.text()
        empleo = self.line_empleo.text()
        email = self.line_email.text()
        self.modelo.setData(self.modelo.index(self.fila, 1), nombre)
        self.modelo.setData(self.modelo.index(self.fila, 2), empleo)
        self.modelo.setData(self.modelo.index(self.fila, 3), email)
        self.modelo.submit()

    def nueva_fila(self):
        nombre = self.line_nombre.text()
        empleo = self.line_empleo.text()
        email = self.line_email.text()

        if len(nombre) > 0 and len(empleo) > 0 and len(email) > 0:
            nueva_fila = self.modelo.rowCount()
            self.modelo.insertRow(nueva_fila)
            self.modelo.setData(self.modelo.index(nueva_fila, 1), nombre)
            self.modelo.setData(self.modelo.index(nueva_fila, 2), empleo)
            self.modelo.setData(self.modelo.index(nueva_fila, 3), email)
            self.modelo.submit()
            self.line_nombre.setText("")
            self.line_empleo.setText("")
            self.line_email.setText("")

    def borrar_fila(self):
        if self.fila >= 0:
            self.modelo.removeRow(self.fila)
            self.modelo.select()
            self.fila = -1
            self.line_nombre.setText("")
            self.line_empleo.setText("")
            self.line_email.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
