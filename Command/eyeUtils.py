# This file is designed to test the use of
#   the photoresistor and laser with the Pi
#   GPIO pins to determine if the laser is
#   connected or not. The output will be
#   indicated by an LED.

import time
import RPi.GPIO as io

def eyeSetup():
    io.setwarnings(False)
    io.setmode(io.BCM)
    io.setup(23, io.IN, pull_up_down=io.PUD_UP)	# voltage sensing pin
    io.setup(21, io.OUT)			# LED indicator output

def eyeOutput():
    io.output(21, 0)
    if io.input(23) != 1:
        io.output(21, 1)
