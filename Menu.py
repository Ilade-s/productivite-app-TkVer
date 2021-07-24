from tkinter import *
from tkinter import filedialog as fldialog  # Choix de fichier etc...
# Messages d'information ou d'avertissement
from tkinter import messagebox as msgbox
import os  # Pour trouver le répertoire courant (os.getcwd)
from DatabaseHandler import CsvHandler as DbM  # Gestion base de donnée
# variables globales
from Global import __VERSION__, show_version, platform, LABELS, x, y
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
        self.create_file_menu() # Menu File
        self.create_web_menu() # Menu Web
        self.create_view_menu() # Menu View
        self.create_graphs_menu() # Menu Graphs
        # ajout about
        self.add_command(
            label="About", command=lambda: msgbox.showinfo("About",
                    f"Productivity App v{__VERSION__}\nMade by Merlet Raphaël, 2021 \
                    \nSource : https://github.com/Ilade-s/productivite-app-TkVer \
                    \nServer side (optionnal) : https://github.com/Tifiloow/productivite-app \
                    \nAssets : https://feathericons.com/"))

    def create_file_menu(self):
        FileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=FileMenu)
        FileMenu.add_command(
            label="New...", command=self.create_file)
        FileMenu.add_command(
            label="Open...", command=self.open_file)
        FileMenu.add_separator()  # séparateur
        FileMenu.add_command(
            label="Save a copy...", command=self.save_new_file)
        FileMenu.add_command(
            label="Close database", command=self.close_file)

    def create_web_menu(self):
        self.WebMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Web", menu=self.WebMenu)
        self.WebMenu.add_command(
            label="Connect to server", command=self.server_connect)
        self.WebMenu.add_command(
            label="Login", command=self.server_login)
        self.WebMenu.add_command(
            label="Signup", command=self.server_signup)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Disconnect", command=self.server_disconnect)
        self.WebMenu.add_command(
            label="Logout", command=self.server_logout)
        self.WebMenu.add_separator()  # séparateur
        self.WebMenu.add_command(
            label="Extract database to csv", command=self.server_extract_CSV)
        self.WebMenu.add_command(
            label="add tasks from csv", command=self.server_import_CSV)

    def create_view_menu(self):
        ViewMenu = Menu(self, tearoff=False)
        self.add_cascade(label="View", menu=ViewMenu)
        Show = Menu(self, tearoff=False)
        self.master.ShowVars = {}
        for priority in ("hight", "medium", "low"):
            self.master.ShowVars[priority] = IntVar()
            self.master.ShowVars[priority].set(1)
            Show.add_checkbutton(
                label=priority, variable=self.master.ShowVars[priority],
                onvalue=1, offvalue=0, command=self.master.MainFrame.render_tasks)
        ViewMenu.add_cascade(label="Show...", menu=Show)
        Sort = Menu(self, tearoff=False)
        self.master.SortingElement = IntVar()
        self.master.SortingElement.set(0)
        SortChoices = ("Old", "New", "Tag", "Due date")
        for e in SortChoices:    
            Sort.add_radiobutton(
                label=e, variable=self.master.SortingElement, 
                value=SortChoices.index(e), command=self.master.MainFrame.render_tasks)
        ViewMenu.add_cascade(label="Order by...", menu=Sort)
        ViewMenu.add_separator() # séparateur
        ViewMenu.add_command(
            label="Reset all", command=self.reset_view)

    def create_graphs_menu(self):
        GraphMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Graphs", menu=GraphMenu)

    # fonctions du menu déroulant File
    def open_file(self, msg=True, path=""):
        """
        Dialogue pour ouverture de base de donnée
        msg : bool (indique si l'ouverture doit être discrète ou non et si on doit déconnecter le serveur)
        path : str (optionnel, si fourni, la fonction ne demandera pas le chemin à nouveau)
        """
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
            self.master.EntryFrame = None
        if path == "":
            path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data", defaultextension=".csv",
                                            title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if path != None and path != "":
            try:
                self.master.File = DbM(path)
                self.master.title(f"Productivity App v{__VERSION__} : {path}")
                if msg:
                    self.show_file()  # affichage tâches
                    print(f"Ouverture DB réussie : {path}")
                    msgbox.showinfo("Ouverture database",
                                    f"Ouverture du fichier {path} réussie")
            except Exception as e:
                print(f"Ouverture DB échouée : {e}")
                if msg:
                    msgbox.showerror("Ouverture database",
                                     f"Ouverture database échouée : {e}")
                return e
        else:
            print("Ouverture DB annulée")
            if msg:
                msgbox.showinfo("Ouverture database",
                                 "Ouverture database annulée")

    def create_file(self, msg=True):
        """
        Dialogue pour ouverture d'une nouvelle base de donnée
        msg : bool (indique si la création doit être discrète ou non et si on doit déconnecter le serveur)
        SORTIE : (exitcode: int, path: str)
        """
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
            self.master.EntryFrame = None
        path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data", defaultextension=".csv",
                                          title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
        if os.path.exists(path):  # file already exists
            return (0, path)
        if path != None and path != "":
            try:
                # création d'un nouveau fichier CSV
                self.master.File = DbM(path, "x+")
                # Ouverture fichier
                self.master.File = DbM(path)
                # Ajout des labels de colonne
                self.master.File.add(LABELS)
                self.master.title(f"Productivity App v{__VERSION__} : {path}")
                print(f"Création DB réussie : {path}")
                if msg:
                    if __name__ != '__main__':  # désactivé lors d'un test individuel
                        self.show_file()  # affichage tâches
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

    def show_file(self):
        """
        Sous-fonction appellée par open_file et create_file.
        """
        self.master.MainFrame.ReaderIndex = 0
        self.master.MainFrame.Tasks = self.master.File.get_tasks()
        self.entryconfig("Web", state=DISABLED)
        #print(f"Tasks : {self.master.MainFrame.Tasks}")
        self.master.MainFrame.render_tasks()
        print("Synchronisation réussie")

    def close_file(self, msg=True):
        """
        Fermeture de la base de donnée (si il y en a une d'ouverte)
        msg : bool (indique si la fermeture doit être discrète ou non)
        """
        if self.master.File == None:
            msgbox.showinfo("Fermeture database",
                            "Il n'y a pas de base de donnée ouverte")
        else:
            try:
                self.master.File.file.close()
                self.master.File = None
                self.master.MainFrame.unpack_tasks()  # Supprime les tâches
                self.master.NavBar.create_widgets()  # Réinitialise les widgets de NavBar
                # Réinitialise le titre de MainFrame
                self.master.MainFrame['text'] = "MainFrame"
                self.entryconfig("Web", state=NORMAL)
                self.master.title(
                    f"Productivity App v{__VERSION__} : Pas de base de donnée ouverte")
                print("DB fermée")
                if msg:
                    msgbox.showinfo("Fermeture database",
                                    "Fermeture du fichier réussie")
            except Exception as e:
                print("Echec fermeture :",e)
                if msg:
                    msgbox.showerror("Fermeture database",
                                     f"Fermeture database échouée : {e}")

    def save_new_file(self):
        if self.master.File == None:
            msgbox.showinfo("Sauvegarde database",
                            "Il n'y a pas de base de donnée ouverte")                   
        else:
            path = fldialog.asksaveasfilename(initialdir=f"{os.getcwd()}/Data",
                                              title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
            if path[-4:] != ".csv" and (platform == "win32" or platform == "win64"):
                path += ".csv"
            if os.path.exists(path):  # file already exists
                print("Sauvegarde DB impossible : fichier déjà existant")
                msgbox.showerror("Sauvegarde database",
                                 "Sauvegarde database impossible : fichier déjà existant")
            elif path != None:
                NewFile = DbM(path, "x+")
                NewFile = DbM(path)
                self.master.File.update_reader()
                for row in self.master.File.Data:
                    NewFile.add(row)
                print(f"Sauvegarde DB réussie : {path}")
                msgbox.showinfo("Sauvegarde database",
                                f"Sauvegarde du fichier réussie {path}")
            else:
                print("Sauvegarde DB annulée")
                msgbox.showinfo("Sauvegarde database",
                                 "Sauvegarde database annulée")

    # fonctions du menu déroulant Web
    def server_connect(self):
        if self.master.Server != None:  # déjà connecté à un serveur
            msgbox.showinfo("Login Serveur",
                            f"Vous êtes déjà connectés au serveur {self.master.Server.adress}")
        else:
            if self.master.EntryFrame != None:
                self.master.EntryFrame.destroy()
                self.master.EntryFrame = None
            self.master.EntryFrame = EntryFrame(
                self.master.MainFrame, "adress")

    def server_login(self):
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

    def server_logout(self, msg=True):
        """
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
            self.master.MainFrame.unpack_tasks()  # Supprime les tâches
            self.master.NavBar.create_widgets()  # Réinitialise les widgets de NavBar
            self.entryconfig("File", state=NORMAL)
            # Réinitialise le titre de MainFrame
            self.master.MainFrame['text'] = "MainFrame"
            oldaccount = self.master.Server.Account
            self.master.Server.Account = None
            self.master.Server.session.close()  # fermeture session
            self.master.title(
                f"Productivity App v{__VERSION__} : {self.master.Server.adress} : non identifié")
            if msg:
                msgbox.showinfo("Login Serveur",
                                f"Déconnecté du compte {oldaccount}")
            print("Déconnecté du compte")

    def server_signup(self):
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
                
    def server_disconnect(self, msg=True):
        """
        msg : bool (indique si la fermeture doit être discrète ou non)
        """
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Déconnexion Serveur",
                            "Vous n'êtes pas connectés à un serveur")
        else:
            if self.master.Server.Account != None:
                self.server_logout(False)
            self.entryconfig("File", state=NORMAL)
            oldserver = self.master.Server.adress
            self.master.Server = None
            self.master.title(
                f"Productivity App v{__VERSION__} : Pas de base de donnée ouverte")
            print("Déconnecté du serveur")
            if msg:
                msgbox.showinfo("Déconnexion Serveur",
                                f"Déconnecté du serveur {oldserver}")

    def server_extract_CSV(self):
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Extract Database",
                            "Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None:  # Pas de compte connecté
            msgbox.showinfo("Extract Database",
                            "Vous n'êtes pas connectés à un compte")
        else:
            try:
                TaskList = self.master.Server.get_data()
                self.server_disconnect(False)
                (exitcode, path) = self.create_file(False)
                # création impossible (le fichier existe déjà)
                if not exitcode:
                    print("File already exists... switching to func open_file")
                    self.open_file(False, path)
                for task in TaskList:
                    self.master.File.add(task)
                self.show_file()  # affichage des tâches
                print(f"Extraction réussie : {path}")
                msgbox.showinfo("Extract Database",
                                f"Extraction réussie dans {path}")
            except Exception as e:
                print("Echec de l'extraction")
                msgbox.showerror(
                    "Extract Database", f"La base de donnée n'a pas pu être extraite : {e}")

    def server_import_CSV(self):
        if self.master.Server == None:  # Pas de serveur ouvert
            msgbox.showinfo("Import Database",
                            "Vous n'êtes pas connectés à un serveur")
        elif self.master.Server.Account == None:  # Pas de compte connecté
            msgbox.showinfo("Import Database",
                            "Vous n'êtes pas connectés à un compte")
        else:
            try:
                # ouverture du fichier
                path = fldialog.askopenfilename(initialdir=f"{os.getcwd()}/Data", defaultextension=".csv",
                                              title="Base de donnée CSV", filetypes=(("CSV file", "*.csv"), ("all files", "*.*")))
                file = DbM(path)
                fileData = file.get_tasks()
                # ajout de chaque tâche
                for task in fileData: 
                    newtask = { # création dict tâche à ajouter
                        "goal": "addElement",
                        "task": task[LABELS.index("name")],
                        "date": task[LABELS.index("date")],
                        "priority": task[LABELS.index("priority")],
                        "tag": task[LABELS.index("tag")],
                        "status": task[LABELS.index("status")]}
                    self.master.Server.add(newtask)
                # mise à jour reader
                self.master.MainFrame.Tasks = self.master.Server.get_data()
                self.master.MainFrame.render_tasks()
                print(f"Importation réussie : {path}")
                msgbox.showinfo("Import Database",
                                f"Importation réussie depuis {path}")
            except Exception as e:
                print("Echec de l'importation")
                msgbox.showerror(
                    "Import Database", f"La base de donnée n'a pas pu être importée : {e}")
        
    # fonction du menu déroulant View
    def reset_view(self):
        """
        Commande permettant de réinitialiser la vue du reader (tout afficher, dans l'ordre d'ajout, plus vieux au plus récent)
        """
        self.master.SortingElement.set(0)
        for var in self.master.ShowVars.values():
            var.set(1)
        self.master.MainFrame.render_tasks()
    
    # fonctions du menu déroulant Graphs




if __name__ == '__main__':  # test affichage
    from MainFrame import *
    show_version()  # affichage info prog

    root = Tk()
    root.title("Test Menu")
    root.geometry("{}x{}".format(x, y))
    # setup test
    root.MainFrame = MainFrame(root)
    root.File = None
    root.Server = None
    root.EntryFrame = None
    Menu = MenuBar(root)
    root.config(menu=Menu)
    root.mainloop()
