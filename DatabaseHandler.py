"""
Sous programme servant à gérer les bases de données au format CSV
Utilisé dans le programme principal ProductivityApp

CsvHandler :
-----------
    - permet de gérer et lire une base de donnée au format CSV
    - FONCTIONS :
        - update_reader : mise a jour de self.Data (liste des lignes)
        - get_tasks : renvoie la liste des lignes de données (index 1 à n)
        - add : ajouter une donnée/ligne
        - remove : retirer une ligne
        - edit : éditer une ligne ou un élément de ligne
"""

import csv  # Module mère gestion CSV
from Global import LABELS

class CsvHandler():
    """
    Permet de gérer et lire une base de donnée au format CSV
    - FONCTIONS :
        - Search : chercher une ligne ou un élément d'une ligne à partir d'une clé
        - add : ajouter une donnée/ligne
        - remove : retirer une ligne
        - edit : éditer une ligne ou un élément de ligne
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

    def update_reader(self):
        """
        Permet de mettre à jour la base de donnée
        """
        self.file.close()
        self.file = open(self.path, "r+", encoding="utf-8", newline='\n')
        self.dbR = csv.reader(self.file, delimiter=self.Delimiter)
        self.Data = [i for i in self.dbR]
        self.dbW = csv.writer(self.file, delimiter=self.Delimiter)
        #print(self.Data)
    
    def get_tasks(self):
        self.update_reader()
        # récupération tâches
        tasks = [task for task in self.Data[1:]]
        return tasks

    def add(self, data):
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
        self.update_reader()

    def remove(self, key):
        """    
        Retire toutes les lignes du fichier correspondantes à clé
       
        PARAMETRES :
        ------------
            - key : str
                - clé contenue dans la ou les lignes à supprimer
        """
        self.Data = list(filter(lambda l: key not in l, self.Data)) # filtrage

        with open(self.path, "w", encoding="utf-8", newline='\n') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(self.Data)
        
        self.__init__(self.path) # réouverture du fichier en mode r+ (lecture/écriture)

    def edit(self, key, status):
        """    
        Edite l'êtat de la tâche (ligne) correspondante à la clé
       
        PARAMETRES :
        ------------
            - key : str
                - clé contenue dans la ou les lignes à editer
            - status : str
                - nouvel état à donner à la ligne
        """
        # édition données
        for l in self.Data:
            if key in l:
                l[LABELS.index("status")] = status

        with open(self.path, "w", encoding="utf-8", newline='\n') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(self.Data)
        
        self.__init__(self.path) # réouverture du fichier en mode r+ (lecture/écriture)

def main():
    Db = CsvHandler("Data/test.csv")
    #print(Db.Data)
    #Db.add(LABELS)
    #Db.update_reader()
    Db.remove(["85"])
    #print(Db.Data)

if __name__=='__main__': # test
    main()
