# Genera una imagen de contenedor que contiene los programas C del generador de trazas
# Creador: José Carlos Morín Garcíoa
# Mail: jose.morin@cinvestav.mx
# Se indica la imagen base
FROM ubuntu:latest
# Ejecuta actualización y descarga librerias necesarias
RUN apt-get update && apt-get install --assume-yes apt-utils
RUN apt-get install build-essential -y
RUN apt-get install make -y
# Se copia el archivo de configuración
COPY code /app/
# Se copia la aplicación del trabajador a la imagen
WORKDIR /app/
RUN make
RUN ["chmod", "+x", "/app/single"]

#docker build -t simulator:singles .
