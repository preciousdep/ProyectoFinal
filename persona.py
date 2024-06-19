from enfermedad import Enfermedad
# aqui se usan atributos de: enfermo, contador, tiempo_infectado

class Persona():
    def __init__(self):
        self.__comunidad = int
        self.__id = int
        self.__nombre = ''
        self.__apellido = ''
        self.__enfermedad = []
        
    # metodos get y set para cada atributo. se van a editar conforme lo necesario

    ###############################
    def get_comunidad(self):
        return self.__comunidad

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_enfermedad(self):
        return self.__enfermedad

    ######################
    def set_comunidad(self, comunidad):
        self.__comunidad = comunidad

    def set_id(self, ident):
        self.__id = ident

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_apellido(self, apellido):
        self.__apellido = apellido

    def set_enfermedad(self, enfermedad):
        self.__enfermedad = enfermedad


    