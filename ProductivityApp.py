"""
Application/Programme de productivité et d'emploi du temps
supporte la connexion au serveur correspondant et l'exportation en CSV
on peut afficher les tâches en se synchronisant au serveur
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
#from tkinter import simpledialog as smpldial  # Demande d'informations simples
import os  # Pour trouver le répertoire courant (os.getcwd)
# permet d'exécuter des fonctions avec arguments avec des widgets tk
from functools import partial
from datetime import date # récupération de la date (ajout de tâche)


class MenuBar(Menu):
    """
    Menu qui s'affiche à gauche dans l'application tkinter

    Affiche les actions possibles en fonction de MainFrame
    """

    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
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
            label="Login", command=self.ServerLogin)
        self.WebMenu.add_command(
            label="Signup", command=self.ServerSignup)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Sync to database", command=self.ServerSync)
        self.WebMenu.add_command(
            label="Extract database to csv", command=self.ServerExtract)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Disconnect", command=self.ServerDisconnect)
        self.WebMenu.add_command(
            label="Logout", command=self.ServerLogout)

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
        if self.master.Server != None:
            self.ServerDisconnect(False)
        if path == "":
            path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data",
                                            title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path != None and path != "":
            try:
                self.master.Db = DbM(path)
                self.master.title(f"Productivity App v{__version__} : {path}")
                print(f"Ouverture DB réussie : {path}")
                if msg:
                    self.SyncDatabase() # affichage tâches
                    msgbox.showinfo("Ouverture database",
                                    f"Ouverture du fichier {path} réussie")
            except Exception as e:
                print("Création DB échouée")
                if msg:
                    msgbox.showerror("Ouverture database",
                                    "Ouverture database échouée")
        else:
            print("Ouverture DB annulée")
            if msg:
                msgbox.showerror("Ouverture database",
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
            if path[:-4] != ".csv":
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
                    self.SyncDatabase() # affichage tâches
                    msgbox.showinfo("Création database",
                                    "Création et ouverture du fichier réussie")
                return (1, path)
            except Exception as e:
                print("Création DB échouée")
                if msg:
                    msgbox.showerror("Création database",
                                    "Création database échouée")
                return (0, path)

        else:
            print("Création DB annulée")
            if msg:
                msgbox.showerror("Création database",
                                 "Création database échouée/annulée")
            return (0, path)
    
    def SyncDatabase(self):
        """
        Sous-fonction appellée par OpenDatabase et CreateDatabase.

        Permet d'afficher les tâches contenues dans le fichier CSV ouvert
        """
        self.master.MainFrame.Tasks = self.master.Db.GetTasks()
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
                self.master.SubFrame.CreateWidgets() # Réinitialise les widgets de SubFrame
                self.master.MainFrame['text'] = "MainFrame" # Réinitialise le titre de MainFrame
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
        if self.master.Server != None:  # déjà connecté à un serveur
            msgbox.showinfo("Login Serveur",
                            f"Vous êtes déjà connectés au serveur {self.master.Server.adress}")
        else:
            if self.master.Db != None:
                self.CloseDatabase(False)
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
            self.master.MainFrame.UnpackTasks()  # Supprime les tâches
            self.master.SubFrame.CreateWidgets() # Réinitialise les widgets de SubFrame
            self.master.MainFrame['text'] = "MainFrame" # Réinitialise le titre de MainFrame
            oldaccount = self.master.Server.Account
            self.master.Server.Account = None
            self.master.Server.session.close()  # fermeture session
            self.master.title(
                f"Productivity App v{__version__} : {self.master.Server.adress} : non identifié")
            if msg:
                msgbox.showinfo("Login Serveur",
                                f"Déconnecté du compte {oldaccount}")
            print("Déconnecté du compte")

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
            if self.master.EntryFrame != None:
                self.master.EntryFrame.destroy()
            oldserver = self.master.Server.adress
            self.master.Server = None
            self.master.title(
                f"Productivity App v{__version__} : Pas de base de donnée ouverte")
            print("Déconnecté du serveur")
            if msg:
                msgbox.showinfo("Déconnexion Serveur",
                                f"Déconnecté du serveur {oldserver}")

    def ServerSync(self):
        """
        Permet de se synchroniser à la base de donnée (après être connecté à un compte)
        """
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Sync Database",
                            "Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None:  # Pas de compte connecté
            msgbox.showinfo("Sync Database",
                            "Vous n'êtes pas connectés à un compte")
        else:
            try:
                self.master.MainFrame.Tasks = self.master.Server.GetData()
                #print(f"Tasks : {self.master.MainFrame.Tasks}")
                self.master.MainFrame.ShowTasks()
                print("Synchronisation réussie")
                msgbox.showinfo("Sync Database", "Synchronisation réussie")
            except Exception as e:
                print("Echec de la synchronisation")
                msgbox.showerror(
                    "Sync Database", f"La base de donnée n'a pas pu être synchronisée : {e}")

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
                if not exitcode:  # création impossible (le fichier existe déjà)
                    print("File already exists... switching to func OpenDatabase")
                    self.OpenDatabase(False, path)
                for task in TaskList:
                    self.master.Db.Add(task)
                self.SyncDatabase() # affichage des tâches
                print(f"Extraction réussie : {path}")
                msgbox.showinfo("Extract Database", f"Extraction réussie dans {path}")
            except Exception as e:
                print("Echec de l'extraction")
                msgbox.showerror(
                    "Extract Database", f"La base de donnée n'a pas pu être extraite : {e}")

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


class MainFrame(LabelFrame):
    """
    Partie principale de l'application qui permet d'afficher les tâches et les demandes d'inputs
    """

    def __init__(self, master) -> None:
        self.master = master
        self.Tasks = []
        self.ShownTasks = []
        self.Ci = 0
        # nombre de tâches affichables sans clippage (dynamique)
        self.maxAff = 7
        super().__init__(master, background="#292D3E",
                         relief=SOLID, text="MainFrame", foreground="white")
        #        height=self.master.geo[1]*.75, width=self.master.geo[0]*.75)
        #self.grid(row=0, column=1, rowspan=1, columnspan=1, sticky='nesw')
        self.place(relx=.25, rely=0, relheight=.75, relwidth=.75)

    def ShowTasks(self):
        """
        Affiche les tâches
        """
        self['text'] = "Liste des tâches"
        # Unpack tâches précedemment affichées
        if self.ShownTasks != []:
            for task in self.ShownTasks:
                task.destroy()

        # création et affichage des widgets
        self.StateTasks = [IntVar() for i in range(
            len(self.Tasks[self.Ci:self.Ci+self.maxAff]))]

        self.ShownTasks = [ttk.Checkbutton(self,
            text=f"{task[2][:60]}... // {task[3]} // {task[4]} // {task[6]}" if len(task[2]) > 60
            else f"{task[2]} // {task[3]} // {task[4]} // {task[6]}", onvalue=1, offvalue=0
            , style="Task.TCheckbutton")
                for task in self.Tasks[self.Ci:self.Ci+self.maxAff]]

        for task in range(len(self.ShownTasks)):
            self.ShownTasks[task]["variable"] = self.StateTasks[task] # assignation variable
            self.ShownTasks[task].pack(anchor="w", padx=20, pady=5) # affichage tâche
        # config style
        s = ttk.Style(self)
        s.configure("Task.TCheckbutton", 
            background="#5B648A", font=(20), anchor="w")
        # Maj état des boutons de SubFrame
        if self.Ci == 0:  # début de la liste des tâches
            self.master.SubFrame.BackButton["state"] = "disabled"
            self.master.SubFrame.NextButton["state"] = "normal"
        # fin de la liste des tâches
        elif self.Ci+self.maxAff >= len(self.Tasks):
            self.master.SubFrame.BackButton["state"] = "normal"
            self.master.SubFrame.NextButton["state"] = "disabled"
        else:  # autre intervalle
            self.master.SubFrame.BackButton["state"] = "normal"
            self.master.SubFrame.NextButton["state"] = "normal"
        self.master.SubFrame.ReaderInfo[
            'text'] = f"{self.Ci+1}-{self.Ci+len(self.ShownTasks)}/{len(self.Tasks)}"

    def UnpackTasks(self):
        """
        Retire toutes les tâches
        """
        for task in self.ShownTasks:
            task.destroy()
        for w in self.master.SubFrame.winfo_children():
            w.destroy()

    def UpdateMaxAff(self):
        """
        Permet de mettre à jour le nombre de tâches affichables sans clippage 
        (et avec un espace pour la Frame d'ajout de tâches)
        """
        # on sait que taille de base = 600*.75 = 450 or on peut y afficher 9 tâches - 2 pour l'espace restant
        # donc yTask = 50 et à la fin on doit retirer 2 au résultat
        CurrentHeight = self.winfo_height()
        #print(f"taille MainFrame : {CurrentHeight}")
        self.maxAff = CurrentHeight//50 - 2
        #print(f"nombre de tâches max : {self.maxAff}")
        # on renvoie ensuite self.maxaff pour SubFrame
        return self.maxAff


class EntryFrame(LabelFrame):
    """
    Frame utilisé pour la récupération d'information textuelles :
        - Récupération d'une adresse web
        - Connexion à un compte
        - Création d'un compte
        - Ajout d'une tâche
    située (packée) dans MainFrame
    """

    def __init__(self, master, purpose="login"):
        """
        Création et affichage de la Frame souhaitée
        master : fenêtre maîtresse (sera MainFrame)
        purpose : str : indique le but de la Frame à afficher (et donc les widgets à ajouter):
            - "login" : fenêtre de connexion avec id et mdp
            - "signup" : fenêtre de création de compte avec id, nom et mdp
            - "adress": fenêtre de récupéation d'une adresse web
            - "task" : bloc de récupération d'infos pour l'ajout d'une tâche
        """
        super().__init__(master, background="#424864",
                         relief=SOLID, text="EntryFrame", foreground="white",)
        self.master = master
        if purpose == "login":
            self.LoginFrame()
        elif purpose == "signup":
            self.SignupFrame()
        elif purpose == "adress":
            self.AdressFrame()
        elif purpose == "task":
            self.TaskFrame()
        self.pack(anchor="nw", pady=5, padx=5, expand=True)

    def LoginFrame(self):
        """
        Widgets de frame permettant de se connecter à un compte existant
        """
        # Création variables des entrées
        iD = StringVar()
        passwd = StringVar()

        def LoginAttempt(iD, passwd):
            try:
                self.master.master.Server.Login(
                    iD.get(), passwd.get(), self.master.master.Server.adress+"/login")
                self.master.master.title(
                    f"Productivity App v{__version__} : {self.master.master.Server.adress} : {iD.get()}")
                msgbox.showinfo("Login Serveur",
                                f"Connexion au compte {iD.get()} réussie")
                self.destroy()
            except Exception as e:
                self.master.master.Server.Account = None
                print(f"Echec login au compte {iD.get()}")
                msgbox.showerror(
                    "Login Serveur", f"Echec de la connexion, veuillez réessayer : {e}")

        self["text"] = "Connexion à un compte"
        # Création widgets
        Label(self, text="email :", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="password :", font=(17), background=self["background"], foreground="white"
              ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self, text="Login", command=partial(LoginAttempt, iD, passwd), width=20
                   ).grid(row=2, column=1, padx=10, pady=10)
        idEntry = ttk.Entry(self, textvariable=iD, width=30,
                            background=self["background"])
        passwdEntry = ttk.Entry(self, textvariable=passwd,
                                width=30, background=self["background"], show="*")
        idEntry.grid(row=0, column=1, padx=10, pady=10)
        passwdEntry.grid(row=1, column=1, padx=10, pady=10)

    def SignupFrame(self):
        """
        Widgets de frame permettant de créer un nouveau compte
        """
        # Création variables des entrées
        iD = StringVar()
        passwd = StringVar()
        name = StringVar()

        def LoginAttempt(iD, name, passwd):
            try:
                self.master.master.Server.Signup(iD.get(), passwd.get(
                ), name.get(), self.master.master.Server.adress+"/signup")
                self.master.master.title(
                    f"Productivity App v{__version__} : {self.master.master.Server.adress} : {iD.get()}")
                msgbox.showinfo("Signup Serveur",
                                f"Création du compte {iD.get()} réussie")
                self.destroy()
            except Exception as e:
                self.master.master.Server.Account = None
                print(f"Echec signup compte {iD.get()}")
                msgbox.showerror(
                    "Signup Serveur", f"Echec de la création, veuillez réessayer : {e}")

        self["text"] = "Création d'un compte"
        # Création widgets
        Label(self, text="email :", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="name :", font=(17), background=self["background"], foreground="white"
              ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="password :", font=(17), background=self["background"], foreground="white"
              ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self, text="Signup", command=partial(LoginAttempt, iD, name, passwd), width=20
                   ).grid(row=3, column=1, padx=10, pady=10)
        idEntry = ttk.Entry(self, textvariable=iD, width=30,
                            background=self["background"])
        nameEntry = ttk.Entry(self, textvariable=name,
                              width=30, background=self["background"])
        passwdEntry = ttk.Entry(self, textvariable=passwd,
                                width=30, background=self["background"], show="*")
        idEntry.grid(row=0, column=1, padx=10, pady=10)
        nameEntry.grid(row=1, column=1, padx=10, pady=10)
        passwdEntry.grid(row=2, column=1, padx=10, pady=10)
    
    def AdressFrame(self):
        """
        Frame permettant de se connecter à un serveur à l'aide de son adresse web
        """
        # Création variables des entrées
        adress = StringVar()

        def ConnexionAttempt(adress):
            adresse = adress.get()
            try:
                self.master.master.Server = WebInterface(adress=adresse)
                print(f"Connecté au serveur : {adresse}")
                self.master.master.title(
                    f"Productivity App v{__version__} : {adresse} : Non identifié")
                msgbox.showinfo(
                    "Connexion serveur", f"Connexion réussie au serveur à l'adresse {adresse}")
                self.destroy()
            except Exception:
                print(f"Connexion au serveur à l'adresse {adresse} échouée")
                msgbox.showerror(
                    "Connexion serveur", f"Connexion au serveur à l'adresse {adresse} échouée")

        self["text"] = "Connexion à un serveur"
        # Création widgets
        Label(self, text="Adresse web :", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self, text="Connect to server", command=partial(ConnexionAttempt, adress), width=20
                   ).grid(row=1, column=1, padx=10, pady=10)
        adressEntry = ttk.Entry(self, textvariable=adress, width=40,
                            background=self["background"])
        adressEntry.grid(row=0, column=1, padx=10, pady=10)
    
    def TaskFrame(self):
        """
        Frame permettant de récupérer les informations nécessaires à l'ajout d'une tâche (sous forme de liste)
        Cette liste sera ensuite ajoutée au fichier CSV ou au serveur selon la connexion active
        """
        # Création variables des entrées
        task = StringVar()
        taskdate = StringVar()
        priority = StringVar()
        priority.set("medium")
        tag = StringVar()
        # création dates sur le mois
        cdate = str(date.today())
        taskdate.set(cdate) # assignation taskdate à la date d'aujourd'hui
        dates = [cdate[:-2]+str(int(cdate[-2:])+i) # bonne chance
                    for i in range(31-int(cdate[-2:]))]+[
                        cdate[:6]+str(int(cdate[6])+1)+cdate[7:-2]+("0"+str(i) if i<10 else str(i)) 
                            if int(cdate[6])+1<=12 
                        else cdate[:6]+"1"+cdate[7:-2]+("0"+str(i) if i<10 else str(i))
                            for i in range(1,int(cdate[-2:])+1)]
        #print(dates)

        def GetTask(task, taskdate, priority, tag):
            try:
                self.task = [task.get(), taskdate.get(), priority.get(), tag.get()]
                # à faire ?
                self.destroy()
            except Exception as e:
                self.master.task = None
                print(f"Echec de l'ajout de la tâche : {task.get()}")

        self["text"] = "Ajout d'une tâche"
        # Création widgets
        Label(self, text="Task", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="n")
        Label(self, text="Due date", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=1, padx=10, pady=10, sticky="n")
        Label(self, text="Priority", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=2, padx=10, pady=10, sticky="n")
        Label(self, text="Tag", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=3, padx=10, pady=10, sticky="n")
        ttk.Button(self, text="Confirm", command=partial(GetTask, task, taskdate, priority, tag), width=20
                   ).grid(row=1, column=4, padx=10, pady=10)
        taskEntry = ttk.Entry(self, textvariable=task, width=20,
                            background=self["background"])
        priorityBox = ttk.Combobox(self, textvariable=priority, width=15,
                            background=self["background"], state="readonly",
                            values=["hight", "medium", "low"])
        dateBox = ttk.Combobox(self, textvariable=taskdate, width=15,
                            background=self["background"], state="readonly",
                            values=dates)
        tagEntry = ttk.Entry(self, textvariable=tag, width=15,
                            background=self["background"])
        taskEntry.grid(row=1, column=0, padx=10, pady=10)
        dateBox.grid(row=1, column=1, padx=10, pady=10)
        priorityBox.grid(row=1, column=2, padx=10, pady=10)
        tagEntry.grid(row=1, column=3, padx=10, pady=10)
        



class ActionFrame(LabelFrame):
    """
    Frame placé à gauche (prenant 1/4 de la longueur) permettant de choisir les actions à effectuer
    """

    def __init__(self, master):
        self.master = master
        super().__init__(master, background="#5B648A",
                         relief=RAISED, text="ActionFrame", foreground="white")
        #    height=self.master.geo[1], width=self.master.geo[0]/4)
        self.CreateWidgets()
        #self.grid(row=0, column=0, rowspan=2, columnspan=1, sticky='nesw')
        self.place(relx=0, rely=0, relheight=1, relwidth=.25)

    def CreateWidgets(self):
        """
        Placement des widgets
        """
        self.addImg = PhotoImage(file="Assets/add-icon.png")
        # ajout widgets
        self.AddButton = ttk.Button(self, text="Ajouter une tâche", image=self.addImg
            , compound=TOP, style="ActionFrame.TButton", command=self.AddTask)
        # config style
        s = ttk.Style(self)
        s.configure("ActionFrame.TButton", borderwidth=5)
        self.AddButton.pack()
    
    def AddTask(self):
        """
        Action déclenchée par le bouton "Ajouter une tâche"
        """
        self.master.EntryFrame = EntryFrame(
                self.master.MainFrame, "task")


class SubFrame(LabelFrame):
    """
    Frame située en dessous de MainFrame servant à changer de page et indiquer la page affichée
    """

    def __init__(self, master) -> None:
        self.master = master
        super().__init__(master, background="#A8B8FF",
                         relief=RAISED, text="SubFrame", foreground="white")
        #        height=self.master.geo[1]*.25, width=self.master.geo[0]*.75)
        self.CreateWidgets()
        #self.grid(row=1, column=1, rowspan=1, columnspan=1, sticky='nesw')
        self.place(relx=.25, rely=.75, relheight=.25, relwidth=.75)

    def CreateWidgets(self):
        """
        Placement des widgets
        """
        self['text'] = "Menu de navigation"
        for w in self.winfo_children():
            w.destroy()
        # config lignes et colonnes
        self.rowconfigure(0, weight=1)
        for i in range(5):
            self.columnconfigure(i, weight=1)
        # importation images
        self.BackImg = PhotoImage(file="Assets/back-arrow.png")
        self.NextImg = PhotoImage(file="Assets/next-arrow.png")
        # ajout des widgets
        self.BackButton = ttk.Button(
            self, text="Previous page", state="disabled", style="SubFrame.TButton"
            , command=self.PreviousPage, image=self.BackImg)
        self.NextButton = ttk.Button(
            self, text="Next page", state="disabled", style="SubFrame.TButton"
            , command=self.NextPage, image=self.NextImg)
        self.ReaderInfo = Label(self, text="..-../..", font=("Arial", 20))
        self.BackButton.grid(row=0, column=1)
        self.NextButton.grid(row=0, column=3)
        self.ReaderInfo.grid(row=0, column=2, ipadx=50, ipady=20)
        # config style boutons
        s = ttk.Style(self)
        s.configure("SubFrame.TButton", font=("Arial", 10))

    def PreviousPage(self):
        """
        Commande appelée par le bouton self.BackButton permettant de revenir à la page précédente 
        (dans l'affichage des tâches)
        """
        affmax = self.master.MainFrame.UpdateMaxAff()  # récupération affmax
        self.master.MainFrame.Ci -= affmax  # maj intervalle des tâches à afficher
        if self.master.MainFrame.Ci < 0:  # afin d'éviter les index négatifs
            self.master.MainFrame.Ci = 0
        self.master.MainFrame.ShowTasks()  # maj affichage

    def NextPage(self):
        """
        Commande appelée par le bouton self.NextButton permettant d'afficher la page suivante
        (dans l'affichage des tâches)
        """
        self.master.MainFrame.Ci += self.master.MainFrame.maxAff  # maj intervalle des tâches à afficher
        self.master.MainFrame.UpdateMaxAff() # maj affichage max
        self.master.MainFrame.ShowTasks()  # maj affichage


class TopLevel(Tk):
    """
    Fenêtre tkinter en elle même, contient les Frames placées en grid
    """

    def __init__(self, x=1200, y=600) -> None:
        """
        Initialisation de la fenêtre
        """
        super().__init__()
        self.DefaultLabel = ["taskID", "userID", "name",
                             "date", "priority", "status", "tag"]
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
    print("===============================================================")
    print(f"Productivity App v{__version__}")
    print(f"Made by {__author__}")
    print("Source : https://github.com/Ilade-s/productivite-app-TkVer")
    print("Server : https://github.com/Tifiloow/productivite-app")
    print("===============================================================")
    # Création fenêtre
    app = TopLevel()
    app.mainloop()


if __name__ == '__main__':  # test
    main()
