from tkinter import *
from tkinter import ttk


class NavBar(LabelFrame):
    """
    Frame située en dessous de MainFrame servant à changer de page et indiquer la page affichée
    """

    def __init__(self, master) -> None:
        self.master = master
        super().__init__(master, background="#A8B8FF",
                         relief=RAISED, text="NavBar", foreground="white")
        self.create_widgets()
        self.place(relx=0, rely=.75, relheight=.25, relwidth=1)

    def create_widgets(self):
        self['text'] = "Menu de navigation"
        for w in self.winfo_children():
            w.destroy()
        # config lignes et colonnes
        self.rowconfigure(0, weight=1)
        for i in range(5):
            self.columnconfigure(i, weight=1)
        # importation images
        self.BackImg = PhotoImage(file="Assets/chevron-left.png")
        self.NextImg = PhotoImage(file="Assets/chevron-right.png")
        # ajout des widgets
        self.BackButton = ttk.Button(
            self, text="Previous page", state="disabled", style="NavBar.TButton", 
                command=self.go_to_previous_page, image=self.BackImg)
        self.NextButton = ttk.Button(
            self, text="Next page", state="disabled", style="NavBar.TButton", 
                command=self.go_to_next_page, image=self.NextImg)
        self.ReaderInfo = Label(self, text="..-../.. (/..)", font=("Arial", 20))
        self.BackButton.grid(row=0, column=1)
        self.NextButton.grid(row=0, column=3)
        self.ReaderInfo.grid(row=0, column=2, ipadx=50, ipady=20)
        # config style boutons
        s = ttk.Style(self)
        s.configure("NavBar.TButton", font=("Arial", 10))

    def go_to_previous_page(self):
        """
        Commande appelée par le bouton self.BackButton permettant de revenir à la page précédente 
        (dans l'affichage des tâches)
        """
        affmax = self.master.MainFrame.update_max_aff()  # récupération affmax
        self.master.MainFrame.ReaderIndex -= affmax  # maj intervalle des tâches à afficher
        if self.master.MainFrame.ReaderIndex < 0:  # afin d'éviter les index négatifs
            self.master.MainFrame.ReaderIndex = 0
        self.master.MainFrame.render_tasks()  # maj affichage

    def go_to_next_page(self):
        """
        Commande appelée par le bouton self.NextButton permettant d'afficher la page suivante
        (dans l'affichage des tâches)
        """
        self.master.MainFrame.ReaderIndex += self.master.MainFrame.maxAff  # maj intervalle des tâches à afficher
        self.master.MainFrame.update_max_aff()  # maj affichage max
        self.master.MainFrame.render_tasks()  # maj affichage


if __name__ == '__main__':  # test de la frame (affichage)
    from Global import x, y, show_version
    show_version()  # affichage info prog

    root = Tk()
    root.title("Test NavBar")
    root.geometry("{}x{}".format(x, y))
    frame = NavBar(root)
    #frame.BackButton['state'] = "normal"
    #frame.NextButton['state'] = "normal"

    root.mainloop()
