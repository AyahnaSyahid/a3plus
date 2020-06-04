from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui, uic

FileDialog = QtWidgets.QFileDialog

def create_shortcut(sequence, objs):
    return QtWidgets.QShortcut(QtGui.QKeySequence(sequence),objs)

class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Exporter2.ui", self)
        self.initialize()
        self.init_connection()
        self.init_shortcut()
        
    def initialize(self):
        self.l_src.setText('-*-')
        self.l_target.setText('-*-')
        self.le_klien.setText('Test')
        
    def init_connection(self):
        self.b_browse.clicked.connect(self.select_directory)
        self.b_export.clicked.connect(lambda : print("Clicked"))
    
    def init_shortcut(self):
        # TODO: Make editable later
        create_shortcut("Ctrl+k", self).activated.connect(
                            lambda : self.le_klien.setFocus())
        create_shortcut("Ctrl+f", self).activated.connect(
                            lambda : self.le_namafile.setFocus())
        create_shortcut("Ctrl+b", self).activated.connect(
                            lambda : self.le_bahan.setFocus())
        create_shortcut("Ctrl+p", self).activated.connect(
                            lambda : self.le_pages.setFocus())
        create_shortcut("Ctrl+q", self).activated.connect(
                            lambda : self.le_qty.setFocus())
        create_shortcut("Ctrl+e", self).activated.connect(
                            lambda : self.b_export.click() if (
                                self.stackedWidget.currentIndex() == 0 ) and self.b_export.isEnabled() else None)
        
    
    def select_directory(self):
        dname = FileDialog.getExistingDirectory(self, "Pilih Folder", self.le_exportfolder.text())
        if dname:
            self.le_exportfolder.setText(dname)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = AppWindow()
    Window.show()
    app.exec_()
