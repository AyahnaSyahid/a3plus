from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QObject
import sys
from pathlib import Path

def get_resources(fname):
    try:
        return str(Path(sys._MEIPASS) / fname)
    except:
        return str(Path(__file__).parent / fname)


def HLine(parent):
    line = QFrame(parent)
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    line.setFixedHeight(10)
    return line

class CSVGenMainWin(QMainWindow):
    inputChanged = pyqtSignal()
    argState = None
    lastSaveLocation = None

    def __init__(self, *args, **kwargs):
        super(CSVGenMainWin, self).__init__(*args, **kwargs)
        centralW = QWidget()
        outerLayout = QVBoxLayout(centralW)
        self.setCentralWidget(centralW)

        centralW.setLayout(outerLayout)
        self.fromNumber = QHBoxLayout()
        self.fieldCount = QHBoxLayout()
        self.pageCount = QHBoxLayout()
        self.fstring = QGridLayout()
        self.command = QHBoxLayout()

        self.sp_from = QSpinBox(self)
        self.sp_from.setMaximum(999999)
        self.sp_from.valueChanged.connect(self.update_preview)

        self.sp_field = QSpinBox(self)
        self.sp_field.setMinimum(1)
        self.sp_field.setMaximum(256)
        self.sp_field.valueChanged.connect(self.update_preview)

        self.sp_page = QSpinBox(self)
        self.sp_page.setMaximum(5000)
        self.sp_page.setMinimum(1)
        self.sp_page.valueChanged.connect(self.update_preview)


        self.prefix = QLineEdit()
        self.prefix.setMaximumWidth(80)
        self.prefix.setToolTip("Karakter Tambahan sebelum Nomor")
        self.prefix.textChanged.connect(self.update_preview)

        self.spec = QLineEdit("04")
        self.spec.setMaximumWidth(80)
        self.spec.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.spec.setToolTip("Format (perataan dan atau padding) Nomor\n biarkan kosongberarti tanpa perataan")
        self.spec.textChanged.connect(self.update_preview)

        self.suffix = QLineEdit()
        self.suffix.setMaximumWidth(80)
        self.suffix.setToolTip("Karakter tambahan setelah Nomor")
        self.suffix.textChanged.connect(self.update_preview)

        self.lpreview = QLabel("<PREVIEW>")
        self.lpreview.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lpreview.setMinimumHeight(42)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_button_clicked)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_button_clicked)

        self.fromNumber.addWidget(QLabel("Mulai dari"))
        self.fromNumber.addWidget(self.sp_from)
        self.fieldCount.addWidget(QLabel("Jumlah isian"))
        self.fieldCount.addWidget(self.sp_field)
        self.pageCount.addWidget(QLabel("Jumlah halaman"))
        self.pageCount.addWidget(self.sp_page)
        self.fstring.addWidget(self.prefix,1, 0)
        self.fstring.addWidget(self.spec,1, 1)
        self.fstring.addWidget(self.suffix,1, 2)
        self.fstring.addWidget(QLabel("Prefix"), 0, 0)
        self.fstring.addWidget(QLabel("Spec"), 0, 1)
        self.fstring.addWidget(QLabel("Suffix"), 0, 2)
        self.command.addSpacerItem(QSpacerItem(85, 20))
        self.command.addWidget(self.save_button)
        self.command.addWidget(self.exit_button)

        outerLayout.addLayout(self.fromNumber)
        outerLayout.addLayout(self.fieldCount)
        outerLayout.addLayout(self.pageCount)
        outerLayout.addWidget(HLine(self))
        outerLayout.addLayout(self.fstring)
        outerLayout.addWidget(HLine(self))
        outerLayout.addWidget(self.lpreview)
        outerLayout.addWidget(HLine(self))
        outerLayout.addLayout(self.command)
        self.setFixedSize(self.sizeHint())

## SLOT PART
    def update_preview(self):
        _st = self.sp_from.value()
        _fd = self.sp_field.value()
        _pg = self.sp_page.value()
        _ed = _st + (_fd * _pg) - 1
        _fm = "{:" + self.spec.text() + "}"
        try:
            G = self.prefix.text() + _fm + self.suffix.text()
            fmtd = G.format(_st) + '  ->  ' + G.format(_ed) + '\n' + 'Total {} '.format(_fd * _pg)
            self.argState = True, (_st, _fd, _pg, "\"" + G + "\"")
        except :
            self.argState = None
            print("Debug :", _fm)
        if self.argState[0] is True:
            self.lpreview.setText(fmtd)
        else:
            self.lpreview.setText("Tidak dapat memformat nomor #{}".format(_fm))



    def save_button_clicked(self):
        if self.argState is None:
            msg = QMessageBox()
            msg.setText("Ada kesalahan pada parameter yang anda masukan !!")
            msg.exec_()
            return
        writeTo, _ = QFileDialog.getSaveFileName(self, self.lastSaveLocation or '.', filter="CSV (*.csv);;All (*.*)")
        s, fd, pg, fm = self.argState[1]
        # ------------  Arr Creations --------------
        hdr = [["F{}".format(x) for x in range(1, fd + 1)]]
        array_numbers = [[(i * pg) + n + s for i in range(fd)] for n in range(pg)]
        if not writeTo.strip():
            return
        with open(writeTo, 'w') as wt:
            wt.write(';'.join(hdr[0]) + '\n')
            for line in array_numbers:
                wt.write(';'.join([fm.format(chunk) for chunk in line]) + "\n")

        from pathlib import Path
        self.lastSaveLocation = str(Path(writeTo).parent)

    def exit_button_clicked(self):
        ans = QMessageBox.question(self, "Keluar ?", "Keluar dari aplikasi",\
                                   QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.close()
        else:
            pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName("CSVGen")
    app.setWindowIcon(QIcon(get_resources("CSVGen.ico")))
    app.setStyle('Fusion')
    mainWin = CSVGenMainWin()
    mainWin.show()
    app.exec_()