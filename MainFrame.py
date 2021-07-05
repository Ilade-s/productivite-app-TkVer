from tkinter import *
from tkinter import ttk
from NavBar import NavBar
from Global import LABELS, ShowVersion, JMOIS
# permet d'exécuter des fonctions avec des paramètres avec un widget tk
from functools import partial
from EntryFrame import *


class MainFrame(LabelFrame):
    """
    Partie principale de l'application qui permet d'afficher les tâches et les demandes d'inputs
    """

    def __init__(self, master) -> None:
        self.master = master
        self.Tasks = []
        self.ShownTasks = []
        self.StateTasks = []
        self.ReaderIndex = 0
        self.AddButton = None
        self.addImg = PhotoImage(file="Assets/add-icon.png")
        # nombre de tâches affichables sans clippage (dynamique)
        self.maxAff = 7
        super().__init__(master, background="#292D3E",
                         relief=SOLID, text="MainFrame", foreground="white")
        self.place(relx=0, rely=0, relheight=.75, relwidth=1)

    def ShowTasks(self):
        """
        Affiche les tâches
        """
        if __name__!='__main__':
            # checks if a database is open, if not, exits the function
            if self.master.File == None and self.master.Server == None:
                return 0
            self.FilterTasks() # filter and sort the task list
            # maj index de lecture après filtrage (si la liste est raccourcie)
            if self.ReaderIndex > len(self.TasksTS):
                self.ReaderIndex = (len(self.TasksTS)-self.UpdateMaxAff()
                            if len(self.TasksTS)-self.UpdateMaxAff() >= 0 else 0)
        else: 
            self.TasksTS = self.Tasks

        self['text'] = "Liste des tâches"
        # Remove and replace task Entryframe
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
        # Unpack tâches précedemment affichées
        if self.ShownTasks:
            for task in self.ShownTasks:
                task.destroy()
        # unpack bouton d'ajout de tâche
        if self.AddButton != None:
            self.AddButton.destroy()
                        
        # création variables à assigner aux tâches si nécessaire (si vide)
        if not self.StateTasks:
            self.StateTasks = [IntVar() for i in range(len(self.Tasks))]
        elif len(self.StateTasks) < len(self.TasksTS):  # nouvelles tâches
            self.StateTasks.extend(
                [IntVar() for i in range(len(self.TasksTS)-len(self.StateTasks))])
        elif len(self.StateTasks) > len(self.TasksTS):  # tâches supprimées
            self.StateTasks = self.StateTasks[:len(self.TasksTS)]

        # création et affichage des widgets
        self.ShownTasks = [TaskFrame(self, task) 
                            for task in self.TasksTS[self.ReaderIndex:self.ReaderIndex+self.maxAff]]

        for task in range(len(self.ShownTasks)):
            # assignation variable et set en fonction de status
            self.StateTasks[self.ReaderIndex+task].set(0 
                if self.TasksTS[task][LABELS.index("status")] == "enable" 
                    else 1)
            self.ShownTasks[task].CheckB["variable"] = self.StateTasks[self.ReaderIndex+task]
            self.ShownTasks[task].taskState = self.StateTasks[self.ReaderIndex+task]
            self.ShownTasks[task].pack(
                anchor="w", padx=20, pady=5, ipadx=self.winfo_width()*.9)  # affichage tâche

        # création bouton d'ajout de tâche
        self.AddTaskButton()
        # Maj état des boutons de NavBar
        self.UpdateNavBar()

    def UpdateNavBar(self):
        if len(self.TasksTS) == 0 or len(self.TasksTS) <= self.maxAff:  # une seule page
            self.master.NavBar.BackButton["state"] = "disabled"
            self.master.NavBar.NextButton["state"] = "disabled"
        elif self.ReaderIndex == 0:  # début de la liste des tâches
            self.master.NavBar.BackButton["state"] = "disabled"
            self.master.NavBar.NextButton["state"] = "normal"
        # fin de la liste des tâches
        elif self.ReaderIndex+self.maxAff >= len(self.TasksTS):
            self.master.NavBar.BackButton["state"] = "normal"
            self.master.NavBar.NextButton["state"] = "disabled"
        else:  # autre intervalle
            self.master.NavBar.BackButton["state"] = "normal"
            self.master.NavBar.NextButton["state"] = "normal"
        self.master.NavBar.ReaderInfo[
            'text'] = f"{self.ReaderIndex+1 if len(self.Tasks) > 0 else 0}-{self.ReaderIndex+len(self.ShownTasks)}/{len(self.TasksTS)} (/{len(self.Tasks)})"

    def FilterTasks(self):
        """
        filtre et trie les tâches de l'attribut self.Tasks selon les choix de l'utilisateur et stocke le résultat dans self.TasksTS (TasksToShow)
        """
        # Filtrage des tâches selon les choix de l'utilisateur
        self.TasksTS = list(filter(
            lambda t: self.master.ShowVars[t[LABELS.index("priority")]].get() == 1,
                                    self.Tasks))
        # Tri des tâches
        # Tri par ordre d'ajout (New ou Old)
        if self.master.SortingElement.get() in (0, 1):
            self.TasksTS.sort(key=lambda x: int(x[0])
                ,reverse=self.master.SortingElement.get())
        # Tri par tag
        elif self.master.SortingElement.get() == 2:
            self.TasksTS.sort(key=lambda x: x[LABELS.index("tag")])
        # Tri par date dûe
        elif self.master.SortingElement.get() == 3:
            self.TasksTS.sort(key=lambda x: int(x[LABELS.index("date")][-2:])+
                int(x[LABELS.index("date")][-5:-3])*JMOIS[int(x[LABELS.index("date")][-5:-3])])

    def AddTaskButton(self):
        """
        Ajoute le bouton "Ajout de tâche" à MainFrame
        """
        self.AddButton = ttk.Button(self, text="Ajouter une tâche",
                                    image=self.addImg, command=self.AddTask)
        self.AddButton.pack(pady=10, padx=20, anchor="w")

    def AddTask(self):
        """
        Action déclenchée par le bouton "Ajouter une tâche"
        """
        self.AddButton.destroy() # retire le bouton pour faire place à l'EntryFrame
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
            self.master.EntryFrame = None
        self.master.EntryFrame = EntryFrame(self, "task")

    def UnpackTasks(self):
        """
        Retire toutes les tâches
        """
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
        for task in self.winfo_children():
            task.destroy()
        for w in self.master.NavBar.winfo_children():
            w.destroy()

    def UpdateMaxAff(self):
        """
        Permet de mettre à jour le nombre de tâches affichables sans clippage 
        (et avec un espace pour la Frame d'ajout de tâches)
        """
        # on sait que taille de base = 600*.75 = 450 or on peut y afficher 9 tâches - 2 pour l'espace restant
        # donc yTask = 50 et à la fin on doit retirer 2 au résultat : 50*nTaches - 2 == yMainFrame
        CurrentHeight = self.winfo_height()
        #print(f"taille MainFrame : {CurrentHeight}")
        self.maxAff = CurrentHeight//50 - 2
        #print(f"nombre de tâches max : {self.maxAff}")
        # on renvoie ensuite self.maxaff pour NavBar
        return self.maxAff
    
