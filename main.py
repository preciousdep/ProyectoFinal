from simulador import Simulador
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gio

# clase ventana

class MainWindow(Gtk.Window):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        

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
    app.run()
    simulador = Simulador()
    simulador.dias()


