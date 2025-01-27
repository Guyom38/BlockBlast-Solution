
import fct as FCT
import variables as VAR
import algo as ALGO

import interface as IHM
import time

# --- importation des librairies Pygame 
import pygame
from pygame.locals import *

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

VAR.img_bloc.append(FCT.image_decoupe(img, 0, 1, 25, 25, 16, 16))
for x in range(8):
    VAR.img_bloc.append(FCT.image_decoupe(img, x, 0, 25, 25, 16, 16))

VAR.tempo = time.time()
t, p = FCT.charger_donnees()
if len(t) > 0 and len(p) > 0:
    VAR.terrain, VAR.pieces = t, p
    
VAR.fenetre.fill((32,32,32))

while VAR.boucle:
    FCT.gestion_utilisateur()
    
    
    ALGO.chercher_lignes_et_colonnes()
    IHM.afficher()
        
    if IHM.bouton("Solution", 1024-216, 16):  # Bouton centré
        old_terrain = [ligne.copy() for ligne in VAR.terrain]
        if ALGO.test_placement_piece(0):
            
            VAR.message = "Bravo"
        else:
            VAR.message = "C'est niqué !"
            VAR.terrain = [ligne.copy() for ligne in old_terrain]
            VAR.pieces = [VAR.pieces[1], VAR.pieces[2], VAR.pieces[0]]


    if IHM.bouton("Intervertir", 1024-216, 80):  # Bouton centré
        ALGO.test_combinaisons()
        #VAR.pieces = [VAR.pieces[1], VAR.pieces[2], VAR.pieces[0]]
    
    IHM.bouton(VAR.message, 0, 735, 1024, 30)
    IHM.afficher_logs(600, 250)
    
    pygame.display.update()
    horloge.tick(25)
    VAR.souris[0] = 0

# --- en sortie de boucle, quitte le programme
#FCT.enregistrer_donnees(VAR.terrain, VAR.pieces)
pygame.quit()             
            



