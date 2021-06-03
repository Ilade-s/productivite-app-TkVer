"""
Application/Programme de productivité et d'emploi du temps
Consiste en une interface graphique tkinter : 
    - Avec un stockage géré par DatabaseHandler :
        - format csv (dossier data)
        (- format sql)
    - on peut ouvrir des bases de données avec nos tâches, en créer et les exporter
    - Affiche et permet de modifier des tâches, ainsi que de les trier par type
"""

__version__ = "0.1"
__author__ = "Merlet Raphaël"

from DatabaseHandler import CsvHandler as DbM  # Gestion base de donnée
from PlotHandler import *  # fonctions de création de graphique
from tkinter import *  # GUI
from tkinter import ttk # meilleurs widgets
import tkinter.filedialog as fldialog  # Choix de fichier etc...
import os  # Pour trouver le répertoire courant (os.getcwd)
import tkinter.messagebox as msgbox  # Messages d'information ou d'avertissement
import shutil  # Sauvegarde/copie de fichiers


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
        self.add_cascade(label="File", underline=0, menu=self.FileMenu)
        self.FileMenu.add_command(
            label="Create new database", command=self.CreateDatabase)
        self.FileMenu.add_command(
            label="Open existant database", command=self.OpenDatabase)
        self.FileMenu.add_command(
            label="Save database", command=self.SaveDatabase)
        self.FileMenu.add_separator() # séparateur dans le menu déroulant <File>
        self.FileMenu.add_command(
            label="Close database", command=self.CloseDatabase)
        # Menu Edit
        self.EditMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Edit", menu=self.EditMenu)
        self.EditMenu.add_command(
            label="Save database as a new file", command=self.OpenDatabase)
        self.EditMenu.add_separator()
        self.EditMenu.add_command(
            label="Close database", command=self.CloseDatabase)

    def OpenDatabase(self):
        """
        Dialogue pour ouverture de base de donnée
        """
        a = f"Productivity App v{__version__} : Pas de base de donnée ouverte"
        a.split()
        path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data",
                title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path != None:
            self.master.Db = DbM(path)
            self.master.title(f"Productivity App v{__version__} : {path}")
            print(f"Ouverture DB réussie : {path}")
            msgbox.showinfo("Ouverture database",
                            "Ouverture du fichier réussie")
        else:
            print("Ouverture DB annulée")
            msgbox.showerror("Ouverture database",
                             "Ouverture database échouée/annulée")

    def CreateDatabase(self):
        """
        Dialogue pour ouverture d'une nouvelle base de donnée
        """
        path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data",
                title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path != None:
            if path[-4:]!=".csv":
                path += ".csv"
            # création d'un nouveau fichier CSV
            self.master.Db = DbM(path, "x+")
            # Ouverture fichier
            self.master.Db = DbM(path)
            # Ajout des labels de colonne
            self.master.Db.Add(self.master.DefaultLabel)
            self.master.title(f"Productivity App v{__version__} : {path}")
            print(f"Création DB réussie : {path}")
            msgbox.showinfo("Création database",
                            "Ouverture du fichier réussie")
        else:
            print("Création DB annulée")
            msgbox.showerror("Création database",
                             "Création database échouée/annulée")

    def CloseDatabase(self):
        """
        Fermeture de la base de donnée (si il y en a une d'ouverte)
        """
        if self.master.Db == None:
            msgbox.showinfo("Fermeture database",
                            "Il n'y a pas de base de donnée ouverte")
        else:
            try:
                self.master.Db.file.close()
                self.master.Db = None
                print("DB fermée")
                msgbox.showinfo("Fermeture database",
                                "Fermeture du fichier réussie")
            except Exception:
                print("Echec fermeture : pas de fichier ouvert ?")
                msgbox.showerror("Fermeture database",
                                    "Fermeture database échouée/annulée")

    def SaveDatabase(self):
        """
        Sauvegarde base de donnée dans un nouveau fichier
        """
        path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data",
                title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path != None:
            self.master.Db = DbM(path)
            print(f"Sauvegarde DB réussie : {path}")
            msgbox.showinfo("Sauvegarde database",
                            "Ouverture du fichier réussie")
        else:
            print("Sauvegarde DB annulée")
            msgbox.showerror("Sauvegarde database",
                             "Sauvegarde database échouée/annulée")


