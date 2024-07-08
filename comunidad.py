from enfermedad import Enfermedad
from persona import Persona
import random


class Comunidad:
    def __init__(self):
        self.ciudadanos = []
        self.__enfermedad = None
        # personas que conoce en promedio
        self.__promedio_fisico = 0
        self.__probabilidad_contacto_estrecho = 0

    # caso de que hayan varias enfermedades. sino, se
    # trata con la enfermedad unica
    def add_enfermedad(self, enfermedad):
        if isinstance(enfermedad, Enfermedad):
            self.__enfermedad = enfermedad
        else:
            pass

    def get_enfermedad(self):
        return self.__enfermedad

    def get_promedio_fisico(self):
        return self.__promedio_fisico

    def get_probabilidad_contacto_estrecho(self):
        return self.__probabilidad_contacto_estrecho

    # draft de funcionamiento de contacto estrecho con familia

    def contacto_estrecho(self, persona1, persona2, enfermedad):
        if isinstance(persona1, Persona) and isinstance(persona2, Persona):
            if persona1.get_apellido() == persona2.get_apellido():
                # probabilidad mas alta al ser familia
                return enfermedad.infeccion()
            else:
                # aqui los de promedio de conocidos
                pass

# se refiere al promedio de 'conocidos' o 'amigos'
# que tiene una persona. se considerara un
# +- 2 personas para ese caso
    def set_promedio_contacto_fisico(self):
        self.__promedio_fisico = random.randint(3, 6)

# que un contacto fisico cualquiera con un conocido o amigo
# sea estrecho y posibilita un contagio. de lo contrario,
# la posibilidad de un contagio sera menor o nula (draft)
    def set_probabilidad_contacto_estrecho(self):
        self.__probabilidad_contacto_estrecho = random.randint(10, 60)

    def agregar_persona_comunidad(self, persona):
        if isinstance(persona, Persona):
            self.ciudadanos.append(persona)

    def retorno_lista_comunidad(self):
        return self.ciudadanos

    def persona_muere(self, persona):
        self.ciudadanos.remove(persona)
