#!/usr/bin/env python3

import socket
import _thread


MESSAGE_TYPE = "subscribe"


CHANNEL = "news"

DATA = CHANNEL + MESSAGE_TYPE

BHOST = '127.0.0.1'  # The BROKER's hostname or IP address
BPORT = 65443        # The port used by the BROKER

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.connect((BHOST, BPORT))
data = s.sendall(DATA.encode())


def listen(connection, data):
    while True:
        data = connection.recv(1024)

        if data is None:
            break
        print('\nClient says: ' + data.decode())


    connection.close()



_thread.start_new_thread(listen ,(s, data, ))

while True:
    menu = input("Command (subscribe/unsubscribe channel_name or first 2 initials for desired language): ")
    if menu.startswith("subscribe"):
        if menu.partition("subscribe ")[2]:
            CHANNEL = menu.partition("subscribe ")[2]
            MESSAGE_TYPE = "subscribe"
            DATA = CHANNEL + MESSAGE_TYPE
            data = s.sendall(DATA.encode())

    elif menu.startswith("unsubscribe"):
            CHANNEL = menu.partition("unsubscribe ")[2]
            MESSAGE_TYPE = "unsubscribe"
            DATA = CHANNEL + MESSAGE_TYPE
            data = s.sendall(DATA.encode())
    elif menu.startswith("en"):
            data = s.sendall("en".encode())
    elif menu.startswith("ro"):
            data = s.sendall("ro".encode())
    elif menu.startswith("ru"):
            data = s.sendall("ru".encode())

s.close()
