# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 11:03:25 2017

@author: rgryan
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib import cm

path = 'C:\\Sciatran2\\AEROSOL_RETRIEVAL_v-1-5\\Campaign\\'
path2 = 'BM_aer_retr_March2017_'

test = 't33'
location = path2+test+'\\'
date = '20170307'
time = '130000'

 
#%%
# Averaging kernels
#==================
akfile = pd.read_csv(path+location+date+'/av_kernels/avk_ext_'+date+'_'+time+'.dat',
                     delim_whitespace=True)

ak_formatrix = akfile.iloc[0:20,5:25]
ak_matrix = ak_formatrix.as_matrix()
dofs = np.trace(ak_matrix)
xlim=[-0.1,1.]
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
akp.set_xlabel('Aer. Ext. AK', fontsize=fontsize)
akp.set_ylabel('Altitude (km)', fontsize=fontsize)  
fig = akp.get_figure()
fig.savefig(path+location+test+'_avk_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')
#%%

#Modelled and measured values
mmfile = pd.read_csv(path+location+date+'/measurements/meas__'+date+'_'+time+'.dat',
                     delim_whitespace=True, parse_dates=[['date', 'time']])
mmfile = mmfile[mmfile['elev']<80]

x = np.array((mmfile['elev']))
y = np.array((mmfile['O4meas']))
y1 = np.array((mmfile['O4retr']))
err = np.array((mmfile['err_O4meas']))

# Calculate RMS value for (O4meas - O4retr)
ss = [(((y[i])-(y1[i]))**2) for i in np.arange(len(y))]
rms = np.sqrt(sum(ss)/len(ss))

fig = plt.figure(figsize=figsize)
ax=fig.add_subplot(111)
ax.errorbar(x,y,yerr=err, fmt='ro', label='measured')
ax.scatter(mmfile['elev'], mmfile['O4retr'], c='black', marker='o',
            label='O4retrieved')

# Set the axes ticks and labels
xticks = [-0.0001, 0, 10, 20, 30]
xlab = 'Elevation angle'
yticks = [0, 0.006, 0.008, 0.010, 0.012]
ylab = 'O4 opt. depth'

ax.set_xticklabels(xticks, fontsize=fontsize)
ax.set_yticklabels(yticks, fontsize=fontsize)
ax.set_xlabel(xlab, fontsize=fontsize)
ax.set_ylabel(ylab, fontsize=fontsize)

plt.text(0, 0.006, 'RMS = '+str(round(rms,6)), size=fontsize)
#ax.legend(loc='upper right', borderaxespad=1, fontsize=fontsize)
fig.savefig(path+location+test+'_meas_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')

#%%%
# Individual profiles and error values
profile = pd.read_csv(path+location+date+'/profiles/prof361nm_'+date+'_'+time+'.dat',
                     delim_whitespace=True)
xlim=(0,0.15)
ylim=(0,4)
#figsize=(3,3)
prop = profile.plot(x='apriori', y='z', style='k-', figsize=figsize,
                    xlim=xlim, ylim=ylim, fontsize=fontsize)
profile.plot(x='retrieved', y='z', xerr='err_retrieved', figsize=figsize, 
             color='darkorange', xlim=xlim, ylim=ylim, ax=prop, fontsize=fontsize)
prop.legend(['a-priori', 'retrieved'], loc='upper right', fontsize=fontsize)

# Set the axes ticks and labels
xticks = [0, 0.05, 0.10, 0.15]
xlab = 'Aer. ext. (km$^{-1}$)'
yticks = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
ylab = 'Altitude (km)'

prop.set_xticklabels(xticks, fontsize=fontsize)
prop.set_yticklabels(yticks, fontsize=fontsize)
prop.set_xlabel(xlab, fontsize=fontsize)
prop.set_ylabel(ylab, fontsize=fontsize)

fig = prop.get_figure()
fig.savefig(path+location+test+'_prof_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')

prep = profile.plot(x='err_smooth', y='z', style='m-', figsize=figsize,
                    xlim=xlim, ylim=ylim, fontsize=fontsize)
profile.plot(x='err_noise', y='z', style='b-',figsize=figsize,
             xlim=xlim, ylim=ylim, ax=prep, fontsize=fontsize)

prep.set_xticklabels(xticks, fontsize=fontsize)
prep.set_yticklabels(yticks, fontsize=fontsize)
prep.set_xlabel(xlab, fontsize=fontsize)
prep.set_ylabel(ylab, fontsize=fontsize)

prep.legend(['Smooth.', 'Noise'], loc='upper right', fontsize=fontsize)
fig2 = prep.get_figure()
fig2.savefig(path+location+test+'_profErrors_'+date+'_'+time+'.pdf', 
                    bbox_inches='tight')