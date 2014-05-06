#!/usr/bin/env python
# encoding: utf-8

# Plotting Application
import time
import zmq
import random
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from collections import deque
from scipy.signal import butter, lfilter, filtfilt

host = "beaglebone.local"

BUF_SIZE = 5000
class Plotter(object):

    """Docstring for Plotter. """

    def __init__(self):
        """@todo: to be defined1. """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://" + host + ":8888")
        self.socket.setsockopt(zmq.SUBSCRIBE, "data")
        self.app = QtGui.QApplication([])

        self.init_gui()
        self.init_data()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.read_data)
        #self.timer2.start(1)
        self.timer2.start(0.5)

    def init_gui(self):
        """@todo: Docstring for init_gui.
        :returns: @todo

        """
        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.resize(1000,600)
        self.win.setWindowTitle('pyqtgraph example: Plotting')
        self.px = self.win.addPlot(title="Axis X")
        self.px.enableAutoRange('y', True)
        self.px.setMouseEnabled(x=False, y=True)


    def init_data(self):
        """@todo: Docstring for init_data.
        :returns: @todo

        """

        self.xcurve = self.px.plot(pen='y')
        self.xdata = deque(np.zeros(BUF_SIZE), maxlen=BUF_SIZE)
        self.tstamp = deque(np.arange(BUF_SIZE), maxlen=BUF_SIZE)


    def read_data(self):
        """@todo: Docstring for read_data.
        :returns: @todo

        """
        din = self.socket.recv_string()
        _, val = din.split()
        fval = float(val)
        print fval
        self.xdata.append(fval)
        self.tstamp.append(self.tstamp[-1]+1)
        #print fval

    def update(self):
        #sample_freq = 1000.0
        sample_freq = 100.0
        cutoff_freq_1 = 31.0
        cutoff_freq_2 = 70.0
        norm_cutoff1 = cutoff_freq_1/(sample_freq/2)
        norm_cutoff2 = cutoff_freq_2/(sample_freq/2)
        # Butterworth filter
        b, a = butter(4, cutoff_freq_1, btype = 'low')
        #b, a = butter(4, [norm_cutoff1, norm_cutoff2], btype = 'bandstop')
        #b, a = butter(4, [norm_cutoff1, norm_cutoff2], btype = 'bandstop')
        #y2 = lfilter(b, a, self.xdata)  # standard filter
        y3 = filtfilt(b, a, self.xdata) # filter with phase shift correction
        #print y2
        #print y3

        #self.xcurve.setData(self.tstamp, y3)
        self.xcurve.setData(self.tstamp, self.xdata)
        #self.ycurve.setData(tstamp, ydata)
        #self.zcurve.setData(tstamp, zdata)

    def stop(self):
        """@todo: Docstring for stop.
        :returns: @todo

        """
        self.timer.stop()
        self.timer2.stop()

if __name__ == '__main__':
    p = Plotter()
    QtGui.QApplication.instance().exec_()
    p.stop()
    del p

