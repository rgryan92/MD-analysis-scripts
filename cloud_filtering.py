# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:44:28 2017

@author: rgryan
"""

# This code takes a linefile of MAX-DOAS spectra and calculates a colour index
#  index (CI) for each spectrum
# The CI results are then appended to QDOAS results
# A threshold CI (CIth) can then be calculated
#%%
# Import section
# =========================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime
from scipy.optimize import curve_fit
# =========================================================================
root = '/Users/rgryan/Documents/PhD/Data/'

# Spectra linefile readin
# =========================================================================
filepath = root+'TIMTAM/TIMTAM_spectra_linefiles/'
file = 'BM_Ulinefiles_11-20Jul17'
extension = '.txt'

# Wavelength calibration readin
# =========================================================================
wlcalpath = root+'TIMTAM/TIMTAM_QDOAS/TIMTAM_ref_files/'
wlcalfile = 'BM_UVcal'
wlcalextension = '.txt'

# WHAT DO WE WANT TO DO HERE?
# =========================================================================
calculate_coeffs = False  # Calculate coefficients from polynomial fit
                                #   to data from sunny days
apply_CI_filter = True          # Apply CI filter to QDOAS data using 
                                #   supplied fit coefficients
    
# Use the coefficients calculated in the program, or
#  coeffiecients supplied seperately (if the latter,
#  need to define them in the code below)
use_calc_coeffs = False
use_supplied_coeffs = True

# ELEVATION ANGLE OFFSET
# =========================================================================
eos = 1.5

# Define the colour index ratio
# =========================================================================
CI_numer_wl = 330   # numerator wavelength value 
CI_denom_wl = 390   # denominator wavelength value  

# Which elev.angle to use for CI threshold determination?
# =========================================================================
EA_for_CIth = 30

# Within what margin of the CI threshold should cloudy data be
#   filtered out?      i.e. 0.05 = within 5%
# =========================================================================
margin = 0.04 

spectrafiletoopen = filepath+file+extension
wlcaltoopen = wlcalpath+wlcalfile+wlcalextension
    
# =========================================================================
# PLOT SETTINGS
# =========================================================================
# plotmethod_a: plot CI for each day and EA, one next to the other
#       in the same style as the SCD plots
# plotmethod_b: Plot the CI vs SZA or time, all data from a data set 
#       in one plot
plotmethod_a = True    
plotmethod_b = False
plot_sza = True
b_xaxis = 'DecTime_AEST' # If plotmethod_b, x-axis 'SZA' or 'DecTime_AEST'

# Dates to plot               
# =========================================================================
an_year = 2017
start_month = 3
end_month = 3
start_day = 1
end_day = 12
start_hour = 20
end_hour = 10

# Other plot settings
# =========================================================================
save_plot = True             # Save the plots generated?
fontsize = 14
figsize = (20, 3)          
legend_pos = (1.09,1)        #(1.12,1) is good for 15x3 plots 
                             #(1.42,1) is good for 4x3 plots (just 1 day of data)
x_label_format = dates.HourLocator(interval=24)

#%%
# QDOAS READ IN INSTRUCTIONS
# =========================================================================
# Input files
# =========================================================================
#QDfilepath = '/Users/rgryan/Documents/PhD/Data/TIMTAM/CI_test/'
QDfilepath = '/Users/rgryan/Documents/PhD/Data/TIMTAM/TIMTAM_QDOAS/'
#QDfile = 'BM_L_sr_1-12Mar_338-370'
#QDfile = 'BM_L_sr_1Mar-6Apr_338-370'
QDfile = 'UM_L_1-12Mar_338-370_1'
QDext = '.ASC'
fitwindow = '338-370'
num_calwindows = 20
inst = 'UM'                     #    The data from which institution is being viewed? 
                                #      UM = Uni. of Melb, UW = Wollongong Uni, NZ = NIWA New Zealand, 
                                #      BM = Bureau of Meteorology Broadmeadows
filetosave = 'Images/'+file

# Reference method
# =========================================================================
ref_each_scan = False
one_ref_only = True

# Fitting window used
# =========================================================================
window_338_370 = True       # UV NO2/O4 fitting window
window_324_359 = False        # HCHO/BrO fitting window
window_336_359 = False       # Second HCHO/BrO fitting window
window_450_520 = False       # Vis NO2/O4 fitting window
window_305_317 = False       # SO2 fitting window
window_350_389 = False        # Doreena's MUMBA fitting window
            
hfmt = dates.DateFormatter('%d/%m %H:%M')

# =========================================================================
# ==================== FILE OPENING INSTRUCTIONS ==========================
# =========================================================================

header = num_calwindows+1             # header of the QDOAS output file (mostly calib. data)
QDfiletoopen = QDfilepath+QDfile+QDext       # define the QDOAS file to open 
startdate = datetime.datetime(an_year, start_month, start_day, start_hour)  
enddate = datetime.datetime(an_year, end_month, end_day, end_hour)

# Defining which trace gases are valid in which fitting window;
# =========================================================================

if window_338_370:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO] = [True, True, True, True, 
                                                                     True, True, True, True, False, False, False]
elif window_324_359:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO] = [True, True, True, False, 
                                                                     True, True, True, True, False, False, False]
elif window_450_520:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO] = [True, True, True, True, 
                                                                     True, True, False, False, True, False, False]
elif window_305_317:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO] = [True, False, True, False, 
                                                                     True, True, True, True, False, True, False]
elif window_350_389:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO] = [True, True, True, False, 
                                                                     True, True, False, True, False, False, False]
 #%%                                                                    
def plot_tgCF_results(tg, ylimit):    
    plot = plt.figure()
    if tg=='CI':
        whattoplot1 = 'CI'
        whattoplot = whattoplot1
        plottitle = inst+' CI'
        ylabel = 'CI'
    else:
        whattoplot1 = 'SCD('+tg+')'
        whattoplot = fitwindow+'.SlCol('+tg+')'
        plottitle = inst+' '+tg+' dSCD '+fitwindow
        ylabel = 'dSCD (molec./cm^2)'
    ylim = ylimit
    f = a2_.plot(x='Date_Time', y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='y.', ylim=ylim, label='2deg')
    f.set_title(plottitle, fontsize=fontsize)
    f.set_xlabel('Date_Time', fontsize=fontsize)
    f.set_ylabel(ylabel, fontsize=fontsize)

    #a2.plot(x='Date_Time', y=whattoplot, ax=f, style='w.', label='2deg', ylim=ylim)
    a3_.plot(x='Date_Time', y=whattoplot, ax=f, style='b.', label='3deg', ylim=ylim)
    a5_.plot(x='Date_Time', y=whattoplot, ax=f, style='g.', label='5deg', ylim=ylim)
    a10_.plot(x='Date_Time', y=whattoplot, ax=f, style='c.', label='10deg', ylim=ylim)
    a20_.plot(x='Date_Time', y=whattoplot, ax=f, style='m.', label='20deg', ylim=ylim)
    a30_.plot(x='Date_Time', y=whattoplot, ax=f, style='r.', label='30deg', ylim=ylim)
    #a90.plot(x='DateTime', y=whattoplot, ax=f, style='k.', label='90deg', ylim=ylim)
        
    f.set_xlim(startdate, enddate)
    #f.xaxis.set_major_locator(x_label_format)
    f.legend(['2deg', '3deg', '5deg', '10deg', '20deg', '30deg'], 
             bbox_to_anchor=legend_pos)
    f.xaxis.set_major_locator(dates.HourLocator(interval=24))
    f.xaxis.set_major_formatter(hfmt)
        
    if save_plot:
        fig = f.get_figure()
        fig.savefig(filepath+inst+'_'+whattoplot1+str(start_day)+str(start_month)+
                str(an_year)+'_'+str(end_day)+str(end_month)+str(an_year)+'.pdf', 
                    bbox_inches='tight')
  #%%                  
# SMALL FUNCTIONS NEEDED IN THIS SCRIPT
# =========================================================================
# Need a function to convert the decimal time to h:m:s time
# =========================================================================
def dtime2hms(dtime):
    int_hours = int(dtime)
    dec_mins = ((dtime-int_hours)*60)
    int_mins = int(dec_mins)
    dec_secs = ((dec_mins-int_mins)*60)
    int_secs = int(dec_secs)
    hms = str(int_hours)+':'+str(int_mins)+':'+str(int_secs)
    return hms
# =========================================================================
def dec_time_to_AEST(time):
    if 16 < time < 24:
        time = (time-14)
    elif 0 < time < 15:
        time = (time+10)
    return time
# =========================================================================
def datetime_to_AEST(datetime):
    if 
# Polynomial functions (for fitting etc)
# =========================================================================
def poly3(x, a, b, c, d):
    return ((a*(x**3)) + (b*(x**2)) + (c*(x))
            + d)

def poly4(x, a, b, c, d, f):
    return ((a*(x**4)) + (b*(x**3)) + (c*(x**2))
            + (d*(x)) + f)

def poly5(x, a, b, c, d, f, g):
    return ((a*(x**5)) + (b*(x**4)) + (c*(x**3))
            + (d*(x**2)) + (f*x) + g)

def poly6(x, a, b, c, d, f, g, h):
    return ((a*(x**6)) + (b*(x**5)) + (c*(x**4))
            + (d*(x**3)) + (f*(x**2)) + g*x + h)

def cos_function(x, a, b, c, d):
    return a*(np.cos((b*x)+c)) + d

def gaussian(x,a,b,c,d):
    return a*(np.exp(((x-b)**2)/(2*(c**2))))+d
#%%
# FUNCTION TO CALCULATE COLOUR INDEX FROM 
def calculate_CI(spectrafiletoopen, wlcaltoopen):
    wlcalheader_list = [0, 0, 0, 0, 0]               # The data file has info at the start
    wlcalheader_df = pd.DataFrame(wlcalheader_list)  #   which we have to account for when
                                                     #   adding the wl cal file
    # ======================================================================    
    wlcalreadin_orig = pd.read_csv(wlcaltoopen, header=None)
    wlcalreadin = wlcalheader_df.append(wlcalreadin_orig)
    wlcalreadin = wlcalreadin.reset_index(drop=True)

    # Readin the data file and add the wavelength calibration data
    # =========================================================================    
    filereadin = pd.read_csv(spectrafiletoopen,  header=None, sep = ' ')
    dftouse = filereadin.transpose()
    dftouse['wl'] = wlcalreadin

    # need to find the index of the wl value closest to the selected 
    #    numerator & denominator wavelengths
    index_numer_list = []
    index_denom_list = []

    # For the ratio numerator:
    for index, row in dftouse.iterrows():
        if (CI_numer_wl-0.2)<(dftouse['wl'][index])<(CI_numer_wl+0.2):
            index_numer_list.append(index)
        elif (CI_denom_wl-0.2)<(dftouse['wl'][index])<(CI_denom_wl+0.2):
            index_denom_list.append(index)
        else:
            continue
        

    # Taking the min of the list ensures only one value is found 
    #   for the numerator and demoninator within the +/- 0.2 range
    index_numer = int(index_numer_list[0])
    index_denom = int(index_denom_list[0])

    # Now in order to use the indexing just created, convert the rows to columns 
    #    so that an average around the set numerator and demoninator can be taken
    # This hopefully reduces the impact of spectral noise
    # =========================================================================    
    dftouse_2 = dftouse.transpose() 
    numer_val = []         # A list for the numerator values to be averaged
    denom_val = []         #  " "     " "   denominator  " "     " "
    for index, row in dftouse_2.iterrows():
        numer_vals2avg = []
        numer_vals2avg.append((dftouse_2[index_numer-2][index])) # Average over values, 2 higher
        numer_vals2avg.append((dftouse_2[index_numer-1][index])) #   and 2 lower than the set
        numer_vals2avg.append((dftouse_2[index_numer][index]))   #   denominator or numerator
        numer_vals2avg.append((dftouse_2[index_numer+1][index]))
        numer_vals2avg.append((dftouse_2[index_numer+2][index]))
        numer_val_indexavg = np.mean(numer_vals2avg)
        numer_val.append(numer_val_indexavg)

        denom_vals2avg = []
        denom_vals2avg.append((dftouse_2[index_denom-2][index]))
        denom_vals2avg.append((dftouse_2[index_denom-1][index]))
        denom_vals2avg.append((dftouse_2[index_denom][index]))
        denom_vals2avg.append((dftouse_2[index_denom+1][index]))
        denom_vals2avg.append((dftouse_2[index_denom+2][index]))
        denom_val_indexavg = np.mean(denom_vals2avg)
        denom_val.append(denom_val_indexavg)

    numer_val_df = pd.DataFrame(numer_val)   # Put the averaged results in DFs so they go 
    denom_val_df = pd.DataFrame(denom_val)   #    nicely into the total DF

    dftouse_2['CI'] = (numer_val_df/denom_val_df) # This actually calculates the CI

    # Create a new data frame.. we want the SZA, elevation angle, date, time and CI
    CI_data = pd.DataFrame()
    CI_data['SZA'] = dftouse_2[0]
    CI_data['EA'] = dftouse_2[2]
    CI_data['Date'] = dftouse_2[3]
    CI_data['Date'] = CI_data.Date.astype(str)
    CI_data['DecTime'] = dftouse_2[4]
    CI_data['DecTime'] = CI_data.DecTime.astype(float)
    CI_data['CI'] = dftouse_2['CI']

    hms_list = []
    for index, row in CI_data.iterrows():
        hms_list.append(dtime2hms(CI_data['DecTime'][index]))
        hms_df = pd.DataFrame(hms_list)
    CI_data['hms'] = hms_df[0]

    CI_data['Date_Time'] = pd.to_datetime((CI_data['Date'] +' '+CI_data['hms']), 
                                   dayfirst=True)

    DecTimeAEST_list = []
    for index, row in CI_data.iterrows():
        DecTimeAEST_list.append(dec_time_to_AEST(CI_data['DecTime'][index]))
        DecTimeAEST_df = pd.DataFrame(DecTimeAEST_list)
    CI_data['DecTime_AEST'] = DecTimeAEST_df[0]
    #CI_data.set_index(['Date_Time'])
    #
    
    return CI_data
#%%
 
def create_QDOAS_df(QDfiletoopen, fitwindow):
    # FILE OPENING INSTRUCTIONS
    readin = pd.read_csv(QDfiletoopen,  header=header, sep = '\t', 
                            parse_dates=[['Date', 'Time']], dayfirst=True)
    
    QDOAS_data = readin.drop_duplicates(subset=['Date_Time'], keep=False)
    #QDOAS_data.set_index(['Date_Time'])
    #del QDOAS_data.index.name
    return QDOAS_data

# END OF FUNCTION
# ===========================================================

# Break the data up into elevation angle specific data frames
# ===========================================================
def create_EA_dfs(readin_df):
    if one_ref_only:
        a90 = readin_df[readin_df['Elev. viewing angle']>80]  # If one_ref_only, we'll have 90 deg
        b90 = readin_df[readin_df['Elev. viewing angle']<80]  #    SCD information 
 
        a30 = b90[b90['Elev. viewing angle']>26]
        b30 = b90[b90['Elev. viewing angle']<25]
    
    elif ref_each_scan:
        a30 = readin_df[readin_df['Elev. viewing angle']>25]  # If ref_each_scan, we won't have   
        b30 = readin_df[readin_df['Elev. viewing angle']<25]  #     any 90 deg SCDs    

    a20 = b30[b30['Elev. viewing angle']>15+eos]                  # Now create the rest of the EA
    b20 = b30[b30['Elev. viewing angle']<15+eos]                  #     specific data frames 

    a10 = b20[b20['Elev. viewing angle']>7.5+eos]
    b10 = b20[b20['Elev. viewing angle']<7.5+eos]

    a5 = b10[b10['Elev. viewing angle']>4.7+eos]
    b5 = b10[b10['Elev. viewing angle']<4.7+eos]

    a3 = b5[b5['Elev. viewing angle']>2.7+eos]
    b3 = b5[b5['Elev. viewing angle']<2.7+eos]

    a2 = b3[b3['Elev. viewing angle']>1.7+eos]
    b1 = b3[b3['Elev. viewing angle']<1.7+eos]
    a1 = b1[b1['Elev. viewing angle']>0.8+eos]
    
    if one_ref_only:
        EA_df_list = [a90, a30, a20, a10, a5, a3, a2, a1]
    elif ref_each_scan:
        EA_df_list = [a30, a20, a10, a5, a3, a2, a1]
        
    return(EA_df_list)
#%%
def calc_CI_threshold(EA_CF, QDOAS_data):    
    SZA_adj_emptylist = np.zeros(len(EA_CF))
    SZA_adj_emptydf = pd.DataFrame(SZA_adj_emptylist)
    EA_CF['SZA_adj'] = SZA_adj_emptydf[0]
    EA_CF['DateTime'] = SZA_adj_emptydf[0]

    # This loop section calculates the adjusted SZA
    # =============================================
    print('NOW CALCULATING ADJUSTED SZA')
    for index, row in EA_CF.iterrows():
        if index<(len(EA_CF)-1):
            if EA_CF['SZA'][index] > EA_CF['SZA'][index+1]:
                EA_CF['SZA_adj'][index] = ((EA_CF['SZA'][index]
                                       -EA_CF['SZA'].min())*(-1))
            else:
                EA_CF['SZA_adj'][index] = (EA_CF['SZA'][index]
                                       -EA_CF['SZA'].min())
        else:
            print('Finished calculating adjusted SZA')
    # =============================================
    # Calculate CIth = CI threshold, based on calculation from adj SZA
    # =============================================
    CIth_emptylist = np.zeros(len(EA_CF)) 
    CIth_emptydf = pd.DataFrame(CIth_emptylist)
    EA_CF['CIth'] = CIth_emptylist[0]
    EA_CF['Filter'] = CIth_emptylist[0]

    print('NOW CALCULATING CI THRESHOLD')
    for index, row in EA_CF.iterrows():
        EA_CF['CIth'][index] = poly6(EA_CF['SZA_adj'][index], 
                                c1, c2, c3, c4, c5, c6, c7)
    
    
    # Do the filtering - determine if values in EA_CF meet the 
    #   filtering criteria or not
    # ========================================================
    for index, row in EA_CF.iterrows():
        upper = EA_CF['CIth'][index] + (EA_CF['CIth'][index]*margin)
        lower = EA_CF['CIth'][index] - (EA_CF['CIth'][index]*margin)
        #if lower < EA_CF['CI'][index] < upper:
        if EA_CF['CI'][index] > lower:
            #EA_CF['DateTime'][index] = EA_CF['DateTime'][index]
            EA_CF['Filter'][index] = 1
        else:
            #EA_CF['DateTime'][index] = 'NaN'
            EA_CF['Filter'][index] = 0

    print('Finished filtering EA_CF')
    
    QDOAS_data_forCF = QDOAS_data.set_index('index')
    del QDOAS_data_forCF.index.name
    EA_CF_ = EA_CF.set_index('index')
    del EA_CF_.index.name

    # Append the filter column to all the QDOAS data
    QDOAS_data_forCF['Filter'] = EA_CF_['Filter']
    QDOAS_data_forCF = QDOAS_data_forCF.reset_index()
    
    print('NOW APPLYING FILTER TO ALL QDOAS DATA')
    for index, row in QDOAS_data_forCF.iterrows():
        if (((28)+eos) < QDOAS_data_forCF['Elev. viewing angle'][
                index] < (32+eos)):
            if QDOAS_data_forCF['Filter'][index] == 1:
                print('IN '+str(index)+' out of '+str(len(QDOAS_data)))
                QDOAS_data_forCF['nothing'][index+6] = 'in'
                QDOAS_data_forCF['nothing'][index+5] = 'in'
                QDOAS_data_forCF['nothing'][index+4] = 'in'
                QDOAS_data_forCF['nothing'][index+3] = 'in'
                QDOAS_data_forCF['nothing'][index+2] = 'in'
                QDOAS_data_forCF['nothing'][index+1] = 'in'
                QDOAS_data_forCF['nothing'][index] = 'in'
                #QDOAS_data_forCF['nothing'][index-1] = 'in'
                #QDOAS_data_forCF['nothing'][index-2] = 'in'
                #QDOAS_data_forCF['nothing'][index-3] = 'in'
            elif QDOAS_data_forCF['Filter'][index] == 0:
                print('OUT '+str(index)+' out of '+str(len(QDOAS_data)))
                QDOAS_data_forCF['nothing'][index+6] = 'out'
                QDOAS_data_forCF['nothing'][index+5] = 'out'
                QDOAS_data_forCF['nothing'][index+4] = 'out'
                QDOAS_data_forCF['nothing'][index+3] = 'out'
                QDOAS_data_forCF['nothing'][index+2] = 'out'
                QDOAS_data_forCF['nothing'][index+1] = 'out'
                QDOAS_data_forCF['nothing'][index] = 'out'
                #QDOAS_data_forCF['nothing'][index-1] = 'out'
                #QDOAS_data_forCF['nothing'][index-2] = 'out'
                #QDOAS_data_forCF['nothing'][index-3] = 'out'
        else:
            continue
    print('NOW FINISHED FILTERING ALL DATA IN RANGE')
    #QDOAS_data_forCF_cut = QDOAS_data_forCF[QDOAS_data_forCF.nothing != 'out']
    return QDOAS_data_forCF
#%%
def calculate_coefficients(EA_CF):
    SZA_adj_emptylist = np.zeros(len(EA_CF))
    SZA_adj_emptydf = pd.DataFrame(SZA_adj_emptylist)
    EA_CF['SZA_adj'] = SZA_adj_emptydf[0]
    EA_CF['DateTime'] = SZA_adj_emptydf[0]

    # This loop section calculates the adjusted SZA
    # =============================================
    print('NOW CALCULATING ADJUSTED SZA')
    for index, row in EA_CF.iterrows():
        if index<(len(EA_CF)-1):
            if EA_CF['SZA'][index] > EA_CF['SZA'][index+1]:
                EA_CF['SZA_adj'][index] = ((EA_CF['SZA'][index]
                                       -EA_CF['SZA'].min())*(-1))
            else:
                EA_CF['SZA_adj'][index] = (EA_CF['SZA'][index]
                                       -EA_CF['SZA'].min())
        else:
            print('Finished calculating adjusted SZA')
    
    idx = np.isfinite(EA_CF.SZA_adj) & np.isfinite(EA_CF.CI)
    x__ = EA_CF.SZA_adj[idx]
    y__ = EA_CF.CI[idx]
    x_ = x__[:(len(x__)-1)]
    y_ = y__[:(len(y__)-1)]
    x = x_.drop(x_.index[16])
    y = y_.drop(y_.index[16])
    popt, pcov = curve_fit(poly6, x, y,  
                    p0=(1e-8, 1e-7, -1e-4, 1e-4, 1, 1, 1))

    
    coefficients = [popt[0], popt[1], popt[2], popt[3], 
                     popt[4], popt[5], popt[6], x, y]
    return coefficients
#%%
# This is the code that actually runs things;
# =========================================================================

# APPLY THE READ IN FUNCTIONS
# =========================================================================
print('NOW READING IN SPECTRAL FILES, CALCULATING CI')
CI_data_ = calculate_CI(spectrafiletoopen, wlcaltoopen)
CI_data = CI_data_.set_index(['Date_Time'])
CI_data = CI_data[~CI_data.index.duplicated(keep='first')]

del CI_data.index.name

print('NOW READING IN QDOAS FILE')
QDOAS_data_ = create_QDOAS_df(QDfiletoopen, fitwindow) 
QDOAS_data = QDOAS_data_.set_index(['Date_Time'])
QDOAS_data = QDOAS_data[~QDOAS_data.index.duplicated(keep='first')]

del QDOAS_data.index.name

# APPEND THE CI INFO TO THE QDOAS DATA
# =========================================================================
QDOAS_data['CI'] = CI_data['CI']
QDOAS_data['DecTime_AEST'] = CI_data['DecTime_AEST']
QDOAS_data = QDOAS_data.reset_index()
QDOAS_data['Date_Time'] = QDOAS_data['index'] # Just to put a date_time
                                              #  col back in the DF

# BREAK UP THE QDOAS DATA INTO ELEV.ANGLE DATA FRAMES
# =========================================================================
print('NOW BREAKING INTO ELEV. ANGLE DATA FRAMES')
if one_ref_only:
    [a90, a30, a20, a10, a5, a3, a2, a1] = create_EA_dfs(QDOAS_data)
elif ref_each_scan:
    [a30, a20, a10, a5, a3, a2, a1] = create_EA_dfs(QDOAS_data)
else:
    print('need to define FRS ref method!')
#%%
# Coefficients calculated from 30 deg EA data
#  6th order polynomial fit to data
if inst == 'BM':
    c30_1 = 6.4262455846701831e-12
    c30_2 = -1.5725091451645166e-10
    c30_3 = -3.8172681509813839e-08
    c30_4 = -1.4370010189086872e-07
    c30_5 = -0.00016600177629422325
    c30_6 = -0.00061352687133673994
    c30_7 = 1.3824820958541586
elif inst == 'UW':
    c30_1 = 6.9759571928730592e-12
    c30_2 = 3.3935510545509575e-11
    c30_3 = -4.1005526856222875e-08
    c30_4 = -1.4370010189086872e-07
    c30_5 = -0.00018428749767470778
    c30_6 = -0.00087515983340219592
    c30_7 = 1.4638059462196218    
elif inst == 'UM':
    c30_1 = 4.0466276173115629e-12
    c30_2 = -1.5053933170602387e-10
    c30_3 = -2.0178039397441404e-08
    c30_4 = 7.6934637225530892e-07
    c30_5 = -0.00023815115752978815
    c30_6 = -0.0012002188810757469
    c30_7 =  1.420293829508035
elif inst == 'NZ':
    c30_1 = 4.8252225106568152e-12
    c30_2 = -6.0643171882867444e-11
    c30_3 = -4.154403641561035e-08
    c30_4 = -7.1739857221105086e-09
    c30_5 = -0.00015334443984359227
    c30_6 = -0.0015469637715157399
    c30_7 = 1.6127049415869148

# Determine which EAs data to use for threshold determination
# =========================================================================
if EA_for_CIth == 5:
    EA_CF = a5.reset_index()
elif EA_for_CIth == 2:
    EA_CF = a2.reset_index() 
elif EA_for_CIth == 3:
    EA_CF = a3.reset_index()
elif EA_for_CIth == 30:
    EA_CF = a30.reset_index()
elif EA_for_CIth == 10:
    EA_CF = a10.reset_index()
elif EA_for_CIth == 20:
    EA_CF = a20.reset_index()
else:
    print('need to define EA for CI threshold!')

if calculate_coeffs == True:
    print('BEGINNING CALCULATION OF COEFFICIENTS')
    coefficients = calculate_coefficients(EA_CF)
elif apply_CI_filter == True:
    if use_calc_coeffs == True:
        [c1, c2, c3, c4, c5, c6, c7] = [C[0],
                                       C[1], C[2], C[3],
                                       C[4], C[5], C[6]]
    else:
        [c1, c2, c3, c4, c5, c6, c7] = [c30_1, c30_2, c30_3, c30_4, 
                                     c30_5, c30_6, c30_7]
    print('STARTING CI THRESHOLD CALCULATIONS AND FILTERING')
    QDOAS_data_forCF = calc_CI_threshold(EA_CF, QDOAS_data)
    QDOAS_data_forCF_cut = QDOAS_data_forCF[QDOAS_data_forCF.nothing != 'out']
    QDOAS_data_forCF.to_csv(QDfilepath+'cloudfiltering/'+QDfile+'_nCF.txt', sep='\t')
    QDOAS_data_forCF_cut.to_csv(QDfilepath+'cloudfiltering/'+QDfile+'_CF.txt', sep='\t')
    if one_ref_only:
        [a90_CF, a30_CF, a20_CF, a10_CF, a5_CF, 
         a3_CF, a2_CF, a1_CF] = create_EA_dfs(QDOAS_data_forCF_cut)
    elif ref_each_scan:
        [a30_CF, a20_CF, a10_CF, a5_CF, a3_CF, a2_CF, 
         a1_CF] = create_EA_dfs(QDOAS_data_forCF_cut)
    else:
        print('need to define FRS ref method!')
else:
    print('hey, you did not define what you wanted to do!')
#%%