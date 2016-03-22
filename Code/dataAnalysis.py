# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:46:16 2016

@author: Robin Amsters

This module is a complete rewrite of several previous loose scripts, except now
object oriented programming is used to increase efficiëncy.

"""
import math
import matplotlib.pyplot as plt
import mleq as ML
import numpy as np
import os
from scipy.stats import norm
from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory

class DataAnalysis(object):
    

    def getFilePath(self, msg):
        # Selecting file trough GUI
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filePath = askopenfilename(title = msg) # show an "Open" dialog box and return the path to the selected file
        return filePath

    def getDirectoryPath(self, msg):
        # Selecting directory trough GUI
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filePath = askdirectory(title = msg) # show an "Open" dialog box and return the path
        return filePath
   
    def getMeasurements(self, filePath, prefix):
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
                              
        NOTE: The .txt file has to end with 2 empty linespaces
        """    
        # Defining local variables
        fileHandle = open(filePath, 'r') #Internal name for file
        lines = fileHandle.readlines() #All lines in the file

        startMeasurement = False # When true, next lines can be considered to be part of the same measurement
        newLineCount = 0 # Counts the number of new lines (measurements are separated by 2 new lines)
        allMeasurements = [] # Contains all of the extracted corner measurements
        currentMeasurement = [] # Contains the measurement currently being extracted
         
        for line in lines:
         
            if line.count(' ') and startMeasurement and not line.count('calibratie'):
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
    
    def getSampleMeasurements(self, masterListLength, subListLength, sample):
        """
            Function that returns a list (masterList) that contains lists (subList)
            of specified length that contain only the specified number. This can be
            used to debug functions when no measurements are available
        """
        sampleMeasurements  = []
        
        sample = [(sample)]    
        
        for mlIndex in range(masterListLength):
            sampleMeasurement = []
            for slIndex in range(subListLength):
                sampleMeasurement.append(sample)
            sampleMeasurements.append(sampleMeasurement)
        
        return sampleMeasurements
    
    def getLevelOfSublists(self, masterList):
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
            return 1 + max(self.getLevelOfSublists(item) for item in masterList)
        else:
            return 0
    
    def plotDist(self, data, mu, std, figNum,figName,saveFig = False):
        
        figNotSaved = "Figure not saved."
        inputError = "Incorrect input."
        
        # Plotting the histograms
        plt.figure(figNum)
        plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')
        
        # Plot the PDFs
        plt.figure(figNum)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Fit results: mu = %.5f,  std = %.5f" % (mu, std)
        plt.title(title)
        
        # Saving figure
        if saveFig:
            saveDir = self.getDirectoryPath("Select a folder to save to figure: ")
            savePath = saveDir + figName
            
            if os.path.isfile(savePath):
              overrideSaveString =  raw_input("File already exists, do you want to override it? (y/n): ")
              
              if type(overrideSaveString) == str:
                  if overrideSaveString == 'y':
                      plt.savefig(savePath)
                      plt.show()
                      
                  elif overrideSaveString == 'n':
                      print figNotSaved
                      
                  else:
                      print inputError
                      print figNotSaved
            else:
                 plt.savefig(savePath)
                 plt.show()
                 
        else:
            print figNotSaved
            
               
    def removeSublistLevel(self, masterList, index):
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

