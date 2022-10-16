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

    def Delete(self, myquery):
        try:
            self.myconnection = self.ConectarDB()
            cursor = self.myconnection.cursor()
            cursor.execute(myquery)
            self.myconnection.commit()
            cursor.close()
            self.myconnection.close()
        except Exception as miError:
            print('Error:',miError)

    def ConectarDB(self):
        return sqlite3.connect("ArchivoBackUp.sqlite3")

    def DisconnectDB(self):
        self.myconnection.close()
