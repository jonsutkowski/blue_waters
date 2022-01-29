# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 21:20:49 2021

@author: Jonathan Sutkowski
"""

from scripts.bracket import Bracket
from scripts.teams import Team, Package
from scripts.portfolio import Portfolio

# accepts a float, returns a float rounded to nearest thousandth
def sci(x):
    return int(x*1000 + 0.5)/1000

NUM_BRACKETS = 10000

Team.generate_team_list()

Bracket.generate_brackets(Bracket, n=NUM_BRACKETS)

Portfolio.generate_random_portfolios(number_of_portfolios=1)

wins_by_seed = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
]

for region in [
    [
        "Gonzaga",
        "Alabama",
        "Arkansas",
        "Florida State",
        "Creighton",
        "USC",
        "Oregon",
        "LSU"
    ],
    [
        "Baylor",
        "Ohio State",
        "West Virginia",
        "Purdue",
        "Villanova",
        "Texas Tech",
        "UConn",
        "Loyola Chicago",
    ],
    [
        "Illinois",
        "Iowa",
        "Texas",
        "Oklahoma State",
        "Tennessee",
        "BYU",
        "Clemson",
        "North Carolina",
    ],
    [
        "Michigan",
        "Houston",
        "Kansas",
        "Virginia",
        "Colorado",
        "San Diego State",
        "Florida",
        "Oklahoma"
    ]
]:
    seed = 0
    for team_name in region:
        for team in Team.TEAM_LIST:
            if team_name == team.name:
                foundTeam = True
                break
        if not foundTeam:
            print("couldn't find team", team_name)

        number_of_championships_won = 0
        for bracket in Bracket.BRACKET_LIST:
            if bracket.scoreboard[team] == 48:
                number_of_championships_won += 1
        wins_by_seed[seed] += sci(number_of_championships_won / NUM_BRACKETS)

        seed += 1

seed = 1
print("seed  |  % championships won in NCAA")
for item in wins_by_seed:
    print(seed, "    | ", item)
    seed += 1


# for portfolio in Portfolio.PORTFOLIO_LIST:
#     print(portfolio.name)
#     for team in portfolio.team_list:
#         print(team.name)
#
#     print(len(portfolio.team_list))




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