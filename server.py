import socket

HOST = '192.168.0.12'
PORT = 17000

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen()
(conn, addr) = sock.accept()

data = conn.recv(1024)
print(data.decode('ascii'))
conn.close()
