# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:39:08 2018

@author: rgryan
"""

# Bar charts for HEIPRO stats tests

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

path = 'E:\\Sciatran2\\TRACEGAS_RETRIEVAL_v-1-4\\Campaign\\'

tg = 'HONO'  # 'HONO'

option = 'diurnalppm'
erroption = 'diurnalppmerrors'

# options are... profiledetails, profileErrors, diurnalVCD, diurnalVCDerrors, diurnalppm, diurnalppmerrors

testsets = ['aerGext', 'aerSH', 'aerAsy','aerSSA', 'tgSH', 'tgGC', 'apElev']  

percentages = []
errpercentages = []
for test in testsets:
    df = pd.read_csv(path+tg+'_'+test+'_resultplots/apriori_tests_'+option+'.txt',
                  sep='\t', header=0)
    df_mean = df['mean'].mean()  # calculate the mean of all values
    df_std = df['std'].mean()    # calculate the standard deviation of the mean
    df_perc = 100*(df_std/df_mean)
    percentages.append(df_perc)  # standard deviation as a percentage of the mean, as a way to normalise
    
    errdf = pd.read_csv(path+tg+'_'+test+'_resultplots/apriori_tests_'+erroption+'.txt',
                  sep='\t', header=0)
    errdf_mean = errdf['mean'].mean()  # calculate the mean of all values
    errdf_std = errdf['std'].mean()    # calculate the standard deviation of the mean
    errdf_perc = 100*(errdf_std/errdf_mean)
    errpercentages.append(errdf_perc)  # standard deviation as a percentage of the mean, as a way to normalise
    
fig1, ax1 = plt.subplots()
f = ax1.bar(np.arange(len(percentages)), percentages, color='orangered')
ax1.set_ylabel('Std as % of mean')
ax1.set_title(tg+' '+option+' std as % of mean')
ax1.set_xticklabels(('z', 'aerGext', 'aerSH', 'aerAsy','aerSSA', 'tgSH', 'tgGC', 'apElev'))

fig2, ax2 = plt.subplots()
g = ax2.bar(np.arange(len(errpercentages)), errpercentages, color='orangered')
ax2.set_ylabel('Std as % of mean')
ax2.set_title(tg+' '+erroption+' std as % of mean')
ax2.set_xticklabels(('z', 'aerGext', 'aerSH',  'aerAsy','aerSSA','tgSH', 'tgGC', 'apElev'))