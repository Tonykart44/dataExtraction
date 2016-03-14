# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:04:37 2016

@author: Robin Amsters

Costum functions that can be used when extracting data from a .txt file that 
was created using the diary function in MATLAB
"""
import math
#==============================================================================
def checkReference(reference, data, accuracy):
    """
    Function to check whether a dataset matches the reference close enough
    
        INPUT:
                reference: reference to match data against, this is a list
                           containing an arbitrary amount of lists of size 2
                data: data to be matched with the reference, 
                      this is a list containing lists containing lists of len 2
                accuracy: parameter that specifies how much data can differ 
                          from reference and still be accepted as matching
    
        OUTPUT
                matchedData: a list containing lists of size 2 of data that has
                             been checked against the reference and accepted
                             according to the specified accuracy. Number inside
                             list represents difference of datapoint with 
                             reference
                             
    """
    matchedData = [] #initalizing output
    
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
                pointDiff = [diff_x, diff_y] #difference as list
                
                distance = math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2)) 
                               
                if distance <= accuracy and point not in matchedPoint:
                # Add current point to matched points if accepted and not already in matchedPoint
                    matchedPoint.append(pointDiff)
                    
                if len(matchedPoint) == len(reference) and matchedPoint not in matchedData:
                # Add points to data when all have been matched against a reference and they are not yet in matchedData
                    matchedData.append(matchedPoint)
    
    return matchedData
#==============================================================================
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
 
#==============================================================================
def getLevelOfSublists(masterList):
    """
        Function that returns the number of sublevels in a list that contains
        other lists.
        
        INPUT: 
              masterList: list in wich sublevels can be present and from which 
                          the levels will be returned
        OUTPUT:
              number of levels in masterList
              
        source: http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to
    """
    if isinstance(masterList, list) and len(masterList) > 0:
        return 1 + max(getLevelOfSublists(item) for item in masterList)
    else:
        return 0
#==============================================================================   
def removeSublistLevel(masterList, index):
    """
    Function that returns all elements from sublists in a masterlist at index
    
    INPUT:
        masterlist: list that has at least one level of sublists from which 
                    elements have to be selected
        index: index of elements in sublist that have to be returned
        
    OUTPUT:
        sublistElements: elements of sublists at index 
    """
    
    # Error messages
    typeError = '''
    ERROR: Input is of wrong type, please use a list with sublevels for 
    masterList, and int for index.
    '''  
    lengthError = '''
    ERROR: One or more of the sublists of masterList have a length that is 
    smaller than the desired index.
    '''
    
    # Initializing output
    sublistElements = []  
    
    # Input checking
    if not isinstance(masterList, list) or not isinstance(index, int):
        print(typeError)      
    elif not isinstance(masterList[0], list):
        print(typeError) 
    elif len(masterList[0]) <= index:
        print(lengthError)
    else:
        # Getting sublists
        for sublist in masterList:
            sublistElements.append(sublist[index])
        
    return sublistElements