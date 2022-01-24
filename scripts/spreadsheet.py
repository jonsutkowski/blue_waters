# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 21:19:37 2021

Note: This is a small library of functions stored in child folder 'scripts',
intended to be run from parent folder 'blue_waters'. It reads from and saves to
'input_data' and 'output_data', respectively.

@author: Jonathan Sutkowski
"""

import csv

class Spreadsheet:
    
    def read_csv(filename):
        csvfile = open(filename, newline='')
        return( list(csv.reader(csvfile)) )
    
    def write_csv(filename, array):
        csvfile = open(filename,"w+", newline='')
        csvWriter = csv.writer(csvfile,delimiter=',')
        csvWriter.writerows(array)
        
        print("Successfully saved "+filename+"!")
        return
    
    def __init__(self):        
        return