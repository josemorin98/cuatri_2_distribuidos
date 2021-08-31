from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import pandas as pd
from flask import Flask, request
from flask import render_template
from flask import Response
from flask import jsonify
import json
import sys
import requests
import time

arg = sys.argv
ip= arg[1]
port = int(arg[2])
type_cluster=arg[3]

app = Flask(__name__)
app.debug = True

def K_means(k,data_clima):
    X_clima = data_clima.iloc[:,[7,8,9,10]]
    kmeans = KMeans(n_clusters=k).fit(X_clima)
    k_labels = kmeans.predict(X_clima)
    return k_labels


def MixtureModel(k,data_clima):
    X_clima = data_clima.iloc[:,[7,8,9,10]]
    app.logger.error('FLAG2')
    modelo_gmm = GaussianMixture(
                n_components    = k,
                covariance_type = 'full',
                random_state    = 123)
    modelo_gmm.fit(X_clima)
    k_labels = modelo_gmm.predict(X_clima)
    app.logger.error('FLAG3')
    return k_labels
    
def read_CSV(name):
    return pd.read_csv("./data/"+name+".csv")

@app.route('/recibir',methods = ['POST'])
def clustering():
    inicio = time.time()
    message = request.get_json()
    # recibir K
    k_ = message['K']
    name = message['name']
    # encabezado de la peticion
    headers = {'PRIVATE-TOKEN': '<your_access_token>', 'Content-Type':'application/json'}
    url = "http://"+ip+":"+str(port)+"/recibir"    
    data_clima = read_CSV(name)
    for k in k_:        
        # KMEANS
        if (type_cluster=="Kmeans"):
            # llamado del clustering
            k_labels = K_means(k,data_clima)
            cluster="Kmeans"
        elif (type_cluster=="GM"):
            k_labels = MixtureModel(k,data_clima)
            cluster="GaussianMixture"
        else:
            k_labels = K_means(k,data_clima)
            cluster="Kmeans"
        # data send
        
        data_clima["clase"]=k_labels
        data_clima.to_csv("./data/results/Clus_"+name+"_DataClust_K="+str(k)+"_"+str(cluster)+".csv")
        
        data = {"K": k,
            "labels": k_labels,
            "name": name+"_K="+str(k)+"_"+str(cluster)}
        
    fin = time.time()
    app.logger.error(str(cluster)+" = "+str(fin-inicio))
        # requests.post(url, data=json.dumps(data), headers=headers)
    return jsonify({'hola':'si lLego al clustering'})


# Prueba
@app.route('/Prueba')
def prueba():
    app.logger.error('Si llegooooooo al balanceo')
    return jsonify({'hola':"SI"})


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)