# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:46:48 2017

@author: rgryan
"""

import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

date = 20170713  # Format:  YYYYMMDD
plotTG = False  # True if trace gas, otherwise aerosol extinction assumed
whatisit = 'AerExt'   # What is being plotted (for save name)
#whatisit = 'NO2'
#whatisit = 'HCHO'

#root = 'C:\\Sciatran2\\AEROSOL_RETRIEVAL_v-1-5\\Campaign\\'
folder = '/Users/rgryan/Google Drive/Documents/PhD/Data/example_aerext_profiles/'

#root = '/Users/rgryan/Google Drive/Documents/PhD/Data/'
#folder = 'BM_aer_retr1_HCHO\\20170221\\profiles\\'

total_path = folder

retrieved_ = pd.DataFrame()
height_ = pd.DataFrame()
times = []

allFiles = glob.glob(total_path + "/*.dat")
for file in allFiles:
    name = file[-29:]
    year = name[10:14]
    month = name[14:16]
    day = name[16:18]
    hour = name[19:21]
    houri = float(hour)
    minute = name[21:23]
    minutei = float(minute)
    sec = name[23:25]
    seci = float(sec)

    date = day+'/'+month+'/'+year
    time = hour+':'+minute
    dec_time_ = float(houri+(minutei/60)+(seci/3600))              # This is now decimal time, appropriate for QDOAS
    dec_time = round(dec_time_, 5)     
    print('dectime is '+str(dec_time)+', norm time is '+time)
    f = pd.read_csv(file, header=0, delim_whitespace=True)
    #retrieved_['0'] = f['z']
    #retrieved['z'] = f['z']
    if plotTG == True:
        retrieved_[str(dec_time)] = f['retr_vmr']
    else:
        retrieved_[str(dec_time)] = f['retrieved']
    times.append(dec_time)
#retrieved_['z'] = f['z']
z = np.array(f['z'])

# PLOT SETTINGS
#==================
figsize = (15,4)
fontsize = 14
maxtime = 17
mintime = 9
maxheight = 4
minheight = 0.11 # No data below here so leave as 0.11 km

# THIS DOES THE PLOTTING
# ======================
plt.figure(figsize=figsize)
cs = plt.contourf(times, z, retrieved_, cmap=cm.RdYlBu_r)
cbar = plt.colorbar()
plt.xlim(mintime, maxtime)
plt.ylim(minheight, maxheight)

plt.ylabel('Height (km)', fontsize=fontsize)
plt.xlabel('Time (hour, AEST)', fontsize=fontsize)
if plotTG == True:
    cbar.ax.set_ylabel(whatisit+' VMR (ppb)', fontsize=fontsize)
else:
    cbar.ax.set_ylabel('Aerosol extinction (km$^-1$)', fontsize=fontsize)
plt.show()

#fig.savefig(root+folder+whatisit+'_plot.pdf', bbox_inches='tight')