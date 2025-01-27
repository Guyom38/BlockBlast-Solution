
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

VAR.img_bloc.append(FCT.image_decoupe(img, 0, 1, 25, 25, VAR.tmini, VAR.tmini))
for x in range(8):
    VAR.img_bloc.append(FCT.image_decoupe(img, x, 0, 25, 25, VAR.tmini, VAR.tmini))

VAR.tempo = time.time()
t, p = FCT.charger_donnees()
if len(t) > 0 and len(p) > 0:
    VAR.terrain, VAR.pieces = t, p



#     ██████   ██████  ██    ██  ██████ ██      ███████ 
#     ██   ██ ██    ██ ██    ██ ██      ██      ██      
#     ██████  ██    ██ ██    ██ ██      ██      █████   
#     ██   ██ ██    ██ ██    ██ ██      ██      ██      
#     ██████   ██████   ██████   ██████ ███████ ███████ 
                                                 
                                                  
VAR.fenetre.fill((32,32,32))
while VAR.boucle:
    FCT.gestion_utilisateur()
    IHM.afficher()
        
    if IHM.bouton("Charger", 1024-216, 20):  # Bouton centré
        t, p = FCT.charger_donnees()
        if len(t) > 0 and len(p) > 0:
            VAR.terrain, VAR.pieces = t, p       

    if IHM.bouton("Enregistrer", 1024-216, 70):  # Bouton centré
        FCT.enregistrer_donnees(VAR.terrain, VAR.pieces )     

    if IHM.bouton("Solution", 1024-216, 120):  # Bouton centré
        VAR.pieces[0] = ALGO2.repositionner_piece(VAR.pieces[0])
        VAR.pieces[1] = ALGO2.repositionner_piece(VAR.pieces[1])
        VAR.pieces[2] = ALGO2.repositionner_piece(VAR.pieces[2])
        ALGO2.Trouver_Meilleure_Solution()       




    pygame.display.update()
    horloge.tick(25)
    VAR.souris[0] = 0

pygame.quit()   



