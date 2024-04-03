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
file = open(current_time + ".txt", "w")

def print(text):
    file.write(str(text)+"\n")
    sys.stdout.write(str(text)+"\n")

arduinos = []
for port, desc, hwid in sorted(ports):
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

    


#setup pwm signal
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
pwm = GPIO.PWM(33, 500)
pwm.start(0)

def write_read(controller, x= ""):
    if (x != ""):
        controller.write(bytes(x, 'utf-8'))
    #time.sleep(0.01)
    data = controller.readline()
    return data



print("Start")
killCounter = 0
counter = 0
cycle = 0
connectedPico = True
lastMessage = ""
while True:
    try:
        receivedSignal = write_read(pico) 
        connectedPico = True
    except serial.serialutil.SerialException:
        print("picoUnplugged")
        pwm.start(0)    
        connectedPico = False
    if connectedPico: 
        stringIn = receivedSignal.decode("utf-8").replace("\r", "").replace("\n", "")
        #print(f"counter: {counter} {stringIn}")
        if stringIn != "" and len(stringIn) == 9 and stringIn[8]=="0":
            if stringIn != lastMessage:
                killCounter = 0
                counter = 0
            if cycle == 0:
                #print(stringIn)
                steeringInformation = stringIn[0:4]
                throttleInfo = stringIn[5:8]
                if (counter < 100):
                    throttle = int(throttleInfo)
                else:
                    throttle = 0
                #print("throttle: ", throttle)
                pwm.start(throttle)
                #print(steeringInformation)
                for arduino in arduinos:
                    try:
                        write_read(arduino, steeringInformation)  
                    except: 
                        pwm.start(0) 
                #print(stringIn)
                print("steering: " + steeringInformation + " throttle: " + str(throttle) + " counter: " + str(counter))
                lastMessage = stringIn
            #cycle = (cycle + 1) % 10
            pico.flush()
        counter+=1
        if (counter > 100 or ((len(stringIn) == 9) and (stringIn[8]=="1"))):
            #for arduino in arduinos:
                #write_read(arduinos, "0500")
            pwm.start(0)
            print("noConnection")
    
    else:
        print("not connected Pico")
        pwm.start(0)


        
            
        


