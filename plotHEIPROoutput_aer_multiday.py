# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 08:55:27 2017

@author: rgryan
"""
# IMPORT SECTION
#===============
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib import cm
import datetime

path = 'E:\\Sciatran2\\AEROSOL_RETRIEVAL_v-1-5\\Campaign\\'
path2='aer_retr_7-9March2017_'
test = 't110'
location = path2+test+'\\'

# Date format for axes: (year, month, day, hour)
startdate = datetime.datetime(2017, 3, 7, 6)  
enddate = datetime.datetime(2017, 3, 9, 20)

tg = 'aer'

dates_list = np.arange(20170307, 20170310, 1)
df_list = []

for d in dates_list:
    date = str(d)
    pdf = pd.read_csv(path+location+date+'/general/retrieval_'+date+'.dat',
                     delim_whitespace=True, skiprows=1, header=None, 
                     parse_dates=[[0,1]], dayfirst=True)
    df_list.append(pdf)

all_profiles_df = pd.concat(df_list, axis=0)
all_profiles_df.columns = ['Date_Time', 'Nr', 'n_iter', 'chisq', 'H', 'd_s',
                           'gamma', 'gamma_max', 'scale', 'AOT361', 'err_AOT361'] 


# Plot daily aerosol extinction diurnal profiles
# ======================
# Filter out entries with very high errors
all_profiles_df  = all_profiles_df[all_profiles_df['err_AOT361']<0.1]     

x = np.array((all_profiles_df['Date_Time']))
y = np.array((all_profiles_df['AOT361']))
err = np.array((all_profiles_df['err_AOT361']))

fig = plt.figure(figsize=(60,3))
ax=fig.add_subplot(111)
ax.errorbar(x,y,yerr=err, fmt='b.', label= 'AOT361')
ax.set_xlim(startdate, enddate)
ax.set_ylim(0, 0.75)
fig.savefig(path+location+test+'_'+tg+'_VCD_'+date+'.png', 
                    bbox_inches='tight')


#%%
# Now heatmap vertical profiles

# Generate dataframe from each day's profile file
df_list1 = []
for d in dates_list:
    date = str(d)
    year = (str(d))[:4]
    month = (str(d))[4:6]
    day = (str(d))[6:]
    
    ddmmyyyy = day+'/'+month+'/'+year
    
    prdf = pd.read_csv(path+location+date+'/general/all_profiles_'+date+'.dat',
                     delim_whitespace=True, header=0)
    prdf_t = prdf.transpose()
    prdf_t = prdf_t.reset_index()
    prdf_t = prdf_t.iloc[1:]
    dates2go = []
    for i in np.arange(len(prdf_t)):
        dates2go.append(ddmmyyyy)
    prdf_t['Date'] = pd.Series(dates2go)
    prdf_t['Time'] = prdf_t['index']
    prdf_t['Date_Time'] = prdf_t['Date']+' '+prdf_t['Time']
    prdf_t['date_time'] = prdf_t.iloc[:,23:].apply(pd.to_datetime, errors='coerce')
    df_list1.append(prdf_t)

# Now concatenate each day into one dataframe
all_vprof_df_t = pd.concat(df_list1, axis=0)
all_vprof_df_t = all_vprof_df_t[all_vprof_df_t > -1000] # remove values of -10000

# set the dataframe index to datetime, needed for plotting
all_vprof_df_t = all_vprof_df_t.set_index(all_vprof_df_t['date_time'])
all_vprof_df_t = all_vprof_df_t.iloc[:,1:21]

# add the altitude values to the profile dataframe
altgrid = np.arange(0.1, 4, 0.2)
altgridcolumns = []
for i in altgrid:
    altgridcolumns.append(str(i))
all_vprof_df_t.columns = altgridcolumns
all_vprof_df = all_vprof_df_t.transpose()
#%%
# Now the heatmap plotting:
fig, ax = plt.subplots(figsize=(60,3.5))

# This bit deals with the x and y ticks
xticks = all_vprof_df.columns
keptticks = xticks[::int(len(xticks)/30)]
xticks = ['' for a in xticks]
xticks[::int(len(xticks)/30)] = keptticks

yticks = all_vprof_df.index[::-1]
keptticks = yticks[::int(len(yticks)/6)]
yticks = ['' for a in yticks]
yticks[::int(len(yticks)/6)] = keptticks

# sb.heatmap is the actual plot
# vmin and vmax control the upper and lower bounds of the colorbar
sb.heatmap(all_vprof_df[::-1], cmap=cm.RdYlBu_r, ax=ax, vmin=0, vmax=0.3,
           xticklabels=xticks, yticklabels=yticks)

plt.yticks(rotation=0)
plt.xticks(rotation=40)
#plt.ylim(0,15)

plt.savefig(path+location+test+'_aerExt_heatmap_'+date+'.png', 
                    bbox_inches='tight')