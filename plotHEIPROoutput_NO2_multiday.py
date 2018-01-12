# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 08:55:27 2017

@author: rgryan
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib import cm
import matplotlib.dates as dates
import datetime

#path = 'C:\\Sciatran2\\AEROSOL_RETRIEVAL_v-1-5\\Campaign\\'
#path2 = 'BM_aer_retr_7March2017_'

path = 'C:\\Sciatran2\\TRACEGAS_RETRIEVAL_v-1-4\\Campaign\\'
path2='BM_March2017_NO2retr_'
test = 't12'
location = path2+test+'\\'

# Date format for axes: (year, month, day, hour)
startdate = datetime.datetime(2017, 3, 1, 6)  
enddate = datetime.datetime(2017, 3, 31, 20)

tg = 'NO2'

all_profiles_df = pd.DataFrame()

dates_list = np.arange(20170301, 20170331, 1)
df_list = []
#%%

for d in dates_list:
    date = str(d)
    pdf = pd.read_csv(path+location+date+'/general/'+tg+'_retrieval_'+date+'.dat',
                     delim_whitespace=True, skiprows=1, header=None, 
                     parse_dates=[[0,1]], dayfirst=True)
    df_list.append(pdf)
all_profiles_df = pd.concat(df_list, axis=0)
all_profiles_df.columns = ['Date_Time', 'Nr',  'n_iter', 'chisq', 'H', 'd_s', 
                         'gamma', 'gamma_max', tg+'_VCD(molec/cm^2)', 'err_'+tg+'_VCD',
                         'Retr_height(km)', 'surf_num_dens(molec/cm^3)', 'err_surf_num_dens',
                         'surf_vmr(ppmv)', 'err_surf_vmr', 'surf_cnc(ug/m^3)', 'err_surf_cnc']

# Plot tg VCD variation
# ======================
# Filter out entries with very high errors
all_profiles_df  = all_profiles_df[all_profiles_df['err_'+tg+'_VCD']<5e15]     

x = np.array((all_profiles_df['Date_Time']))
y = np.array((all_profiles_df[tg+'_VCD(molec/cm^2)']))
err = np.array((all_profiles_df['err_'+tg+'_VCD']))

fig = plt.figure(figsize=(70,2))
ax=fig.add_subplot(111)
ax.errorbar(x,y,yerr=err, fmt='c.', label= tg+' VCD')
ax.set_xlim(startdate, enddate)
ax.set_ylim(0, 3.5e16)
fig.savefig(path+location+test+'_'+tg+'_VCD_'+date+'.pdf', 
                    bbox_inches='tight')

# Plot tg surface vmr variation
# ==============================
all_profiles_df  = all_profiles_df[all_profiles_df['err_surf_vmr']<0.004]     
x = np.array((all_profiles_df['Date_Time']))
y1 = np.array((all_profiles_df['surf_vmr(ppmv)']))
err1 = np.array((all_profiles_df['err_surf_vmr']))

fig = plt.figure(figsize=(70,2))
ax=fig.add_subplot(111)
ax.errorbar(x,y1,yerr=err1, fmt='c.', label=tg+' VMR')
ax.set_xlim(startdate, enddate)
ax.set_ylim(0, 0.03)
ax.legend(loc='upper right', borderaxespad=1)
fig.savefig(path+location+test+'_'+tg+'_surfVMR_'+date+'.pdf', 
                    bbox_inches='tight')

#%%
# Now heatmap vertical profiles
df_list1 = []
for d in dates_list:
    date = str(d)
    year = (str(d))[:4]
    month = (str(d))[4:6]
    day = (str(d))[6:]
    
    ddmmyyyy = day+'/'+month+'/'+year
    
    prdf = pd.read_csv(path+location+date+'/general/all_'+tg+'_vmr_prof_'+date+'.dat',
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
all_vprof_df_t = pd.concat(df_list1, axis=0)
all_vprof_df_t = all_vprof_df_t[all_vprof_df_t > -1000] # remove values of -10000

all_vprof_df_t = all_vprof_df_t.set_index(all_vprof_df_t['date_time'])
all_vprof_df_t = all_vprof_df_t.iloc[:,1:21]

#%%
altgrid = np.arange(0.1, 4, 0.2)
altgridcolumns = []
for i in altgrid:
    altgridcolumns.append(str(i))
all_vprof_df_t.columns = altgridcolumns
all_vprof_df = all_vprof_df_t.transpose()
#%%
fig, ax = plt.subplots(figsize=(70,3))

xticks = all_vprof_df.columns
keptticks = xticks[::int(len(xticks)/15)]
xticks = ['' for a in xticks]
xticks[::int(len(xticks)/15)] = keptticks

yticks = all_vprof_df.index[::-1]
keptticks = yticks[::int(len(yticks)/6)]
yticks = ['' for a in yticks]
yticks[::int(len(yticks)/6)] = keptticks

sb.heatmap(all_vprof_df[::-1], cmap=cm.RdYlBu_r, ax=ax, vmin=0, vmax=0.03,
           xticklabels=xticks, yticklabels=yticks)

plt.yticks(rotation=0)
plt.xticks(rotation=40)
plt.ylim(0,15)

plt.savefig(path+location+test+'_'+tg+'_VMR_heatmap_'+date+'.pdf', 
                    bbox_inches='tight')