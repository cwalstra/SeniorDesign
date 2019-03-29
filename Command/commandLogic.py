'''
This file implements the command and control logic for the saving system.

Written by Chris Walstra (@cwalstra)
'''

# Imports
import socket
import sys
import netifaces as ni
import time
import numpy as np
import traceback
from thermCam import thermCamSetup, thermCamReading
from socketUtils import socketSetup
from eyeUtils import eyeSetup, eyeOutput
from levelUtils import levelSetup, levelOutput
from timeit import default_timer as Timer

def main():
    debug = True
    if debug:
        print("Thermal Camera setup...")
    motorGroup = thermCamSetup()
    if debug:
        print("Photoelectric Eye setup...")
    eyeSetup()
    if debug:
        print("Water Level Sensor setup...")
    read, stdev = levelSetup()

    print("Socket setup...")
    (conn, addr) = socketSetup()
    peopleHistory = [0, 0, 0, 0, 0, 0, 0, 0]
    thermHistory = [0, 0, 0, 0]
    eyeHistory = [0, 0, 0, 0]
    levelHistory = [0, 0, 0, 0]

    if debug:
        print("Starting Main Loop")

    try:
        while True:
            start = Timer()
            data = conn.recv(1024).decode()
            readEnd = Timer()
            if not data:
                print("Not Data")
                break
            else:
                if debug:
                    print("Data: " + data)
            ack = "ack"
            conn.send(ack.encode())
            numberOfPeople = int(data)
            peopleHistory.insert(0, numberOfPeople)
            peopleHistory.pop()
            if debug:
                print(peopleHistory)

            thermCamOutput = thermCamReading(motorGroup)
            thermHistory.insert(0, thermCamOutput)
            thermHistory.pop()
            if debug:
                print(thermHistory)

            eyeOut = eyeOutput()
            eyeHistory.insert(0, eyeOut)
            eyeHistory.pop()
            if debug:
                print(eyeHistory)

            levelSensorOut, read, stdev = levelOutput(read, stdev)
            levelHistory.insert(0, levelSensorOut)
            levelHistory.pop()
            if debug:
                print(levelHistory)

            if 1 in peopleHistory or 2 in peopleHistory:
                if True in thermHistory and True in eyeHistory or \
                   True in thermHistory and True in levelHistory or \
                   True in eyeHistory and True in levelHistory:
                       # do something positive
                       print("Saving needed")
                       continue
            elif True in thermHistory and True in eyeHistory and True in levelHistory:
                # do positive thing
                print("Saving needed")
            else:
                # do negative thing
                print("    No saving needed")

            end = Timer()
            readTime = readEnd - start
            elapsedTime = end - start
            print('Runtime: ' + str(elapsedTime))
            print('Readtime: ' + str(readTime))
    except Exception:
        traceback.print_exc()

    conn.close()
'''
# Get information in from the thermal camera, the water level sensor, and the photoelectric eye

# Store values in list to maintain memory

# Evaluate for test conditions
# Is there a person/people in the pool area/has there been in the past few samples (last 8 samples)
# Does the thermal camera see someone recently (last 4 samples)?
# Has the photoelectric eye been tripped in the past 4 samples?
# Has the waterlevel sensor detected in a disturbance in the past 4 samples?
'''
if __name__ == "__main__":
    main()
