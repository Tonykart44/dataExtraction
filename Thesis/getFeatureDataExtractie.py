# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:00:30 2016

@author: Robin Amsters

File that extraxts data from txt file that contains getFeature data from txt files
"""
import math
"""
DEFINING FUNCTIONS
"""
def checkReference(reference, data, accuracy):
    """
    A function to check whether a dataset matches the reference close enough
    
        INPUTS:
                reference: reference to match data against, this is a list
                           containing an arbitrary amount of lists of size 2
                data: data to be matched with the reference, 
                      this is a list containing lists containing lists of len 2
                accuracy: parameter that specifies how much data can differ 
                          from reference and still be accepted as matching
    
        OUTPUTS
                matchedData: a list containing lists of size 2 of data that has
                             been checked against the reference and accepted
                             according to the specified accuracy
                             
    """
    # Variables
    matchedData = []  
    
    for measurement in data:
        matchedPoint = [] #datapoints (list of len 2) that have been matched
        for point in measurement:
            x_p = point[0] #measured x coordinates
            y_p = point[1] #measured y coordinates
            for ref in reference:
                x_ref = ref[0] #reference x coordinates
                y_ref = ref[1] #reference u coordinates
                
                diff_x = float(x_p) - float(x_ref) #difference in x coordinates
                diff_y = float(y_p) - float(y_ref) #difference in y coordinates
                
                distance = math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2)) 
                               
                if distance <= accuracy and point not in matchedPoint:
                # Add current point to matched points if accepted and not already in matchedPoint
                    matchedPoint.append(point)
                    
                if len(matchedPoint) == len(reference) and matchedPoint not in matchedData:
                # Add points to data when all have been matched against a reference and they are not yet in matchedData
                    matchedData.append(matchedPoint)

    return matchedData
   
def getMeasurements(filePath):
    """
    A function that extracts measurements from a .txt file    

    INPUTS:
            filePath: full path of the file to be read
    
    OUTPUTS:
            allMeasurements: list containing the all the measurements as smaller lists
    
    """    
    # Defining local variables

    fileHandle = open(filePath, 'r') #Internal name for file
    lines = fileHandle.readlines() #All lines in the file
    lines = lines[0:] #While debugging sometimes not the entire file is used
    
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
        
        if line.count('corners_world ='):
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

""" 
MAIN SCRIPT: USING FUNCTIONS TO EXTRACT DATA
"""

# Defining variables
filePath = '/home/robin/Bureaublad/getFeatureCalibratieData.txt'
refMeasurements = [[1.5405, 0.6808], [1.3355, -0.3614], [0.8496, -0.7070]] # reference data which is considered correct (from camera)

corners = getMeasurements(filePath) #List containing all corner measurements
filteredCorners = checkReference(refMeasurements, corners, 1) # Measurements which are not due to random noise



        