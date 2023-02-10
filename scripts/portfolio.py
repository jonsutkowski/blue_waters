# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:01:45 2021

@author: Jonathan Sutkowski
"""
# Import libraries
import random
import os
import webbrowser
import time
import itertools
from scripts.spreadsheet import Spreadsheet
from scripts.teams import Team, Package
from scripts.bracket import Bracket

class Portfolio:
    # master list of all portfolios
    PORTFOLIO_LIST = []

    # Starting balance
    STARTING_BALANCE = 100

    ## VARIOUS FUNCTIONS

    def get_portfolio_by_name(name):
        for portfolio in Portfolio.PORTFOLIO_LIST:
                if name == portfolio.name:
                        return portfolio
        return 'Null'
    
    # Create a Portfolio object for every possible combination of teams one can buy.
    def generate_all_portfolios():
        # Generate list of all teams that are not available in packages, and all packages.
        # (basically, everything that has a price tag)
        menu = []
        for team in Team.TEAM_LIST:
            if type(team.price) == int:
                menu.append(team)

        for package in Package.PACKAGE_LIST:
            menu.append(package)

        global max
        max = 0
        global start_time
        start_time = time.time()

        # Generate list of each possible combination of teams/packages to buy.
        def generate_purchase_combinations(menu, current_balance):
            # If the menu is empty, return empty list
            if len(menu) == 0:
                return []

            # If the menu is not empty, first check if the current_balance can
            # purchase everything remaining on the menu. If it can, just return
            # a list containing the one potential combination: namely, the entire
            # menu.
            total_menu_cost = 0
            for item in menu:
                total_menu_cost += int(item.price)
            if current_balance >= total_menu_cost:
                return [ menu ]

            # If there is not enough to buy every single team, generate two lists:
            # one of all the combinations of teams if we buy the first team on the menu,
            # the other all the combinations of teams if we do not.
            purchase_combinations = []
            first_item_on_menu = menu[0]
            menu_without_first_item = menu[1:]
            balance_if_purchase_first_item = current_balance - int(first_item_on_menu.price)

            for purchase_combination in generate_purchase_combinations(menu_without_first_item, current_balance):
                purchase_combinations.append(purchase_combination)

            if balance_if_purchase_first_item >= 0:
                for purchase_combination in generate_purchase_combinations(menu_without_first_item, \
                                                                           balance_if_purchase_first_item):
                    purchase_combinations.append([first_item_on_menu] + purchase_combination)

            global max
            if len(purchase_combinations) > max:
                print(len(purchase_combinations), time.time() - start_time)
                max = len(purchase_combinations)

            return purchase_combinations

        # generate list of portfolio names.
        portfolio_names = []
        for row in Spreadsheet.read_csv("input_data/name_bank.csv"):
            portfolio_names.append(row[0].strip() + " #" + str(random.randint(1, 1000)))
        random.shuffle(portfolio_names) # "shuffle the deck" of portfolio names

        # loop through each possible combination of purchases. Create a portfolio object for each one.
        for purchase_combination in generate_purchase_combinations(menu, Portfolio.STARTING_BALANCE):
            new_portfolio = Portfolio.new_portfolio()
            try:
                new_portfolio.name = portfolio_names[0]
                portfolio_names = portfolio_names[1:]
            except:
                new_portfolio.name = "Un-named Portfolio"

            new_portfolio.package_list = []
            new_portfolio.team_list = []
            for item in purchase_combination:
                if type(item) == Package:
                    new_portfolio.package_list.append(item)
                    for team in item.team_list:
                        new_portfolio.team_list.append(team)
                if type(item) == Team:
                    new_portfolio.team_list.append(item)

        return

    # Generate list of random portfolios
    def generate_random_portfolios(number_of_portfolios=1):
        import time
        # generate list of portfolio names.
        portfolio_names = []
        for row in Spreadsheet.read_csv("input_data/name_bank.csv"):
            portfolio_names.append(row[0].strip() + " #" + str(random.randint(1, 1000)))
        random.shuffle(portfolio_names) # "shuffle the deck" of portfolio names

        # Generate list of all teams that are not available in packages, and all packages.
        # (basically, everything that has a price tag)
        menu = []
        for team in Team.TEAM_LIST:
            if type(team.price) == int:
                menu.append(team)

        for package in Package.PACKAGE_LIST:
            menu.append(package)

        # Create n random portfolio objects.
        new_portfolios = []
        for i in range(0, number_of_portfolios):
            start_time = time.time()

            # Create randomized menu
            shuffled_menu = menu[:]
            random.shuffle(shuffled_menu)

            # Set initial amount of spending money to the default value.
            spending_money = Portfolio.STARTING_BALANCE

            # Instantiate list of teams for the new random portfolio
            new_team_list = []

            # Buy each affordable item in the randomized menu in order.
            while len(shuffled_menu) > 0 and spending_money > 0:
                next_item_on_menu = shuffled_menu[0]
                shuffled_menu = shuffled_menu[1:]

                if spending_money >= int(next_item_on_menu.price):
                    spending_money -= int(next_item_on_menu.price)
                    if type(next_item_on_menu) == Package:
                        for team in next_item_on_menu.team_list:
                            new_team_list.append(team)
                    if type(next_item_on_menu) == Team:
                        new_team_list.append(next_item_on_menu)

            # Create new portfolio object for team list
            new_portfolio = Portfolio.new_portfolio(new_team_list)

            print("Generated", new_portfolio.name, "in", int(time.time() - start_time), "seconds")
            new_portfolios.append(new_portfolio)

        # populate each portfolio object with the amount of points scored in each bracket
        for bracket in Bracket.BRACKET_LIST:
            for portfolio in Portfolio.PORTFOLIO_LIST:

                # Count how many points were scored by each team in the portfolio.
                points_scored_in_bracket = 0
                for team in portfolio.team_list:
                    points_scored_in_bracket += bracket.scoreboard[team]

                # add that score to the portfolio's 'points_history' value.
                portfolio.points_history.append(points_scored_in_bracket)

        return new_portfolios

    # Given a portfolio, create random "deviances" from the portfolio and return a list
    def generate_random_portfolio_from_seed(seed_portfolio, number_of_teams_to_sell=1):
        # get initial seed team list
        seed_team_list = seed_portfolio.team_list[:]

        # ensure there will not be a list index error
        if number_of_teams_to_sell > len(seed_team_list):
            number_of_teams_to_sell = len(seed_team_list) - 1

        # find out how much money the seed team list is worth
        seed_team_dollar_value = 0
        for team in seed_team_list:
            if type(team.price) == int:
                seed_team_dollar_value += team.price
        for package in seed_portfolio.package_list:
            for package_i in Package.PACKAGE_LIST:
                if package == package_i.name:
                    package = package_i
            seed_team_dollar_value += package.price

        potential_buys = [] # list of teams to potentially buy. important to do this step before the teams to be removed have been removeed from seed_team_list
        for team in Team.TEAM_LIST:
            if team not in seed_team_list:
                potential_buys.append(team)

        # sell 'number_of_teams_to_sell' teams at random
        random.shuffle(seed_team_list)

        available_budget = Portfolio.STARTING_BALANCE - seed_team_dollar_value
        removed_teams = []
        for i in range(0, number_of_teams_to_sell):
            team = seed_team_list[i]
            if type(team.price) == int:
                seed_team_list.remove(team) # If it is a solo team, just remove the team, and add the team's price tag to the available budget.
                removed_teams.append(team)
                available_budget += team.price
            else:
                for package_i in Package.PACKAGE_LIST:
                    if package_i.name == team.price:
                        package = package_i
                
                for team in package.team_list: # If it is team in a package, remove every associated team from the seed_team_list.
                    seed_team_list.remove(team) 
                    removed_teams.append(team)
                available_budget += package.price
        
        # Randomize potential buys
        random.shuffle(potential_buys)

        # Add the removed teams to the bottom of the list of potential_buys.
        potential_buys = potential_buys + removed_teams

        # for each team in potential buys (sorted randomly plus the removed teams placed at the very end), keep buying teams until
        # out of money
        for team in potential_buys:
            if type(team.price) == int:
                if available_budget >= team.price:
                    available_budget -= team.price
                    seed_team_list.append(team)
            else:
                package = team.price
                for package_i in Package.PACKAGE_LIST:
                    if package_i.name == team.price:
                        package = package_i

                if package.price <= available_budget:
                    packageAlreadyInSeedList = False
                    for team in seed_team_list:
                        if team.price == package.name:
                            packageAlreadyInSeedList = True
                    
                    if not packageAlreadyInSeedList:
                        available_budget -= package.price
                        for team in package.team_list:
                            seed_team_list.append(team)
        
        return Portfolio.new_portfolio(team_list = seed_team_list)

    # given a portfolio, return the number of times that value exceeded "points_to_win_bracket".
    def get_number_of_wins(portfolio, points_to_win_bracket=175):
        number_of_wins = 0
        for point_value in portfolio.points_history:
            if point_value >= points_to_win_bracket:
                number_of_wins += 1
        return number_of_wins

    def print_portfolio(portfolio, includeTeams = True, points_to_win_bracket=175):
        import matplotlib.pyplot as plt
        # Print name
        print("\nPortfolio:", portfolio.name)

        # Print amount of money all the teams add up to
        dollar_value = 0
        packages_already_counted = []
        for team in portfolio.team_list:
            if type(team.price) == int:
                dollar_value += team.price
            else:
                package = None
                for package_i in Package.PACKAGE_LIST:
                    if team.price == package_i.name:
                        package = package_i
                if package == None:
                    continue

                if not package in packages_already_counted:
                    dollar_value += package.price
                    packages_already_counted.append(package)
        print("Total Cost:", dollar_value)

        # Print the number of wins the team gets
        print(
            "# times scored > " + str(points_to_win_bracket) + ":",
            Portfolio.get_number_of_wins(portfolio, points_to_win_bracket)
        )

        # Print Teams
        if includeTeams:
            print("Teams: [")
            for team in sorted(portfolio.team_list, key=lambda x: x.name):  # print list of team names (sorted alphabetically)
                print("    ", ('"' + team.name + '",' + 60*' ')[:50], "# price:", team.price)
            print("]")

        # Create a histogram of the portfolio
        histogram_image_path = os.path.abspath("output_data/plots/" + portfolio.name + ".png").replace("#","")
        plt.hist(portfolio.points_history, bins=15)
        plt.title('Distribution of Points Won')
        plt.savefig(histogram_image_path)

        ### Create an html file from template
        output_html_path = os.path.abspath("output_data/" + portfolio.name + ".html")
        # load html template
        report_html = []
        for line in open("scripts/report_template.html","r").readlines():
            report_html.append(line)

        # Change html title
        report_html[6] = '      <h1>' + 'Portfolio: ' + portfolio.name + '</h1>\n'

        # Insert histogram image
        report_html[7] = '      <img src="' + histogram_image_path + '" alt="My Image" style="width:400px;height:300px;">\n'

        # save html template
        with open(output_html_path, 'w', newline='') as file:
            for line in report_html:
                file.write(line)

        webbrowser.open(output_html_path)

    # Given some portfolio, crawl around by selling one team at a time until
    # a portfolio is found that is a 'local minima' (no one-team swap will
    # improve the score)
    def find_relative_best_portfolio_from_seed(portfolio, points_to_win_bracket=175):
        # Create list of all teams/packages which the seed portfolio does not have.
        menu = []
        for team in Team.TEAM_LIST:
            if team in portfolio.team_list:
                continue
            if type(team.price) == int:
                menu.append(team)
        for package in Package.PACKAGE_LIST:
            if package in portfolio.package_list:
                continue
            menu.append(package)

        # Calculate amount of money which the portfolio has "leftover"
        leftover_money = Portfolio.STARTING_BALANCE
        for team in portfolio.team_list:
            if type(team.price) == int:
                leftover_money -= team.price
        for package in portfolio.package_list:
            leftover_money -= package.price

        ## Generate all random portfolios which are one 'step' away from the initial portfolio
        new_portfolios = []
        for team_to_sell in portfolio.team_list:
            if type(team_to_sell.price) != int:
                continue
            remaining_teams = portfolio.team_list[:]
            remaining_teams.remove(team_to_sell)
            price_of_team_sold = team_to_sell.price
            for combination in Portfolio.generate_purchase_combinations(menu, leftover_money+price_of_team_sold):
                packages_in_combination = []
                for item in combination:
                    if type(item) == Package:
                        packages_in_combination.append(item)
                for package in packages_in_combination:
                    combination.remove(package)
                    for team in package.team_list:
                        combination.append(team)
                print("TYPES:", type(combination), type(remaining_teams))
                new_portfolio = Portfolio.new_portfolio(combination + remaining_teams)

                print("sold", team_to_sell.name, "($" + str(team_to_sell.price) + ") and bought ", end='')
                for item in combination:
                    if type(item.price) == int:
                        print(item.name, "($" + str(item.price) + ")", end='')
                    else:
                        print(item.name, "(" + item.price.name + " $" + str(item.price.price) + ") ", end='')
                print()
                dummy_var = input("enter anything to continue:")
                new_portfolios.append(new_portfolio)

        for package_to_sell in portfolio.package_list:
            remaining_teams = portfolio.team_list[:]
            for team in package_to_sell.team_list:
                remaining_teams.remove(team)
            price_of_package_sold = package_to_sell.price
            for combination in Portfolio.generate_purchase_combinations(menu, leftover_money+price_of_package_sold):
                packages_in_combination = []
                for item in combination:
                    if type(item) == Package:
                        packages_in_combination.append(item)
                for package in packages_in_combination:
                    combination.remove(package)
                    for team in package.team_list:
                        combination.append(team)
                new_portfolios.append(Portfolio.new_portfolio(combination + remaining_teams))

        # Add the 'old' portfolio to the list of portfolios (just in case that is still the highest-winning portfolio)
        new_portfolios.append(portfolio)
        
        max_number_of_wins = 0
        current_portfolio_champ = None
        for portfolio in new_portfolios:
            current_portfolio_number_of_wins = 0
            for point_value in portfolio.points_history:
                if point_value >= points_to_win_bracket:
                    current_portfolio_number_of_wins += 1
            
            if current_portfolio_number_of_wins > max_number_of_wins or max_number_of_wins == 0:
                max_number_of_wins = current_portfolio_number_of_wins
                current_portfolio_champ = portfolio

        if current_portfolio_champ == portfolio:
            return portfolio
        else:
            return Portfolio.find_relative_best_portfolio_from_seed(current_portfolio_champ)

    def generate_purchase_combinations(menu, current_balance):
        # If the menu is empty, return empty list
        if len(menu) == 0:
            return []

        # If the menu is not empty, first check if the current_balance can
        # purchase everything remaining on the menu. If it can, just return
        # a list containing the one potential combination: namely, the entire
        # menu.
        total_menu_cost = 0
        for item in menu:
            total_menu_cost += int(item.price)
        if current_balance >= total_menu_cost:
            return [ menu ]

        # Sort the list by decreasing price (necessary for the combination algorithm)
        menu.sort(key=lambda x: x.price, reverse=False)

        # If there is not enough to buy every single team, generate two lists:
        # one of all the combinations of teams if we buy the first team on the menu,
        # the other all the combinations of teams if we do not.
        purchase_combinations = []

        for n in range(0, 5):
            print(len(list(itertools.combinations(menu, n))))
            AtLeastOneCombinationWithinBudget = False
            for purchase_combination in itertools.combinations(menu, n):
                purchase_combination = list(purchase_combination) # convert from 'tuple' to 'list'
                purchase_combination_total_cost = 0
                for item in purchase_combination:
                    purchase_combination_total_cost += item.price

                # Determine if purchase combination can even be bought.
                if purchase_combination_total_cost > current_balance:
                    continue
                else:
                    AtLeastOneCombinationWithinBudget = True

                # Determine if purchase combination could have bought another team,
                # but did not.
                leftover_money = current_balance - purchase_combination_total_cost
                invalid_purchase_combination = False
                for item in list(set(menu) - set(purchase_combination)):
                    if item.price <= leftover_money:
                        invalid_purchase_combination = True

                if not invalid_purchase_combination:
                    purchase_combinations.append(purchase_combination)

            if not AtLeastOneCombinationWithinBudget:
                break

        # first_item_on_menu = menu[0]
        # menu_without_first_item = menu[1:]
        # balance_if_purchase_first_item = current_balance - int(first_item_on_menu.price)
        # for i in range(len(menu)):
        #     total_remaining_menu_cost = 0
        #     for item in menu[i:]:
        #         total_remaining_menu_cost += int(item.price)
        #     if total_remaining_menu_cost <= current_balance:
        #         purchase_combinations.append(menu[i:])
        #         break
        #     elif menu[i].price <= current_balance:
        #         combination = [menu[i]]
        #         remaining_balance = current_balance - menu[i].price
        #         for j in range(i+1, len(menu)):
        #             if menu[j].price <= remaining_balance:
        #                 combination.append(menu[j])
        #                 remaining_balance -= menu[j].price
        #         purchase_combinations.append(combination)

        # for purchase_combination in Portfolio.generate_purchase_combinations(menu_without_first_item, current_balance):
        #     purchase_combinations.append(purchase_combination)
        #
        # if balance_if_purchase_first_item >= 0:
        #     for purchase_combination in Portfolio.generate_purchase_combinations(menu_without_first_item, \
        #                                                                balance_if_purchase_first_item):
        #         purchase_combinations.append([first_item_on_menu] + purchase_combination)

        print("\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nPortfolio.generate_purchase_combinations()\n")
        print("given the following menu and $" + str(current_balance) + ":")
        for item in menu:
            print(item.name, item.price)
        print("\nThe following combinations were obtained:")
        for combo in purchase_combinations:
            print("-> ", end='')
            for item in combo:
                if type(item.price) == int:
                    print(item.name, "$" + str(item.price), end=', ')
                else:
                    print(item.name, "$" + str(item.price.price), end=', ')
            print()

        return purchase_combinations

    # Function for instantiation of a Bracket Object
    def __init__(self):
        # add instance variables
        self.team_list = []       # A list of all the teams included in the portfolio
        self.package_list = []    # a list of any packages the portfolio might have
        self.points_history = []  # A list of how many points were one in each round generated by bracket.py

        # add to PACKAGE_LIST
        Portfolio.PORTFOLIO_LIST.append(self)

        return

    # Function to check portfolio list before creating a portfolio
    def new_portfolio(team_list=[]):
        # Convert team_list to a list of team objects (as opposed to team names)
        if len(team_list) > 0 and type(team_list[0]) == str:
            for i in range(0, len(team_list)):
                team_name = team_list[i]
                for team in Team.TEAM_LIST:
                    if team_name == team.name:
                        team_list[i] = team

        team_list = sorted(team_list, key=lambda x: x.name)
        for portfolio_i in Portfolio.PORTFOLIO_LIST:
            team_list_i = sorted(portfolio_i.team_list, key=lambda x: x.name)
            
            if team_list == team_list_i:
                return portfolio_i
        
        return Portfolio(team_list)

    # Function for instantiation of Portfolio Object with a given set of teams
    def __init__(self, team_list=[]):
        # Create portfolio name
        portfolio_names = []
        for row in Spreadsheet.read_csv("input_data/name_bank.csv"):
            portfolio_names.append(row[0].strip() + " #" + str(random.randint(1, 1000)))
        random.shuffle(portfolio_names) # "shuffle the deck" of portfolio names
        self.name = portfolio_names[0]

        # add instance variables
        self.team_list = team_list       # A list of all the teams included in the portfolio
        self.package_list = []          # a list of any packages the portfolio might have

        # populate package list
        for team in team_list:
            if type(team.price) != int:
                new_package = team.price
                if not new_package in self.package_list:
                    self.package_list.append(new_package)


        self.points_history = []  # A list of how many points were one in each round generated by bracket.py
        for bracket in Bracket.BRACKET_LIST:

            # Count how many points were scored by each team in the portfolio.
            points_scored_in_bracket = 0
            for team in self.team_list:
                points_scored_in_bracket += bracket.scoreboard[team]

            # add that score to the portfolio's 'points_history' value.
            self.points_history.append(points_scored_in_bracket)
        
        # add to PACKAGE_LIST
        Portfolio.PORTFOLIO_LIST.append(self)

        return
