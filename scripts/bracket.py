# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:01:45 2021

@author: Jonathan Sutkowski
"""
# Import libraries
import random
from scripts.spreadsheet import Spreadsheet
from scripts.teams import Team, Package

class Bracket:
    # master list of all brackets
    BRACKET_LIST = []

    # Important parameter! This indicates how many points a team earns based on the number of
    # wins during the tournament,
    WIN_TO_POINTS_DICTIONARY = {
        0 : 0,
        1 : 4,
        2 : 8,
        3 : 16,
        4 : 24,
        5 : 36,
        6 : 48
    }

    ## VARIOUS FUNCTIONS

    # Given team A and B's winning probabilities, return 'true' if A randomly won.
    # https://sabr.org/journal/article/probabilities-of-victory-in-head-to-head-team-matchups/
    def didWin(A, B):
        probability = A * (1 - B) / (A * (1 - B) + B * (1 - A))

        return random.random() <= probability

    # generate_brackets will create n bracket objects. It assumes input_data/menu.csv is ordered such that
    # the first team listed plays the second team, the winner of the first two teams plays the winner of the
    # second two teams, and so on.
    def generate_brackets(self, n=100):
        for i in range(0, n):
            # create a list of teams ordered as described above.
            remaining_teams = Team.TEAM_LIST[:]
            full_bracket = [ remaining_teams[:] ]

            while len(remaining_teams) > 1:
                # create a new list for the teams that move on to the next round.
                teams_to_continue_to_next_round = []

                # Iterate through every pair of teams and have them "play" each other (pit their win_ratios against
                # each other and say who wins with some calculated probability)
                for n in range(0, int(len(remaining_teams)/2)):
                    team_a = remaining_teams[2*n]
                    team_b = remaining_teams[2*n + 1]

                    if Bracket.didWin(team_a.win_ratio, team_b.win_ratio):
                        teams_to_continue_to_next_round.append(team_a)
                    else:
                        teams_to_continue_to_next_round.append(team_b)

                remaining_teams = teams_to_continue_to_next_round[:]
                full_bracket.append(teams_to_continue_to_next_round[:])

            # Create the scoreboard dictionary, which will first store the number of wins for each team, and then
            # will be converted to store the number of points earned for each team.
            scoreboard = {}
            for team in Team.TEAM_LIST:
                scoreboard[team] = 0

            for winning_team_list in full_bracket[1:]:  # Iterate through each round, starting with competitors in round 2
                for team in winning_team_list:          # Add one victory to each team in the current round
                    scoreboard[team] += 1

            for team in scoreboard.keys():
                num_wins = scoreboard[team]
                scoreboard[team] = Bracket.WIN_TO_POINTS_DICTIONARY[num_wins]   # convert num_wins to POINTS

            # Create bracket object to store this information in.
            bracket = Bracket()
            bracket.full_bracket = full_bracket
            bracket.scoreboard = scoreboard

        return

    # Function for instantiation of a Bracket Object
    def __init__(self):
        # add instance variables
        self.scoreboard = None  # A dictionary mapping each team object to the amount of points that team scored.
        self.full_bracket = None # A list of lists of teams, one for each round of the tournament.

        # add to PACKAGE_LIST
        Bracket.BRACKET_LIST.append(self)

        return