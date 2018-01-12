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
filepath = 'C:\\Users\\rgryan\\Google Drive\\Documents\\PhD\\Data\\Broady_QDOAS_output\\'

inst = 'BM'                         #    The data from which institution is being viewed? 
                                    #      UM = Uni. of Melb, UW = Wollongong Uni, NZ = NIWA New Zealand, 
                                    #      BM = Bureau of Meteorology Broadmeadows
file = 'BM_March17_UV'
fitwindow = '324.5-359'
num_calwindows = 20

filetosave = 'Images/'+file
ext = '.ASC'

# Dates to plot               
# =========================================================================
an_year = 2017
start_month = 3
end_month = 3
start_day = 3
end_day = 4
start_hour = 20
end_hour = 9

# Reference method
# =========================================================================
ref_each_scan = True
one_ref_only = False
EAoffset = 0    #Elevation angle offset(degrees)

show_error = True      # Show error bars on dSCD plots?   
calculate_VCDs = False  # If not, column renaming is overridden to just use
                        #   column names straight from file
                        
remove90s = True     # Needed if wanting to plot error bars in qdoas files
                     #   generated using sequential referencing
# Fitting window used
# =========================================================================
window_338_370 = False       # UV NO2/O4 fitting window
window_324_359 = True        # HCHO/BrO fitting window
window_336_359 = False       # Second HCHO/BrO fitting window
window_450_520 = False       # Vis NO2/O4 fitting window
window_305_317 = False       # SO2 fitting window
window_350_389 = False        # Doreena's MUMBA fitting window

# Plot settings
# =========================================================================
save_plot = True             # Save the plots generated?
plot_Rfn = False              # Plot the formaldehyde/NO2 ratio?
plot_VCDs = False            # True if plot the VCDs, false if plot SCDs
fontsize = 10
figsize = (4, 3)          
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

header = num_calwindows+1             # header of the QDOAS output file (mostly calib. data)
filetoopen = filepath+file+ext       # define the QDOAS file to open 
startdate = datetime.datetime(an_year, start_month, start_day, start_hour)  
enddate = datetime.datetime(an_year, end_month, end_day, end_hour)

# Defining which trace gases are valid in which fitting window;
# =========================================================================

if window_338_370:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO, HONO] = [True, True, True, True, 
                                                                     True, True, True, True, False, False, False, False]
elif window_324_359:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO, HONO] = [True, True, True, False, 
                                                                     True, True, True, True, False, False, False, True]
elif window_450_520:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO, HONO] = [True, True, True, True, 
                                                                     True, True, False, False, True, False, False, False]
elif window_305_317:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO, HONO] = [True, False, True, False, 
                                                                     True, True, True, True, False, True, False, False]
elif window_350_389:
    [Ring, O4, NO2t, NO2s, O3t, O3s, HCHO, BrO, H2O, SO2, CHOCHO, HONO] = [True, True, True, False, 
                                                                     True, True, False, True, False, False, False, False]


