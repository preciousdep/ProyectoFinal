from persona import Persona
from comunidad import Comunidad
from enfermedad import Enfermedad
import random
import pandas as pd
import numpy as np


class Simulador:
    def __init__(self):
        self.comunidad = Comunidad()
        self.enfermedad = Enfermedad(
            # control aleatorio de tasa de contagio/dias recuperacion
            # si se escapa de esos valores, no funciona el modelo
            "influenza", random.randint(10, 16), random.randint(2, 5))
        self.__contador_recuperados = 0
        self.__contador_muertos = 0
        self.__contador_susceptibles = 0
        self.__contador_contagiados = 0
        self.__contador_dias = 0
        self.__dias_max = self.enfermedad.get_tiempo_infectado()
        self.lista_ciudadanos_comunidad = len(
            self.comunidad.retorno_lista_comunidad())

        self.tasa_recuperacion = 0

    # getters y setters
    def get_susceptibles(self):
        return self.__contador_susceptibles

    def get_contagiados(self):
        return self.__contador_contagiados

    def get_recuperados(self):
        return self.__contador_recuperados

    def get_muertos(self):
        return self.__contador_muertos

    def get_contador_dias(self):
        return self.__contador_dias

    def contar_dias(self):
        self.__contador_dias += 1

    def get_dias_max_enfermedad(self):
        return self.__dias_max

    # asegurarse que no hayan familias de mas de 3 personas
    def check_apellido(self, apellido):
        lista_ciudadanos_comunidad = self.comunidad.retorno_lista_comunidad()
        contador_apellido = 0
        for i in lista_ciudadanos_comunidad:
            if i.get_apellido() == apellido:
                contador_apellido += 1
                return False
            elif contador_apellido == 3:
                return True

    # se crea el objeto comunidad y la lista de personas que pertenecen a ella
    # junto con la enfermedad que corresponde
    def crea_comunidad(self):
        datos = pd.read_csv('nombres.csv')
        nombres = pd.DataFrame(datos)
        ###############
        miembros_comunidad = random.randint(6000, 10000)
        # valores aleatorios controlados
        self.comunidad.set_probabilidad_contacto_estrecho()
        self.comunidad.set_promedio_contacto_fisico()
        ident = 0

        for i in range(miembros_comunidad):
            # a corresponde al nombre aleatorio del archivo
            # y p al apellido
            a = random.randint(0, 299)
            p = random.randint(0, 299)
            # draft infectados iniciales
            infectado = random.randint(0, 600)
            ident += 1
            nombre_ciudadano = nombres.iloc[a, 0]
            apellido_ciudadano = nombres.iloc[p, 1]
            while self.check_apellido(apellido_ciudadano):
                apellido_ciudadano = nombres.iloc[p+1, 1]
            ciudadano = Persona(ident, nombre_ciudadano, apellido_ciudadano)
            # probabilidad del 1% de que ciudadano sea contagio inicial
            if infectado == 1:
                ciudadano.set_contagiado(True)
                ciudadano.set_sir(1)
            else:
                ciudadano.set_contagiado(False)
                ciudadano.set_sir(0)
            # se agrega a la lista de ciudadanos en la comunidad
            self.lista_ciudadanos_comunidad = len(
                self.comunidad.retorno_lista_comunidad())
            self.comunidad.agregar_persona_comunidad(ciudadano)
            self.comunidad.add_enfermedad(self.enfermedad)

    # en caso de que la persona muera
    # estando enfermo, se elimina de la lista
    # y se suma a los recuperados por medio de
    # __contador_muertos
    def muereono(self):
        for i in self.comunidad.retorno_lista_comunidad():
            if i.get_contagiado():
                a = random.randint(0, 100)
                if a <= 2:
                    self.comunidad.persona_muere(i)
                    self.__contador_muertos += 1

    # esta funciona para un conteo diario
    # de cada grupo del sir
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
        self.__contador_susceptibles = susceptibles
        self.__contador_contagiados = contagios
        self.__contador_recuperados = recuperados + self.get_muertos()

    def contar_dias_curarse(self):
        # cuenta los dias que lleva la persona
        # si el estado de contagio es True
        for i in self.comunidad.retorno_lista_comunidad():
            if i.get_dias_enfermo() >= self.get_dias_max_enfermedad() and (
             i.get_contagiado()):
                i.set_contagiado(False)
                i.set_sir(2)
            if i.get_contagiado() and i.get_dias_enfermo() <= (
             self.get_dias_max_enfermedad()):
                i.contar_dias_enfermo()

    # mecanismo de contagio aleatorio:
    # la persona interactua con una cantidad aproximada de personas
    # (contactos_dia) y se escogen personas aleatorias con las
    # cuales interactua, de ahi ocurre el contacto
    def contagio(self):
        lista = self.comunidad.retorno_lista_comunidad()
        # pasa por la lista y evalua los posibles contactos de cada
        # persona uno por uno
        for i in self.comunidad.retorno_lista_comunidad():
            contactos_dia = random.randint(
                self.comunidad.get_promedio_fisico()-2,
                self.comunidad.get_promedio_fisico()+2)

            for j in range(0, contactos_dia):
                persona_x = random.randint(0, len(lista)-1)
                persona2 = self.comunidad.retorno_lista_comunidad()[
                    persona_x]
            # aqui se evalua si el contacto es estrecho, de ahi llama
            # a la funcion que toma la tasa de contagio (en enfermedad)
            # para ver si se contagia o no la otra persona
                estrecho = self.comunidad.get_probabilidad_contacto_estrecho()
                decidir_estrecho = random.randint(0, 100)
            # si la persona 1 esta contagiada
                if i.get_sir() == 1:
                    if persona2.get_sir() == 0:
                        # contacto fisico a estrecho por ser familia 100%
                        if i.get_apellido() == persona2.get_apellido():
                            valor = self.enfermedad.infeccion()
                            if valor:
                                self.comunidad.retorno_lista_comunidad()[
                                    persona_x].set_contagiado(valor)
                                self.comunidad.retorno_lista_comunidad()[
                                    persona_x].set_sir(1)
                        # esto si el contacto fisico es estrecho o no
                        elif decidir_estrecho < estrecho:
                            valor = self.enfermedad.infeccion()
                            if valor:
                                self.comunidad.retorno_lista_comunidad()[
                                    persona_x].set_contagiado(valor)
                                self.comunidad.retorno_lista_comunidad()[
                                    persona_x].set_sir(1)
                # contagio bilateral
                elif persona2.get_sir() == 1:
                    if i.get_sir() == 0:
                        if i.get_apellido() == persona2.get_apellido():
                            valor = self.enfermedad.infeccion()
                            if valor:
                                i.set_contagiado(valor)
                                i.set_sir(1)
                            # esto si el contacto fisico es estrecho o no
                        elif decidir_estrecho < estrecho:
                            valor = self.enfermedad.infeccion()
                            if valor:
                                i.set_contagiado(valor)
                                i.set_sir(1)

    # se guarda la lista de 'arreglo' para luego
    # almacenarla en un arreglo numpy y asi poder hacer
    # el plot
    def guardar_en_numpy(self, arreglo):
        lista = np.array(arreglo)
        return lista
