# Libreria para realizar codigos
import os
import sys
import pandas as pd
import subprocess
import  csv

arg = sys.argv
# argumentos a recibir
# ./generator <samples > <size> <inter_arrival> <read_ratio> <sas_size> <distribution> <mean> <stdev> <Concurrency> > traza1.txt
samples= arg[1]
inter_arrival= arg[2]
#distribution: 1:Uniforme, 2:Poisson, y 3:Normal
distribution= arg[3]
t_service = arg[4]
meanD = 0
stdv = 0
tam=500
if(distribution=='3'):
    meanD = 10
    stdv = 5
elif(distribution=='2'):
    tam=500
csvrows = []
aux = []
    

# Creamos el archivo
with open('Resultados.csv', 'w') as csvfile:
    fieldnames = ['traza','meanInter', 'Num_Peticiones','w','r', 'Average_delay_in_queue',  'Average_number_in_queue',  'Server_Utilization',  'Time_simulation_ended']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    
    for rep in range(32):
        print("\nTraza - " + str(rep))
        print('Generador')
        # ejecutar el contenedor para generar la traza
        # print('docker run --rm -ti --name generator1 generator:traza ./generator ' +str(samples)+ ' 500 '+str(inter_arrival)+' 80 549093 '+ str(distribution)+' '+ str(meanD) +' '+str(stdv)+' 1 > ./traza.csv')
        os.system('docker run --rm -ti --name generator1 generator:traza ./generator ' +str(samples)+ ' '+str(tam)+' '+str(inter_arrival)+' 80 549093 '+ str(distribution)+' '+ str(meanD) +' '+str(stdv)+' 1 > ./traceGenerator/traza.csv')

        traza = pd.read_csv('./traceGenerator/traza.csv', delimiter=' ', header=None)
        suma = 0
        for x in range(len(traza.iloc[:,0])-1):
            suma = suma + traza[0][(x+1)] -traza[0][x]
            
        meanInter=(suma/(len(traza.iloc[:,0])-1))/1000
        # Resultados
        # media del interarribo en segundos
        # cantidad de peticiones 549093

        print("meanInter = " + str(meanInter) + "Num Peticiones = "+ str(len(traza.iloc[:,0]))) 
        # ejecutar el contenedor para el simulador
        print('Simulador')
        # print('docker run --rm -ti --name single1 simulator:singles ./single '+str(meanInter)+' 1 '+str(len(traza.iloc[:,0])))
        os.system('docker run --rm -ti --name single1 simulator:singles ./single '+str(meanInter)+' '+ str(t_service)+' '+str(len(traza.iloc[:,0]))+'> ./QueueSimulator/simulator.csv')
        single = pd.read_csv("./QueueSimulator/simulator.csv", delimiter=',')
         
        # Resultados
        print(single)
        
        if(len(single.iloc[0])>1):
            aux={'traza': (rep+1),
                'meanInter': meanInter,
                'Num_Peticiones': len(traza.iloc[:,0]),
                'w': traza.iloc[:,2].value_counts()[0],
                'r': traza.iloc[:,2].value_counts()[1],
                'Average_delay_in_queue': single['Average_delay_in_queue'][0],  
                'Average_number_in_queue': single['Average_number_in_queue'][0],
                'Server_Utilization': single['Server_Utilization'][0],
                'Time_simulation_ended': single['Time_simulation_ended'][0]
                }
        else:
            aux={'traza': (rep+1),
                'meanInter': meanInter,
                'Num_Peticiones': len(traza.iloc[:,0]),
                'w': traza.iloc[:,2].value_counts()[0],
                'r': traza.iloc[:,2].value_counts()[1],
                'Average_delay_in_queue': 'Overflow',  
                'Average_number_in_queue': 'Overflow',
                'Server_Utilization': 'Overflow',
                'Time_simulation_ended': single['Overflow_of_the_array_time_arrival_at_time'][0]
                }

        csvrows.append(aux)
    
    writer.writerows(csvrows)

print("\nPruebas Completas")
print('docker run --rm -ti --name generator1 generator:traza ./generator ' +str(samples)+ ' '+str(tam)+' '+str(inter_arrival)+' 80 549093 '+ str(distribution)+' '+ str(meanD) +' '+str(stdv)+' 1 > ./traceGenerator/traza.csv')
print('docker run --rm -ti --name single1 simulator:singles ./single '+str(meanInter)+' '+ str(t_service)+' '+str(len(traza.iloc[:,0]))+'> ./QueueSimulator/simulator.csv')