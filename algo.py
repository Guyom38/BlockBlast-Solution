

import variables as VAR
import fct as FCT
import interface as IHM



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
                VAR.terrain[ligne][x] = "6"
                
    if (len(liste_colonnes) > 0):
        for ix in range(len(liste_colonnes)):
            for y in range(8):
                colonne = liste_colonnes[ix]            
                VAR.terrain[y][colonne] = "7"
    
    return (len(liste_lignes), len(liste_colonnes))
                
def placement_piece(p, x, y):
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

    