import random

class Enfermedad:
    def __init__(self):
        self.__probabilidad = 0
        self.__tiempo_infectado = 0
        self.__enfermo = False
        self.__contador = 0

    def get_probabilidad(self):
        return self.__probabilidad

    def set_probabilidad(self, probabilidad):
        self.__probabilidad = random.random(0.0,1.0)

    def get_tiempo_infectado(self):
        return self.__tiempo_infectado

    def set_tiempo_infectado(self):
        self.__tiempo_infectado = random.randint(1,30)

    def get_enfermo(self):
        return self.__enfermo

    def set_enfermo(self, enfermo):
        self.__enfermo = enfermo

    def get_contador(self):
        return self.__contador
    
    # se va a llamar a la funcion por cada paso para contar
    # los dias de enfermo
        
    def contador_enfermo(self):
        self.__contador += 1