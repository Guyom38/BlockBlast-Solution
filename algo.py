

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
    for (xb, yb) in VAR.pieces_composition[p]:
        if x + xb >= 8 or y + yb >= 8: 
            return False
        if VAR.terrain[y + yb][x + xb] != "0":
            return False    
    
    # Étape 2 : Appliquer les modifications au terrain
    for (xb, yb) in VAR.pieces_composition[p]:
        if VAR.terrain[y + yb][x + xb] == "0":
            VAR.terrain[y + yb][x + xb] = str(3 + p)

    return True


# --------------------------------------------------------------------------------------------------
def chercher_lignes_et_colonnes2():
    # Trouver les lignes complètement remplies
    lignes = [y for y in range(8) if all(VAR.terrain[y][x] != "0" for x in range(8))]

    # Trouver les colonnes complètement remplies
    colonnes = [x for x in range(8) if all(VAR.terrain[y][x] != "0" for y in range(8))]

    # Détruire les lignes et colonnes trouvées
    return detruits_lignes_et_colonnes(lignes, colonnes)

# --------------------------------------------------------------------------------------------------
def detruits_lignes_et_colonnes2(liste_lignes, liste_colonnes):
    # Détruire les lignes
    for ligne in liste_lignes:
        VAR.terrain[ligne] = ["6"] * 8  # Remplace toute la ligne par "6"

    # Détruire les colonnes
    for colonne in liste_colonnes:
        for y in range(8):
            VAR.terrain[y][colonne] = "7"  # Remplace chaque case de la colonne par "7"

    return len(liste_lignes), len(liste_colonnes)