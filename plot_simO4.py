# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:57:08 2017

@author: rgryan
"""

import pandas as pd
import datetime

startdate = datetime.datetime(2017, 3, 7, 7,30)  
enddate = datetime.datetime(2017, 3, 7, 18, 0)

# Read in O4 simulations
simpath = 'E:/Sciatran2/AEROSOL_RETRIEVAL_v-1-5/Campaign/'

# read in qdoas file for O4 observations
qdpath = 'E:\\PhD\\Broady_data_backup\\Broady_QDOAS_output/'
qdfileUV = 'BM_March17_UV_FH1.txt'
qdfileVIS = 'BM_March17_vis_FH1.txt'
#%%	

# Read in qdoas file
qddfUV = pd.read_csv(qdpath+qdfileUV, header=0, sep='\t',
                   parse_dates=[['date_AEST','time_AEST']], dayfirst=True)
qddfUV = qddfUV.sort_values('date_AEST_time_AEST')
#qddfUV = qddfUV.set_index(pd.DatetimeIndex(qddfUV['date_AEST_time_AEST']))
qddfUV = qddfUV[qddfUV['Elev. viewing angle']<80] # drop 90 deg values
qddfUV = qddfUV[qddfUV['338-370.SlCol(O4)']>0] # Weed out failed results which have RMS = 1e-5

qddfVIS = pd.read_csv(qdpath+qdfileVIS, header=0, sep='\t',
                   parse_dates=[['date_AEST','time_AEST']], dayfirst=True)
qddfVIS = qddfVIS.sort_values('date_AEST_time_AEST')
#qddfVIS = qddfVIS.set_index(pd.DatetimeIndex(qddfVIS['date_AEST_time_AEST']))
qddfVIS = qddfVIS[qddfVIS['Elev. viewing angle']<80] # drop 90 deg values

qddf = pd.merge_asof(qddfUV, qddfVIS, on='date_AEST_time_AEST')
qddf = qddf.set_index(pd.DatetimeIndex(qddf['date_AEST_time_AEST']))


qddf30 = qddf[qddf['Elev. viewing angle_x']>26]
qddf30 = qddf30[qddf30['Elev. viewing angle_y']>26]
qddf30_ = qddf[qddf['Elev. viewing angle_x']<15]
qddf10 = qddf30_[qddf30_['Elev. viewing angle_x']>8]
qddf10 = qddf10[qddf10['Elev. viewing angle_y']>8]

#%%
simtests = ['aer_retr_7-9March2017_t133', 'aer_retr_7-9March2017_t134', 'aer_retr_7-9March2017_t135']
#simtests = ['BM_aer_retr_7March2017_t81']
simdfs30 = []
simdfs10 = []

od360 = 4.291e-46

for t in simtests:
    simdf = pd.read_csv(simpath+t+'/20170307/general/meas_20170307.dat',
                           delim_whitespace=True, header=0, parse_dates=[['date', 'time']],
                            dayfirst=True)
    simdf = simdf[simdf['elev']<80] # drop 90 deg values
    simdf = simdf[simdf['O4retr']>0.00001]  # remove errors which are negative results and values ~1e-51
    simdf = simdf[simdf['O4retr']<0.1]
    simdf['O4retr_scd'] = simdf['O4retr']/od360
    simdf['O4meas_scd'] = simdf['O4meas']/od360
    simdf['err_O4meas_scd'] = simdf['err_O4meas']/od360
    simdf30 = simdf[simdf['elev']>28]
    simdf30_ = simdf[simdf['elev']<18]
    simdf10 = simdf30_[simdf30_['elev']>8]
    
    simdfs30.append(simdf30)
    simdfs10.append(simdf10)
    
sim_sh07 = simdfs30[0]
sim_sh08 = simdfs30[1]
sim_sh10 = simdfs30[2]
#sim_sh022 = simdfs10[3]
#sim_sh010 = simdfs10[4]

simplot = sim_sh07.plot(x='date_time', y='O4retr_scd', style='bo')
sim_sh08.plot(x='date_time', y='O4retr_scd', style='mo', ax=simplot)
sim_sh10.plot(x='date_time', y='O4retr_scd', style='yo', ax=simplot)
#sim_sh022.plot(x='date_time', y='O4retr_scd', style='ro', ax=simplot)
#sim_sh030.plot(x='date_time', y='O4retr_scd', style='go', ax=simplot)
#sim_sh005.plot(x='date_time', y='O4meas_scd', yerr='err_O4meas_scd',
#               ax=simplot, color='black')
qddf30['338-370.SlCol(O4)'].plot(color='black', ax=simplot)
#qddf30['460-490.SlCol(O4)'].plot(color='brown', ax=simplot)

simplot.set_xlim(startdate, enddate)
simplot.set_ylim(2.4e43,4.8e43)
simplot.legend(['0.7', '0.85', '1.0', 'Measured_360 nm'], loc=2, bbox_to_anchor=(1,1))
simplot.set_ylabel('O4 dSCD')
f = simplot.get_figure()
#f.savefig(simpath+'BM_7March_sim_vs_meas_O4dSCD_10deg.png', bbox_inches='tight')