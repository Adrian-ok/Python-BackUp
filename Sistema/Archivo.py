import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QApplication, QFileDialog, QMessageBox
from DataBase.DataBase import CRUD
from AutoBackUp import *

class Archivos():

    def __init__(self, _name, _destiny):
        self._name = _name
        self._destiny = _destiny

    def NewFile(self):

        myCrud = CRUD()

        self._name = self.txtNameFile.text()

        if self._name != "":
            mydata = str(self._name)
            myconnection = myCrud.ConectarDB()
            cursor = myconnection.cursor()

            cursor.execute("INSERT INTO RUTAS (RUTA) VALUES (?)",[mydata])
            myconnection.commit()
            myconnection.close()

            self.txtNameFile.clear()
            Archivos.ReadFile(self, self.lastid)
        else:
            Archivos.Alert(self, 0)
            print("Error")

    def ReadFile(self, id_ruta):
        myCrud = CRUD()

        if id_ruta > 0:
            myquery = "SELECT * FROM RUTAS WHERE ID = " + str(id_ruta) + ";"
            index = self.tableF.rowCount()

        else:

            for indice, ancho in enumerate((10, 530), start=0):
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
        Archivos.ReadFile(self, self.lastid)

    def BrowserFile2(self):
        destiny = QFileDialog.getExistingDirectory(self, "Select folder")
        self.txtDestiny.setText(destiny)

    def SaveDestiny(self):
        myCrud = CRUD()

        self._destiny = self.txtDestiny.text()

        if self._destiny != "":
            mydata = str(self._destiny)
            myconnection = myCrud.ConectarDB()
            cursor = myconnection.cursor()

            cursor.execute("INSERT INTO DESTINO (RUTA_D) VALUES (?)",[mydata])
            myconnection.commit()
            myconnection.close()

            self.frame.hide()
            self.btnFrame.show()
        else:
            Archivos.Alert(self, 0)

    def BrowserFiles(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file') #verificar la ruta antes de ejecutar
        self.txtNameFile.setText(fileName[0])

    def VisibleFrame(self):
        self.frame.show()
        self.btnFrame.hide()

    def Alert(self, nroMsg):
        if nroMsg == 0:
            msgWarning = QMessageBox.warning(self, 'Error Campo Vacio', "Campo Vacio Ingrese un dato Por favor", QMessageBox.Ok)
            return msgWarning
        elif nroMsg == 1:
            msgOk = QMessageBox.information(self, 'BackUp', "BackUp Exitoso", QMessageBox.Ok)
            return msgOk
        elif nroMsg == 2:
            msgArchivos = QMessageBox.warning(self, 'Error Archivos', "No hay Archivos cargados", QMessageBox.Ok)
            return msgArchivos
        else:
            msgDestino = QMessageBox.warning(self, 'Error Destino', "No hay Destino cargado", QMessageBox.Ok)
            return msgDestino

    def DeleteFile(self):
        myCrud = CRUD()
        myquery = "DELETE FROM RUTAS WHERE ID = " + str(self.selectedId) + ";"
        myCrud.Delete(myquery)
        Archivos.ReadFile(self, 0)

    def clicked_tabla(self):
        item = self.tableF.selectedItems()
        self.rowTable = self.tableF.currentRow()
        self.selectedId = int(item[0].text())
        print('itemm',int(item[0].text()))
        self._name = item[1].text()

    def ClickTableView(self):
        myconnection = sqlite3.connect("AchivoBackUp.sqlite3")
        cursor = myconnection.cursor()

        files =cursor.fetchall()
        myconnection.close() 
        for file in files:
            self._name = file[1]
        self.txtNameFile.setText(self._name)

    def BackUp(self):

        myconnection = sqlite3.connect("ArchivoBackUp.sqlite3")
        cursor = myconnection.cursor()
        myquery = "SELECT RUTA FROM RUTAS;"
        cursor.execute(myquery)
        result2 = cursor.fetchall()

        if len(result2) > 0:

            myquery2 = "SELECT RUTA_D FROM DESTINO;"
            cursor.execute(myquery2)
            result = cursor.fetchall()

            if len(result) > 0:

                files = recuperarRutas()
                names = recuperarNom()
                destiny = RecuperarDestino()

                BackUp(files, names, destiny)

                Archivos.Alert(self, 1)

            else:
                Archivos.Alert(self, 3)
        
        else:
            Archivos.Alert(self, 2)