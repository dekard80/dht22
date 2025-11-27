from board import D4
from adafruit_dht import DHT22
from math import log
from time import sleep


class Dht22sensor:
    def __init__(self, pin):
        self.dhtDevice = DHT22(D4, use_pulseio=False)

# try to read the sensor until the reading is successful
# it is based on examples from Adafruit's CircuitPython libraries
# https://github.com/adafruit/Adafruit_CircuitPython_DHT
    def read(self):
        while True:
            try:
                self.temperature = self.dhtDevice.temperature
                self.humidity = self.dhtDevice.humidity
                break
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read,
                # just keep going
                sleep(2)
            except Exception as error:
                self.dhtDevice.exit()
                raise error
        return self.temperature, self.humidity

# calculate the dew point
    def dewPoint(self, Tc, Rh):
        try:
            self.Es = 6.11 * pow(10, (7.5 * Tc) / (237.7 + Tc))
            self.E = (Rh * self.Es) / 100
            self.dew_point = (-430.22 + 237.7 * log(self.E)) / (-log(self.E) + 19.08)  # noqa: E501
        except ValueError as error:
            return 0.0
        return self.dew_point
