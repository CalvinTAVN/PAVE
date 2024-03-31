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
    arduino.write(bytes(x, 'utf-8'))
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
    de.V_Slider([10, 60, 5, 38], "act_throttle", de.colors['sec'], de.fonts['default'], -1, 1),
])

# Joystick
joystick = pygame.joystick.Joystick(0)
print("Detected joystick '%s'" % joystick.get_name())
# Main loop
counter = 0
randomList = [-2, -1, 0, 1, 2]
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
    screen.elements[1].x = joystick.get_axis(0)
    outPutSignal = outPutSignal + str(int((joystick.get_axis(0)+1)*500)).zfill(4)

    #throttle
    screen.elements[2].y = joystick.get_axis(3)
    #invert throttle to be from 0 to 1000
    throttle_adapt = 1000 - int((joystick.get_axis(3)+1)*500)
    throttleAdapt = throttle_adapt + random.choice(randomList)
    outPutSignal = outPutSignal + str(throttle_adapt).zfill(4)    
    
    #if stop throttle
    if (joystick.get_button(5)):
        screen.elements[0].color = de.colors['green']
        screen.elements[0].text = "Throttle is Stopped"
        outPutSignal = outPutSignal + "1"
        #print("throttleStop")
    else:
        screen.elements[0].color = de.colors['red']
        screen.elements[0].text = "Stop Throttle"
        outPutSignal = outPutSignal + "0"

    # Draw
    screen.draw(screen.screen)
    pygame.display.update()
    pygame.time.Clock().tick(60)


    outPutSignal = outPutSignal + "x"
    print(outPutSignal)
    write_read(outPutSignal)
    #counter+=1
    #print(counter)
    #write_read(str(counter).zfill(8) + "x")
    #print(str(int((joystick.get_axis(0)+1)*500)).zfill(4)+"x")
    #write_read(str(int((joystick.get_axis(3)+1)*5000000)).zfill(8)+"x")