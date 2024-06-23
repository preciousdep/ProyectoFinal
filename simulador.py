from persona import Persona
from comunidad import Comunidad
from enfermedad import Enfermedad
import random
import pandas as pd


    # prueba de simulador para interactuar con las clases
    # draft crea una comunidad para controlar el manejo del contagio
    # y como ocurren (aun no se usan formulas) (se usa pandas)

def crea_comunidad():
    datos = pd.read_csv('nombres.csv')
    nombres = pd.DataFrame(datos)
    comunidad = Comunidad()
    miembros_comunidad = random.randint(100,8000)
    ident = 0

    for i in range(miembros_comunidad):
        # a corresponde al nombre aleatorio del archivo
        # y p al apellido
        a = random.randint(0,299)
        p = random.randint(0,299)
        # draft infectados iniciales
        infectado = random.randint(0,100)
        ident += 1
        nombre_ciudadano = nombres.iloc[a,0]
        apellido_ciudadano = nombres.iloc[p,1]
        ciudadano = Persona(ident,nombre_ciudadano,apellido_ciudadano)
        # probabilidad del 1% de que una persona sea contagio inicial
        if infectado == 1:
            ciudadano.set_contagiado(True)
        else:
            ciudadano.set_contagiado(False)
        #se agrega a la lista de ciudadanos en la comunidad
        comunidad.agregar_persona_comunidad(ciudadano)
    contar_contagiados_comunidad(comunidad)
            

def contar_contagiados_comunidad(comunidad):
    contador_contagiados = 0
    lista_ciudadanos_comunidad = comunidad.retorno_lista_comunidad()
    for i in lista_ciudadanos_comunidad:
        if i.get_contagiado():
            contador_contagiados += 1

    print(contador_contagiados, "contagios iniciales de", len(lista_ciudadanos_comunidad))

crea_comunidad()