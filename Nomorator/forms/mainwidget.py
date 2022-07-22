from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QColorDialog, QFontDialog, QFontComboBox, QFileDialog
from PyQt5.QtGui import QColor, QPixmap, QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QThread, QSize, QFile
from nomorator.nomorator import Nomorator

from pathlib import Path

UIFILE = Path(__file__).parent.resolve() / "mainwidget.ui"


class MainWidget(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi(UIFILE, self)
        self.prog.setHidden(True)
        self.outFontColor = QColor(0, 0, 0, 255)
        self.update_chColor(self.outFontColor)
        self.getFromFile = None

    @pyqtSlot(str)
    def saved_messages(self, msg):
        QMessageBox.information(self, "Info", msg)
        saveTo, _filter = QFileDialog.getSaveFileName(self, "Simpan sebagai", "", "PDF (*.pdf)")
        if len(saveTo):
            QFile(msg).rename(saveTo)
        else:
            QFile(msg).remove()

    def generatedSettings(self) -> dict:
        ret = dict()
        ret["ukHalamanW"] = self.lHal.value() or 318
        ret["ukHalamanH"] = self.tHal.value() or 475
        ret["offsetW"] = self.lOffset.value() or 1
        ret["offsetH"] = self.tOffset.value() or 1
        ret["fromFile"] = self.frFile.isChecked()
        ret["fileName"] = self.getFromFile
        ret["posX"] = self.posx.value() or 0
        ret["posY"] = self.posy.value() or 0
        ret["startNum"] = self.startN.value() or 0
        ret["stopNum"] = self.stopN.value() or 100
        ret["fDigit"] = self.digit.value() or 0
        ret["prefix"] = self.pref.text() or ""
        ret["suffix"] = self.suff.text() or ""
        ret["grid1"] = self.grid1.value() or 1
        ret["grid2"] = self.grid2.value() or 1
        ret["colorMode"] = self.imode.currentText() or "RGB"
        ret["imageDpi"] = self.dpi.value() or 254
        ret["outputDir"] = UIFILE.parent
        ret["font"] = self.ftBox.currentFont()
        ret["font-color"] = self.outFontColor
        ret["font-size"] = self.ftSize.value()
        ret["useDuplicate"] = self.duplikasi.isChecked()
        ret["dupX"] = self.dupX.value()
        ret["dupY"] = self.dupY.value()
        return ret

    @pyqtSlot()
    def on_go_clicked(self):
        self.nomorator = Nomorator(self.generatedSettings())
        self.worker = QThread()
        self.nomorator.moveToThread(self.worker)
        self.worker.started.connect(self.nomorator.doJobs)
        self.worker.started.connect(lambda : self.prog.setHidden(False))
        self.nomorator.finished.connect(self.worker.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(lambda :self.prog.setHidden(True))
        self.nomorator.finished.connect(self.nomorator.deleteLater)
        self.nomorator.messages[str].connect(self.saved_messages)
        self.worker.start()

    @pyqtSlot()
    def on_chColor_clicked(self):
        newColor = QColorDialog.getColor(self.outFontColor, self, "Ubah warna font")
        if newColor.isValid() and self.outFontColor != newColor:
            self.update_chColor(newColor)
            self.outFontColor = newColor

    @pyqtSlot(QColor)
    def update_chColor(self, clr):
        size: QSize = self.chColor.geometry().size()
        pxm = QPixmap(20, 20)
        pxm.fill(clr)
        self.chColor.setIcon(QIcon(pxm))

    @pyqtSlot()
    def on_chFont_clicked(self):
        cbf: QFontComboBox = self.ftBox
        newFont: QFont = QFontDialog.getFont(cbf.currentFont(), self, "Pilih Font")
        if newFont[0] != cbf.currentFont():
            cbf.setCurrentFont(newFont[0])
            self.ftSize.setValue(newFont[0].pointSizeF())

    @pyqtSlot(bool)
    def on_frFile_toggled(self, state):
        if state:
            f, _filt = QFileDialog.getOpenFileName(self, "Pilih file")
            self.getFromFile = f
            if not len(f):
                self.getFromFile = None
                self.frFile.setChecked(False)
            else:
                self.srcFile.setText(f)
                self.startN.setDisabled(True)
                self.stopN.setDisabled(True)
                self.digit.setDisabled(True)
        else :
            self.getFromFile = None
            self.startN.setDisabled(False)
            self.stopN.setDisabled(False)
            self.digit.setDisabled(False)
