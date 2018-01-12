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
from decimal import Decimal
#from os import path


sh = True    # Plotting the scale height info?
zc = False   # Plotting the zero height concentration info?
re = False    # Plotting the a.p. relative error info?
op = False   # Plotting a.p. aerosol optical properties info?

path = 'E:\\Sciatran2\\TRACEGAS_RETRIEVAL_v-1-4\\Campaign\\'

testset = 'apElev'
# OPTIONS:   aerGext aerSH  tgSH tgGC  aerAsy  aerAng  aerSSA  apElev  tgRErr  

tg = 'HONO'
tg1 = 'HCHO'
#tg1 = tg

date = '20170307'
time = '130130'
startdate = datetime.datetime(2017, 3, 7, 6)  
enddate = datetime.datetime(2017, 3, 7, 20)

tests = ['t131', 't102','t132']
dates = ['20170307','20170308', '20170309']

#scale_height = [0.2, 0.4, 0.6, 0.8, 1.0,1.2]
#ground extinction = [0.02,0.04, 0.06, 0.08, 0.1, 0.12]
#relerror = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
#opprop = [0.3, 0.8, 1.29, 1.8]
#asy = [0.66, 0.69, 0.72, 0.75]
#ssa = [0.7, 0.8, 0.89, 1.0]

values = [-1.5, -1, -0.5]

colours = ['red', 'orange', 'yellow', 'green', 'lightseagreen', 
           'skyblue', 'mediumblue', 'midnightblue', 
           'darkviolet', 'darkmagenta', 'magenta', 'pink']

mm_rms = []
ppm_ave = []
vcd_ave = []
ppm_vals = pd.DataFrame()
ppm_err_vals = pd.DataFrame()
vcd_vals = pd.DataFrame()
vcd_err_vals = pd.DataFrame()
prof_vals = pd.DataFrame()
prof_err_vals = pd.DataFrame()
ppmErr_ave = []
ppmPErr_ave = []
vcdErr_ave = []
vcdPErr_ave = []
csq_ave = []
dofs_ave = []

if not os.path.exists(path+tg+'_'+testset+'_resultplots'):
        os.mkdir(path+tg+'_'+testset+'_resultplots')

for test in tests:
    mmfilelist = []
    concfilelist = []
    for date in dates:
        fullpath = path+tg+'_retr_7-9March2017_'+test+'\\'+date+'\\'
    
        # Read in the measured and retrieved values
        mmfile_ = pd.read_csv(fullpath+'general/meas_'+date+'.dat', delim_whitespace=True, 
                       parse_dates=[['date', 'time']], dayfirst=True)
        #mmfile_ = mmfile_.sort_values('date_time')
        #mmfile_ = mmfile_.drop_duplicates(subset='date_time')
        
        mmfile_ = mmfile_[mmfile_['elev']<80]
        mmfile_ = mmfile_[mmfile_[tg1+'retr']>0] # remove negative retrievals (not physical)
        mmfilelist.append(mmfile_)
        # Read in the retrieved concentrations and errors
        concfile_ = pd.read_csv(fullpath+'general/'+tg1+'_retrieval_'+date+'.dat', delim_whitespace=True, 
                       parse_dates=[['Date', 'Time']], dayfirst=True)   
        #concfile_ = concfile_[concfile_['AOT361']<0.225] # remove errors where concentrations too high to be realistic
        concfile_ = concfile_[concfile_['surf_vmr(ppmv)']>0] #  and remove negative concentrations values
        concfilelist.append(concfile_)
    
    # Section to deal with concentrations values and errors
    concfile = pd.concat(concfilelist)
    concfile.reset_index(inplace=True)
    ppm_ave.append(concfile['surf_vmr(ppmv)'].mean())
    ppmErr_ave.append(concfile['err_surf_vmr'].mean())
    vcd_ave.append(concfile[tg1+'_VCD(molec/cm^2)'].mean())
    vcdErr_ave.append(concfile['err_'+tg1+'_VCD'].mean())
    concfile['ppm_percentError'] = 100*(concfile['err_surf_vmr']/concfile['surf_vmr(ppmv)'])
    concfile['vcd_percentError'] = 100*(concfile['err_'+tg1+'_VCD']/concfile[tg1+'_VCD(molec/cm^2)'])
    ppmPErr_ave.append(concfile['ppm_percentError'].mean())
    vcdPErr_ave.append(concfile['vcd_percentError'].mean())
    
    # The chi squared
    csq_ave.append(concfile['chisq'].mean())
    
    # Section to calculate RMS value for (meas - retr)
    mmfile = pd.concat(mmfilelist)
    mmfile.reset_index(inplace=True)
    x = np.array((mmfile['elev']))
    y = np.array((mmfile[tg1+'meas']))
    y1 = np.array((mmfile[tg1+'retr']))
    err = np.array((mmfile['err_'+tg1+'meas']))

    ss = [(((y[i])-(y1[i]))**2) for i in np.arange(len(y))]
    rms = np.sqrt(sum(ss)/len(ss))
    mm_rms.append(rms)
     
    # Save the daily conc diurnal profile, and associated errors
    ppm_vals[test] = concfile['surf_vmr(ppmv)']
    ppm_err_vals[test] = concfile['err_surf_vmr']
    vcd_vals[test] = concfile[tg1+'_VCD(molec/cm^2)']
    vcd_err_vals[test] = concfile['err_'+tg1+'_VCD']
    
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
    akfile = pd.read_csv(fullpath+'av_kernels/avk_'+date+'_'+time+'.dat',
                     delim_whitespace=True)

    ak_formatrix = akfile.iloc[0:20,5:25]
    ak_matrix = ak_formatrix.as_matrix()
    dofs = np.trace(ak_matrix)
    xlim=[-0.1,1.]
    fontsize=14
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
    fig.savefig(path+tg+'_'+testset+'_resultplots/'+test+'_avk_'+date+'_'+time+'.png', 
                    bbox_inches='tight')
