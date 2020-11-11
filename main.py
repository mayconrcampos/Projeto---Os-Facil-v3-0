import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from abas import *
from db import Db
#import webbrowser


class Main(Janela, Funcs, Mensagem, Db, Aba_01, Aba_02, Aba_03, Aba_04, Aba_05, Aba_06, Aba_07):
    def __init__(self):
        self.janela()

        self.botoes_aba_01()
        self.liga_stack()
        self.liga_botoes_aba_01()

        self.botoes_aba_02()
        self.liga_botoes_aba_02()
        self.mostrar_tview_clientes()

        self.botoes_aba_03()
        self.liga_botoes_aba_03()
        self.mostrar_tview_produtos()

        self.botoes_aba_04()
        self.liga_botoes_aba_04()
        self.lista_clientes()
        self.mostrar_tview_os()

        self.botoes_aba_05()
        self.liga_botoes_aba_05()

        self.botoes_aba_06()
        self.liga_botoes_aba_06()

        self.botoes_aba_07()
        self.liga_botoes_aba_07()

        self.janela.show()


if __name__ == "__main__":
    app = Main()
    Gtk.main()