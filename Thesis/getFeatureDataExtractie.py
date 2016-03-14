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

"""
DEFINING FUNCTIONS
"""   
def getDistribution(filePath, refMeasurements):
    #List containing all corner measurements
    measurements = dE.getMeasurements(filePath,'corners_world =') 
    
    # Measurements which are not due to random noise
    filteredMeasurements = dE.checkReference(refMeasurements, measurements, 0.2) 
    
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