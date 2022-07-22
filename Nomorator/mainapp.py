from PyQt5.QtWidgets import QApplication
import sys
from forms.mainwidget import MainWidget

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    mainwg = MainWidget()
    mainwg.show()
    app.exec()