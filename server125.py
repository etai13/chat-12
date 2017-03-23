import socket
import select
import datetime

ABC = "abcdefghijklmnopkrstuvwxz"


def find_string(m):
    s = ""
    for char in m:
        if char in ABC:
            s += char
    return s


def get_time():
    time = str(datetime.datetime.now())
    time = time[11:16]
    return time


def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        for client in wlist:
            if client is not client_socket:
                client.send(data)
                messages_to_send.remove(message)


def send_to_sender(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        for client in wlist:
            if client is client_socket:
                client.send(data)
                messages_to_send.remove(message)

server_socket = socket.socket()

server_socket.bind(("0.0.0.0", 23))
server_socket.listen(5)

open_client_socket = []
messages_to_send = []
hard_coded = []
kicked_users = []
muted = []

print "starting..."

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_socket.append(new_socket)
        else:
            data = current_socket.recv(1024)
            l = int(data[0])
            p = data[l + 1]
            m = data[l + 2:]
            s = find_string(m)
            if "uit" in s:
                l = int(data[0])
                messages_to_send.append((current_socket, get_time() + " " + data[1: l + 1] + " has left the chat"))
                print "Connection with client closed"
                send_waiting_messages(wlist)
                open_client_socket.remove(current_socket)
            else:
                l = int(data[0])
                p = data[l + 1]
                if p == '1':
                    m = data[l + 2:]
                    if data[1: l + 1] in kicked_users:
                        print "not in chat"
                    elif data[1] == '@':
                        print "name is incorrect"
                        messages_to_send.append((current_socket, "name is incorrect"))
                        send_to_sender(wlist)
                    elif data[1: l + 1] in muted:
                        print "client is muted"
                        messages_to_send.append((current_socket, "you're muted"))
                        send_to_sender(wlist)
                    else:
                        s = find_string(m)
                        time = get_time()
                        if data[1: l + 1] in hard_coded:
                            messages_to_send.append((current_socket, time + " @" + data[1: l + 1] + ": " + s))
                        else:
                            messages_to_send.append((current_socket, time + " " + data[1: l + 1] + ": " + s))
                        send_waiting_messages(wlist)
                if p == '2':
                    l = int(data[0])
                    s = data[1: l + 1]
                    if s in kicked_users:
                        print "can't do that"
                        messages_to_send.append((current_socket, "can't do that"))
                        send_to_sender(wlist)
                    else:
                        p = data[l + 1]
                        m = data[l + 2:]
                        f = find_string(m)
                        hard_coded.append(f)
                        print "done"
                if p == '3':
                    l = int(data[0])
                    s = data[1: l + 1]
                    if not s in hard_coded:
                        print "can't to that"
                        messages_to_send.append((current_socket, "can't do that"))
                        send_to_sender(wlist)
                    else:
                        m = data[l + 2:]
                        s = find_string(m)
                        kicked_users.append(s)
                        print "kicked done"
                        messages_to_send.append((current_socket, s + " kicked from chat"))
                        send_waiting_messages(wlist)
                if p == '4':
                    l = int(data[0])
                    s = data[1: l + 1]
                    if not s in hard_coded:
                        print "can't to that"
                        messages_to_send.append((current_socket, "can't do that"))
                        send_to_sender(wlist)
                    else:
                        m = data[l + 2:]
                        s = find_string(m)
                        muted.append(s)
                        print "muted done"
                        messages_to_send.append((current_socket, s + " is muted"))
                        send_waiting_messages(wlist)
                if p == '5':


    send_waiting_messages(wlist)