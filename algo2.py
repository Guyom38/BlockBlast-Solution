import fct as FCT
import algo as ALGO
import interface as IHM

import variables as VAR
import itertools

# --- importation des librairies Pygame 
import pygame, time
from pygame.locals import *


def repositionner_piece():
    """
    Repositionne chaque pièce de VAR.pieces vers le haut et la gauche tout en conservant
    les dimensions 5x5 en complétant avec des "0" si nécessaire.
    """
    for piece in VAR.pieces:
        # Supprimer les lignes vides en haut
        while len(piece) > 0 and all(cell == "0" for cell in piece[0]):
            piece.pop(0)

        # Supprimer les lignes vides en bas
        while len(piece) > 0 and all(cell == "0" for cell in piece[-1]):
            piece.pop(-1)

        # Supprimer les colonnes vides à gauche
        while len(piece[0]) > 0 and all(row[0] == "0" for row in piece):
            for row in piece:
                row.pop(0)

        # Supprimer les colonnes vides à droite
        while len(piece[0]) > 0 and all(row[-1] == "0" for row in piece):
            for row in piece:
                row.pop(-1)

        # Compléter la matrice pour qu'elle fasse à nouveau 5x5
        while len(piece) < 5:  # Ajouter des lignes vides en bas
            piece.append(["0"] * 5)
        for row in piece:  # Ajouter des colonnes vides à droite
            while len(row) < 5:
                row.append("0")

    # Mettre à jour l'affichage après repositionnement
    IHM.afficher()
    pygame.display.update()



def Memoriser_Grille(id_grille):
    VAR.old_terrain[id_grille] = [row.copy() for row in VAR.terrain]

def Restaurer_Grille(id_grille):
    VAR.terrain = [row.copy() for row in VAR.old_terrain[id_grille]]

def Appliquer_Suppression_Lignes_Et_Colonnes():
    for y in range(8):
        for x in range(8):      
            if int(VAR.terrain[y][x]) > 5:
                VAR.terrain[y][x] = "0"  
            elif  int(VAR.terrain[y][x]) > 0:
                VAR.terrain[y][x] = "1"  
    


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

            Restaurer_Grille(id_piece)


    return liste_emplacements_possibles


        
def Trouver_Meilleure_Solution():
    repositionner_piece()

    Memoriser_Grille(3)
    
    nbP = 0
    for piece1, piece2, piece3 in Genere_Permutation_Pieces():
        nbP +=1

    pm, p1, p2, p3 = 0, 0, 0, 0
    i, max_score, max_penalites, id_best = 0, 0, 0, -1

    liste_permutations_pieces = Genere_Permutation_Pieces()
    solutions = {}
    for piece1, piece2, piece3 in liste_permutations_pieces:
        pm += 1
        Restaurer_Grille(3)

        liste1 = Genere_Liste_Bonnes_Places(piece1)
        for id_piece1, (x1, y1), (nb_lignes1, nb_colonnes1) in liste1:
            p1 += 1
            Restaurer_Grille(id_piece1)

            ALGO.placement_piece(id_piece1, x1, y1)
            ALGO.chercher_lignes_et_colonnes()
            Appliquer_Suppression_Lignes_Et_Colonnes()
            liste2 = Genere_Liste_Bonnes_Places(piece2)

            for id_piece2, (x2, y2), (nb_lignes2, nb_colonnes2) in liste2:
                p2 += 1
                Restaurer_Grille(id_piece2)       

                ALGO.placement_piece(id_piece2, x2, y2)
                ALGO.chercher_lignes_et_colonnes()
                Appliquer_Suppression_Lignes_Et_Colonnes()
                liste3 = Genere_Liste_Bonnes_Places(piece3)
                
                print ((piece1, piece2, piece3))
                print (" => " + str((x1, y1)))
                print (" => " + str((x2, y2)))
                print (str(liste3))
                for id_piece3, (x3, y3), (nb_lignes3, nb_colonnes3) in liste3:

                    p3 += 1
                    Restaurer_Grille(id_piece3)  

                    ALGO.placement_piece(id_piece3, x3, y3)
                    ALGO.chercher_lignes_et_colonnes()
                    Appliquer_Suppression_Lignes_Et_Colonnes()
                    zone, penalites = trouver_zones_vides_et_score()

                    score = nb_lignes1 + nb_lignes2 + nb_lignes3 + nb_colonnes1 + nb_colonnes2 + nb_colonnes3
                    solutions[i] = ( (id_piece1, x1, y1, nb_lignes1 + nb_colonnes1), (id_piece2, x2, y2, nb_lignes2 + nb_colonnes2), (id_piece3, x3, y3, nb_lignes3 + nb_colonnes3), score, penalites) 
                    if score >= max_score and (penalites > max_penalites or max_penalites == 0):
                        if id_best != -1:
                            print ("AVANT " + str(solutions[id_best]))
                        print ("NOUVEAU " + str(solutions[i]))
                        id_best, max_score, max_penalites = i, score, penalites
                    i += 1

                pourcentage = int ((100 /  nbP )* pm)                            
                IHM.barre_progression("Calcul des possibilités : ", pourcentage, 16, 720, 1008)
                pygame.display.update()

    Restaurer_Grille(3)
    if id_best > -1:
        xx, yy, premier = 16, 400, True
        (id_piece1, x1, y1, t1), (id_piece2, x2, y2, t2), (id_piece3, x3, y3, t3), score, penalites = solutions[id_best]
        print((id_best, solutions[id_best]))

        for id_piece, xxx, yyy in ((id_piece1, x1, y1), (id_piece2, x2, y2), (id_piece3, x3, y3)):      
            test = ALGO.placement_piece(id_piece, xxx, yyy)
            IHM.afficher_grille(xx, yy, not premier)
            IHM.pause(0.2)
            xx += 32*9
            ALGO.chercher_lignes_et_colonnes()
            Appliquer_Suppression_Lignes_Et_Colonnes()    

    else:
        IHM.barre_progression("Aucune solution trouvée ( "+ str(i) + ") : ", pourcentage, 16, 720, 1008, 40, (255,0,0), (200,16,16), (255,255,255))
        pygame.display.update()



