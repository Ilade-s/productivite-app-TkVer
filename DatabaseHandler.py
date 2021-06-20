"""
Sous programme servant à gérer les bases de données au format CSV
Utilisé dans le programme principal ProductivityApp

CsvHandler :
-----------
    - permet de gérer et lire une base de donnée au format CSV
    - FONCTIONS :
        - Search : chercher une ligne ou un élément d'une ligne à partir d'une clé
        - Add : ajouter une donnée/ligne
        - Remove : retirer une ligne
        - Edit : éditer une ligne ou un élément de ligne
"""

import csv  # Module mère gestion CSV

class CsvHandler():
    """
    Permet de gérer et lire une base de donnée au format CSV
    - FONCTIONS :
        - Search : chercher une ligne ou un élément d'une ligne à partir d'une clé
        - Add : ajouter une donnée/ligne
        - Remove : retirer une ligne
        - Edit : éditer une ligne ou un élément de ligne
    """

    def __init__(self, path, mode="r+", Delimiter=",") -> None:
        """
        Ouvre la base de donnée

        PARAMETRES :
            - path : str
                - Chemin du fichier CSV de la base de donnée
            - mode : str
                - mode d'ouverture du fichier
                - "x+" : création d'un nouveau fichier CSV
                - "r+" : lecture/écriture d'un fichier existant
                - si l'ouverture en mode "r+" échoue, "x+" sera utilisé (va créer un nouveau fichier)
                - default = "r+"
            - Delimiter : str
                - comma entre les données du CSV
                - default = ","
        """
        self.Delimiter = Delimiter
        self.path = path
        if mode=="x+":
            with open(path, "x+", encoding="utf-8", newline='\n') as file:
                self.dbR = csv.reader(file, delimiter=Delimiter)
        else:
            try:
                self.file = open(path, mode, encoding="utf-8", newline='\n')
                self.dbR = csv.reader(self.file, delimiter=Delimiter)
                self.Data = [i for i in self.dbR]
                self.dbW = csv.writer(self.file, delimiter=Delimiter)
            except FileNotFoundError:
                #print("Fichier non trouvé")
                with open(path, "x+", encoding="utf-8", newline='\n') as file:
                    self.dbR = csv.reader(file, delimiter=Delimiter)

    def ReadAll(self):
        """
        Permet de mettre à jour la base de donnée
        """
        self.file.close()
        self.file = open(self.path, "r+", encoding="utf-8", newline='\n')
        self.dbR = csv.reader(self.file, delimiter=self.Delimiter)
        self.Data = [i for i in self.dbR]
        self.dbW = csv.writer(self.file, delimiter=self.Delimiter)
        #print(self.Data)
    
    def GetTasks(self):
        """
        Permet de récupérer la liste des tâches contenues dans le fichier
        """
        self.ReadAll() # mise à jour reader
        # récupération tâches
        tasks = [task for task in self.Data[1:]]
        #print(tasks)

        return tasks

    def Add(self, data):
        """
        Permet d'ajouter la ligne data

        PARAMETRES :
        ------------
            - data : list
                - ligne à ajouter au fichier csv
        
        SORTIE :
        ------------
            - Aucune
        """
        self.dbW.writerow(data)
        self.ReadAll()

    def Remove(self, key):
        pass

    def Edit(self, key, data, dataheader=None):
        pass

def main():
    Db = CsvHandler("Data/test.csv")
    print(Db.Data)
    Db.Add(["name", "creation", "duedate","type"])
    Db.ReadAll()
    print(Db.Data)

if __name__=='__main__': # test
    main()