class MainFrame(ttk.Frame):
    """
    Partie principale de l'application qui permet d'afficher les tâches et les demandes d'inputs
    """

    def __init__(self, master=None) -> None:
        self.master = master
        # Style Frame
        s = ttk.Style()
        s.configure("MainFrame.TFrame", background="#292D3E", relief=SOLID)
        super().__init__(master, style="MainFrame.TFrame")
        self.CreateWidgets()
    
    def CreateWidgets(self):
        """
        Placement des widgets
        """
        Label(self, text="MainFrame", font=("Arial",20), background="grey").pack(anchor=CENTER)


class ActionFrame(ttk.Frame):
    """
    Frame placé à gauche (prenant 1/4 de la longueur) permettant de choisir les actions à effectuer
    """

    def __init__(self, master=None) -> None:
        self.master = master
        # Style Frame
        s = ttk.Style()
        s.configure("ActionFrame.TFrame", background="#5B648A", relief=RAISED)
        super().__init__(master, style="ActionFrame.TFrame")
        self.CreateWidgets()
    
    def CreateWidgets(self):
        """
        Placement des widgets
        """
        def AddLabel():
            if self.master.Db != None:
                self.master.Db.Add(["name", "creation", "duedate", "type"])

        Label(self, text="ActionFrame", font=("Arial",20), background="grey").pack(anchor=CENTER)

        Button(self, text="Ajouter label", command=AddLabel).pack(ipadx=20,ipady=10)
    

class TopLevel(Tk):
    """
    Fenêtre tkinter en elle même, contient les Frames placées en grid
    """

    def __init__(self, x=1200, y=600) -> None:
        """
        Initialisation de la fenêtre
        """
        self.DefaultLabel = ["name", "creation", "duedate", "type"]
        self.geo = (x,y)
        super().__init__()
        self.title(f"Productivity App v{__version__} : Pas de base de donnée ouverte")
        self.Db = None
        self.geometry("{}x{}".format(x, y))
        # Placement des Frames
        self.SetupFrames()

    def SetupFrames(self):
        """
        Place les Frames dans la grille
        """
        print("Placement Frames...")
        # Création Style
        self.s = ttk.Style()
        self.s.configure("ActionFrame.TFrame", background="#5B648A", relief=RAISED) # Style ActionFrame
        self.s.configure("MainFrame.TFrame", background="#292D3E", relief=SUNKEN) # Style MainFrame
        # Configuration lignes et colonnes
        for r in range(1):
            self.rowconfigure(r)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        # Placement Frames dans les colonnes
        print("Création Menu...")
        self.Menu = MenuBar(self)
        self.config(menu=self.Menu)
        # placement Menu d'actions
        print("Création ActionFrame...")
        self.ActionFrame = ActionFrame(self)
        self.ActionFrame.grid(row=0,column=0,ipadx=self.geo[0]/4,ipady=self.geo[1])
        # Placement MainFrame
        print("Création MainFrame...")
        self.MainFrame = MainFrame(self)
        self.MainFrame.grid(row=0,column=1,ipadx=self.geo[0]/4*3,ipady=self.geo[1])



def main():
    print("===============================================================")
    print(f"Productivity App v{__version__}")
    print(f"Made by {__author__}")
    print("Source : https://github.com/Ilade-s/productivite-app-TkVer")
    print("===============================================================")
    # Création fenêtre
    app = TopLevel()
    app.mainloop()


if __name__ == '__main__':  # test
    main()
