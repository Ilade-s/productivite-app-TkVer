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
import shutil # Sauvegarde/copie de fichiers

class MenuBar(Menu):
    """
    Menu qui s'affiche à gauche dans l'application tkinter

    Affiche les actions possibles en fonction de MainFrame
    """

    def __init__(self, master, dbtype="csv") -> None:
        super().__init__(master)
        self.master = master
        self.dbtype = dbtype
        self.FileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=self.FileMenu)
        self.FileMenu.add_command(label="Open database", command=self.OpenDatabase)
        self.EditMenu.add_command(label="Save database", command=self.SaveDatabase)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Close database", command=self.CloseDatabase)
        # Menu Edit
        self.EditMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Edit", menu=self.EditMenu)
        self.EditMenu.add_command(label="Save database as a new file", command=self.OpenDatabase)
        self.EditMenu.add_separator()
        self.EditMenu.add_command(label="Close database", command=self.CloseDatabase)

    
    def OpenDatabase(self):
        """
        Dialogue pour ouverture de base de donnée
        """
        path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data",
            title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path!=None:
            self.master.Db = DbM(path)
            self.master.Db.dbW.writerow(["name","creation","duedate","type"])
            print(f"Ouverture DB réussie : {path}")
            msgbox.showinfo("Ouverture database","Ouverture du fichier réussie")
        else:
            print("Ouverture DB annulée")
            msgbox.showerror("Ouverture database","Ouverture database échouée/annulée")

    
    def CloseDatabase(self):
        """
        Fermeture de la base de donnée
        """
        self.master.Db.file.close()
        print("DB fermée")
    
    def SaveDatabase(self):
        """
        Sauvegarde base de donnée dans un nouveau fichier
        """
        path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data",
            title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path!=None:
            self.master.Db = DbM(path)
            self.master.Db.dbW.writerow(["name","creation","duedate","type"])
            print(f"Sauvegarde DB réussie : {path}")
            msgbox.showinfo("Sauvegarde database","Ouverture du fichier réussie")
        else:
            print("Sauvegarde DB annulée")
            msgbox.showerror("Sauvegarde database","Sauvegarde database échouée/annulée")

class MainFrame(Frame):
    """
    Partie principale de l'application qui permet d'afficher les tâches et les demandes d'inputs
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
        self.Db = None
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