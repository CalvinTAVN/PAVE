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

"""
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    #time.sleep(0.001)
    #data = arduino.readline()
    #return data
"""

pygame.display.set_caption('PAVE Dashboard')
h = 800
w = 600

# UI elements
screen = de.Screen(h, w, [
    de.Button([1, 1, 10, 8], "Start", de.colors['green'], de.fonts['default'], lambda: print("Start")),
    de.Button([1, 10, 10, 8], "Stop", de.colors['red'], de.fonts['default'], lambda: print("Stop")),
    de.H_Slider([20, 90, 60, 8], "cmd_rudder", de.colors['sec'], de.fonts['default'], -1, 1),
    de.H_Slider([20, 80, 60, 8], "act_rudder", de.colors['sec'], de.fonts['default'], -1, 1),
    de.V_Slider([2, 60, 5, 38], "cmd_throttle", de.colors['sec'], de.fonts['default'], -1, 1),
    de.V_Slider([10, 60, 5, 38], "act_throttle", de.colors['sec'], de.fonts['default'], -1, 1),
    de.Button([30, 20, 20, 8], "stop Throttle", de.colors['green'], de.fonts['default'], lambda: print("Start")),
])

# Joystick
joystick = pygame.joystick.Joystick(0)
print("Detected joystick '%s'" % joystick.get_name())
counter = 0
# Main loop
while True:
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
    
    print([joystick.get_axis(i) for i in range(joystick.get_numaxes())])
    screen.elements[2].x = joystick.get_axis(0)
    screen.elements[4].y = joystick.get_axis(3)
    
    #if stop throttle

    # Draw
    screen.draw(screen.screen)
    pygame.display.update()
    pygame.time.Clock().tick(60)

    counter+=1
    print(counter)

    #print(str(int((joystick.get_axis(3)+1)*5000000)).zfill(8)+"x")
    #write_read(str(int((joystick.get_axis(3)+1)*5000000)).zfill(8)+"x")


