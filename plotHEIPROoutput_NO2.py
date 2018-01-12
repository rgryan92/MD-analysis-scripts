# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:30:01 2017

@author: rgryan

Script to look at HEIPRO output data from one timeperiod
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib import cm
import datetime


path = 'C:\\Sciatran2\\TRACEGAS_RETRIEVAL_v-1-4\\Campaign\\'
path2='BM_March2017_NO2retr_'
test = 't12'
location = path2+test+'\\'
date = '20170307'
time = '130400'

tg = 'NO2'
tg1 = 'NO2'
SCDpower = '17'

startdate = datetime.datetime(2017, 3, 7, 6)  
enddate = datetime.datetime(2017, 3, 7, 20)
 
#%%
# Averaging kernels
#==================
akfile = pd.read_csv(path+location+date+'/av_kernels/avk_'+date+'_'+time+'.dat',
                     delim_whitespace=True)

ak_formatrix = akfile.iloc[0:20,5:25]
ak_matrix = ak_formatrix.as_matrix()
dofs = np.trace(ak_matrix)
xlim=[-0.5,1.]
fontsize=16
figsize=(3.5,3.5)

akp = akfile.plot(x='AVK_0.1km', y='z', color='red', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_0.3km', y='z', ax=akp,  color='orangered', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_0.5km', y='z', ax=akp,  color='orange', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_0.7km', y='z', ax=akp,  color='yellow', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_0.9km', y='z', ax=akp,  color='greenyellow', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_1.1km', y='z', ax=akp,  color='limegreen', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_1.3km', y='z', ax=akp,  color='green', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_1.5km', y='z', ax=akp,  color='lightseagreen', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_1.7km', y='z', ax=akp,  color='aqua', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_1.9km', y='z', ax=akp,  color='mediumaquamarine', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_2.1km', y='z', ax=akp,  color='mediumturquoise', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_2.3km', y='z', ax=akp,  color='powderblue', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_2.5km', y='z', ax=akp,  color='skyblue', xlim=xlim,
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_2.7km', y='z', ax=akp,  color='mediumblue', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_2.9km', y='z', ax=akp,  color='royalblue', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_3.1km', y='z', ax=akp,  color='midnightblue', xlim=xlim,
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_3.3km', y='z', ax=akp,  color='darkviolet', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_3.5km', y='z', ax=akp,  color='darkmagenta', xlim=xlim, 
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_3.7km', y='z', ax=akp,  color='magenta',xlim=xlim,
                  figsize=figsize, fontsize=fontsize)
akfile.plot(x='AVK_3.9km', y='z', ax=akp,  color='pink',xlim=xlim,
                  figsize=figsize, fontsize=fontsize)
entries = ['tot','0.1', '0.3', '0.5', '0.7', '0.9', '1.1', '1.3', '1.5', '1.7', 
            '1.9', '2.1', '2.3', '2.5', '2.7', '2.9', '3.1', '3.3', 
            '3.5', '3.7', '3.9']
akp.legend(entries, fontsize=7, loc='center left', bbox_to_anchor=(1, 0.5))
akp.text(0.25, 3.2, 'DOFS = '+str(round(dofs,3)), size=15)
#akp.set_title('NO2_AVK_'+date+'_'+time, fontsize=fontsize)
akp.set_xlabel(tg+' Ave. Kernel', fontsize=fontsize)
akp.set_ylabel('Altitude (km)', fontsize=fontsize)  
fig = akp.get_figure()
fig.savefig(path+location+test+'_avk_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')
#%%

#Modelled and measured values
mmfile = pd.read_csv(path+location+date+'/measurements/'+tg1+'_meas__'+date+'_'+time+'.dat',
                     delim_whitespace=True, parse_dates=[['date', 'time']])
mmfile = mmfile[mmfile['elev']<80]

x = np.array((mmfile['elev']))
y = np.array((mmfile[tg+'meas']))
y1 = np.array((mmfile[tg+'retr']))
err = np.array((mmfile['err_'+tg+'meas']))

# Calculate RMS value for (O4meas - O4retr)
ss = [(((y[i]/1e17)-(y1[i])/1e17)**2) for i in np.arange(len(y))]
rms = np.sqrt(sum(ss)/len(ss))

fig = plt.figure(figsize=figsize)
ax=fig.add_subplot(111)
ax.errorbar(x,y,yerr=err, fmt='ro', label=tg+'measured')
ax.scatter(mmfile['elev'], mmfile[tg+'retr'], c='black', marker='o',
            label=tg+'retrieved')

# Set the axes ticks and labels
xticks = [-0.0001, 0, 10, 20, 30]
xlab = 'Elevation angle'
yticks = [0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]
ylab = tg+' SCD (x10$^{'+SCDpower+'}$)'

ax.set_xticklabels(xticks, fontsize=fontsize)
ax.set_yticklabels(yticks, fontsize=fontsize)
ax.set_xlabel(xlab, fontsize=fontsize)
ax.set_ylabel(ylab, fontsize=fontsize)

