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

def lookForPeople(frame):
    image = frame.array
    image = imutils.resize(image, width=min(400,image.shape[1]))
    orig = image.copy()

    (rects,weights) = hog.detectMultiScale(image, winStride = (4, 4), padding = (8, 8), scale = 1.05)

    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    rects = np.array([[x, y, x+w, y+h] for (x, y, w, h) in rects])
    picks = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    people = str(len(picks))

    goodConnection = True
    mySocket.send(people.encode())
    print("Data sent")
    data = mySocket.recv(1024).decode()
    print("Data: " + data)
    if data != "ack":
        goodConnection = False
        print("Connection Dropped")

    for (xA, yA, xB, yB) in picks:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

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
        if not lookForPeople(newFrame):
            break

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
