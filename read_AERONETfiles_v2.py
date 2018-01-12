# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:55:16 2017

@author: rgryan
"""
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

aeronetpath = '/Users/rgryan/Google Drive/Documents/PhD/Data/aeronet/'

startdate = datetime.date(2003, 1, 1)
enddate = datetime.date(2018,1, 1)

plot_aod = False
plot_ang = False
plot_asy = False
plot_ssa = True

files = ['030101_171231_Canberra',
             '060101_091231_Adelaide_Site_7', '100101_151231_Brisbane-Uni_of_QLD',
             '980101_121231_Tinga_Tingana', '130101_171231_Fowlers_Gap']
             
colors = ['blue',  'red', 'orange', 'magenta', 'green']

if plot_aod:
    ext = '.lev20'
    col = 'AOT_440'
    ylabel = 'AOD @440 nm'
    header=4
elif plot_ang:
    ext = '.lev20'
    col = '340-440Angstrom'
    ylabel = 'Angstrom exp. 340-440 nm'
    header=4
elif plot_asy:
    ext = '.asyday'
    col = 'ASYM440-T'
    ylabel = 'Asym. param @439 nm'
    header=3
elif plot_ssa:
    ext = '.ssa'
    col = 'SSA440-T'
    ylabel = 'S.S. Albedo @440 nm'
    header=3
#%%
dflist = []    
def make_aeronet_df(ext,file,col,header):
    myfile = aeronetpath+file+ext
    if os.path.isfile(myfile) == True:
        adf = pd.read_csv(aeronetpath+file+ext, sep=',', header=header,
                     parse_dates=[['Date(dd-mm-yyyy)','Time(hh:mm:ss)']], dayfirst=True)
        adf = adf.set_index(pd.DatetimeIndex(adf['Date(dd-mm-yyyy)_Time(hh:mm:ss)']))
        adfm = adf.resample('M').mean()
    else:
        print('no data at '+myfile)
        adfm = pd.DataFrame()
    return adfm
    
for file in files:
    adfm = make_aeronet_df(ext, file, col, header)
    dflist.append(adfm)
#%%
aeronetplot = dflist[0][col].plot(figsize=(10,2), color=colors[0])
if len(dflist[1]>0):
    dflist[1][col].plot(figsize=(10,2), color=colors[1], ax=aeronetplot)
else:
    print('no data')
if len(dflist[2]>0):
    dflist[2][col].plot(figsize=(10,2), color=colors[2], ax=aeronetplot)
else:
    print('no data')
if len(dflist[3]>0):
    dflist[3][col].plot(figsize=(10,2), color=colors[3], ax=aeronetplot)
else:
    print('no data')
if len(dflist[4]>0):
    dflist[4][col].plot(figsize=(10,2), color=colors[4], ax=aeronetplot)
else:
    print('no data')
aeronetplot.set_xlabel('Year')
aeronetplot.set_ylabel(ylabel)
aeronetplot.set_xlim(startdate, enddate)
aeronetplot.legend(['Canberra','Adelaide', 'Brisbane', 'Tingana', 
                'Fowlers Gap'], loc=2, bbox_to_anchor=(1,1))
aeronetplot.set_title('All S.E. Australian Aeronet sites')             
f = aeronetplot.get_figure()
f.savefig(aeronetpath+col+'_monthlyavgs_SE_Australia.png', bbox_inches='tight')
plt.close("all")
#%%
# df for stats

df4stats = pd.DataFrame()

df4stats['Canberra'] = dflist[0][col]
df4stats['Adelaide'] = dflist[1][col]
df4stats['Brisbane'] = dflist[2][col]
df4stats['Tinga'] = dflist[3][col]
df4stats['Fowlers Gap'] = dflist[4][col]
df4stats['mean'] = df4stats.mean(axis=1)
df4stats['std'] = df4stats.std(axis=1)

std_mean = df4stats['std'].mean()
mean_mean = df4stats['mean'].mean()

aeronetstatsplot = df4stats['mean'].plot(yerr=std_mean, figsize=(10,2))
aeronetstatsplot.set_ylabel(ylabel)
aeronetstatsplot.set_xlabel('Year')
aeronetstatsplot.set_xlim(startdate, enddate)
aeronetstatsplot.set_title('Average over S.E. Aust Aeronet sites')

startdate1 = datetime.datetime(2002, 1, 1)
d = pd.date_range(startdate1, periods=20, freq='Y')
aeronetstatsplot.fill_between(d, mean_mean+std_mean, mean_mean-std_mean, color='orange',
                              alpha=0.4)
g = aeronetstatsplot.get_figure()
g.savefig(aeronetpath+col+'_Allmonthlyavgs_SE_Australia.png', bbox_inches='tight')
#%%