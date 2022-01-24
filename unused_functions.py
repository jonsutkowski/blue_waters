# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 21:17:40 2021

@author: Jonathan Sutkowski
"""

def old_generate_portfolios():
        # create array of 68 falses.
        array_i = []
        for i in range(0,68):
            array_i.append(False)
        
        # Check array_i and add portfolio. if it is not maxed out, iterate and repeat.
        while True:
            
            # Iterate array_i, or break out of loop if array_i is "maxed out" (all True)
            isMaxedOut = True
            for j in array_i:
                if j == False:
                    # If there is at least one False in the array, do not break
                    # out of iteration.
                    isMaxedOut = False
            
            if isMaxedOut:
                # If there is not even one False in the array, break out.
                print(array_i)
                break
            else:
                array_i = Portfolio.increment(array_i)
        
        return
