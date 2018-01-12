# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 10:49:48 2017

@author: rgryan
"""

import pandas as pd
import numpy as np
import matplotlib as plt

qdfilepath = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\TIMTAM_QDOAS_output\\'
qdfilename = 'BM_21Feb17_338-370'
ext = '.ASC'

numcalwindows = 20

qdData = pd.read_csv(qdfilepath+qdfilename+ext, sep='\t', 
                     header=numcalwindows+1)


# Function to calculate the AMF as 1/cos(SZA)
#===========================================
def calc_simple_AMF(SZA):
    Sd = SZA
    Sr = Sd*(np.pi/180)
    A = np.cos(1/Sr)
    return A
#===========================================
# Apply the function to the SZA column in the dataframe
qdData['simple_AMF'] = qdData['SZA'].apply(calc_simple_AMF)
#===========================================

# Plot the SZA vs the simple AMF
#===========================================
f = qdData.plot(x='SZA', y='simple_AMF', xlim=[0,100],
                ylim=[-2, 2])