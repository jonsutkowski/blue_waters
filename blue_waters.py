# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 21:20:49 2021

@author: Jonathan Sutkowski
"""

from scripts.bracket import Bracket
from scripts.teams import Team, Package

Team.generate_team_list()

Bracket.generate_brackets(Bracket, n=100000)


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