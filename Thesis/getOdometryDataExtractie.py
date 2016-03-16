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
import matplotlib.pyplot as plt
import numpy as np
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
    
    index = 0 #index to compare data with in reference
    
    for measurement in data:
        
        for point in measurement: #Checking and selecting measurements
        
            if not len(point) == 1:
                print lengthError
                
            else:
                data_point = point[0]
                
                if type(data_point) == str:
                    data_point = float(data_point)
                    
                ref = reference[index][0]

                if not len(ref) == 1:
                    print lengthError   
                    
                else:
                    
                    ref_point = ref[0]
                                        
                    if type(ref_point) == str:
                        ref_point = float(ref_point)
                    distance = abs(data_point-ref_point)
                
                    matchedData.append(distance)                    
                    
            index += 1
    return matchedData

def getDistribution(filePath, refMeasurements_ds, refMeasurements_dth):
    #List containing all corner measurements
    measurements_ds = dE.getMeasurements(filePath,'ds =')
    measurements_dth = dE.getMeasurements(filePath,'dth =')
    
    # Measurements which are not due to random noise
    filteredMeasurements_ds = checkReference(refMeasurements_ds, measurements_ds, 0.2) 
    filteredMeasurements_dth = checkReference(refMeasurements_dth, measurements_dth, 0.2)  
    
    # Getting normal distribution parameters
    mu_ds, std_ds = norm.fit(filteredMeasurements_ds)
    mu_dth, std_dth = norm.fit(filteredMeasurements_dth)
    
#    return mu, std, allDifferences
    return mu_ds, std_ds, mu_dth, std_dth
    
""" 
MAIN SCRIPT: USING FUNCTIONS TO EXTRACT DATA
"""

# Getting distributions

# Selecting file trough GUI
filePath = dE.getFilePath()

# Getting measurements
measurements_ds = dE.getMeasurements(filePath,'ds =') #getting measurements of distance
measurements_dth = dE.getMeasurements(filePath,'dth =') #getting measurements of angle

 # reference data which is considered correct (from camera)
refMeasurements_ds = dE.getSampleMeasurements(len(measurements_ds),1,0)
refMeasurements_dth = dE.getSampleMeasurements(len(measurements_dth),1,0)

# Difference with real measurements 
filteredMeasurements_ds = checkReference(refMeasurements_ds, measurements_ds, 0.2) 
filteredMeasurements_dth = checkReference(refMeasurements_dth, measurements_dth, 0.2)

 # Getting normal distribution parameters
mu_ds, std_ds = norm.fit(filteredMeasurements_ds)
mu_dth, std_dth = norm.fit(filteredMeasurements_dth) 

# Plotting

# Plotting the histogram of ds
plt.figure(1)
plt.hist(filteredMeasurements_ds, bins=25, normed=True, alpha=0.6, color='g')

# Plot the PDF of ds
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu_ds, std_ds)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu_ds, std_ds)
plt.title(title)
plt.savefig('getOdometryDistrubution_ds.png')

# Plotting the histogram of dth
plt.figure(2)
plt.hist(filteredMeasurements_dth, bins=25, normed=True, alpha=0.6, color='g')

# Plot the PDF of dth
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu_dth, std_dth)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu_dth, std_dth)
plt.title(title)
plt.savefig('getOdometryDistrubution_dth.png')



