"""
Contient les variables fonctions nécessaires dans plusieurs fichiers
"""
from sys import platform # connaitre la plateforme/OS
__version__ = "0.1"
__author__ = "Merlet Raphaël"
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
    print(f"Made by {__author__}")
    print("Source : https://github.com/Ilade-s/productivite-app-TkVer")
    print("Server : https://github.com/Tifiloow/productivite-app")
    print("===============================================================")