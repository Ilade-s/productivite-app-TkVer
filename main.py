"""
Application/Programme de productivité et d'emploi du temps
supporte la connexion au serveur correspondant et l'exportation en CSV
on peut afficher les tâches en se synchronisant au serveur
"""

from Global import __version__, __author__, x, y, ShowVersion, platform, DefaultLabel # variables globales
# importation des frames
from SubFrame import *
from MainFrame import *
from EntryFrame import *
from ActionFrame import *
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
        self.DefaultLabel = DefaultLabel
        self.style = ttk.Style()
        if platform=="linux":
            self.style.theme_use("clam")
        self.geo = (x, y)
        self.iconphoto(True, PhotoImage(file="Assets/favicon.png"))
        self.title(
            f"Productivity App v{__version__} : Pas de base de donnée ouverte")
        self.Db = None
        self.Server = None
        self.EntryFrame = None
        self.geometry("{}x{}".format(x, y))
        #self.resizable(False, False)
        # Placement des Frames
        self.SetupFrames()

    def SetupFrames(self):
        """
        Place les Frames dans la grille
        """
        print("Placement Frames...")
        # Placement Frames dans les colonnes
        print("Création Menu...")
        self.Menu = MenuBar(self)
        self.config(menu=self.Menu)
        # placement Menu d'actions
        print("Création ActionFrame...")
        self.ActionFrame = ActionFrame(self)
        # Placement MainFrame
        print("Création MainFrame...")
        self.MainFrame = MainFrame(self)
        # Placement SubFrame
        print("Création SubFrame...")
        self.SubFrame = SubFrame(self)


def main():
    ShowVersion() # affichage info prog
    # Création fenêtre
    app = TopLevel()
    app.mainloop()


if __name__ == '__main__':  # test
    main()
