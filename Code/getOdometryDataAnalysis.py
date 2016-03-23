# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:35:54 2016

@author: Robin Amsters

test file for dataAnalysis
"""

from dataAnalysis import GetOdometry

saveFigs = True
numOfBins = 5

GetOdometry1 = GetOdometry()

#DEBUG
measurements_s = GetOdometry1.measurements_s
measurements_th = GetOdometry1.measurements_th
ref_s  = GetOdometry1.refMeasurements_s
ref_th  = GetOdometry1.refMeasurements_th
# END DEBUG

ds = GetOdometry1.checkReference("s")
dth = GetOdometry1.checkReference("th")

mu_ds, std_ds = GetOdometry1.getDistribution(ds)
mu_dth, std_dth = GetOdometry1.getDistribution(dth)

GetOdometry1.plotDist(ds, mu_ds, std_ds, numOfBins, 1, "/ds_0_0_5", saveFigs)
GetOdometry1.plotDist(dth, mu_dth, std_dth, numOfBins, 2, "/dth_0_0_5", saveFigs)