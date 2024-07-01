from persona import Persona
from comunidad import Comunidad
from enfermedad import Enfermedad
import random
import pandas as pd

    # prueba de simulador para interactuar con las clases
    # draft crea una comunidad para controlar el manejo del contagio
    # y como ocurren (aun no se usan formulas) (se usa pandas)


class Simulador:
    def __init__(self):
        #asegurarse que no hayan familias de mas de 3 personas
        self.comunidad = Comunidad()
        self.enfermedad = Enfermedad("influenza",20,4)

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
        miembros_comunidad = random.randint(1000,10000)
        self.comunidad.set_probabilidad_contacto_estrecho()
        self.comunidad.set_promedio_contacto_fisico()

        ident = 0
        print(f"""Promedio de contacto fisico de la comunidad: {self.comunidad.get_promedio_fisico()} personas \n
    Probabilidad de que un contacto fisico no familiar sea estrecho: {self.comunidad.get_probabilidad_contacto_estrecho()}% """)

        for i in range(miembros_comunidad):
            # a corresponde al nombre aleatorio del archivo
            # y p al apellido
            a = random.randint(0,299)
            p = random.randint(0,299)
            # draft infectados iniciales
            infectado = random.randint(0,100)
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
            #se agrega a la lista de ciudadanos en la comunidad
            self.comunidad.agregar_persona_comunidad(ciudadano)

    def muereono(self):
        for i in self.comunidad.retorno_lista_comunidad():
            if i.get_contagiado() == True :
                a = random.randint(0,100)
                if a <= 2:
                    self.comunidad.persona_muere(i)
                    print(f"{i.get_id()}. {i.get_nombre()} {i.get_apellido()} ha muerto...")
                
    def contar_contagiados_comunidad(self):
        contador_contagiados = 0
        lista_ciudadanos_comunidad = self.comunidad.retorno_lista_comunidad()
        for i in lista_ciudadanos_comunidad:
            if i.get_contagiado():
                contador_contagiados += 1
                print(i.get_id(), i.get_nombre(), i.get_apellido(), "presenta la enfermedad")
        return contador_contagiados

    def contar_dias_curarse(self,contador):
        lista_ciudadanos_comunidad = self.comunidad.retorno_lista_comunidad()
        enfermedad = self.comunidad.get_enfermedad()
        dias_max = enfermedad.get_tiempo_infectado()
        contador_recuperados = 0
        for i in lista_ciudadanos_comunidad:
            if i.get_contagiado() == True:
                i.contar_dias_enfermo()
            
            if i.get_dias_enfermo() == dias_max:
                recuperado = random.randint(0,100)
                if recuperado >= 20:
                    i.set_contagiado(False)
                    i.set_sir(2)
                    print(f"{i.get_nombre()} {i.get_apellido()} se ha recuperado")

            if i.get_sir() == 2:
                contador_recuperados += 1

    # mecanismo de contagio random draft
    def contagio(self):
        lista = self.comunidad.retorno_lista_comunidad()
        for i in lista:
            contactos_dia = random.randint(self.comunidad.get_promedio_fisico()-1, self.comunidad.get_promedio_fisico()+1)
            if i.get_contagiado() == True:
                estrecho = self.comunidad.get_probabilidad_contacto_estrecho()
                for i in range(0,contactos_dia):
                    persona_x = random.randint(0,len(lista)-1)
                    decidir_contagio = random.randint(0,100)
                    if decidir_contagio < estrecho:
                        valor = self.enfermedad.infeccion()
                        self.comunidad.retorno_lista_comunidad()[persona_x].set_contagiado(valor)


    #def guarda_en_archivo(): #overwrite o agregar linea?


    def dias(self):
        pasandias = True
        self.crea_comunidad()
        self.comunidad.add_enfermedad(self.enfermedad)
        contador_dias = 0
        while pasandias:
            contador_dias += 1
            contagios = self.contar_contagiados_comunidad()
            self.contar_dias_curarse(contador_dias)
            print(f"Dia {contador_dias}")
            self.contagio()
            print(f"{contagios} casos activos de {len(self.comunidad.retorno_lista_comunidad())}")
            # las personas de la comunidad disminuyen constantemente
            self.muereono()
            input()