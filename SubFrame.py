from tkinter import *
from tkinter import ttk


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
        self.place(relx=0, rely=.75, relheight=.25, relwidth=1)

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
            self, text="Previous page", state="disabled", style="SubFrame.TButton", 
                command=self.PreviousPage, image=self.BackImg)
        self.NextButton = ttk.Button(
            self, text="Next page", state="disabled", style="SubFrame.TButton", 
                command=self.NextPage, image=self.NextImg)
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
        self.master.MainFrame.UpdateMaxAff()  # maj affichage max
        self.master.MainFrame.ShowTasks()  # maj affichage


if __name__ == '__main__':  # test de la frame (affichage)
    from Global import x, y, ShowVersion
    ShowVersion()  # affichage info prog

    root = Tk()
    root.title("Test Subframe")
    root.geometry("{}x{}".format(x, y))
    frame = SubFrame(root)
    #frame.BackButton['state'] = "normal"
    #frame.NextButton['state'] = "normal"

    root.mainloop()
