from tkinter import *
from tkinter import filedialog as fldialog  # Choix de fichier etc...
# Messages d'information ou d'avertissement
from tkinter import messagebox as msgbox
import os  # Pour trouver le répertoire courant (os.getcwd)
from DatabaseHandler import CsvHandler as DbM  # Gestion base de donnée
# variables globales
from Global import __version__, ShowVersion, platform, DefaultLabel, x, y
from EntryFrame import *


class MenuBar(Menu):
    """
    Menu qui s'affiche à gauche dans l'application tkinter

    Affiche les actions possibles en fonction de MainFrame
    """

    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        # Création des menus déroulants
        self.CreateFileMenu() # Menu File
        self.CreateWebMenu() # Menu Web
        self.CreateViewMenu() # Menu View

    def CreateFileMenu(self):
        FileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=FileMenu)
        FileMenu.add_command(
            label="New...", command=self.CreateDatabase)
        FileMenu.add_command(
            label="Open...", command=self.OpenDatabase)
        FileMenu.add_separator()  # séparateur
        FileMenu.add_command(
            label="Save as...", command=self.SaveDatabase)
        FileMenu.add_command(
            label="Close database", command=self.CloseDatabase)

    def CreateWebMenu(self):
        self.WebMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Web", menu=self.WebMenu)
        self.WebMenu.add_command(
            label="Connect to server", command=self.ServerConnect)
        self.WebMenu.add_command(
            label="Login", command=self.ServerLogin)
        self.WebMenu.add_command(
            label="Signup", command=self.ServerSignup)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Disconnect", command=self.ServerDisconnect)
        self.WebMenu.add_command(
            label="Logout", command=self.ServerLogout)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Extract database to csv", command=self.ServerExtract)
        self.WebMenu.add_command(
            label="Add tasks from csv", command=self.ServerImport)

    def CreateViewMenu(self):
        ViewMenu = Menu(self, tearoff=False)
        self.add_cascade(label="View", menu=ViewMenu)
        Show = Menu(self, tearoff=False)
        self.master.ShowVars = {}
        for priority in ("hight", "medium", "low"):
            self.master.ShowVars[priority] = IntVar()
            self.master.ShowVars[priority].set(1)
            Show.add_checkbutton(
                label=priority, variable=self.master.ShowVars[priority],
                onvalue=1, offvalue=0, command=self.master.MainFrame.ShowTasks)
        ViewMenu.add_cascade(label="Show...", menu=Show)
        Sort = Menu(self, tearoff=False)
        self.master.SortingElement = IntVar()
        self.master.SortingElement.set(0)
        SortChoices = ("Old", "New", "Tag", "Due date")
        for e in SortChoices:    
            Sort.add_radiobutton(
                label=e, variable=self.master.SortingElement, 
                value=SortChoices.index(e), command=self.master.MainFrame.ShowTasks)
        ViewMenu.add_cascade(label="Order by...", menu=Sort)
        ViewMenu.add_separator() # séparateur
        ViewMenu.add_command(
            label="Reset all", command=self.ResetView)

    # fonctions du menu déroulant File
    def OpenDatabase(self, msg=True, path=""):
        """
        Dialogue pour ouverture de base de donnée
        msg : bool (indique si l'ouverture doit être discrète ou non et si on doit déconnecter le serveur)
        path : str (optionnel, si fourni, la fonction ne demandera pas le chemin à nouveau)
        """
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
            self.master.EntryFrame = None
        if path == "":
            path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data",
                                            title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path != None and path != "":
            try:
                self.master.Db = DbM(path)
                self.master.title(f"Productivity App v{__version__} : {path}")
                if msg:
                    self.SyncDatabase()  # affichage tâches
                    print(f"Ouverture DB réussie : {path}")
                    msgbox.showinfo("Ouverture database",
                                    f"Ouverture du fichier {path} réussie")
            except Exception as e:
                print(f"Ouverture DB échouée : {e}")
                if msg:
                    msgbox.showerror("Ouverture database",
                                     f"Ouverture database échouée : {e}")
        else:
            print("Ouverture DB annulée")
            if msg:
                msgbox.showinfo("Ouverture database",
                                 "Ouverture database annulée")

    def CreateDatabase(self, msg=True):
        """
        Dialogue pour ouverture d'une nouvelle base de donnée
        msg : bool (indique si la création doit être discrète ou non et si on doit déconnecter le serveur)
        SORTIE : (exitcode: int, path: str)
        """
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
            self.master.EntryFrame = None
        if self.master.Server != None:
            self.ServerDisconnect(False)
        path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data",
                                          title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if os.path.exists(path):  # file already exists
            return (0, path)
        if path != None and path != "":
            if path[:-4] != ".csv" and (platform == "win32" or platform == "win64"):
                path += ".csv"
            try:
                # création d'un nouveau fichier CSV
                self.master.Db = DbM(path, "x+")
                # Ouverture fichier
                self.master.Db = DbM(path)
                # Ajout des labels de colonne
                self.master.Db.Add(self.master.DefaultLabel)
                self.master.title(f"Productivity App v{__version__} : {path}")
                print(f"Création DB réussie : {path}")
                if msg:
                    if __name__ != '__main__':  # désactivé lors d'un test individuel
                        self.SyncDatabase()  # affichage tâches
                    msgbox.showinfo("Création database",
                                    "Création et ouverture du fichier réussie")
                return (1, path)
            except Exception as e:
                print(f"Création DB échouée {e}")
                if msg:
                    msgbox.showerror("Création database",
                                     f"Création database échouée {e}")
                return (0, path)

        else:
            print("Création DB annulée")
            if msg:
                msgbox.showinfo("Création database",
                                 "Création database annulée")
            return (0, path)

    def SyncDatabase(self):
        """
        Sous-fonction appellée par OpenDatabase et CreateDatabase.

        Permet d'afficher les tâches contenues dans le fichier CSV ouvert
        """
        self.master.MainFrame.ReaderIndex = 0
        self.master.MainFrame.Tasks = self.master.Db.GetTasks()
        self.entryconfig("Web", state=DISABLED)
        #print(f"Tasks : {self.master.MainFrame.Tasks}")
        self.master.MainFrame.ShowTasks()
        print("Synchronisation réussie")

    def CloseDatabase(self, msg=True):
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
                self.master.MainFrame.UnpackTasks()  # Supprime les tâches
                self.master.NavBar.CreateWidgets()  # Réinitialise les widgets de NavBar
                # Réinitialise le titre de MainFrame
                self.master.MainFrame['text'] = "MainFrame"
                self.entryconfig("Web", state=NORMAL)
                self.master.title(
                    f"Productivity App v{__version__} : Pas de base de donnée ouverte")
                print("DB fermée")
                if msg:
                    msgbox.showinfo("Fermeture database",
                                    "Fermeture du fichier réussie")
            except Exception as e:
                print("Echec fermeture :",e)
                if msg:
                    msgbox.showerror("Fermeture database",
                                     f"Fermeture database échouée : {e}")

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
                                f"Sauvegarde du fichier réussie {path}")
            else:
                print("Sauvegarde DB annulée")
                msgbox.showinfo("Sauvegarde database",
                                 "Sauvegarde database annulée")

    # fonctions du menu déroulant Web
    def ServerConnect(self):
        """
        Dialogue pour connexion à un serveur web
        """
        if self.master.Server != None:  # déjà connecté à un serveur
            msgbox.showinfo("Login Serveur",
                            f"Vous êtes déjà connectés au serveur {self.master.Server.adress}")
        else:
            if self.master.EntryFrame != None:
                self.master.EntryFrame.destroy()
                self.master.EntryFrame = None
            self.master.EntryFrame = EntryFrame(
                self.master.MainFrame, "adress")

    def ServerLogin(self):
        """
        Dialogue pour identification d'un compte dans le serveur
        """
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Login Serveur",
                            "Vous n'êtes pas connecté à un serveur")
        elif self.master.Server.Account != None:
            msgbox.showinfo("Login Serveur",
                            f"Vous êtes déjà connectés au compte {self.master.Server.Account}\nVeuilez vous déconnecter avant de vous reconnecter")
        else:
            if self.master.EntryFrame != None:
                self.master.EntryFrame.destroy()
                self.master.EntryFrame = None
            self.master.EntryFrame = EntryFrame(
                self.master.MainFrame, "login")

    def ServerLogout(self, msg=True):
        """
        Permet de se déconnecter de son compte
        msg : bool (indique si la déconnexion doit être discrète ou non)
        """
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Logout Serveur",
                            "Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None:  # Pas de compte connecté
            msgbox.showinfo("Logout Serveur",
                            "Vous n'êtes pas connectés à un compte")
        else:
            if self.master.EntryFrame != None:
                self.master.EntryFrame.destroy()
            self.master.MainFrame.UnpackTasks()  # Supprime les tâches
            self.master.NavBar.CreateWidgets()  # Réinitialise les widgets de NavBar
            self.entryconfig("File", state=NORMAL)
            # Réinitialise le titre de MainFrame
            self.master.MainFrame['text'] = "MainFrame"
            oldaccount = self.master.Server.Account
            self.master.Server.Account = None
            self.master.Server.session.close()  # fermeture session
            self.master.title(
                f"Productivity App v{__version__} : {self.master.Server.adress} : non identifié")
            if msg:
                msgbox.showinfo("Login Serveur",
                                f"Déconnecté du compte {oldaccount}")
            print("Déconnecté du compte")

    def ServerSignup(self):
        """
        dialogue (EntryFrame) permettant de créer un compte
        """
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Signup Serveur",
                            "Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account != None:
            msgbox.showinfo("Signup Serveur",
                            f"Vous êtes déjà connectés au compte {self.master.Server.Account}\nVeuilez vous déconnecter avant d'en créer un nouveau")
        else:
            if self.master.EntryFrame != None:
                self.master.EntryFrame.destroy()
                self.master.EntryFrame = None
            self.master.EntryFrame = EntryFrame(
                self.master.MainFrame, "signup")
                
    def ServerDisconnect(self, msg=True):
        """
        Déconnexion d'un serveur web
        msg : bool (indique si la fermeture doit être discrète ou non)
        """
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Déconnexion Serveur",
                            "Vous n'êtes pas connectés à un serveur")
        else:
            if self.master.Server.Account != None:
                self.ServerLogout(False)
            self.entryconfig("File", state=NORMAL)
            oldserver = self.master.Server.adress
            self.master.Server = None
            self.master.title(
                f"Productivity App v{__version__} : Pas de base de donnée ouverte")
            print("Déconnecté du serveur")
            if msg:
                msgbox.showinfo("Déconnexion Serveur",
                                f"Déconnecté du serveur {oldserver}")

    def ServerExtract(self):
        """
        Permet d'extraire la base de donnée dans un fichier CSV
        """
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Extract Database",
                            "Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None:  # Pas de compte connecté
            msgbox.showinfo("Extract Database",
                            "Vous n'êtes pas connectés à un compte")
        else:
            try:
                TaskList = self.master.Server.GetData()
                #print(f"Tasks : {TaskList}")
                (exitcode, path) = self.CreateDatabase(False)
                # création impossible (le fichier existe déjà)
                if not exitcode:
                    print("File already exists... switching to func OpenDatabase")
                    self.OpenDatabase(False, path)
                for task in TaskList:
                    self.master.Db.Add(task)
                self.SyncDatabase()  # affichage des tâches
                print(f"Extraction réussie : {path}")
                msgbox.showinfo("Extract Database",
                                f"Extraction réussie dans {path}")
            except Exception as e:
                print("Echec de l'extraction")
                msgbox.showerror(
                    "Extract Database", f"La base de donnée n'a pas pu être extraite : {e}")

    def ServerImport(self):
        """
        Permet d'ajouter des tâches au serveur depuis un fichier CSV
        """
        

    # fonction du menu déroulant View
    def ResetView(self):
        """
        Commande permettant de réinitialiser la vue du reader (tout afficher, dans l'ordre d'ajout, plus vieux au plus récent)
        """
        self.master.SortingElement.set(0)
        for var in self.master.ShowVars.values():
            var.set(1)
        self.master.MainFrame.ShowTasks()



if __name__ == '__main__':  # test affichage
    from MainFrame import *
    ShowVersion()  # affichage info prog

    root = Tk()
    root.DefaultLabel = DefaultLabel
    root.title("Test Menu")
    root.geometry("{}x{}".format(x, y))
    # setup test
    root.MainFrame = MainFrame(root)
    root.Db = None
    root.Server = None
    root.EntryFrame = None
    Menu = MenuBar(root)
    root.config(menu=Menu)
    root.mainloop()
