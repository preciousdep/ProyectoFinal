from persona import Persona
from comunidad import Comunidad
from enfermedad import Enfermedad
import random

# prueba de simulador para interactuar con las clases

covid = Enfermedad('covid',20, random.randint(1,40))
talca = Comunidad()
talca.add_enfermedad(covid)

persona1 = Persona(1,'Paco','Pipipi')
persona2 = Persona(2,'Peca','Pipipi')

talca.agregar_persona_comunidad(persona1)
talca.agregar_persona_comunidad(persona2)

# draft funcionamiento del contagio

persona2.set_contagiado(True)

#valor es un bool

valor = talca.contacto_estrecho(persona1,persona2,covid)
persona1.set_contagiado(valor)

if persona1.get_contagiado() == True:
    print(f"{persona1.get_nombre()} se ha enfermado")
else:
    print("nope")