#%%    
    profile = pd.read_csv(fullpath+'/profiles/'+tg1+'_prof_'+date+'_'+time+'.dat',
                     delim_whitespace=True)
    prof_vals[test] = profile['retr_vmr']
    prof_err_vals[test] = profile['err_r_vmr']
    
    xlim=(0,0.03)
    ylim=(0,4)
    #figsize=(3,3)
    prop = profile.plot(x='apriori(vmr)', y='z', style='k-', figsize=figsize,
                    xlim=xlim, ylim=ylim, fontsize=fontsize)
    profile.plot(x='retr_vmr', y='z', xerr='err_r_vmr', figsize=figsize, 
             color='darkorange', xlim=xlim, ylim=ylim, ax=prop, fontsize=fontsize)
    prop.legend(['a-priori', 'retrieved'], loc='upper right', fontsize=fontsize)

    # Set the axes ticks and labels
    xticks = [0,  0.5, 0.10, 0.15, 0.20,0.25, 0.30]
    xlab = 'NO2 (ppb)'
    yticks = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    ylab = 'Altitude (km)'

    prop.set_xticklabels(xticks, fontsize=fontsize)
    prop.set_yticklabels(yticks, fontsize=fontsize)
    prop.set_xlabel(xlab, fontsize=fontsize)
    prop.set_ylabel(ylab, fontsize=fontsize)

    fig = prop.get_figure()
    fig.savefig(path+tg+'_'+testset+'_resultplots/'+test+'_prof_'+date+'_'+time+'.png', 
                   bbox_inches='tight')

    prep = profile.plot(x='err_s_vmr', y='z', style='m-', figsize=figsize,
                    xlim=xlim, ylim=ylim, fontsize=fontsize)
    profile.plot(x='err_m_vmr', y='z', style='b-',figsize=figsize,
             xlim=xlim, ylim=ylim, ax=prep, fontsize=fontsize)

    prep.set_xticklabels(xticks, fontsize=fontsize)
    prep.set_yticklabels(yticks, fontsize=fontsize)
    prep.set_xlabel(xlab, fontsize=fontsize)
    prep.set_ylabel(ylab, fontsize=fontsize)

    prep.legend(['Smooth.', 'Noise'], loc='upper right', fontsize=fontsize)
    fig2 = prep.get_figure()
    fig2.savefig(path+tg+'_'+testset+'_resultplots/'+test+'_profErrors_'+date+'_'+time+'.png', 
                   bbox_inches='tight')

#%%
statsummary = pd.DataFrame()
statsummary['test'] = pd.Series(tests)
statsummary['mm_rms'] = pd.Series(mm_rms)
statsummary['ppm_ave'] = pd.Series(ppm_ave)
statsummary['ppmErr_ave'] = pd.Series(ppmErr_ave)
statsummary['ppmPErr_ave'] = pd.Series(ppmPErr_ave)
statsummary['vcd_ave'] = pd.Series(vcd_ave)
statsummary['vcdErr_ave'] = pd.Series(vcdErr_ave)
statsummary['vcdPErr_ave'] = pd.Series(vcdPErr_ave)
statsummary['csq_ave'] = pd.Series(csq_ave)
statsummary['dofs_ave'] = pd.Series(dofs_ave)

ppm_vals.columns = [str(i) for i in values]
ppm_err_vals.columns = [str(i) for i in values]
vcd_vals.columns = [str(i) for i in values]
vcd_err_vals.columns = [str(i) for i in values]
    
