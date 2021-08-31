Antes de comenzar es necesario tener instaladas las siguientes librerías:
make
gcc

GENERADOR DE TRAZAS

generator.c es una aplicación que permite generar trazas de un tamaño aleatorio establecido por el usuario. Estas trazas, contienen una serie de tuplas con operaciones de lectura y escritura de archivos. Para cada una de las tuplas, se especifica un interarrivo, el tipo de operación a realizar (lectura o escritura), el tamaño del fichero y la localización del mismo.

Para compilar generator utiliza el siguiente comando:
make clean ------> sirve para borrar los ejecutables antiguos
make  --------> genera el ejecutable


Ejecutar generator:

./generator <samples > <size> <inter_arrival> <read_ratio> <sas_size> <distribution> <mean> <stdev> <Concurrency> > traza1.txt

Ejemplo:
./generator 100 500 1 80 549093 1 0 0 1

Donde:
samples: es el número de muestras que se desea obtener (a partir de 100 muestras)
size: tamaño de la porción
inter_arrival: es el tiempo de interarrivo promedio de las peticiones
read_ratio: el raito de lectura (utilizando la proporcion de pareto)
sas_size: el tamaño promedio de los paquetes/archivos en las peticiones
distribution: 1:Uniforme, 2:Poisson, y 3:Normal
mean: la media utilizada para la distribución normal
stdev: desviación estándar utilizada para la distribución normal
Concurrency: la concurrencia de peticiones (se recomienda utilizarlo solo en 1 o 2 para el valor a asignar)


SIMULADOR DE COLAS
Este aplicativo permite calcular la media del tiempo de las operaciones en cola, la media del número de archivos en cola, la utilización del servidor y el tiempo final de simulación.

Para compilar single utiliza el siguiente comando:
make clean ------> sirve para borrar los ejecutables antiguos
make  --------> genera el ejecutable

Ejecutar single:

./single mean_interarrival mean_service num_delays_required

Ejemplo:
./single 6.17  1  242

Donde:
mean_interarrival: es el tiempo en el que llega cada petición realizada
mean_service: es el tiempo promedio de servicio
num_delays_required: son los retardos que habran entre las peticiones realizadas




