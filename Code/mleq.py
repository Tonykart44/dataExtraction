# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 16:28:21 2016

@author: Robin Amsters

Module containing Python equivalents of MATLAB functions
"""

import numpy as np


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return[rho, phi]

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return[x, y]
