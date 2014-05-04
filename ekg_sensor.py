# IR Temperature sensor
import Adafruit_BBIO.ADC as ADC
from sensor import Sensor

class EKG(Sensor):

    """EKG Sensor."""

    ADC_CHANNEL="AIN0"

    def __init__(self):
        Sensor.__init__(self)
        ADC.setup()

    def get_reading(self):
        val = ADC.read(self.ADC_CHANNEL)
        return val * 1.8


