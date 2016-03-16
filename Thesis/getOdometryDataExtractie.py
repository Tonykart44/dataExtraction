# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:36:00 2016

@author: robin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:00:30 2016

@author: Robin Amsters

File that extraxts data from txt file that contains getFeature data from txt files
"""
import dataExtraction as dE
from scipy.stats import norm

"""
DEFINING FUNCTIONS
"""
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
    
    index = 0
    
    for measurement in data:
#        matchedPoint = [] #datapoints (list of len 2) that have been matched
        
        for point in measurement: #Checking and selecting measurements
        
            if not len(point) == 1:
                print lengthError
                
            else:
                data_point = point[0]
                
                ref = reference[index]

                if not len(ref) == 1:
                    print lengthError
                    
                else:
                    ref_point = ref[0]
                    
                    distance = abs(float(data_point)-float(ref_point))
                
                    matchedData.append(distance)                    
                    
#                    if distance <= accuracy and point not in matchedPoint:
#                        # Add current point to matched points if accepted and not already in matchedPoint
#                        matchedPoint.append(distance)
#
#                    if len(matchedPoint) == len(reference) and matchedPoint not in matchedData:
#                        # Add points to data when all have been matched against a reference and they are not yet in matchedData
#                        matchedData.append(matchedPoint)
            index += 1
    return matchedData

def getDistribution(filePath, refMeasurements_ds, refMeasurements_dth):
    #List containing all corner measurements
    measurements_ds = dE.getMeasurements(filePath,'ds =')
    measurements_dth = dE.getMeasurements(filePath,'dth =')
    
    # Measurements which are not due to random noise
    filteredMeasurements_ds = checkReference(refMeasurements_ds, measurements_ds, 0.2) 
    filteredMeasurements_dth = checkReference(refMeasurements_dth, measurements_dth, 0.2)  
#    #Split filtered corners in list of points that belong together
#    measurements_point_A = dE.removeSublistLevel(filteredMeasurements_ds,0)
#    measurements_point_B = dE.removeSublistLevel(filteredMeasurements_dth,1)
#    # Extracting difference in x and y coordinates from split corners
#    x_A = getSublistElements(measurements_point_A, 0)
#    y_A = getSublistElements(measurements_point_A, 1)
#    
#    # Putting all the differences in one list
#    allDifferences = []
#    allDifferences.extend(x_A)
#    allDifferences.extend(y_A)
#    allDifferences.extend(x_B)
#    allDifferences.extend(y_B)
#    allDifferences.extend(x_C)
#    allDifferences.extend(y_C)
#    
#    # Getting normal distribution parameters
#    mu, std = norm.fit(allDifferences)
    
#    return mu, std, allDifferences
    return filteredMeasurements_ds, filteredMeasurements_dth
    
""" 
MAIN SCRIPT: USING FUNCTIONS TO EXTRACT DATA
"""

# Defining file variables
filePath = '/home/robin/Bureaublad/getOdometrySampleData.txt'
refMeasurements_ds = [[0], [0.0255], [0.0209]] # reference data which is considered correct (from camera)
refMeasurements_dth = [[0], [-0.004], [-0.0080]]
measurements_ds = dE.getMeasurements(filePath,'ds =')
measurements_dth = dE.getMeasurements(filePath,'dth =')
filteredMeasurements_ds, filteredMeasurements_dth = getDistribution(filePath, refMeasurements_ds, refMeasurements_dth)



