from operator import index
import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QApplication, QFileDialog
from DataBase.DataBase import CRUD

class Archivos():

    def __init__(self, _name, _destiny):
        self._name = _name
        self._destiny = _destiny

    def NewFile(self):

        myCrud = CRUD()

        self._name = self.txtNameFile.text()
        mydata = str(self._name)
        myconnection = myCrud.ConectarDB()
        cursor = myconnection.cursor()

        cursor.execute("INSERT INTO RUTAS (RUTA) VALUES (?)",[mydata])
        myconnection.commit()
        myconnection.close()

        self.txtNameFile.clear()
        Archivos.ReadFile(self, self.lastid)

    def ReadFile(self, id_ruta):

        myCrud = CRUD()

        if id_ruta > 0:
            myquery = "SELECT * FROM RUTAS WHERE ID = " + str(id_ruta) + ";"
            index = self.tableF.rowCount()

        else:

            for indice, ancho in enumerate((10, 300), start=0):
                self.tableF.setColumnWidth(indice, ancho)

            myquery = "SELECT * FROM RUTAS;"
            index = 0

        rutas = myCrud.Read(myquery)

        for ruta in rutas:
            ID = ruta[0]
            RUTA = ruta[1]

            self.tableF.setRowCount(index + 1)
            self.tableF.setItem(index, 0, QTableWidgetItem(str(ID)))
            self.tableF.setItem(index, 1, QTableWidgetItem(RUTA))
            index += 1

        myCrud.DisconnectDB()

        return rutas


    def MostrarRutas(self):
        Archivos.ReadFile(self, 0)

    def BrowserFile2(self):
        destiny = QFileDialog.getExistingDirectory(self, "Select folder")
        self.txtDestiny.setText(destiny)

    def SaveDestiny(self):
        myCrud = CRUD()

        self._destiny = self.txtDestiny.text()
        mydata = str(self._destiny)
        myconnection = myCrud.ConectarDB()
        cursor = myconnection.cursor()

        cursor.execute("INSERT INTO DESTINO (RUTA_D) VALUES (?)",[mydata])
        myconnection.commit()
        myconnection.close()

        self.frame.hide()

    def BrowserFiles(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file') #verificar la ruta antes de ejecutar
        self.txtNameFile.setText(fileName[0])

    def VisibleFrame(self):
        self.frame.show()
        self.btnFrame.hide()