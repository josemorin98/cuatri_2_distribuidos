#!/usr/bin/python3           # This is client.py file

import socket
import json
import sys

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 51000

# connection to hostname on the port.
s.connect((host, port))        
m = "{\"meanInter\": 1.5, \"timeSer\": 0.5, \"pet\": 98}"
data = json.loads(m)
s.sendall(bytes(json.dumps(data),encoding="utf-8"))

# Receive no more than 1024 bytes
msg = s.recv(1024)                                     

s.close()
print (msg.decode("utf-8"))