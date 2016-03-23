# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:35:54 2016

@author: Robin Amsters

Data analysis on getFeature data
"""

from dataAnalysis import GetFeature

saveFigs = True
numOfBins = 25

# Reference points from camera measurements
realRef = [[0.8377, 0.0794],[0.5229, -0.6547]]


# Getting distribution on r and theta
testGetFeature = GetFeature(realRef, 0.044)

measurements = testGetFeature.measurements # Only for debug

filteredMeasurements = testGetFeature.checkReference() 
filteredPolar = testGetFeature.getPolar(filteredMeasurements)

params_r_A, params_th_A, r_A, th_A, params_r_B, params_th_B, r_B, th_B = testGetFeature.getDistribution(filteredPolar)

# Random noise centered around measurement
testGetFeature.plotDist(r_A, params_r_A[0], params_r_A[1], numOfBins, 1, '/dist_noise_r_A', saveFigs)
testGetFeature.plotDist(th_A, params_th_A[0], params_th_A[1], numOfBins, 2, '/dist_noise_th_A',saveFigs)

testGetFeature.plotDist(r_B, params_r_B[0], params_r_B[1], numOfBins, 3, '/dist_noise_r_B',saveFigs)
testGetFeature.plotDist(th_B, params_th_B[0], params_th_B[1], numOfBins, 4, '/dist_noise_th_B',saveFigs)


# Reference points from camera measurements in polar 
realRef = [[[0.8377, 0.0794]],[[0.5229, -0.6547]]]

realRefPolar = testGetFeature.getPolar(realRef)
testGetFeature.setRef = realRefPolar
testGetFeature.setMeasurements = filteredPolar
polarDiff = testGetFeature.checkReference(True)
params_r_A, params_th_A, r_A, th_A, params_r_B, params_th_B, r_B, th_B = testGetFeature.getDistribution(polarDiff)

# Random noise centered around difference between reference and measurment
testGetFeature.plotDist(r_A, params_r_A[0], params_r_A[1], numOfBins, 5, '/dist_diff_r_A',saveFigs)
testGetFeature.plotDist(th_A, params_th_A[0], params_th_A[1], numOfBins, 6, '/dist_diff_th_A',saveFigs)

testGetFeature.plotDist(r_B, params_r_B[0], params_r_B[1], numOfBins, 7, '/dist_diff_r_B',saveFigs)
testGetFeature.plotDist(th_B, params_th_B[0], params_th_B[1], numOfBins, 8, '/dist_diff_th_B',saveFigs)