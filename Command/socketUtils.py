import netifaces as ni
import socket
import sys

def socketSetup():
    # Get device's IP address
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    server = str(ip)
    port = 5003

    # Start socket
    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err_msg:
        print("Socket failed on startup")
        sys.exit

    # Wait for another device to connect
    try:
        mySocket.bind((server, port))

        mySocket.listen(1)
        connection, address = mySocket.accept()
    except:
        print("Socket failed to connect")
        sys.exit()

    return (connection, address)