def trouver_zones_vides_et_score():
    """
    Parcourt le terrain (8x8) et génère une liste des zones vides, avec un score basé sur leur taille.
    
    :param terrain: Matrice 8x8 représentant le terrain.
    :return: Un tuple (zones, score_total) :
             - zones : Liste des zones vides. Chaque élément est un dictionnaire contenant :
               - "index" : Index de la zone.
               - "position" : (x, y) de départ de la zone.
               - "cellules" : Nombre total de cellules dans la zone.
             - score_total : Score total en fonction des pénalités appliquées aux zones vides.
    """
    # Initialiser la liste des zones et un tableau pour marquer les cellules visitées
    zones = []
    visites = [[False for _ in range(8)] for _ in range(8)]
    index_zone = 0
    score_total = 0

    def explorer_zone(x, y):
        """
        Explore une zone vide en partant d'une position donnée (x, y).
        Utilise une recherche en profondeur (DFS) pour marquer les cellules connectées.
        :param x: Coordonnée x de départ.
        :param y: Coordonnée y de départ.
        :return: Liste des cellules de la zone explorée.
        """
        pile = [(x, y)]
        cellules = []
        while pile:
            cx, cy = pile.pop()
            if 0 <= cx < 8 and 0 <= cy < 8 and not visites[cy][cx] and VAR.terrain[cy][cx] == "0":
                visites[cy][cx] = True
                cellules.append((cx, cy))
                # Ajouter les voisins à explorer
                pile.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        return cellules

    # Parcourir chaque cellule du terrain
    for y in range(8):
        for x in range(8):
            if VAR.terrain[y][x] == "0" and not visites[y][x]:
                # Trouver une nouvelle zone vide
                cellules_zone = explorer_zone(x, y)
                if cellules_zone:
                    taille_zone = len(cellules_zone)

                    # Calculer la pénalité en fonction de la taille de la zone
                    if taille_zone == 1:
                        score_total += -1000  # Pénalité pour une zone de taille 1
                    elif taille_zone == 2:
                        score_total += -500   # Pénalité pour une zone de taille 2
                    elif taille_zone == 3:
                        score_total += -250   # Pénalité pour une zone de taille 3

                    # Ajouter la zone à la liste des zones
                    zones.append({
                        "index": index_zone,
                        "position": cellules_zone[0],  # Première cellule de la zone
                        "cellules": taille_zone
                    })
                    index_zone += 1

    score_total -= (len(zones) * 5)
    return zones, score_total
