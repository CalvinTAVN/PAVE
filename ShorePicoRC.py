from machine import I2C
from time import sleep
#from humPro import humPro
import uselect
import sys

from machine import Pin, UART
import random


class humPro:
    def __init__(self, crespPin, bePin, cmdPin, ctsPin, txPin, rxPin, modeIndPin):
        self.CRESP = Pin(crespPin, Pin.IN)  # CRESP pin (FOR INTERRUPT)
        self.BE = Pin(bePin, Pin.IN)  # BE pin (CAN BE READ THROUGH LSTATUS IF NEEDED)
        self.CMD = Pin(cmdPin, Pin.OUT)  # CMD pin
        self.CTS = Pin(ctsPin, Pin.IN)  # CTS pin
        self.TX = Pin(txPin, Pin.OUT)  # TX pin
        self.RX = Pin(rxPin, Pin.IN)  # RX pin
        self.MODE_IND = Pin(modeIndPin, Pin.IN)  # MODE_IND pin
        self.uart = UART(0, 9600, tx=self.TX, rx=self.RX)  # initialize UART
        self.buff = self.data = ""
        self.DATA_LEN = 32

    def transmitData(self, data):
        if self.CTS.value() == 0:
            self.CMD.value(1)
            self.uart.write(str(data) + "\n")  # prints a line of data to HumPRO
            self.CMD.value(0)
        else:
            return False

    def readPacket(self):
        return self.uart.readline()

    # used to read data from the uart connection with the HumPRO
    def readData(self):
        packet = self.readPacket()

        if packet is not None:
            try:
                packetStr = packet.decode("utf-8")

                for x in range(len(packetStr)):
                    char = packetStr[x]

                    if char != "x" and char != "\n":
                        self.buff += char
                    elif char == "x":
                        if len(self.buff) == self.DATA_LEN:
                            self.data = self.buff
                        self.buff = ""

            except UnicodeError:
                print("Invalid packet")

    def getData(self):
        if self.data != "" and self.data != "\n":
            return self.data
        else:
            return None

    def transmitRandNumber(self):
        num = self.generateRandom()
        self.transmitData(num)
        print("sending " + str(num))

    def generateRandom(self):
        num = 0
        for i in range(10):
            num += random.randint(0, 9)
            num * 10
        return num

    def transmitCommands(self, commandString, waypoint):
        string = str(commandString) + " " + str(waypoint)
        self.transmitData(string)

    def transmitTelemetry(self, lat, long, heading):
        outString = (
            "x"
            + str(round(lat, 5)).zfill(8)
            + ", "
            + str(round(long, 5)).zfill(8)
            + ", "
            + str(round(heading, 5).zfill(8))
        )

        self.transmitData(outString)



rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)

file = open("data.txt", "w").close()
file = open("data.txt", "w")

led = machine.Pin(25, machine.Pin.OUT)

while True:
    sleep(0.1)
    led.toggle()

    list = uselect.select([sys.stdin], [], [], 0.01)
    
    if list[0]:
        byte = sys.stdin.read(1)
        print(byte)
        rf.transmitData(byte)
    else:
        byte = None

    #rf.readData()
    #out = rf.getData()

    #print(out)
    #file.write(str(out) + "\n")
