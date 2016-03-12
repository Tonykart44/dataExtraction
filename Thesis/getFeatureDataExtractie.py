# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:00:30 2016

@author: Robin Amsters

File that extraxts data from txt file that contains getFeature data from txt files
"""


# Opening file and reading contents
filePath = '/home/robin/Bureaublad/getFeatureCalibratieData.txt'
fileHandle = open(filePath, 'r')
lines = fileHandle.readlines()
lines = lines[0:]

# Defining variables
startMeasurement = False # When true, next lines can be considered to be part of the same measurement
newLineCount = 0 # Counts the number of new lines (measurements are separated by 2 new lines)
cornerMatrix = [] # Contains all of the extracted corner measurements
currentMeasurement = [] # Contains the measurement currently being extracted
refMeasurements = [[1.4, 0.1], [1.5, 0.7], [-0.75, 0.7], [0, -0.7], [0.85, -0.7], [1.3, -0.35]] # reference data which is considered correct (from camera)

# Looping over each line in file
for line in lines:
    
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
        cornerMatrix.append(currentMeasurement)
        currentMeasurement = []
        startMeasurement = False
        newLineCount = 0

"""
DEFINING FUNCTIONS
"""

def checkReference(reference, data, accuracy):
    """
    A function to check wheter a dataset matches the reference close enough
    
        INPUTS:
                reference: reference to match data against, this is a list
                           containing an arbitrary amount of lists of size 2
                data: data to be matched with the reference, 
                      this is a list of size 2
                accuracy: parameter that specifies how much data can differ 
                          from reference and still be accepted
    
        OUTPUTS
                matchedData: ???
    """
    
    pass    