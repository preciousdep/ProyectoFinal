from enfermedad import Enfermedad
# aqui se usan atributos de: enfermo, contador, tiempo_infectado

class Persona:
    def __init__(self,identidad, nombre,apellido):
        self.__id = identidad
        self.__nombre = nombre
        self.__apellido = apellido
        self.__contagiado = False
        self.__estado_sir = 0
        # 0  significa susceptible, 1 significa infectado y 2 recuperado
        self.__dias_enfermo = 0
        

    ###############################
    def get_comunidad(self):
        return self.__comunidad

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido
    
    def get_contagiado(self):
        return self.__contagiado

    def get_sir(self):
        return self.__estado_sir
    def get_dias_enfermo(self):
        return self.__dias_enfermo

    ######################
    def set_comunidad(self, comunidad):
        self.__comunidad = comunidad

    # valor es un bool
    def set_contagiado(self,valor):
        self.__contagiado = valor
        # se reinicia cada vez que el estado cambia
        self.__dias_enfermo = 0

    def set_sir(self,valor):
        self.__estado_sir = valor

    #################
    def contar_dias_enfermo(self):
        self.__dias_enfermo += 1



    