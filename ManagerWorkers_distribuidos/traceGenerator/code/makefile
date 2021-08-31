CC=gcc -g
FLAGS=-lm

all: generator
generator: generator.c statlib.o genericlib.o
	$(CC)  -o generator generator.c statlib.o genericlib.o $(FLAGS)
	

statlib.o: statlib.c statlib.h
	$(CC) -Wall -c -o statlib.o statlib.c

genericlib.o: genericlib.c genericlib.h
	$(CC) -Wall -c -o genericlib.o genericlib.c


clean: 
	rm *.o 
	rm generator


