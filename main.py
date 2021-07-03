from PyQt5 import QtWidgets
from front import Ui_Dialog
import sys

class window(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #initialization design


app = QtWidgets.QApplication([]) #new copy QApplication
application = window()
application.show() #show window

#app.exec_ - start app
#sys.exit - cycle
sys.exit(app.exec_())