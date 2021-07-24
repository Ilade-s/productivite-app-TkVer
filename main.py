"""
Application/Programme de productivité et d'emploi du temps
supporte la connexion au serveur correspondant et l'exportation en CSV
on peut afficher les tâches en se synchronisant au serveur
"""

# variables globales
from Global import __VERSION__, __AUTHOR__, x, y, show_version, platform
# importation des frames
from NavBar import *
from MainFrame import *
from EntryFrame import *
from Menu import *


class TopLevel(Tk):
    """
    Fenêtre tkinter en elle même, contient les Frames placées en grid
    """

    def __init__(self, x=x, y=y) -> None:
        """
        Initialisation de la fenêtre
        """
        super().__init__()
        self.style = ttk.Style()
        if platform=="linux":
            self.style.theme_use("clam")
        self.iconphoto(True, PhotoImage(file="Assets/calendar.png"))
        self.title(
            f"Productivity App v{__VERSION__} : Pas de base de donnée ouverte")
        self.File = None
        self.Server = None
        self.EntryFrame = None
        self.geometry("{}x{}".format(x, y))
        # Placement des Frames
        self.setup_frames()

    def setup_frames(self):
        """
        Place les Frames dans la grille
        """
        print("Placement Frames...")
        # Placement Frames (initialisation des classes)
        # Placement MainFrame
        print("Création MainFrame...")
        self.MainFrame = MainFrame(self)
        # Placement NavBar
        print("Création NavBar...")
        self.NavBar = NavBar(self)
        # Placement Menu
        print("Création Menu...")
        self.Menu = MenuBar(self)
        self.config(menu=self.Menu)


def main():
    show_version() # affichage info prog
    # Création fenêtre
    app = TopLevel()
    app.mainloop()


if __name__ == '__main__':
    main()
