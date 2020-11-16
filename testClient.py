import socket
import json
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 443       # The port used by the server

list = b'NoseThe\0011\001600\0013000'

def test():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(list)
        data = s.recv(100).decode()

        print('Received', data)

if __name__ =='__main__':
    for i in range(100):
        test()
