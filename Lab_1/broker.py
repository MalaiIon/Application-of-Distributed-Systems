    #!/usr/bin/env python3

import socket
import _thread
import time
import sqlite3
connection = sqlite3.connect("mydb.db")
cursor = connection.cursor()
from translate import Translator


global connex, SUBSCRIBERS, MESSAGES, f, LANGUAGES
connex = []
HOST = '127.0.0.1'  
PORT = 65443        

f = open("write-tap.txt", "a+")

SUBSCRIBERS = {"news":[],"medicine":[],"learning":[],"errors":[]}
MESSAGES = {"news":[],"medicine":[],"learning":[],"errors":[]}
LANGUAGES = {"en":[],"ro":[],"ru":[]}

def handle_error(connection, message):
	time.sleep(1)
	try:
		connection.send(message.encode())
	except:
		try:
			time.sleep(3)
			connection.send(message.encode())
		except:
			MESSAGES["errors"].append(message)

			for subscriber in SUBSCRIBERS["errors"]:
				subscriber.send(message.encode())



def handle_client(connection, data, channel):
    global connex, LANGUAGES
    connex.append(connection)

    print (SUBSCRIBERS)
    for message in MESSAGES[channel]:
        time.sleep(1)					
        try:
            connection.send(message.encode())

        except:

            handle_error(connection, message)


    last_data = None
    while True:
        if data is not last_data: 
            f.write(time.ctime() + " " + str(addr) + " " + data.decode()+"\n")
        if data.decode().partition(channel)[2].startswith("subscribe"):
            SUBSCRIBERS[channel].append(connection)
        elif data.decode().endswith("unsubscribe"):
            SUBSCRIBERS[data.decode().partition("unsubscribe")[0]].remove(connection)
        elif data.decode().endswith("subscribe"):
            SUBSCRIBERS[data.decode().partition("subscribe")[0]].append(connection)

        elif data.decode().partition(channel)[2].startswith("unsubscribe"):
            SUBSCRIBERS[channel].remove(connection)

        if data.decode().startswith("en"):
            LANGUAGES["en"].append(connection)
        elif data.decode().startswith("ro"):
            LANGUAGES["ro"].append(connection)
        elif data.decode().startswith("ru"):
            LANGUAGES["ru"].append(connection)

        data = connection.recv(1024)


        if data is None:
            break

        last_data = data

    connection.close()




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
            conn, addr = s.accept()
            res = []
            print ("New connection!", str(addr))
            data = conn.recv(1024)
            f.write(time.ctime() + " " + str(addr) + " " + data.decode() + "\n")
            for channel in SUBSCRIBERS.keys():
               if data.decode().startswith(channel):
                  if data.decode().partition(channel)[2].startswith("subscribe"):
                     _thread.start_new_thread(handle_client ,(conn, data, channel, ))
                  if data.decode().partition(channel)[2].startswith("unsubscribe"):
                     SUBSCRIBERS[channel].remove(conn) 
                     pass
                  if data.decode().partition(channel)[2].startswith("publish"):
                      n_msg = int(data.decode().partition("publish")[2][0])

                      for i in range(n_msg): 
                          if "news" in data.decode().partition("publish")[2][1:]:
                              channel = "news"


                          elif "school" in data.decode().partition("publish")[2][1:]:
                              channel = "learning"
                          elif "headache" in data.decode().partition("publish")[2][1:]:
                              channel = "medicine"

                          if channel is "news":
                              cursor.execute("SELECT * FROM news")

                          res = cursor.fetchall()



                          for c in SUBSCRIBERS[channel]:

                              try:
                                  to_send = data.decode().partition("publish")[2][1:]
                                  for pair in res:
                                      if pair[0] in to_send:
                                          ind = to_send.index(pair[0])+len(pair[0])
                                          to_send = to_send[:ind] + " (The news was published in " + pair[1] + ")" + to_send[ind:]
                                  MESSAGES[channel].append(to_send)
                                  MESSAGES[channel] = MESSAGES[channel][-3:] 
                                  print (f.read())


                                  for language in LANGUAGES:
                                      for connection in LANGUAGES[language]:
                                          if c is connection:
                                            translator = Translator(from_lang="autodetect", to_lang=language)
                                            temp = translator.translate(to_send)
                                            if "PLEASE SELECT TWO DISTINCT LANGUAGES" not in temp:
                                                to_send = temp
                                  c.send(to_send.encode()) 
                                  print (to_send)
                              except Exception as e:
                                  print (e)
                                  handle_error(connection, to_send)

                          data = conn.recv(1024)




    s.close()
