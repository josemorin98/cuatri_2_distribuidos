#!/usr/bin/python3           # This is server.py file
import socket                                         
import json
import sys
import pandas as pd
import os

aux=[]
# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9999                         

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(1)                                           
terminar = True
while terminar:
    # establish a connection
    clientsocket,addr = serversocket.accept()      

    print("Got a connection from %s" % str(addr))

    msg = clientsocket.recv(1024)
    msg2 = 'Thank you for connecting'+ "\r\n"
    msg2 = msg.decode("utf-8");
    msg2 = json.loads(msg2)
    print(msg2)
    os.system('./single ' + str(msg2['meanInter']) + " " + str(msg2['timeSer']) + " " + str(msg2['pet']) + " > simulator.csv")
    single = pd.read_csv("./simulator.csv", delimiter=',')     
    # Resultados
    
    if(len(single.iloc[0])>1):
        aux='{"Average_delay_in_queue":' + str(single['Average_delay_in_queue'][0]) + ',"Average_number_in_queue":' + str(single['Average_number_in_queue'][0]) +',"Server_Utilization":' + str(single['Server_Utilization'][0])+',"Time_simulation_ended":' + str(single['Time_simulation_ended'][0])+'}'
    else:
        aux='{"Average_delay_in_queue": "Overflow", "Average_number_in_queue": "Overflow","Server_Utilization": "Overflow","Time_simulation_ended": ' + str(single['Overflow_of_the_array_time_arrival_at_time'][0])+"}"
    print(aux)
    data = json.loads(aux)
    clientsocket.send(bytes(json.dumps(data),encoding="utf-8"))
    clientsocket.close()
    terminar = False
serversocket.close()