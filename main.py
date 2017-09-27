import sys
from PyQt5 import QtWidgets
from app import App

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    applikation = App()
    sys.exit(app.exec_())