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

def getDistribution(filePath, refMeasurements_ds, refMeasurements_dth):
    #List containing all corner measurements
    measurements_ds = dE.getMeasurements(filePath,'ds =')
    measurements_dth = dE.getMeasurements(filePath,'d =')
    
    # Measurements which are not due to random noise
    filteredMeasurements_ds = dE.checkReference(refMeasurements_ds, measurements_ds, 0.2) 
    filteredMeasurements_dth = dE.checkReference(refMeasurements_dth, measurements_dth, 0.2)  
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
refMeasurements_ds = [[0.8], [0.05], [0.3]] # reference data which is considered correct (from camera)
refMeasurements_dth = [[0.2], [0.5]]
filteredMeasurements_ds, filteredMeasurements_dth = getDistribution(filePath, refMeasurements_ds, refMeasurements_dth)



