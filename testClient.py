import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9999       # The port used by the server

list = json.dumps(['NoseThe', 1, 600, 3000]).encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(list)
    data = s.recv(100)

print('Received', json.loads(data.decode('utf-8')))
