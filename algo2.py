import fct as FCT
import algo as ALGO
import interface as IHM

import variables as VAR


# --- importation des librairies Pygame 
import pygame, time
from pygame.locals import *
from concurrent.futures import ThreadPoolExecutor

def repositionner_piece():
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



def memoriser_grille(id_grille):
    VAR.old_terrain[id_grille] = [row.copy() for row in VAR.terrain]

def restaurer_grille(id_grille):
    VAR.terrain = [row.copy() for row in VAR.old_terrain[id_grille]]

def mettre_a_jour_grille():
    VAR.terrain = [
        ["0" if int(cell) > 5 else "1" if int(cell) > 0 else cell for cell in row]
        for row in VAR.terrain
    ]
    
def Genere_Liste_Bonnes_Places(id_piece):
    memoriser_grille(id_piece)

    liste_emplacements_possibles = []
    for y in range(8):
        for x in range(8):
            if ALGO.placement_piece(id_piece, x, y):
                nb_lignes, nb_colonnes = ALGO.chercher_lignes_et_colonnes()
                liste_emplacements_possibles.append((id_piece, (x, y), (nb_lignes, nb_colonnes)))
                restaurer_grille(id_piece)

    return liste_emplacements_possibles



def optimiser_pieces():
    repositionner_piece()   
    
    VAR.pieces_composition = [
        [
            (x, y)  # Coordonnées de la case occupée
            for y in range(5)  # Parcourt les lignes
            for x in range(5)  # Parcourt les colonnes
            if VAR.pieces[p][y][x] == "1"  # Si la case est occupée
        ]
        for p in range(3)  # Parcourt les pièces
    ]
     
                
    
def Trouver_Meilleure_Solution():
    VAR.duree_traitement = time.time()
    
    solutions = {}
    pm, p1, i = 0, 0, 0
    max_score, max_penalites, id_best = 0, 0, -1
    liste_permutations_pieces = [   (0, 1, 2), \
                                    (0, 2, 1), \
                                    (1, 0, 2), \
                                    (1, 2, 0), \
                                    (2, 0, 1), \
                                    (2, 1, 0)   ]
    
    optimiser_pieces()
    memoriser_grille(3)
    
    for piece1, piece2, piece3 in liste_permutations_pieces:
        p1 = 0
        pm += 1
        
        restaurer_grille(3)        
        liste1 = Genere_Liste_Bonnes_Places(piece1)
        for id_piece1, (x1, y1), (nb_lignes1, nb_colonnes1) in liste1:
            p1 += 1
            
            restaurer_grille(id_piece1)
            ALGO.placement_piece(id_piece1, x1, y1)
            ALGO.chercher_lignes_et_colonnes()
            mettre_a_jour_grille()            
            
            liste2 = Genere_Liste_Bonnes_Places(piece2)
            for id_piece2, (x2, y2), (nb_lignes2, nb_colonnes2) in liste2:
                
                restaurer_grille(id_piece2)
                ALGO.placement_piece(id_piece2, x2, y2)
                ALGO.chercher_lignes_et_colonnes()
                mettre_a_jour_grille()
                
                liste3 = Genere_Liste_Bonnes_Places(piece3)                
                for id_piece3, (x3, y3), (nb_lignes3, nb_colonnes3) in liste3:

                    restaurer_grille(id_piece3)
                    ALGO.placement_piece(id_piece3, x3, y3)
                    ALGO.chercher_lignes_et_colonnes()
                    mettre_a_jour_grille()
                    
                    score = (nb_lignes1 + nb_lignes2 + nb_lignes3) + (nb_colonnes1 + nb_colonnes2 + nb_colonnes3)
                    zone, penalites = trouver_zones_vides_et_score()

                    
                    solutions[i] = (    (id_piece1, x1, y1, nb_lignes1 + nb_colonnes1), \
                                        (id_piece2, x2, y2, nb_lignes2 + nb_colonnes2), \
                                        (id_piece3, x3, y3, nb_lignes3 + nb_colonnes3), \
                                        score, penalites) 
                    if score >= max_score and (penalites > max_penalites or max_penalites == 0):
                         id_best, max_score, max_penalites = i, score, penalites
                    i += 1

                afficher_progression(pm, p1, liste1)
                
    restaurer_grille(3)
    afficher_meilleure_combinaison(id_best, solutions)


def afficher_progression(pm, p1, liste1):
    pourcentage = int ((100 /  6 ) * pm)                            
    IHM.barre_progression("Progression Permutation Pieces : ", pourcentage, 16, 680, 994, 30)
    pourcentage2 = int ((100 / len(liste1)) * p1)
    IHM.barre_progression("Progression Placements Piece 1 : ", pourcentage2, 16, 720, 994, 30)
      
    pygame.display.update()
    
def afficher_meilleure_combinaison(id_best, solutions):
    if id_best > -1:
        xx, yy, premier = 16, 350, True
        (id_piece1, x1, y1, t1), (id_piece2, x2, y2, t2), (id_piece3, x3, y3, t3), score, penalites = solutions[id_best]

        for id_piece, xxx, yyy in ((id_piece1, x1, y1), (id_piece2, x2, y2), (id_piece3, x3, y3)):      
            test = ALGO.placement_piece(id_piece, xxx, yyy)
            IHM.afficher_grille(xx, yy, not premier)
            xx += 32*9
            ALGO.chercher_lignes_et_colonnes()
            mettre_a_jour_grille()  
              
        IHM.barre_progression("Durée du traitement : " + str(round(time.time() - VAR.duree_traitement,3)) + "s    ...", 100, 16, 680, 994, 90)

    else:
        IHM.barre_progression("Aucune solution trouvée  : ", 0, 16, 720, 994, 40, (255,0,0), (200,16,16), (255,255,255))
        pygame.display.update()
    
def trouver_zones_vides_et_score():

    # Initialiser les zones et les cellules visitées
    zones = []
    visites = [[False] * 8 for _ in range(8)]
    score_total = 0
    index_zone = 0

    def explorer_zone_bfs(x, y):
        # Utiliser une file pour explorer les cellules (BFS)
        file = [(x, y)]
        cellules_zone = []
        while file:
            cx, cy = file.pop(0)
            if 0 <= cx < 8 and 0 <= cy < 8 and not visites[cy][cx] and VAR.terrain[cy][cx] == "0":
                visites[cy][cx] = True
                cellules_zone.append((cx, cy))

                # Ajouter les voisins à la file
                file.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        return cellules_zone

    # Parcourir toutes les cellules de la grille
    for y in range(8):
        for x in range(8):
            if VAR.terrain[y][x] == "0" and not visites[y][x]:
                # Trouver une nouvelle zone vide
                cellules_zone = explorer_zone_bfs(x, y)
                taille_zone = len(cellules_zone)

                if taille_zone > 0:
                    # Calculer directement la pénalité
                    if taille_zone == 1:
                        score_total += -1000  # Pénalité pour une zone de taille 1
                    elif taille_zone == 2:
                        score_total += -500   # Pénalité pour une zone de taille 2
                    elif taille_zone == 3:
                        score_total += -250   # Pénalité pour une zone de taille 3

                    # Ajouter la zone à la liste des zones
                    zones.append({
                        "index": index_zone,
                        "position": cellules_zone[0],  # Première cellule
                        "cellules": taille_zone
                    })
                    index_zone += 1

    # Ajouter une pénalité pour chaque zone détectée
    score_total -= len(zones) * 5

    return zones, score_total

