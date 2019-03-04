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

#TODO: Implement multiprocessing, probably via pool to limit the number of processes, may need to add locks to properly manage resourcews

def lookForPeople(frame):
    image = frame.array
    image = imutils.resize(image, width=min(400,image.shape[1]))
    orig = image.copy()

    (rects,weights) = hog.detectMultiScale(image, winStride = (4, 4), padding = (8, 8), scale = 1.1)

    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    rects = np.array([[x, y, x+w, y+h] for (x, y, w, h) in rects])
    picks = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    if len(picks) > 0:
        GPIO.output(LED, True)
    else:
        GPIO.output(LED, False)

    for (xA, yA, xB, yB) in picks:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow("Frame", image)


# LED Setup
LED = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)

# Set up OpenCV for person detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Camera initialization
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

for newFrame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start = Timer()
    lookForPeople(newFrame) 

    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    end = Timer()
    elapsedTime = end - start
    print('Runtime: {0}', elapsedTime)
    if key == ord("q"):
        break
