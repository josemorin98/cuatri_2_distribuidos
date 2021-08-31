import requests
import json
import pandas as pd
import threading
import time

def read_CSV(name):
    return pd.read_csv(name)
def read_CSV2(name,ini,fin):
    return pd.read_csv(name,skiprows=ini,nrows=fin)
# 
#9 data_clima = pd.read_csv("/home/morin/Escritorio/A3/Diferencial_EMAS-MERRA(1).csv")
# data_clima = pd.read_csv("/home/morin/Escritorio/A3/DataPreproces.csv")
# data_clima = pd.read_csv("/home/morin/Escritorio/A3/Diferencial_EMAS-MERRA(1) (copia).csv")
# data_clima = pd.read_csv("/home/morin/Escritorio/A3/DataPreproces.csv")
# data_H = data_clima.columns.values.tolist()
# data_V = data_clima.values.tolist()
    
    # url = "http://0.0.0.0:5560/pre"
    # url = "http://0.0.0.0:5570/dividir_K"

headers = {'PRIVATE-TOKEN': '<your_access_token>', 'Content-Type':'application/json'}
# data = {"K": [2],
#             "Dts": data_V,
#             "Col": data_H}
# def prueba(x):
#     url = "http://0.0.0.0:557"+str(x+1)+"/recibir"
#     data = {"K": [(x+1)],
#             "Dts": data_V,
#             "Col": data_H}
#     requests.post(url, data=json.dumps(data), headers=headers)

# def enviar_datos(url):
#     requests.get("http://"+url)
    
# def prueba_hilos():
#     workers=2
#     for x in range(workers):
#         aux = threading.Thread(target=prueba,args=(x,))
#         aux.start()
        
def prueba_n():
    url = "http://192.168.0.12:5602/preprocer"
    data = {"K": [2,3,4],
            "name":'DataPreproces'}
    
    x = requests.post(url, data=json.dumps(data), headers=headers)
    print(x.status_code)

# data = read_CSV("./Diferencial_EMAS-MERRA.csv")
# totaal = int(len(data)/5)
# p = 8
# n = 12
# print(data.loc[p:n,])



# inicio = time.time()
prueba_n()
# fin = time.time()
# print(str(fin-inicio))
