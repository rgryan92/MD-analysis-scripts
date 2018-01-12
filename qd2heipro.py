# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 09:14:20 2017

@author: rgryan
"""
import pandas as pd
import numpy as np

file = 'UW_March17_UV'
ext = '.ASC'
path = 'C:\\Users\\rgryan\\Google Drive\\Documents\\PhD\\Data\\Broady_QDOAS_output\\'
calwindows = 25

def dateAEST(datetime):
    year = int(datetime[:4])
    month = int(datetime[5:7])
    day = int(datetime[8:10])
    hour = int(datetime[11:13])
    if 16<hour<24:
        dayA = day+1
    else:
        dayA = day
    if month == 2:
        if dayA>28:
            dayA_ = 1
            monthA_ = 3
            yearA_ = year
        else:
            dayA_ = dayA
            monthA_ = month
            yearA_ = year
    elif month == 4 or 6 or 9 or 11:
        if day>30:
            dayA_ = 1
            monthA_ = month+1
            yearA_ = year
        else:
            dayA_ = dayA
            monthA_ = month
            yearA_ = year
    elif month == 1 or 3 or 5 or 7 or 8 or 10:
        if dayA > 31:
            dayA_ = 1
            monthA_ = month+1
            yearA_ = year
        else:
            dayA_ = dayA
            monthA_ = month
            yearA_ = year
    elif month == 12:
        if dayA>31:
            dayA = 1
            monthA_ = 1
            yearA_ = year+1
        else:
            dayA_ = dayA
            monthA_ = month
            yearA_ = year
    if dayA_<10 and monthA_<10:
        dateA = '0'+str(dayA_)+'/0'+str(monthA_)+'/'+str(yearA_)
    elif dayA_<10 and monthA_>10:
        dateA = '0'+str(dayA_)+'/'+str(monthA_)+'/'+str(yearA_)
    elif dayA_>10 and monthA_<10:
        dateA = str(dayA_)+'/0'+str(monthA_)+'/'+str(yearA_)
    else:
        dateA = str(dayA_)+'/'+str(monthA_)+'/'+str(yearA_)
    
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
    if hourA<10:
        timeA = '0'+str(hourA)+':'+minssecs
    else:
        timeA = str(hourA)+':'+minssecs
    return timeA

def qd2heipro(file, calwindows):
    # Read in the data
    #=================
    readin = pd.read_csv(path+file+ext, sep='\t', header=calwindows+1, 
                         parse_dates=[['Date', 'Time']], dayfirst=True)
    readin = readin.sort_values('Date_Time')
    readin = readin.drop_duplicates(subset='Date_Time')  
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
f.to_csv(path+file+'_FH1.txt', sep='\t')
print('FINISHED!')