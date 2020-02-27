import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('0.0.0.0', 8080))
sock.send("I am CLIENT<br>".encode())
from_server = sock.recv(4096)
sock.close()
print(from_server.decode())