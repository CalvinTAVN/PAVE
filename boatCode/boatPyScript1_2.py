import time
import serial
import RPi.GPIO as GPIO
from datetime import datetime
import sys

#receiving signal information from pico
#bottom right usb port for wifi dongle
#/dev/ttyACM1    top right usb port
#top left for arduino when we get to it

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
try:
    file = open('/home/pes/Documents/PAVE/boatCode/data/' + current_time + ".txt", "w")
except:
    pass

def print(text):
    file.write(str(text)+"\n")
    sys.stdout.write(str(text)+"\n")
    
time.sleep(5)
arduinos = []
for port, desc, hwid in sorted(ports):
    print(port)
    print(desc)
    print(hwid)
    for i in hwid.split():
        if i.startswith("SER="):  
            if i == "SER=e661640843856f28":
                pico = serial.Serial(port=port, baudrate=9600, timeout=0.1)
                print("mappedPico")
                break
    else:
        try:
            arduinos.append(serial.Serial(port=port, baudrate=9600, timeout=0.1))
            print("appendedArduino")
        except:
            print("oof")
#arduinos.append(serial.Serial(port="/dev/ttyUSB1", baudrate=9600, timeout=0.1))
    
for arduino in arduinos:
    if arduino.name.startswith("/dev/ttyAM"):
        arduinos.remove(arduino)

#setup pwm signal
GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)
pwm = GPIO.PWM(5, 500)
pwm.start(0)

def write_read(controller, readData,  x= ""):
    if (x != ""):
        controller.write(bytes(x, 'utf-8'))
    time.sleep(0.001)
    controller.flush()
    data = None
    if readData:
        data = controller.readline()
    return data


print("Start")
counter = 0
connectedPico = True
lastMessage = ""
signalTimeOut = 100
cycle = 0
while True:
    try:
        receivedSignal = write_read(pico, True) 
        connectedPico = True
    except serial.serialutil.SerialException:
        print("picoUnplugged")
        pwm.start(0)    
        connectedPico = False
    if connectedPico: 
        stringIn = receivedSignal.decode("utf-8").replace("\r", "").replace("\n", "")
        #print(f"counter: {counter} value: {stringIn}")
        #if stringIn != "" and len(stringIn) == 9:
        throttle = 0
        if (len(stringIn) == 9):
            if stringIn != lastMessage:
                counter = 0
            if (cycle == 0):
                #print(stringIn)
                steeringInformation = stringIn[0:4]
                throttleInfo = stringIn[4:7]
                if (counter < signalTimeOut):
                    throttle = int(throttleInfo)
                else:
                    throttle = 0
                if (throttle < 0):
                    throttle = 0
                elif (throttle > 100):
                    throttle = 100
                pwm.start(throttle)
                for arduino in arduinos:
                    try:
                        #print(arduino)
                        write_read(arduino, False, steeringInformation)  
                    except: 
                        print("oofCantSendArduinoSerial")
                        pwm.start(0)
                print("steering: " + steeringInformation + " throttle: " + str(throttle) + " counter: " + str(counter))
            cycle = (cycle + 1) % 10
            lastMessage = stringIn
            #pico.flush()
        counter+=1      
        if (counter > signalTimeOut):
            #for arduino in arduinos:
                #write_read(arduinos, "0500")
            pwm.start(0)
            print("noConnection")
    
    else:
        print("not connected boatPico")
        pwm.start(0)


        
            
        


