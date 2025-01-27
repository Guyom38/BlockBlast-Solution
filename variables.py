#https://www.patorjk.com/software/taag/#p=display&f=ANSI%20Regular&t=BOUCLE

import fct as FCT

import pygame
from pygame.locals import *

old_terrain = [[], [], [], []]
terrain = []
terrain.append(["0","0", "0", "0", "0", "0", "0", "0"])
terrain.append(["0","0", "0", "0", "0", "0", "0", "0"])
terrain.append(["0","1", "1", "1", "1", "1", "1", "1"])
terrain.append(["0","0", "0", "1", "1", "1", "1", "1"])
terrain.append(["1","0", "1", "1", "1", "1", "1", "1"])
terrain.append(["1","0", "1", "1", "1", "1", "1", "1"])
terrain.append(["0","0", "0", "0", "0", "0", "0", "1"])
terrain.append(["1","1", "1", "0", "1", "1", "1", "1"])



pieces = []

pieces.append([])
pieces[0].append(["1", "1", "1", "0", "0"])
pieces[0].append(["0", "1", "0", "0", "0"])
pieces[0].append(["0", "0", "0", "0", "0"])
pieces[0].append(["0", "0", "0", "0", "0"])
pieces[0].append(["0", "0", "0", "0", "0"])

pieces.append([])
pieces[1].append(["1", "1", "1", "1", "1"])
pieces[1].append(["0", "0", "0", "0", "0"])
pieces[1].append(["0", "0", "0", "0", "0"])
pieces[1].append(["0", "0", "0", "0", "0"])
pieces[1].append(["0", "0", "0", "0", "0"])

pieces.append([])
pieces[2].append(["0", "1", "0", "0", "0"])
pieces[2].append(["1", "1", "1", "0", "0"])
pieces[2].append(["0", "0", "0", "0", "0"])
pieces[2].append(["0", "0", "0", "0", "0"])
pieces[2].append(["0", "0", "0", "0", "0"])


fenetre = None
img_bloc = None

souris = [0, 0, 0]
boucle = True
tempo = 0
message = ""

logs = []

tmini = 8