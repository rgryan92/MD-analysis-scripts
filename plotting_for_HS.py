# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 14:08:35 2017

@author: rgryan
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

hist = False  # plot histogram of gradmax distributions?

path = 'E:\\PhD\\Broady_data_backup\\UniMelb\\broady_data_rr\\HS_1-30-MAR\\UM_gradmax_info_March2017\\'
#path = 'E:\\PhD\\Broady_data_backup\\BOM\\spectra\\U\\hs\\BM_hs_gradmaxinfo_March2017\\'
file = 'all'
ext = '.txt'

data1 = pd.read_csv(path+file+ext, header=None, sep = ' ')
data1.columns = ['number', 'dec_hour', 'gradmax', 't_amb']

# drop any values greater than zero or temp less than 5
#  since I've seen by inspection that 
#  these don't make sense
data1 = data1.drop(data1[data1.gradmax > 3].index)
data1 = data1.drop(data1[data1.gradmax < -3].index)
data1 = data1.drop(data1[data1.t_amb < 15].index)
data = data1.dropna(how='any')

# Scatter plot of gradmax vs temp or time
# =======================================
plot = plt.figure()
figsize = (5,3)
fontsize = 14
yaxis = 't_amb'
xaxis = 'gradmax'
xlim = (-4,0)
ylim=(10,40)

'''
if hist == True:
    p = data.gradmax.plot.hist(bins=20, fontsize=fontsize, color='yellow')


    data.plot(x=xaxis, y=yaxis, style='go',figsize=figsize,
              fontsize=fontsize, xlim=xlim, ylim=ylim, 
              ax=p, secondary_y=True)       
else:
    p = data.plot(x=xaxis, y=yaxis, style='go',figsize=figsize,
              fontsize=fontsize, xlim=xlim, ylim=ylim)
fig = p.get_figure()
fig.savefig(path+file+'_vs_'+yaxis+'.png', bbox_inches='tight')  
# =======================================
'''
model = sm.OLS(data.t_amb, sm.add_constant(data.gradmax))
q = model.fit().params
results = model.fit()

x = np.arange(-5, 5)

ax = data.plot(x=xaxis, y=yaxis, kind='scatter', fontsize=fontsize, 
               figsize=figsize, color='y')
ax.plot(x, q.const+ q.gradmax*x, color='blue')
ax.set_xlim([-4, 4])
ax.set_ylim([10,45])
m = str(round(q[0], 3))
c = str(round(q[1], 3))
#print('y='+m+'x + '+c)
ax.text(-3,40.2, 'y='+m+'*x + '+c, fontsize=fontsize, color='blue')
fig = ax.get_figure()
fig.savefig(path+file+'_vs_'+yaxis+'.png', bbox_inches='tight') 