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
from WebHandler import WebInterface  # Classe d'interfacage avec un serveur web
from tkinter import *  # GUI
from tkinter import ttk  # meilleurs widgets
from tkinter import filedialog as fldialog  # Choix de fichier etc...
# Messages d'information ou d'avertissement
from tkinter import messagebox as msgbox
from tkinter import simpledialog as smpldial  # Demande d'informations simples
import os  # Pour trouver le répertoire courant (os.getcwd)


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
        self.FileMenu.add_separator()  # séparateur
        self.FileMenu.add_command(
            label="Close database", command=self.CloseDatabase)
        self.FileMenu.add_separator()  # séparateu
        self.FileMenu.add_command(
            label="Exit", command=self.master.destroy)
        # Menu Web
        self.WebMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Web", menu=self.WebMenu)
        self.WebMenu.add_command(
            label="Connect to server", command=self.ServerConnect)
        self.WebMenu.add_command(
            label="Disconnect", command=self.ServerDisconnect)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Sync to database", command=self.ServerSync)
        self.WebMenu.add_command(
            label="Extract database to csv", command=self.ServerExtract)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Login", command=self.ServerLogin)
        self.WebMenu.add_command(
            label="Logout", command=self.ServerLogout)

    # fonctions du menu déroulant File
    def OpenDatabase(self, msg=True, path=""):
        """
        Dialogue pour ouverture de base de donnée
        msg : bool (indique si l'ouverture doit être discrète ou non et si on doit déconnecter le serveur)
        path : str (optionnel, si fourni, la fonction ne demandera pas le chemin à nouveau)
        """
        if self.master.Server != None and msg:
            self.ServerDisconnect()
        if path == "":
            path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data",
                    title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path != None:
            self.master.Db = DbM(path)
            self.master.title(f"Productivity App v{__version__} : {path}")
            print(f"Ouverture DB réussie : {path}")
            if msg:
                msgbox.showinfo("Ouverture database",
                                f"Ouverture du fichier {path} réussie")
        else:
            print("Ouverture DB annulée")
            if msg:
                msgbox.showerror("Ouverture database",
                                "Ouverture database échouée/annulée")

    def CreateDatabase(self, msg=True):
        """
        Dialogue pour ouverture d'une nouvelle base de donnée
        msg : bool (indique si la création doit être discrète ou non et si on doit déconnecter le serveur)
        SORTIE : (exitcode: int, path: str)
        """
        if self.master.Server != None and msg:
            self.ServerDisconnect()
        path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data",
                                          title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if os.path.exists(path): # file already exists
            return (0, path)
        if path != None:
            if path[:-4] != ".csv":
                path += ".csv"
            # création d'un nouveau fichier CSV
            self.master.Db = DbM(path, "x+")
            # Ouverture fichier
            self.master.Db = DbM(path)
            # Ajout des labels de colonne
            self.master.Db.Add(self.master.DefaultLabel)
            self.master.title(f"Productivity App v{__version__} : {path}")
            print(f"Création DB réussie : {path}")
            if msg:
                msgbox.showinfo("Création database",
                                "Création et ouverture du fichier réussie")
            return (1, path)
        else:
            print("Création DB annulée")
            if msg:
                msgbox.showerror("Création database",
                                "Création database échouée/annulée")
            return (0, path)

    def CloseDatabase(self,msg=True):
        """
        Fermeture de la base de donnée (si il y en a une d'ouverte)
        msg : bool (indique si la fermeture doit être discrète ou non)
        """
        if self.master.Db == None:
            msgbox.showinfo("Fermeture database",
                            "Il n'y a pas de base de donnée ouverte")
        else:
            try:
                self.master.Db.file.close()
                self.master.Db = None
                self.master.title(
                    f"Productivity App v{__version__} : Pas de base de donnée ouverte")
                print("DB fermée")
                if msg:
                    msgbox.showinfo("Fermeture database",
                                    "Fermeture du fichier réussie")
            except Exception:
                print("Echec fermeture : pas de fichier ouvert ?")
                if msg:
                    msgbox.showerror("Fermeture database",
                                        "Fermeture database échouée/annulée")

    def SaveDatabase(self):
        """
        Sauvegarde base de donnée dans un nouveau fichier
        """
        if self.master.Db == None:
            msgbox.showinfo("Sauvegarde database",
                            "Il n'y a pas de base de donnée ouverte")
        else:
            path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data",
                                              title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
            if path[-4:] != ".csv":
                path += ".csv"
            if path != None:
                NewFile = DbM(path, "x+")
                NewFile = DbM(path)
                self.master.Db.ReadAll()
                for row in self.master.Db.Data:
                    NewFile.Add(row)
                print(f"Sauvegarde DB réussie : {path}")
                msgbox.showinfo("Sauvegarde database",
                                "Sauvegarde du fichier réussie")
            else:
                print("Sauvegarde DB annulée")
                msgbox.showerror("Sauvegarde database",
                                 "Sauvegarde database échouée/annulée")

    # fonctions du menu déroulant Web
    def ServerConnect(self):
        """
        Dialogue pour connexion à un serveur web
        """
        if self.master.Db != None:
            self.CloseDatabase(False)
        # Fenêtre de demande de l'adresse web
        adresse = smpldial.askstring(
            "Adresse du serveur", "Adresse web complète (IP ou normale):")
        try:
            self.master.Server = WebInterface(adress=adresse)
            print(f"Connecté au serveur : {adresse}")
            self.master.title(
                f"Productivity App v{__version__} : {adresse} : Non identifié")
            msgbox.showinfo(
                "Connexion serveur", f"Connexion réussie au serveur à l'adresse {adresse}")
        except Exception:
            print(f"Connexion au serveur à l'adresse {adresse} échouée")
            msgbox.showerror(
                "Connexion serveur", f"Connexion au serveur à l'adresse {adresse} échouée")

    def ServerLogin(self):
        """
        Dialogue pour identification d'un compte dans le serveur
        """
        if self.master.Server == None: # Pas de serveur ouvert
            msgbox.showinfo("Login Serveur","Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account != None:
            msgbox.showinfo("Login Serveur",f"Vous êtes déjà connectés au compte {self.master.Server.Account}\nVeuilez vous déconnecter avant")
        else:
            # Récupération identitifant et mot de passe
            #adresse = smpldial.askstring("Connexion compte","Adresse page de connexion :")
            iD = smpldial.askstring("Connexion compte","Identifant/Adresse mail :")
            passwd = smpldial.askstring("Connexion compte","Mot de passe :", show="*")
            # Essai de login
            try:
                self.master.Server.Login(iD, passwd, self.master.Server.adress+"/login")
                self.master.title(
                    f"Productivity App v{__version__} : {self.master.Server.adress} : {iD}")
                msgbox.showinfo("Login Serveur",f"Connexion au compte {iD} réussie")
            except Exception as e: # Echec login
                self.master.Server.Account = None
                print(f"Echec login au compte {iD}")
                msgbox.showerror("Login Serveur",f"Echec de la connexion, veuillez rééssayer : {e}")

    def ServerLogout(self,msg=True):
        """
        Permet de se déconnecter de son compte
        msg : bool (indique si la déconnexion doit être discrète ou non)
        """
        if self.master.Server == None: # Pas de serveur ouvert
            msgbox.showinfo("Logout Serveur","Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None: # Pas de compte connecté
            msgbox.showinfo("Logout Serveur","Vous n'êtes pas connectés à un compte") 
        else:
            self.master.Server.Account = None
            self.master.title(
                    f"Productivity App v{__version__} : {self.master.Server.adress} : non identifié")
            if msg:
                msgbox.showinfo("Login Serveur",f"Déconnecté du compte")
            print("Déconnecté du compte")

    def ServerDisconnect(self):
        """
        Déconnexion d'un serveur web
        """
        if self.master.Server == None: # Pas de serveur ouvert
            msgbox.showinfo("Déconnexion Serveur","Vous n'êtes pas connectés à un serveur")
        else:
            if self.master.Server.Account != None:
                self.ServerLogout(False)
            self.master.Server = None
            self.master.title(
                f"Productivity App v{__version__} : Pas de base de donnée ouverte")
            print("Déconnecté du serveur")

    def ServerSync(self):
        """
        Permet de se synchroniser à la base de donnée (après être connecté à un compte)
        """
        if self.master.Server == None: # Pas de serveur ouvert
            msgbox.showinfo("Sync Database","Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None: # Pas de compte connecté
            msgbox.showinfo("Sync Database","Vous n'êtes pas connectés à un compte") 
        else:
            try:
                self.master.MainFrame.Tasks = self.master.Server.GetData()
                #print(f"Tasks : {self.master.MainFrame.Tasks}")
                self.master.MainFrame.ShowTasks()
                print("Synchronisation réussie")
                msgbox.showinfo("Sync Database","Synchronisation réussie")
            except Exception as e:
                print("Echec de la synchronisation")
                msgbox.showerror("Sync Database",f"La base de donnée n'a pas pu être synchronisée : {e}")
    
    def ServerExtract(self):
        """
        Permet d'extraire la base de donnée dans un fichier CSV
        """
        if self.master.Server == None: # Pas de serveur ouvert
            msgbox.showinfo("Extract Database","Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None: # Pas de compte connecté
            msgbox.showinfo("Extract Database","Vous n'êtes pas connectés à un compte") 
        else:
            try:
                (exitcode, path) = self.CreateDatabase(False)
                if not exitcode: # création impossile (le fichier existe déjà)
                    print("Le fichier existe déjà... switching to func OpenDatabase")
                    self.OpenDatabase(False, path)
                TaskList = self.master.Server.GetData()
                #print(f"Tasks : {TaskList}")
                for task in TaskList:
                    self.master.Db.Add(task[1:])
                msgbox.showinfo("Extract Database","Extraction réussie")
            except Exception as e:
                print("Echec de l'extraction")
                msgbox.showerror("Extract Database",f"La base de donnée n'a pas pu être extraite : {e}")


class MainFrame(ttk.Frame):
    """
    Partie principale de l'application qui permet d'afficher les tâches et les demandes d'inputs
    """

    def __init__(self, master) -> None:
        self.master = master
        self.Tasks = []
        self.ShownTasks = []
        self.Ci = 0
        # Style Frame
        s = ttk.Style()
        s.configure("MainFrame.TFrame", background="#292D3E", relief=SOLID)
        super().__init__(master, style="MainFrame.TFrame")
        self.CreateWidgets()

    def CreateWidgets(self):
        """
        Placement des widgets
        """
        Label(self, text="MainFrame", font=("Arial", 20),
              background="grey").pack(anchor=CENTER)
    
    def ShowTasks(self):
        """
        Affiche les tâches
        """
        # Unpack tâches précedemment affichées
        if self.ShownTasks != []:
            for task in self.ShownTasks:
                task.destroy()

        self.ShownTasks = [Checkbutton(self, text=f"{task[1]} // {task[2]}", 
            background="#5B648A", font=(20), width=15, anchor="w") 
                for task in self.Tasks[self.Ci:self.Ci+10]]
        for task in self.ShownTasks:
            task.pack(pady=5,padx=20,anchor="w")


class ActionFrame(ttk.Frame):
    """
    Frame placé à gauche (prenant 1/4 de la longueur) permettant de choisir les actions à effectuer
    """

    def __init__(self, master) -> None:
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
        Label(self, text="ActionFrame", font=("Arial", 20),
              background="grey").pack(anchor=CENTER)


class SubFrame(ttk.Frame):
    """

    """

    def __init__(self, master) -> None:
        self.master = master
        # Style Frame
        s = ttk.Style()
        s.configure("SubFrame.TFrame", background="#A8B8FF", relief=RAISED)
        super().__init__(master, style="SubFrame.TFrame")
        self.CreateWidgets()

    def CreateWidgets(self):
        """
        Placement des widgets
        """
        Label(self, text="SubFrame", font=("Arial", 20),
              background="grey").pack(anchor=CENTER)


class TopLevel(Tk):
    """
    Fenêtre tkinter en elle même, contient les Frames placées en grid
    """

    def __init__(self, x=1200, y=600) -> None:
        """
        Initialisation de la fenêtre
        """
        self.DefaultLabel = ["name", "date", "priority"]
        self.geo = (x, y)
        super().__init__()
        self.title(
            f"Productivity App v{__version__} : Pas de base de donnée ouverte")
        self.Db = None
        self.Server = None
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
        self.s.configure("ActionFrame.TFrame", background="#5B648A",
                         relief=RAISED)  # Style ActionFrame
        self.s.configure("MainFrame.TFrame", background="#292D3E",
                         relief=SUNKEN)  # Style MainFrame
        # Configuration lignes et colonnes
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        # Placement Frames dans les colonnes
        print("Création Menu...")
        self.Menu = MenuBar(self)
        self.config(menu=self.Menu)
        # placement Menu d'actions
        print("Création ActionFrame...")
        self.ActionFrame = ActionFrame(self)
        self.ActionFrame.grid(
            row=0, column=0, rowspan=2, columnspan=1, sticky='nesw')
        # Placement MainFrame
        print("Création MainFrame...")
        self.MainFrame = MainFrame(self)
        self.MainFrame.grid(
            row=0, column=1, rowspan=1, columnspan=1, sticky='nesw')
        # Placement SubFrame
        print("Création SubFrame...")
        self.SubFrame = SubFrame(self)
        self.SubFrame.grid(
            row=1, column=1, rowspan=1, columnspan=1, sticky='nesw')


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
