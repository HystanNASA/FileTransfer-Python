import socket

HOST = '192.168.0.12'
PORT = 17000
MSG  = 'Hello there!'

sock = socket.socket()
sock.connect((HOST, PORT))
sock.sendall(MSG.encode('ascii'))

sock.close()
