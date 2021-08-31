# Librerias
import pandas as pd
import numpy as np
from datetime import datetime
# Librerias Flask
from flask import Flask, request
from flask import render_template
from flask import Response
from flask import jsonify
import json
import sys
import random
import requests
import threading
import time

arg = sys.argv
workers= int(arg[1])
ip= arg[2]
port = int(arg[3])

# Inicicalizar Flask
# from flask import Flask
app = Flask(__name__)
app.debug = True
app.config['PROPAGATE_EXCEPTIONS'] = True

def init_workres_array(workers):
    pet_in = []
    for i in range(workers):
        pet_in.append([])
    return pet_in

def RaoundRobin(cargas, traza, workers):
    for x in range(len(traza)):
        select_bin = x % workers
        cargas[select_bin].append(traza[x])
    return cargas

def enviar_datos(url,datas):
    headers = {'PRIVATE-TOKEN': '<your_access_token>', 'Content-Type':'application/json'}
    requests.post(url, data=json.dumps(datas), headers=headers)

@app.route('/recibir',methods = ['POST'])
def k_dividir():
    inicio = time.time()
    # Rwcibe los datos
    message = request.get_json()
    k_ = message['K']
    # genera los balaneacdores vacios
    init_k = init_workres_array(workers)
    # Divide las cargas entre los n workers
    init_k = RaoundRobin(init_k,k_,workers)
    # Despliega los balanceos
    # Calculo de las ip
    peticiones = []
    for x in range(workers):
        if (len(init_k[x])>0):
            url = "http://"+ip+":"+str(port)+str(x)+"/recibir"
            data = {"K": init_k[x],
                    "name":message['name']}
            aux = threading.Thread(target=enviar_datos,args=(url,data))
            aux.start() 
    fin = time.time()
    app.logger.error("Balance K ------- = "+str(fin-inicio))
    return jsonify({'hola':init_k})
    
# Prueba
@app.route('/Prueba')
def prueba():
    app.logger.error('Si llegooooooo')
    return jsonify({'hola':"SI"})


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)