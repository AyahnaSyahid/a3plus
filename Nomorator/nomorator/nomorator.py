from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDateTime, QSizeF, Qt, QPointF
from PyQt5.QtGui import QPageSize, QPainter
from PyQt5.QtPrintSupport import QPrinter


def PXtoMM(pxValue, dpi):
    inch = pxValue / dpi
    return inch * 25.4

def MMtoPX(mmvalue, dpi):
    return mmvalue / 25.4 * dpi

def CMtoPX(cmval, dpi):
    return cmval / 2.54 * dpi

def PXtoCM(pxval, dpi):
    return pxval / dpi * 2.54

def serial_generator(first, last, dlength, prefix, suffix, grid1=1, grid2=1, reverse=True):

    if last is None:
        with open(first[0]) as opf:
            for line in opf:
                yield line.strip()
        return

    fmt = f"{prefix}{{:0>{dlength}}}{suffix}"
    count = last - first + 1
    page_count, rest = divmod(count, grid1 * grid2)
    page_count += 1 if rest else 0
    current_page = 0 if not reverse else page_count

    #   0   5  10  15  20
    #  25  30  35  40  45
    #  50  55  60  65  70
    #  75  80  85  90  95
    # 100 105 110 115 120

    while True:
        for r in range(int(grid2)):
            for c in range(int(grid1)):
                num = (c * page_count) + (r * grid1 * page_count) + current_page
                yield fmt.format(num + first)
        current_page += 1 if not reverse else -1
        if reverse:
            if current_page <= -1:
                break
        else:
            if current_page >= page_count:
                break

class Nomorator(QObject):

    finished = pyqtSignal()
    messages = pyqtSignal(str)
    started = pyqtSignal()
    progress = pyqtSignal(float)
    
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings

    @pyqtSlot()
    def doJobs(self):
        self.started.emit()
        settings = self.settings
        page_size =\
            QPageSize(
                QSizeF(settings["ukHalamanW"], settings["ukHalamanH"]),
                QPageSize.Millimeter,
                "Custom A3+",
                QPageSize.ExactMatch)

        printer = QPrinter(mode=QPrinter.HighResolution)
        settings["outputPath"] = settings["outputDir"] /\
                                 (QDateTime.currentDateTime().toString("yyyy-MM-dd_HH.mm.ss") + ".pdf")

        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(settings["outputPath"].resolve().as_posix())
        printer.setColorMode(QPrinter.GrayScale if settings["colorMode"] == "Grayscale" else QPrinter.Color)
        printer.setPageSize(page_size)
        printer.setResolution(settings["imageDpi"])
        printer.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)
        painter = QPainter(printer)
        painter.save()
        pen = painter.pen()
        pen.setColor(settings["font-color"])
        painter.setPen(pen)
        font = settings["font"]
        font.setPointSizeF(settings["font-size"])
        painter.setFont(font)
        if settings["fromFile"]:
            numgen = serial_generator(settings["fileName"], None, None, None, None, settings["grid1"], settings["grid2"], False)
        else:
            numgen = serial_generator(settings["startNum"],
                                  settings["stopNum"],
                                  settings["fDigit"],
                                  settings["prefix"],
                                  settings["suffix"],
                                  settings["grid1"],
                                  settings["grid2"],
                                  False)
        _run = True
        
        while _run:
            for row in range(settings["grid2"]):
                for col in range(settings["grid1"]):
                    try:
                        tx = next(numgen)
                    except StopIteration:
                        _run = False
                        break
                    pos1 = settings["posX"] + (settings["offsetW"] * col)
                    pos2 = settings["posY"] + (settings["offsetH"] * row)
                    point = QPointF(MMtoPX(pos1, settings["imageDpi"]), MMtoPX(pos2, settings["imageDpi"]))
                    painter.drawText(point, tx)
                    if settings["useDuplicate"]:
                        point += QPointF(MMtoPX(settings["dupX"], settings["imageDpi"]), MMtoPX(settings["dupY"], settings["imageDpi"]))
                        painter.drawText(point, tx)
                if not _run:
                    break
            if not _run:
                break
            printer.newPage()
        painter.restore()
        painter.end()
        self.messages.emit(settings["outputPath"].as_posix())
        self.finished.emit()


if __name__ == "__main__":
    pass