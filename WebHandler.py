"""
Sous programme permettant de créer une interface avec un serveur web (local ou distant)
La classe est initialisée avec l'adresse du serveur en argument
"""

import requests
from requests.models import Response

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
    
    def Login(self, username, password, adress):
        """
        Permet de s'identifier au serveur avec un compte (préexistant uniquement)

        PARAMETRE :
        ------------
            - username : str
                - identifiant/adresse email
            - password : str
                - mot de passe du compte
            - adress : str
                - adresse pour se login au serveur
        """
        self.Account = username
        # création payload credentials
        payload = {
            'email': username,
            'password': password
        }

        # Use 'with' to ensure the session context is closed after use.
        self.session = requests.Session()
        p = self.session.post(adress, data=payload)
        #print("login :",p.status_code)

        if p.status_code != requests.codes.ok:
            raise(Exception)
        # An authorised request.
        r = self.session.get(self.adress+"profile")
        #print("profile :",r.status_code)

        if r.status_code != requests.codes.ok:
            raise(Exception)
        
        if not "Welcome" in r.text:
            raise(Exception)
        
        print(f"Login réussi : {self.Account}")

    def Signup(self, username, password, name, adress):
        """
        Permet de s'identifier au serveur avec un compte (préexistant uniquement)

        PARAMETRE :
        ------------
            - username : str
                - identifiant/adresse email
            - password : str
                - mot de passe du compte
            - name : str
                - nom du compte
            - adress : str
                - adresse pour se créer un compte
        """
        self.Account = username
        # création payload credentials
        payload = {
            'email': username,
            'name': name,
            'password': password
        }

        # Use 'with' to ensure the session context is closed after use.
        self.session = requests.Session()
        p = self.session.post(adress, data=payload, allow_redirects=True)
        #print("login :",p.status_code)
        if p.status_code != requests.codes.ok:
            raise(Exception)
        if not p.url == self.adress+"login":
            raise(Exception)

        print(f"Création du compte réussie : {self.Account}")

        self.Login(username, password, self.adress+"login")


    def GetData(self, subpage="/getdata"):
        """
        Permet de récupérer la base de données de toutes les tâches liées à l'utilisateur
        subpage : str (extension indiquant le sous page permettant des récupérer les données)
        """
        r = self.session.post(self.adress+subpage)

        if r.status_code != requests.codes.ok:
            raise(Exception)

        return r.json()

    def AddTask(self): # à faire
        """
        Ajoute un tâche
        """