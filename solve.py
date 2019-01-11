#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 08:11:44 2019

@author: 3415104
"""
from grille import *
from function import *
from scipy.optimize import linprog
import random
from Adventurer import *

def policyIteration(dungeon):
    continuer = 1
    
    while continuer:
        conv = 1
        t = 0
        while conv:
            for state in dungeon.getAllStates():
                state.valueBefore.append(state.value)
                if state.decision:
                    state.value = gamma() * sum([state.T[state.decision][state2] * state2.value for state2 in state.getAllNeighbourState(state.decision)])
                else:
                    state.value = gamma() * sum([state.T[state.case.possibleMove[0]][state2] * state2.value for state2 in state.getAllNeighbourState(state.case.possibleMove[0])])
        
            m = [abs(state.value - state.valueBefore[-1]) for state in dungeon.getAllStates()]
            
            #showQ(dungeon, 0)
            if np.max(m)<1e-5:
                conv = 0
            t+=1
            
        for state in dungeon.getAllStates():
            for i in range(len(state.case.possibleMove)):
                action = state.case.possibleMove[i]
                somme = state.R[action] + gamma()*sum([state.T[action][state2] * state2.value for state2 in state.getAllNeighbourState(action)])
                
                if i == 0 or somme > state.value:
                    state.value = somme
                    state.decisionBefore.append(state.decision)
                    state.decision = action
        
        if [0 if state.decision == state.decisionBefore else 1 for state in dungeon.getAllStates()]:
            return dungeon
        
        
def PL(dungeon):
    dic = {}
    states = dungeon.states
    for i in range(len(states)):
        dic[states[i]] = i
    
    c = np.array([1 for i in states])
    actions = ["right", "left", "top", "bottom"]
    b_ub = []
    a_ub = []
    for action in actions:
        for state in states:
            if action in state.case.voisin.keys():
                b_ub.append(-state.R[action])
                voisin = state.getAllNeighbourState(action)
                
                l= []
                for state2 in states:
                    if state2 in voisin:
                        l.append(state.T[action][state2])
                    else:
                        l.append(0.0)
                        
                line = l
                line[dic[state]]-=1
                a_ub.append(line)
    
    bounds = [(-100, 100) for i in states]
    
    res = linprog(c, a_ub, b_ub, bounds = bounds)
    print(res)
    
    for state in states:
        i = 0
        for action in state.case.voisin.keys():
            v = state.R[action] + sum([state.T[action][state2] * res[dic[state2]] for state2 in state.getAllNeighbourState(action)])
            if v > state.value or i== 0:
                state.value = v
                state.decision = action
            i+=1
    return dungeon

def valueIteration(dungeon):
    
    # Lancement de  l'itération à la valeur
    continuer = 1
    t=0
    while continuer:
        for state in dungeon.states:
            for action in state.T.keys():
                        
                q = state.Q[action]
                state.Q[action] = state.R[action] + gamma()*sum([state.T[action][state2] * state2.value for state2 in state.getAllNeighbourState(action)])
                if state.case.i == 0 and state.case.j == 2 and "key" in state.objects and "sword" in state.objects and "treasure" not in state.objects and action=="left":
                    print("Action en cours : "+action)
                    print("Valeur de cette action : "+str(state.R[action]))
                    print([state.T[action][state2] * state2.value for state2 in state.getAllNeighbourState(action)])
                    print(state.value)
                    q = state.Q[action]
                    print(q)
                            
            state.valueBefore.append(state.value)
            state.value = max([val for val in state.Q.values()])
    
        m = [abs(state.value - state.valueBefore[-1]) for state in dungeon.states]
        
        #showQ(dungeon, 0)
        if np.max(m)<1e-5:
            continuer = 0
        t+=1
    
    
    for state in dungeon.states:        
        state.decision = [action for action in state.T.keys() if state.Q[action] == np.max([state.Q[action2] for action2 in state.T.keys()])][0]

    return dungeon

def qlearning(dungeon):
    randomly = 0.2
    nb_episode = 5
    max_step = 5000
    actions = ["right", "left", "top", "bottom"]
    qtable = [[0 for i in actions] for state in dungeon.states]
    
    numberIterationToWin = []
    
    tot = 0
    i = 0
    while i < nb_episode:
        
        tot +=1
        dungeon.adventurer = Adventurer()
        state = dungeon.getState(dungeon.startingPosition, [])
        adventurer = dungeon.adventurer
        adventurer.objects = []
        adventurer.goIn(state.case)
        finish = False
        sumRewards = 0
        
        for j in range(max_step):
            # Choix d'une action
            if random.uniform(0, 1) < randomly**i:
                action = random.choice(list(state.case.voisin.keys()))
            else:
                k = 0
                val = -float("inf")
                for l in range(len(actions)):
                    if qtable[dungeon.states.index(state)][l] > val and actions[l] in state.case.voisin.keys():
                        k = l
                        val = qtable[dungeon.states.index(state)][l]
                action = actions[k]
                
            # Faire cette action
            adventurer.goIn(state.case.voisin[action])
            alive = adventurer.case.action(adventurer)
            
            newState = dungeon.getState(adventurer.case, adventurer.objects)
            if not alive:
                reward = -100
                finish= True
            elif "treasure" in newState.objects and type(newState.case) == StartingPosition:
                reward = 99
                numberIterationToWin.append(j)
                finish = True
                i+=1
                print("finish", i)
            else:
                reward = 0
                
            sumRewards += reward
            qtable[dungeon.states.index(state)][actions.index(action)] = alpha(i) * (reward + gamma() * np.max(qtable[dungeon.states.index(newState)]) - qtable[dungeon.states.index(state)][actions.index(action)])
            
            state = newState
            if finish:
                break
            
    # Créer les décision
    for state in dungeon.states:
        i = dungeon.states.index(state)
        val = -float("inf")
        for action in state.T.keys():
            if qtable[i][actions.index(action)] > val:
                state.decision = action
                val = qtable[i][actions.index(action)]
        
        
        
        
        