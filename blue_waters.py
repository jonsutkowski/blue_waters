# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 21:20:49 2021

@author: Jonathan Sutkowski
"""

import random
from scripts.portfolio import Portfolio

tracker = {}

for i in range(0,50):
    team_array = [random.random(), 0, 0] # winning probability, wins, losses
    tracker[i] = team_array

# Given team A and B's winning probabilities, return 'true' if A randomly won.
# https://sabr.org/journal/article/probabilities-of-victory-in-head-to-head-team-matchups/
def didWin(A, B):
    probability = A * (1 - B) / (A*(1 - B) + B*(1-A))
    
    return random.random() <= probability

# accepts a float, returns a float rounded to nearest thousandth
def sci(x):
    return int(x*1000 + 0.5)/1000

#for t in range(0,1000):
#    for a in tracker:
#        for b in tracker:
#            A = tracker[a][0]
#            B = tracker[b][0]
#
#            did_win = didWin(A, B)
#            
#            if did_win:
#                tracker[a][1] += 1
#                tracker[b][2] += 1
#            else:
#                tracker[a][2] += 1
#                tracker[b][1] += 1

#for i in tracker:
#    array = tracker[i]
#    tracker[i].append(array[1]/(array[1] + array[2]))