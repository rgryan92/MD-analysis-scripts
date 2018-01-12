# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 16:49:24 2017

@author: rgryan
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# CODE TO PLOT AMF vs OZONE SLANT COLUMNS, TO CALCULATE TOTAL COL OZONE

path = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\TIMTAM_QD_TOC\\o3_amf_lut_v2_0\\'
inst = 'UW'
file = inst+'_21FebPM_fromLUT'
ext  = '.dat'

doi = 21

figsize=(3,3)
fontsize=14
xlim=[0,25]
ylim=[-2e19, 1.8e20]

# colours...
if inst == 'BM':
    colour = 'g'
elif inst == 'UM':
    colour = 'b'
elif inst == 'NZ':
    colour == 'y'
else:
    colour = 'r'

o3data = pd.read_csv(path+file+ext, delim_whitespace=True, skiprows=6)
o3data.columns=['Day','SZA', 'SCD','AMF']

o3data = o3data[o3data['Day'] == doi]
o3data_ndacc = o3data[o3data['SZA'] > 85.99]
o3data_ndacc = o3data_ndacc[o3data_ndacc['SZA'] < 90.01]


def fit_line(x,y):
    X = sm.add_constant(x)
    model = sm.OLS(y, X)
    fit = model.fit()
    return fit.params[1], fit.params[0]

m , b = fit_line(o3data_ndacc['AMF'], o3data_ndacc['SCD'])

# m is retrieved VCD in molec/cm2
# need it first in molec/m2
m_ = m/(1e-4)

# Now to Dobson Units
md = m_/(2.867e20)

pts = np.linspace(o3data['AMF'].min(), o3data['AMF'].max(), 100)

p = o3data.plot(x='AMF', y='SCD', style=colour+'o', figsize=figsize, 
                fontsize=fontsize, xlim=xlim, ylim=ylim, legend=False)
#plt.scatter(o3data_ndacc['AMF'], o3data_ndacc['SCD'], color='blue')
p.plot(pts, m*pts + b, color='k')
p.text(1, 1.5e20, 'VCD = '+str(round(md, 2))+' DU', fontsize=fontsize)
p.set_xlabel('AMF', fontsize=fontsize)
p.set_ylabel('O3 dSCD (molec/cm$^2$)', fontsize=fontsize)
p_ = p.get_figure()
p_.savefig(path+file+'_'+str(doi)+'_result_plot.pdf', bbox_inches='tight')
#