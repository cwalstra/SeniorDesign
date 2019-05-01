# This file is designed to test the use of
#   the photoresistor and laser with the Pi
#   GPIO pins to determine if the laser is
#   connected or not. The output will be
#   indicated by an LED.

import time
import RPi.GPIO as io
import queue
from time import sleep

LEDgreen = 12

def eyeSetup():
    io.setwarnings(False)
    io.setmode(io.BCM)
    io.setup(23, io.IN, pull_up_down=io.PUD_UP)	# voltage sensing pin
    io.setup(LEDgreen, io.OUT)
    io.output(LEDgreen, 0)

def eyeOutput(q):
    eyeHistory = [False, False, False, False, False, False, False, False, False,False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while True:
        io.output(LEDgreen, 0)
        if io.input(23) != 1:
            eyeHistory.insert(0, True)
            eyeHistory.pop()
            io.output(LEDgreen, 1)
        else:
            eyeHistory.insert(0, False)
            eyeHistory.pop()
            
        try:
            thing = q.get(False)
            q.put(eyeHistory, False)
        except queue.Empty:
            q.put(eyeHistory, False)
        except queue.Full:
            thing = q.get(False)
            q.put(eyeHistory, False)

        sleep(0.1)
