"""
Contient les variables et fonctions nécessaires dans plusieurs fichiers
"""
from sys import platform # connaitre la plateforme/OS
from datetime import date # récupération de la date (ajout de tâche)
CDATE = str(date.today())  # date actuelle (format AAAA-MM-JJ)
__version__ = "1.1"
__author__ = "Raphaël"
__advisor__ = "Elisa"
DefaultLabel = ["taskID", "userID", "name",
                             "date", "priority", "status", "tag"]
# taille fenêtre (utilisé dans Tk.geometry())
x = 1000 
y = 600
# nombre de jour par mois (année non bissextile, dans l'ordre de janvier à décembre)
jMois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def ShowVersion():
    """
    Affiche la version et les informations sur le programme dans la console
    """
    print("===============================================================")
    print(f"Productivity App v{__version__}")
    print(f"Made by {__author__} (with the advices of {__advisor__})")
    print("Source : https://github.com/Ilade-s/productivite-app-TkVer")
    print("Server (optionnal) : https://github.com/Tifiloow/productivite-app")
    print("===============================================================")