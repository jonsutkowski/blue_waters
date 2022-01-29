# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:01:45 2021

@author: Jonathan Sutkowski
"""
# Import libraries
import random
import time
from scripts.spreadsheet import Spreadsheet
from scripts.teams import Team, Package
from scripts.bracket import Bracket

class Portfolio:
    # master list of all portfolios
    PORTFOLIO_LIST = []

    # Starting balance
    STARTING_BALANCE = 100

    ## VARIOUS FUNCTIONS

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
            portfolio_names.append(row[0])
        random.shuffle(portfolio_names) # "shuffle the deck" of portfolio names

        # loop through each possible combination of purchases. Create a portfolio object for each one.
        for purchase_combination in generate_purchase_combinations(menu, Portfolio.STARTING_BALANCE):
            new_portfolio = Portfolio()
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

    # Generate list
    def generate_random_portfolios(number_of_portfolios=1):
        # generate list of portfolio names.
        portfolio_names = []
        for row in Spreadsheet.read_csv("input_data/name_bank.csv"):
            portfolio_names.append(row[0])
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
        for i in range(0, number_of_portfolios):
            # Create randomized menu
            shuffled_menu = menu[:]
            random.shuffle(shuffled_menu)

            # Create new Portfolio object
            new_portfolio = Portfolio()
            try:
                new_portfolio.name = portfolio_names[0]
                portfolio_names = portfolio_names[1:]
            except:
                new_portfolio.name = "Un-named Portfolio"
            new_portfolio.team_list = []
            new_portfolio.package_list = []

            # Set initial amount of spending money to the default value.
            spending_money = Portfolio.STARTING_BALANCE

            # Buy each affordable item in the randomized menu in order.
            while len(shuffled_menu) > 0 and spending_money > 0:
                next_item_on_menu = shuffled_menu[0]
                shuffled_menu = shuffled_menu[1:]

                if spending_money > int(next_item_on_menu.price):
                    spending_money -= int(next_item_on_menu.price)
                    if type(next_item_on_menu) == Package:
                        new_portfolio.package_list.append(next_item_on_menu)
                        for team in next_item_on_menu.team_list:
                            new_portfolio.team_list.append(team)
                    if type(next_item_on_menu) == Team:
                        new_portfolio.team_list.append(next_item_on_menu)

        # populate each portfolio object with the amount of points scored in each bracket
        for bracket in Bracket.BRACKET_LIST:
            for portfolio in Portfolio.PORTFOLIO_LIST:

                # Count how many points were scored by each team in the portfolio.
                points_scored_in_bracket = 0
                for team in portfolio.team_list:
                    points_scored_in_bracket += bracket.scoreboard[team]

                # add that score to the portfolio's 'points_history' value.
                portfolio.points_history.append(points_scored_in_bracket)

        return



    # Function for instantiation of a Bracket Object
    def __init__(self):
        # add instance variables
        self.team_list = []       # A list of all the teams included in the portfolio
        self.package_list = []    # a list of any packages the portfolio might have
        self.points_history = []  # A list of how many points were one in each round generated by bracket.py

        # add to PACKAGE_LIST
        Portfolio.PORTFOLIO_LIST.append(self)

        return