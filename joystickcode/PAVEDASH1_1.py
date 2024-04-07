'''
Dashboard for RC / autonomous control
Interface with Onshore systems

currently mockup
'''

# Load display
import pygame, sys
from pygame.locals import *
import dash_elements as de
import time
import serial
import random

#use com 5
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)


def write_read(x):
    try:
        arduino.write(bytes(x, 'utf-8'))
    except:
        print("oof")
    time.sleep(0.01)
    #data = arduino.readline()
    #return data


pygame.display.set_caption('PAVE Dashboard')
h = 800
w = 600

# UI elements
screen = de.Screen(h, w, [
    de.Button([30, 20, 20, 8], "stop Throttle", de.colors['red'], de.fonts['default'], lambda: print("stop Throttle")),
    de.H_Slider([20, 80, 60, 8], "act_steering", de.colors['sec'], de.fonts['default'], -1, 1),
    de.V_Slider([10, 60, 5, 38], "act_throttle", de.colors['sec'], de.fonts['default'], 0, 100),
    de.Button([30, 40, 20, 8], "Connected", de.colors['green'], de.fonts['default'], lambda: print("Connected")),
])

# Joystick
joystick = pygame.joystick.Joystick(0)
print("Detected joystick '%s'" % joystick.get_name())
# Main loop

#012345678
#0-3 will be steering
#4-6 will be throttle
#8 will be noise


counter = 0
throttle = 0
randomList = ["0", "1", "2", "3", "4"]
while True:
    outPutSignal = ""
    # Check for events
    for event in pygame.event.get():
        # Quit
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Resize
        if event.type == VIDEORESIZE:
            h = event.w
            w = event.h
            screen.screen = pygame.display.set_mode((h, w), pygame.RESIZABLE)
        # Mouse click
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            screen.check_click(pos)
    
            
    #print([joystick.get_axis(i) for i in range(joystick.get_numaxes())])
    #steering
    steering = joystick.get_axis(0)
    screen.elements[1].x = steering
    steering = int((joystick.get_axis(0)+1)*500) 
    if (steering > 1000):
        steering = 1000
    elif (steering < 0):
        steering = 0
    outPutSignal = outPutSignal + str(steering).zfill(4)

    #throttle
    #r2 is 5, increase speed
    if (joystick.get_button(7)):
        throttle+=1
    #L2 = 6, decrease speed
    if (joystick.get_button(6)):
        throttle-=1
    #if you go over boundaries of pwm signal
    if (throttle > 100):
        throttle = 100
    elif (throttle < 0):
        throttle = 0
    outPutSignal = outPutSignal + str(throttle).zfill(3)    
    screen.elements[2].y = 100 - throttle
    
    #if stop throttle
    #B is 2
    if (joystick.get_button(2)):
        screen.elements[0].color = de.colors['green']
        screen.elements[0].text = "Throttle is Stopped"
        #get the first 4 which will be only steering
        outPutSignal = outPutSignal[0:4] + "000"
        throttle = 0
    else:
        screen.elements[0].color = de.colors['red']
        screen.elements[0].text = "Stop Throttle"
        outPutSignal = outPutSignal
    
    """
    if (joystick.get_button(8)):
        screen.elements[3].color = de.colors['green']
        screen.elements[3].text = "no Signal Sent"
        outPutSignal = outPutSignal + "1"
    else:
        screen.elements[3].color = de.colors['red']
        screen.elements[3].text = "Signal is being sent"
        outPutSignal = outPutSignal + "0"
    """

    #add random noise into system
    outPutSignal = outPutSignal + random.choice(randomList)
    outPutSignal = outPutSignal + "1"


    # Draw
    screen.draw(screen.screen)
    pygame.display.update()
    pygame.time.Clock().tick(30)

    outPutSignal = outPutSignal + "x"
    print("after: ", outPutSignal)
    try:
        #write_read(str(steering).zfill(4))
        write_read(outPutSignal)
    except: 
        print("writingtoPicoError")
        

    