from RPi import GPIO as io
from sensorkit.UltrasonicHCSR04 import UltrasonicHCSR04
import time
import threading

input0 = 17
input1 = 27

enable = 22

io.setmode(io.BCM)

io.setup(input0, io.OUT)
io.setup(input1, io.OUT)
io.setup(enable, io.OUT)

pwm = io.PWM(enable, 100)
dc = 30.0
pwm.start(30)

while(True):
    command = raw_input("Give a command(up, down, stop, forward, backward): ")
    if command == "up":
        dc += 10
        pwm.ChangeDutyCycle(dc)
    elif command == "down":
        dc -= 10
        pwm.ChangeDutyCycle(dc)
    elif command == "forward":
        io.output(input0, True)
        io.output(input1, False)
    elif command == "backward":
        io.output(input0, False)
        io.output(input1, True)
    elif command == "stop":
        break;

pwm.stop()
io.cleanup()
