# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:02:25 2017

@author: rgryan

Updated code for slant column comparison and stats
"""
import pandas as pd

path = 'E:/PhD/Broady_data_backup/Broady_QDOAS_output/'


BM_uv = ''
BM_vs = ''
UM_uv = ''
UM_vs = ''
UW_uv = ''
UW_vs = ''
NZ_uv = ''
NZ_vs = ''

def pandasreadin(file, fitrange, poi):
    # Do the pandas read in
    df_ = pd.read_csv(path+file+'.txt', header=0, sep='\t',
                   parse_dates=[['date_AEST','time_AEST']], dayfirst=True)
    df_ = df_[df_['Elev. viewing angle']<80] # remove the 90 deg values
    
    # Include only the bits we care about
    df = pd.DataFrame()
    df['date_time'] = df_['date_AEST_time_AEST']
    df['EA'] = df_['Elev. viewing angle']
    df['SZA'] = df_['SZA']
    df[fitrange+'.SlCol('+poi+')'] = df_[fitrange+'.SlCol('+poi+')']
    df[fitrange+'.SlErr('+poi+')'] = df_[fitrange+'.SlErr('+poi+')']
    df[fitrange+'.RMS'] = df_[fitrange+'.RMS']
    df = df[df[fitrange+'.SlCol('+poi+')']>10]
    
    # Break in to elevation angle specific dataframes
    df30 = df[df['EA']>25]
    df30_ = df[df['EA']<25]
    df20 = df30_[df30_['EA']>18]
    df20_= df[df['EA']<15]
    df10 = df20_[df20_['EA']>8]
    df10_= df[df['EA']<7]
    df5 = df10_[df10_['EA']>4]
    
    dfset = [df, df30, df20, df10, df5]
    return dfset

BM_uv = pandasreadin('BM_March17_UV_FH1', '338-370', 'O4')
BM_vs = pandasreadin('BM_March17_vis_FH1', '460-490', 'O4')
UM_uv = pandasreadin('UM_March17_UV_FH1', '338-370', 'O4')
UM_vs = pandasreadin('UM_March17_vis__FH1', '460-490', 'O4')
UW_uv = pandasreadin('UW_March17_UV_FH1', '338-370', 'O4')
UW_vs = pandasreadin('UW_March17_vis_FH1', '460-490', 'O4')
NZ_uv = ''
NZ_vs = ''

#%%

# Plot O4 timeseries from each instrument

import datetime
startdate = datetime.datetime(2017, 3, 16, 6,00)  # format: (year, month, day, hour, min)
enddate = datetime.datetime(2017, 3, 20, 18, 0)

#1. UV O4 scds
figsize = (10,3)
UV_O4scd_plot = BM_uv[1].plot(x='date_time', y='338-370.SlCol(O4)', style = 'g.', figsize=figsize)
UM_uv[1].plot(x='date_time', y='338-370.SlCol(O4)', style = 'b.', ax=UV_O4scd_plot)
UW_uv[1].plot(x='date_time', y='338-370.SlCol(O4)', style = 'r.', ax=UV_O4scd_plot)
UV_O4scd_plot.set_xlim(startdate, enddate)
UV_O4scd_plot.set_ylim(0, 2.5e43)
UV_O4scd_plot.legend(['BM', 'UM', 'UW'], loc=2, bbox_to_anchor=(1,1))
UV_O4scd_plot.set_title('O4 dSCD 30 deg EA - UV range')

#2.VIS O4 scds
figsize = (10,3)
vis_O4scd_plot = BM_vs[1].plot(x='date_time', y='460-490.SlCol(O4)', style = 'g.', figsize=figsize)
UM_vs[1].plot(x='date_time', y='460-490.SlCol(O4)', style = 'b.', ax=vis_O4scd_plot)
UW_vs[1].plot(x='date_time', y='460-490.SlCol(O4)', style = 'r.', ax=vis_O4scd_plot)
vis_O4scd_plot.set_xlim(startdate, enddate)
vis_O4scd_plot.set_ylim(0, 2.5e43)
vis_O4scd_plot.legend(['BM', 'UM', 'UW'], loc=2, bbox_to_anchor=(1,1))
vis_O4scd_plot.set_title('O4 dSCD 30 deg EA - vis range')

#%%
#1. UV O4 RMS
figsize = (10,3)
UV_O4rms_plot = BM_uv[1].plot(x='date_time', y='338-370.RMS', style = 'g.', figsize=figsize)
UM_uv[1].plot(x='date_time', y='338-370.RMS', style = 'b.', ax=UV_O4rms_plot)
UW_uv[1].plot(x='date_time', y='338-370.RMS', style = 'r.', ax=UV_O4rms_plot)
UV_O4rms_plot.set_xlim(startdate, enddate)
UV_O4rms_plot.set_ylim(0, 0.001)
UV_O4rms_plot.legend(['BM', 'UM', 'UW'], loc=2, bbox_to_anchor=(1,1))
UV_O4rms_plot.set_title('RMS 30 deg EA - UV range')

#2.VIS O4 scds
figsize = (10,3)
vis_O4rms_plot = BM_vs[1].plot(x='date_time', y='460-490.RMS', style = 'g.', figsize=figsize)
UM_vs[1].plot(x='date_time', y='460-490.RMS', style = 'b.', ax=vis_O4rms_plot)
UW_vs[1].plot(x='date_time', y='460-490.RMS', style = 'r.', ax=vis_O4rms_plot)
vis_O4rms_plot.set_xlim(startdate, enddate)
vis_O4rms_plot.set_ylim(0, 0.001)
vis_O4rms_plot.legend(['BM', 'UM', 'UW'], loc=2, bbox_to_anchor=(1,1))
vis_O4rms_plot.set_title('RMS 30 deg EA - vis range')

#%%
k = BM_uv[0]
