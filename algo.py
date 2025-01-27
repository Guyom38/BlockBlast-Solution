
import os
import variables as VAR
import fct as FCT
import interface as IHM


import itertools
import copy

# --------------------------------------------------------------------------------------------------
def chercher_lignes_et_colonnes():
    lignes = []
    for y in range(8):
        carre = 0
        for x in range(8):
            if VAR.terrain[y][x] != "0":
                carre += 1
                        
        if carre == 8:
            lignes.append(y)
            
    colonnes = []
    for x in range(8):
        carre = 0
        for y in range(8):
            if VAR.terrain[y][x] != "0":
                carre += 1
        
        if carre == 8:
            colonnes.append(x)
            
    return detruits_lignes_et_colonnes(lignes, colonnes)

# --------------------------------------------------------------------------------------------------
def detruits_lignes_et_colonnes(liste_lignes, liste_colonnes):
    if (len(liste_lignes) > 0):
        for iy in range(len(liste_lignes)):
            for x in range(8):
                ligne = liste_lignes[iy]            
                VAR.terrain[ligne][x] = "8"
                
    if (len(liste_colonnes) > 0):
        for ix in range(len(liste_colonnes)):
            for y in range(8):
                colonne = liste_colonnes[ix]            
                VAR.terrain[y][colonne] = "8"
    
    return (len(liste_lignes), len(liste_colonnes))
                
def placement_piece(p, x, y):
    """
    Tente de placer une pièce sur le terrain en fonction de ses coordonnées et de sa forme.
    
    :param p: Index de la pièce à placer (dans la liste VAR.pieces).
    :param x: Coordonnée x (colonne) de la position de départ sur le terrain.
    :param y: Coordonnée y (ligne) de la position de départ sur le terrain.
    :return: True si le placement est réussi, False sinon.
    
    Fonctionnement :
    1. Vérifie si la pièce peut être placée sans dépasser les limites du terrain 
       ou entrer en conflit avec des cases déjà occupées.
    2. Si le placement est valide, modifie le terrain en y ajoutant les valeurs de la pièce.
    3. Retourne `True` en cas de succès, ou `False` si le placement est impossible.
    """
    
    # Étape 1 : Vérifier si le placement est valide
    for yb in range(len(VAR.pieces[p])):  # Parcourt les lignes de la pièce
        for xb in range(len(VAR.pieces[p][yb])):  # Parcourt les colonnes de la pièce
            if VAR.pieces[p][yb][xb] == "1":  # Si la case de la pièce est occupée
                # Vérifier si on dépasse les limites du terrain
                if x + xb >= 8 or y + yb >= 8: 
                    return False
                # Vérifier si la case correspondante sur le terrain est déjà occupée
                if VAR.terrain[y + yb][x + xb] != "0":
                    return False    
    
    # Étape 2 : Appliquer les modifications au terrain
    for yb in range(len(VAR.pieces[p])):  # Parcourt les lignes de la pièce
        for xb in range(len(VAR.pieces[p][yb])):  # Parcourt les colonnes de la pièce
            # Si la case de la pièce est occupée et que la case sur le terrain est vide
            if VAR.pieces[p][yb][xb] == "1" and VAR.terrain[y + yb][x + xb] == "0":
                # Marquer la case sur le terrain avec une valeur unique
                VAR.terrain[y + yb][x + xb] = str(3 + p)
    
    # Étape 3 : Retourner le succès
    return True

    
        
def effacer_placement(p):
     for y in range(8):
         for x in range(8):
             if VAR.terrain[y][x] == str(3 + p):
                VAR.terrain[y][x] = "0"

                           
def test_placement_piece(p):
    old_terrain = [ligne.copy() for ligne in VAR.terrain]
    
    if p == 3:
        return True
    
    for y in range(8):
        for x in range(8):
            
            IHM.afficher_grille(0, 300+(p*140), True)
            cool = placement_piece(p, x, y)
            print((p, x, y, cool))
            
            
            if cool:
                chercher_lignes_et_colonnes()       
                IHM.afficher_grille(140, 300+(p*140), True)
                            
            
            if cool:
                effacer_placement(4)
                effacer_placement(5)
                IHM.afficher_grille(300, 300+(p*140), True) 

                if p == 0:
                    if test_placement_piece(p+1):
                        valide_piece()  
                    else:
                        VAR.terrain = [ligne.copy() for ligne in old_terrain]     
            else:
                VAR.terrain = [ligne.copy() for ligne in old_terrain]

                
    return False
                 
                 
                 
def valide_piece():
    pX = 16
    IHM.afficher_grille(pX, 10 * 32, True) 
    
    for y in range(8):
        for x in range(8):      
            if int(VAR.terrain[y][x]) > 0:
                VAR.terrain[y][x] = "1"    
    
    pX += (16 * 8) + 16
    IHM.afficher_grille(pX, 10 * 32, True) 
 
    chercher_lignes_et_colonnes()
    
    pX += (16 * 8) + 16
    IHM.afficher_grille(pX, 10 * 32, True)

    effacer_placement(4)
    effacer_placement(5)
   
    pX += (16 * 8) + 16
    IHM.afficher_grille(pX, 10 * 32, True)



def score_terrain():
    """
    Calcule le score du terrain actuel en comptant le nombre de lignes et colonnes pleines.
    :return: Nombre total de lignes et colonnes détruites.
    """
    lignes, colonnes = 0, 0

    # Compter les lignes pleines
    for y in range(8):
        if all(VAR.terrain[y][x] != "0" for x in range(8)):
            lignes += 1

    # Compter les colonnes pleines
    for x in range(8):
        if all(VAR.terrain[y][x] != "0" for y in range(8)):
            colonnes += 1

    return lignes + colonnes


def test_combinaisons():
    pX, pY = 16, 400
    """
    Teste toutes les combinaisons possibles de placement des pièces pour maximiser les lignes/colonnes détruites.
    """
    best_score = 0
    best_terrain = None
    best_permutation = None

    # Générer toutes les permutations possibles des pièces
    for permutation in itertools.permutations(range(3)):
        # Sauvegarder l'état initial du terrain
        original_terrain = [row.copy() for row in VAR.terrain]

        valid = True
        for piece_index in permutation:
            piece_placed = False
            for y in range(8):
                for x in range(8):
                    if placement_piece(piece_index, x, y):
                        piece_placed = True
                        IHM.afficher_grille(pX, pY, True)
                        pX += 140
                        chercher_lignes_et_colonnes()  # Éliminer les lignes/colonnes pleines
                                        
                        IHM.afficher_grille(pX, pY, True)
                        IHM.pause()
                        
                        pX += 140
                        if pX > 800:
                            pY += 140
                            pX = 16
                        if pY > 700:
                            pY = 250
                            pX = 16
                        break
                if piece_placed:
                    break

            # Si une pièce ne peut pas être placée, cette permutation échoue
            if not piece_placed:
                valid = False
                break

        # Calculer le score si la permutation est valide
        if valid:
            current_score = score_terrain()
            if current_score > best_score:
                best_score = current_score
                best_terrain = [row.copy() for row in VAR.terrain]
                best_permutation = permutation

        # Restaurer le terrain initial
        VAR.terrain = [row.copy() for row in original_terrain]

    # Appliquer la meilleure permutation trouvée
    if best_permutation:
        VAR.terrain = best_terrain
        print(f"Meilleure permutation : {best_permutation} avec un score de {best_score}")
    else:
        print("Aucune solution trouvée.")
