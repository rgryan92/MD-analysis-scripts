# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 09:14:20 2017

@author: rgryan
"""
import pandas as pd
import numpy as np

file = 'BM_17Feb17_324-359'
ext = '.ASC'
path = '/Users/rgryan/Google Drive/TIMTAM/TIMTAM_QDOAS_output/'
calwindows = 20

def dateAEST(datetime):
    year = datetime[:4]
    month = datetime[5:7]
    monthyear = month+'/'+year
    day = int(datetime[8:10])
    hour = int(datetime[11:13])
    if 16<hour<24:
        dayA = day+1
    else:
        dayA = day
    dateA = str(dayA)+'/'+monthyear
    return dateA
def timeAEST(datetime):
    hour = int(datetime[11:13])
    mins = datetime[14:16]
    secs = datetime[17:19]
    minssecs = mins+':'+secs
    if 16<hour<24:
        hourA = hour-14
    else:
        hourA = hour+10
    timeA = str(hourA)+':'+minssecs
    return timeA

def qd2heipro(file, calwindows):
    # Read in the data
    #=================
    readin = pd.read_csv(path+file+ext, sep='\t', header=calwindows+1, 
                         parse_dates=[['Date', 'Time']], dayfirst=True)
    
    # Deal with the excess 90deg EA scans
    #====================================
    readin = readin[readin['SZA']<88]  # Remove values before daily measurement sequence starts
    readin90s = readin[readin['Elev. viewing angle']>80] # Take out 90deg EA scans
    readin90s = readin90s[::3] # Take only every third 90deg measurement
    leftover = readin[readin['Elev. viewing angle']<80] # All other EAs
    dflist = [leftover, readin90s]          # Join the other EAs and the 90s back together
    backtogether = pd.concat(dflist, axis=0)#  using concat
    backtogether = backtogether.sort_values('Date_Time') # Sort the values by time to get them
                                                         #   in the right order again
    # Convert to date time AEST    
    backtogether['datetime'] = backtogether['Date_Time'].astype(str)
    backtogether['date_AEST'] = np.nan  # Create empty columns to fill later
    backtogether['time_AEST'] = np.nan
    
    backtogether['date_AEST'] = backtogether['datetime'].map(dateAEST)
    backtogether['time_AEST'] = backtogether['datetime'].map(timeAEST)
    
    return backtogether
    
f = qd2heipro(file, calwindows)
f.to_csv(path+file+'_FH.txt', sep='\t')
print('FINISHED!')