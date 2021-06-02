"""
Sous programme de création de plot (graphiques) matplotlib
Sauvegarde les plots sous forme d'images pour qu'ils soient ensuite affichés dans le fenêtre tkinter 

FONCTIONS :
----------
    - CircularPlot : Pour création de diagramme circulaire
    - GraphPlot : Pour création de diagramme en barres
"""

import matplotlib.pyplot as plt # Création de plots

def CircularPlot(data, labels, title="Bilan des tâches"):
    """
    Création de diagrammes circulaires

    PARAMETRES :
    ------------
        - data : list
            - données à exploiter pour graphique
        - labels : list[str]
            - labels des données dans l'ordre des types de la liste data
        - title : str
            - Titre à donner au graphique
    
    SORTIE : 
    ------------
        - Aucune (sauvegarde de l'image en .png dans le dossier de travail)
    """
    pass

def GraphPlot(data, labels, title="Bilan des tâches"):
    """
    Création de diagrammes en barres

    PARAMETRES :
    ------------
        - data : list
            - données à exploiter pour graphique
        - labels : list[str]
            - labels des données dans l'ordre des types de la liste data
        - title : str
            - Titre à donner au graphique
    
    SORTIE :
    ------------
        - Aucune (sauvegarde de l'image en .png dans le dossier de travail)
    """
    pass

def main():
    pass

if __name__=='__main__': # test
    main()