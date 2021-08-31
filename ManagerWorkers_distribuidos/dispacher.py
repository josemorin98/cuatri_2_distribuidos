import random
import numpy as np
import socket
import json
import sys
import os
import threading

def display_workers(workers):
    for x in range(workers):
        os.system('docker run -d --name worker'+ str(x)+' -p 5100'+str(x)+':9999 simulatordos:singlesdos')
    return ("Se desplgaron " + str(workers) + " workers")

def drop_workers(workers):
    for x in range(workers):
        os.system('docker rm -f worker'+ str(x))
    return ("Se eliminaron " + str(workers) + " workers")

def client_socket():
    print("nada")

def RaoundRobin(cargas, traza, workers):
    for x in range(len(traza.iloc[:,0])):
        select_bin = x % workers
        cargas[select_bin].append(traza[0][x])
    return cargas

def PseudoRandom(cargas, traza, workers):
    for x in range(len(traza.iloc[:,0])):
        select_bin = random.randint(0, workers-1)
        cargas[select_bin].append(traza[0][x])
    return cargas

def TwoChoices(cargas, traza, workers):
    select_bin = 0
    select_bin2 = 0
    aux = True
    if(workers==1):
        for x in range(len(traza.iloc[:,0])):
            cargas[0].append(traza[0][x])
    else:
        for x in range(len(traza.iloc[:,0])):
            select_bin = random.randint(0, workers-1)
            while(aux):
                select_bin2 = random.randint(0, workers-1)
                if(select_bin != select_bin2):
                    aux = False
            if( len(cargas[select_bin]) < len(cargas[select_bin2]) ):
                cargas[select_bin].append(traza[0][x])
            else:
                cargas[select_bin2].append(traza[0][x])
            aux = True
    return cargas

def sokcet_client(meanInter, timeSer, pet, port2):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # get local machine name
    host = socket.gethostname()                           

    port = port2

    # connection to hostname on the port.
    s.connect((host, port))        
    m = '{\"meanInter\": '+str(meanInter)+', \"timeSer\": '+str(timeSer)+', \"pet\": '+str(pet)+'}'
    data = json.loads(m)
    s.sendall(bytes(json.dumps(data),encoding="utf-8"))

    # Receive no more than 1024 bytes
    msg = s.recv(1024)                                     

    s.close()
    # print (msg.decode("utf-8"))
    return msg.decode("utf-8")