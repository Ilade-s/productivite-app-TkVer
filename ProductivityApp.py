"""
Application/Programme de productivité et d'emploi du temps
Consiste en une interface graphique tkinter : 
    - Avec un stockage géré par DatabaseHandler :
        - format csv (dossier data)
        (- format sql)
    - Permet de gérer plusieurs utilisateurs
    - Affiche et permet de modifier des tâches, ainsi que de les trier par type
"""

__version__ = "0.1"
__author__ = "Merlet Raphaël"

from DatabaseHandler import CsvHandler as DbM # Gestion base de donnée
from PlotHandler import * # fonctions de création de graphique
from tkinter import * # GUI
from tkinter.ttk import *  # meilleurs widgets
import tkinter.filedialog as fldialog  # Choix de fichier etc...
import os  # Pour trouver le répertoire courant (os.getcwd)
import tkinter.messagebox as msgbox  # Messages d'information ou d'avertissement

class MenuBar(Menu):
    """
    Menu qui s'affiche à gauche dans l'application tkinter

    Affiche les actions possibles en fonction de MainFrame
    """

    def __init__(self, master, dbtype="csv") -> None:
        super().__init__(master)
        self.master = master
        self.dbtype = dbtype
        self.DbMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=self.DbMenu)
        self.DbMenu.add_command(label="Open database", underline=1, command=self.OpenDatabase)
    
    def OpenDatabase(self):
        """
        Dialogue pour ouverture de base de donnée
        """
        path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data",
            title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))

        self.master.Db = DbM(path)

class MainFrame(Frame):
    """
    Partie principale de l'application qui ermet d'afficher les tâches et les demandes d'inputs
    """

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.pack()

class SubFrame(Frame):
    """
    Bandeau en bas de l'application qui permet de quitter et de changer de pages dans la liste des tâches
    """

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.pack()

class TopLevel(Tk):
    """
    Fenêtre tkinter en elle même, contient les Frames placées en grid
    """

    def __init__(self, x=1000, y=600) -> None:
        super().__init__()
        self.geometry("{}x{}".format(x,y))
        # Placement des Frames
        self.SetupFrames()
    
    def SetupFrames(self):
        """
        Place les Frames dans la grille
        """
        # Configuration lignes et colonnes
        for r in range(2):
            self.rowconfigure(r)
        for c in range(4):
            self.columnconfigure(c)
        # Placement Frames dans les colonnes
        self.Menu = MenuBar(self)
        self.config(menu=self.Menu)

        

def main():
    print("===============================================================")
    print(f"Productivity App v{__version__}")
    print(f"Made by {__author__}")
    print("Source : https://github.com/Ilade-s/productivite-app-TkVer")
    print("===============================================================")

    app = TopLevel()
    app.mainloop()

if __name__=='__main__': # test
    main()