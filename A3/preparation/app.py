# Librerias
import pandas as pd
import numpy as np
from datetime import datetime
# Librerias Flask
from flask import Flask, request
from flask import render_template
from flask import Response
import json
import requests
import sys

arg = sys.argv
ip_port = arg[1]
# Inicicalizar Flask
# from flask import Flask
app = Flask(__name__)
app.debug = True

def Preprocesing(data_cl):
  # Lectura de archivos
  data_clima =  data_cl
  print('Lectura...Listo')

  # ELiminacion de columnas nulas y remplazo de valores Null a Nan
  data_clima_clus = data_clima.copy()
  data_clima_clus = data_clima_clus.drop(['Codigo','Hidroregion','Topoforma','Differential_max','Differential_min','Humedad', 'Presion_barometrica', 'Precipitacion', 'Radiacion_solar', 'Etiqueta_clase'], axis=1)
  data_clima_clus = data_clima_clus.replace('Null',None)
  data_clima_clus = data_clima_clus.replace('NaN',None)
  print('Eliminacion...Listo')

  # Relleno de valores faltantes
  data_clima_clus = data_clima_clus.fillna({'Temp_mean_emas': -99.0,})
  for x in range (len(data_clima_clus)):
    if ((data_clima_clus.loc[x,'Temp_max_emas'] == -99.0) or (np.isnan(data_clima_clus.loc[x,'Temp_max_emas'])) or (data_clima_clus.loc[x,'Temp_max_emas'] > data_clima_clus.loc[x,'Temp_max_merra']+5) or (data_clima_clus.loc[x,'Temp_max_emas'] < data_clima_clus.loc[x,'Temp_max_merra']-5)):
      data_clima_clus.loc[x,'Temp_max_emas'] = data_clima_clus.loc[x,'Temp_max_merra']
    if ((data_clima_clus.loc[x,'Temp_min_emas'] == -99.0) or (np.isnan(data_clima_clus.loc[x,'Temp_min_emas'])) or (data_clima_clus.loc[x,'Temp_min_emas'] > data_clima_clus.loc[x,'Temp_min_merra']+5) or (data_clima_clus.loc[x,'Temp_min_emas'] < data_clima_clus.loc[x,'Temp_min_merra']-5)):
      data_clima_clus.loc[x,'Temp_min_emas'] = data_clima_clus.loc[x,'Temp_min_merra']
    if ((data_clima_clus.loc[x,'Temp_mean_emas'] == -99.0)):
      data_clima_clus.loc[x,'Temp_mean_emas'] = data_clima_clus.loc[x,'Temp_mean_merra']
  data_clima_clus.Temp_mean_emas = data_clima_clus.Temp_mean_emas.astype(np.float64)
  print('Relleno...Listo')

  # Separacion de fecha
  years=[]
  months=[]
  days=[]
  all = data_clima_clus.iloc[:,1]
  for x in all:
    date_time_obj = datetime.strptime(x, '%d/%M/%Y')
    years.append(date_time_obj.strftime("%Y"))
    months.append(date_time_obj.strftime("%M"))
    days.append(str(date_time_obj.strftime("%d")))
  data_clima_clus = data_clima_clus.drop(columns='Fecha')
  data_clima_clus.insert(1,"Ano",years,True)
  data_clima_clus.insert(2,"Mes",months,True)
  data_clima_clus.insert(3,"Dia",days,True)
  print('Fecha...Listo')

  name = 'DataPreproces'
  # Create csv
  data_clima_clus.to_csv("./data/"+name+".csv")
  return data_clima_clus, name

def read_CSV(name):
    return pd.read_csv("./data/"+name)
  
    

@app.route('/pre', methods = ['POST'])
def pre():
    message = request.get_json()
    data_ = read_CSV(message['name'])
    data_2,name = Preprocesing(data_)
    
    app.logger.error("FLAG")
    
    url = "http://"+str(ip_port)+"/recibir"
    headers = {'PRIVATE-TOKEN': '<your_access_token>', 'Content-Type':'application/json'}
    app.logger.error(url)
    data = {"K": message['K'],
            "name":name}
    
    requests.post(url, data=json.dumps(data), headers=headers)
    return Response(status=200)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)