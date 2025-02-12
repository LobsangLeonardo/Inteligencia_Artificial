import turtle  
from random import random
import time
# Nombre: Armenta Fuentes Lobsang Leonardo
#Codigo creacion de cubo usando turtle

# La flecha con la que se va a crear el cubo
flecha = turtle.Turtle() 
t = turtle.Screen()            
# Crea el primer cuadrado del cubo
for i in range(4): 
    flecha.forward(100) 
    flecha.left(90)

# Las distancias entre los dos cubos para poder crear el cubo.
flecha.goto(50,50) 
# Crea el otro cuadrado de la parte trasera para la creacion del cubo.
for i in range(5): 
    flecha.forward(100) 
    flecha.left(90) 

# El poder crear las lineas del cubo de forma correcta.
flecha.goto(150,50) 
flecha.goto(100,0) 
flecha.goto(100,100) 
flecha.goto(150,150) 
flecha.goto(50,150) 
flecha.goto(0,100)

time.sleep(2.0)

