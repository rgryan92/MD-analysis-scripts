# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:57:08 2017

@author: rgryan
"""

import pandas as pd

simpath = '/Volumes/Expansion Drive/PhD/Broady_data_backup/Broady_HEIPRO_output/'

simtests = ['BM_aer_retr_7March2017_t75', 'BM_aer_retr_7March2017_t76', 'BM_aer_retr_7March2017_t77']
simdfs30 = []
simdfs10 = []

od360 = 4.291e-46

for t in simtests:
    simdf = pd.read_csv(simpath+t+'/20170307/general/meas_20170307.dat',
                           delim_whitespace=True, header=0, parse_dates=[['date', 'time']],
                            dayfirst=True)
    simdf = simdf[simdf['elev']<80] # drop 90 deg values
    simdf = simdf[simdf['O4retr']>0.00001]  # remove errors which are negative results and values ~1e-51
    simdf = simdf[simdf['O4retr']<0.2]
    simdf['O4retr_scd'] = simdf['O4retr']/od360
    simdf['O4meas_scd'] = simdf['O4meas']/od360
    simdf30 = simdf[simdf['elev']>28]
    simdf30_ = simdf[simdf['elev']<18]
    simdf10 = simdf30_[simdf30_['elev']>8]
    
    simdfs30.append(simdf30)
    simdfs10.append(simdf10)
    
sim_sh05 =  simdfs10[0]
sim_sh075 =  simdfs10[1]
sim_sh1 =  simdfs10[2]

simplot = sim_sh05.plot(x='date_time', y='O4retr_scd', style='ko')
sim_sh05.plot(x='date_time', y='O4meas_scd', style='ro', ax=simplot)