from PyQt4 import QtGui, QtCore
import sys
from ClassPlot import ClassPlot
from RegionPlot import RegionPlot
import AudioBackend
from numpy import linspace, sin, interp
from AnalogDevice import AnalogDevice
import frequencies
from scipy import interpolate

InterpNo = 0
InterpSpline = 1
InterpLinear = 2

class MyWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(QtGui.QWidget, self).__init__(parent)

        self.global_plot = ClassPlot(self)
        self.analog_device = AnalogDevice(self)
        self.region_plot = RegionPlot(self)
        self.combo_note = QtGui.QComboBox()
        self.spin_level = QtGui.QSpinBox()
        self.spin_oscillation = QtGui.QSpinBox()

        self.centralLayout = QtGui.QVBoxLayout(self)
        layout1 = QtGui.QHBoxLayout()
        layout2 = QtGui.QVBoxLayout()

        layout2.addWidget(QtGui.QLabel("Note:"))
        layout2.addWidget(self.combo_note)
        layout2.addWidget(QtGui.QLabel("Response level (dB):"))
        layout2.addWidget(self.spin_level)
        layout2.addWidget(QtGui.QLabel("Arrow oscillation:"))
        layout2.addWidget(self.spin_oscillation)
        self.spin_level.setRange(-50, 50)
        self.spin_level.setValue(-20)
        self.spin_oscillation.setRange(2, 20)
        self.spin_oscillation.setValue(4)
        layout2.addItem(QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred))
        self.centralLayout.setContentsMargins(10, 10, 10, 10)
        layout1.addLayout(layout2)
        layout1.addWidget(self.analog_device)
        layout1.addWidget(self.region_plot)
        self.centralLayout.addLayout(layout1)
        self.centralLayout.addWidget(self.global_plot)

        self.timer = QtCore.QTimer()
        # update interval should correspond to rate CHUNK/RATE or be greater
        self.timer.setInterval(1000.0 * AudioBackend.CHUNK / AudioBackend.RATE)
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.update_plot)
        self.connect(self.combo_note, QtCore.SIGNAL('currentIndexChanged(int)'), self.changedNote)
        self.connect(self.spin_level, QtCore.SIGNAL('valueChanged(int)'), self.changedLevel)
        self.connect(self.spin_oscillation, QtCore.SIGNAL('valueChanged(int)'), self.changedOscillation)
        self.timer.start()

        self.region_plot.setFreqRange(frequencies.freqs[0], frequencies.freqs[2], frequencies.freqs[1], "C0")
        self.combo_note.insertItems(0, frequencies.notes)
        self.analog_device.setRange(-4, 4)

    def update_plot(self):
        y = AudioBackend.analyseStream()
        x = linspace(0, AudioBackend.RATE, AudioBackend.CHUNK)

        global_x, global_y, global_ind = self.interpolate((x, y), self.global_plot.getFreqRange(), InterpLinear)
        region_x, region_y, region_ind = self.interpolate((x, y), self.region_plot.getFreqRange(), InterpSpline)

        self.global_plot.setdata(global_x, global_y, global_ind)
        self.region_plot.setdata(region_x, region_y, region_ind)
        nearest = frequencies.freqs[self.combo_note.currentIndex() + 1]
        #nearest = frequencies.find_nearest(frequencies.freqs, region_x[region_ind])
        if region_y[region_ind] > self.spin_level.value():
            self.analog_device.setValue(region_x[region_ind] - nearest)
        else:
            self.analog_device.setValue(0)

    def changedNote(self, index):
        min_freq = frequencies.freqs[index]
        freq = frequencies.freqs[index + 1]
        max_freq = frequencies.freqs[index + 2]
        self.region_plot.setFreqRange(min_freq, max_freq, freq, frequencies.notes[index])

    def changedLevel(self, value):
        self.global_plot.setResponseLevel(value)
        self.region_plot.setResponseLevel(value)

    def changedOscillation(self, value):
        val = self.spin_oscillation.value()
        self.analog_device.setRange(-val, val)

    def interpolate(self, xy_values, freq_range, interp_type):
        x, y = xy_values
        min_freq, max_freq = freq_range
        xnew = []
        ynew = []
        if interp_type == InterpLinear:
            xnew = linspace(min_freq, max_freq, AudioBackend.CHUNK / 2)
            ynew = interp(xnew, x, y)
        if interp_type == InterpSpline:
            xnew = linspace(min_freq, max_freq, AudioBackend.CHUNK / 2)
            tck = interpolate.splrep(x, y, s=0)
            ynew = interpolate.splev(xnew,tck,der=0)
        if interp_type == InterpNo:
            xnew, ynew = x, y
        ind = ynew.argmax()
        return xnew, ynew, ind

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = MyWindow()
    w.setWindowTitle("Music tuner 1.2")
    w.resize(800, 400)
    w.show()
    sys.exit(app.exec_())
