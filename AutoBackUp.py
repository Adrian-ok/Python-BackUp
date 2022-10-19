#---------------------------------------------------------------------------
#Importaciones
from posixpath import abspath
import re, sqlite3, shutil, os, ntpath, pathlib, zipfile, zlib
from datetime import date,datetime


#---------------------------------------------------------------------------
#Funciones

def recuperarRutas():

    rutasFiles = []
    ruta = pathlib.Path("ArchivoBackUp.sqlite3").absolute()
    #Consulta para obtener las rutas
    myconnection = sqlite3.connect(ruta)
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

# def recuperarNom():

#     #Consulta para obtener rutas 
#     nameFiles = []
#     ruta = pathlib.Path("ArchivoBackUp.sqlite3").absolute()
#     myconnection = sqlite3.connect(ruta)
#     cursor = myconnection.cursor()

#     myquery = "SELECT RUTA FROM RUTAS;"
#     cursor.execute(myquery)

#     result = cursor.fetchall()
#     #------------------------------------------------------

#     for i in result: #Recorro las rutas para quitar el nombre
#         name = str(i) 

#         characters_to_remove = "(',)" 
#         pattern = "[" + characters_to_remove + "]" 
#         res = re.sub(pattern, "", name)

#         nameFinal = ntpath.basename(res) #NtPath me devuelve solamente el nombre del archivo
#         nameFiles.append(nameFinal) #agrego solamente el nombre a la lista
    
#     return nameFiles

def RecuperarDestino():
    ruta = pathlib.Path("ArchivoBackUp.sqlite3").absolute()
    myconnection = sqlite3.connect(ruta)
    cursor = myconnection.cursor()

    myquery = "SELECT RUTA_D FROM DESTINO WHERE ID = (SELECT MAX(ID) FROM DESTINO);"
    cursor.execute(myquery)

    result = cursor.fetchall()
    r = str(result)

    chars = ['[', ']', "'", "'", ",", "(", ")"] #Cargo los caracteres a eliminar en una lista 
    res = r.translate(str.maketrans('', '', ''.join(chars))) #Recuperar destino me devuelve el string pero con [] y '' asi que aca se los saco 
    destiny = os.path.normpath(res) #Os.path hace el trabajo de pasar las  / a \

    return destiny

def BackUp(list, dest):
    
    fechaBackUp = date.today()#declaro la fecha actual
    # strFechaBackUp = str(fechaBackUp).replace("-","/") #remplazo guiones
    print(fechaBackUp)


    nuevoRar = zipfile.ZipFile(dest + "\\" + f"BackUp {fechaBackUp}.rar", 'w')

    for i in range(0,len(list)): #como ambas listas tienen la misma longitud recorro con un mismo for
        print(list[i])

        nuevoRar.write(list[i], compress_type=zipfile.ZIP_DEFLATED)
        
        # rutaEntrada = list[i] #ruta de entrada 
        # rutaDestino = dest + '\\' + f"BackUp {name[i]}" #ruta salida con fecha y nombre del archivo, Verificar antes de ejecutar
        # print("POR ACA PASO 3")
        # print(rutaDestino)
        # shutil.copyfile(rutaEntrada, rutaDestino) #shutil copia los archivos
        i+=1

    nuevoRar.close()
    # shutil.make_archive(str(dest + "\\" + f"BackUp {strFechaBackUp}"), "zip", dest)

def borrar(dest):

    hoy = str(date.today())

    for file in os.listdir(dest):
        p = os.path.join(dest, file) # junto la ruta con el nombre del archivo

        i = file.index("2")#en i guardo el nro de indice que ocupa el numero 2 en el nombre del archivo
        j = file.index(".")#en j lo mismo pero del .

        result = file[i:j]#result es igual a lo que esta entre i y j (seria la fecha del archivo)

        a = datetime.strptime(result, '%Y-%m-%d') #le doy formato fecha al result para poder operar luego
        b = datetime.strptime(hoy, '%Y-%m-%d')   #lo mismo con la fehca de hoy

        dif_fecha = (b - a).days #resto la fecha actual y la del archivo para obtener la diferencia en dias

        if dif_fecha >= 15:#si la diferencia es igual o mayor a 15 borro el archivo
            os.remove(p)







#----------------------------------------------------------------------------
#Ejecucion

# files = recuperarRutas()
# names = recuperarNom()
# destino = RecuperarDestino()

# print(destino)

# chars = ['[', ']', "'", "'", ",", "(", ")"] #Cargo los caracteres a eliminar en una lista 

# res = destino.translate(str.maketrans('', '', ''.join(chars))) #Recuperar destino me devuelve el string pero con [] y '' asi que aca se los saco 

# destiny = os.path.normpath(res) #Os.path hace el trabajo de pasar las  / a \ 

# print(destiny)

# BackUp(files, names, destino)

# ruta = pathlib.Path("ArchivoBackUp.sqlite3").absolute()

# print(ruta)





#BackUp(files)