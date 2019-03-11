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

def socketSetup():
# Start a server to get information from the Pi processing the NoIR feed
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    server = str(ip)
    port = 5001

    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err_msg:
        print("Socket failed on startup")
        sys.exit()

    mySocket.bind((server,port))

    mySocket.listen(1)
    connection, address = mySocket.accept()

    print("Connection from: " + str(addr))

    return (connection, address)

def main():
    (conn, addr) = socketSetup()
    # try/while True:
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            conn.send("ack".encode())
    except:
        conn.close()

    conn.close()

# Get information in from the thermal camera, the water level sensor, and the photoelectric eye

# Store values in list to maintain memory

# Evaluate for test conditions
# Is there a person/people in the pool area/has there been in the past few samples (last 8 samples)
# Does the thermal camera see someone recently (last 4 samples)?
# Has the photoelectric eye been tripped in the past 4 samples?
# Has the waterlevel sensor detected in a disturbance in the past 4 samples?

if __name__ == "__main__":
    main()