class GetFeature(DataAnalysis):
    
    def __init__(self, refMeasurements, accuracy):
        self.filePath =  self.getFilePath("Please select a measurement file: ")
        self.refMeasurements = refMeasurements
        self.measurements = self.getMeasurements(self.filePath, 'corners_world =')
        self.accuracy = accuracy
        
    def setRef(self, newRef):
        self.refMeasurements = newRef
        
    def setMeasurements(self, newMeaserments):
        self.measurements = newMeaserments
        
    def checkReference(self, returnDiff = False):
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
        
        for measurement in self.measurements:
            
            matchedPoint = [] #datapoints (list of len 2) that have been matched
            
            for point in measurement: #Checking and selecting measurements
            
                if not len(point) == 2:
                    print lengthError
                    
                else:
                    x_p = point[0] #measured x coordinates
                    y_p = point[1] #measured y coordinates
        
                for ref in self.refMeasurements:
    
                    if not len(ref) == 2:
                        print lengthError
                        
                    else:
                        x_ref = ref[0] #reference x coordinates
                        y_ref = ref[1] #reference u coordinates
                        
                        diff_x = float(x_p) - float(x_ref) #difference in x coordinates
                        diff_y = float(y_p) - float(y_ref) #difference in y coordinates
                        
                        pointDiff = [diff_x, diff_y] #difference as list
                        distance = math.sqrt(pow(diff_x, 2) + pow(diff_y, 2))
                        
                        if distance <= self.accuracy and point not in matchedPoint:
                            # Add current point to matched points if accepted and not already in matchedPoint
                            if returnDiff:
                                matchedPoint.append(pointDiff)
                            else:
                                matchedPoint.append(point)
    
                        if len(matchedPoint) == len(self.refMeasurements) and matchedPoint not in matchedData:
                            # Add points to data when all have been matched against a reference and they are not yet in matchedData
                            matchedData.append(matchedPoint)
        
        return matchedData
           
    def getPolar(self, carthesianMeasurements):
        
        # Outputformat: r,t in tuples inside list
        
        polarMeasurements = []
        for measurement in carthesianMeasurements:

            polarMeasurement = []
            
            for point in measurement:

                x_p = float(point[0])
                y_p = float(point[1])
                
                point_pol = ML.cart2pol(x_p, y_p)
                polarMeasurement.append(point_pol)
            
            polarMeasurements.append(polarMeasurement)
            
        return polarMeasurements
                
    def getDistribution(self, measurements):
        
        inputError = "Incorrect input."
        
        try:

            len_sublists = len(measurements[0])
            
            if len_sublists <= 0:
                print inputError 
                
            elif len_sublists >= 1:
            
                measurements_point_A = super(GetFeature, self).removeSublistLevel(measurements, 0)
                
                # Extracting r and th coordinates 
                r_A = super(GetFeature, self).removeSublistLevel(measurements_point_A, 0)
                th_A = super(GetFeature, self).removeSublistLevel(measurements_point_A, 1)
                
                mu_r_A, std_r_A = norm.fit(r_A)
                params_r_A = (mu_r_A, std_r_A)
                
                mu_th_A, std_th_A = norm.fit(th_A)
                params_th_A  = (mu_th_A, std_th_A)
                
                if len_sublists >= 2:
                    
                    measurements_point_B = super(GetFeature, self).removeSublistLevel(measurements, 1)
                    
                    # Extracting r and th coordinates 
                    r_B = super(GetFeature, self).removeSublistLevel(measurements_point_B, 0)
                    th_B = super(GetFeature, self).removeSublistLevel(measurements_point_B, 1)
                    
                    mu_r_B, std_r_B = norm.fit(r_B)
                    params_r_B = (mu_r_B, std_r_B)                    
                    
                    mu_th_B, std_th_B = norm.fit(th_B)
                    params_th_B  = (mu_th_B, std_th_B)
                    

                    if len_sublists >= 3:
                        
                        measurements_point_C = super(GetFeature, self).removeSublistLevel(measurements, 2)
                    
                        # Extracting r and th coordinates 
                        r_C = super(GetFeature, self).removeSublistLevel(measurements_point_C, 0)
                        th_C = super(GetFeature, self).removeSublistLevel(measurements_point_C, 1)
                        
                        mu_r_C, std_r_C = norm.fit(r_C)
                        params_r_C = (mu_r_C, std_r_C)                    
                        
                        mu_th_C, std_th_C = norm.fit(th_C)
                        params_th_C  = (mu_th_C, std_th_C)
                        
                        return params_r_A, params_th_A, r_A, params_r_B, params_th_B, r_B, params_r_C, params_th_C, r_C
                    else:
                        return params_r_A, params_th_A, r_A, th_A, params_r_B, params_th_B, r_B, th_B
                        
                        if len_sublists > 3:
                            print inputError     
                    
                else:
                    return params_r_A, params_th_A, r_A
        
        except:
            print inputError
            
class GetOdometry(DataAnalysis):
    
    def __init__(self):
        
        # Setting reference
        self.refPath = self.getFilePath("Select a reference file: ")
        self.refMeasurements_s, self.refMeasurements_th = self.getReference()
        # Setting measurements
        self.measurementPath = self.getFilePath("Select a measurement file: ")
        self.measurements_s = self.getMeasurements(self.measurementPath, "s =")
        self.measurements_th = self.getMeasurements(self.measurementPath, "th =")
        
    def getReference(self):
        
        ref_s = []
        ref_th = []
        
        positions = self.getMeasurements(self.refPath, "pos =")  
        print positions
        print(len(positions))

        for index in xrange(0,len(positions),2):
            
            print index
            
            x_1 = float(positions[index][0][0])
            y_1 = float(positions[index][0][1])
            x_2 = float(positions[index+1][0][0])
            y_2 = float(positions[index+1][0][1])
            
            print (x_1)

            diff_x = x_1 - x_2
            diff_y = y_1 - y_2
            
            dist = math.sqrt(diff_x**2 + diff_y**2)
            angle = math.atan(diff_y/diff_x)
            
            ref_s.append([dist])
            ref_th.append([angle])
            
        return ref_s, ref_th
        
    def checkReference(self, dataType):
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
        
        if dataType == "s":
            measurements = self.measurements_s
            reference = self.refMeasurements_s
            
        elif dataType == "th":
            measurements = self.measurements_th
            reference = self.refMeasurements_th
        
        else:
            print "Incorrect dataType."
            measurements = []
            reference = []
        
        index = 0
        
        for measurement in measurements:
            
            for point in measurement: #Checking and selecting measurements
            
                if not len(point) == 1:
                    print lengthError
                    
                else:
                    dx = point[0] #measured distance or angle -> x
                    ref = reference[index] #reference to compare to
    
                if not len(ref) == 1:
                    print lengthError
                    
                else:
                    dx_ref = ref[0] #reference x coordinates
                    diff_x = float(dx) - float(dx_ref) #difference in x variable
                    distance = abs(diff_x)
                    matchedData.append(distance)
                    
                index += 1
        
        return matchedData
        
    def getDistribution(self, dx):
        
        mu_x, std_x = norm.fit(dx)
        
        return mu_x, std_x
        
        

    