class TaskFrame(Frame):
    """
    Template de frame qui sera packée dans MainFrame.

    Contient la tâche en CheckButton à gauche ainsi qu'un bouton à droite permettant de supprimer la tâche (placés en grid)
    """

    def __init__(self, master, task) -> None:
        """
        Constructeur de Frame de tâche

        PARAMETRE : 
            - master : class
                - instance de MainFrame en cours
            - task : list
                - la tâche à afficher
        """
        self.colors = { # couleurs de polices en fonction de la priorité
            'hight': '#3C1414', # rouge sombre
            'medium': '#3E281B', # orange sombre
            'low': '#30482D' # vert sombre
        }
        self.master = master
        self.task = task # liste de tâche
        self.SupprImg = PhotoImage(file="Assets/remove-icon.png") # icône du bouton de supression
        super().__init__(master, background=self.master['background'],
                        relief=SOLID)
        self.CreateWidgets()
    
    def CreateWidgets(self):
        """
        Ajoute les widgets dans la frame
        """
        task = self.task

        def TaskSelected(taskID):
            """
            Action d'un CheckButton de tâche lorsque que l'user interagit avec lui (pour la mettre comme faite ou non)
            param taskID : str : numéro sous forme de string qui peret de retrouver une tâche dans la liste
            """
            #print("Tâche selectionnée :", taskID) # debug
            #print("Etat de la tâche :", ("faite" if self.taskState.get() else "à faire")) # debug
            try:
                if self.master.master.File != None: # fichier CSV ouvert
                    self.master.master.File.Edit(taskID,
                        ("disable" if self.taskState.get() else "enable"))
                    self.master.Tasks = self.master.master.File.GetTasks()

                elif self.master.master.Server != None: # connecté à un serveur
                    self.master.master.Server.Edit(taskID,
                        ("disable" if self.taskState.get() else "enable"))
                    self.master.Tasks = self.master.master.Server.GetData()
                
                print(f"Etat de la tâche {taskID} mis à jour")

            except Exception as e:
                print(f"Echec de l'interaction avec la tâche {taskID} : {e}")
                msgbox.showerror("Interaction avec une tâche",
                    f"Echec de l'interaction avec la tâche {taskID} : {e}") 


        def RemoveTask(taskID):
            """
            Action du bouton qui permet de retirer la tâche du fichier ou du serveur et de mettre à jour MainFrame
            param taskID : str : ID (task[0]) de la tâche à retirer
            """
            #print(taskID) # debug
            try:
                if self.master.master.File != None: # fichier CSV ouvert
                    self.master.master.File.Remove(taskID)
                    self.master.Tasks = self.master.master.File.GetTasks()

                elif self.master.master.Server != None: # connecté à un serveur
                    self.master.master.Server.Remove(taskID)
                    self.master.Tasks = self.master.master.Server.GetData()

                self.master.ShowTasks()
                print(f"Tâche {taskID} retirée avec succés")
            except Exception as e:
                print(f"Echec de la suppression de la tâche {taskID} {e}")
                msgbox.showerror("Suppression d'une tâche",
                    f"Echec de la suppression de la tâche {taskID} : {e}") 

        # ajout widgets
        # widget tâche
        self.CheckB = ttk.Checkbutton(self,
            text=f"{task[2][:30]}... // {task[3]} // {task[4]} // {task[6]}" if len(task[2]) > 60
            else f"{task[2]} // {task[3]} // {task[4]} // {task[6]}", onvalue=1, offvalue=0,
            style=f"{task[0]}.TCheckbutton", command=partial(TaskSelected, task[0]))
        self.CheckB.grid(row=0, column=0, sticky="w")
        # bouton de suppression
        ttk.Button(self, text="Supprimer tâche",
                    image=self.SupprImg, command=partial(RemoveTask, task[0])
                        ).place(rely=0, relx=.9)
        # config style
        s = ttk.Style(self)
        s.configure(f"{task[0]}.TCheckbutton",
                    background="#5B648A", font=("Arial", 16), anchor="w",
                    foreground=self.colors[task[4]])


if __name__ == '__main__':  # test de la frame (affichage)
    ShowVersion()  # affichage info prog
    from Global import x, y

    root = Tk()
    root.title("Test Mainframe")
    root.geometry("{}x{}".format(x, y))
    root.MainFrame = MainFrame(root)
    # setup test
    root.NavBar = NavBar(root)
    root.EntryFrame = None
    root.MainFrame.ShowTasks()

    root.mainloop()
