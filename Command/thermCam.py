import time
import busio
import board
import adafruit_amg88xx
import RPi.GPIO as GPIO

def thermCamSetup():
    i2c = busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c)
    return amg

def thermCamReading(amg):
    highTemps = 0
    rowCounter = 0
    highTempList = []
    for row in amg.pixels:
        # Pad to 1 decimal place
        rowCounter += 1
        columnCounter = 0
        for temp in row:
            columnCounter += 1
            if temp > 26.0:
                highTemps += 1
                highTempList.append((rowCounter, columnCounter))

    if highTemps > 4:
        return True
    else:
        return False

'''
Potential algorithms
Look for groups - make a list of tuples with indices ?????

Adjust the threshold temperature and/or # of positive values

Look for values that stand out with respect to average 
'''

