import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

p1 = GPIO.PWM(32, 100)
p2 = GPIO.PWM(33, 100)

p1.start(50)
p2.start(50)