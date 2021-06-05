"""
Sous programme servant à gérer les bases de données
Utilisé dans le programme principal ProductivityApp

CLASSES :
-----------
    - CsvHandler :
        - permet de gérer et lire une base de donnée au format CSV
        - FONCTIONS :
            - Search : chercher une ligne ou un élément d'une ligne à partir d'une clé
            - Add : ajouter une donnée/ligne
            - Remove : retirer une ligne
            - Edit : éditer une ligne ou un élément de ligne
    - SqlHandler :
        - permet de gérer et lire une base de données avec une interface SQL
        - pour l'instant vide, sera faite et utilisée dans un second temps
"""

import csv  # Module mère gestion CSV
import sys  # Pour arrêt des fonctions en cas d'erreur (+ messages d'erreur)

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

        #if self.Data != [] and self.Data[-1] == []:
        #    self.dbW.writerow([])
        #self.dbW.writerow([1,2,3])

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

    def Search(self, key, dataheader=None):
        """
        Permet de chercher une donnée ou une ligne de donnée dans la base de donnée

        PARAMETRES :
        ------------
            - key : str
                - clé de la donnée/des données à chercher
            - dataheader : None | str
                - None : signifie que toute la/les lignes correspondantes doivent être récupérées
                - str : header de la ligne de donnée à récupérer
                - default = None
        
        SORTIE :
        -----------
            - données : list
                - si dataheader = None, contient les lignes sous forme de listes
                - si key correspond à plusieurs lignes, elles seront TOUTES renvoyées
        """
        self.ReadAll()

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
