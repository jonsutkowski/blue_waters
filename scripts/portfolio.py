# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:01:45 2021

@author: Jonathan Sutkowski
"""
from scripts.spreadsheet import Spreadsheet

class Portfolio:
    
    # master list of all portfolios
    PORTFOLIO_LIST = []
    
    # master list of all potential portfolio names
    NAME_LIST = []
    
    # master menu of all team prices & packages. formatted with team name or
    # package name in the first column, and the true seed along the first row
    first_row = ['name','cost']
    for i in range(1,69):
        first_row.append(str(i))
    MENU = [first_row]
    
    ## VARIOUS FUNCTIONS
    
    def test():
        Spreadsheet.write_csv('test',[[1]])
        return
    
    # this function accepts an array of booleans, and treating it like a binary
    # number (True = 1, False = 0), adds one.
    def increment(array):
        
        index = len(array) - 1
        
        if array[index] == False:
            # If last digit of array is 0, simply change to 1 and return array.
            array[index] = True
            return array
        
        elif index == 0:
            # If array has 1 element, and that element is True, return 'False'
            return [False]
        
        else:
            # If last digit of array is 1, increment the higher-order digits
            # on the array and replace last digit with a 0.
            array = Portfolio.increment(array[:index])
            array.append(False)
            return array
    
    # function iterates through all possible portfolios. If the portfolio cost
    # is over budget, pass to next iteration. Elif an existing portfolio contains
    # all teams that current iteration has, pass to next iteration. Elif current
    # iteration contains all teams that an existing portfolio has, replace existing
    # portfolio with current iteration. Else, Create new portfolio.
    def generate_portfolios():
        

        return
    
    # function saves portfolios to output_data/portfolios.csv
    def save_portfolios():
        
        return
    
    # function loads in portfolios from output_data/portfolios.csv
    def load_portfolios():
        
        return
    
    # function loads 'menu' of teams from The Big Dance into a 2-D array
    def load_menu():
        
        menu_array = Spreadsheet.read_csv('input_data/menu.csv')
        
        portfolio_menu = Portfolio.MENU
        
        # iterate thru all but first row of menu.csv
        for i in range(1, len(menu_array)):
            
            # check if cost is numeric.
            if menu_array[i][2].isnumeric():
                # If cost is numeric, simply create row with team name in first
                # column, and '1' in the column whose index is one more than
                # the team's true seed
                
                true_seed = int(menu_array[i][0]) # obtain true_seed int
                new_row = [menu_array[i][1]] # create new row's first column
                cost = int(menu_array[i][2])
                new_row.append(cost) # append cost in second row.
                for i in range(1,true_seed): #append empty string for all but last column
                    new_row.append('')
                
                new_row.append('1') # append '1' corresponding to true_seed

                portfolio_menu.append(new_row) # add new row to Portfolio.MENU
            else:
                # if cost is not numeric, this line is a package! check if
                # package has already been created in Portfolio.MENU:
                packageAlreadyAdded = False
                for j in range(0,len(portfolio_menu)):
                    if portfolio_menu[j][0] == menu_array[i][2]:
                        packageAlreadyAdded = True
                        package_index = j
                
                if packageAlreadyAdded:
                    # If package is already added, add to its respective row
                    # a '1' in the index row[true_seed + 1]
                    length_of_row = len(portfolio_menu[package_index])
                    true_seed = int(menu_array[i][0]) #obtain true_seed int
                    
                    # extend blank spaces as far as needed to include
                    # index (true_seed + 1). If row is already long enough,
                    # this loop will simply not run.
                    for j in range(length_of_row,true_seed + 2):
                        portfolio_menu[package_index].append('')
                    
                    # replace the row's point at index true_seed + 1 with a '1'
                    portfolio_menu[package_index][true_seed + 1] = '1'
                else:
                    # If a package has not yet been added, find the cost,
                    # and create the row.
                    
                    # loop thru menu.csv to find cost
                    cost = False
                    for row in menu_array:
                        # if our package's price is listed, obtain the price
                        if row[3] == menu_array[i][2]:
                            cost = int(row[4])
                            break
                    
                    # debugging: if string is in cost column of menu.csv, but
                    # it doesn't match up with a package item on menu.csv, this
                    # message will be printed.
                    if cost == False:
                        print("could not find a cost for", menu_array[i][2])
                    
                    true_seed = int(menu_array[i][0]) # obtain true seed int
                    new_row = [menu_array[i][2]] # create new row's first column
                    new_row.append(cost) # append cost in second row.
                    
                    for i in range(1,true_seed): #append empty string for all but last column
                        new_row.append('')
                    
                    new_row.append('1') # append '1' corresponding to true_seed
                    
                    portfolio_menu.append(new_row) # add new row to Portfolio.MENU
                    
        # Officially overwrite Portfolio.MENU with portfolio_menu
        Portfolio.MENU = portfolio_menu
        return
    
    # function re-writes 'menu.csv' to the default, empty file ready for
    # data to be input.
    def reset_menu():
        
        # Make sure user understands the ramifications
        prompt = "Are you sure you want to reset menu.csv? The data currently stored in menu.csv will not be recoverable.\nEnter 'affirmative' if you want to do this: "
        
        if input(prompt) == 'affirmative':
            menu_headers = ["true_seed","name","cost","package","cost"]
            Spreadsheet.write_csv('input_data/menu.csv', [menu_headers])
        
        return

    # function that loads names into NAME_LIST, adds all possible portfolios
    # that can be purchased with the limited amount of money.    
    def __init__(self, array):
        
        # Check that identical portfolio was not already instantiated. If it
        # is, then do not add to PORTFOLIO_LIST.
        for i in Portfolio.PORTFOLIO_LIST:
            if Portfolio.PORTFOLIO_LIST[i].array == array:
                print("Attempted to add array that has already been added:\n", array)
                return
        
        # add array to portfolio
        self.array = array
        # assign the name after previous created portfolio
        self.name = len(Portfolio.PORTFOLIO_LIST)        
        # Add portfolio to master list
        Portfolio.PORTFOLIO_LIST.append(self)
        
        return