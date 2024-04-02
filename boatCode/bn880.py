#micropython, GPS module on boat

from machine import Pin, UART, I2C

from micropyGPS import MicropyGPS

# Import utime library to implement delay
import utime, time


class BN880:
    def __init__(self, tx=8, rx=9, baudrate=9600):
        self.gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
        self.buff = bytearray(255)
        self.gps_decoder = MicropyGPS()

    def toString(self, debug=True):
        self.gps_module.readline()
        self.buff = str(self.gps_module.readline())
        if debug:
            print(self.buff)
        for x in self.buff:
            self.gps_decoder.update(x)
        return (
            "Latitude: "
            + self.gps_decoder.latitude_string()
            + " Longitude: "
            + self.gps_decoder.longitude_string()
        )

    def read(self, debug=True):
        self.gps_module.readline()
        self.buff = str(self.gps_module.readline())
        if debug:
            print(self.buff)
        for x in self.buff:
            self.gps_decoder.update(x)

        lat = self.gps_decoder.latitude_string().split()
        long = self.gps_decoder.longitude_string().split()

        latDec = int(lat[0]) + float(lat[1].replace("'", "")) / 60
        longDec = int(long[0]) + float(long[1].replace("'", "")) / 60

        if lat[2] == "S":
            latDec *= -1
        if long[2] == "W":
            longDec *= -1

        return latDec, longDec

