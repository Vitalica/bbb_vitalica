#!/usr/bin/env python
# encoding: utf-8

# Main Application
import time
import zmq
from temp_sensor import IRTemp
from ekg_sensor import EKG
import random
from math import sin,pi
from sensor import Sensor
#from bbb_vitalica import pulseox_sensor

class FakeData(Sensor):

    """Docstring for FakeData. """

    def __init__(self):
        """@todo: to be defined1. """
        Sensor.__init__(self)
        self.i = 0
        self.clip = 100.

    def get_reading(self):
        """@todo: Docstring for get_data.
        :returns: @todo

        """
        t = ((self.i+1.)%self.clip)/self.clip
        self.i+=1

        x = sin(2*pi*t)
        return x


def publish_data():
    """@todo: Docstring for publish_data.
    :returns: @todo

    """
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:8888")

    #sensor_data = FakeData()
    sensor_data = EKG()

    while True:
        x = sensor_data.get_reading()
        out = "data " + str(x)
        #print '->', out
        socket.send(out)
        time.sleep(0.001)
        #time.sleep(0.01)

if __name__ == '__main__':
    publish_data()
