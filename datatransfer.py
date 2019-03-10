import socket
import sys
import argparse

# params :
# -s    server      
# -c    client
# -p  port
# -h  host
# -f    filename    

def serverRoutine(sock, host, port):

    sock.bind((host, port))
    sock.listen(1)
    conn, addr = sock.accept()

    filename = bytes(0)
    while sys.getsizeof(filename) < 255:
        recvdata = conn.recv(1)

        if recvdata == '.':
            recvdata += conn.recv(3)
            filename += recvdata
            break

        filename += recvdata

    print(filename)

    try:
        file = open(filename, 'wb')

        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
        
        file.close()

        conn.sendall("DONE!")
    except:    
        print("Couldn't create the file!")

    return

def clientRoutine(sock, host, port, data, filename):

    try:
        sock.connect((host, port))
    except:
        print("Couldn't connect to server!")
        return
    
    try:
        sock.sendall(filename)
        sock.sendall(data)
        print(sock.recv(32))
    except:
        print("Couldn't send data to server!")

    return

HOST =  socket.gethostbyname(socket.gethostname())
PORT = 17000
SERVER = True
FILE_NAME = ''
FILE_DATA = ''
FILE = ''

parser = argparse.ArgumentParser()
parser.add_argument("-s", help = "Server", action = "store_true")
parser.add_argument("-c", help = "Client", action = "store_true")
parser.add_argument("-p", type = int, help = "Setup the local port")
parser.add_argument("-ht", type = str, help = "Setup the local host")
parser.add_argument("-f", type = str, help = "The name of the file")
args = parser.parse_args()

if args.s:
    SERVER = True

if args.c:
    SERVER = False

if args.p:
    PORT = args.p

if args.ht:
    HOST = args.ht

if (args.f != None) and (args.c == True):
    FILE_NAME = args.f
    try:
        FILE = open(FILE_NAME, 'rb')
        FILE_DATA = FILE.read()
        FILE.close()
    except:
        print("Couldn't open the file!")
        sys.exit(1)
elif ((args.f == None) and (args.c == True)) or ((args.f != None) and (args.c == False)):
    print("Use the -f flag if it's client.")
    sys.exit(1)

s = socket.socket()

print("Server IP: ", HOST)

if SERVER == True:
    serverRoutine(s, HOST, PORT)
else:
    clientRoutine(s, HOST, PORT, FILE_DATA, FILE_NAME)

s.close()