from tkinter import *
from tkinter import ttk
from SubFrame import SubFrame
from Global import ShowVersion

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
        # Remove and replace task Entryframe 
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
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
            background="#5B648A", font=("Arial", 16), anchor="w")
        # Maj état des boutons de SubFrame
        if len(self.Tasks) == 0: # pas de fichier (test)
            self.master.SubFrame.BackButton["state"] = "disabled"
            self.master.SubFrame.NextButton["state"] = "disabled"
        elif self.Ci == 0:  # début de la liste des tâches
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

if __name__=='__main__': # test de la frame (affichage)
    ShowVersion() # affichage info prog
    from Global import x, y

    root = Tk()
    root.title("Test Mainframe")
    root.geometry("{}x{}".format(x,y))
    root.MainFrame = MainFrame(root)
    # setup test
    root.SubFrame = SubFrame(root)
    root.EntryFrame = None
    root.MainFrame.ShowTasks()

    root.mainloop()