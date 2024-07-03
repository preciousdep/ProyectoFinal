from simulador import Simulador
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gio

# clase ventana

class MainWindow(Gtk.Window):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(vbox)

        self.label_info_comunidad = Gtk.Label(label=f"Probabilidad de contacto estrecho: {simulador.comunidad_probabilidad_estrecho}")
        vbox.append(self.label_info_comunidad)

        self.label_susceptibles = Gtk.Label(label=f"Susceptibles: {simulador.contador_susceptibles}")
        vbox.append(self.label_susceptibles)

        self.label_contagiados = Gtk.Label(label=f"Contagiados: {simulador.contador_contagiados}")
        vbox.append(self.label_contagiados)

        self.label_recuperados = Gtk.Label(label=f"Recuperados: {simulador.contador_recuperados}")
        vbox.append(self.label_recuperados)

        self.label_muertos = Gtk.Label(label=f"Muertos: {simulador.contador_muertos}")
        vbox.append(self.label_muertos)

        self.button = Gtk.Button(label="Pasar dia")
        self.button.connect("clicked", self.on_button_clicked)
        vbox.append(self.button)

    def on_button_clicked(self, widget):
        simulador.dias()
        self.label_info_comunidad.set_text(f"Paso {simulador.texto_dia} dia/s")
        self.label_susceptibles.set_text(f"Susceptibles: {simulador.contador_susceptibles}")
        self.label_contagiados.set_text(f"Contagiados: {simulador.contador_contagiados}")
        self.label_recuperados.set_text(f"Recuperados: {simulador.contador_recuperados}")
        self.label_muertos.set_text(f"Muertos: {simulador.contador_muertos}")


# clase aplicacion

class App(Gtk.Application):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    # estado en curso de la aplicación

    def do_activate(self):
        print("Simulacion en curso")
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()



if __name__ == "__main__":
    app = App()
    simulador = Simulador()
    simulador.crea_comunidad()
    app.run(None)

