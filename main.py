import socket
import os
import argparse

# -s    server
# -c    client
# -ip   ip
# -p    port
# -d    destination
# -f    name of file

# server receives the file, client sends the file

def clientRoutine(host, port, filename):
    
    if filename == '':
        return 1

    sockfd = socket.socket()
    data = None

    sockfd.connect((host, port))

    with open(filename, 'rb') as f:
        data = f.read()
        f.close()

    sockfd.sendall(filename.encode('ascii'))
    sockfd.recv(10)
    sockfd.sendall(data)

    sockfd.close()

    return 0

def serverRoutine(host, port, destination):
    sockfd = socket.socket()

    sockfd.bind((host, port))
    sockfd.listen(5)
    conn, addr = sockfd.accept()

    filename = conn.recv(10)
    conn.sendall(b'k')

    data = conn.recv(1024)
    while(True):
        d = conn.recv(1024)
        if not d:
            break
        data = data + d

    if destination != '':
        filename = destination + filename

    with open(filename, 'wb') as f:
        f.write(data)
        f.close()

    sockfd.close()

    return 0

def main():

    HOSTIP = ''
    DESTINATION = ''
    FILENAME = ''
    SERVER = True
    PORT = 17000

    parser = argparse.ArgumentParser(description = 'data transer')
    parser.add_argument('-s', action = 'store_true')
    parser.add_argument('-c', action = 'store_false')
    parser.add_argument('-ip', type=str)
    parser.add_argument('-p', type=int)
    parser.add_argument('-d', type=str)
    parser.add_argument('-f')

    args = parser.parse_args()

    if args.f:
        FILENAME = args.f

    if args.s == True:
        SERVER = True
    else:
        SERVER = False
    
    if args.ip:
        HOSTIP = args.ip
    else:
        HOSTIP = socket.gethostbyname(socket.gethostname())
        
    if args.p:
        PORT = args.p
    
    if args.d:
        DESTINATION = args.d

    if SERVER == True:
        print("Server IP: ", HOSTIP)
        if serverRoutine(HOSTIP, PORT, DESTINATION) != 0:
            print("Something's gone wrong")
    else:
        if clientRoutine(HOSTIP, PORT, FILENAME) != 0:
            print("Use arguments")
            exit(1)

if __name__ == "__main__":
    main()

