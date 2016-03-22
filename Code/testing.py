# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:35:54 2016

@author: Robin Amsters

test file for dataAnalysis
"""

from dataAnalysis import GetOdometry

testGetOdometry = GetOdometry()

#DEBUG
measurements_s = testGetOdometry.measurements_s
measurements_th = testGetOdometry.measurements_th
ref_s  = testGetOdometry.refMeasurements_s
ref_th  = testGetOdometry.refMeasurements_th
# END DEBUG

ds = testGetOdometry.checkReference("s")
dth = testGetOdometry.checkReference("th")

mu_ds, std_ds = testGetOdometry.getDistribution(ds)
mu_dth, std_dth = testGetOdometry.getDistribution(dth)

testGetOdometry.plotDist(ds, mu_ds, std_ds, 1, "/ds_0_5", True)
testGetOdometry.plotDist(dth, mu_dth, std_dth, 2, "/dth_0_5", True)