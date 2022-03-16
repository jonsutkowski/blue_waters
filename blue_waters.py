# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 21:20:49 2021

@author: Jonathan Sutkowski
"""

from scripts.bracket import Bracket
from scripts.teams import Team, Package
from scripts.portfolio import Portfolio

class BlueWaters:

    def initiate_model(num_brackets = 10000):
        Team.generate_team_list()

        Bracket.generate_brackets(Bracket, n = num_brackets)

        Portfolio.generate_random_portfolios(number_of_portfolios=100)

    def print_win_rates_by_regional_seed():
        # Get the number of brackets
        NUM_BRACKETS = len(Bracket.BRACKET_LIST)

        # accepts a float, returns a float rounded to nearest thousandth
        def sci(x):
            return int(x*1000 + 0.5)/1000

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
        
        index = 0
        region_1 = []
        region_2 = []
        region_3 = []
        region_4 = []
        for team in Team.TEAM_LIST:
            index += 1
            if index in range(1, 17):
                region_1.append(team)
            if index in range(17, 33):
                region_2.append(team)
            if index in range(33, 49):
                region_3.append(team)
            if index in range(49, 65):
                region_4.append(team)

        def get_top_8_teams(region):
            sorted = False
            while sorted == False:
                sorted = True

                for i in range(0, len(region) - 1):
                    team_i = region[i]
                    team_iplus1 = region[i+1]

                    if team_i.true_seed > team_iplus1.true_seed:
                        sorted = False
                        region[i] = team_iplus1
                        region[i+1] = team_i
            
            output_regions = []
            for team in region[0:8]:
                output_regions.append(team.name)

            return output_regions

        regions = [
            get_top_8_teams(region_1),
            get_top_8_teams(region_2),
            get_top_8_teams(region_3),
            get_top_8_teams(region_4)
        ] 

        for region in regions:
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

    # Given some portfolio, crawl around by selling one team at a time until
    # a portfolio is found that is a 'local minima' (no one-team swap will
    # improve the score)
    def find_best_portfolio(portfolio, points_to_win_bracket=175):
        # Generate a bunch of random portfolios one 'step' away from the initial portfolio
        new_portfolios = []
        for i in range(0, 200):
            new_portfolios.append(Portfolio.generate_random_portfolio_from_seed(portfolio, number_of_teams_to_sell = 1))
        
        # Add the 'old' portfolio to the list of portfolios (just in case that is the highest-winning portfolio)
        new_portfolios.append(portfolio)
        
        max_number_of_wins = 0
        current_portfolio_champ = None
        for portfolio in new_portfolios:
            current_portfolio_number_of_wins = 0
            for point_value in portfolio.points_history:
                if point_value >= points_to_win_bracket:
                    current_portfolio_number_of_wins += 1
            
            if current_portfolio_number_of_wins > max_number_of_wins:
                max_number_of_wins = current_portfolio_number_of_wins
                current_portfolio_champ = portfolio

        if current_portfolio_champ == portfolio:
            return portfolio
        else:
            return BlueWaters.find_best_portfolio(current_portfolio_champ)

if __name__ == "__main__":
    BlueWaters.initiate_model(10000)

    BlueWaters.print_win_rates_by_regional_seed()

    random_portfolios = Portfolio.PORTFOLIO_LIST[:]

    for portfolio in random_portfolios:
        BlueWaters.find_best_portfolio(portfolio)
    
    Portfolio.plot_portfolios()


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