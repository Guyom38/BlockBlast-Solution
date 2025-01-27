import fct as FCT
import variables as VAR

# --- importation des librairies Pygame 
import pygame, time
from pygame.locals import *


def afficher(mini = False):    
    
    afficher_grille(16, 16, mini)
    afficher_pieces_disponibles(16, 16)
    
    
def afficher_grille(pX, pY, mini):   
    taille = VAR.tmini if mini else 32 
    mini_img = 9 if mini else 0
    
    for y in range(8):
        for x in range(8):
            xX = pX + (x*taille)
            yY = pY + (y*taille)
            if VAR.souris[0] == 1 and VAR.souris[1] >= xX and VAR.souris[1] <= xX + taille and VAR.souris[2] >= yY and VAR.souris[2] <= yY + taille:
                VAR.terrain[y][x] = "0" if VAR.terrain[y][x] != "0" else "1"
            
            i = int(VAR.terrain[y][x])
            VAR.fenetre.blit(VAR.img_bloc[i+mini_img], (xX, yY))
            
            
def afficher_pieces_disponibles(pX, pY):
    pX, pY = pX + (8 * 32), pY
    for p in range(3):
        pX += 16
        for y in range(5):
            for x in range(5):
                xX = pX + (x*32)
                yY = pY + (y*32)
            
                if VAR.souris[0] == 1 and VAR.souris[1] >= xX and VAR.souris[1] <= xX + 32 and VAR.souris[2] >= yY and VAR.souris[2] <= yY + 32:
                    VAR.pieces[p][y][x] = "0" if VAR.pieces[p][y][x] != "0" else "1"
                    
                i = 0
                if y < len(VAR.pieces[p]) and x < len(VAR.pieces[p][y]):
                    if VAR.pieces[p][y][x] == "1":
                        i = 3 + p                        
                VAR.fenetre.blit(VAR.img_bloc[i], (xX, yY))   
        pX += 5 * 32
        

def bouton(texte, x, y, longueur=200, hauteur=40, 
           couleur_normal=(100, 100, 200), couleur_clique=(50, 50, 150), 
           couleur_texte=(255, 255, 255), police_taille=24):

    # Obtenir la position de la souris et l'état des boutons
    souris = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()
    result = False
    
    # Définir la couleur du bouton (animation)
    couleur = couleur_normal
    if x < souris[0] < x + longueur and y < souris[1] < y + hauteur:
        if clic[0] == 1:  # Si le bouton est relâché après un clic
            result = True
            couleur = couleur_clique

    # Dessiner le bouton
    pygame.draw.rect(VAR.fenetre, couleur, (x, y, longueur, hauteur))

    # Ajouter le texte sur le bouton
    police = pygame.font.Font(None, police_taille)
    texte_rendu = police.render(texte, True, couleur_texte)
    VAR.fenetre.blit(texte_rendu, (x + (longueur - texte_rendu.get_width()) // 2, 
                                y + (hauteur - texte_rendu.get_height()) // 2))

    
    if result:
        pygame.display.update()
        time.sleep(0.2)
    return result


    
def pause(delais = 1):
    pygame.display.update()
    time.sleep(delais)

def barre_progression(texte, pourcentage, x, y, longueur=300, hauteur=40, 
                      couleur_barre=(100, 200, 100), couleur_fond=(200, 200, 200), 
                      couleur_texte=(0, 0, 0), police_taille=24):
    # S'assurer que le pourcentage reste dans les bornes [0, 100]
    pourcentage = max(0, min(100, pourcentage))

    # Dessiner le fond de la barre
    pygame.draw.rect(VAR.fenetre, couleur_fond, (x, y, longueur, hauteur))

    # Dessiner la barre de progression
    largeur_remplie = int((longueur * pourcentage) / 100)
    pygame.draw.rect(VAR.fenetre, couleur_barre, (x, y, largeur_remplie, hauteur))

    # Ajouter le texte centré
    police = pygame.font.Font(None, police_taille)
    texte_complet = f"{texte} {pourcentage}%"
    texte_rendu = police.render(texte_complet, True, couleur_texte)
    VAR.fenetre.blit(texte_rendu, (x + (longueur - texte_rendu.get_width()) // 2, 
                                   y + (hauteur - texte_rendu.get_height()) // 2))
