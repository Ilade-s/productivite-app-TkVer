from tkinter import *
from tkinter import ttk
from EntryFrame import *


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
        self.place(relx=0, rely=0, relheight=1, relwidth=.15)

    def CreateWidgets(self):
        """
        Placement des widgets
        """
        self['text'] = "Barre d'outils"
        self.removeImg = PhotoImage(file="Assets/remove-icon.png")
        # ajout widgets
        self.RemoveButton = ttk.Button(self, text="Retirer des tâches", image=self.removeImg,
                                    compound=TOP, style="ActionFrame.TButton", 
                                    command=self.RemoveTasks, state="disabled")
        # config style
        s = ttk.Style(self)
        s.configure("ActionFrame.TButton", borderwidth=5)
        # affichage widgets
        self.RemoveButton.pack(pady=10)
    
    def RemoveTasks(self):
        """
        Action déclenchée par le bouton "retirer des tâches"
        """
        # aucune tâche sélectionnée
        if sum([state.get() for state in self.master.MainFrame.StateTasks]) == 0:
            print("Suppression impossible : aucune tâche n'est sélectionnée")
            msgbox.showerror("Remove tasks",
            "Aucune tâche à retirer n'est sélectionnée")
        else:
            for i in range(self.master.MainFrame.StateTasks): # balayage indexs états boutons
                keysID = []
                # récupération ID de tâche
                if self.master.MainFrame.StateTasks[i].get() == 1:
                    keysID.append(self.master.MainFrame.Tasks[i][0])

            # supression lignes du CSV ou du serveur
            if self.master.Server != None: # connecté à un serveur
                pass

            elif self.master.Db != None: # BDD CSV ouverte
                self.master.Db.Remove(keysID)
            
            else: # pas de BDD ouverte
                print("Aucune BDD ouverte, supression de tâches impossible")
                msgbox.showerror("Suppression de tâche",
                                f"Echec de l'ajout de la tâche  \nAucune base de donnée n'est ouverte")



    def ActivateButtons(self):
        """
        Permet d'activer tous les boutons d'ActionFrame
        """
        self.RemoveButton['state'] = "normal"


if __name__ == '__main__':  # test affichage et boutons

    from MainFrame import *
    from Global import x, y, ShowVersion
    ShowVersion()  # affichage info prog

    root = Tk()
    root.title("Test Actionframe")
    root.geometry("{}x{}".format(x, y))
    frame = ActionFrame(root)
    # setup test
    root.EntryFrame = None
    root.MainFrame = MainFrame(root)

    root.mainloop()
