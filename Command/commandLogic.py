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
from thermCam import thermCamSetup, thermCamReading
from socketUtils import socketSetup

def main():
    (conn, addr) = socketSetup()
    motorGroup = thermCamSetup()
    peopleHistory = [0, 0, 0, 0, 0, 0, 0, 0]
    thermHistory = [0, 0, 0, 0]
    eyeHistory = [0, 0, 0, 0]
    levelHistory = [0, 0, 0, 0]
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            numberOfPeople = int(data)
            peopleHistory.insert(0, numberOfPeople)
            peopleHistory.pop()

            conn.send("ack".encode())
            thermCamOutput = thermCamReading(motorGroup)
            thermHistory.insert(0, thermCamOutput)
            thermHistory.pop()

            eyeOut = #function
            eyeHistory.insert(0, eyeOut)
            eyeHistory.pop()

            levelSensorOut = #function
            levelHistory.insert(0, levelSensorOut)
            levelHistory.pop()

            if 1 in peopleHistory or 2 in people History:
                if True in thermHistory and True in eyeHistory or
                   True in thermHistory and True in levelHistory or
                   True in eyeHistory and True in levelHistory:
                       # do something positive
            elif True in thermHistory and True in eyeHistory and True in levelHistory:
                # do positive thening
    except:
        conn.close()

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
