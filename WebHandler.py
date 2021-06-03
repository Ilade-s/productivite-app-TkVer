"""
Sous programme permettant de créer une interface avec un serveur web (local ou distant)
La classe est initialisée avec l'adresse du serveur en argument
"""

import requests

class WebInterface():
    """
    Permet de créer une connexion avec un serveur
    """
    
    def __init__(self, adress) -> None:
        """
        Initialise l'interface et tente une requête GET

        PARAMETRE :
        ------------
            - adress : str
                - adresse du serveur web
        
        SORTIE :
        ------------
            - True : connexion et tests réussis
            - False : échec de la connexion
        """
        self.Account = None
        self.adress = adress
        testrequest = requests.get(self.adress) # test GET
    
    def Login(self, username, password):
        """
        Permet de s'identifier au serveur avec un compte (préexistant uniquement)

        PARAMETRE :
        ------------
            - username : str
                - identifiant/adresse email
            - password : str
                - mot de passe du compte
        
        SORTIE :
        ------------
            - Aucune
        """
        self.Account = username
        print(f"Credentials : \n\t- username : {username} \n\t- password : {password}")

    def GetDatabase(self):
        """
        Permet de récupérer la base de données de toutes les tâches liées à l'utilisateur
        """
        pass