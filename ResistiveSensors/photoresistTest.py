# This file is designed to test the use of
#   the photoresistor and laser with the Pi
#   GPIO pins to determine if the laser is
#   connected or not. The output will be
#   indicated by an LED.

import time
import RPi.GPIO as io

LED = 12

io.setwarnings(False)
io.setmode(io.BCM)
io.setup(23, io.IN, pull_up_down=io.PUD_UP)	# voltage sensing pin
io.setup(LED, io.OUT)				# LED indicator output

print("Running photoresistor test...")
print("Type Ctrl-C to quit")

while True:
	io.output(LED, 0)
	if io.input(23) == 1:
		time.sleep(0.1)
	else:
		io.output(LED, 1)
		time.sleep(0.1)
