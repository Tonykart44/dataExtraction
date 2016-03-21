# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:35:54 2016

@author: Robin Amsters

test file for dataAnalysis
"""

from dataAnalysis import GetOdometry

testGetOdometry = GetOdometry()
measurements_s = testGetOdometry.measurements_s
measurements_th = testGetOdometry.measurements_th
ref = testGetOdometry.refMeasurements
tst = testGetOdometry.checkReference(True)