ppm_vals['std'] = ppm_vals.std(axis=1)
ppm_vals['mean'] = ppm_vals.mean(axis=1)
ppm_err_vals['std'] = ppm_err_vals.std(axis=1)
ppm_err_vals['mean'] = ppm_err_vals.mean(axis=1)
vcd_vals['std'] = vcd_vals.std(axis=1)
vcd_vals['mean'] = vcd_vals.mean(axis=1)
vcd_err_vals['std'] = vcd_err_vals.std(axis=1)
vcd_err_vals['mean'] = vcd_err_vals.mean(axis=1)
prof_err_vals['std'] = prof_err_vals.std(axis=1)
prof_vals['std'] = prof_vals.std(axis=1)
prof_err_vals['mean'] = prof_err_vals.mean(axis=1)
prof_vals['mean'] = prof_vals.mean(axis=1)
ppm_vals['Date_Time'] = concfile['Date_Time']
ppm_vals = ppm_vals[ppm_vals.Date_Time.notnull()]
ppm_err_vals['Date_Time'] = concfile['Date_Time']
ppm_err_vals = ppm_err_vals[ppm_err_vals.Date_Time.notnull()]
vcd_vals['Date_Time'] = concfile['Date_Time']
vcd_vals = vcd_vals[vcd_vals.Date_Time.notnull()]
vcd_err_vals['Date_Time'] = concfile['Date_Time']
vcd_err_vals = vcd_err_vals[vcd_err_vals.Date_Time.notnull()]

# Calculate mean standard deviations for concentrations and profiles
prof_avg_std = prof_vals['std'].mean()
prof_avg_avg = prof_vals['mean'].mean()
ppm_avg_std = ppm_vals['std'].mean()
ppm_avg_avg = ppm_vals['mean'].mean()
ppm_avg_std_err = ppm_err_vals['std'].mean()
ppm_avg_avg_err = ppm_err_vals['mean'].mean()
vcd_avg_std = "{:.5E}".format(Decimal(vcd_vals['std'].mean()))
vcd_avg_avg = "{:.5E}".format(Decimal(vcd_vals['mean'].mean()))
vcd_avg_std_err = "{:.5E}".format(Decimal(vcd_err_vals['std'].mean()))
vcd_avg_avg_err = "{:.5E}".format(Decimal(vcd_err_vals['mean'].mean()))

#%%
statsummary.to_csv(path+tg+'_'+testset+'_resultplots/apriori_tests_statsummary.txt', sep = '\t', index=False)
vcd_vals.to_csv(path+tg+'_'+testset+'_resultplots/apriori_tests_diurnalVCD.txt', sep = '\t', index=False)
vcd_err_vals.to_csv(path+tg+'_'+testset+'_resultplots/apriori_tests_diurnalVCDerrors.txt', sep = '\t', index=False)
ppm_vals.to_csv(path+tg+'_'+testset+'_resultplots/apriori_tests_diurnalppm.txt', sep = '\t', index=False)
ppm_err_vals.to_csv(path+tg+'_'+testset+'_resultplots/apriori_tests_diurnalppmerrors.txt', sep = '\t', index=False)
prof_vals.to_csv(path+tg+'_'+testset+'_resultplots/apriori_tests_profiledetails.txt', sep = '\t', index=False)
prof_err_vals.to_csv(path+tg+'_'+testset+'_resultplots/apriori_tests_profileErrors.txt', sep = '\t', index=False)
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
fig1 = plt.figure(figsize=figsize)
ax=fig.add_subplot(111)
ax1=fig1.add_subplot(111)
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
    x = np.array((vcd_vals['Date_Time']))
    y = np.array((vcd_vals[j]))
    z = np.array((ppm_vals[j]))
    yerr = np.array((vcd_err_vals[j]))
    zerr = np.array((ppm_err_vals[j]))
    ax.errorbar(x,y,yerr=yerr,color=colours[c])
    ax1.errorbar(x,z,yerr=zerr,color=colours[c])
    c = c+1
ax.legend(strings, fontsize=fontsize, loc=2, bbox_to_anchor=(1,1))
ax.set_xlabel('Time', fontsize=fontsize)
ax.set_ylabel(tg+' VCD', fontsize=fontsize)
ax1.legend(strings, fontsize=fontsize, loc=2, bbox_to_anchor=(1,1))
ax1.set_xlabel('Time', fontsize=fontsize)
ax1.set_ylabel(tg+' surface conc. (ppm)', fontsize=fontsize)
fig.savefig(path+tg+'_'+testset+'_resultplots/'+tg+'_'+testset+'_vcd.png', bbox_to_anchor='tight')    
fig1.savefig(path+tg+'_'+testset+'_resultplots/'+tg+'_'+testset+'_ppm.png', bbox_to_anchor='tight')    

#%%
# Plot the stats summaries

y1 = 'csq_ave'
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
fg.savefig(path+tg+'_'+testset+'_resultplots/'+y1+'_'+y2+'.png', 
                  bbox_inches='tight')

