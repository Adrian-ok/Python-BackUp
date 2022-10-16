import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget
from Sistema.Archivo import Archivos
from PyQt5.uic import loadUi

#---------------------------------------------------------------------------------

from Sistema.Archivo import Archivos

class MainWindow(QMainWindow):
      def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            loadUi("BackUp.ui", self)

            self.frame.hide()

            self.lastid = 0

            self.btnSave.clicked.connect(lambda: Archivos.NewFile(self))
            self.btnFrame.clicked.connect(lambda: Archivos.VisibleFrame(self))
            self.btnSave_2.clicked.connect(lambda: Archivos.SaveDestiny(self))
            self.btnBrowse.clicked.connect(lambda: Archivos.BrowserFiles(self))
            self.btnBrowse_2.clicked.connect(lambda: Archivos.BrowserFile2(self))
            self.btnRefresh.clicked.connect(lambda: Archivos.ReadFile(self, self.lastid))
            Archivos.MostrarRutas(self)


#---------------------------------------------------------------------------------
# EJECUCION
if __name__ == "__main__":
    mi_aplicacion = QApplication(sys.argv)
    mi_app = MainWindow()
    mi_app.show()
    sys.exit(mi_aplicacion.exec_())