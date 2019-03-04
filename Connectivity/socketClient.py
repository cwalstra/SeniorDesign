import socket
import netifaces as ni

ni.ifaddresses('eth0')
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
host = str(ip)
port = 5001

mySocket = socket.socket()
mySocket.connect((host,port))

message = input(" ? ")

while message != 'q':\
    mySocket.send(message.encode())
    data = mySocket.recv(1024).decode()
                                            
    print ('Received from server: ' + data)
    message = input(" ? ")

mySocket.close()
