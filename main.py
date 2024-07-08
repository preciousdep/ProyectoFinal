import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject, GLib
import matplotlib.pyplot as plt
from simulador import Simulador
plt.switch_backend('tkagg')


def on_quit_action(self, _action):
    quit()


# clase ventana
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(vbox)

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)
        self.set_title("Simulador de epidemia")

        # Listado del menu
        menu = Gio.Menu.new()

        # Create a popover
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # crea un menu
        self.menu_popover = Gtk.MenuButton()
        self.menu_popover.set_popover(self.popover)
        self.menu_popover.set_icon_name("open-menu-symbolic")

        # agrega headerbar el menu popover
        header_bar.pack_end(self.menu_popover)

        # Add an about dialog
        about_menu = Gio.SimpleAction.new("about", None)
        about_menu.connect("activate", self.show_about_dialog)
        self.add_action(about_menu)
        menu.append("Acerca de", "win.about")

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", on_quit_action)
        self.add_action(action)
        menu.append("Salir", "win.quit")

        self.label_pasos = Gtk.Label(label="Dia: 1")
        vbox.append(self.label_pasos)

        self.label_total_personas = Gtk.Label(
            label=f"Total comunidad: {simulador.lista_ciudadanos_comunidad}")
        vbox.append(self.label_total_personas)

        self.label_susceptibles = Gtk.Label(
            label=f"Susceptibles: {simulador.get_susceptibles()}")
        vbox.append(self.label_susceptibles)

        self.label_contagiados = Gtk.Label(
            label=f"Contagiados: {simulador.get_contagiados()}")
        vbox.append(self.label_contagiados)

        self.label_recuperados = Gtk.Label(
            label=f"Recuperados: {simulador.get_recuperados()}")
        vbox.append(self.label_recuperados)

        self.label_muertos = Gtk.Label(
            label=f"Muertos: {simulador.get_muertos()}")
        vbox.append(self.label_muertos)

        self.label_tasa_contagio = Gtk.Label(
            label=f"Tasa de contagio: {simulador.enfermedad.get_probabilidad()}%")
        vbox.append(self.label_tasa_contagio)

        self.label_tasa_recuperacion = Gtk.Label(
            label=f"Tasa de recuperacion: {simulador.get_dias_max_enfermedad()} dias")
        vbox.append(self.label_tasa_recuperacion)

        self.button = Gtk.Button(label="Pasar dia")
        self.button.connect("clicked", self.on_button_clicked)
        vbox.append(self.button)

        self.boton_grafico = Gtk.Button(label="Mostrar Grafico")
        self.boton_grafico.connect("clicked", self.boton_grafico_mostrar)
        vbox.append(self.boton_grafico)

        # aqui se van a guardar los datos de cada dia en listas dentro de lista
        # para posteriormente guardarlos en un arreglo numpy y poder agregar
        # al grafico plot
        self.arreglo_datos = []

    # detalles ventana
    def show_about_dialog(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)
        self.about.set_authors(["Astrid"])
        self.about.set_copyright("Copyright 2024 Astrid Leon")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_version("1.0")
        self.about.set_visible(True)

    # respuesta del boton para mostrar el grafico
    def boton_grafico_mostrar(self, widget):
        lista_np = simulador.guardar_en_numpy(self.arreglo_datos)
        dias = lista_np[:, 0]
        susceptibles = lista_np[:, 1]
        infectados = lista_np[:, 2]
        recuperados = lista_np[:, 3]

        fig = plt.figure()
        ax = fig.subplots()

        ax.plot(dias, susceptibles, label='Susceptibles', marker='o')
        ax.plot(dias, infectados, label='Infectados', marker='s')
        ax.plot(dias, recuperados, label='Recuperados', marker='^')

        ax.set_xlabel('Dias')
        ax.set_ylabel('Poblacion')
        ax.set_title('Simulador de contagio')
        ax.legend()
        ax.grid(True)

        plt.show()

    # pasa un dia de la simulacion
    def on_button_clicked(self, widget):
        simulador.contar_dias()
        simulador.contar_contagiados_comunidad()
        # los contagios ocurren luego del check inicial del dia
        simulador.contagio()
        simulador.contar_dias_curarse()
        simulador.muereono()

        if simulador.get_contagiados() != 0:
            simulador.tasa_recuperacion = (
             simulador.get_recuperados() / simulador.get_contagiados())
        else:
            simulador.tasa_recuperacion = 0
        # se 'refrescan' todas las etiquetas mostradas
        self.label_pasos.set_text(f"Dia: {simulador.get_contador_dias()}")
        self.label_total_personas.set_text(
            f"Total comunidad: {simulador.lista_ciudadanos_comunidad}")
        self.label_susceptibles.set_text(
            f"Susceptibles: {simulador.get_susceptibles()}")
        self.label_contagiados.set_text(
            f"Contagiados: {simulador.get_contagiados()}")
        self.label_recuperados.set_text(
            f"Recuperados: {simulador.get_recuperados()}")
        self.label_muertos.set_text(f"Muertos: {simulador.get_muertos()}")
        self.label_tasa_recuperacion.set_text(
            f"Tasa de recuperacion: {simulador.get_dias_max_enfermedad()} dias")
        self.label_tasa_contagio.set_text(
            f"Tasa de contagio: {simulador.enfermedad.get_probabilidad()}%")
        # se agregan los datos del dia al arreglo
        self.arreglo_datos.append(
            [simulador.get_contador_dias(), simulador.get_susceptibles(),
             simulador.get_contagiados(), simulador.get_recuperados()])


# clase aplicacion

class App(Gtk.Application):
    def __init__(self, **kwargs):
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
    simulador.contar_dias()
    simulador.contar_contagiados_comunidad()
    app.run(None)
