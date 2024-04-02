#Raspberry pico on boat
#micropython

from machine import I2C
from hmc5883l import HMC5883L
from bn880 import BN880
from time import sleep
import time
from boatCode.humPro import humPro
import math


DO_TELEM = True

if DO_TELEM:
    compass = HMC5883L()
    gps = BN880()


rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)

#not sure what these are for 
txPin = machine.Pin(4)
rxPin = machine.Pin(5)
uart = machine.UART(1, 9600, tx=txPin, rx=rxPin)

led = machine.Pin(25, machine.Pin.OUT)

sleep(0.5)





print("start")
lastMessage = ""

cycle = 0

while True:
    sleep(0.001)
    led.toggle()

    
    rf.readData()
    if rf.getData() is not None and rf.getData() != lastMessage:
        print(rf.getData())
        lastMessage = rf.getData()
    elif cycle == 0 and rf.getData() == lastMessage:
        print(rf.getData())
    cycle = (cycle + 1) % 30

    lat, long = gps.read()
    print("lat: %.3f, long %.3f" % (lat, long))

