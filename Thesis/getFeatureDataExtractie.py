# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:00:30 2016

@author: robin

File that extraxts data from txt file that contains getFeature data
"""


# Opening file and reading contents
filePath = '/home/robin/Bureaublad/getFeatureCalibratieData.txt'
fileHandle = open(filePath, 'r')
lines = fileHandle.readlines()
lines = lines[0:]

# Defining variables
startMeasurement = False # When true, next lines can be considered to be part of the same measurement
newLineCount = 0 # Counts the number of new lines (measurements are separated by 2 new lines)
cornerMatrix = []
currentMeasurement = []

# Looping over each line in file
for line in lines:
    
    if line.count(' ') and startMeasurement:
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
        cornerMatrix.append(currentMeasurement)
        currentMeasurement = []
        startMeasurement = False
        newLineCount = 0
    