def create_readin_df(filetoopen, fitwindow):
    # FILE OPENING INSTRUCTIONS
    readin_start = pd.read_csv(filetoopen,  header=header, sep = '\t', 
                            parse_dates=[['Date', 'Time']], dayfirst=True)
    
    VCD_O4 = []        # DEFINE ARRAYS TO PUT SPECIFIC 
    VCD_O4e = []       #    TRACE GAS INTO INTO
    VCD_NO2t = []
    VCD_NO2te = []
    VCD_NO2s = []
    VCD_NO2se = []
    VCD_O3s = []
    VCD_O3se = []
    VCD_O3t = []
    VCD_O3te = []
    VCD_BrO = []
    VCD_BrOe = []
    VCD_HCHO = []
    VCD_HCHOe = []
    VCD_H2O = []
    VCD_H2Oe = []
    VCD_CHOCHO = []
    VCD_CHOCHOe = []
    VCD_SO2 = []
    VCD_SO2e = []
    tot_O3 = []
    tot_O3e = []
    zeros = np.zeros(2048)

    if calculate_VCDs == True:
    
        # CALCULATING GEOM. APPROXIMATION VERTICAL COLUMN DENSITIES (VCDs)
        # ================================================================
        if O4:
            for index, row in readin_start.iterrows():
                VCD_O4.append(((readin_start[fitwindow+'.SlCol(O4)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_O4e.append(((readin_start[fitwindow+'.SlErr(O4)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_O4_df = pd.DataFrame(VCD_O4)
            VCD_O4_dft = VCD_O4_df.transpose()
            VCD_O4e_df = pd.DataFrame(VCD_O4e)
            VCD_O4e_dft = VCD_O4e_df.transpose()
        else:
            VCD_O4_df = pd.DataFrame(zeros)
            VCD_O4_dft = VCD_O4_df.transpose()
            VCD_O4e_df = pd.DataFrame(zeros)
            VCD_O4e_dft = VCD_O4e_df.transpose()
    
        if NO2t:
            for index, row in readin_start.iterrows():
                VCD_NO2t.append(((readin_start[fitwindow+'.SlCol(NO2t)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_NO2te.append(((readin_start[fitwindow+'.SlErr(NO2t)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_NO2t_df = pd.DataFrame(VCD_NO2t)
            VCD_NO2t_dft = VCD_NO2t_df.transpose()
            VCD_NO2te_df = pd.DataFrame(VCD_NO2te)
            VCD_NO2te_dft = VCD_NO2te_df.transpose()
        else:
            VCD_NO2t_df = pd.DataFrame(zeros)
            VCD_NO2t_dft = VCD_NO2t_df.transpose()
            VCD_NO2te_df = pd.DataFrame(zeros)
            VCD_NO2te_dft = VCD_NO2te_df.transpose()
    
        if NO2s:
            for index, row in readin_start.iterrows():
                VCD_NO2s.append(((readin_start[fitwindow+'.SlCol(NO2t)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_NO2se.append(((readin_start[fitwindow+'.SlErr(NO2t)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_NO2s_df = pd.DataFrame(VCD_NO2s)
            VCD_NO2s_dft = VCD_NO2s_df.transpose()
            VCD_NO2se_df = pd.DataFrame(VCD_NO2se)
            VCD_NO2se_dft = VCD_NO2se_df.transpose()
        else:
            VCD_NO2s_df = pd.DataFrame(zeros)
            VCD_NO2s_dft = VCD_NO2s_df.transpose()
            VCD_NO2se_df = pd.DataFrame(zeros)
            VCD_NO2se_dft = VCD_NO2se_df.transpose()
        if O3s:
            for index, row in readin_start.iterrows():
                VCD_O3s.append(((readin_start[fitwindow+'.SlCol(O3s)'][index])
                               )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_O3se.append(((readin_start[fitwindow+'.SlErr(O3s)'][index])
                                )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_O3s_df = pd.DataFrame(VCD_O3s)
            VCD_O3s_dft = VCD_O3s_df.transpose()
            VCD_O3se_df = pd.DataFrame(VCD_O3se)
            VCD_O3se_dft = VCD_O3se_df.transpose()
        else:
            VCD_O3s_df = pd.DataFrame(zeros)
            VCD_O3s_dft = VCD_O3s_df.transpose()
            VCD_O3se_df = pd.DataFrame(zeros)
            VCD_O3se_dft = VCD_O3se_df.transpose()
        if O3t:
            for index, row in readin_start.iterrows():
                VCD_O3t.append(((readin_start[fitwindow+'.SlCol(O3t)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_O3te.append(((readin_start[fitwindow+'.SlErr(O3t)'][index]))/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_O3t_df = pd.DataFrame(VCD_O3t)
            VCD_O3t_dft = VCD_O3t_df.transpose()
            VCD_O3te_df = pd.DataFrame(VCD_O3te)
            VCD_O3te_dft = VCD_O3te_df.transpose()
        else:
            VCD_O3t_df = pd.DataFrame(zeros)
            VCD_O3t_dft = VCD_O3t_df.transpose()
            VCD_O3te_df = pd.DataFrame(zeros)
            VCD_O3te_dft = VCD_O3te_df.transpose()
    
        if BrO:
            for index, row in readin_start.iterrows():
                VCD_BrO.append(((readin_start[fitwindow+'.SlCol(BrO)'][index])
                               )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_BrOe.append(((readin_start[fitwindow+'.SlErr(BrO)'][index])
                                )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_BrO_df = pd.DataFrame(VCD_BrO)
            VCD_BrO_dft = VCD_BrO_df.transpose()
            VCD_BrOe_df = pd.DataFrame(VCD_BrOe)
            VCD_BrOe_dft = VCD_BrOe_df.transpose()
        else:
            VCD_BrO_df = pd.DataFrame(zeros)
            VCD_BrO_dft = VCD_BrO_df.transpose()
            VCD_BrOe_df = pd.DataFrame(zeros)
            VCD_BrOe_dft = VCD_BrOe_df.transpose()
    
        if HCHO:
            for index, row in readin_start.iterrows():
                VCD_HCHO.append(((readin_start[fitwindow+'.SlCol(HCHO)'][index])
                                )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_HCHOe.append(((readin_start[fitwindow+'.SlErr(HCHO)'][index])
                                 )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_HCHO_df = pd.DataFrame(VCD_HCHO)
            VCD_HCHO_dft = VCD_HCHO_df.transpose()
            VCD_HCHOe_df = pd.DataFrame(VCD_HCHOe)
            VCD_HCHOe_dft = VCD_HCHOe_df.transpose()
        else:
            VCD_HCHO_df = pd.DataFrame(zeros)
            VCD_HCHO_dft = VCD_HCHO_df.transpose()
            VCD_HCHOe_df = pd.DataFrame(zeros)
            VCD_HCHOe_dft = VCD_HCHOe_df.transpose()
    
        if CHOCHO:
            for index, row in readin_start.iterrows():
                VCD_CHOCHO.append(((readin_start[fitwindow+'.SlCol(CHOCHO)'][index])
                                  )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_CHOCHOe.append(((readin_start[fitwindow+'.SlErr(CHOCHO)'][index])
                                   )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_CHOCHO_df = pd.DataFrame(VCD_CHOCHO)
            VCD_CHOCHO_dft = VCD_CHOCHO_df.transpose()
            VCD_CHOCHOe_df = pd.DataFrame(VCD_CHOCHOe)
            VCD_CHOCHOe_dft = VCD_CHOCHOe_df.transpose()
        else:
            VCD_CHOCHO_df = pd.DataFrame(zeros)
            VCD_CHOCHO_dft = VCD_HCHO_df.transpose()
            VCD_CHOCHOe_df = pd.DataFrame(zeros)
            VCD_CHOCHOe_dft = VCD_CHOCHOe_df.transpose()
    
        if H2O:
            for index, row in readin_start.iterrows():
                VCD_H2O.append(((readin_start[fitwindow+'.SlCol(H2O)'][index])
                               )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_H2Oe.append(((readin_start[fitwindow+'.SlErr(H2O)'][index])
                                )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_H2O_df = pd.DataFrame(VCD_H2O)
            VCD_H2O_dft = VCD_H2O_df.transpose()
            VCD_H2Oe_df = pd.DataFrame(VCD_H2Oe)
            VCD_H2Oe_dft = VCD_H2Oe_df.transpose()
        else:
            VCD_H2O_df = pd.DataFrame(zeros)
            VCD_H2O_dft = VCD_H2O_df.transpose()
            VCD_H2Oe_df = pd.DataFrame(zeros)
            VCD_H2Oe_dft = VCD_H2Oe_df.transpose()
    
        if SO2:
            for index, row in readin_start.iterrows():
                VCD_SO2.append(((readin_start[fitwindow+'.SlCol(SO2)'][index])
                               )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
                VCD_SO2e.append(((readin_start[fitwindow+'.SlErr(SO2)'][index])
                                )/((1/np.sin(np.radians(readin_start['Elev. viewing angle'][index])))-1))
            VCD_SO2_df = pd.DataFrame(VCD_SO2)
            VCD_SO2_dft = VCD_SO2_df.transpose()
            VCD_SO2e_df = pd.DataFrame(VCD_SO2e)
            VCD_SO2e_dft = VCD_SO2e_df.transpose()
        else:
            VCD_SO2_df = pd.DataFrame(zeros)
            VCD_SO2_dft = VCD_SO2_df.transpose()
            VCD_SO2e_df = pd.DataFrame(zeros)
            VCD_SO2e_dft = VCD_SO2e_df.transpose()
    
    
        # Calculate total ozone by adding the O3s and O3t SCDs
        # ====================================================
        if O3s and O3t:
            for index, row in readin_start.iterrows():
                tot_O3.append(((readin_start[fitwindow+'.SlCol(O3s)'][index])
                              )+((readin_start[fitwindow+'.SlCol(O3s)'][index])))
#            tot_O3e.append()
            tot_O3_df = pd.DataFrame(tot_O3)
            tot_O3_dft = tot_O3_df.transpose()
#        tot_O3e_df = pd.DataFrame(tot_O3e)
#        tot_O3e_dft = tot_O3e_df.transpose()
        
        readin_t = readin_start.transpose()           # take original data frame
        readin_t1 = readin_t.append(VCD_O4_dft)       #  then append all the
        readin_t2 = readin_t1.append(VCD_O4e_dft)     #  VCD data to it 
        readin_t3 = readin_t2.append(VCD_NO2t_dft)
        readin_t4 = readin_t3.append(VCD_NO2te_dft)
        readin_t5 = readin_t4.append(VCD_O3s_dft)
        readin_t6 = readin_t5.append(VCD_O3se_dft)
        readin_t7 = readin_t6.append(VCD_O3t_dft)
        readin_t8 = readin_t7.append(VCD_O3te_dft)
        readin_t9 = readin_t8.append(VCD_BrO_dft)
        readin_t10 = readin_t9.append(VCD_BrOe_dft)
        readin_t11 = readin_t10.append(VCD_HCHO_dft)
        readin_t12 = readin_t11.append(VCD_HCHOe_dft)
        readin_t13 = readin_t12.append(VCD_H2O_dft)
        readin_t14 = readin_t13.append(VCD_H2Oe_dft)
        readin_t15 = readin_t14.append(VCD_NO2s_dft)
        readin_t16 = readin_t15.append(VCD_NO2se_dft)
        readin_t17 = readin_t16.append(VCD_CHOCHO_dft)
        readin_t18 = readin_t17.append(VCD_CHOCHOe_dft)
        readin_t19 = readin_t18.append(VCD_SO2_dft)
        readin_t20 = readin_t19.append(VCD_SO2e_dft)
        readin = readin_t20.transpose()               # This is the final data frame

        # NOW DEFINE THE COLUMN NAMES - THIS IS IMPORTANT FOR THE CORRECT PLOTTING
        # ========================================================================
        if window_338_370:
            readin.columns = ['Date_Time', 'SZA', 'Solar Azimuth Angle', 'Elev. viewing angle', fitwindow+'.Chi', fitwindow+'.SlCol(RMS)',
                 fitwindow+'.RefZm', fitwindow+'.SlCol(O4)', fitwindow+'.SlErr(O4)', fitwindow+'.SlCol(NO2t)', fitwindow+'.SlErr(NO2t)',
                  fitwindow+'.SlCol(Ring)', fitwindow+'.SlErr(Ring)', fitwindow+'.SlCol(BrO)', fitwindow+'.SlErr(BrO)',
                 fitwindow+'.SlCol(O3t)', fitwindow+'.SlErr(O3t)', fitwindow+'.SlCol(O3s)', fitwindow+'.SlErr(O3s)', 
                  fitwindow+'.SlCol(HCHO)', fitwindow+'.SlErr(HCHO)', fitwindow+'.SlCol(NO2s)', fitwindow+'.SlErr(NO2s)', 
                      'nothing', fitwindow+'.VCol(O4)', fitwindow+'.VErr(O4)', 
                  fitwindow+'.VCol(NO2t)', fitwindow+'.VErr(NO2t)', fitwindow+'.VCol(O3s)', fitwindow+'.VErr(O3s)', 
                  fitwindow+'.VCol(O3t)', fitwindow+'.VErr(O3t)', fitwindow+'.VCol(BrO)', fitwindow+'.VErr(BrO)', 
                  fitwindow+'.VCol(HCHO)', fitwindow+'.VErr(HCHO)', fitwindow+'.VCol(H2O)', fitwindow+'.VErr(H2O)',
                 fitwindow+'.VCol(NO2s)', fitwindow+'.VErr(NO2s)', fitwindow+'.VCol(CHOCHO)', fitwindow+'.VErr(CHOCHO)',
                     fitwindow+'.VCol(SO2)', fitwindow+'.VErr(SO2)']
        elif window_324_359:
            readin.columns = ['Date_Time', 'SZA', 'Solar Azimuth Angle', 'Elev. viewing angle', fitwindow+'.Chi', fitwindow+'.SlCol(RMS)',
                 fitwindow+'.RefZm', fitwindow+'.SlCol(O4)', fitwindow+'.SlErr(O4)', fitwindow+'.shift', fitwindow+'.shiftErr',
                          fitwindow+'.str', fitwindow+'.strErr', fitwindow+'.shift', fitwindow+'.shiftErr',
                          fitwindow+'.str', fitwindow+'.strErr',fitwindow+'.SlCol(NO2t)', fitwindow+'.SlErr(NO2t)',
                  fitwindow+'.SlCol(Ring)', fitwindow+'.SlErr(Ring)', fitwindow+'.SlCol(BrO)', fitwindow+'.SlErr(BrO)',
                 fitwindow+'.SlCol(O3t)', fitwindow+'.SlErr(O3t)', fitwindow+'.SlCol(O3s)', fitwindow+'.SlErr(O3s)', 
                  fitwindow+'.SlCol(HCHO)', fitwindow+'.SlErr(HCHO)', fitwindow+'.Specshift1', fitwindow+'.SpecshiftErr1',
                          fitwindow+'.Specstr1', fitwindow+'.SpecstrErr1', 'nothing', fitwindow+'.VCol(O4)', fitwindow+'.VErr(O4)', 
                  fitwindow+'.VCol(NO2t)', fitwindow+'.VErr(NO2t)', fitwindow+'.VCol(O3s)', fitwindow+'.VErr(O3s)', 
                  fitwindow+'.VCol(O3t)', fitwindow+'.VErr(O3t)', fitwindow+'.VCol(BrO)', fitwindow+'.VErr(BrO)', 
                  fitwindow+'.VCol(HCHO)', fitwindow+'.VErr(HCHO)', fitwindow+'.VCol(H2O)', fitwindow+'.VErr(H2O)',
                 fitwindow+'.VCol(NO2s)', fitwindow+'.VErr(NO2s)', fitwindow+'.VCol(CHOCHO)', fitwindow+'.VErr(CHOCHO)',
                     fitwindow+'.VCol(SO2)', fitwindow+'.VErr(SO2)']    
        elif window_450_520:
            readin.columns = ['Date_Time', 'SZA', 'Solar Azimuth Angle', 'Elev. viewing angle', fitwindow+'.Chi', fitwindow+'.SlCol(RMS)',
                 fitwindow+'.RefZm', fitwindow+'.SlCol(O4)', fitwindow+'.SlErr(O4)', fitwindow+'.SlCol(NO2t)', fitwindow+'.SlErr(NO2t)',
                 fitwindow+'.SlCol(Ring)', fitwindow+'.SlErr(Ring)', fitwindow+'.SlCol(O3t)', fitwindow+'.SlErr(O3t)',
                  fitwindow+'.SlCol(O3s)', fitwindow+'.SlErr(O3s)', fitwindow+'.SlCol(H2O)', fitwindow+'.SlErr(H2O)', fitwindow+'.SlCol(NO2s)', fitwindow+'.SlErr(NO2s)',  
                  'nothing', fitwindow+'.VCol(O4)', fitwindow+'.VErr(O4)', 
                  fitwindow+'.VCol(NO2t)', fitwindow+'.VErr(NO2t)', fitwindow+'.VCol(O3s)', fitwindow+'.VErr(O3s)', 
                  fitwindow+'.VCol(O3t)', fitwindow+'.VErr(O3t)', fitwindow+'.VCol(BrO)', fitwindow+'.VErr(BrO)', 
                  fitwindow+'.VCol(HCHO)', fitwindow+'.VErr(HCHO)', fitwindow+'.VCol(H2O)', fitwindow+'.VErr(H2O)',
                 fitwindow+'.VCol(NO2s)', fitwindow+'.VErr(NO2s)', fitwindow+'.VCol(CHOCHO)', fitwindow+'.VErr(CHOCHO)',
                     fitwindow+'.VCol(SO2)', fitwindow+'.VErr(SO2)'] 
    
        elif window_305_317:
            readin.columns = ['Date_Time', 'SZA', 'Solar Azimuth Angle', 'Elev. viewing angle', fitwindow+'.Chi', fitwindow+'.SlCol(RMS)',
                 fitwindow+'.RefZm', fitwindow+'.SlCol(NO2t)', fitwindow+'.SlErr(NO2t)', fitwindow+'.SlCol(Ring)', 
                      fitwindow+'.SlErr(Ring)', fitwindow+'.SlCol(BrO)', fitwindow+'.SlErr(BrO)',
                  fitwindow+'.SlCol(O3t)', fitwindow+'.SlErr(O3t)', fitwindow+'.SlCol(O3s)', fitwindow+'.SlErr(O3s)', 
                      fitwindow+'.SlCol(HCHO)', fitwindow+'.SlErr(HCHO)', fitwindow+'.SlCol(SO2)', fitwindow+'.SlErr(SO2)',
                      'nothing', fitwindow+'.VCol(O4)', fitwindow+'.VErr(O4)', 
                  fitwindow+'.VCol(NO2t)', fitwindow+'.VErr(NO2t)', fitwindow+'.VCol(O3s)', fitwindow+'.VErr(O3s)', 
                  fitwindow+'.VCol(O3t)', fitwindow+'.VErr(O3t)', fitwindow+'.VCol(BrO)', fitwindow+'.VErr(BrO)', 
                  fitwindow+'.VCol(HCHO)', fitwindow+'.VErr(HCHO)', fitwindow+'.VCol(H2O)', fitwindow+'.VErr(H2O)',
                 fitwindow+'.VCol(NO2s)', fitwindow+'.VErr(NO2s)', fitwindow+'.VCol(CHOCHO)', fitwindow+'.VErr(CHOCHO)',
                     fitwindow+'.VCol(SO2)', fitwindow+'.VErr(SO2)']
        elif window_350_389:
            readin.columns = ['Date_Time', 'SZA', 'Solar Azimuth Angle', 'Elev. viewing angle', fitwindow+'.Chi', fitwindow+'.SlCol(RMS)',
                 fitwindow+'.RefZm', fitwindow+'.SlCol(O4)', fitwindow+'.SlErr(O4)', fitwindow+'.SlCol(Ring)', 
                      fitwindow+'.SlErr(Ring)', fitwindow+'.SlCol(O3t)', fitwindow+'.SlErr(O3t)',
                  fitwindow+'.SlCol(NO2t)', fitwindow+'.SlErr(NO2t)', fitwindow+'.SlCol(BrO)', fitwindow+'.SlErr(BrO)', 
                      fitwindow+'.SlCol(O3s)', fitwindow+'.SlErr(O3s)', 
                      'nothing', fitwindow+'.VCol(O4)', fitwindow+'.VErr(O4)', 
                  fitwindow+'.VCol(NO2t)', fitwindow+'.VErr(NO2t)', fitwindow+'.VCol(O3s)', fitwindow+'.VErr(O3s)', 
                  fitwindow+'.VCol(O3t)', fitwindow+'.VErr(O3t)', fitwindow+'.VCol(BrO)', fitwindow+'.VErr(BrO)', 
                  fitwindow+'.VCol(HCHO)', fitwindow+'.VErr(HCHO)', fitwindow+'.VCol(H2O)', fitwindow+'.VErr(H2O)',
                 fitwindow+'.VCol(NO2s)', fitwindow+'.VErr(NO2s)', fitwindow+'.VCol(CHOCHO)', fitwindow+'.VErr(CHOCHO)',
                     fitwindow+'.VCol(SO2)', fitwindow+'.VErr(SO2)']
    
        else:
            print("Oi, you forgot to define the fitting window, idiot!")
    else:
        readin = readin_start
    #readin = readin.drop_duplicates(subset=['Date_Time'], keep=False)

    #readin = readin.set_index('Date_Time')
    return readin

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
        b90 = readin_df[readin_df['Elev. viewing angle']<80]
        a30 = b90[b90['Elev. viewing angle']>25]  # If ref_each_scan, we won't have   
        b30 = b90[b90['Elev. viewing angle']<25]  #     any 90 deg SCDs    

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
    
    if one_ref_only:
        EA_df_list = [a90, a30, a20, a10, a5, a3, a2, a1]
    elif ref_each_scan:
        EA_df_list = [a30, a20, a10, a5, a3, a2, a1]
        
    return(EA_df_list)
#%%    
def plot_tg_results(tg, ylimit):    
#    plot = plt.figure()
    if plot_VCDs:
        whattoplot1 = 'VCD('+tg+')'
        whattoplot = fitwindow+'.VCol('+tg+')'
        error = fitwindow+'.VErr('+tg+')'
        plottitle = inst+' '+tg+' VCD '+fitwindow+' nm'
        ylabel = 'VCD (molec./cm^2)'
        ylim = ylimit
        f = a2.plot(x='Date_Time', y=whattoplot, yerr=error, fontsize=fontsize, figsize=figsize, 
                     style='r.', ylim=ylim, label='20deg')
        f.set_title(plottitle, fontsize=fontsize)
        f.set_xlabel('Date_Time', fontsize=fontsize)
        f.set_ylabel(ylabel, fontsize=fontsize)
        f.set_xlim(startdate, enddate)
        #f.xaxis.set_major_locator(x_label_format)
        f.legend(['20deg VCD'], bbox_to_anchor=legend_pos)
        f.xaxis.set_major_locator(dates.HourLocator(interval=6))
        f.xaxis.set_major_formatter(hfmt)
        
    else:
        if tg == 'RMS':
            whattoplot = fitwindow+'.RMS'
            whattoplot1 = 'RMS'
            yerror = 0
        elif tg == 'shift_tg':
            whattoplot = fitwindow+'.Shift(O4)'
            whattoplot1 = 'Shift'
            yerror = fitwindow+'.Err Shift(O4)'
        elif tg == 'shift_spec':
            whattoplot = fitwindow+'.Shift(Spectrum)'
            whattoplot1 = 'Shift'
            yerror = fitwindow+'.Err Shift(Spectrum)'
        else:
            whattoplot1 = 'SCD('+tg+')'
            whattoplot = fitwindow+'.SlCol('+tg+')'
            yerror = fitwindow+'.SlErr('+tg+')'
        plottitle = inst+' '+tg+' dSCD '+fitwindow
        ylabel = 'dSCD (molec./cm^2)'
        ylim = ylimit
        if show_error == True:        
            f = a1.plot(x='Date_Time', y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='y.', ylim=ylim, yerr=yerror, label='20deg')
        
            a3.plot(x='Date_Time', y=whattoplot, yerr=yerror, ax=f, style='b.', 
                    label='3deg', ylim=ylim)
            a5.plot(x='Date_Time', y=whattoplot, yerr=yerror, ax=f, style='g.', 
                    label='5deg', ylim=ylim)
            a10.plot(x='Date_Time', y=whattoplot, yerr=yerror, ax=f, style='c.', 
                     label='10deg', ylim=ylim)
            a20.plot(x='Date_Time', y=whattoplot, yerr=yerror, ax=f, style='m.', 
                     label='20deg', ylim=ylim)
            a30.plot(x='Date_Time', y=whattoplot, yerr=yerror, ax=f, style='r.', 
                     label='30deg', ylim=ylim)
            #a90.plot(x='Date_Time', y=whattoplot, yerr=yerror, ax=f, style='k.', 
             #        label='90deg', ylim=ylim)
        else:
            f = a1.plot(x='Date_Time', y=whattoplot, fontsize=fontsize, figsize=figsize, 
                    style='y.', ylim=ylim, label='20deg')
        
            a3.plot(x='Date_Time', y=whattoplot, ax=f, style='b.', 
                    label='3deg', ylim=ylim)
            a5.plot(x='Date_Time', y=whattoplot, ax=f, style='g.', 
                    label='5deg', ylim=ylim)
            a10.plot(x='Date_Time', y=whattoplot, ax=f, style='c.', 
                     label='10deg', ylim=ylim)
            a20.plot(x='Date_Time', y=whattoplot, ax=f, style='m.', 
                     label='20deg', ylim=ylim)
            a30.plot(x='Date_Time', y=whattoplot, ax=f, style='r.', 
                     label='30deg', ylim=ylim)
            #a90.plot(x='Date_Time', y=whattoplot, ax=f, style='k.', 
               #      label='90deg', ylim=ylim)
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

if remove90s:
    readin = readin[readin['Elev. viewing angle']<80]
else:
    readin=readin

readin = readin[readin[fitwindow+'.RMS'] < 1e2] # remove the problem ones where
                                                # an error causes a value of 
                                                # ~9e+36
# Run the second function on the result
# =================================================
#EA_df_list = create_EA_dfs(readin)

if one_ref_only:
    [a90, a30, a20, a10, a5, a3, a2, a1] = create_EA_dfs(readin)
elif ref_each_scan:
    [a30, a20, a10, a5, a3, a2, a1] = create_EA_dfs(readin)
 
#plot_tg_results('NO2t', [-2e16,2.5e17])
#plot_tg_results('O4', [-2e42,6e43])
plot_tg_results('HCHO', [-2e16,4e17])
#plot_tg_results('O3t', [-3e19,6e19])
plot_tg_results('RMS', [0.0002,0.001])
#plot_tg_results('O3s', [-8e19,6e19])
#plot_tg_results(('Ring'), [-0.05, 2e-2])
#plot_tg_results('shift_tg', [-0.4, 0.4])
#plot_tg_results('shift_spec', [-0.008, -0.001])
plot_tg_results('hono', [-2e15,6e15])
#plot_tg_results('CHOCHO', [-3e15,7e15])