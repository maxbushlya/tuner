from numpy import linspace, abs, mean, std
from PyQt4 import Qt, QtGui, QtCore
import PyQt4.Qwt5 as Qwt
from PlotPicker import picker
import frequencies
import AudioBackend

class ClassPlot(Qwt.QwtPlot):
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.minfreq = 20
        self.maxfreq = 5000
        self.maxFftFreq = AudioBackend.RATE / 2
        self.response_level = -20

        # set plot layout
        self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setAlignCanvasToScales(True)

        #self.setAxisScale(Qwt.QwtPlot.yLeft, -1., 1.)

        # insert a few curves
        self.curve = Qwt.QwtPlotCurve()
        self.curve.setPen(QtGui.QPen(Qt.Qt.red))
        self.curve.attach(self)

        # attach a grid
        grid = Qwt.QwtPlotGrid()
        grid.enableXMin(True)
        grid.setMajPen(Qt.QPen(Qt.QPen(Qt.Qt.gray)))
        grid.setMinPen(Qt.QPen(Qt.QPen(Qt.Qt.lightGray)))
        grid.setZ(1000.)
        grid.attach(self)

        self.marker = Qwt.QwtPlotMarker()
        self.marker.setLabelAlignment(Qt.Qt.AlignRight)
        self.marker.attach(self)

        self.center_marker = Qwt.QwtPlotMarker()
        self.center_marker.setYValue(self.response_level)
        self.center_marker.setLabelAlignment(Qt.Qt.AlignRight)
        #self.center_marker.setLineStyle(Qwt.QwtPlotMarker.VLine)
        self.center_marker.setLinePen(QtGui.QPen(Qt.Qt.green))
        self.center_marker.setLineStyle(Qwt.QwtPlotMarker.HLine)
        self.center_marker.attach(self)

        xtitle = Qwt.QwtText('Frequency (Hz)')
        #xtitle.setFont(QtGui.QFont(8))
        self.setAxisTitle(Qwt.QwtPlot.xBottom, xtitle)
        ytitle = Qwt.QwtText('PSD (dB A)')
        #ytitle.setFont(QtGui.QFont(8))
        self.setAxisTitle(Qwt.QwtPlot.yLeft, ytitle)

        # picker used to display coordinates when clicking on the canvas
        self.picker = picker(Qwt.QwtPlot.xBottom,
                               Qwt.QwtPlot.yLeft,
                               Qwt.QwtPicker.PointSelection,
                               Qwt.QwtPlotPicker.CrossRubberBand,
                               Qwt.QwtPicker.ActiveOnly,
                               self.canvas())

        self.setAxisScale(Qwt.QwtPlot.yLeft, -90, 90)
        self.setAxisScale(Qwt.QwtPlot.xBottom, self.minfreq, self.maxfreq)

        #self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)

    def setdata(self, xnew, ynew, ind):
        self.curve.setData(xnew, ynew)

        if ynew[ind] > self.response_level and xnew[ind] > self.minfreq and xnew[ind] < self.maxfreq:
            nearest = frequencies.find_nearest(frequencies.equal_tempered_freqs.keys(), xnew[ind])
            str =  "%04.02f Hz [%s %02.02f Hz]"%(xnew[ind], frequencies.equal_tempered_freqs[nearest], xnew[ind] - nearest)
            text = Qwt.QwtText(str)
            text.setColor(Qt.Qt.blue)
            text.setBackgroundBrush(Qt.QBrush(Qt.Qt.yellow))
            fn = self.fontInfo().family()
            text.setFont(Qt.QFont(fn, 8, Qt.QFont.Bold))
            self.marker.setLabel(text)
            self.marker.setXValue(xnew[ind])
            self.marker.setYValue(ynew[ind])
        else:
            self.marker.setLabel(Qwt.QwtText(""))

        self.replot()

    def setFreqRange(self, min, max):
        self.minfreq = min
        self.maxfreq = max
        self.setAxisScale(Qwt.QwtPlot.xBottom, self.minfreq, self.maxfreq)

    def getFreqRange(self):
        return self.minfreq, self.maxfreq

    def setResponseLevel(self, val):
        if val > -50 and val < 100:
            self.response_level = val
            self.center_marker.setYValue(val)
            print self.__class__, val


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    window = ClassPlot()
    window.show()
    sys.exit(app.exec_())
