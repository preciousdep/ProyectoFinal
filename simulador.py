from persona import Persona
from comunidad import Comunidad
from enfermedad import Enfermedad
import random
import pandas as pd
import numpy as np
#idea: guardar todos los dias en una lista de numpy

    # prueba de simulador para interactuar con las clases
    # draft crea una comunidad para controlar el manejo del contagio
    # y como ocurren (aun no se usan formulas) (se usa pandas)


class Simulador:
    def __init__(self):
        #asegurarse que no hayan familias de mas de 3 personas
        self.comunidad = Comunidad()
        self.enfermedad = Enfermedad("influenza",20,5)
        self.contador_recuperados = 0
        self.contador_muertos = 0
        self.contador_susceptibles = 0 
        self.contador_contagiados = 0
        self.contador_dias = 0
        self.dias_max = self.enfermedad.get_tiempo_infectado()

        self.lista_ciudadanos_comunidad = len(self.comunidad.retorno_lista_comunidad())

        self.comunidad_promedio_fisico = self.comunidad.get_promedio_fisico()
        self.comunidad_probabilidad_estrecho = self.comunidad.get_probabilidad_contacto_estrecho()
        self.probabilidad_enfermo = self.enfermedad.get_probabilidad()
        self.tasa_recuperacion = 0

        ### variables a mostrar
    def get_contagiados(self):
        return self.contador_contagiados
    
    def get_recuperados(self):
        return self.contador_recuperados

    def check_apellido(self,apellido):
        lista_ciudadanos_comunidad = self.comunidad.retorno_lista_comunidad()
        contador_apellido = 0
        for i in lista_ciudadanos_comunidad:
            if i.get_apellido() == apellido:
                contador_apellido += 1
                return False
            elif contador_apellido == 3: 
                return True 
        
    def crea_comunidad(self):
        datos = pd.read_csv('nombres.csv')
        nombres = pd.DataFrame(datos)
        ###############
        miembros_comunidad = random.randint(5000,10000)
        self.comunidad.set_probabilidad_contacto_estrecho()
        self.comunidad.set_promedio_contacto_fisico()
        ident = 0

        for i in range(miembros_comunidad):
            # a corresponde al nombre aleatorio del archivo
            # y p al apellido
            a = random.randint(0,299)
            p = random.randint(0,299)
            # draft infectados iniciales
            infectado = random.randint(0,1000)
            ident += 1
            nombre_ciudadano = nombres.iloc[a,0]
            apellido_ciudadano = nombres.iloc[p,1]
            while self.check_apellido(apellido_ciudadano):
                apellido_ciudadano = nombres.iloc[p+1,1]
            ciudadano = Persona(ident,nombre_ciudadano,apellido_ciudadano)
            # probabilidad del 1% de que una persona sea contagio inicial
            if infectado == 1:
                ciudadano.set_contagiado(True)
                ciudadano.set_sir(1)
            else:
                ciudadano.set_contagiado(False)
                ciudadano.set_sir(0)
            #se agrega a la lista de ciudadanos en la comunidad
            self.lista_ciudadanos_comunidad = len(self.comunidad.retorno_lista_comunidad())
            self.comunidad.agregar_persona_comunidad(ciudadano)
            self.comunidad.add_enfermedad(self.enfermedad)


    def muereono(self):
        for i in self.comunidad.retorno_lista_comunidad():
            if i.get_contagiado() == True :
                a = random.randint(0,100)
                if a <= 2:
                    self.comunidad.persona_muere(i)
                    self.contador_muertos += 1

                
    def contar_contagiados_comunidad(self):
        contagios = 0
        susceptibles = 0
        recuperados = 0
        lista_ciudadanos_comunidad = self.comunidad.retorno_lista_comunidad()
        for i in lista_ciudadanos_comunidad:
            if i.get_sir() == 1:
                contagios += 1
            elif i.get_sir() == 2:
                recuperados += 1
            elif i.get_sir() == 0:
                susceptibles += 1
        # aqui se guardan la cantidad de personas pertenecientes a cada grupo
        # y eso se reinicia a diario
        self.contador_susceptibles = susceptibles
        self.contador_contagiados = contagios
        self.contador_recuperados = recuperados + self.contador_muertos

    def contar_dias_curarse(self):
        # cuenta los dias que lleva la persona
        # si el estado de contagio es True
        for i in self.comunidad.retorno_lista_comunidad():
            if i.get_dias_enfermo() >= self.dias_max and i.get_contagiado():
                i.set_contagiado(False)
                i.set_sir(2)
            if i.get_contagiado() and i.get_dias_enfermo() <= self.dias_max:
                i.contar_dias_enfermo()


    # mecanismo de contagio random draft
    def contagio(self):
        lista = self.comunidad.retorno_lista_comunidad()
        # pasa por la lista y evalua los contactos de cada
        # persona uno por uno
        for i in lista:
            contactos_dia = random.randint(self.comunidad.get_promedio_fisico()-1, 
                            self.comunidad.get_promedio_fisico()+1)
            # si contagiado es ver
            if i.get_contagiado():
                estrecho = self.comunidad.get_probabilidad_contacto_estrecho()
                for j in range(0,contactos_dia):
                    persona_x = random.randint(0,len(lista)-1)
                    decidir_contagio = random.randint(0,100)
                    persona2 = self.comunidad.retorno_lista_comunidad()[persona_x]

                    if persona2.get_sir() == 0:
                        # contacto fisico a estrecho
                        if i.get_apellido() == persona2.get_apellido():
                            valor = self.enfermedad.infeccion()
                            if valor:
                                self.comunidad.retorno_lista_comunidad()[persona_x].set_contagiado(valor)
                                self.comunidad.retorno_lista_comunidad()[persona_x].set_sir(1) 
                        # contacto familiar 100% estrecho
                        elif decidir_contagio < estrecho:
                            valor = self.enfermedad.infeccion()
                            if valor:
                                self.comunidad.retorno_lista_comunidad()[persona_x].set_contagiado(valor)
                                self.comunidad.retorno_lista_comunidad()[persona_x].set_sir(1)
 
    def guardar_en_numpy(self,arreglo):
        lista = np.array(arreglo)
        return lista

    def dias(self):
        self.contador_dias += 1
        print(self.contador_dias)
        self.contar_dias_curarse()
        self.texto_dia = self.contador_dias
