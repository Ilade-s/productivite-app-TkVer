"""
Sous programme permettant de créer une interface avec un serveur web (local ou distant)
La classe est initialisée avec l'adresse du serveur en argument
"""

import requests
import json

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
        r = requests.get(self.adress) # test GET
        if r.status_code != requests.codes.ok:
            raise(Exception)
    
    def login(self, username, password, adress):
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

        payload = {
            'email': username,
            'password': password
        }

        self.session = requests.Session()
        p = self.session.post(adress, data=payload)

        p.raise_for_status()

        r = self.session.get(self.adress+"profile" if self.adress[-1]=="/" 
                                else self.adress+"/profile")

        r.raise_for_status()
        
        if not "Welcome" in r.text:
            raise(Exception)
        
        print(f"login réussi : {self.Account}")

    def sign_up(self, username, password, name, adress):
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

        self.session = requests.Session()
        p = self.session.post(adress, data=payload, allow_redirects=True)
        # checks to see if the signup succeded
        p.raise_for_status()
        if not p.url == self.adress+"login":
            raise(Exception)

        print(f"Création du compte réussie : {self.Account}")

        self.login(username, password, self.adress+"login")

    def get_data(self, subpage="/getdata"):
        """
        Permet de récupérer la base de données de toutes les tâches liées à l'utilisateur
        subpage : str (extension indiquant le sous page permettant des récupérer les données)
        """
        r = self.session.post(self.adress+subpage)

        r.raise_for_status()

        return r.json()

    def add(self, task):
        """
        Ajoute un tâche

        PARAMETRE :
            - task : dict
                - dictionnaire au format {userID, task, date, priority, tag} représentant la tâche à ajouter
        """
        r = self.session.post(self.adress, data=json.dumps(task, separators=(',', ':')))

        r.raise_for_status()

    def remove(self, taskID):
        """
        Supprime une tâche

        PARAMETRE :
            - taskID : str | int
                - identifiant unique permettant de reconnaitre chaque tâche
        """
        payload = {
            "goal" : "removeElement",
            "taskID" : str(taskID)
        }

        r = self.session.post(self.adress, data=json.dumps(payload, separators=(',', ':')))

        r.raise_for_status()
    
    def edit(self, taskID, status):
        """
        Edite l'êtat d'une tâche

        PARAMETRE :
            - taskID : str | int
                - identifiant unique permettant de reconnaitre chaque tâche
            - status : str
                - nouvel êtat à donner à la tâche
        """
        payload = {
            "goal" : "updateStatus",
            "taskID" : str(taskID),
            "status" : status
        }

        r = self.session.post(self.adress, data=json.dumps(payload, separators=(',', ':')))

        r.raise_for_status()
