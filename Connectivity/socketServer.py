import socket
import sys
import netifaces as ni
import time

ni.ifaddresses('eth0')
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
server = str(ip)
port = 5001

try:
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err_msg:
    print("Socket start up failed.  Error code: " + str(err_msg[0]) + " , Error message : " + err_msg[1])
    sys.exit()

mySocket.bind((server,port))

mySocket.listen(1)
conn, addr = mySocket.accept()
print("Connection from: " + str(addr))

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(str(data))

    data = input("New message: ")
    conn.send(data.encode())

conn.close
