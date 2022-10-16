#-------------------------------------------
import os, ntpath
# listpath = []

# #-------------------------------------------
# item = "\\" #item que quiero agregar a la lista

path = "C:/Nueva carpeta/FILES/Libro1.xslx" 

# for i in range(len(path)):
#     listpath.append(path[i])

# print()
# print(listpath)
# print()

# for j in range(len(listpath)):
#     if listpath[j] == "/":
#         listpath[j] = item
        
# #-------------------------------------------


# print("el Item es: ", item)
# print()
# print(listpath)

res = os.path.normpath(path)
r = ntpath.basename(res)

print(r)