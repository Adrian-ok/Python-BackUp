import sqlite3, pathlib, os
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QApplication, QFileDialog, QMessageBox
from DataBase import CRUD
from AutoBackUp import *

class Archivos():

    def __init__(self, _name, _destiny):
        self._name = _name 
        self._destiny = _destiny

    def NewFile(self):

        myCrud = CRUD()

        self._name = self.txtNameFile.text() #al self name le asigno lo que tengo en el text 

        if self._name != "": #verifico que no este vacio

            directorio = str(pathlib.Path(self._name).absolute()) #Guardo la direccion absoluta que igresa el usuario
            directorioF = directorio + "/" #al directorio le agreafo la / al final porque pathlib la quita

            files = [] #declaro la lista files

            for file in os.listdir(directorio): #recorro los archivos dentro del directorio os.listdir lista los archivos de la ruta pasada
                ruta = directorioF + file #Junto la ruta de la carpeta con el archivo en cuestion
                rutaF = ruta.replace("\\", "/")#Remplazo las barras \ por /

                files.append(rutaF)#Agrego la ruta terminada del archivo a la lista


            for i in files: #Recorro la lista de archivos

                mydata = i #Data a agregar a la bd
                myconnection = myCrud.ConectarDB() #Creo la conexion
                cursor = myconnection.cursor() #Creo el cursor

                cursor.execute("INSERT INTO RUTAS (RUTA) VALUES (?)",[mydata]) #Paso la consulta y los datos
                myconnection.commit()#Agrego el registro 
                myconnection.close()#Cierro la bd


            self.txtNameFile.clear() #Limpio el text
            Archivos.ReadFile(self, self.lastid) #Actualizo la tabla
        else:
            Archivos.Alert(self, 0)#Si esta vacio el text le mando una alerta

    def ReadFile(self, id_ruta): #Mostrar Rutas en la tabla
        myCrud = CRUD()

        if id_ruta > 0: #Si el id es mayor a 0 
            myquery = "SELECT * FROM RUTAS WHERE ID = " + str(id_ruta) + ";" #Actualizo la tabla solo para mostrar ese ultimo id ingresado
            index = self.tableF.rowCount()

        else:

            for indice, ancho in enumerate((10, 530), start=0): #Configuro el tamaño de la tabla
                self.tableF.setColumnWidth(indice, ancho)

            myquery = "SELECT * FROM RUTAS;" #Muestro todos los registros
            index = 0

        rutas = myCrud.Read(myquery) #Obtengo los registros de mi consulta

        for ruta in rutas: #Los cargo en la tabla
            ID = ruta[0]
            RUTA = ruta[1]

            self.tableF.setRowCount(index + 1)
            self.tableF.setItem(index, 0, QTableWidgetItem(str(ID)))
            self.tableF.setItem(index, 1, QTableWidgetItem(RUTA))
            index += 1

        myCrud.DisconnectDB() #Me desconecto de la bd

        return rutas


    def MostrarRutas(self): #Mostrar los archivos en la tabla
        Archivos.ReadFile(self, self.lastid) #LLamo a redfile y le paso sus parametros

    def BrowserFile2(self): #Abre el explorador de archivos para seleccionar la carpeta de destino
        destiny = QFileDialog.getExistingDirectory(self, "Select folder")
        self.txtDestiny.setText(destiny)

    def SaveDestiny(self): #Guardar el Destino Ingresado
        myCrud = CRUD()

        self._destiny = self.txtDestiny.text() #Destiny es igual a lo cargado en el text

        if self._destiny != "":#Controlo que no este vacio
            mydata = str(self._destiny) 
            myconnection = myCrud.ConectarDB()
            cursor = myconnection.cursor()

            cursor.execute("INSERT INTO DESTINO (RUTA_D) VALUES (?)",[mydata])
            myconnection.commit()
            myconnection.close()

            self.frame.hide() #Escondo le frame que contiene el buscador de destino
            self.btnFrame.show() #Vuelvo a mostrar el boton que habilita el frame, en caso de quiera cambiar el destino
        
        else:
            Archivos.Alert(self, 0)#Si esta vacio le Advierto

    def BrowserFiles(self): #Abro el explorador de archivos para indicarle la carpeta que contiene los archivos a copiar
        fileName = QFileDialog.getExistingDirectory(self, 'Select folder') 
        self.txtNameFile.setText(fileName)

    def VisibleFrame(self): #Funciona para mostrar y econder el frame y el boton
        self.frame.show()
        self.btnFrame.hide()

    def Alert(self, nroMsg): #Establesco las alertas
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

    def DeleteFile(self): #Borrar los registros cargados
        myCrud = CRUD()
        myquery = "DELETE FROM RUTAS WHERE ID = " + str(self.selectedId) + ";"
        myCrud.Delete(myquery)
        Archivos.ReadFile(self, 0)

    def clicked_tabla(self): #Seleccionar con click la fila a eliminar
        item = self.tableF.selectedItems() #En item guardo el item seleccionado
        self.rowTable = self.tableF.currentRow() #En rowtable guardo la cantidad de filas de la tabla
        self.selectedId = int(item[0].text()) #en selectedId el id de la fila
        print('itemm',int(item[0].text())) #Impresion de control
        self._name = item[1].text() 

    def BackUp(self): #BackUp se encarga de consultar rutas y archivos y las copia
        ruta = pathlib.Path("ArchivoBackUp.sqlite3").absolute()
        myconnection = sqlite3.connect(ruta)
        cursor = myconnection.cursor()
        myquery = "SELECT RUTA FROM RUTAS;"
        cursor.execute(myquery)
        result2 = cursor.fetchall()

        if len(result2) > 0: #Si la tabla rutas es igual a 0 esta vacia

            myquery2 = "SELECT RUTA_D FROM DESTINO;"
            cursor.execute(myquery2)
            result = cursor.fetchall()

            if len(result) > 0: #Si la tabla Destino ese igual a 0 esta vacia

                files = recuperarRutas() 
                # names = recuperarNom()
                destiny = RecuperarDestino()

                BackUp(files,destiny) #Llamo a backUp y le paso la ruta de destino del backup
                borrar(destiny) #llamo a borrar y le paso la ruta de destino del backup

                Archivos.Alert(self, 1) #Aviso BackUp Exitoso

            else:
                Archivos.Alert(self, 3) #Aviso que no hay destino
        
        else:
            Archivos.Alert(self, 2) #Aviso que no hay aarchivos para hacer backup