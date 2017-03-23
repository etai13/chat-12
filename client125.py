import socket
import select
import msvcrt

IP = "127.0.0.1"
PORT = 23
my_socket = socket.socket()
my_socket.connect((IP, PORT))
open_server_socket = []
s = ""
messages = []
while True:
    if msvcrt.kbhit() == 1:
        print "in"
        c = msvcrt.getch()
        while c != '.':
            s += c
            c = msvcrt.getch()
        my_socket.send(s)
        s = ""
    rlist, wlist, xlist = select.select([my_socket] + open_server_socket, open_server_socket, [], 0.5)
    if my_socket in rlist:
        data = my_socket.recv(1024)
        print data
