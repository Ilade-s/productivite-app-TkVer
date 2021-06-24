"""
Contient les variables et fonctions nécessaires dans plusieurs fichiers
"""
from sys import platform # connaitre la plateforme/OS
__version__ = "1.0"
__author__ = "Merlet Raphaël"
__advisor__ = "Elisa"
DefaultLabel = ["taskID", "userID", "name",
                             "date", "priority", "status", "tag"]
# taille fenêtre (utilisé dans Tk.geometry())
x = 1000 
y = 600

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