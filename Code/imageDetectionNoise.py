# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 21:36:55 2016

@author: Robin Amsters

Script that fits a normal distribution to the noise on image detection
this script is very simular to getFeatureDataExtractie, but differs in that 
only one point is considered
"""
import dataExtraction as dE
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import math


"""
DEFINING FUNCTIONS
"""   
#==============================================================================
def checkReference(reference, data, accuracy):
    """
    Function to check whether a dataset matches the reference close enough
    
        INPUT:
                reference: reference to match data against, this is a list
                           containing an arbitrary amount of lists of size 1 or 
                           2
                data: data to be matched with the reference, 
                      this is a list containing lists containing lists of len 1
                      or 2
                accuracy: parameter that specifies how much data can differ 
                          from reference and still be accepted as matching
    
        OUTPUT
                matchedData: a list containing lists of size 1 or 2 of data 
                             that has been checked against the reference and 
                             accepted according to the specified accuracy. 
                             Number inside list represents difference of 
                             datapoint with reference
                             
    """
    matchedData = [] #initalizing output
    lengthError = '''ERROR: length of input is incorrect, please use only 
    lists with sublists that have a length of 1 or 2.'''
    
    for measurement in data:
        
        matchedPoint = [] #datapoints (list of len 2) that have been matched
        
        for point in measurement: #Checking and selecting measurements
            if not len(point) == 2:
                print lengthError
                
            else:
                x_p = point[0] #measured x coordinates
                y_p = point[1] #measured y coordinates
    
            for ref in reference:

                if not len(ref) == 2:
                    print lengthError
                    
                else:
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
def getDistribution(filePath, refMeasurements):
    #List containing all corner measurements
    measurements = dE.getMeasurements(filePath,'pos =') 
    
    # Measurements which are not due to random noise
    filteredMeasurements = checkReference(refMeasurements, measurements, 500)  
    
    # Extracting difference in x and y coordinates from split corners
    x_A = removeSublistLevel(filteredMeasurements, 0)
    y_A = removeSublistLevel(filteredMeasurements, 1)
    
    # Putting all the differences in one list
    allDifferences = []
    allDifferences.extend(x_A)
    allDifferences.extend(y_A)
    
    # Getting normal distribution parameters
    mu, std = norm.fit(allDifferences)
    
    return mu, std, allDifferences
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
            for sub in sublist:
                sublistElements.append(sub[index])
        
    return sublistElements
#==============================================================================
    
""" 
MAIN SCRIPT: USING FUNCTIONS TO EXTRACT DATA
"""

# Selecting file trough GUI
filePath = dE.getFilePath()

refMeasurements = [['0.4949', '0.5029']] # reference data which is considered correct (from camera)

# Getting distributions
mu, std, allDifferences = getDistribution(filePath, refMeasurements)

# Plotting the histograms
plt.figure(1)
plt.hist(allDifferences, bins=25, normed=True, alpha=0.6, color='g')

# Plot the PDFs
plt.figure(1)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.5f,  std = %.5f" % (mu, std)
plt.title(title)

# Saving figure
save_string = raw_input("Do you want to save the figure ? (y/n): ")
if save_string == 'y':
    savePath = dE.getSavePath()
    plt.savefig(savePath + '/imageDetectionNoise.png')
elif save_string == 'n':
    print('Figure not saved')
else:
    print('Input invalid, figure not saved')
