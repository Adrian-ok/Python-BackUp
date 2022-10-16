from distutils import errors
import sqlite3

class CRUD(object):

    def __init__(self):
        self.myconnection = ""
        return

    def Read(self, myquery):
        self.myconnection = self.ConectarDB()
        self.myconnection.text_factory = lambda b: b.decode(errors = 'ignore')
        result = self.myconnection.execute(myquery)
        return result

    def ConectarDB(self):
        return sqlite3.connect("ArchivoBackUp.sqlite3")

    def DisconnectDB(self):
        self.myconnection.close()
