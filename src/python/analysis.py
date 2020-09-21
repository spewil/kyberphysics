# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:31:59 2020

@author: gonca
"""

import os
import numpy as np
import matplotlib.pyplot as plt

#fname = ''
metadata = os.path.splitext(fname)[0] + '.csv'
data = np.fromfile(fname, dtype=np.float32)
channels = np.genfromtxt(metadata)
data = data.reshape((len(channels),-1,64))

stack = np.vstack([data[i,:,0] + i * 15000 for i,c in enumerate(channels)])
plt.plot(stack.T)