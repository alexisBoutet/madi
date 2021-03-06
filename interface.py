# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *
from grille import *
from function import *
from solve import *

"""
Affichage
"""
# Affiche les décisions en fonctions d'une liste d'objet
def afficheDecision(dungeon, objects, do_blit=False):
    actions = ["right", "left", "top", "bottom"]
    pygame.init()
    tailleX = 60
    tailleY = 36
    fenetre = pygame.display.set_mode((len(dungeon.cases[0]) * tailleX, len(dungeon.cases) * tailleY))
    imagedecisions = {action:pygame.image.load(action+".png").convert_alpha() for action in actions}
    print(imagedecisions)
    image = [[0 for i in ligne] for ligne in dungeon.cases]
    for i in range(len(dungeon.cases)):
        for j in range(len(dungeon.cases[0])): 
            case = dungeon.cases[i][j]
            image[i][j] = pygame.image.load(case.image).convert()
            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
            # Si on a un choix à faire dans la case
            if type(case) not in [Wall, Cracks, MovingPlatform, MagicPortal]:
                state = dungeon.getState(case, objects)
                # Si il y a une décision et quel a été calculé
                if state.decision and state.value != 0.0:
                    fenetre.blit(imagedecisions[state.decision], (j*tailleX,i*tailleY))
     
    continuer = 1
    #Boucle infinie
    if do_blit:
        while continuer:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT:     #Si un de ces événements est de type QUIT
                    continuer = 0      #On arrête la boucle
                
                if event.type == KEYDOWN:
                    
                    if event.key == K_KP0:
                        continuer = 0
                        afficheDecision(dungeon, dungeon.possibleSac[0], True)
                        
                    if event.key == K_KP1:
                        continuer = 0
                        afficheDecision(dungeon, dungeon.possibleSac[1], True)
                        
                    if event.key == K_KP2:
                        continuer = 0
                        afficheDecision(dungeon, dungeon.possibleSac[2], True)
                        
                    if event.key == K_KP3:
                        continuer = 0
                        afficheDecision(dungeon, dungeon.possibleSac[3], True)
                        
                    if event.key == K_KP4:
                        continuer = 0
                        afficheDecision(dungeon, dungeon.possibleSac[4], True)
                        
                    if event.key == K_KP5:
                        continuer = 0
                        afficheDecision(dungeon, dungeon.possibleSac[5], True)
                        
            pygame.display.flip()
 
# Permet de jouer au jeu seul et de demander de l'aide avec espace si un des algorithmes a été lancé
def jouer(dungeon):
    pygame.init()
    tailleX = 60
    tailleY = 36
    fenetre = pygame.display.set_mode((len(dungeon.cases) * tailleX, len(dungeon.cases[0]) * tailleY))
    perso = pygame.image.load("perso.png").convert_alpha()
    image = [[0 for i in ligne] for ligne in dungeon.cases]
    for i in range(len(dungeon.cases)):
        for j in range(len(dungeon.cases[0])): 
            case = dungeon.cases[i][j]
            image[i][j] = pygame.image.load(case.image).convert()
            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
    
    i, j = dungeon.startingPosition.i, dungeon.startingPosition.j
    fenetre.blit(perso, (j*tailleX,i*tailleY))
    adventurer = dungeon.adventurer
    adventurer.goIn(dungeon.startingPosition)
    adventurer.objects = []
    state = dungeon.getState(dungeon.startingPosition, adventurer.objects)
    
    continuer = 1
    #Boucle infinie
    while continuer:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
                
            
                
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if "left" in case.voisin.keys():
                        case = case.voisin["left"]
                if event.key == K_RIGHT:
                    if "right" in case.voisin.keys():
                        case = case.voisin["right"]                 
                if event.key == K_UP:
                    if "top" in case.voisin.keys():
                        case = case.voisin["top"]                 
                if event.key == K_DOWN:
                    if "bottom" in case.voisin.keys():
                        case = case.voisin["bottom"]   
                
                # Si on souhaite avoir de l'aide
                if event.key == K_SPACE:
                    if state.decision:
                        case = case.voisin[state.decision]
                        
                adventurer.goIn(case)
                alive = adventurer.case.action(adventurer)
                if not alive:
                    adventurer.goIn(dungeon.startingPosition)
                    adventurer.objects = []
 
                case = adventurer.case
                # Evenement de la pièce
                state = dungeon.getState(case, adventurer.objects)
                for i in range(len(dungeon.cases)):
                    for j in range(len(dungeon.cases[0])):
                        fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
            
            
                    """ Quel état on est """
                    #state.afficher()

            
                    #print(state.objects)
                fenetre.blit(perso, (state.case.j*tailleX,state.case.i*tailleY))
        #Rafraîchissement de l'écran
        pygame.display.flip()
           
def affiche(dungeon):
    pygame.init()
    tailleX = 60
    tailleY = 36
    fenetre = pygame.display.set_mode((len(dungeon.cases[0]) * tailleX, len(dungeon.cases) * tailleY))
    perso = pygame.image.load("perso.png").convert_alpha()
    image = [[0 for i in ligne] for ligne in dungeon.cases]
    for i in range(len(dungeon.cases)):
        for j in range(len(dungeon.cases[0])): 
            case = dungeon.cases[i][j]
            image[i][j] = pygame.image.load(case.image).convert()
            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
    
    i, j = dungeon.startingPosition.i, dungeon.startingPosition.j
    fenetre.blit(perso, (j*tailleX,i*tailleY))
    adventurer = dungeon.adventurer
    adventurer.goIn(dungeon.startingPosition)
    adventurer.objects = []
    state = dungeon.getState(dungeon.startingPosition, adventurer.objects)
    
    continuer = 1
    #Boucle infinie 
    display_decisions = False
    while continuer:
        pygame.time.Clock().tick(30)
        case = adventurer.case
        state = dungeon.getState(case, adventurer.objects)

        for i in range(len(dungeon.cases)):
            for j in range(len(dungeon.cases[0])):
                fenetre.blit(image[i][j], (j*tailleX,i*tailleY))

        if display_decisions:
            afficheDecision(dungeon, dungeon.adventurer.objects)

        fenetre.blit(perso, (state.case.j*tailleX,state.case.i*tailleY))
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle

            if event.type == KEYDOWN:
                if event.key == K_SPACE: 
                    adventurer.goIn(case.voisin[state.decision])
                    adventurer.case.action(adventurer)

			
                if event.key == K_o:
                    display_decisions = not display_decisions


 

                    #state.afficher()
                    #print(state.objects)
        #Rafraîchissement de l'écran
        pygame.display.flip()


nom = "generate55.txt"
#generateDungeon(5, 5, nom)
dungeon = Dungeon()
dungeon.open(nom)
dungeon.instanciation(Adventurer(), False)
qlearning(dungeon)
#PL(dungeon)
#valueIteration(dungeon)
saveDecision(dungeon, "Resultat"+nom)
affiche(dungeon)
