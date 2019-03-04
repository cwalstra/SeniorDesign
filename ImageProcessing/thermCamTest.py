import time
import busio
import board
import adafruit_amg88xx
import RPi.GPIO as GPIO
 
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

LED = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)

while True:
    print("\n")
    print("Splitter")
    highTemps = 0
    for row in amg.pixels:
        # Pad to 1 decimal place
        print(['{0:.1f}'.format(temp) for temp in row])
        for temp in row:
            if temp > 26.0:
                highTemps += 1
    if highTemps > 4:
        GPIO.output(LED, True)
    else:
        GPIO.output(LED, False)
