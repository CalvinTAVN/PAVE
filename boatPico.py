from machine import I2C
#from hmc5883l import HMC5883L
from time import sleep
import time
from bn880 import BN880
from humPro import humPro
import math

DO_TELEM = True

# check that correct PINs are set on hmc5883l library
if DO_TELEM:
    #compass = HMC5883L()
    gps = BN880()

rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)

RADIUS = 6371
APPROX_LAT = 38.63589

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

thisTime = time.ticks_ms
lastTime = 0

def getSpeed(lastX, lastY, thisX, thisY, dt):
    xVelo = (thisX - lastX) / dt
    yVelo = (thisY - lastY) / dt
    
    return math.sqrt(xVelo * xVelo + yVelo * yVelo)

def get_bearing(startx, starty, endx, endy):
    startx = 180*startx/math.pi
    starty = 180*starty/math.pi
    endx = 180*endx/math.pi
    endy = 180*endy/math.pi
    
    d_lambda = endy - starty
    dx = math.sin(d_lambda)*math.cos(endx)
    dy = math.cos(startx)*math.sin(endx) - math.sin(startx)*math.cos(endx)*math.cos(d_lambda)
    theta = math.degrees(math.atan2(dx, dy))
    if(theta < 0): theta += 360
    return theta

def toGrid(lat, long):
    x = RADIUS * long * math.cos(APPROX_LAT * math.pi / 180)
    y = RADIUS * lat * math.pi / 180

    return x, y

while True:
    sleep(0.1)
    led.toggle()
    
    steeringFormat = "%03d" % steering
    throttleFormat = "%03d" % throttle
    
    byteIn = rf.readPacket()
    count += 1
    #print(count)

    if checkLoops - loopsSince < 0:
        killed = True

    if byteIn is not None:
        strIn = byteIn.decode("utf-8").replace("\n","")
        #print(strIn)
        
        if strIn == "1":
            loopsSince = 0
            killed = False
        
        if strIn != "k":
            if killed == False:
                if strIn == "w":
                    if throttle < 300: throttle += 1
                    #print("Increase throttle")
                elif strIn == "s":
                    if throttle > 0: throttle += -1
                    #print("Deacrease throttle")
                elif strIn == "c":
                    throttle = 0
                elif strIn == "p":
                    throttle = 0
                    steering = 150
                throttleFormat = "%03d" % throttle
            if strIn == "4":
                steering = 290
                #print("Steer left")
            elif strIn == "5":
                steering = 200
                #print("Steer right")
            elif strIn == "7":
                steering = 100
            elif strIn == "8":
                steering = 10
            elif strIn == "6":
                steering = 150
                #print("Reset steering")
            elif strIn == "u":
                # unkill
                killed = False
            loopsSince = 0
        elif strIn == "k":
            # send kill code here
            throttleFormat = "xxx"
            killed = True
            throttle = 0
    #if killed == True: throttleFormat = "xxx"

    steeringFormat = "%03d" % steering
        
        #if strIn != '\n': print(strIn)
            
    strControl = steeringFormat + throttleFormat
    #uart.write(strControl+'\n')
    print(strControl) # MUST BE PRINTED TO COBSOLE SO JETSON CAN READ
    loopsSince += 1
    count += 1
    
    lat, long = gps.read()
    rf.transmitData("lat: %.3f, long %.3f" % (lat, long))
    print("lat: %.3f, long %.3f" % (lat, long))
            
    '''
    if DO_TELEM:
        lastTime = thisTime
        thisTime = time.ticks_ms()
        
        dt = time.ticks_diff(thisTime, lastTime)
        
        x, y, z = compass.read()
        deg, minutes = compass.heading(x, y)
        #heading = (deg + minutes / 60) * math.pi / 180
        
        lat, long = gps.read()
        
        formatLat = "%09.5f" % lat
        formatLong = "%010.5f" % long
        formatHeading = "%09.5f" % heading
        formatSpeed = "%09.5f" % speed
        
        strOut = 'x' + throttleFormat + ", " + steeringFormat + ", " + formatLat + ", " + formatLong + ", " + formatHeading
        #strOut = 'x' + throttleFormat + ", " + steeringFormat + ", " + formatLat + ", " + formatLong + ", " + formatHeading + ", " + formatSpeed
        #print(strOut)
        
        # changed this from count == 20, count = 0
        if count % 20 == 0:
            rf.transmitData(strOut)
            
        if count % 50 == 0:
            lastFiveLat = fiveLat
            lastFiveLong = fiveLong
            
            fiveLat[0] = lat
            fiveLong[0] = long
        if count % 51 == 0:
            fiveLat[1] = lat
            fiveLong[1] = long
        if count % 52 == 0:
            fiveLat[2] = lat
            fiveLong[2] = long
        if count % 53 == 0:
            fiveLat[3] = lat
            fiveLong[3] = long
        if count % 54 == 0:
            fiveLat[4] = lat
            fiveLong[4] = long
            
        if count > 104:
            for i in range(5):
                x, y = toGrid(fiveLat[i], fiveLong[i])
                lastX, lastY = toGrid(lastFiveLat[i], lastFiveLong[i])
                
                headings[i] = get_bearing(lastFiveLat[i], lastFiveLong[i], fiveLat[i], fiveLong[i])
                speeds[i] = getSpeed(x, y, lastX, lastY, dt)
                
            heading = (headings[0] + headings[1] + headings[2] + headings[3] + headings[4]) / 5
            speed = (speeds[0] + speeds[1] + speeds[2] + speeds[3] + speeds[4]) / 5
    '''
            

