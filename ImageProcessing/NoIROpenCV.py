'''
This code was written by Chris Walstra based on a program written by Adrian Rosebrock on the PyImageSearch blog.

It implements a person detection algorithm for a video coming from a Raspberry Pi camera while sending the data to an off-machine socket server.
'''

from __future__ import print_function
from imutils.object_detection import non_max_suppression
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import imutils
import numpy as np
from imutils import paths
import RPi.GPIO as GPIO
from multiprocessing import Pool
from timeit import default_timer as Timer
import netifaces as ni
import socket
import traceback
from os import system

def lookForPeople(frame):
    # make the picture smaller to simplify search
    image = frame.array
    image = imutils.resize(image, width=min(400,image.shape[1]))
    orig = image.copy()

    # Run the person detection algorithm
    (rects,weights) = hog.detectMultiScale(image, winStride = (4, 4), padding = (8, 8), scale = 1.05)

    # Created rectangles to frame the people
    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Remove rectangles that overlap too much
    rects = np.array([[x, y, x+w, y+h] for (x, y, w, h) in rects])
    picks = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    people = str(len(picks))

    # Send the number of people out
    goodConnection = True
    mySocket.send(people.encode())
    print("Data sent")
    data = mySocket.recv(1024).decode()
    print("Data: " + data)
    if data != "ack":
        goodConnection = False
        print("Connection Dropped")

    # Draw rectangles around the people
    for (xA, yA, xB, yB) in picks:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    # show the image
    cv2.imshow("Frame", image)

    return goodConnection

# Socket Setup
host = "153.106.113.63"
port = 5002
mySocket = socket.socket()
mySocket.connect((host, port))

# Set up OpenCV for person detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

myString = ""

# Camera initialization
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

try:
    for newFrame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        start = Timer()
        # Copy the image to allow stitching
        imwrite("leftSide.jpeg", frame)
        system("scp leftSide.jpeg pi@153.106.113.238:SeniorDesign/StitchingImages")
        if not lookForPeople(newFrame):
            break

        # Exit strategy
        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        end = Timer()
        elapsedTime = end - start
        print('Runtime: {0}', elapsedTime)
        myString = str(newFrame)
        if key == ord("q"):
            break

except KeyboardInterrupt:
    print(myString)
except Exception:
    traceback.print_exc()

mySocket.close()
