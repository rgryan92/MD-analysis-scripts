# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:44:55 2017

@author: rgryan

#=====================================================================================================================
# This code takes a folder, with subfolders containing .std spectra (outputted from DOASIS), and converts them all
#     to line-format files. Each line in the file is one spectrum.
#     The line formatting is appropriate for reading in by QDOAS.
# This code has been updated so it handle calibration and direct sun spectra
# It has now been updated SO THAT IT CORRECTLY SUBTRACTS THE OFFSET AND DARK CURRENT SPECTRA.
#=====================================================================================================================
# Updated 03-10-2017,
# For the Broady MAX-DOAS intercomparison campaign
# RGRyan
#=====================================================================================================================

# data save in the following format:
#    st_ddmmyyyy_Uxxxxxxx
#    where st = spectrum type (sc = scattered light, ds = direct sun, dc = dark current cal, oc = offset cal)
#    ddmmyyyy = date
#    U (or V) indicates UV (or Visible) spectrum
#    xxxxxxx is the 7 digit folder number from DOASIS
#       (this is needed for the iteration thru folders, rather than strictly needed for naming purposes)

#=====================================================================================================================

# What needs to be varied?
#     1. the folderpath and folderdate, specific to the main folder you're looking in
#     2. The foldernumber (this needs to be the number of the first subfolder you want the program to go to)
#     3. The lastfolder number (this tells the program when to stop looking and converting)
#     4. The folder letter. Once all the "U"s are converted, then you have to change this in order to convert all
#             the "V"s
#     5. Whether you want to do the offset and dark current correction
"""
# Section of things to check or change
#=====================================================================================================================

folderpath = 'C:/Users/rgryan/Google Drive/Documents/PhD/Data/Broady_data_backup/UWollongong/SP2017a/SP1703/'

foldernumber = 0              # The initial subfolder number, where the program will start
lastfolder =   100              # The final subfolder number, after which the program will stop converting
folders0indexed = True            # folder numbers starting with zero?
folderletter = 'U'                 # 'U' for UV spectra, 'V' for visible spectra

correct_dc = True                   # 'False' turns off the dark current correction 
correct_os = True                   # 'False' turns off the offset correction

only_save_hs_int = True             # True if wanting to save an abridged version of the horizon scan data, with only 
                                    #      intensity values, not all the spectral data
                                    
calcCI = True                       # Calculate colour index?
CIn = 330                           # Numerator for color index
CId = 390                           # denominator for color index

saveSC = True                      # save scattered light spectra?
saveDS = False                      # save direct sun spectra?
saveHS = True                      # save horizon scan spectra?
saveDC = True                      # save dark current calibrations?
saveOS = True                      # save offset calibrations?    
saveCI = True                       # save colour index results?
    
inst = 'UW'                         # The data from which institution is being plotted? <just for saving purposes!>
                                    #      UM = Uni. of Melb, UW = Wollongong Uni, NZ = NIWA New Zealand, 
                                    #      BM = Bureau of Meteorology Broadmeadows

# Date format
date_format_1 = True                # For date format in UniMelb MS-DOAS STD spectra, MM/DD/YYYY
date_format_2 = False                 # For date format in UW'gong MS-DOAS STD spectra, DD-Mon-YYYY
        
# settings for saving        
end = ".txt"
path2save = folderpath[3:]+folderletter+'\\'

# Import section
#=====================================================================================================================
import numpy as np
import glob
import pandas as pd

# Section to deal with dark and offset calibration spectra
#=====================================================================================================================
if inst == 'UM':
    UVoc__ = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UM_calfiles\\UM_UV_offset.std'
    visoc__ = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UM_calfiles\\UM_vis_offset.std'
    UVdc__= 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UM_calfiles\\UM_UV_darkcurrent.std'
    visdc__ = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UM_calfiles\\UM_vis_darkcurrent.std'
    Uwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UM_calfiles\\UM_UVcal.txt'
    Vwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UM_calfiles\\UM_viscal.txt'
elif inst == 'BM':
    UVoc__ = 'E:/PhD/Broady_data_backup/TIMTAM_ref_files/BM_calfiles/ofsuv_U0000003.std'
    visoc__ = 'E:/PhD/Broady_data_backup/TIMTAM_ref_files/BM_calfiles/ofsvis_V0000003.std'
    visdc__ = 'E:/PhD/Broady_data_backup/TIMTAM_ref_files/BM_calfiles/dcvis_V0000005.std'
    UVdc__ = 'E:/PhD/Broady_data_backup/TIMTAM_ref_files/BM_calfiles/dcuv_U0000005.std'
    Uwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\BM_calfiles\\BM_UVcal.txt'
    Vwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\BM_calfiles\\BM_viscal.txt'

elif inst == 'UW': 
    UVoc__ = 'E:/PhD/Broady_data_backup/UWollongong/Cals/offset_U_UW.std'
    visoc__ = 'E:/PhD/Broady_data_backup/UWollongong/Cals/offset_V_UW.std'
    visdc__ = 'E:/PhD/Broady_data_backup/UWollongong/Cals/dc_V_UW.std'
    UVdc__ = 'E:/PhD/Broady_data_backup/UWollongong/Cals/dc_U_UW.std'
    Uwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UW_calfiles\\UW_UVcal.txt'
    Vwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\UW_calfiles\\UW_viscal.txt'

elif inst == 'NZ':
    UVoc__ = 'E:/PhD/Broady_data_backup/NIWA/NIWA cal files/OFS_U0060764.std'
    UVdc__ = 'E:/PhD/Broady_data_backup/NIWA/NIWA cal files/DC_U0060763.std'
    visoc__ = 'C:\\Users\\rgryan\\Google Drive\\Documents\\PhD\\Data\\Broady_data_backup\\NIWA\\spectra\\NZ_STD_Spectra_V\\OFS_V0060764.std'
    visdc__ = 'C:\\Users\\rgryan\\Google Drive\\Documents\\PhD\\Data\\Broady_data_backup\\NIWA\\spectra\\NZ_STD_Spectra_V\\DC_V0060763.std'
    Uwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\NZ_calfiles\\NZ_UVcal.txt'
    Vwlcal = 'C:\\Users\\rgryan\\Google Drive\\TIMTAM\\NZ_calfiles\\NZ_viscal.txt'
else:
    print('Error - Offset or DC cal files not defined')

# Read in Offset calibration for UV and Vis
# ==========================================
UVoc_path = open(UVoc__, 'r')
UVoc_data = UVoc_path.readlines()
UVoc_data_strpd = [(UVoc_data[i].strip('\n')) for i in range(len(UVoc_data))]
     
visoc_path = open(visoc__, 'r')
visoc_data = visoc_path.readlines()
visoc_data_strpd = [(visoc_data[i].strip('\n')) for i in range(len(visoc_data))]
    
# Find the data in the offset calibration spectrum
# ==========================================
if folderletter == 'U':
    ocCal_ = UVoc_data_strpd[3:2051]
elif folderletter == 'V':
    ocCal_ = visoc_data_strpd[3:2051]

ocCal = [float(i) for i in ocCal_]

# Dark current calibration readin
# ==========================================
UVdc_path = open(UVdc__, 'r')
UVdc_data = UVdc_path.readlines()
UVdc_data_strpd = [(UVdc_data[i].strip('\n')) for i in range(len(UVdc_data))]

visdc_path = open(visdc__, 'r')
visdc_data = visdc_path.readlines()
visdc_data_strpd = [(visdc_data[i].strip('\n')) for i in range(len(visdc_data))]

if folderletter == 'U':
    dcCal_ = UVdc_data_strpd[3:2051]
elif folderletter == 'V':
    dcCal_ = visdc_data_strpd[3:2051]

dcCal = [float(i) for i in dcCal_]

# Find the number of scans and the exposure time for the calibration spectra
#===================================================================
oc_numscans_ = UVoc_data_strpd[2059]
oc_numscansX = oc_numscans_.split()
oc_numscans = float(oc_numscansX[1])

oc_texp_ = UVoc_data_strpd[2072]        # time in ms
oc_texpX = oc_texp_.split()
oc_texp = float(oc_texpX[2])
oc_inttime = oc_texp*oc_numscans

dc_numscans_ = UVdc_data_strpd[2059]
dc_numscansX = dc_numscans_.split()
dc_numscans = float(dc_numscansX[1])

dc_texp_ = UVdc_data_strpd[2072]      # time in ms
dc_texpX = dc_texp_.split()
dc_texp = float(dc_texpX[2])
dc_inttime = dc_numscans*dc_texp

#===================================================================
# Calibration spectra process
# 1. Offset spectrum is proportional to number of scans. Therefore need to divide by number of scans
if correct_os == True:
    ocCal_c1 = [(ocCal[i]/oc_numscans) for i in range(len(ocCal))] # This has units of counts/scan 
else:
    ocCal_c1 = [(0) for i in range(len(ocCal))]
    
# 2. Correct dark-current spectrum for the offset
if correct_dc == True:
    dcCal_c1 = [(dcCal[i] - ((ocCal_c1[i])*dc_numscans)) for i in range(len(dcCal))] # this has units of counts
    dcCal_c = [((dcCal_c1[i]/dc_inttime)) for i in range(len(dcCal))]                # this has units of counts/ms
else:
    dcCal_c = [(0) for i in range(len(dcCal))]

# 3. Correct offset spectrum using corrected dark current spectrum
if correct_os == True:
    ocCal_c2 = [(ocCal[i] - (dcCal_c[i]*oc_inttime)) for i in range(len(ocCal))]     # this has units of counts
    ocCal_c = [(ocCal_c2[i]/oc_numscans) for i in range(len(ocCal_c2))]              # this has units of counts/scan
else:
    ocCal_c = [(0) for i in range(len(ocCal))] 
# corrected dark current passed to the next stage in units of counts/ms 
# corrected offeset spectrum passed to the next stage in units of counts/scan


# Create wavelength cal dataframe so we only need to do this once, only to be 
#   used if Colour Index calculation is performed
if folderletter == 'U':
    w = open(Uwlcal, 'r')
else:
    w = open(Vwlcal, 'r')

wl_data = w.readlines()
wl_data_strpd = []

for i in range(len(wl_data)):
    wl_data_strpd.append(wl_data[i].strip('\n'))

#%%
lastfolderplus1 = lastfolder+1

while foldernumber < lastfolderplus1:
    
    # Empty lists and data frames to write to;
    sc_list = []     # for scattered light measurements                  
    ds_list = []     # for direct sun measurements
    dc_list = []     # for dark current cakibration measurements
    oc_list = []     # for offset calibration measurements
    hs_list = []     # for horizon scan measurements
    ci_list = []
    
    sc_frame_to_fill = pd.DataFrame()
    ds_frame_to_fill = pd.DataFrame()
    oc_frame_to_fill = pd.DataFrame()
    dc_frame_to_fill = pd.DataFrame()
    hs_frame_to_fill = pd.DataFrame()

    if folders0indexed:
        if len(str(foldernumber)) < 2:
            foldername = 'STD_'+folderletter+'000000'+str(foldernumber)
        elif len(str(foldernumber)) < 3:
            foldername = 'STD_'+folderletter+'00000'+str(foldernumber)
        elif len(str(foldernumber)) < 4:
            foldername = 'STD_'+folderletter+'0000'+str(foldernumber)
        elif len(str(foldernumber)) < 5:
            foldername = 'STD_'+folderletter+'000'+str(foldernumber)
        elif len(str(foldernumber)) < 6:
            foldername = 'STD_'+folderletter+'00'+str(foldernumber)
        elif len(str(foldernumber)) < 7:
            foldername = 'STD_'+folderletter+'0'+str(foldernumber)
    else:
        foldername = 'STD_'+folderletter+str(foldernumber)
    #total_path = folderpath+folderdate+foldername
    total_path = folderpath+foldername

    allFiles = glob.glob(total_path + "/*.std")
            
    print("Now converting: ", folderletter,foldernumber)

    for file_ in allFiles:
        f = open(file_, 'r')
        file_data = f.readlines()
        file_data_strpd = []

        for i in range(len(file_data)):
            file_data_strpd.append(file_data[i].strip('\n'))
        
        # This section deals with the time and date
        #===================================================================
        
        hhmmss = file_data_strpd[2056]                              # This is the measurement start time
        [hours, mins, secs] = [int(x) for x in hhmmss.split(':')]
        dec_time_ = float(hours+(mins/60)+(secs/3600))              # This is now decimal time, appropriate for QDOAS
        dec_time = round(dec_time_, 5)     
         
        # Find and convert the date
        #===================================================================
        if date_format_1 == True:
            date_MDY = file_data_strpd[2054]
            [month, day, year] = [int(info) for info in date_MDY.split("/")]
            day_str = str(day)
            month_str = str(month)
            year_str = str(int(year))
            if day<10:
                day_str = "0"+day_str

            if month<10:
                month_str = "0"+month_str
                
        else:
            date_MDY = file_data_strpd[2054]
            [day, month, year] = [info for info in date_MDY.split("-")]
            day_str = str(int(day))
            year_str = str(int(year))
            
            if month == 'Jan':
                month_str = '01'
            elif month == 'Feb':
                month_str = '02'
            elif month == 'Mar':
                month_str = '03'
            elif month == 'Apr':
                month_str = '04'
            elif month == 'May':
                month_str = '05'
            elif month == 'Jun':
                month_str = '06'
            elif month == 'Jul':
                month_str = '07'
            elif month == 'Aug':
                month_str = '08'
            elif month == 'Sep':
                month_str = '09'        
            elif month == 'Oct':
                month_str = '10'
            elif month == 'Nov':
                month_str = '11'
            else:
                month_str = '12'
                
        date_DMY = day_str +"/"+ month_str+"/" + year_str
       
                 
        # This section finds the data
        #===================================================================
        md_data = file_data_strpd[3:2051]
        md_data_int_ = [int(i) for i in md_data]
        
        # Find the number of scans and the exp time
        #===================================================================
        numscans_ = file_data_strpd[2059]
        numscansX = numscans_.split()
        numscans = float(numscansX[1])
        texp_ = file_data_strpd[2072]    # time in ms
        texpX = texp_.split()
        texp = float(texpX[2])
        inttime = numscans*texp          # int time in ms
        inttime_sec = inttime/1000
        
        # Calculate the Dark current spectrum to subtract;
        dc_ts = [(dcCal_c[i]*(inttime)) for i in range(len(md_data))]    # dcCal_c comes in as counts/ms, so *by measurement
                                                                         #     exposure time (ms)

        # Calculate the offset spectrum to subract;
        oc_ts = [(ocCal_c[i]*(numscans)) for i in range(len(md_data_int_))] # ocCal_c comes in as counts/scan, so *by 
                                                                            #     measurement number of scans

        # Total calibration spectrum to subtract
        cal_ts = [(oc_ts[i]+dc_ts[i]) for i in range(len(md_data_int_))]  # cal_ts now has units of counts
        
        # The calibration-corrected data list to pass to the next stage:
        md_data_int = [(md_data_int_[i] - cal_ts[i]) for i in range(len(md_data_int_))]

        # Now we need to differentiate between DS, calibration and scattered light spectra
        # First, define the names for the different options;
        #=================================================================================
        ds = False        # Direct sun
        oc = False        # offset calibration spectrum
        dc = False        # dark current calibration spectrum
        sc = False        # scattered light (MAX) measurement
        hs = False        # horizon scan measurements
        other_calib = False     # To handle other (Hg lamp) calibrations which are run but don't actually work!
        
        angle_data = file_data_strpd[2051]
        #print(angle_data)

        if angle_data[0:2] == 'DS':
            ds = True
        elif angle_data[:] == 'ofs':
            oc = True
        elif angle_data[:] == 'dc':
            dc = True
        elif angle_data[0] == 'h':
            other_calib = True        
        elif inttime_sec < 5:
            hs = True                   
        else:
            sc = True
        #else:
         #   hs=True
            
        #=================================================================================
        # Direct sun spectrum case;
        #=================================================================================
        if ds:
             #find the elevation angle;
            [other1, EA_real_, other2] = [angle for angle in angle_data[3:].split(" ")]
            #[EAactual, azim] = [float(angle) for angle in angle_data[3:].split(" ")]
            EA_real = round(float(EA_real_), 2)

            # find the SZA;
            scan_geom = file_data_strpd[2099]
            scan_geom_split = scan_geom.split(" ")
            SZA_ = float(scan_geom_split[5])
            SZA = round(SZA_, 2)

            # For direct sun measurements, the azimuth angle is the solar azimuth angle, which is also given 
            #     in the scan geometry section used to find the SZA;
            AzA_ = float(scan_geom_split[3])
            AzA = round(AzA_, 2)
            
            # This section finds the calibration-corrected data
            #===================================================================
            ds_data_flt = md_data_int
            
            # Put everything in the right order for QDOAS...
            ds_data_flt.insert(0, dec_time)   # .append adds things to the end of a list
            ds_data_flt.insert(0, date_DMY)   # .insert(0, x) adds x to the top of a list
            ds_data_flt.insert(0, EA_real)    # Values added on top in reverse order to
            ds_data_flt.insert(0, AzA)        #     ensure they are in correct order!
            ds_data_flt.insert(0, SZA) 

            # Prepare the new data frame for saving
            ds_data_flt_a = np.array(ds_data_flt)
            ds_data_flt_a.transpose()

            ds_data_df= pd.DataFrame(ds_data_flt_a)
            ds_data_dft = ds_data_df.transpose()

            ds_list.append(ds_data_dft)

        #=================================================================================
        # Scattered light spectrum case;
        #================================================================================= 
        elif sc:
            #[EAset, EAactual, azipos] = [float(angle) for angle in angle_data.split(" ") if angle]
            [EAset, EAactual, azim] = [float(angle) for angle in angle_data.split(" ") if angle]
            #EA_real_ = float(EAset)
            
            if EAactual > 80:
                EA_real = 90 
            else: 
                EA_real = round(EAactual, 2)

            # find the SZA;
            scan_geom = file_data_strpd[2099]
            scan_geom_split = scan_geom.split(" ")
            SZA = float(scan_geom_split[5])
            SZA = round(SZA, 2)

            # We know the azimuth angle because we just use a compass to find it
            AzA = round(float(210), 1)
            
            # This section finds the calibration-corrected data
            #===================================================================
            sc_data_flt = md_data_int
            
            if calcCI == True:
                sc_data_forCI = pd.DataFrame(md_data_int_)
                sc_data_forCI.columns = ['int']
                sc_data_forCI['wl'] = pd.DataFrame(wl_data_strpd)
                sc_data_forCI = sc_data_forCI.astype('float')
                sc_data_forCI['wl_n_diff'] = abs(sc_data_forCI['wl'] - CIn)
                sc_data_forCI['wl_d_diff'] = abs(sc_data_forCI['wl'] - CId)
                numidx = sc_data_forCI['wl_n_diff'].idxmin()
                denidx = sc_data_forCI['wl_d_diff'].idxmin()
                CI = (sc_data_forCI['int'][numidx])/(sc_data_forCI['int'][denidx])
                
                ave_int__ = file_data_strpd[2065]
                ave_int_split = ave_int__.split(" ")
                ave_int_ = float(ave_int_split[2])
                ave_int = round(ave_int_, 2)
            
                if texp > 0:
                    norm_ave_int = (ave_int/texp)
                else:
                    norm_ave_int = 0
    
                ci_data_flt = []
                ci_data_flt.insert(0, CI) 
                ci_data_flt.insert(0, norm_ave_int)                
                ci_data_flt.insert(0, hhmmss)
                ci_data_flt.insert(0, date_DMY)   
                ci_data_flt.insert(0, EAset)    
                ci_data_flt.insert(0, AzA)        
                ci_data_flt.insert(0, SZA)

                

                # Prepare the new data frame for saving
                ci_data_flt_a = np.array(ci_data_flt)
                ci_data_flt_a.transpose()

                ci_data_df= pd.DataFrame(ci_data_flt_a)
                ci_data_dft = ci_data_df.transpose()

                ci_list.append(ci_data_dft)
            
            # Put everything in the right order for QDOAS...
            sc_data_flt.insert(0, dec_time)   # .append adds things to the end of a list
            sc_data_flt.insert(0, date_DMY)   # .insert(0, x) adds x to the top of a list
            sc_data_flt.insert(0, EAset)    # Values added on top in reverse order to
            sc_data_flt.insert(0, AzA)        #     ensure they are in correct order!
            sc_data_flt.insert(0, SZA)

            # Prepare the new data frame for saving
            sc_data_flt_a = np.array(sc_data_flt)
            sc_data_flt_a.transpose()

            sc_data_df= pd.DataFrame(sc_data_flt_a)
            sc_data_dft = sc_data_df.transpose()

            sc_list.append(sc_data_dft)
            
        #=================================================================================
        # Horizon scan case;
        #================================================================================= 
        elif hs:
            [EAsupposed, EAactual, azim] = [float(angle) for angle in angle_data.split(" ")[:3] if angle]
            #[EAset, azipos] = [float(angle) for angle in angle_data.split(" ") if angle]
            #EA_real_ = float(EAstart)
            
            if EAactual > 80:
                EA_real = 90 
            else: 
                EA_real = round(EAactual, 2)
                
            # find the SZA;
            scan_geom = file_data_strpd[2099]
            scan_geom_split = scan_geom.split(" ")
            SZA = float(scan_geom_split[5])
            SZA = round(SZA, 2)
            
            # find intensity values
            int_1138 = float(file_data_strpd[1138])
            int_1094 = float(file_data_strpd[1094])
            ave_int__ = file_data_strpd[2065]
            ave_int_split = ave_int__.split(" ")
            ave_int_ = float(ave_int_split[2])
            ave_int = round(ave_int_, 2)
            
            if texp > 0:
                norm_ave_int = (ave_int/texp)
                norm_int_1094 = int_1094/texp                
            else:
                norm_ave_int = 0
                norm_int_1094 = 0                
            
            # We know the azimuth angle because we just use a compass to find it
            AzA = float(200)
            AzA = round(AzA, 1)
            
            # This section finds the calibration-corrected data
            #===================================================================
            
            if only_save_hs_int == True:
                hs_data_flt = []
                hs_data_flt.insert(0, ave_int)
                hs_data_flt.insert(0, norm_int_1094)   # second intensity point
                hs_data_flt.insert(0, norm_ave_int)    # relative intensity between the two                
                hs_data_flt.insert(0, dec_time)        # .append adds things to the end of a list
                hs_data_flt.insert(0, date_DMY)        # .insert(0, x) adds x to the top of a list
                hs_data_flt.insert(0, EA_real)         # Values added on top in reverse order to
                hs_data_flt.insert(0, AzA)             #     ensure they are in correct order!
                hs_data_flt.insert(0, SZA)
            else:
                hs_data_flt = md_data_int              # Appropriate for QDOAS!
                hs_data_flt.insert(0, dec_time)        # .append adds things to the end of a list
                hs_data_flt.insert(0, date_DMY)        # .insert(0, x) adds x to the top of a list
                hs_data_flt.insert(0, EA_real)         # Values added on top in reverse order to
                hs_data_flt.insert(0, AzA)             #     ensure they are in correct order!
                hs_data_flt.insert(0, SZA)
            
            # Prepare the new data frame for saving
            hs_data_flt_a = np.array(hs_data_flt)
            hs_data_flt_a.transpose()

            hs_data_df= pd.DataFrame(hs_data_flt_a)
            hs_data_dft = hs_data_df.transpose()

            hs_list.append(hs_data_dft)

        #=================================================================================
        # Offset calibration spectrum case;
        #================================================================================= 
        elif oc:
            SZA = 0
            EA_real = 0
            AzA = 0

            # Put everything in the right order for QDOAS...
            # Don't want calibration corrected data here since this is the calibration!
            oc_data_flt = md_data_int_

            oc_data_flt.insert(0, dec_time)   
            oc_data_flt.insert(0, date_DMY)   
            oc_data_flt.insert(0, 'oc')    
            oc_data_flt.insert(0, numscans)        
            oc_data_flt.insert(0, texp) 

            # Prepare the new data frame for saving
            oc_data_flt_a = np.array(oc_data_flt)
            oc_data_flt_a.transpose()

            oc_data_df= pd.DataFrame(oc_data_flt_a)
            oc_data_dft = oc_data_df.transpose()

            oc_list.append(oc_data_dft)

        #=================================================================================
        # Dark current calibration spectrum case;
        #================================================================================= 
        elif dc:
            SZA = 0
            EA_real = 0
            AzA = 0

            # again don't want the calibration-corrected data so take md_data_int_
            dc_data_flt = md_data_int_
            
            # Put everything in the right order for QDOAS...
            dc_data_flt.insert(0, dec_time) 
            dc_data_flt.insert(0, date_DMY)   
            dc_data_flt.insert(0, 'dc')    
            dc_data_flt.insert(0, numscans)       
            dc_data_flt.insert(0, texp) 

            # Prepare the new data frame for saving
            dc_data_flt_a = np.array(dc_data_flt)
            dc_data_flt_a.transpose()

            dc_data_df= pd.DataFrame(dc_data_flt_a)
            dc_data_dft = dc_data_df.transpose()

            dc_list.append(dc_data_dft)
        
        elif other_calib:
            print('Found calibration spectra in file ', foldernumber)
        else:
            print("oh dear, something has gone wrong :(")
            
        #print(date_DMY)    
    # Saving section
    #=================================================================================
    date2save = day_str + month_str+ year_str


    # Save ds to file;
    #=================================================================================
    if len(ds_list)>0:
        if saveDS == True:
            ds_frame_to_fill = pd.concat(ds_list)
            ds_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_DS_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)
        #else: 
            #print("There's no direct sun data in this folder")

        # Save sc to file;
        #=================================================================================    
    if len(sc_list)>0:
        if saveSC == True:
            sc_frame_to_fill = pd.concat(sc_list)
            sc_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_SC_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)

        # Save hs to file;
        #=================================================================================    
    if len(hs_list)>0:
        if saveHS == True:
            hs_frame_to_fill = pd.concat(hs_list)
            hs_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_HS_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)
            
        # Save oc to file;
        #=================================================================================
        if len(oc_list)>0:
            if saveOS == True:
                oc_frame_to_fill = pd.concat(oc_list)
                oc_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_OC_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)


    # Save dc to file;
    #=================================================================================
    if len(dc_list)>0:
        if saveDC == True:
            dc_frame_to_fill = pd.concat(dc_list)
            dc_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_DC_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)
        
    # Save colour index to file;
    #=================================================================================
    if len(ci_list)>0:
        if saveCI == True:
            ci_frame_to_fill = pd.concat(ci_list)
            ci_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_CI_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)    

        #=================================================================================
    foldernumber = foldernumber+100

print("FINISHED! :-)")
#%%

sc_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_SC_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)

ci_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_CI_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)
dc_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_DC_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)
oc_frame_to_fill.to_csv(r'C:/'+path2save+inst+'_OC_'+date2save+'-'+folderletter+str(foldernumber)+end, 
                                   sep = ' ', header =None, index=None)