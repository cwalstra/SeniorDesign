import socket
import netifaces as ni
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from sys import getsizeof
import pickle
import struct

host = "127.0.0.1"
port = 5003

mySocket = socket.socket()
mySocket.connect((host,port))

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

try:
    for frame in camera.capture_continuous("output.jpg", format="bgr", use_video_port=True):
        newFrame = read("output.jpg", "rb")
        data = pickle.dumps(newFrame)
        clientsocket.sendall(struck.pack("L", len(data)) + data)
except:
    mySocket.close()

