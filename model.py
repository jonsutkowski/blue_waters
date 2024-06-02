# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 21:20:49 2021

@author: Jonathan Sutkowski
"""

from random import random
import csv
import numpy as np
import multiprocessing
import datetime
from scripts.bracket import Bracket
from scripts.teams import Team, Package
from scripts.portfolio import Portfolio
from sklearn.manifold import TSNE

class MonteCarloModel:
    from random import random
    import csv
    import numpy as np
    from scripts.bracket import Bracket
    from scripts.teams import Team, Package
    from scripts.portfolio import Portfolio

    # create t-SNE transform (sklearn.manifold.TSNE object). It will get initialized with 100 random portfolios
    # upon the first time plot_portfolios() is run, and the same transform will be used in subsequent plots.
    dimension_reduction_transform = "null"

    def initiate_model(num_brackets = 10000, num_portfolios=1):
        Team.generate_team_list()

        Bracket.generate_brackets(Bracket, n = num_brackets)

        Portfolio.generate_random_portfolios(num_portfolios)

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

    # This makes use of portfolio.py's "find_relative_best_portfolio_from_seed" and uses it in a more "meta" way.
    # It never ends--the user must ctrl+C out of the function when he wants to get out. It continually flushes
    # out objects from RAM to attempt to get higher and higher results.
    def find_best_portfolio(portfolio, points_to_win_bracket=175, number_competitors_per_iteration=5, num_processors=1):
        current_champion = portfolio
        new_champion = None
        while True:
            # Create new random portfolios (the current portfolio is assumed to be at some relative maximum, so we
            # need to "leap" out of the pocket to discover new relative maxima.)
            new_seed_portfolios = []
            for i in range(0, number_competitors_per_iteration):
                new_seed_portfolios.append(
                    Portfolio.generate_random_portfolio_from_seed(current_champion, number_of_teams_to_sell=5)
                )

            # Use these random portfolios as the seeds to search for a relative maximum which can be reached step-wise
            # (ie selling one team at a time)
            print("\nGenerating relative maxima with the following five portfolios:")
            for portfolio in new_seed_portfolios:
                Portfolio.print_portfolio(portfolio, includeTeams=False)
            
            new_relative_best_portfolios_input_arguments = []
            new_relative_best_portfolios = []
            for portfolio in new_seed_portfolios:
                new_relative_best_portfolios_input_arguments.append(
                    [portfolio, points_to_win_bracket]
                )
                new_relative_best_portfolios.append(
                    Portfolio.find_relative_best_portfolio_from_seed(portfolio, points_to_win_bracket)
                )

            # # Run all of the portfolio jobs in parallel (if num_processors is not specified, it as assumed
            # # the user does not want to parallel process)
            # with multiprocessing.Pool(num_processors) as pool:
            #     new_relative_best_portfolios = pool.map(
            #         Portfolio.find_relative_best_portfolio_from_seed,
            #         new_relative_best_portfolios_input_arguments
            #     )

            
            print("\nRelative maxima from the current newest five portfolios:")
            for portfolio in new_relative_best_portfolios:
                Portfolio.print_portfolio(portfolio, includeTeams=False)
            
            # Finally, compare all the contenders for the best relative maximum along with the current_champion. If
            # one of the contenders performs better, it becomes the new champion and the cycle repeats.
            new_champion = current_champion
            new_champion_number_of_wins = Portfolio.get_number_of_wins(new_champion, points_to_win_bracket)
            for portfolio in new_relative_best_portfolios:
                number_of_wins = Portfolio.get_number_of_wins(portfolio, points_to_win_bracket)

                if number_of_wins > new_champion_number_of_wins:
                    new_champion = portfolio
                    new_champion_number_of_wins = Portfolio.get_number_of_wins(new_champion, points_to_win_bracket)
            
            print("\nNew highest-winning relative max portfolio:")
            Portfolio.print_portfolio(new_champion, includeTeams=False)

            if new_champion == current_champion:
                print("\nFound the same highest performing portfolio twice. exiting. Portfolio info:")
                Portfolio.print_portfolio(new_champion)
                break

            # If looping back to generate more portfolios, purge the current list of portfolios by removing all but the top 100.
            # This code TBD.
            highest_scores = np.zeros(100)
            for portfolio in Portfolio.PORTFOLIO_LIST:
                portfolio_score = Portfolio.get_number_of_wins(portfolio, points_to_win_bracket)
                portfolio_has_highest_score = False
                for i in range(0, len(highest_scores)):
                    if portfolio_score > highest_scores[i]:
                        portfolio_has_highest_score = True
                        for j in range(i+1, len(highest_scores)):
                            highest_scores[j] = highest_scores[j - 1]
                        highest_scores[i] = portfolio_score
                
                if not portfolio_has_highest_score:
                    Portfolio.PORTFOLIO_LIST.remove(portfolio)
                    del portfolio
            print("\nUpdate: There are now only", len(Portfolio.PORTFOLIO_LIST), "portfolios on PORTFOLIO_LIST.\n")
        
        return current_champion
            
    def plot_portfolios():
        from mpl_toolkits import mplot3d
        import numpy as np
        import matplotlib.pyplot as plt
        from sklearn.decomposition import PCA
        #import umap

        # Get the data from portfolios
        portfolios_data_to_plot = {
            "standard_deviations": [],
            "averages_of_points_scored": [],
            "number_of_wins": [],
            "portfolio_n64_coords": [],
            "portfolio_dimension_reduced_X_coord": [],
            "portfolio_dimension_reduced_Y_coord": []
        }
        portfolios_data_to_plot["standard_deviations"] = []
        portfolios_data_to_plot["averages_of_points_scored"] = []
        portfolios_data_to_plot["numbers_of_wins"] = []
        for portfolio in Portfolio.PORTFOLIO_LIST:
            points_history = portfolio.points_history

            standard_deviation = np.std(points_history)
            average_points_scored = np.average(points_history)
            number_of_wins = sum(i > 175 for i in points_history)

            portfolios_data_to_plot["standard_deviations"].append(standard_deviation)
            portfolios_data_to_plot["averages_of_points_scored"].append(average_points_scored)
            portfolios_data_to_plot["numbers_of_wins"].append(number_of_wins)

            portfolio_n64_coords = []
            for team in Team.TEAM_LIST:
                if team in portfolio.team_list:
                    portfolio_n64_coords.append(1)
                else:
                    portfolio_n64_coords.append(0)
            portfolios_data_to_plot["portfolio_n64_coords"].append(portfolio_n64_coords)

        # If the dimension_reduction_transform object is "null", generate a transform using a set of
        # randomly generated portfolios. Each of the random portfolios are converted
        # into a 64-variable data point (a "1" or "0" for each team)
        if MonteCarloModel.dimension_reduction_transform == "null":
            baseline_n64_coords = []
            random_portfolios = Portfolio.generate_random_portfolios(100)
            for portfolio in random_portfolios:
                portfolio_n64_coords = []
                for team in Team.TEAM_LIST:
                    if team in portfolio.team_list:
                        portfolio_n64_coords.append(1)
                    else:
                        portfolio_n64_coords.append(0)
                baseline_n64_coords.append(portfolio_n64_coords)
            baseline_n64_coords = np.array(baseline_n64_coords)
            MonteCarloModel.dimension_reduction_transform = TSNE(n_components=2)
            MonteCarloModel.dimension_reduction_transform.fit(baseline_n64_coords)

        portfolio_n64_coords = portfolios_data_to_plot["portfolio_n64_coords"]
        #umap_transformer = umap.UMAP(n_neighbors=5, min_dist=0.1)
        #umap_transformer.fit_transform(baseline_n64_coords)
        #portfolio_n2_coords = umap_transformer.transform(portfolio_n64_coords)
        #pca = PCA(n_components=2)
        #pca.fit(baseline_n64_coords)
        portfolio_n64_coords = np.array(portfolio_n64_coords)
        portfolio_n2_coords = MonteCarloModel.dimension_reduction_transform.fit_transform(portfolio_n64_coords)
        for n2_coord in portfolio_n2_coords:
            portfolios_data_to_plot["portfolio_dimension_reduced_X_coord"].append(n2_coord[0])
            portfolios_data_to_plot["portfolio_dimension_reduced_Y_coord"].append(n2_coord[1])

        ## Plot the data

        fig = plt.figure()
        ax = plt.axes(projection='3d')

        xdata = portfolios_data_to_plot["portfolio_dimension_reduced_X_coord"]
        ydata = portfolios_data_to_plot["portfolio_dimension_reduced_Y_coord"]
        zdata = portfolios_data_to_plot["numbers_of_wins"]
        ax.scatter3D(xdata, ydata, zdata)
        plt.show()
        plt.pause(3)

    def export_team_data():
        # Get all the team data
        output_array = []
        for team in Team.TEAM_LIST:
            new_row = []

            new_row.append(team.name)
            for bracket in Bracket.BRACKET_LIST:
                new_row.append(bracket.scoreboard[team])
            
            output_array.append(new_row)

        # Transpose the array
        transposed_output_array = []
        for j in range(0, len(output_array[0])):
            new_row = []
            for i in range(0, len(output_array)):
                new_row.append(output_array[i][j])
            transposed_output_array.append(new_row)
        
        # Save it to csv
        filename = "blue_waters_team_data.csv"   # Create the output filename
        csvfile = open(filename, "w+", newline='')                  # create the file
        csvWriter = csv.writer(csvfile, delimiter=',')
        csvWriter.writerows(transposed_output_array)                           # load the data into the file
        
        return

    def generate_expected_values(printValues=False):
        output_array = []
        output_array.append(["Name", "Expected_value", "ROI"])
        for team in Team.TEAM_LIST:
            sum = 0
            n = 0
            for bracket in Bracket.BRACKET_LIST:
                sum += bracket.scoreboard[team]
                n += 1

            expected_value = sum / n
            price = team.price
            if type(team.price) == Package:
                continue

            ROI = expected_value / price
            output_array.append([team.name, str(expected_value), str(ROI)])
        for package in Package.PACKAGE_LIST:
            package_expected_value = 0
            for team in package.team_list:
                sum = 0
                n = 0
                for bracket in Bracket.BRACKET_LIST:
                    sum += bracket.scoreboard[team]
                    n += 1

                expected_value = sum / n

                package_expected_value += expected_value
            package_ROI = package_expected_value / package.price
            output_array.append([package.name, str(package_expected_value), str(package_ROI)])

        # print expected values.
        if printValues:
            for line in output_array:
                print(line)

        # save expected values to csv.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        output_file = "output_data/" + timestamp + "_expected_values.csv"
        csvfile = open(output_file, "w+", newline='')                  # create the file
        csvWriter = csv.writer(csvfile, delimiter=',')
        csvWriter.writerows(output_array)                           # load the data into the file

if __name__ == "__main__":
    MonteCarloModel.initiate_model(num_brackets=10000, num_portfolios=500)
    initial_portfolio = MonteCarloModel.Portfolio.new_portfolio([
        "Alabama",                                         # price: 21
        "Baylor",                                          # price: 10
        "Drake",                                           # price: <scripts.teams.Package object at 0x7f0dba1c9580>
        "Illinois",                                        # price: 2
        "Iona",                                            # price: <scripts.teams.Package object at 0x7f0dae99fc70>
        "Kansas",                                          # price: 20
        "Kennesaw St.",                                    # price: <scripts.teams.Package object at 0x7f0dba1d8cd0>
        "Kent St.",                                        # price: 1
        "Kentucky",                                        # price: 4
        "Lousiana",                                        # price: <scripts.teams.Package object at 0x7f0dae99fc70>
        "Marquette",                                       # price: 14
        "Miami",                                           # price: 5
        "Missouri",                                        # price: 3
        "Northern Kentucky",                               # price: <scripts.teams.Package object at 0x7f0dae99fc70>
        "Oral Roberts",                                    # price: <scripts.teams.Package object at 0x7f0dba1d8cd0>
        "TCU",                                             # price: 4
        "Tennessee",                                       # price: 6
        "UNC Asheville",                                   # price: <scripts.teams.Package object at 0x7f0dba1c9580>
        "USC",                                             # price: <scripts.teams.Package object at 0x7f0dae99fc70>
        "VCU",                                             # price: 1
        "Virginia"                                         # price: 5
    ])
    initial_portfolio.name = "Initial Portfolio"

    MonteCarloModel.plot_portfolios()

    exit(0)

    #initial_portfolio.print_portfolio()
    while True:
        best_portfolio = MonteCarloModel.Portfolio.find_relative_best_portfolio_from_seed(initial_portfolio)
        #best_portfolio.print_portfolio()

    MonteCarloModel.export_team_data()
    MonteCarloModel.print_win_rates_by_regional_seed()

    initial_best_portfolio = Portfolio.find_relative_best_portfolio_from_seed(Portfolio.PORTFOLIO_LIST[0])
    portfolio = Portfolio.PORTFOLIO_LIST[0]

    portfolio.find_relative_best_portfolio_from_seed(portfolio)
    for n in range(0,100):
        Portfolio.generate_random_portfolio_from_seed(portfolio).name
    
    print("Plotting portfolios:")
    MonteCarloModel.plot_portfolios()
