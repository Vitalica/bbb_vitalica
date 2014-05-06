# IR Temperature sensor
from Adafruit_I2C import Adafruit_I2C
from sensor import Sensor

class IRTemp(Sensor):

    """Docstring for IRTemp. """

    I2C_ADDRESS = 0x5a

    def __init__(self):
        """@todo: to be defined1. """
        Sensor.__init__(self)
        self.have_sensor = False

        try:
            self.i2c = Adafruit_I2C(self.I2C_ADDRESS)
            self.have_sensor = True
        except:
            pass

    def to_degree(self, val):
        """Change i2c raw data to F

        :val: @todo
        :returns: @todo

        """
        # See datasheet for conversion
        return (val*0.02 - 273.15)*9./5 + 32

    def get_reading(self):
        if self.have_sensor:
            #raw = self.i2c.readS16(0x8)
            raw = self.i2c.readS16(0x7)
            return self.to_degree(raw)
        else:
            return -1