plt.text(9.5, 1.75e17, 'RMS = '+str(round(rms,4)), size=fontsize)
#ax.legend(loc='upper right', borderaxespad=1, fontsize=fontsize)
fig.savefig(path+location+test+'_meas_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')

#%%%
# Individual profiles and error values
profile = pd.read_csv(path+location+date+'/profiles/'+tg1+'_prof_'+date+'_'+time+'.dat',
                     delim_whitespace=True)
xlim=(0,0.015)
ylim=(0,4)
#figsize=(3,3)
prop = profile.plot(x='apriori(vmr)', y='z', style='k-', figsize=figsize,
                    xlim=xlim, ylim=ylim, fontsize=fontsize)
profile.plot(x='retr_vmr', y='z', xerr='err_r_vmr', figsize=figsize, 
             color='darkorange', xlim=xlim, ylim=ylim, ax=prop, fontsize=fontsize)
prop.legend(['a-priori', 'retrieved'], loc='upper right', fontsize=fontsize)

# Set the axes ticks and labels
xticks = [0, 5, 10, 15]
xlab = tg+' VMR (ppb)'
yticks = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
ylab = 'Altitude (km)'

prop.set_xticklabels(xticks, fontsize=fontsize)
prop.set_yticklabels(yticks, fontsize=fontsize)
prop.set_xlabel(xlab, fontsize=fontsize)
prop.set_ylabel(ylab, fontsize=fontsize)

fig = prop.get_figure()
fig.savefig(path+location+test+'_prof_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')

prep = profile.plot(x='err_s_vmr', y='z', style='m-', figsize=figsize,
                    xlim=xlim, ylim=ylim, fontsize=fontsize)
profile.plot(x='err_m_vmr', y='z', style='b-',figsize=figsize,
             xlim=xlim, ylim=ylim, ax=prep, fontsize=fontsize)

prep.set_xticklabels(xticks, fontsize=fontsize)
prep.set_yticklabels(yticks, fontsize=fontsize)
prep.set_xlabel(xlab, fontsize=fontsize)
prep.set_ylabel(ylab, fontsize=fontsize)

prep.legend(['Smooth.', 'Noise'], loc='upper right', fontsize=fontsize)
fig2 = prep.get_figure()
fig2.savefig(path+location+test+'_profErrors_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')

#%%

# Plot daily tg VCD variation
concfile = pd.read_csv(path+location+date+'/general/'+tg1+'_retrieval_'+date+'.dat',
                     delim_whitespace=True, parse_dates=[['Date', 'Time']])

x = np.array((concfile['Date_Time']))
y = np.array((concfile[tg+'_VCD(molec/cm^2)']))
err = np.array((concfile['err_'+tg+'_VCD']))
y1 = np.array((concfile['surf_vmr(ppmv)']))
err1 = np.array((concfile['err_surf_vmr']))

# plot the surface vmr on the same plot
fig = plt.figure(figsize=(4,3))
ax1=fig.add_subplot(111)
ax1.errorbar(x,y,yerr=err, fmt='k.', label= tg+' VCD')
#ax1.set_xlim(startdate, enddate)
ax1.set_ylim(0,3e16)
ax1.grid(which='major', axis='y')
ax2 = ax1.twinx()
ax2.errorbar(x,y1,yerr=err1, fmt='m.', label=tg+' VMR')
#ax2.set_xlim(startdate, enddate)
ax2.set_ylim(0, 0.015)
ax2.grid(b=None)

fig.savefig(path+location+test+'_'+tg+'_dailyConc_'+date+'.png', 
                   bbox_inches='tight')

#%%

# Plot daily extinction vertical profile
allprof = pd.read_csv(path+location+date+'/general/all_'+tg1+'_vmr_prof_'+date+'.dat',
                     delim_whitespace=True)
allprof = allprof.set_index('altitude')

xticks = ['06:36','06:48','07:00','07:12','07:24','07:36','07:48',
         '08:00','08:12','08:24','08:36','08:48','09:00','09:12',
         '09:24','09:36','09:48','10:00','10:12','10:24','10:36',
         '10:48','11:00','11:12','11:24','11:36','11:48','12:00',
         '12:12','12:24','12:36','12:48','13:00','13:12','13:24',
         '13:36','13:48','14:00','14:12','14:24','14:36','14:48',
         '15:00','15:12','15:24','15:36','15:48','16:00','16:12',
         '16:24','16:36','16:48','17:00','17:12','17:24','17:36',
         '17:48','18:00','18:12','18:24']

keptticks = xticks[::int(len(xticks)/10)]
xticks = ['' for x in xticks]
xticks[::int(len(xticks)/10)] = keptticks


allprof1 = allprof[allprof > -10] # remove values of -10000

fig, ax = plt.subplots(figsize=(5,3))
sb.heatmap(allprof1[::-1], cmap=cm.RdYlBu_r, ax=ax, xticklabels=xticks,
           yticklabels=4)
plt.xticks(rotation=90)
plt.savefig(path+location+test+'_daily'+tg+'_vmr_Profile_'+date+'.png', 
                    bbox_inches='tight')
#%%
