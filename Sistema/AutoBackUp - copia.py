#---------------------------------------------------------------------------
#Importaciones
from logging import exception
import re
import sqlite3
import shutil
from datetime import date


#---------------------------------------------------------------------------
#Funciones

def recuperarRutas():

    rutasFiles = []

    #Consulta para obtener las rutas
    myconnection = sqlite3.connect("ArchivoBackUp.sqlite3")
    cursor = myconnection.cursor()

    myquery = "SELECT RUTA FROM RUTAS;"
    cursor.execute(myquery)

    result = cursor.fetchall()
    #------------------------------------------------------

    for i in result: #Recorro las rutas encontradas

        road = str(i) #En road guardo la ruta 

        #Guardo los caracteres que quiero borrar, ya que la consulta me devuelve la ruta pero con
        #caracteres de mas como los () y las '
        characters_to_remove = "(),'" 

        pattern = "[" + characters_to_remove + "]"
        finishRoad = re.sub(pattern, "", road)#con Re.sub puedo borrar varios caracteres indicados anteriormente

        rutasFiles.append(finishRoad)#Agrego la ruta sin caracteres de mas a mi lista rutasFiles
    
    return rutasFiles #retorno la lista

def recuperarNom():

    #Consulta para obtener rutas 
    nameFiles = []

    myconnection = sqlite3.connect("ArchivoBackUp.sqlite3")
    cursor = myconnection.cursor()

    myquery = "SELECT RUTA FROM RUTAS;"
    cursor.execute(myquery)

    result = cursor.fetchall()
    #------------------------------------------------------

    for i in result: #Recorro las rutas
        name = str(i) 

        nameBarra = 23 #nameBarra me guarda la posicion en la cual esta la ultima / de mi ruta, va a variar dependiendo la carpeta 
        namex = name.index(".") #NameX hace lo mismo solo que ocupo .index para que me devuelva la posicion del . de la extencion .xlsx

        nameFinal = name[nameBarra : namex ] #extraigo el nombre del archivo que esta entre la / y el . de mi ruta

        nameFiles.append(nameFinal) #agrego nameFinal a la lista
    
    return nameFiles

def RecuperarDestino():

    myconnection = sqlite3.connect("ArchivoBackUp.sqlite3")
    cursor = myconnection.cursor()

    myquery = "SELECT RUTA_D FROM DESTINO WHERE ID = (SELECT MAX(ID) FROM DESTINO);"
    cursor.execute(myquery)

    result = cursor.fetchall()
    r = str(result)

    characters_to_remove = "()," 

    pattern = "[" + characters_to_remove + "]" 
    finishResult = re.sub(pattern, "", r)


    return str(finishResult)

def BackUp(list, name):
    
    fechaBackUp = date.today() #declaro la fecha actual
    strFechaBackUp = str(fechaBackUp).replace("-",".") #remplazo guiones

    for i in range(0,len(list)): #como ambas listas tienen la misma longitud recorro con un mismo for
        print(list[i], name[i])
        

        rutaEntrada = list[i] #ruta de entrada 
        rutaDestino = 'F:\TRABAJO\BackUp_Excel\Copias' + '\\' + f"BackUp {strFechaBackUp} - {name[i]}.xlsx" #ruta salida con fecha y nombre del archivo, Verificar antes de ejecutar

        print("POR ACA PASO")

        shutil.copyfile(rutaEntrada, rutaDestino) #shutil copia los archivos
        i+=1

#----------------------------------------------------------------------------
#Ejecucion

files = recuperarRutas()
names = recuperarNom()
destino = RecuperarDestino()

chars = ['[', ']']

res = destino.translate(str.maketrans('', '', ''.join(chars)))

destiny = res.replace("/", '\\')

print(destiny)

BackUp(files,names)





#BackUp(files)