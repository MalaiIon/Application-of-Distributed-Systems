#!/usr/bin/env python3

import socket
import math
from textwrap import wrap



HOST = '127.0.0.1'  # The BROKER's hostname or IP address
PORT = 65443       # The port used by the BROKER
BUFFSIZE=1024


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))

    MESSAGE_TYPE = "publish"

    CHANNEL = input("Please introduce your channel: ")


    MESSAGE = input("Please introduce your message: ")

    MESSAGE_TYPE += str(math.ceil(len(MESSAGE + MESSAGE_TYPE) / BUFFSIZE))

    DATA = CHANNEL + MESSAGE_TYPE + MESSAGE
    REAL_BUFFSIZE = BUFFSIZE - len(CHANNEL) - len(MESSAGE_TYPE)



    #s.sendall(DATA.encode()) #declare nr of stuffs

    for i in range(math.ceil(len(DATA) / BUFFSIZE)): #Serialize
        #s.sendall(DATA.encode())

        DATA = CHANNEL + MESSAGE_TYPE + wrap(MESSAGE,REAL_BUFFSIZE)[i]

        s.sendall(DATA.encode())
        #data = conn.recv(1024)




print('Your message has been sent.')
