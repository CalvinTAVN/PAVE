#Raspberry pico on boat
#micropython


from machine import I2C
#from hmc5883l import HMC5883L
from time import sleep
import time
from boatCode.humPro import humPro
import math

DO_TELEM = True



rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)


txPin = machine.Pin(4)
rxPin = machine.Pin(5)
uart = machine.UART(1, 9600, tx=txPin, rx=rxPin)

led = machine.Pin(25, machine.Pin.OUT)

sleep(0.5)

steering = 150
throttle = 0

checkLoops = 100
loopsSince = 0

killed = False

count = 0

fiveLat = [0, 0, 0, 0, 0]
fiveLong = fiveLat
lastFiveLat = fiveLat
lastFiveLong = fiveLong

headings = [0,0,0,0,0]
speeds = headings

fiveX = [0, 0, 0, 0, 0]
fiveY = fiveX
lastFiveX = fiveX
lastFiveY = fiveY

heading = 0
speed = 0

xVelo = 0
yVelo = 0


print("start")
lastMessage = ""

cycle = 0

while True:
    sleep(0.001)
    led.toggle()
    
    steeringFormat = "%03d" % steering
    throttleFormat = "%03d" % throttle
    '''
    byteIn = rf.readPacket()
    count += 1
    #print(count)
    
    if byteIn is not None:
        strIn = byteIn.decode("utf-8").replace("\n","")
        print(strIn)
    '''
    
    rf.readData()
    if rf.getData() is not None and rf.getData() != lastMessage:
        print(rf.getData())
        lastMessage = rf.getData()
    elif cycle == 0 and rf.getData() == lastMessage:
        print(rf.getData())
    cycle = (cycle + 1) % 30
