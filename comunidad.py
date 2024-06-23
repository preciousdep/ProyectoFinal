from enfermedad import Enfermedad
from persona import Persona
import random

class Comunidad:
    def __init__(self):
        self.ciudadanos = []
        self.num_ciudadanos = int
        self.num_contagiados = int
        self.__enfermedades = []
        self.__promedio_fisico = int
        self.__probabilidad_contacto_estrecho = float

    def add_enfermedad(self, enfermedad):
        if isinstance(enfermedad, Enfermedad):
            self.__enfermedades.append(enfermedad)
        else:
            pass

    def get_enfermedad(self):
        return self.__enfermedades

    def get_promedio_fisico(self):
        return self.__promedio_fisico

    def get_probabilidad_contacto_fisico(self):
        return self.__probabilidad_contacto_fisico

    def set_num_ciudadanos(self,numero):
        self.num_ciudadanos = numero

    def set_num_contagiados(self,numero):
        self.num_contagiados = numero

    # draft de funcionamiento de contacto estrecho con familia y apellidos iguales

    def contacto_estrecho(self, persona1, persona2,enfermedad):
        if isinstance(persona1, Persona) and isinstance(persona2,Persona):
            if persona1.get_apellido() == persona2.get_apellido():
                return enfermedad.infeccion()
            else:
                pass

    def set_promedio_contacto_fisico(self):
        self.__promedio_fisico = random.randint()
            
    def agregar_persona_comunidad(self,persona):
        if isinstance(persona,Persona):
            self.ciudadanos.append(persona)

    def retorno_lista_comunidad(self):
        return self.ciudadanos