# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 08:01:11 2016

@author: robin
"""

import dataExtraction as dE

filePath = dE.getFilePath()
measurements,lines = dE.getMeasurements(filePath, 'pos =')