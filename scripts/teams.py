# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:01:45 2021

@author: Jonathan Sutkowski
"""
# Import libraries
from scripts.spreadsheet import Spreadsheet

# Set parameters which govern how the win_ratio value is generated based on the seed
AVERAGE_WIN_RATIO = 0.83
RANGE_OF_WIN_RATIOS = 0.31

class Team:
    # master list of all portfolios
    TEAM_LIST = []

    ## VARIOUS FUNCTIONS
    # Create a team object for each team, and then a package object for each package
    def generate_team_list():
        # Read menu from input_data/menu.csv
        menu_array = Spreadsheet.read_csv('input_data/menu.csv')

        # Create list of packages
        for i in range(1, len(menu_array)):
            package_name = menu_array[i][3]
            package_price = menu_array[i][4]

            # break out of loop at the end of the list of packages
            if package_name == '':
                break

            # Create a package object
            new_package = Package()
            new_package.name = package_name
            new_package.team_list = []
            new_package.price = package_price

        # iterate thru all but first row of menu.csv
        for i in range(1, len(menu_array)):
            # Create a Team object
            new_team = Team()
            new_team.true_seed = int(menu_array[i][0])  # obtain true_seed int
            new_team.name = menu_array[i][1]            # obtain name string
            new_team.price = menu_array[i][2]           # obtain price int

            # check if cost is numeric.
            if not new_team.price.isnumeric():
                # if cost is not numeric, this team belongs to a package! Add
                # the team to the package object's team_list instance variable
                foundPackage = False
                for package in Package.PACKAGE_LIST:
                    if new_team.price == package.name:
                        package.team_list.append(new_team)
                        foundPackage = True
                if not foundPackage:
                    print("unable to find package object for team:", new_team.name)
            else:
                new_team.price = int( new_team.price )

        ## Populate the win_ratio value for each team
        # win_ratio of first seed
        maximum_win_ratio = AVERAGE_WIN_RATIO + RANGE_OF_WIN_RATIOS / 2
        # win ratio difference between each team
        win_ratio_increment_value = RANGE_OF_WIN_RATIOS / (len(Team.TEAM_LIST) - 1)
        for team in Team.TEAM_LIST:
            # arranged in order of true seed, each team's win_ratio is spaced out across
            # the range of win_ratios specified at the top of this script.
            team.win_ratio = maximum_win_ratio - win_ratio_increment_value * (team.true_seed - 1)

        return


    def __init__(self):
        # add instance variables
        self.name = None
        self.win_ratio = None
        self.true_seed = None
        self.price = None

        # Add to TEAM_LIST
        Team.TEAM_LIST.append(self)

        return


class Package:
    # master list of all portfolios
    PACKAGE_LIST = []

    ## VARIOUS FUNCTIONS

    def __init__(self):
        # add instance variables
        self.name = None
        self.team_list = None
        self.price = None

        # add to PACKAGE_LIST
        Package.PACKAGE_LIST.append(self)

        return
