

import os, time
import variables as VAR
import pygame
from pygame.locals import *
import json

def image_vide(dimx, dimy):
    return pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)

def image_decoupe(img, x, y, dimx, dimy, dimxZ = -1, dimyZ = -1):
    tmp = pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)
    tmp.blit(img, (0,0), (int(x) * dimx, int(y) * dimy, dimx, dimy))
                                
    # --- Colle le decors 
    if dimxZ != -1 and dimyZ != -1:   
        tmp = pygame.transform.scale(tmp, (dimxZ, dimyZ))
    return tmp
    
def GenereMat2D(dimX, dimY, valeurDefaut):
    return [[valeurDefaut for x in range(dimY)] for i in range(dimX)]


def gestion_utilisateur():
    for event in pygame.event.get():        
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            VAR.boucle = False
        
        # Détection du clic de souris
        if event.type == MOUSEBUTTONDOWN and time.time() - VAR.tempo > 0.15:
            # Vérifie quel bouton est cliqué
            if event.button == 1:  # Bouton gauche
                VAR.souris = [1, event.pos[0], event.pos[1]]
            elif event.button == 2:  # Bouton du milieu
                VAR.souris = [2, event.pos[0], event.pos[1]]
            elif event.button == 3:  # Bouton droit
                VAR.souris = [3, event.pos[0], event.pos[1]]            
            VAR.tempo = time.time()

        if event.type == MOUSEBUTTONUP:
            VAR.souris = [0, event.pos[0], event.pos[1]]
            
def enregistrer_donnees(terrain, pieces, nom_fichier="data.json"):
    """
    Enregistre le terrain et les pièces dans un fichier JSON.
    :param terrain: Matrice 8x8 représentant le terrain.
    :param pieces: Dictionnaire des pièces indexées.
    :param nom_fichier: Nom du fichier de sauvegarde.
    """
    try:
        donnees = {
            "terrain": terrain,
            "pieces": pieces
        }
        with open(nom_fichier, "w") as fichier:
            json.dump(donnees, fichier)
        print(f"Données enregistrées dans {nom_fichier}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")

def charger_donnees(nom_fichier="data.json"):
    """
    Charge le terrain et les pièces depuis un fichier JSON.
    :param nom_fichier: Nom du fichier à charger.
    :return: Tuple contenant le terrain et les pièces.
    """
    try:
        with open(nom_fichier, "r") as fichier:
            donnees = json.load(fichier)
        print(f"Données chargées depuis {nom_fichier}.")
        return donnees["terrain"], donnees["pieces"]
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'existe pas.")
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
    return [[0 for _ in range(8)] for _ in range(8)], {}  # Terrain et pièces vides par défaut
