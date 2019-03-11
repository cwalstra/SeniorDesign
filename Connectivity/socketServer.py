import socket
import sys
import netifaces as ni
import time
import cv2
import struct
import pickle
import numpy as np

ni.ifaddresses('eth0')
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
server = str(ip)
server = "127.0.0.1"
port = 5003

try:
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err_msg:
    print("Socket start up failed.  Error code: " + str(err_msg[0]) + " , Error message : " + err_msg[1])
    sys.exit()

mySocket.bind((server,port))
print("Socket ready")

mySocket.listen(1)
conn, addr = mySocket.accept()
print("Connection from: " + str(addr))

payload_size = struct.calcsize("L")
try:
    while True:
        data = None
        print("HMS Daring")
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        print("HMS Brazen")
        msg_size = struct.unpack("L", packed_message_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        print(frame)
        cv2.imshow("Bad Name", frame)
except:
    conn.close
