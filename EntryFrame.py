from tkinter import *
from tkinter import ttk
from Global import __VERSION__, __AUTHOR__, JMOIS, CDATE  # variables globales
from tkinter import messagebox as msgbox
# permet d'exécuter des fonctions avec arguments avec des widgets tk
from functools import partial
from WebHandler import WebInterface  # Classe d'interfacage avec un serveur web


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
                         relief=SOLID, text="EntryFrame", foreground="white")
        self.master = master
        if purpose == "login":
            self.LoginFrame()
        elif purpose == "signup":
            self.SignupFrame()
        elif purpose == "adress":
            self.AdressFrame()
        elif purpose == "task":
            self.TaskFrame()
        self.pack(anchor="nw", pady=5, padx=20, expand=True)

    def LoginFrame(self):
        """
        Widgets de frame permettant de se connecter à un compte existant
        """
        # Création variables des entrées
        iD = StringVar()
        passwd = StringVar()

        def LoginAttempt(iD, passwd):
            try:
                self.master.master.Server.login(
                    iD.get(), passwd.get(), self.master.master.Server.adress+"/login")
                self.master.master.title(
                    f"Productivity App v{__VERSION__} : {self.master.master.Server.adress} : {iD.get()}")
                msgbox.showinfo("login Serveur",
                                f"Connexion au compte {iD.get()} réussie")
                self.ServerSync()
                self.destroy()
            except Exception as e:
                self.master.master.Server.Account = None
                print(f"Echec login au compte {iD.get()}")
                msgbox.showerror(
                    "login Serveur", f"Echec de la connexion, veuillez réessayer : {e}")

        self["text"] = "Connexion à un compte"
        # Création widgets
        Label(self, text="email :", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="password :", font=(17), background=self["background"], foreground="white"
              ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self, text="login", command=partial(LoginAttempt, iD, passwd), width=20
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
                self.master.master.Server.sign_up(iD.get(), passwd.get(
                ), name.get(), self.master.master.Server.adress+"/signup")
                self.master.master.title(
                    f"Productivity App v{__VERSION__} : {self.master.master.Server.adress} : {iD.get()}")
                msgbox.showinfo("sign_up Serveur",
                                f"Création du compte {iD.get()} réussie")
                self.ServerSync()
                self.destroy()
            except Exception as e:
                self.master.master.Server.Account = None
                print(f"Echec signup compte {iD.get()}")
                msgbox.showerror(
                    "sign_up Serveur", f"Echec de la création du compte, veuillez réessayer : {e}")

        self["text"] = "Création d'un compte"
        # Création widgets
        Label(self, text="email :", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="name :", font=(17), background=self["background"], foreground="white"
              ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="password :", font=(17), background=self["background"], foreground="white"
              ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self, text="sign_up", command=partial(LoginAttempt, iD, name, passwd), width=20
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

    def ServerSync(self):
        """
        Permet de se synchroniser à la base de donnée (après être connecté à un compte)
        """
        self.master.ReaderIndex = 0
        self.master.Tasks = self.master.master.Server.get_data()
        #print(f"Tasks : {self.master.MainFrame.Tasks}")
        if __name__ != '__main__':  # désactivé lors d'un test individuel
            self.master.render_tasks()
        print("Synchronisation réussie")

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
                    f"Productivity App v{__VERSION__} : {adresse} : Non identifié")
                self.master.master.Menu.entryconfig("File", state=DISABLED)
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
        ttk.Button(self, text="Cancel", command=self.destroy, width=20
                   ).grid(row=1, column=0, padx=10, pady=10)
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
        self.dates = self.CreateDateList(CDATE)
        taskdate.set(CDATE)  # assignation taskdate à la date d'aujourd'hui

        def GetTask(task, taskdate, priority, tag):
            try:
                if self.master.master.Server != None:  # connecté à un serveur
                    print("Ajout de la tâche au serveur...")
                    newtask = {
                        "goal": "addElement",
                        "task": task.get(),
                        "date": taskdate.get(),
                        "priority": priority.get(),
                        "tag": tag.get(),
                        "status": "enable"}
                    print("Tâche :", newtask)
                    self.master.master.Server.add(newtask)
                    print("Synchronisation des modifications...")
                    # mise à jour liste des tâches
                    self.master.Tasks = self.master.master.Server.get_data()
                    # mise à jour index (pour montrer la nouvelle tâche)
                    self.master.ReaderIndex = (len(self.master.Tasks)-self.master.update_max_aff()
                                      if len(self.master.Tasks)-self.master.update_max_aff() >= 0 else 0)  # mise à jour index (pour montrer la nouvelle tâche)
                    self.master.render_tasks()  # mise à jour lecteur

                elif self.master.master.File != None:  # base de donnée CSV ouverte
                    newtask = [(str(int(self.master.Tasks[-1][0])+1) if self.master.Tasks else "0"),
                               (self.master.Tasks[-1][1]
                                if self.master.Tasks else "anonymous"),
                               task.get(), taskdate.get(), priority.get(), "enable", tag.get()]
                    print("Tâche :", newtask)
                    print("Ajout de la tâche au fichier CSV...")
                    self.master.master.File.add(newtask)
                    print("Synchronisation des modifications...")
                    self.master.Tasks = self.master.master.File.get_tasks()  # mise à jour liste des tâches
                    self.master.ReaderIndex = (len(self.master.Tasks)-self.master.update_max_aff()
                                      if len(self.master.Tasks)-self.master.update_max_aff() >= 0 else 0)  # mise à jour index (pour montrer la nouvelle tâche)
                    self.master.render_tasks()  # mise à jour lecteur

                # Erreur : rien d'ouvert (normalement impossible en conditions normales)
                else:
                    print("Aucune BDD ouverte, ajout d'une tâche impossible")
                    msgbox.showerror("Ajout d'une tâche",
                                     f"Echec de l'ajout de la tâche {task.get()} \nAucune base de donnée n'est ouverte")
                self.destroy()
            except Exception as e:
                self.master.task = None
                print(
                    f"Echec de l'ajout de la tâche : {task.get()} : \n-->{e}")

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
        ttk.Button(self, text="Cancel", command=self.master.render_tasks, width=20
                   ).grid(row=0, column=4, padx=10, pady=10)
        ttk.Button(self, text="Confirm", command=partial(GetTask, task, taskdate, priority, tag), width=20
                   ).grid(row=1, column=4, padx=10, pady=10)
        taskEntry = ttk.Entry(self, textvariable=task, width=20,
                              background=self["background"])
        dateBox = ttk.Combobox(self, textvariable=taskdate, width=15,
                               background=self["background"], state="readonly",
                               values=self.dates)
        priorityBox = ttk.Combobox(self, textvariable=priority, width=15,
                                   background=self["background"], state="readonly",
                                   values=["hight", "medium", "low"])
        tagEntry = ttk.Entry(self, textvariable=tag, width=15,
                             background=self["background"])
        taskEntry.grid(row=1, column=0, padx=10, pady=10)
        dateBox.grid(row=1, column=1, padx=10, pady=10)
        priorityBox.grid(row=1, column=2, padx=10, pady=10)
        tagEntry.grid(row=1, column=3, padx=10, pady=10)

    def CreateDateList(self, cdate):
        """
        retourne une liste des dates dans le format AAAA-MM-JJ sur 30 jours inclus avec cdate
        """
        return [cdate[:-2]+(str(int(cdate[-2:])+i) if int(cdate[-2:])+i > 9 else cdate[-2]+str(int(cdate[-1])+i))  # création de la liste des dates sur un mois
                 for i in range(JMOIS[int(cdate[5:7])-1]-int(cdate[-2:])+1)]+[
            cdate[:6]+str(int(cdate[6])+1)+cdate[7:-2] + \
            ("0"+str(i) if i < 10 else str(i))
            if int(cdate[6])+1 <= 12
            else cdate[:6]+"1"+cdate[7:-2]+("0"+str(i) if i < 10 else str(i))
            for i in range(1, int(cdate[-2:])+1)]


if __name__ == '__main__':
    print("Le test d'EntryFrame se fait via celui du Menu")
