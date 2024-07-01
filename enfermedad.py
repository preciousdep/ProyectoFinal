import random

class Enfermedad:
    def __init__(self,nombre,probabilidad,tiempo):
        self.__nombreenfermedad = nombre
        #en entero de 0 a 100 para poder trabajarlo
        self.__probabilidad = probabilidad
        self.__tiempo_infectado = tiempo
        self.__contador = 0

    def get_nombre_enfermedad(self):
        return self.__nombreenfermedad

    def get_probabilidad(self):
        return self.__probabilidad

    def get_tiempo_infectado(self):
        return self.__tiempo_infectado

    def get_contador(self):
        return self.__contador
    
    # se va a llamar a la funcion por cada paso para contar
    # los dias de enfermo
        
    def contador_enfermo(self):
        self.__contador += 1

    # draft de como se infecta una persona devuelve un bool que sera
    # asignado al estado de contagiado de una persona
    # considerar: recupera, inmune. muere, eliminar?? vacuna, posibilidad 100%

    def infeccion(self):
        #intervalo
        prob = self.get_probabilidad()
        x = random.randint(0,100)
        if x <= prob:
            return True
        else:
            return False

