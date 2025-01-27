import fct as FCT
import algo as ALGO
import interface as IHM

import variables as VAR
import itertools

# --- importation des librairies Pygame 
import pygame, time
from pygame.locals import *

def Memoriser_Grille(id_grille):
    VAR.old_terrain[id_grille] = [row.copy() for row in VAR.terrain]

def Restaurer_Grille(id_grille):
    VAR.terrain = [row.copy() for row in VAR.old_terrain[id_grille]]

def Appliquer_Suppression_Lignes_Et_Colonnes():
    ALGO.effacer_placement(4)
    ALGO.effacer_placement(5)

def Genere_Permutation_Pieces():
    return itertools.permutations(range(3))

def Genere_Liste_Bonnes_Places(id_piece):
    Memoriser_Grille(id_piece)

    liste_emplacements_possibles = []
    for y in range(8):
        for x in range(8):
            if ALGO.placement_piece(id_piece, x, y):
                nb_lignes, nb_colonnes = ALGO.chercher_lignes_et_colonnes()
                liste_emplacements_possibles.append((id_piece, (x, y), (nb_lignes, nb_colonnes)))
                #IHM.afficher_grille(16, 16, False)                
                #IHM.pause()

            Restaurer_Grille(id_piece)


    return liste_emplacements_possibles
