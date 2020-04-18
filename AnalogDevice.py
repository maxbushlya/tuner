from PyQt4 import QtGui, QtCore, Qt

class AnalogDevice(QtGui.QWidget):
    def __init__(self, parent = None):
        super(AnalogDevice, self).__init__(parent)
        self.mark_count = 7
        self.value_type = "dB"
        self.min_value = -12
        self.max_value = 12
        self.value = 0
        self.min_angle = -120
        self.max_angle = 120

        self.setMinimumSize(150, 150)
        self.setMaximumSize(250, 250)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

    def paintEvent(self, event):
        angle_step = 1.0 * (self.max_angle - self.min_angle) / (self.mark_count - 1)
        value_step = 1.0 *(self.max_value - self.min_value) / (self.mark_count - 1)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(3)
        painter.setPen(pen)
        font = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)
        painter.setFont(font)

        sz = min(self.width(), self.height())

        # set painter to center of widget
        painter.translate(self.width()/2, self.height()/2)

        #################
        # draw border
        painter.drawEllipse(-sz/2 + 2, -sz/2 + 2, sz - 4, sz - 4)

        ################
        # draw arrow
        arrowTriangle = QtGui.QPolygon([QtCore.QPoint(-5, 20), QtCore.QPoint(0, -sz/2 + 20),
                                        QtCore.QPoint(5, 20), QtCore.QPoint(0, -sz/2 + 20),
                                        QtCore.QPoint(5, 20), QtCore.QPoint(-5, 20)])
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(127, 0, 127))
        painter.rotate(angle_step / value_step * self.value)
        painter.drawEllipse(QtCore.QRect(-9, 9, 18, -18))
        painter.drawConvexPolygon(arrowTriangle)
        painter.restore()

        #####################
        # draw triangle marks
        markerTriangle = QtGui.QPolygon([QtCore.QPoint(-3, -sz/2 + 1),
                                         QtCore.QPoint(0, -sz/2 + 12),
                                         QtCore.QPoint(3, -sz/2 + 1)])
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 127, 0))
        painter.rotate(self.min_angle)
        for i in xrange(self.mark_count):
            painter.drawConvexPolygon(markerTriangle)
            painter.rotate(angle_step)
        painter.restore()

        #################
        # draw dewice title
        text = Qt.QString(self.value_type)
        font.setPointSize(20)
        painter.setFont(font)
        size = painter.fontMetrics().size(Qt.Qt.TextSingleLine, text)
        painter.drawText(-size.width()/2, 25 + size.height(), text)

        ####################
        # draw text marks
        font.setPointSize(10)
        painter.setFont(font)
        painter.rotate(self.min_angle)
        val = self.min_value
        for i in xrange(self.mark_count):
            text = Qt.QString("%s%03.01f"%("+" if val > 0 else "", val))
            size = painter.fontMetrics().size(Qt.Qt.TextSingleLine, text)
            painter.drawText(-size.width()/2, -sz/2 + 12 + size.height(), text)
            painter.rotate(angle_step)
            val += value_step


#    def resizeEvent(self, event):
#        size = event.size()
#        val = min(size.width(), size.height())
#        self.resize(val, val)

    def setMarkCount(self, count):
        self.mark_count = count

    def setValueTypeString(self, type):
        self.value_type = type

    def setRange(self, min, max):
        self.min_value = min
        self.max_value = max
        self.repaint()

    def setValue(self, val):
        if (self.value != val and val > self.min_value and val < self.max_value):
            self.value = val
            self.repaint()
            return
        if (self.value != val and val < self.min_value):
            self.value = self.min_value
            self.repaint()
            return
        if (self.value != val and val > self.max_value):
            self.value = self.max_value
            self.repaint()
            return

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win = QtGui.QWidget()
    dew = AnalogDevice()
    dew.setRange(-4, 4)
    layout = QtGui.QVBoxLayout(win)
    layout.addWidget(dew)
    layout.addWidget(QtGui.QComboBox(win))
    win.resize(200, 200)
    win.show()
    sys.exit(app.exec_())