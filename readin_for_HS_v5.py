# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 11:15:47 2017

@author: rgryan
"""

# Import section
#=====================================================================================================================
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

days = ['01', '03', '04', '05', '06', '07', '08', '09', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']

days = ['21']
month = '09'
year_long = '2017'
year = '17'

inst = 'UM'

save_temp_info = True
plot_temp_info = True
datapath = 'C:\\Users\\rgryan\\Google Drive\\Documents\\PhD\\Data\\UM_MAXDOAS_Aurora\\pre-voyage\\spectra\\New folder\\'
#datapath = 'C:\\Users\\rgryan\\Google Drive\\Documents\\PhD\\Data\\UM_MAXDOAS_Aurora\\pre-voyage\\spectra\\'
#datapath = 'E:\\PhD\\Broady_data_backup\\BOM\\spectra\\U\\hs\\'
#templogpath = 'E:\\PhD\\Broady_data_backup\\NIWA\\log\\NZ_Templog_15-22Feb2017\\'
#templogpath = 'E:\\PhD\\Broady_data_backup\\BOM\\log\\BM_Templog_17Feb-7Apr2017\\'
#templogpath = 'C:\\Users\\rgryan\\Google Drive\\Documents\\PhD\\Data\\UM_MAXDOAS_Aurora\\pre-voyage\\logs\\'
templogpath = datapath
gradmaxtemplist_ = []   # lists to save the gradmax and temperature
gradmaxEAlist_ = []     #    information too

# FUCNTION TO CONVERT DEC TIME TO HH:MM:SS
# ========================================
def dectime2hms(dechours):
    hour_i = int(dechours)
    if hour_i < 10:
        hour_s = '0'+str(hour_i)
    else:
        hour_s = str(hour_i)
    mins_i = int((dechours - float(hour_i))*60) 
    if mins_i < 10:
        mins_s = '0'+str(mins_i)
    else:
        mins_s = str(mins_i)    
    secs_i = int((((dechours - float(hour_i))*60)-float(mins_i))*60)
    if secs_i < 10:
        secs_s = '0'+str(secs_i)
    else:
        secs_s = str(secs_i)
    hms = hour_s+':'+mins_s+':'+secs_s
    return hms

# ========================================
for d in days:
    day = d
    print('now looking at '+day+'/'+month+'/'+year_long)
    folder2lookat = inst+'_HS_'+day+month+year
    date = day+month+year   # this date is just used for saving later on

    allFiles = glob.glob(datapath+folder2lookat + "/*.txt")
    df_from_each_file = (pd.read_csv(f, index_col=None, header=None, 
                                     sep= ' ') for f in allFiles)
    readin = pd.concat(df_from_each_file, ignore_index=True)
    readin.columns = ['SZA', 'Azimuth', 'EA', 'Date', 'time', 
                      'norm_ave_int', 'norm_int_1094', 'ave_int']
    readin[['SZA', 'Azimuth', 'EA', 'time', 'norm_ave_int', 
        'norm_int_1094', 'ave_int']] = readin[['SZA', 
                                   'Azimuth', 'EA', 'time', 
                                   'norm_ave_int', 'norm_int_1094', 
                                   'ave_int']].astype(float)
    
    readin['DateTime'] = pd.to_datetime((readin['Date']+' '+readin.time.apply(
            dectime2hms)), dayfirst=True)
    readin = readin.set_index(readin['DateTime'])
    readin.sort_values('DateTime', inplace=True)
    
    # Drop all the values where the Elevation angle is out of range
    # ... some 90 deg values have snuck in
    readin = readin.drop(readin[readin.EA > 10].index)
    
    if save_temp_info == True:
        temp_log = templogpath+'Temperature'+year+month+day+'.log'
        temp_df = pd.read_csv(temp_log,  header=None, skiprows=1, sep = ';')
        temp_df.columns = ['Date', 'time', 'AM_PM', 'Pressure', 'T_Electronics', 'T_Spectrometer',
                   'T_Telescope', 'T2', 'T_Ambient', 'PowerOut']

        temp_df['DateTime'] = pd.to_datetime(temp_df['Date'].map(str) + 
               ' ' + temp_df['time'] + ' ' + temp_df['AM_PM'], dayfirst=True)
        temp_df = temp_df.set_index([temp_df['DateTime']])
        temp_df.sort_values('DateTime', inplace=True)
        
        R = pd.merge_asof(readin, temp_df,
                          left_on='DateTime', right_on='DateTime',
                          direction='nearest')
        R = R.set_index('DateTime')
                          
    else:
        continue
        
#%%
    plot = plt.figure()
    figsize = (5,3)
    fontsize = 14
    legpos = (0.5,0.3)

    whattoplot = 'norm_ave_int'
    style = 'bo'
    gradstyle = 'r--'
    xlim = [-8, 12]
    #timesets = ['21:00', '22:00', '23:00', '00:00', '01:00', '02:00', '03:00',
    #            '04:00', '05:00', '06:00', '07:00', '08:00', '09:00']
    #timesetsA = ['7am', '8am', '9am', '10am', '11am', '12pm', '1pm',
    #            '2pm', '3pm', '4pm', '5pm', '6pm', '7pm']
    
    timesets = ['02:00', '02:10', '02:20', '02:30',
                '02:40', '02:50', '03:00', '03:10', '03:20', '02:30', '03:40', 
                '03:50', '04:00', '04:10', '04:20', '04:30', '04:40', '04:50', 
                '05:00', '05:10', '05:20', '05:30', '05:40', '05:50', '06:00']
    
    gradmaxtemplist = []
    gradmaxEAlist = []

    a1 = R.between_time(start_time='02:30', end_time='02:50')
    maxint1 = a1.norm_ave_int.max() + 0.15*(a1.norm_ave_int.max())
    minint1 = a1.norm_ave_int.min() - 0.15*(a1.norm_ave_int.max())
    h = a1.plot(x='EA', y=whattoplot, fontsize=fontsize, 
                ylim=[minint1, maxint1],
                xlim=xlim, style='.', figsize=figsize)    
    
    for i in np.arange(len(timesets)):
        if i < (len(timesets)-1):
            start = timesets[i]
            end = timesets[i+1]
            #ts = R.between_time(start_time=start, end_time=end)
            ts = R.between_time(start_time=start, 
                                end_time=end)
            if len(ts)>0:
                ts_grad = pd.DataFrame((ts.norm_ave_int.diff(periods=1)
                   )/(ts.EA.diff(periods=1)))
                ts_grad_t = ts_grad.transpose()
                EAs = pd.DataFrame(ts['EA'])
                Temps = pd.DataFrame(ts['T_Ambient'])
                EAs_t = EAs.transpose()
                Temps_t = Temps.transpose()
                ts_grad_dft1 = EAs_t.append(ts_grad_t)
                ts_grad_dft = ts_grad_dft1.append(Temps_t)
                ts_grad_df = ts_grad_dft.transpose()
                ts_grad_df.columns = ['EA', 'grad', 'temp']
                maxint = ts.norm_ave_int.max() + 0.15*(ts.norm_ave_int.max())
                minint = ts.norm_ave_int.min() - 0.15*(ts.norm_ave_int.max())
                g = ts.plot(x='EA', y=whattoplot, fontsize=fontsize, 
                            ylim=[minint, maxint],
                            xlim=xlim, style=style, figsize=figsize)
                g.set_title('Horizon scan '+timesets[i]+'_'+date,
                            fontsize=fontsize)
                g.set_xlabel('Elevation angle', fontsize=fontsize)
                g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
                gradmax = ts_grad_df.grad.idxmax()
                gradmaxtemplist.append(ts_grad_df.temp[gradmax])
                gradmaxtempdf = pd.DataFrame(gradmaxtemplist)
                pkpos = ts_grad_df.EA[gradmax]
                gradmaxEAlist.append(pkpos)
                gradmaxEAdf = pd.DataFrame(gradmaxEAlist)
                #print(pkpos)
                g.axvline(pkpos, color='r', linestyle='--', ymax=maxint, 
                          ymin=minint)
                pktime = ts.time_y[gradmax]
                g.legend(['data', 'grad, max at '+str(pkpos)], 
                          bbox_to_anchor=legpos)
                ts.plot(x='EA', y=whattoplot, fontsize=fontsize, style='.',
                        label=start, ylim=[minint1, maxint1],
                        xlim=xlim, ax=h)
                fig = g.get_figure()
                fig.savefig(datapath+folder2lookat+'/'+timesets[i]+'_'+date+'.png', 
                            bbox_inches='tight')    
                plt.close(fig) 
    h.set_title('All horizon scans '+date, fontsize=fontsize)
    h.legend(timesets[:-1], bbox_to_anchor=(1.,1.), loc=2)
    fig = h.get_figure()
    fig.savefig(datapath+folder2lookat+'/allHS_'+date+'.png', 
                            bbox_inches='tight')
    
    if len(gradmaxtemplist) > 0:
        gradmaxtemplist_.append(gradmaxtempdf)
        gradmaxtempdf_ = pd.concat(gradmaxtemplist_)
        gradmaxtempdf_ = gradmaxtempdf_.reset_index()
        gradmaxEAlist_.append(gradmaxEAdf)
        gradmaxEAdf_= pd.concat(gradmaxEAlist_)
        gradmaxEAdf_ = gradmaxEAdf_.reset_index()

if plot_temp_info == True:    
    gradmaxinfo = pd.DataFrame()
    gradmaxinfo['Temp'] = gradmaxtempdf_[0]
    gradmaxinfo['gradmax'] = gradmaxEAdf_[0]
    #gradmaxinfo.columns = ['Temp', 'gradmax']
    
    # drop any values greater than zero or temp less than 5
    #  since I've seen by inspection that 
    #  these don't make sense
    gradmaxinfo = gradmaxinfo.drop(
            gradmaxinfo[gradmaxinfo.gradmax > 0].index)
    gradmaxinfo = gradmaxinfo.drop(
            gradmaxinfo[gradmaxinfo.gradmax < -3].index)
    gradmaxinfo = gradmaxinfo.drop(
            gradmaxinfo[gradmaxinfo.Temp < 15].index)
    
    gradmaxinfo.to_csv(datapath+inst+'gradmaxinfo_March2017.txt', 
                       sep=' ', header=True, index=False)

#%%
    # Scatter plot of gradmax vs temp or time
    # =======================================
    plot = plt.figure()
    figsize = (5,3)
    fontsize = 14
    yaxis = 'Temp'
    xaxis = 'gradmax'

    model = sm.OLS(gradmaxinfo.Temp, sm.add_constant(gradmaxinfo.gradmax))
    q = model.fit().params
    results = model.fit()

    x = np.arange(-5, 5)

    ax = gradmaxinfo.plot(x=xaxis, y=yaxis, kind='scatter', fontsize=fontsize, 
               figsize=figsize, color='y')
    ax.plot(x, q.const+ q.gradmax*x, color='blue')
    ax.set_xlim([-4, 4])
    ax.set_ylim([10,50])
    m = str(round(q[0], 3))
    c = str(round(q[1], 3))
    #print('y='+m+'x + '+c)
    ax.text(-3.5,44.2, 'y='+m+'*x + '+c, fontsize=fontsize, color='blue')
    fig = ax.get_figure()
    fig.savefig(datapath+'_vsTAmbient_'+yaxis+'.png', bbox_inches='tight') 
#%%
