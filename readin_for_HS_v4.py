# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Import section
#=====================================================================================================================
import glob
import pandas as pd
import matplotlib.pyplot as plt

#days = ['18', '19', '20', '21']
days = ['19']
month = '02'
year_long = '2017'
year = '17'

save_temp_info = True

#folderpath = 'E:\\PhD\\Broady_data_backup\\UniMelb\\broady_data_rr\\HS_1-30-MAR\\'
#folderpath = 'F:/PhD/Broady_data_backup/UniMelb/broady_data_rr/SP2017a/U/HS_1-8-MAR/'
folderpath = 'E:\\PhD\\Broady_data_backup\\NIWA\\spectra\\NZ_linefiles_U\\NZ_HS and Cal files\\'
for d in days:
    # SECTION TO IMPORT THE HORIZON SCAN (HS) DATA
    #=====================================================================================================================

    day = d
    print('now looking at '+day+'/'+month+'/'+year_long)
    folder2lookat = 'NZ_HS_'+day+month+year
    date = day+month+year   # this date is just used for saving later on

    files = glob.glob(folderpath+folder2lookat + "/*.txt")

    # create empty list to put all the data in
    file_data_strpd = []
    file_data_split = []
    newdf = pd.DataFrame()

    for file_ in files:
        f = open(file_, 'r')
        file_data = f.readlines()
    
        for i in range(len(file_data)):
            file_data_strpd.append(file_data[i].strip('\n'))
        for i in range(len(file_data_strpd)):
            file_data_split.append(file_data_strpd[i].split(' '))

    #print(file_data_strpd)
        
    readin = pd.DataFrame(file_data_split)
    readin.columns = ['SZA', 'Azimuth', 'EA', 'Date', 'time', 'norm_ave_int', 'norm_int_1094']
    readin[['SZA', 'Azimuth', 'EA', 'time', 'norm_ave_int', 
        'norm_int_1094']] = readin[['SZA', 'Azimuth', 'EA', 'time', 'norm_ave_int', 'norm_int_1094']].astype(float)

    # Drop all the values where the Elevation angle is out of range
    readin = readin.drop(readin[readin.EA > 10].index)
    
    # create time-based horizon scan sets

    # time to complete EA horizon scan sets is less than 0.3 in terms of decimal time
    # time between EA horizon scan sets is more than 0.8 in terms of decimal time

    a23 = readin[readin['time']>23]     # Take out the 23 hr data
    if len(a23)>0:
        a23_grad = pd.DataFrame((a23.norm_ave_int.diff(periods=1))/(a23.EA.diff(periods=1)))
        a23_grad_t = a23_grad.transpose()
        EAs = pd.DataFrame(a23.EA)
        EAs_t = EAs.transpose()
        a23_grad_dft = EAs_t.append(a23_grad_t)
        a23_grad_df = a23_grad_dft.transpose()
        a23_grad_df.columns = ['EA', 'grad']

    b23 = readin[readin['time']<23]     # Then cut the dataframe down incrementally
    a22 = b23[b23['time']>22]

    if len(a22)>0:
        a22_grad = pd.DataFrame((a22.norm_ave_int.diff(periods=1))/(a22.EA.diff(periods=1)))
        a22_grad_t = a22_grad.transpose()
        EAs = pd.DataFrame(a22.EA)
        EAs_t = EAs.transpose()
        a22_grad_dft = EAs_t.append(a22_grad_t)
        a22_grad_df = a22_grad_dft.transpose()
        a22_grad_df.columns = ['EA', 'grad']

    b22 = b23[b23['time']<22]
    a21 = b22[b22['time']>20]

    if len(a21)>0:
        a21_grad = pd.DataFrame((a21.norm_ave_int.diff(periods=1))/(a21.EA.diff(periods=1)))
        a21_grad_t = a21_grad.transpose()
        EAs = pd.DataFrame(a21.EA)
        EAs_t = EAs.transpose()
        a21_grad_dft = EAs_t.append(a21_grad_t)
        a21_grad_df = a21_grad_dft.transpose()
        a21_grad_df.columns = ['EA', 'grad']

    b21 = b22[b22['time']<20]
    a8 = b21[b21['time']>8]

    if len(a8)>0:
        a8_grad = pd.DataFrame((a8.norm_ave_int.diff(periods=1))/(a8.EA.diff(periods=1)))
        a8_grad_t = a8_grad.transpose()
        EAs = pd.DataFrame(a8.EA)
        EAs_t = EAs.transpose()
        a8_grad_dft = EAs_t.append(a8_grad_t)
        a8_grad_df = a8_grad_dft.transpose()
        a8_grad_df.columns = ['EA', 'grad']

    b8 = b21[b21['time']<8]
    a7 = b8[b8['time']>7]

    if len(a7) >0: 
        a7_grad = pd.DataFrame((a7.norm_ave_int.diff(periods=1))/(a7.EA.diff(periods=1)))
        a7_grad_t = a7_grad.transpose()
        EAs = pd.DataFrame(a7.EA)
        EAs_t = EAs.transpose()
        a7_grad_dft = EAs_t.append(a7_grad_t)
        a7_grad_df = a7_grad_dft.transpose()
        a7_grad_df.columns = ['EA', 'grad']

    b7 = b8[b8['time']<7]
    a6 = b7[b7['time']>6]

    if len(a6)>0:
        a6_grad = pd.DataFrame((a6.norm_ave_int.diff(periods=1))/(a6.EA.diff(periods=1)))
        a6_grad_t = a6_grad.transpose()
        EAs = pd.DataFrame(a6.EA)
        EAs_t = EAs.transpose()
        a6_grad_dft = EAs_t.append(a6_grad_t)
        a6_grad_df = a6_grad_dft.transpose()
        a6_grad_df.columns = ['EA', 'grad']

    b6 = b7[b7['time']<6]
    a5 = b6[b6['time']>5]

    if len(a5)>0:
        a5_grad = pd.DataFrame((a5.norm_ave_int.diff(periods=1))/(a5.EA.diff(periods=1)))
        a5_grad_t = a5_grad.transpose()
        EAs = pd.DataFrame(a5.EA)
        EAs_t = EAs.transpose()
        a5_grad_dft = EAs_t.append(a5_grad_t)
        a5_grad_df = a5_grad_dft.transpose()
        a5_grad_df.columns = ['EA', 'grad']

    b5 = b6[b6['time']<5]
    a4 = b5[b5['time']>4]

    if len(a4)>0:
        a4_grad = pd.DataFrame((a4.norm_ave_int.diff(periods=1))/(a4.EA.diff(periods=1)))
        a4_grad_t = a4_grad.transpose()
        EAs = pd.DataFrame(a4.EA)
        EAs_t = EAs.transpose()
        a4_grad_dft = EAs_t.append(a4_grad_t)
        a4_grad_df = a4_grad_dft.transpose()
        a4_grad_df.columns = ['EA', 'grad']

    b4 = b5[b5['time']<4]
    a3 = b4[b4['time']>3]

    if len(a3)>0:
        a3_grad = pd.DataFrame((a3.norm_ave_int.diff(periods=1))/(a3.EA.diff(periods=1)))
        a3_grad_t = a3_grad.transpose()
        EAs = pd.DataFrame(a3.EA)
        EAs_t = EAs.transpose()
        a3_grad_dft = EAs_t.append(a3_grad_t)
        a3_grad_df = a3_grad_dft.transpose()
        a3_grad_df.columns = ['EA', 'grad']

    b3 = b4[b4['time']<3]
    a2 = b3[b3['time']>2]

    if len(a2)>0:
        a2_grad = pd.DataFrame((a2.norm_ave_int.diff(periods=1))/(a2.EA.diff(periods=1)))
        a2_grad_t = a2_grad.transpose()
        EAs = pd.DataFrame(a2.EA)
        EAs_t = EAs.transpose()
        a2_grad_dft = EAs_t.append(a2_grad_t)
        a2_grad_df = a2_grad_dft.transpose()
        a2_grad_df.columns = ['EA', 'grad']

    b2 = b3[b3['time']<2]
    a1 = b2[b2['time']>1]

    if len(a1)>0:
        a1_grad = pd.DataFrame((a1.norm_ave_int.diff(periods=1))/(a1.EA.diff(periods=1)))
        a1_grad_t = a1_grad.transpose()
        EAs = pd.DataFrame(a1.EA)
        EAs_t = EAs.transpose()
        a1_grad_dft = EAs_t.append(a1_grad_t)
        a1_grad_df = a1_grad_dft.transpose()
        a1_grad_df.columns = ['EA', 'grad']

    b1 = b2[b2['time']<1]
    a0 = b1[b1['time']>0]

    if len(a0)>0:
        a0_grad = pd.DataFrame((a0.norm_ave_int.diff(periods=1))/(a0.EA.diff(periods=1)))
        a0_grad_t = a0_grad.transpose()
        EAs = pd.DataFrame(a0.EA)
        EAs_t = EAs.transpose()
        a0_grad_dft = EAs_t.append(a0_grad_t)
        a0_grad_df = a0_grad_dft.transpose()
        a0_grad_df.columns = ['EA', 'grad']
        
    # create lists for saving critical information into:
    # ==============================================================
    hs_EA_info = []
    hs_time_info = []
    #.... where the EA and time are at the max. gradient position

    # Then do the plotting
    # ==============================================================
    plot = plt.figure()
    figsize = (5,3)
    fontsize = 14
    legpos = (0.5,0.3)

    whattoplot = 'norm_ave_int'
    style = 'bo'
    gradstyle = 'r--'
    xlim = [-6, 6]

    if len(a0) > 0:
        maxint = a0.norm_ave_int.max() + 0.15*(a0.norm_ave_int.max())
        minint = a0.norm_ave_int.min() - 0.15*(a0.norm_ave_int.max())
        g = a0.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 0 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a0_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax0 = a0_grad_df.grad.idxmax()
        pkpos0 = a0_grad_df.EA[gradmax0]
        g.axvline(pkpos0, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime0 = a0.time[gradmax0]
        g.legend(['data', 'grad, max at '+str(pkpos0)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/0utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
        
        hs_EA_info.append(pkpos0)
        hs_time_info.append(pktime0)

    if len(a1) > 0:
        maxint = a1.norm_ave_int.max() + 0.15*(a1.norm_ave_int.max())
        minint = a1.norm_ave_int.min() - 0.15*(a1.norm_ave_int.max())
        g = a1.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 1 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a1_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax1 = a1_grad_df.grad.idxmax()
        pkpos1 = a1_grad_df.EA[gradmax1]
        g.axvline(pkpos1, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime1 = a1.time[gradmax1]
        g.legend(['data', 'grad, max at '+str(pkpos0)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/1utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos1)
        hs_time_info.append(pktime1) 
    
    if len(a2) > 0:
        maxint = a2.norm_ave_int.max() + 0.15*(a2.norm_ave_int.max())
        minint = a2.norm_ave_int.min() - 0.15*(a2.norm_ave_int.max())
        g = a2.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 2 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a2_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax2 = a2_grad_df.grad.idxmax()
        pkpos2 = a2_grad_df.EA[gradmax2]
        g.axvline(pkpos2, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime2 = a2.time[gradmax2]
        g.legend(['data', 'grad, max at '+str(pkpos2)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/2utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos2)
        hs_time_info.append(pktime2)  
    
    if len(a3) > 0:
        maxint = a3.norm_ave_int.max() + 0.15*(a3.norm_ave_int.max())
        minint = a3.norm_ave_int.min() - 0.15*(a3.norm_ave_int.max())
        g = a3.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 3 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a3_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax3 = a3_grad_df.grad.idxmax()
        pkpos3 = a3_grad_df.EA[gradmax3]
        g.axvline(pkpos3, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime3 = a3.time[gradmax3]
        g.legend(['data', 'grad, max at '+str(pkpos3)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/3utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos3)
        hs_time_info.append(pktime3)
    
    if len(a4) > 0:
        maxint = a4.norm_ave_int.max() + 0.15*(a4.norm_ave_int.max())
        minint = a4.norm_ave_int.min() - 0.15*(a4.norm_ave_int.max())
        g = a4.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 4 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a4_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax4 = a4_grad_df.grad.idxmax()
        pkpos4 = a4_grad_df.EA[gradmax4]
        g.axvline(pkpos4, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime4 = a4.time[gradmax4]
        g.legend(['data', 'grad, max at '+str(pkpos4)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/4utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos4)
        hs_time_info.append(pktime4)
    
    if len(a5) > 0:
        maxint = a5.norm_ave_int.max() + 0.15*(a5.norm_ave_int.max())
        minint = a5.norm_ave_int.min() - 0.15*(a5.norm_ave_int.max())
        g = a5.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 5 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a5_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax5 = a5_grad_df.grad.idxmax()
        pkpos5 = a5_grad_df.EA[gradmax5]
        g.axvline(pkpos5, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime5 = a5.time[gradmax5]
        g.legend(['data', 'grad, max at '+str(pkpos5)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/5utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos5)
        hs_time_info.append(pktime5)
    
    if len(a6) > 0:
        maxint = a6.norm_ave_int.max() + 0.15*(a6.norm_ave_int.max())
        minint = a6.norm_ave_int.min() - 0.15*(a6.norm_ave_int.max())
        g = a6.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 6 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a6_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax6 = a6_grad_df.grad.idxmax()
        pkpos6 = a6_grad_df.EA[gradmax6]
        g.axvline(pkpos6, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime6 = a6.time[gradmax6]
        g.legend(['data', 'grad, max at '+str(pkpos6)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/6utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos6)
        hs_time_info.append(pktime6)
    
    if len(a7) > 0:
        maxint = a7.norm_ave_int.max() + 0.15*(a7.norm_ave_int.max())
        minint = a7.norm_ave_int.min() - 0.15*(a7.norm_ave_int.max())
        g = a7.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 7 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a7_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax7 = a7_grad_df.grad.idxmax()
        pkpos7 = a7_grad_df.EA[gradmax7]
        g.axvline(pkpos7, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime7 = a7.time[gradmax7]
        g.legend(['data', 'grad, max at '+str(pkpos7)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/7utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos7)
        hs_time_info.append(pktime7) 
    
    if len(a8) > 0:
        maxint = a8.norm_ave_int.max() + 0.15*(a8.norm_ave_int.max())
        minint = a8.norm_ave_int.min() - 0.15*(a8.norm_ave_int.max())
        g = a8.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 8 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a8_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax8 = a8_grad_df.grad.idxmax()
        pkpos8 = a8_grad_df.EA[gradmax8]
        g.axvline(pkpos8, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime8 = a8.time[gradmax8]
        g.legend(['data', 'grad, max at '+str(pkpos8)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/8utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos8)
        hs_time_info.append(pktime8)
    
    if len(a21) > 0:
        maxint = a21.norm_ave_int.max() + 0.15*(a21.norm_ave_int.max())
        minint = a21.norm_ave_int.min() - 0.15*(a21.norm_ave_int.max())
        g = a21.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 21 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a21_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax21 = a21_grad_df.grad.idxmax()
        pkpos21 = a21_grad_df.EA[gradmax21]
        g.axvline(pkpos21, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime21 = a21.time[gradmax21]
        g.legend(['data', 'grad, max at '+str(pkpos21)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/21utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos21)
        hs_time_info.append(pktime21)
    
    if len(a22) > 0:
        maxint = a22.norm_ave_int.max() + 0.15*(a22.norm_ave_int.max())
        minint = a22.norm_ave_int.min() - 0.15*(a22.norm_ave_int.max())
        g = a22.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 22 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a22_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax22 = a22_grad_df.grad.idxmax()
        pkpos22 = a22_grad_df.EA[gradmax22]
        g.axvline(pkpos22, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime22 = a22.time[gradmax22]
        g.legend(['data', 'grad, max at '+str(pkpos22)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/22utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
           
        hs_EA_info.append(pkpos22)
        hs_time_info.append(pktime22)
    
    if len(a23) > 0:
        maxint = a23.norm_ave_int.max() + 0.15*(a23.norm_ave_int.max())
        minint = a23.norm_ave_int.min() - 0.15*(a23.norm_ave_int.max())
        g = a23.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[minint, maxint],
                xlim=xlim, style=style, figsize=figsize)
        g.set_title('Horizon scan 23 hrs '+date, fontsize=fontsize)
        g.set_xlabel('Elevation angle', fontsize=fontsize)
        g.set_ylabel('Norm. ave. intensity', fontsize=fontsize)
        #a23_grad_df.plot(x='EA', y='grad', ax=g, style=gradstyle, xlim=xlim)
        gradmax23 = a23_grad_df.grad.idxmax()
        pkpos23 = a23_grad_df.EA[gradmax23]
        g.axvline(pkpos23, color='r', linestyle='--', ymax=maxint, ymin=minint)
        pktime23 = a23.time[gradmax23]
        g.legend(['data', 'grad, max at '+str(pkpos23)], bbox_to_anchor=legpos)
        
        fig = g.get_figure()
        fig.savefig(folderpath+folder2lookat+'/23utc_hs_'+date+'.png', bbox_inches='tight')    
        plt.close(fig)  
       
        hs_EA_info.append(pkpos23)
        hs_time_info.append(pktime23) 
        
    # PLOT ALL THE DATA FROM THE DAY TOGETHER
    # ============================================
    plt.style.use(['bmh','seaborn-whitegrid'])

    h = a0.plot(x='EA', y=whattoplot, fontsize=fontsize, ylim=[-200, 10000],
                xlim=(-4,4), figsize=figsize, style='.')
    h.set_title('Horizon scans '+date, fontsize=fontsize)
    h.set_xlabel('Elevation angle', fontsize=fontsize)
    h.set_ylabel('Norm. ave. intensity', fontsize=fontsize)

    a1.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    a2.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    a3.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    a4.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    a5.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    a6.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    a7.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    a8.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    #a21.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    #a22.plot(x='EA', y=whattoplot, xlim=(-4,4), ax=h, style='.')
    #a23.plot(x='EA', y=whattoplot, ax=h, style='.')

    h.legend(['11','12','13','14','15','16','17', '18'], bbox_to_anchor=(1.3,1.04))
    fig = h.get_figure()
    fig.savefig(folderpath+folder2lookat+'/all_hs_'+date+'.png', bbox_inches='tight')
    plt.close(fig)  
    
    def to_hrs(s):
        hr, mins, sec = [float(x) for x in s.split(':')]
        return hr+(mins/60)+(sec/3600)
    
    # SECTION TO IMPORT THE TELESCOPE TEMPERATURE DATA
    #=====================================================================================================================
    if save_temp_info == True:
        temp_log = 'E:\\PhD\\Broady_data_backup\\NIWA\\log\\NZ_Templog_15-22Feb2017\\Temperature'+year+month+day+'.log'
        temp_df = pd.read_csv(temp_log,  header=1, sep = ';')
        temp_df.columns = ['Date', 'Time', 'AM_PM', 'Pressure', 'T_Electronics', 'T_Spectrometer',
                   'T_Telescope', 'T2', 'T_Ambient', 'PowerOut']

        temp_df['date_time'] = temp_df['Date'].map(str) + ' ' + temp_df['Time'] + ' ' + temp_df['AM_PM']
        temp_df['date_time'] = pd.to_datetime(temp_df['date_time'])

        #temp_df['hours'] =temp_df.date_time.apply(lambda x: x.minute) 

        # Create decimal time column in the temp data frame
        # =================================================


        temp_df['dec_time'] = [to_hrs(i) for i in temp_df['Time']]

        for idx, row in temp_df.iterrows():
            if temp_df['AM_PM'][idx] == 'AM' and temp_df['dec_time'][idx] > 12:
                temp_df['dec_time'][idx] = (temp_df['dec_time'][idx] - 12)
            elif temp_df['AM_PM'][idx] == 'PM':
                temp_df['dec_time'][idx] = (temp_df['dec_time'][idx] + 12)


        hs_temp_info = []
        t_of_interest = 'T_Ambient'
        for idx, row in temp_df.iterrows():
            if (pktime0 - 0.01) < temp_df['dec_time'][idx] < (pktime0 + 0.01):
                temp_idx0 = temp_df[t_of_interest][idx]
            if (pktime1 - 0.01) < temp_df['dec_time'][idx] < (pktime1 + 0.01):
                temp_idx1 = temp_df[t_of_interest][idx]
            if (pktime2 - 0.01) < temp_df['dec_time'][idx] < (pktime2 + 0.01):
                temp_idx2 = temp_df[t_of_interest][idx]
            if (pktime3 - 0.01) < temp_df['dec_time'][idx] < (pktime3 + 0.01):
                temp_idx3 = temp_df[t_of_interest][idx]
            if (pktime4 - 0.01) < temp_df['dec_time'][idx] < (pktime4 + 0.01):
                temp_idx4 = temp_df[t_of_interest][idx]
            if (pktime5 - 0.01) < temp_df['dec_time'][idx] < (pktime5 + 0.01):
                temp_idx5 = temp_df[t_of_interest][idx]
            if (pktime6 - 0.01) < temp_df['dec_time'][idx] < (pktime6 + 0.01):
                temp_idx6 = temp_df[t_of_interest][idx]
            if (pktime7 - 0.01) < temp_df['dec_time'][idx] < (pktime7 + 0.01):
                temp_idx7 = temp_df[t_of_interest][idx]
            if (pktime8 - 0.01) < temp_df['dec_time'][idx] < (pktime8 + 0.01):
                temp_idx8 = temp_df[t_of_interest][idx]
            if (pktime21 - 0.01) < ((temp_df['dec_time'][idx])) < (pktime21 + 0.01):
                temp_idx21 = temp_df[t_of_interest][idx]
            if (pktime22 - 0.01) < ((temp_df['dec_time'][idx])) < (pktime22 + 0.01):
                temp_idx22 = temp_df[t_of_interest][idx]
            if (pktime23 - 0.01) < ((temp_df['dec_time'][idx])) < (pktime23 + 0.01):
                temp_idx23 = temp_df[t_of_interest][idx]

        hs_temp_info.append(temp_idx0)
        hs_temp_info.append(temp_idx1)
        hs_temp_info.append(temp_idx2)
        hs_temp_info.append(temp_idx3)
        hs_temp_info.append(temp_idx4)
        hs_temp_info.append(temp_idx5)
        hs_temp_info.append(temp_idx6)
        hs_temp_info.append(temp_idx7)
        hs_temp_info.append(temp_idx8)
        hs_temp_info.append(temp_idx21)
        hs_temp_info.append(temp_idx22)
        hs_temp_info.append(temp_idx23)

        hs_EA_info_df = pd.DataFrame(hs_EA_info)
        hs_EA_info_dft = hs_EA_info_df.transpose()

        hs_time_info_df = pd.DataFrame(hs_time_info)
        hs_time_info_dft = hs_time_info_df.transpose()

        hs_temp_info_df = pd.DataFrame(hs_temp_info)
        hs_temp_info_dft = hs_temp_info_df.transpose()

        hs_info_dft1 = hs_time_info_dft.append(hs_EA_info_dft)
        hs_info_dft = hs_info_dft1.append(hs_temp_info_dft)
        hs_info_df = hs_info_dft.transpose()

        #Save the info to text file
        # ==========================
        hs_info_df.to_csv(folderpath+'gradmax_info_'+day+month+year+'-1.txt', sep=' ',
                      header=False)
    else:
        continue
    
    