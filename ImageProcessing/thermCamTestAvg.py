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

noDetectRange = []
detectRange = []

while True:
    print("\n")
    print("Splitter")
    highTemps = 0
    arraySum = 0
    rowCounter = 0
    highTempList = []
    maxTemp = 0
    minTemp = 100
    for row in amg.pixels:
        # Pad to 1 decimal place
        rowCounter += 1
        columnCounter = 0
        #print(['{0:.1f}'.format(temp) for temp in row])
        for temp in row:
            arraySum += temp
            columnCounter += 1
            if temp > 26.0:
                highTemps += 1
                highTempList.append((rowCounter, columnCounter))
            if temp > maxTemp:
                maxTemp = temp
            if temp < minTemp:
                minTemp = temp

    average = arraySum / 64

    if maxTemp - average >= 1.8:
        GPIO.output(LED, True)
        detectRange.append(maxTemp - average)
    else:
        GPIO.output(LED, False)
        noDetectRange.append(maxTemp - average)

    print(highTempList)
    print(noDetectRange)
    print(detectRange)

'''
Potential algorithms
Look for groups - make a list of tuples with indices ?????

Adjust the threshold temperature and/or # of positive values

Look for values that stand out with respect to average 
'''

