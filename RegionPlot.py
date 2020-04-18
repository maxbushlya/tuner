from ClassPlot import ClassPlot
from PyQt4 import Qt, QtGui
import PyQt4.Qwt5 as Qwt

class RegionPlot(ClassPlot):
    def __init__(self, *args):
        ClassPlot.__init__(self, *args)

        self.center = 0
        self.center_marker = Qwt.QwtPlotMarker()
        self.center_marker.setLabelAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignRight)
        self.center_marker.setLineStyle(Qwt.QwtPlotMarker.VLine)
        self.center_marker.setLinePen(QtGui.QPen(Qt.Qt.red))
        self.center_marker.attach(self)

    def setFreqRange(self, min, max, value, label):
        ClassPlot.setFreqRange(self, min, max)

        self.center = value
        self.center_marker.setXValue(value)
        self.center_marker.setLabel(Qwt.QwtText(label))

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    window = RegionPlot()
    window.setFreqRange(100, 1000, 201, "text")
    window.show()
    sys.exit(app.exec_())