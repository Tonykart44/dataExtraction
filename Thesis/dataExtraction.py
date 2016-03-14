# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:04:37 2016

@author: robin

Costum functions that can be used when extracting data from a .txt file that 
was created using the diary function in MATLAB
"""

def getMeasurements(filePath, prefix):
    """
    Function that extracts measurements from a .txt file    

    INPUT:
            filePath: full path of the file to be read
            prefix: MATLAB prints the name of the variable before printing its
                    value, this string should be entered here as it shows the 
                    start of the measurement.
                    
                    e.g.
                    
                    ds =

                        0.0209
                        
                        
                    ds =
                    
                        0.0418
                    
                    etc.
                    
                    In the above example the prefix is 'ds ='
    
    OUTPUT:
            allMeasurements: list containing the all the measurements as 
                             smaller lists inside lists. Thus there will be
                             two levels of sublists, use removeSubListLevel 
                             when measurements are not spread across multiple 
                             lines
    """    
    # Defining local variables

    fileHandle = open(filePath, 'r') #Internal name for file
    lines = fileHandle.readlines() #All lines in the file
    
    startMeasurement = False # When true, next lines can be considered to be part of the same measurement
    newLineCount = 0 # Counts the number of new lines (measurements are separated by 2 new lines)
    allMeasurements = [] # Contains all of the extracted corner measurements
    currentMeasurement = [] # Contains the measurement currently being extracted
    
    for line in lines:
    # Looping over each line in file
    
        if line.count(' ') and startMeasurement:
            # If the line contains a space and the measurement has started, add this line to the currentMeasurement matrix
            currentMeasurement.append(line.split())
            newLineCount = 0
        
        if line.count(prefix):
            # Check whether measurement has started, this is done after the if 
            # that adds measurements so that 'corners_world' and '=' are not added
            startMeasurement = True
            newLineCount = 0   
            
        elif line.isspace():
            # Keep track of how many lines with no text are after each other
            newLineCount += 1
        
        if newLineCount >= 2 and startMeasurement:
            # Measurements are separated by two newlines
            allMeasurements.append(currentMeasurement)
            currentMeasurement = []
            startMeasurement = False
            newLineCount = 0
            
    return allMeasurements