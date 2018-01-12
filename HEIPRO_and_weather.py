# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:39:08 2017

@author: rgryan

****************************************************************
READ IN HEIPRO OUTPUT DATA AND WEATHER DATA FOR COMPARISON PLOTS
****************************************************************
"""
# 1. Setup information
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from pylab import * 
import numpy as np
from matplotlib import cm
import datetime

# Path to the HEIPRO data
#========================
path = '/Users/rgryan/Documents/PhD/Data/TIMTAM/test_NO2_HEIPRO_output/'
NO2path = 'BM_March2017_NO2retr_t12/'
HCHOpath = 'BM_March2017_HCHOretr_t1/'
HONOpath = 'BM_March2017_HONOretr_t1/'

# Path to the weather data
#====================================================================
wpath = '/Users/rgryan/Documents/PhD/Data/TIMTAM/Glenlitta data Feb-Jun 2017/'
wfilename = 'HD01D_Data_086392_45751039446330.txt'

# Path to colour index data
cipath = path
cifile = 'BM_CI_March2017.txt'

# dates of interest
#==================
startdate = datetime.datetime(2017, 3, 2, 6) # (year, month, day, hour)
enddate = datetime.datetime(2017, 3, 20, 20)
dates_list = np.arange(20170302, 20170320)

#tg3 = 'HONO'
# Resample data?
#===============
resample = False
resample_freq = 'H'    # 'D' = calender day, 'H' = hourly

# Format for figure saving (.png or .pdf)
#========================================
figfmt = '.png'

# 2. READ IN HEIPRO OUTPUT DATA
#====================================================================

def readin_HEIPRO_conc_data(location, tg1, tg):
    df_list = []
    tgdf_list = []
    for d in dates_list:
        date = str(d)
        pdf = pd.read_csv(path+location+date+'/general/'+tg1+'_retrieval_'+date+'.dat',
                      delim_whitespace=True, skiprows=1, header=None,
                      parse_dates=[[0,1]], dayfirst=True)
        df_list.append(pdf)
    all_profiles_df = pd.concat(df_list, axis=0)
    all_profiles_df.columns = ['Date_Time', tg+'_Nr', tg+'_n_iter', tg+'_chisq', tg+'_H', tg+'_d_s',
                           tg+'_gamma', tg+'_gamma_max', tg+'_VCD', tg+'_VCD_error', 
                           tg+'_Retr_height', tg+'_surf_num_density',tg+'_err_surf_num_dens', 
                           tg+'_surf_vmr', tg+'_err_surf_vmr', tg+'_surf_conc', tg+'_err_surf_conc']
    all_profiles_df[tg+'_surf_vmr_ppb'] = all_profiles_df[tg+'_surf_vmr']*1000
    all_profiles_df[tg+'_err_surf_vmr_ppb'] = all_profiles_df[tg+'_err_surf_vmr']*1000
    all_profiles_df = all_profiles_df.sort_values('Date_Time')
    all_profiles_df = all_profiles_df.drop_duplicates('Date_Time')
    all_profiles_df['dt'] = all_profiles_df['Date_Time']
    all_profiles_df.index = all_profiles_df['dt']
    return all_profiles_df

NO2_data = readin_HEIPRO_conc_data(NO2path, 'NO2', 'NO2')
HCHO_data = readin_HEIPRO_conc_data(HCHOpath, 'HCHO', 'HCHO')
HONO_data = readin_HEIPRO_conc_data(HONOpath, 'HCHO', 'HONO')

tgdata = NO2_data
HCHOcolslist = ['HCHO_VCD','HCHO_VCD_error','HCHO_surf_vmr_ppb','HCHO_err_surf_vmr_ppb']
HONOcolslist = ['HONO_VCD','HONO_VCD_error','HONO_surf_vmr_ppb','HONO_err_surf_vmr_ppb']
for i in HCHOcolslist:
    tgdata[i] = HCHO_data[i]
for j in HONOcolslist:
    tgdata[j] = HONO_data[j]
#%%
# 3. READ IN WEATHER DATA
#====================================================================
wdatafile = wpath+wfilename
metdata = pd.read_csv(wdatafile, header=0, sep = ';')

metdata.columns = ['hd', 'stationnumber', 'year', 'month', 'day', 'hour', 'min', 
                   'airtemp', 'airtempQ', 'RH', 'RHQ', 'windspeed', 'windspeedQ', 
                   'winddir', 'winddirQ', 'hashtag']

# Sort out datetime from strings of date data in different columns;
metdata['datetime1'] = (metdata['year'].map(str) + '/' + metdata['month'].map(str) + '/'+
                        metdata['day'].map(str) + ' ' + metdata['hour'].map(str) +
                        ':' + metdata['min'].map(str))
metdata['Date_Time'] = pd.to_datetime(metdata['datetime1'], infer_datetime_format=True)

# get data only in required date range
mask = (metdata['Date_Time']>startdate) & (metdata['Date_Time']<= enddate)
metdata_ = metdata.loc[mask]

# Convert the data we want to plot, to float values
metdata['airtemp'] = metdata['airtemp'].astype(float)
metdata['windspeed'] = metdata['windspeed'].astype(float)
metdata['winddir'] = metdata['winddir'].astype(float)

# 4. Read in the colour index data
#====================================================================
cidata = pd.read_csv(path+'BM_CI_March2017.txt', header=None, sep=' ',
                     parse_dates=[[3,4]], dayfirst=True)                     
cidata.columns = ['Date_Time', 'sza_uncorrected', 'azim', 'EA', 'norm_ave_int',
                  'CI']
cidata = cidata.sort_values('Date_Time')    # Sort the values by date and time
cidata = cidata.drop_duplicates(['Date_Time'], keep='first') # Drop the duplicate date_times
cidata = cidata.loc[mask]  # Take only the data in required date range

#%%
# 5. Now merge the weather and HEIPRO dataframes
#====================================================================
combined1 = pd.merge_asof(tgdata, metdata_, on='Date_Time')
combined = pd.merge_asof(combined1, cidata, on='Date_Time')
#combined_ = combined
combined.index = pd.DatetimeIndex(combined['Date_Time'])
if resample==True:
    combined = combined.resample(resample_freq).mean()
else:
    combined = combined

#%%
# Rose plot for TG vs wind direction and speed
#====================================================================
angles = combined['winddir'].as_matrix() 
speed = combined['windspeed'].as_matrix()
tgvalues = combined['HONO_surf_vmr_ppb'].as_matrix()
rad_angles = pi/180 * angles 

ttl = 'Winds_&_HONOsurfVMR, March2017'
fig = figure(figsize=(7,7)) 
title(ttl, fontsize=13) 
ax = fig.add_subplot(111) 
fig.add_axes(([0.15,0.15,0.725,0.725]), polar=True) 
labels = arange(0,360,22.5) 
lines = arange(0,360,22.5)
ax.axis('off') 
#bar(rad_angles, data, alpha=0.75, align='center', linewidth=0)
s = scatter(rad_angles, speed, c=tgvalues, linewidths=0)
#s = scatter(rad_angles, speed)
fig.colorbar(s)
s.set_clim([0,0.5])
savefig(path+ttl+figfmt, bbox_to_anchor='tight')

#%%
# Linear plot of TG value vs met parameter
#====================================================================
xval = 'HONO_surf_vmr_ppb'
yval = 'airtemp'
p1 = combined.plot(x=xval, y=yval, style='mo', xlim=[0,0.6],
                   ylim=[10,40], figsize=(6,5))
p1.set_xlabel(xval)
p1.legend_.remove()
p1.set_ylabel(yval)
p1_ = p1.get_figure()
p1_.savefig(path+xval+'_vs_'+yval+figfmt, bbox_to_anchor='tight')
#%%
# Timeseries plot of tg values
#====================================================================
xval = 'Date_Time'
yval = 'HONO_surf_vmr_ppb'
yerr = 'HONO_err_surf_vmr_ppb'

x=np.array((combined[xval]))
y=np.array((combined[yval]))
err=np.array((combined[yerr]))

fg = plt.figure(figsize=(50,3))
ax1 = fg.add_subplot(111)
ax1.errorbar(x,y,yerr=err, fmt='m.')
ax1.set_xlim(startdate, enddate)
ax1.set_ylim(0,0.6)

p2_ = ax1.get_figure()
p2_.savefig(path+xval+'_vs_'+yval+figfmt, bbox_to_anchor='tight')
#%%
# Timeseries plot of tg ratios
#====================================================================
N = 'HCHO_surf_vmr_ppb'
Ne = 'HCHO_err_surf_vmr_ppb'
D = 'NO2_surf_vmr_ppb'
De = 'NO2_err_surf_vmr_ppb'

# need a function to define the propagated error
def div_err_prop(A, dA, B, dB):
    err = np.sqrt(((dA/A)**2)+((dB/B)**2))
    return err

combined['roi'] = (combined[N]/combined[D])
combined['err_roi'] = div_err_prop(combined[N], combined[Ne],
                            combined[D], combined[De])
combined_ = combined[combined['err_roi']<0.5]

x=np.array((combined_['Date_Time']))
y=np.array((combined_['roi']))
err=np.array((combined_['err_roi']))

fg = plt.figure(figsize=(50,3))
ax1 = fg.add_subplot(111)
ax1.errorbar(x,y,yerr=err, fmt='c.')
ax1.set_xlim(startdate, enddate)
ax1.set_ylim(0,2.5)
p3_ = ax1.get_figure()
p3_.savefig(path+N+'_div_'+D+figfmt, bbox_to_anchor='tight')

#%%
# Rose plot for TG ratios vs wind direction and speed
#====================================================================
angles = combined_['winddir'].as_matrix() 
speed = combined_['windspeed'].as_matrix()
tgvalues = combined_['roi'].as_matrix()
rad_angles = pi/180 * angles 

ttl = N+' div '+D
fig = figure(figsize=(7,7)) 
title(ttl, fontsize=13) 
ax = fig.add_subplot(111) 
fig.add_axes(([0.15,0.15,0.725,0.725]), polar=True) 
labels = arange(0,360,22.5) 
lines = arange(0,360,22.5)
ax.axis('off') 
#bar(rad_angles, data, alpha=0.75, align='center', linewidth=0)
s = scatter(rad_angles, speed, c=tgvalues, linewidths=0)
#s = scatter(rad_angles, speed)
fig.colorbar(s)
s.set_clim([0,2.0])
savefig(path+ttl+figfmt, bbox_to_anchor='tight')

#%%
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Create wind speed and direction variables

ws = np.random.random(500) * 6
wd = np.random.random(500) * 360
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()