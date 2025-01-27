
import fct as FCT
import variables as VAR
import algo as ALGO
import algo2 as ALGO2

import interface as IHM
import time

# --- importation des librairies Pygame 
import pygame
from pygame.locals import *

#     ██ ███    ██ ██ ████████ ██  █████  ██      ██ ███████  █████  ████████ ██  ██████  ███    ██ 
#     ██ ████   ██ ██    ██    ██ ██   ██ ██      ██ ██      ██   ██    ██    ██ ██    ██ ████   ██ 
#     ██ ██ ██  ██ ██    ██    ██ ███████ ██      ██ ███████ ███████    ██    ██ ██    ██ ██ ██  ██ 
#     ██ ██  ██ ██ ██    ██    ██ ██   ██ ██      ██      ██ ██   ██    ██    ██ ██    ██ ██  ██ ██ 
#     ██ ██   ████ ██    ██    ██ ██   ██ ███████ ██ ███████ ██   ██    ██    ██  ██████  ██   ████ 
                                                                                              
                                                                                              
# --- initialisation du moteur Pygame
pygame.init()
VAR.fenetre = pygame.display.set_mode((1024, 768), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Block Blast Resolution")
horloge = pygame.time.Clock()


img = pygame.image.load("blocs.png")
VAR.img_bloc = []

VAR.img_bloc.append(FCT.image_decoupe(img, 0, 1, 25, 25, 32, 32))
for x in range(8):
    VAR.img_bloc.append(FCT.image_decoupe(img, x, 0, 25, 25, 32, 32))

VAR.img_bloc.append(FCT.image_decoupe(img, 0, 1, 25, 25, 8, 8))
for x in range(8):
    VAR.img_bloc.append(FCT.image_decoupe(img, x, 0, 25, 25, 8, 8))

VAR.tempo = time.time()
t, p = FCT.charger_donnees()
if len(t) > 0 and len(p) > 0:
    VAR.terrain, VAR.pieces = t, p


liste_permutations_pieces = ALGO2.Genere_Permutation_Pieces()

#     ██████   ██████  ██    ██  ██████ ██      ███████ 
#     ██   ██ ██    ██ ██    ██ ██      ██      ██      
#     ██████  ██    ██ ██    ██ ██      ██      █████   
#     ██   ██ ██    ██ ██    ██ ██      ██      ██      
#     ██████   ██████   ██████   ██████ ███████ ███████ 
                                                 
                                                  
VAR.fenetre.fill((32,32,32))
while VAR.boucle:
    FCT.gestion_utilisateur()

    solutions = []
    for piece1, piece2, piece3 in liste_permutations_pieces:
        liste1 = ALGO2.Genere_Liste_Bonnes_Places(piece1)
 
        for id_piece1, (x1, y1), (nb_lignes1, nb_colonnes1) in liste1:

            ALGO.placement_piece(id_piece1, x1, y1)
            ALGO.chercher_lignes_et_colonnes()
            ALGO2.Appliquer_Suppression_Lignes_Et_Colonnes()
            liste2 = ALGO2.Genere_Liste_Bonnes_Places(piece2)
 
            for id_piece2, (x2, y2), (nb_lignes2, nb_colonnes2) in liste2:
                
                ALGO.placement_piece(id_piece2, x2, y2)
                ALGO.chercher_lignes_et_colonnes()
                ALGO2.Appliquer_Suppression_Lignes_Et_Colonnes()
                liste3 = ALGO2.Genere_Liste_Bonnes_Places(piece3)

                for id_piece3, (x3, y3), (nb_lignes3, nb_colonnes3) in liste3:

                    ALGO.placement_piece(id_piece3, x3, y3)
                    ALGO.chercher_lignes_et_colonnes()
                    ALGO2.Appliquer_Suppression_Lignes_Et_Colonnes()
                    print(( " ==> ", (id_piece1, x1, y1, nb_lignes1 + nb_colonnes1), (id_piece2, x2, y2, nb_lignes2 + nb_colonnes2), (id_piece3, x3, y3, nb_lignes3 + nb_colonnes3), (nb_lignes1 + nb_lignes2 + nb_lignes3 + nb_colonnes1 + nb_colonnes2 + nb_colonnes3) ))

                    solutions.append( ((id_piece1, x1, y1, nb_lignes1 + nb_colonnes1), (id_piece2, x2, y2, nb_lignes2 + nb_colonnes2), (id_piece3, x3, y3, nb_lignes3 + nb_colonnes3), (nb_lignes1 + nb_lignes2 + nb_lignes3 + nb_colonnes1 + nb_colonnes2 + nb_colonnes3)) )




        xx, yy = 16, 16
        for (id_piece1, x1, y1, t1), (id_piece2, x2, y2, t2), (id_piece3, x3, y3, t3), score  in solutions:
            for id_piece, xxx, yyy in ((id_piece1, x1, y1), (id_piece2, x2, y2), (id_piece3, x3, y3)):
                ALGO.placement_piece(id_piece, xxx, yyy)
                IHM.afficher_grille(xx, yy, True)
                xx += 80
                ALGO.chercher_lignes_et_colonnes()
                ALGO2.Appliquer_Suppression_Lignes_Et_Colonnes()
                IHM.afficher_grille(xx, yy, True)
                xx += 80

            
            police = pygame.font.Font(None, 64)
            texte_rendu = police.render(str(score), True, (255,255,255))
            VAR.fenetre.blit(texte_rendu, (xx + 100 , yy+16))
           
            xx = 16
            yy += 90
            IHM.pause(1)

    input(">>")       
    IHM.afficher()

    pygame.display.update()
    horloge.tick(25)
    VAR.souris[0] = 0

pygame.quit()   



