from persona import Persona
from comunidad import Comunidad
from enfermedad import Enfermedad
import random
import pandas as pd
import numpy as np #probando

    # prueba de simulador para interactuar con las clases
    # draft crea una comunidad para controlar el manejo del contagio
    # y como ocurren (aun no se usan formulas) (se usa pandas)


#asegurarse que no hayan familias de mas de 3 personas
def check_apellido(comunidad,apellido):
    lista_ciudadanos_comunidad = comunidad.retorno_lista_comunidad()
    contador_apellido = 0
    for i in lista_ciudadanos_comunidad:
        if i.get_apellido() == apellido:
            contador_apellido += 1
            return False
        elif contador_apellido == 3: 
            return True 
    
def crea_comunidad():
    datos = pd.read_csv('nombres.csv')
    nombres = pd.DataFrame(datos)
    comunidad = Comunidad()
    miembros_comunidad = random.randint(1000,10000)
    comunidad.set_probabilidad_contacto_estrecho()
    comunidad.set_promedio_contacto_fisico()

    ident = 0
    print(f"""Promedio de contacto fisico de la comunidad: {comunidad.get_promedio_fisico()} personas \n
Probabilidad de que un contacto fisico no familiar sea estrecho: {comunidad.get_probabilidad_contacto_estrecho()}% """)

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
        while check_apellido(comunidad,apellido_ciudadano):
            apellido_ciudadano = nombres.iloc[p+1,1]
        ciudadano = Persona(ident,nombre_ciudadano,apellido_ciudadano)
        # probabilidad del 1% de que una persona sea contagio inicial
        if infectado == 1:
            ciudadano.set_contagiado(True)
            ciudadano.set_sir(1)
        else:
            ciudadano.set_contagiado(False)
        #se agrega a la lista de ciudadanos en la comunidad
        comunidad.agregar_persona_comunidad(ciudadano)
    return comunidad

def crear_enfermedad():
        enfermedad = Enfermedad("influenza",20,15)
        return enfermedad
            
def contar_contagiados_comunidad(comunidad):
    contador_contagiados = 0
    lista_ciudadanos_comunidad = comunidad.retorno_lista_comunidad()
    for i in lista_ciudadanos_comunidad:
        if i.get_contagiado():
            contador_contagiados += 1
            print(i.get_id(), i.get_nombre(), i.get_apellido(), "presenta la enfermedad")

    print(contador_contagiados, "contagios iniciales de", len(lista_ciudadanos_comunidad))

def contar_dias_curarse(comunidad,contador):
    lista_ciudadanos_comunidad = comunidad.retorno_lista_comunidad()
    enfermedad = comunidad.get_enfermedad()
    dias_max = enfermedad.get_tiempo_infectado()
    contador_recuperados = 0
    for i in lista_ciudadanos_comunidad:
        if i.get_contagiado() == True:
            i.contar_dias_enfermo()
        
        if i.get_dias_enfermo() == dias_max:
            vive_o_muere = random.randint(0,100)
            if vive_o_muere >= 20:
                i.set_contagiado(False)
                i.set_sir(2)
                print(f"{i.get_nombre()} {i.get_apellido()} se ha recuperado")
            else:
                print(f"{i.get_nombre()} {i.get_apellido()} ha muerto...")
                i.set_contagiado(False)
                
                #draft, falta el mecanismo de muerte
                #update: que ocurra dentro de la enfermedad??

        if i.get_sir() == 2:
            contador_recuperados += 1

#def contagio(comunidad):

#def guarda_en_archivo(): #overwrite o agregar linea?


def dias():
    pasandias = True
    enfermedad = crear_enfermedad()
    comunidad = crea_comunidad()
    comunidad.add_enfermedad(enfermedad)
    contador_dias = 0
    while pasandias:
        contador_dias += 1
        contar_contagiados_comunidad(comunidad)
        contar_dias_curarse(comunidad,contador_dias)
        print(f"Dia {contador_dias}")
        input()

dias()
    # falta revisar numpy