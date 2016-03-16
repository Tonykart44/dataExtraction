# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:00:30 2016

@author: Robin Amsters

File that extraxts data from txt file that contains getFeature data from txt files
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

def getDistribution(filePath, refMeasurements):
    #List containing all corner measurements
    measurements = dE.getMeasurements(filePath,'corners_world =') 
    
    # Measurements which are not due to random noise
    filteredMeasurements = checkReference(refMeasurements, measurements, 0.2) 
    
    #Split filtered corners in list of points that belong together
    measurements_point_A = dE.removeSublistLevel(filteredMeasurements,0)
    measurements_point_B = dE.removeSublistLevel(filteredMeasurements,1)
    measurements_point_C = dE.removeSublistLevel(filteredMeasurements,2)        
    
    # Extracting difference in x and y coordinates from split corners
    x_A = dE.removeSublistLevel(measurements_point_A, 0)
    y_A = dE.removeSublistLevel(measurements_point_A, 1)
    
    x_B = dE.removeSublistLevel(measurements_point_B, 0)
    y_B = dE.removeSublistLevel(measurements_point_B, 1)
    
    x_C = dE.removeSublistLevel(measurements_point_C, 0)
    y_C = dE.removeSublistLevel(measurements_point_C, 1)
    
    # Putting all the differences in one list
    allDifferences = []
    allDifferences.extend(x_A)
    allDifferences.extend(y_A)
    allDifferences.extend(x_B)
    allDifferences.extend(y_B)
    allDifferences.extend(x_C)
    allDifferences.extend(y_C)
    
    # Getting normal distribution parameters
    mu, std = norm.fit(allDifferences)
    
    return mu, std, allDifferences

""" 
MAIN SCRIPT: USING FUNCTIONS TO EXTRACT DATA
"""

# Defining file variables
filePath = '/home/robin/Bureaublad/getFeatureCalibratieData.txt'
refMeasurements = [[1.5405, 0.6808], [1.3355, -0.3614], [0.8496, -0.7070]] # reference data which is considered correct (from camera)

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
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)
plt.savefig('getFeatureDistribution.png')