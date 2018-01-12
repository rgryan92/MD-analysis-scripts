# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:46:27 2017

@author: rgryan
"""

# Import section
#====================================================================
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime
import pandas as pd
from windrose import WindroseAxes
import matplotlib.cm as cm
from windrose import plot_windrose

# Readin details (file name etc)
#====================================================================
datapath = '/Users/rgryan/Documents/PhD/Data/TIMTAM/Glenlitta data Feb-Jun 2017/'
datafilename = 'HD01D_Data_086392_45751039446330.txt'

# Define the date range to plot               
#====================================================================
an_year = 2017
start_month = 3
end_month = 3
start_day = 2
end_day = 20
start_hour = 6        # 0500 local time = 1900 UTC
end_hour = 20         # 2000 local time = 1000 UTC
                      # starting at hour=19, ending at hour=10 is what we're doing
                      #     in the QDOAS plotting Python script
                    
# Plot settings
# =========================================================================
save_plot = True             # Save the plots generated?
fontsize = 14
figsize = (60, 3)          
legend_pos = (1.12,1)        #(1.12,1) is good for 15x3 plots 
                             #(1.42,1) is good for 4x3 plots (just 1 day of data)
x_label_format = dates.DayLocator()   # x-axis Label style 
                                       # for multiple day plots, DateLocator() works
                                       # for single day plots, it doesn't (!!), so use
                                       #     YearLocator()
# Resampling of the data?
resample = True
resamFreq = '12min'

# Should not need to alter the code below here:
# The readin is using Pandas
#====================================================================
datafile = datapath+datafilename
metdata = pd.read_csv(datafile, header=0, sep = ';')

metdata.columns = ['hd', 'stationnumber', 'year', 'month', 'day', 'hour', 'min', 
                   'airtemp', 'airtempQ', 'RH', 'RHQ', 'windspeed', 'windspeedQ', 
                   'winddir', 'winddirQ', 'hashtag']

# Sort out datetime from strings of date data in different columns;
#====================================================================
metdata['datetime1'] = (metdata['year'].map(str) + '/' + metdata['month'].map(str) + '/'+
                        metdata['day'].map(str) + ' ' + metdata['hour'].map(str) +
                        ':' + metdata['min'].map(str))
metdata['datetime'] = pd.to_datetime(metdata['datetime1'], infer_datetime_format=True)

metdata.index = pd.to_datetime(metdata.pop('datetime1'), infer_datetime_format=True)

# This workaround converts to UTC time (Rather than AEST)
#====================================================================
metdata.index = metdata.index.tz_localize('UTC').tz_convert('Etc/GMT+10')
del metdata.index.name

# Convert the data we want to plot, to float values
#====================================================================
metdata['airtemp'] = metdata['airtemp'].astype(float)
metdata['windspeed'] = metdata['windspeed'].astype(float)
metdata['winddir'] = metdata['winddir'].astype(float)

if resample == True:
    metdata['airtemp'] = metdata.airtemp.resample(resamFreq).mean()   
    metdata['windspeed'] = metdata.windspeed.resample(resamFreq).mean()   
    metdata['winddir'] = metdata.winddir.resample(resamFreq).mean()   

metdata.reset_index(level=0, inplace=True)

startdate = datetime.datetime(an_year, start_month, start_day, (start_hour))  
enddate = datetime.datetime(an_year, end_month, end_day, (end_hour))


#%%
#ax = WindroseAxes.from_ax()

from pylab import * 

df4wr = pd.DataFrame()
df4wr['speed'] = metdata['windspeed']
df4wr['direction'] = metdata['winddir']
df4wr.index = pd.DatetimeIndex(metdata['index'])

#df4wr = df4wr[df4wr["datetime"].isin(pd.date_range(startdate, enddate))]
df4wr = df4wr[(df4wr.index > '2017-03-10') & (df4wr.index <= '2017-03-20')]

angles = df4wr['direction'].as_matrix() 
data = df4wr['speed'].as_matrix()
rad_angles = pi/180 * angles 

fig = figure(figsize=(8,8)) 
title('Wind Speed/Direction Frequency.', fontsize=13) 
ax = fig.add_subplot(111) 
fig.add_axes(([0.15,0.15,0.725,0.725]), polar=True) 
labels = arange(0,360,22.5) 
lines = arange(0,360,22.5) 
ax.axis('off') 
#bar(rad_angles, data, alpha=0.75, align='center', linewidth=0)
scatter(rad_angles, data, c=data)