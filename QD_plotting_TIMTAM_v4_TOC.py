# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 14:26:46 2017

@author: rgryan
"""

# Import section
# =========================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime


# =========================================================================
# ============== SECTION OF THINGS TO CHECK AND CHANGE ====================
# =========================================================================

# Input files
# =========================================================================
filepath = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\TIMTAM_QD_TOC\\'

inst = 'BM'                         #    The data from which institution is being viewed? 
                                    #      UM = Uni. of Melb, UW = Wollongong Uni, NZ = NIWA New Zealand, 
                                    #      BM = Bureau of Meteorology Broadmeadows
file = inst+'_TIMTAM_TOCfitting_450-550_v2'
fitwindow = '450-550'
num_calwindows = 20

filetosave = 'Images/'+file
ext = '.ASC'

# Dates to plot               
# =========================================================================
an_year = 2017
start_month = 2
end_month = 2
start_day = 16
end_day = 22
start_hour = 20
end_hour = 9

# Reference method
# =========================================================================
EAoffset = 0    #Elevation angle offset(degrees)

show_error = False      # Show error bars on dSCD plots?   

# Plot settings
# =========================================================================
save_plot = True             # Save the plots generated?
plot_Rfn = False              # Plot the formaldehyde/NO2 ratio?
plot_VCDs = False            # True if plot the VCDs, false if plot SCDs
fontsize = 10
figsize = (10, 3)          
legend_pos = (1.42,1)        #(1.12,1) is good for 15x3 plots 
                             #(1.42,1) is good for 4x3 plots (just 1 day of data)
hourinterval = 3             # x-axis label time interval (hours)
x_label_format = dates.MonthLocator()   # x-axis Label style 
                                       # for multiple day plots, DateLocator() works
                                       # for single day plots, it doesn't (!!), so use
                                       #     YearLocator()
            
hfmt = dates.DateFormatter('%d/%m %H:%M')

# =========================================================================
# ==================== FILE OPENING INSTRUCTIONS ==========================
# =========================================================================

header = num_calwindows+1            # header of the QDOAS output file (mostly calib. data)
filetoopen = filepath+file+ext       # define the QDOAS file to open 
startdate = datetime.datetime(an_year, start_month, start_day, start_hour)  
enddate = datetime.datetime(an_year, end_month, end_day, end_hour)

def create_readin_df(filetoopen, fitwindow):
    # FILE OPENING INSTRUCTIONS
    readin = pd.read_csv(filetoopen,  header=header, sep = '\t', 
                            parse_dates=[['Date', 'Time']], dayfirst=True)
    
    #readin = readin.drop_duplicates(subset=['Date_Time'], keep=False)

    #readin = readin.set_index('Date_Time')
    return readin

# END OF FUNCTION
# ===========================================================

# Break the data up into elevation angle specific data frames
# ===========================================================
def create_EA_dfs(readin_df):
    a90 = readin_df[readin_df['Elev. viewing angle']>80]  # If one_ref_only, we'll have 90 deg
    b90 = readin_df[readin_df['Elev. viewing angle']<80]  #    SCD information 
 
    a30 = b90[b90['Elev. viewing angle']>26]
    b30 = b90[b90['Elev. viewing angle']<25]

    a20 = b30[b30['Elev. viewing angle']>15]                  # Now create the rest of the EA
    b20 = b30[b30['Elev. viewing angle']<15]                  #     specific data frames 

    a10 = b20[b20['Elev. viewing angle']>(7.5+EAoffset)]
    b10 = b20[b20['Elev. viewing angle']<(7.5+EAoffset)]

    a5 = b10[b10['Elev. viewing angle']>(4.7+EAoffset)]
    b5 = b10[b10['Elev. viewing angle']<(4.7+EAoffset)]

    a3 = b5[b5['Elev. viewing angle']>(2.7+EAoffset)]
    b3 = b5[b5['Elev. viewing angle']<(2.7+EAoffset)]

    a2 = b3[b3['Elev. viewing angle']>(1.7+EAoffset)]
    b1 = b3[b3['Elev. viewing angle']<(1.7+EAoffset)]
    a1 = b1[b1['Elev. viewing angle']>(0.8+EAoffset)]
    
    EA_df_list = [a90, a30, a20, a10, a5, a3, a2, a1]
        
    return(EA_df_list)
#%%    
def plot_tg_results(tg, ylimit):    
#    plot = plt.figure()        
    if tg == 'RMS':
        whattoplot = fitwindow+'_'+inst+'.RMS'
        whattoplot1 = 'RMS'
        yerror = 0
    elif tg == 'shift_tg':
        whattoplot = fitwindow+'_'+inst+'.Shift(O4)'
        whattoplot1 = 'Shift'
        yerror = fitwindow+'_'+inst+'.Err Shift(O4)'
    elif tg == 'shift_spec':
        whattoplot = fitwindow+'_'+inst+'.Shift(Spectrum)'
        whattoplot1 = 'Shift'
        yerror = fitwindow+'_'+inst+'.Err Shift(Spectrum)'
    else:
        whattoplot1 = 'SCD('+tg+')'
        whattoplot = fitwindow+'_'+inst+'.SlCol('+tg+')'
        yerror = fitwindow+'_'+inst+'.SlErr('+tg+')'
    plottitle = inst+' '+tg+' dSCD '+fitwindow
    ylabel = 'dSCD (molec./cm^2)'
    ylim = ylimit
    if show_error == True:        
        f = a90.plot(x='Date_Time', y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='b.', ylim=ylim, yerr=yerror, label='90deg')
    else:
        f = a90.plot(x='Date_Time', y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='b.', ylim=ylim, label='90deg')
    f.set_title(plottitle, fontsize=fontsize)
    f.set_xlabel('Date_Time', fontsize=fontsize)
    f.set_ylabel(ylabel, fontsize=fontsize)   
    f.set_xlim(startdate, enddate)
    #f.xaxis.set_major_locator(x_label_format)
    f.legend(['2deg', '3deg', '5deg', '10deg', '20deg', '30deg'], 
                 bbox_to_anchor=legend_pos)
    f.xaxis.set_major_locator(dates.HourLocator(interval=hourinterval))
    f.xaxis.set_major_formatter(hfmt)
        
    if save_plot:
        fig = f.get_figure()
        fig.savefig(filepath+filetosave+whattoplot1+str(start_day)+str(start_month)+
                str(an_year)+'_'+str(end_day)+str(end_month)+str(an_year)+'_'+
                fitwindow+'.pdf', 
                    bbox_inches='tight')
#%%                    
                    
                    
# Run the first function on the data frame read in
# =================================================
readin = create_readin_df(filetoopen, fitwindow) 

readin = readin[readin[fitwindow+'_'+inst+'.RMS'] < 1e2] # remove the problem ones where
                                                # an error causes a value of 
                                                # ~9e+36
# Run the second function on the result
# =================================================
[a90, a30, a20, a10, a5, a3, a2, a1] = create_EA_dfs(readin)

 
plot_tg_results('NO2s', [-2e16,2.5e17])
#plot_tg_results('HCHO', [-2e16,4e17])
#plot_tg_results('O3t', [-3e19,6e19])
plot_tg_results('RMS', [0.0002,0.001])
plot_tg_results('O3s', [-1e19,1e20])
#plot_tg_results(('Ring'), [-0.05, 2e-2])
#plot_tg_results('shift_tg', [-0.4, 0.4])
#plot_tg_results('shift_spec', [-0.008, -0.001])
#plot_tg_results('hono', [-2e15,6e15])
#plot_tg_results('CHOCHO', [-3e15,7e15])

#%%
# SECTION  TO PREPARE OZONE SLANT COLUMNS FOR USE IN O3 LOOK UP TABLE PROGRAM
# format: Day number, SZA, O3 SCD
                            
def get_day_AEST(DateTime):
    day = int(DateTime[8:10])
    hour = int(DateTime[11:13])
    if 16 < hour < 24:
        dayA = day+1
    else:
        dayA = day
    return dayA

# Only want the 90deg EA values
readin4LUT = readin[readin['Elev. viewing angle'] > 80]
readin4LUT['DateTime'] = readin4LUT['Date_Time'].astype(str)
readin4LUT['day'] = readin4LUT['DateTime'].map(lambda x: get_day_AEST(x))
forlut = pd.DataFrame()
forlut['day'] = readin4LUT['day']
#forlut = forlut[forlut['day'] == 17]

forlut['sza'] = readin4LUT['SZA']
forlut = forlut[forlut['sza'] > 30]  # needed in program
forlut = forlut[forlut['sza'] < 92]  # needed in program

forlut['O3_scd'] = readin4LUT[fitwindow+'_'+inst+'.SlCol(O3s)']
forlut.to_csv(filepath+file+'_forLUT.dat', sep=' ', header=False, index=False)
