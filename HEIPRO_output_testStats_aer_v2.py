# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:05:22 2017

@author: rgryan
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import datetime
import os


sh = False    # Plotting the scale height info?
zc = False   # Plotting the zero height concentration info?
re = True    # Plotting the a.p. relative error info?
op = False   # Plotting a.p. aerosol optical properties info?

path = 'E:\\Sciatran2\\AEROSOL_RETRIEVAL_v-1-5\\Campaign\\'

testset = ''

date = '20170307'
time = '130130'
startdate = datetime.datetime(2017, 3, 7, 6)  
enddate = datetime.datetime(2017, 3, 7, 20)

tests = ['t111', 't112', 't102', 't113','t114', 't115']
dates = ['20170307','20170308', '20170309']

#scale_height = [0.2, 0.4, 0.6, 0.8, 1.0,1.2]
#ground extinction = [0.02,0.04, 0.06, 0.08, 0.1, 0.12]
#relerror = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
#opprop = [0.3, 0.8, 1.29, 1.8]
#asy = [0.66, 0.69, 0.72, 0.75]
#ssa = [0.7, 0.8, 0.89, 1.0]

values = [0.2, 0.4, 0.6, 0.8, 1.0,1.2]

colours = ['red', 'orange', 'yellow', 'green', 'lightseagreen', 
           'skyblue', 'mediumblue', 'midnightblue', 
           'darkviolet', 'darkmagenta', 'magenta', 'pink']

if not os.path.exists(path+'aer_'+testset+'_resultplots'):
        os.mkdir(path+'aer_'+testset+'_resultplots')

mm_rms = []
aod_ave = []
aod_vals = pd.DataFrame()
aod_err_vals = pd.DataFrame()
prof_vals = pd.DataFrame()
prof_err_vals = pd.DataFrame()
aodErr_ave = []
aodPErr_ave = []
csq_ave = []
dofs_ave = []

