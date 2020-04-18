from PyQt4 import Qt, QtGui, QtCore
import PyQt4.Qwt5 as Qwt
import ClassPlot
import frequencies
import numpy

class picker(Qwt.QwtPlotPicker):
    def __init__(self, *args):
        Qwt.QwtPlotPicker.__init__(self, *args)

    def trackerText(self, pos):
        pos2 = self.invTransform(pos)
        nearest = frequencies.find_nearest(numpy.array(frequencies.equal_tempered_freqs.keys()), pos2.x())
        str = ''
        if (pos2.x() - nearest) >= 0:
            str =  "%04.02f Hz [%s +%02.01f Hz]"%(pos2.x(), frequencies.equal_tempered_freqs[nearest], pos2.x() - nearest)
        else:
            str =  "%04.02f Hz [%s %02.01f Hz]"%(pos2.x(), frequencies.equal_tempered_freqs[nearest], pos2.x() - nearest)
        text = Qwt.QwtText(str)
        return text#Qwt.QwtText("%d Hz, %.1f dB" %(pos2.x(), pos2.y()))

    def drawTracker(self, painter):
        textRect = self.trackerRect(painter.font())
        if not textRect.isEmpty():
                 label = self.trackerText(self.trackerPosition())
                 if not label.isEmpty():
                        painter.save()
                        painter.setPen(Qt.Qt.NoPen)
                        painter.setBrush(Qt.Qt.white)
                        painter.drawRect(textRect)
                        painter.setPen(Qt.Qt.black)
                        #painter->setRenderHint(QPainter::TextAntialiasing, false);
                        label.draw(painter, textRect)
                        painter.restore()