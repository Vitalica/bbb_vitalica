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
from pulseox_sensor import PulseOx

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
    socket = context.socket(zmq.REQ)

    #sensor_data = FakeData()

    ekg = EKG()
    pulse = PulseOx()
    #irtemp = IRTemp()
    irtemp = FakeData()


    data_out = []
    while True:
        socket.connect("tcp://localhost:5678")
        data_ekg = ekg.get_reading()
        data_pulse = pulse.get_reading()
        data_temp = irtemp.get_reading()

        data_out.append(data_ekg)
        data_out.append(data_pulse[0])
        data_out.append(data_pulse[1])
        data_out.append(data_temp)

        try:
            #out = "data " + str(x)
            socket.send("".join(out))
            time.sleep(0.01)
            out = map(str, data_out)
            print '->', out
            #time.sleep(0.01)
        except:
            pass

if __name__ == '__main__':
    publish_data()