for test in tests:
    mmfilelist = []
    aodfilelist = []
    for date in dates:
        fullpath = path+'aer_retr_7-9March2017_'+test+'\\'+date+'\\'
    
        # Read in the measured and retrieved values
        mmfile_ = pd.read_csv(fullpath+'general/meas_'+date+'.dat', delim_whitespace=True, 
                       parse_dates=[['date', 'time']], dayfirst=True)
        #mmfile_ = mmfile_.sort_values('date_time')
        #mmfile_ = mmfile_.drop_duplicates(subset='date_time')
        
        mmfile_ = mmfile_[mmfile_['elev']<80]
        mmfile_ = mmfile_[mmfile_['O4retr']>0] # remove negative retrievals (not physical)
        mmfilelist.append(mmfile_)
        # Read in the retrieved AOD and errors
        aodfile_ = pd.read_csv(fullpath+'general/retrieval_'+date+'.dat', delim_whitespace=True, 
                       parse_dates=[['Date', 'Time']], dayfirst=True)
        #aodfile_ = aodfile_.sort_values('Date_Time')
        #aodfile_ = aodfile_.drop_duplicates(subset='Date_Time')    
        aodfile_ = aodfile_[aodfile_['AOT361']<0.225] # remove errors where AOD too high to be realistic
        aodfile_ = aodfile_[aodfile_['AOT361']>0] #  and remove negative AOD values
        aodfilelist.append(aodfile_)
    
    # Section to deal with AOD values and errors
    aodfile = pd.concat(aodfilelist)
    aodfile.reset_index(inplace=True)
    aod_ave.append(aodfile['AOT361'].mean())
    aodErr_ave.append(aodfile['err_AOT361'].mean())
    aodfile['percentError'] = 100*(aodfile['err_AOT361']/aodfile['AOT361'])
    aodPErr_ave.append(aodfile['percentError'].mean())
    # The chi squared
    csq_ave.append(aodfile['chisq'].mean())
    
    # Section to calculate RMS value for (O4meas - O4retr)
    mmfile = pd.concat(mmfilelist)
    mmfile.reset_index(inplace=True)
    x = np.array((mmfile['elev']))
    y = np.array((mmfile['O4meas']))
    y1 = np.array((mmfile['O4retr']))
    err = np.array((mmfile['err_O4meas']))

    ss = [(((y[i])-(y1[i]))**2) for i in np.arange(len(y))]
    rms = np.sqrt(sum(ss)/len(ss))
    mm_rms.append(rms)
     
    # Save the daily aod diurnal profile, and associated errors
    aod_vals[test] = aodfile['AOT361']
    aod_err_vals[test] = aodfile['err_AOT361']
    
    # Averaging kernels
    akfiles = glob.glob(fullpath+'av_kernels/*.dat')
    dofs_ = []
    for file in akfiles:
        akf = pd.read_csv(file, delim_whitespace=True)

        ak_formatrix = akf.iloc[0:20,5:25]
        ak_matrix = ak_formatrix.as_matrix()
        dofs_.append(np.trace(ak_matrix))
    dofs_ave.append((sum(dofs_)/float(len(dofs_))))
    
    # Also plot specific averaging kernels from one measurement time
    akfile = pd.read_csv(fullpath+'av_kernels/avk_ext_'+date+'_'+time+'.dat',
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
    fig.savefig(path+'aer_'+testset+'_resultplots/'+test+'_avk_'+date+'_'+time+'.png', 
                    bbox_inches='tight')
    profile = pd.read_csv(fullpath+'/profiles/prof361nm_'+date+'_'+time+'.dat',
                     delim_whitespace=True)
    prof_vals[test] = profile['retrieved'][:3]
    prof_err_vals[test] = profile['err_retrieved'][:3]
    
    xlim=(0,0.30)
    ylim=(0,4)
    #figsize=(3,3)
    prop = profile.plot(x='apriori', y='z', style='k-', figsize=figsize,
                    xlim=xlim, ylim=ylim, fontsize=fontsize)
    profile.plot(x='retrieved', y='z', xerr='err_retrieved', figsize=figsize, 
             color='darkorange', xlim=xlim, ylim=ylim, ax=prop, fontsize=fontsize)
    prop.legend(['a-priori', 'retrieved'], loc='upper right', fontsize=fontsize)

    # Set the axes ticks and labels
    xticks = [0,  5, 10, 15, 20, 25, 30]
    xlab = '(km$^{-1}$) (x10$^{-2})'
    yticks = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    ylab = 'Altitude (km)'

    prop.set_xticklabels(xticks, fontsize=fontsize)
    prop.set_yticklabels(yticks, fontsize=fontsize)
    prop.set_xlabel(xlab, fontsize=fontsize)
    prop.set_ylabel(ylab, fontsize=fontsize)

    fig = prop.get_figure()
    fig.savefig(path+'aer_'+testset+'_resultplots/'+test+'_prof_'+date+'_'+time+'.png', 
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
    fig2.savefig(path+'aer_'+testset+'_resultplots/'+test+'_profErrors_'+date+'_'+time+'.png', 
                    bbox_inches='tight')

#%%
statsummary = pd.DataFrame()
statsummary['test'] = pd.Series(tests)
statsummary['mm_rms'] = pd.Series(mm_rms)
statsummary['aod_ave'] = pd.Series(aod_ave)
statsummary['aodErr_ave'] = pd.Series(aodErr_ave)
statsummary['aodPErr_ave'] = pd.Series(aodPErr_ave)
statsummary['csq_ave'] = pd.Series(csq_ave)
statsummary['dofs_ave'] = pd.Series(dofs_ave)

aod_vals.columns = [str(i) for i in values]
aod_err_vals.columns = [str(i) for i in values]
    
aod_vals['std'] = aod_vals.std(axis=1)
aod_vals['mean'] = aod_vals.mean(axis=1)
aod_err_vals['std'] = aod_err_vals.std(axis=1)
aod_err_vals['mean'] = aod_err_vals.mean(axis=1)
prof_err_vals['std'] = prof_err_vals.std(axis=1)
prof_err_vals['mean'] = prof_err_vals.mean(axis=1)
prof_vals['std'] = prof_vals.std(axis=1)
prof_vals['mean'] = prof_vals.mean(axis=1)
aod_vals['Date_Time'] = aodfile['Date_Time']
aod_vals = aod_vals[aod_vals.Date_Time.notnull()]
aod_err_vals['Date_Time'] = aodfile['Date_Time']
aod_err_vals = aod_err_vals[aod_err_vals.Date_Time.notnull()]

# Calculate mean standard deviations for AOD and profiles
prof_lowest500_avg_std = prof_vals['std'].mean()
aod_avg_std = aod_vals['std'].mean()

#%%

statsummary.to_csv(path+'aer_'+testset+'_resultplots/apriori_tests_statsummary.txt', sep = '\t', index=False)
aod_vals.to_csv(path+'aer_'+testset+'_resultplots/apriori_tests_diurnalAOD.txt', sep = '\t', index=False)
aod_err_vals.to_csv(path+'aer_'+testset+'_resultplots/apriori_tests_diurnalAODerrors.txt', sep = '\t', index=False)
prof_err_vals.to_csv(path+'aer_'+testset+'_resultplots/apriori_tests_profileErrors.txt', sep = '\t', index=False)
prof_vals.to_csv(path+'aer_'+testset+'_resultplots/apriori_tests_profiledetails.txt', sep = '\t', index=False)

#%%
# Plot all the diurnal profiles together
# ======================================
scale_height_strings = [str(i) for i in scale_height]
zconc_strings = [str(i) for i in zconc]
relerror_strings = [str(i) for i in relerror]

strings = [str(i) for i in values]
figsize=(17,4)
fontsize=14

fig = plt.figure(figsize=figsize)
ax=fig.add_subplot(111)
#ax.set_facecolor('white')
c=0   # Colour counter

if sh==True:
    savename='scaleheight'   
elif zc==True:
    savename='zconc'
elif re==True:
    savename='relerror'
elif op==True:
    savename = 'EA'
    
for j in strings:
    x = np.array((aod_vals['Date_Time']))
    y = np.array((aod_vals[j]))
    yerr = np.array((aod_err_vals[j]))
    ax.errorbar(x,y,yerr=yerr,color=colours[c])  
    c = c+1
ax.legend(strings, fontsize=fontsize, loc=2, bbox_to_anchor=(1,1))
ax.set_xlabel('Time', fontsize=fontsize)
ax.set_ylabel('AOD', fontsize=fontsize)
fig.savefig(path+'aer_'+testset+'_resultplots/apriori_tests_diurnalAOD_'+testset+'.png', bbox_to_anchor='tight')    
#%%
# Plot the stats summaries

y1 = 'mm_rms'
y2 = 'dofs_ave'

figsize=(4,3)

if sh==True:
    savename='scaleheight'
    xlab = 'Scale height (km)'
elif zc==True:
    savename='zconc'
    xlab = 'z(0) ext. ($km^(-1)$)'
elif re==True:
    savename='relerror'
    xlab = 'z(0) ext. ($km^{-1}$)'
elif op==True:
    savename = 'EA'
    xlab= 'Elev. angle correction'
statsummary['ofinterest'] = pd.Series(values)
    
ssplot = statsummary.plot(x='ofinterest', y=y1, style='ro', figsize=figsize, label='RMS')
statsummary.plot(x='ofinterest', y=y2, ax=ssplot, secondary_y=True, style='bo',
                 figsize=figsize, label='DOFs')
lines = ssplot.get_lines() + ssplot.right_ax.get_lines()
ssplot.set_xlabel(xlab, fontsize=fontsize)
ssplot.set_ylabel(y1, fontsize=fontsize, color='red')
ssplot.right_ax.set_ylabel(y2, fontsize=fontsize, color='blue')
ssplot.grid(False)
ssplot.right_ax.grid(False)
ssplot.legend(lines, [l.get_label() for l in lines], loc='center right')
fg = ssplot.get_figure()
fg.savefig(path+'aer_'+testset+'_resultplots/'+y1+'_'+y2+'.png', 
                  bbox_inches='tight')
