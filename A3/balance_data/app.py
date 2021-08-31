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
data_balance = arg[4]
type_balance = arg[5]

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

def RaoundRobin(cargas, list_to, workers):
    for x in range(len(list_to)):
        select_bin = x % workers
        cargas[select_bin].append(list_to[x])
    return cargas

def PseudoRandom(cargas, list_to, workers):
    for x in range(len(list_to)):
        select_bin = random.randint(0, workers-1)
        cargas[select_bin].append(list_to[x])
    return cargas

def TwoChoices(cargas, list_to, workers):
    select_bin = 0
    select_bin2 = 0
    aux = True
    if(workers==1):
        for x in range(len(list_to)):
            cargas[0].append(list_to[x])
    else:
        for x in range(len(list_to)):
            select_bin = random.randint(0, workers-1)
            while(aux):
                select_bin2 = random.randint(0, workers-1)
                if(select_bin != select_bin2):
                    aux = False
            if( len(cargas[select_bin]) < len(cargas[select_bin2]) ):
                cargas[select_bin].append(list_to[x])
            else:
                cargas[select_bin2].append(list_to[x])
            aux = True
    return cargas

def type_blane_cond(tipo):
    if (tipo=='Y'):
        return 'Ano'
    elif (tipo=='M'):
        return 'Mes'
    elif (tipo=='D'):
        return 'Dia'
    else:
        return 'Mes'

def enviar_datos(url,datas):
    headers = {'PRIVATE-TOKEN': '<your_access_token>', 'Content-Type':'application/json'}
    requests.post(url, data=json.dumps(datas), headers=headers)

def read_CSV(name):
    return pd.read_csv("./data/"+name+".csv")


# @app.route('/dividir_K')
@app.route('/recibir',methods = ['POST'])
def k_dividir():
    inicio=time.time()
    # Rwcibe los datos
    message = request.get_json()
    k_ = message['K']
    app.logger.error(k_)
    # genera los balaneacdores vacios
    init_data = init_workres_array(workers)
    data_clus = read_CSV(message['name'])
    # numero de anos
    type_balance_str = type_blane_cond(data_balance)
    list_balance = data_clus[type_balance_str].unique()
    # Balanceador Round Robin
    if (type_balance=='RR'):
        init_data = RaoundRobin(init_data,list_balance,workers)
    elif (type_balance=='PS'):
        init_data = PseudoRandom(init_data,list_balance,workers)
    elif (type_balance=='TC'):
        init_data = TwoChoices(init_data,list_balance,workers)
    else:
        init_data = RaoundRobin(init_data,list_balance,workers)
    
    # Calculo de las ip
    peticiones = []
    id=0
    for x in range(workers):
        if (len(init_data[x])>0):
            concac=[]
            for val in init_data[x]:
                concac.append(data_clus[data_clus[type_balance_str]==val])
            data_fin = pd.concat(concac)
            name = str(port)+str(id)+"_LD="+type_balance+"_DLB="+data_balance
            data_fin.to_csv("./data/"+name+".csv")
            data = {"K": k_,
                "name": name}
            url = "http://"+ip+":"+str(port)+str(id)+"/recibir"
            aux = threading.Thread(target=enviar_datos,args=(url,data))
            peticiones.append(aux)
            id+=1
    
    for hilo in peticiones:
        hilo.start()
    
    fin = time.time()
    app.logger.error(name+" = "+str(fin-inicio))
    return jsonify({'hola':'si lego al balance data'})
    
# Prueba
@app.route('/Prueba')
def prueba():
    app.logger.error('Si llegooooooo al balanceo')
    return jsonify({'hola':"SI"})


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)