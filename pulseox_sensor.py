# IR Temperature sensor
import serial
from sensor import Sensor

class PulseOx(Sensor):

    """Pulse Oximeter Sensor."""
    PORT='/dev/ttyUSB0'

    def __init__(self):
        Sensor.__init__(self)
        self.have_serial = False
        try:
            self.ser = serial.Serial(port=self.PORT, baudrate=115200, timeout=1)
            self.have_serial = True
        except:
            pass


    def get_reading(self):

        if self.have_serial :
            count = 0
            init_data= "".join(map(chr,[0x7D,0x81,0xA1,0x80,0x80,0x80,0x80,0x80,0x80]))
            self.ser.write(init_data)
            while count < 10:
                count +=1
                raw_data = map(ord, self.ser.read(8))
                if len(raw_data) < 8:
                    return

                if raw_data[0] == 1 and raw_data[-1] == 0xff:
                    pulse, oxygen = raw_data[5] - 128, raw_data[6] - 128
                    self.ser.flush()
                    return pulse, oxygen
        else:
            return (-1,-1)

