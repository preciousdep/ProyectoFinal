from enfermedad import Enfermedad
# aqui se usan atributos de: enfermo, contador, tiempo_infectado

class Persona():
    def __init__(self,identidad, nombre,apellido):
        self.__id = identidad
        self.__nombre = nombre
        self.__apellido = apellido
        self.__contagiado = False
        
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
    
    def get_contagiado(self):
        return self.__contagiado

    ######################
    def set_comunidad(self, comunidad):
        self.__comunidad = comunidad

    # valor es un bool
    def set_contagiado(self,valor):
        self.__contagiado = valor


    