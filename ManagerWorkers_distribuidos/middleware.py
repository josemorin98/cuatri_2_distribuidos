# Libreria para realizar codigos
import os
import sys
import pandas as pd
import subprocess
import  csv
import numpy as np
import dispacher
import socket
import json

def init_workres_array(workers):
    pet_in = []
    for i in range(workers):
        pet_in.append([])
    return pet_in

arg = sys.argv
# argumentos a recibir
# ./generator <samples > <size> <inter_arrival> <read_ratio> <sas_size> <distribution> <mean> <stdev> <Concurrency> > traza1.txt
samples= arg[1]
inter_arrival= arg[2]
#distribution: 1:Uniforme, 2:Poisson, y 3:Normal
balanceo = arg[3]

t_service = arg[4]
meanD = 0
stdv = 0
tam=500
csvrows = []


workers = int(arg[5])



print(dispacher.display_workers(workers))
# ejecutar el contenedor para generar la traza      
os.system('docker run --rm --name generator1 generatordos:trazados ./generator ' +str(samples)+ ' '+str(tam)+' '+str(inter_arrival)+' 80 549093 1 '+ str(meanD) +' '+str(stdv)+' 1 > ./traceGenerator/traza.csv')
traza = pd.read_csv('./traceGenerator/traza.csv', delimiter=' ', header=None)
print("\nTraza - Generada")
meanInter = []
sumat=0

if(balanceo == '0'):    
    print("\nRound Robin")
    pet_in_workers_RR = init_workres_array(workers)
    pet_in_workers_RR = dispacher.RaoundRobin(pet_in_workers_RR, traza, workers)
    for i in range(workers):
        print(len(pet_in_workers_RR[i]))
        for x in range(len(pet_in_workers_RR[i])-1):
        #     print(pet_in_workers_RR[i])
            sumat = sumat + float(pet_in_workers_RR[i][(x+1)]) -float(pet_in_workers_RR[i][x])
        meanInter.append((sumat/(len(pet_in_workers_RR[i])-1))/1000)
        sumat=0
    requests = []
    for pet in range(workers):
        json_request = json.loads(dispacher.sokcet_client(meanInter[pet], t_service, len(pet_in_workers_RR[pet]), 51000+pet))
        aux={'meanInter': meanInter[pet],
                'Num_Peticiones': len(pet_in_workers_RR[pet]),
                'Average_delay_in_queue': json_request['Average_delay_in_queue'],  
                'Average_number_in_queue': json_request['Average_number_in_queue'],
                'Server_Utilization': json_request['Server_Utilization'],
                'Time_simulation_ended': json_request['Time_simulation_ended']
                }
        requests.append(aux)
        # print(requests[pet])
        
elif(balanceo == '1'):
    print("\nPseudo Random")
    pet_in_workers_PR = init_workres_array(workers)
    pet_in_workers_PR = dispacher.PseudoRandom(pet_in_workers_PR, traza, workers)
    for i in range(workers):
        print(len(pet_in_workers_PR[i]))
        for x in range(len(pet_in_workers_PR[i])-1):
            sumat = sumat + float(pet_in_workers_PR[i][(x+1)]) -float(pet_in_workers_PR[i][x])
        meanInter.append((sumat/(len(pet_in_workers_PR[i])-1))/1000)
        sumat=0
    requests = []
    for pet in range(workers):
        json_request = json.loads(dispacher.sokcet_client(meanInter[pet], t_service, len(pet_in_workers_PR[pet]), 51000+pet))
        aux={'meanInter': meanInter[pet],
                'Num_Peticiones': len(pet_in_workers_PR[pet]),
                'Average_delay_in_queue': json_request['Average_delay_in_queue'],  
                'Average_number_in_queue': json_request['Average_number_in_queue'],
                'Server_Utilization': json_request['Server_Utilization'],
                'Time_simulation_ended': json_request['Time_simulation_ended']
                }
        requests.append(aux)
        # print(requests[pet])
        
elif(balanceo == '2'):
    print("\nTwo Choices")
    pet_in_workers_TC = init_workres_array(workers)
    pet_in_workers_TC = dispacher.TwoChoices(pet_in_workers_TC, traza, workers)
    for i in range(workers):
        print(len(pet_in_workers_TC[i]))
        for x in range(len(pet_in_workers_TC[i])-1):
            sumat = sumat + float(pet_in_workers_TC[i][(x+1)]) -float(pet_in_workers_TC[i][x])
        meanInter.append((sumat/(len(pet_in_workers_TC[i])-1))/1000)
        sumat=0
    requests = []
    for pet in range(workers):
        json_request = json.loads(dispacher.sokcet_client(meanInter[pet], t_service, len(pet_in_workers_TC[pet]), 51000+pet))
        aux={'meanInter': meanInter[pet],
                'Num_Peticiones': len(pet_in_workers_TC[pet]),
                'Average_delay_in_queue': json_request['Average_delay_in_queue'],  
                'Average_number_in_queue': json_request['Average_number_in_queue'],
                'Server_Utilization': json_request['Server_Utilization'],
                'Time_simulation_ended': json_request['Time_simulation_ended']
                }
        requests.append(aux)
        # print(requests[pet])
        
with open('Resultados_'+str(samples)+'_'+str(workers)+'_'+str(balanceo)+'.csv', 'w') as csvfile:
    fieldnames = ['meanInter', 'Num_Peticiones','Average_delay_in_queue',  'Average_number_in_queue',  'Server_Utilization',  'Time_simulation_ended']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(requests)

# print(requests)
print(dispacher.drop_workers(workers))