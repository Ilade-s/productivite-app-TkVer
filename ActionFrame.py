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
        self.place(relx=0, rely=0, relheight=1, relwidth=.25)

    def CreateWidgets(self):
        """
        Placement des widgets
        """
        self.addImg = PhotoImage(file="Assets/add-icon.png")
        # ajout widgets
        self.AddButton = ttk.Button(self, text="Ajouter une tâche", image=self.addImg,
                                    compound=TOP, style="ActionFrame.TButton", 
                                    command=self.AddTask, state="disabled")
        # config style
        s = ttk.Style(self)
        s.configure("ActionFrame.TButton", borderwidth=5)
        self.AddButton.pack()

    def AddTask(self):
        """
        Action déclenchée par le bouton "Ajouter une tâche"
        """
        if self.master.EntryFrame != None:
            self.master.EntryFrame.destroy()
            self.master.EntryFrame = None
        self.master.EntryFrame = EntryFrame(
            self.master.MainFrame, "task")


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
